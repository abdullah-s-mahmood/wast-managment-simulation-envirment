#!/usr/bin/env python3
"""Fresh pinned ns-3 core build and 1ns installation/linkage reference probe.

This executes an independently obtained upstream dependency, never the designated
legacy archive. No network model or physical accuracy is accepted by this probe.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import signal
import subprocess
import sys
import tarfile
import time
from pathlib import Path, PurePosixPath
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROFILE = ROOT / "docs/tooling/S020_NS3_PROFILE.json"
FIXTURE = ROOT / "tests/fixtures/ns3_installation_smoke.cc"
OFF_FEATURES = ("NS3_EXAMPLES", "NS3_TESTS", "NS3_PYTHON_BINDINGS", "NS3_ENABLE_BUILD_VERSION", "NS3_CCACHE", "NS3_PRECOMPILE_HEADERS", "NS3_VISUALIZER", "NS3_GSL", "NS3_SQLITE", "NS3_EIGEN")


class BuildRejected(RuntimeError):
    """A failed/incomplete installation is not readiness or model validation."""


def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Reject duplicate contract/result keys."""
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise BuildRejected("duplicate JSON field")
        result[key] = value
    return result


def read_profile(path: Path) -> dict[str, Any]:
    """Validate reviewed release/configuration and resource bounds, no defaults."""
    data = json.loads(path.read_bytes(), object_pairs_hook=unique)
    if not isinstance(data, dict) or set(data) != {"schema_version", "release", "archive", "toolchain_minimums", "build", "budgets", "expected", "fixture_sha256", "scientific_validation", "simulator_support_verified"} or type(data["schema_version"]) is not int or data["schema_version"] != 1:
        raise BuildRejected("unsupported ns-3 profile schema")
    if data["release"] != "3.47" or data["scientific_validation"] != "UNVALIDATED" or data["simulator_support_verified"] is not False:
        raise BuildRejected("unapproved ns-3 release or clearance claim")
    archive = data["archive"]
    if archive != {"url": "https://www.nsnam.org/releases/ns-3.47.tar.bz2", "size_bytes": 42929716, "sha256": "8b3adca956c834ea436b915986ab8fd053e90041acae7426895d595aaa3ccc39", "publisher_sha1": "897c3f2db2c6de6a8291e46b3020dbeb1af75269"} or type(archive.get("size_bytes")) is not int:
        raise BuildRejected("unapproved upstream source identity")
    if data["toolchain_minimums"] != {"gcc": "11.1", "cmake": "3.20", "ninja": "1.10"} or data["build"] != {"type": "Release", "modules": ["core"], "parallel_jobs": 2, "examples": False, "upstream_tests": False, "python_bindings": False}:
        raise BuildRejected("unreviewed compiler/build scope")
    if any(type(data["build"][key]) is not bool for key in ("examples", "upstream_tests", "python_bindings")) or type(data["build"]["parallel_jobs"]) is not int:
        raise BuildRejected("invalid build flag types")
    maxima = {"archive_members": 20000, "member_bytes": 33554432, "uncompressed_bytes": 536870912, "configure_seconds": 120, "build_seconds": 600, "command_seconds": 10, "minimum_free_bytes": 1073741824}
    budgets = data["budgets"]
    if not isinstance(budgets, dict) or set(budgets) != set(maxima) or any(type(v) is not int or not 1 <= v <= maxima[k] for k, v in budgets.items()):
        raise BuildRejected("invalid or unbounded resource budget")
    if data["fixture_sha256"] != hashlib.sha256(FIXTURE.read_bytes()).hexdigest() or data["expected"] != {"status": "NS3_CORE_SMOKE_PASS", "event_time_ns": 1} or type(data["expected"]["event_time_ns"]) is not int:
        raise BuildRejected("fixture/reference contract disagreement")
    return cast(dict[str, Any], data)


def version_at_least(observed: str, minimum: str) -> None:
    """Compare numeric release tuples; reject unknown/prerelease tool strings."""
    if re.fullmatch(r"\d+\.\d+(?:\.\d+)?", observed) is None or re.fullmatch(r"\d+\.\d+(?:\.\d+)?", minimum) is None:
        raise BuildRejected("unrecognized tool version")
    actual = tuple(map(int, observed.split("."))) + (0,) * (3 - len(observed.split(".")))
    required = tuple(map(int, minimum.split("."))) + (0,) * (3 - len(minimum.split(".")))
    if actual < required:
        raise BuildRejected("tool version below release requirement")


def verify_archive(path: Path, config: dict[str, Any]) -> str:
    """Check full size and SHA256 before extraction/execution; never substitute."""
    if path.stat().st_size != config["archive"]["size_bytes"]:
        raise BuildRejected("upstream source size mismatch")
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    if digest != config["archive"]["sha256"]:
        raise BuildRejected("upstream source SHA256 mismatch")
    return digest


def reserve_work(path: Path) -> None:
    """Reject stale caches/evidence/symlinks rather than overwrite prior work."""
    if path.exists() or path.is_symlink():
        raise BuildRejected("stale/existing work or build cache; preserve and choose a fresh owned directory")
    path.mkdir(parents=True)


def require_tool(path: Path) -> Path:
    """Require explicit installed tool path; do not silently select a fallback."""
    if not path.is_file() or not os.access(path, os.X_OK):
        raise BuildRejected("missing tool (" + path.name + "); install supported compiler/CMake/Ninja or pass its explicit path")
    return path.resolve()


def clean_environment(original: dict[str, str]) -> dict[str, str]:
    """Ignore inherited build/runtime overrides; this is not a host sandbox."""
    return {k: v for k, v in original.items() if not k.startswith(("PYTHON", "PIP_", "UV_", "CMAKE_", "NS3_")) and k not in {"CC", "CXX", "CFLAGS", "CXXFLAGS", "CPPFLAGS", "LDFLAGS", "LD_LIBRARY_PATH", "LD_PRELOAD", "VIRTUAL_ENV", "CONDA_PREFIX", "CPATH", "CPLUS_INCLUDE_PATH", "LIBRARY_PATH", "PKG_CONFIG_PATH"}}


def checked(command: list[str], log: Path, env: dict[str, str], timeout: float) -> None:
    """Log actual status; bound the Linux group and reap the direct child."""
    started = time.monotonic()
    with log.open("w") as stream:
        process = subprocess.Popen(command, cwd=log.parent, env=env, stdin=subprocess.DEVNULL, stdout=stream, stderr=subprocess.STDOUT, start_new_session=True)
        try:
            process.wait(timeout=timeout)
            status = "EXITED"
        except subprocess.TimeoutExpired:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.wait()
            status = "TIMED_OUT_KILLED_REAPED"
    log.with_suffix(".command.json").write_text(json.dumps({"argv": command, "exit_code": process.returncode, "status": status, "wall_seconds": time.monotonic() - started}, indent=2) + "\n")
    if status != "EXITED" or process.returncode:
        raise BuildRejected("build/run command failed or timed out; inspect retained private command/log")


def preflight(archive: Path, config: dict[str, Any], destination: Path) -> list[tarfile.TarInfo]:
    """Bound regular/within-root dependency members before data-filter extraction."""
    members: list[tarfile.TarInfo] = []
    seen: set[str] = set()
    total = 0
    started = time.monotonic()
    try:
        with tarfile.open(archive, "r:bz2") as source:
            for member in source:
                name = PurePosixPath(member.name)
                total += member.size
                if name.is_absolute() or ".." in name.parts or not name.parts or name.parts[0] != "ns-3.47" or str(name) in seen or not (member.isfile() or member.isdir() or member.issym() or member.islnk()):
                    raise BuildRejected("unsafe/duplicate source archive member")
                if len(members) >= config["budgets"]["archive_members"] or member.size > config["budgets"]["member_bytes"] or total > config["budgets"]["uncompressed_bytes"] or time.monotonic() - started > config["budgets"]["configure_seconds"]:
                    raise BuildRejected("source archive resource budget exceeded")
                tarfile.data_filter(member, str(destination))
                seen.add(str(name))
                members.append(member)
    except (tarfile.TarError, ValueError) as exc:
        raise BuildRejected("source archive malformed or unsafe link") from exc
    return members


def check_cache(path: Path, source: Path, compiler: Path) -> None:
    """Verify actual CMake source/compiler/module/build values without duplicates."""
    expected = {"CMAKE_HOME_DIRECTORY": str(source), "CMAKE_CXX_COMPILER": str(compiler), "NS3_ENABLED_MODULES": "core", "CMAKE_BUILD_TYPE": "Release"}
    expected.update({key: "OFF" for key in OFF_FEATURES})
    found: dict[str, str] = {}
    for line in path.read_text().splitlines():
        match = re.match(r"([^:#]+):[^=]+=(.*)$", line)
        if match and match[1] in expected:
            if match[1] in found:
                raise BuildRejected("duplicate build-cache contract value")
            if match[1] in OFF_FEATURES and ":BOOL=" not in line:
                raise BuildRejected("unrecognized/unused feature-disable option in cache")
            found[match[1]] = match[2]
    if found != expected:
        raise BuildRejected("stale/foreign compiler, source, modules or build profile in cache")


def check_output(config: dict[str, Any], text: str) -> None:
    """Exact software reference: one event observed at1ns, not physical evidence."""
    try:
        data = json.loads(text, object_pairs_hook=unique)
    except ValueError as exc:
        raise BuildRejected("invalid/incomplete execution output") from exc
    if not isinstance(data, dict) or data != config["expected"] or type(data.get("event_time_ns")) is not int:
        raise BuildRejected("ns-3 execution differs from the exact1ns reference")


def build(config: dict[str, Any], archive: Path, work: Path, compiler: Path, cmake: Path, ninja: Path) -> dict[str, object]:
    """Build only verified upstream core, then compile/run the independent probe."""
    if sys.flags.isolated != 1 or sys.implementation.name != "cpython" or ".".join(map(str, sys.version_info[:3])) != (ROOT / ".python-version").read_text().strip() or Path(sys.prefix).resolve() != (ROOT / ".venv").resolve() or sys.prefix == sys.base_prefix:
        raise BuildRejected("use S018 isolated pinned project Python for orchestration")
    if platform.system() != "Linux" or platform.machine() != "x86_64":
        raise BuildRejected("S020 installation profile is Linux x86_64 only; other platforms NOT_RUN")
    compiler, cmake, ninja = require_tool(compiler), require_tool(cmake), require_tool(ninja)
    verify_archive(archive, config)
    reserve_work(work)
    if shutil.disk_usage(work).free < config["budgets"]["minimum_free_bytes"]:
        raise BuildRejected("insufficient free space; preserve evidence and review resource budget")
    if (Path.home() / ".ns3rc").exists():
        raise BuildRejected("ambient .ns3rc requires review; do not silently inherit or replace it")
    env = clean_environment(dict(os.environ))
    env["LC_ALL"] = "C"
    tools: dict[str, str] = {}
    for name, executable, arguments in (("gcc", compiler, ["-dumpfullversion", "-dumpversion"]), ("cmake", cmake, ["--version"]), ("ninja", ninja, ["--version"])):
        log = work / (name + "-version.log")
        checked([str(executable), *arguments], log, env, config["budgets"]["command_seconds"])
        version = log.read_text().splitlines()[0]
        if name == "cmake":
            version = version.removeprefix("cmake version ")
        version_at_least(version, config["toolchain_minimums"][name])
        tools[name] = version
    checked([str(compiler), "--version"], work / "compiler-identity.log", env, config["budgets"]["command_seconds"])
    if "g++" not in (work / "compiler-identity.log").read_text().splitlines()[0]:
        raise BuildRejected("this profile selects GNU g++, not an unverified compiler family")
    extracted = work / "source"
    members = preflight(archive, config, extracted)
    with tarfile.open(archive, "r:bz2") as source_tar:
        source_tar.extractall(extracted, members=members, filter="data")
    verify_archive(archive, config)
    source = extracted / "ns-3.47"
    if (source / "VERSION").read_text().strip() != config["release"]:
        raise BuildRejected("source VERSION differs from pinned release")
    cache = work / "cmake-cache"
    artifacts = work / "artifacts"
    configure = [str(cmake), "-S", str(source), "-B", str(cache), "-G", "Ninja", "-DCMAKE_BUILD_TYPE=Release", "-DCMAKE_CXX_COMPILER=" + str(compiler), "-DCMAKE_MAKE_PROGRAM=" + str(ninja), "-DNS3_OUTPUT_DIRECTORY=" + str(artifacts), "-DNS3_ENABLED_MODULES=core", "-DNS3_EXAMPLES=OFF", "-DNS3_TESTS=OFF", "-DNS3_PYTHON_BINDINGS=OFF", "-DNS3_ENABLE_BUILD_VERSION=OFF", "-DNS3_CCACHE=OFF", "-DNS3_PRECOMPILE_HEADERS=OFF", "-DNS3_VISUALIZER=OFF", "-DNS3_GSL=OFF", "-DNS3_SQLITE=OFF", "-DNS3_EIGEN=OFF"]
    checked(configure, work / "configure.log", env, config["budgets"]["configure_seconds"])
    check_cache(cache / "CMakeCache.txt", source, compiler)
    checked([str(cmake), "--build", str(cache), "--target", "core", "--parallel", str(config["build"]["parallel_jobs"])], work / "build.log", env, config["budgets"]["build_seconds"])
    libraries = [p for p in (artifacts / "lib").glob("libns3*-core*.so") if p.is_file() and not p.is_symlink()]
    if len(libraries) != 1:
        raise BuildRejected("missing/ambiguous freshly built core library")
    library = libraries[0]
    executable = work / "ns3-installation-smoke"
    checked([str(compiler), "-std=c++20", "-I" + str(artifacts / "include"), str(FIXTURE), str(library), "-Wl,-rpath," + str(library.parent), "-o", str(executable)], work / "probe-compile.log", env, config["budgets"]["configure_seconds"])
    for index in (1, 2):
        log = work / f"run-{index}.log"
        checked([str(executable)], log, env, config["budgets"]["command_seconds"])
        check_output(config, log.read_text())
    verify_archive(archive, config)
    return {"status": "NS3_CORE_INSTALLATION_SMOKE_PASS", "release": config["release"], "source_sha256": config["archive"]["sha256"], "tool_versions": tools, "core_library_sha256": hashlib.sha256(library.read_bytes()).hexdigest(), "fixture_sha256": config["fixture_sha256"], "repeat_runs": 2, "expected_event_time_ns": 1, "upstream_test_suite": "NOT_RUN", "python_bindings": "NOT_RUN", "scientific_validation": "UNVALIDATED", "simulator_support_verified": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", required=True, type=Path)
    parser.add_argument("--work-dir", required=True, type=Path)
    parser.add_argument("--profile", type=Path, default=DEFAULT_PROFILE)
    parser.add_argument("--cxx", type=Path, default=Path("/usr/bin/g++"))
    parser.add_argument("--cmake", type=Path, default=Path("/usr/bin/cmake"))
    parser.add_argument("--ninja", type=Path, default=Path("/usr/bin/ninja"))
    args = parser.parse_args()
    try:
        if args.work_dir.is_symlink():
            raise BuildRejected("preserve symlinked work location")
        config = read_profile(args.profile)
        receipt = build(config, args.archive.resolve(), args.work_dir.resolve(), args.cxx, args.cmake, args.ninja)
        (args.work_dir / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
        print(json.dumps(receipt, indent=2))
        return 0
    except (BuildRejected, OSError, ValueError, KeyError, TypeError, tarfile.TarError) as exc:
        message = str(exc) if isinstance(exc, BuildRejected) else "dependency/profile operation failed; inspect private diagnostics"
        print("NS3_SMOKE_REJECTED: " + message, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
