#!/usr/bin/env python3
"""Bounded S019 installation/API smoke; never advances simulation time.

Only the independently installed, pinned upstream profile is executed. This is
not the legacy archive, a scenario runner, a host sandbox, or physical validation.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
import importlib.metadata
import json
import os
import platform
import re
import signal
import socket
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROFILE = ROOT / "docs/tooling/S019_SUMO_PROFILE.json"


class SmokeRejected(RuntimeError):
    """Installation smoke failed; its retained diagnostics are not acceptance."""


@dataclass(frozen=True)
class Profile:
    """Release IDs, protocol integer, wall-clock seconds and fixture SI values."""

    release: str
    python: str
    protocol: int
    packages: dict[str, str]
    budgets: dict[str, int]
    fixture: dict[str, int]
    sha256: str
    requirements: Path


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Reject duplicate JSON keys rather than accepting a hidden last value."""
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise SmokeRejected("duplicate profile/receipt field")
        result[key] = value
    return result


def load_profile(path: Path) -> Profile:
    """Validate explicit profile, source hashes and bounded diagnostic inputs."""
    raw = path.read_bytes()
    data = json.loads(raw, object_pairs_hook=unique_object)
    fields = {"schema_version", "profile_id", "release", "python", "platform", "traci_protocol", "packages", "budgets", "fixture", "scientific_validation", "simulator_support_verified"}
    if not isinstance(data, dict) or set(data) != fields or type(data["schema_version"]) is not int or data["schema_version"] != 1:
        raise SmokeRejected("unsupported profile schema")
    if not isinstance(data["release"], str) or re.fullmatch(r"\d+\.\d+\.\d+", data["release"]) is None or data["python"] != (ROOT / ".python-version").read_text().strip():
        raise SmokeRejected("invalid release or development interpreter disagreement")
    if data["profile_id"] != "SUMO128_LINUX_X86_64" or data["platform"] != {"system": "Linux", "machine": "x86_64", "minimum_glibc": "2.28"}:
        raise SmokeRejected("unapproved installation profile/platform")
    if type(data["traci_protocol"]) is not int or data["traci_protocol"] < 1 or data["scientific_validation"] != "UNVALIDATED" or data["simulator_support_verified"] is not False:
        raise SmokeRejected("invalid protocol or unsupported clearance claim")
    packages: dict[str, str] = {}
    if not isinstance(data["packages"], list):
        raise SmokeRejected("missing package artifacts")
    for package in data["packages"]:
        if not isinstance(package, dict) or set(package) != {"name", "version", "filename", "url", "size_bytes", "sha256", "license_expression"}:
            raise SmokeRejected("invalid package metadata")
        name = package["name"]
        if not isinstance(name, str) or name in packages or package["version"] != data["release"]:
            raise SmokeRejected("duplicate or mismatched package release")
        if not isinstance(package["sha256"], str) or re.fullmatch(r"[0-9a-f]{64}", package["sha256"]) is None or not isinstance(package["url"], str) or not package["url"].startswith("https://files.pythonhosted.org/") or not isinstance(package["filename"], str) or not package["filename"].endswith(".whl") or type(package["size_bytes"]) is not int or package["size_bytes"] <= 0:
            raise SmokeRejected("unhashed/nonpublic wheel metadata")
        packages[name] = package["version"]
    if set(packages) != {"eclipse-sumo", "sumo-data", "traci", "sumolib"}:
        raise SmokeRejected("unapproved simulator package set")
    requirements = "# S019 Linux x86_64 profile; independently fetched public PyPI wheel hashes.\n" + "".join(p["name"] + "==" + p["version"] + " --hash=sha256:" + p["sha256"] + "\n" for p in data["packages"])
    if (path.parent / "requirements-sumo-linux.txt").read_text() != requirements:
        raise SmokeRejected("profile/requirements pin or hash disagreement")
    budgets = data["budgets"]
    if not isinstance(budgets, dict) or set(budgets) != {"command_timeout_seconds", "worker_timeout_seconds", "socket_timeout_seconds", "installation_timeout_seconds"} or any(type(v) is not int or not 1 <= v <= (600 if k == "installation_timeout_seconds" else 60) for k, v in budgets.items()) or not budgets["socket_timeout_seconds"] < budgets["command_timeout_seconds"] < budgets["worker_timeout_seconds"]:
        raise SmokeRejected("invalid bounded wall-clock budgets")
    fixture = data["fixture"]
    if not isinstance(fixture, dict) or set(fixture) != {"grid_number", "grid_length_m", "lane_count", "speed_m_per_s", "seed"} or any(type(v) is not int for v in fixture.values()) or fixture != {"grid_number": 2, "grid_length_m": 100, "lane_count": 1, "speed_m_per_s": 10, "seed": 19}:
        raise SmokeRejected("unreviewed diagnostic fixture")
    return Profile(data["release"], data["python"], data["traci_protocol"], packages, budgets, fixture, hashlib.sha256(raw).hexdigest(), path.parent / "requirements-sumo-linux.txt")


def check_executable_version(text: str, release: str) -> None:
    """Require an exact stable first-line release, not a substring/nightly."""
    line = text.splitlines()[0] if text else ""
    if re.fullmatch(r"Eclipse SUMO sumo (?:Version )?" + re.escape(release), line) is None:
        raise SmokeRejected("SUMO executable version mismatch; use the pinned profile executable")


def check_handshake(config: Profile, packages: dict[str, str], version: tuple[object, object]) -> None:
    """Require every package pin, API protocol and server release together."""
    if not isinstance(version, tuple) or len(version) != 2 or packages != config.packages or type(version[0]) is not int or version[0] != config.protocol or version[1] != "SUMO " + config.release:
        raise SmokeRejected("SUMO/TraCI package, protocol or server release mismatch")


def check_platform(config: Profile, system: str, machine: str, libc: str) -> None:
    """Reject untested wheel targets before executing a dependency binary."""
    if system != "Linux" or machine != "x86_64" or re.fullmatch(r"\d+\.\d+", libc) is None or tuple(map(int, libc.split("."))) < (2, 28):
        raise SmokeRejected("profile requires Linux x86_64 with glibc>=2.28; other targets NOT_RUN")


def child_environment(original: dict[str, str]) -> dict[str, str]:
    """Ignore ambient source/index paths and alternate TraCI implementations."""
    return {k: v for k, v in original.items() if not k.startswith(("PYTHON", "PIP_", "UV_")) and k not in {"VIRTUAL_ENV", "CONDA_PREFIX", "SUMO_HOME", "LIBSUMO_AS_TRACI", "LIBTRACI_AS_TRACI"}}


def required_executable(prefix: Path, name: str) -> Path:
    """Resolve only an explicit profile entry point; never search ambient PATH."""
    path = prefix / "bin" / name
    if not path.is_file() or not os.access(path, os.X_OK) or not path.resolve().is_relative_to(prefix.resolve()):
        raise SmokeRejected("missing/outside-profile executable; install the pinned SUMO environment")
    return path


def bounded_worker(command: list[str], env: dict[str, str], timeout: float, diagnostics: Path | None = None) -> subprocess.CompletedProcess[str]:
    """Bound trusted worker/descendants; kill and reap the Linux process group."""
    process = subprocess.Popen(command, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, start_new_session=True)
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        os.killpg(process.pid, signal.SIGKILL)
        stdout, stderr = process.communicate()
        if diagnostics is not None:
            (diagnostics / "worker.stdout").write_text(stdout)
            (diagnostics / "worker.stderr").write_text(stderr)
        raise SmokeRejected("SUMO smoke worker timed out; process group killed/reaped") from exc
    return subprocess.CompletedProcess(command, process.returncode, stdout, stderr)


def validate_receipt(config: Profile, receipt: object) -> None:
    """Installation completion explicitly excludes simulation or model clearance."""
    expected = {"status": "SUMO_INSTALLATION_SMOKE_PASS", "release": config.release, "protocol": config.protocol, "packages": config.packages, "simulation_steps": 0, "scientific_validation": "UNVALIDATED", "simulator_support_verified": False}
    if not isinstance(receipt, dict) or receipt != expected or type(receipt.get("simulation_steps")) is not int or type(receipt.get("protocol")) is not int or receipt.get("simulator_support_verified") is not False:
        raise SmokeRejected("incomplete/mismatched worker receipt or unsupported clearance claim")


def install_profile(config: Profile, prefix: Path, work: Path) -> None:
    """Create a fresh dedicated venv; hash-check all wheels with pinned uv.

    Existing prefixes are preserved, even partial earlier failures. Network setup
    has its own explicit wall-clock budget; no global install or source build.
    """
    if prefix.exists() or prefix.is_symlink():
        raise SmokeRejected("preserve existing SUMO environment; choose a fresh owned prefix")
    if sys.flags.isolated != 1 or ".".join(map(str, sys.version_info[:3])) != config.python:
        raise SmokeRejected("install using S018 isolated pinned Python")
    manager = ROOT / ".venv/bin/uv"
    env = child_environment(dict(os.environ))
    expected = tomllib.loads((ROOT / "pyproject.toml").read_text())["tool"]["uv"]["required-version"][2:]
    observed = subprocess.run([str(manager), "--version"], env=env, capture_output=True, text=True, check=True, timeout=config.budgets["command_timeout_seconds"])
    if observed.stdout.split()[:2] != ["uv", expected]:
        raise SmokeRejected("installation manager differs from S018 pin")
    commands = [
        [sys.executable, "-I", "-m", "venv", str(prefix)],
        [str(manager), "--no-config", "--no-cache", "pip", "sync", "--python", str(prefix / "bin/python"), "--require-hashes", "--only-binary", ":all:", "--default-index", "https://pypi.org/simple", str(config.requirements.resolve())],
    ]
    for index, command in enumerate(commands):
        with (work / f"install-{index}.log").open("w") as log:
            subprocess.run(command, env=env, stdout=log, stderr=subprocess.STDOUT, check=True, timeout=config.budgets["installation_timeout_seconds"])


def worker(config: Profile, prefix: Path, work: Path) -> dict[str, object]:
    """Create empty diagnostic network, handshake, close; zero simulation steps."""
    if sys.flags.isolated != 1 or ".".join(map(str, sys.version_info[:3])) != config.python or Path(sys.prefix).resolve() != prefix.resolve() or sys.prefix == sys.base_prefix:
        raise SmokeRejected("use isolated pinned Python in the dedicated SUMO venv")
    packages = {name: importlib.metadata.version(name) for name in config.packages}
    if packages != config.packages:
        raise SmokeRejected("binding/application package version mismatch")
    traci = importlib.import_module("traci")
    sumolib = importlib.import_module("sumolib")
    for module in (traci, sumolib):
        if module.__file__ is None or not Path(module.__file__).resolve().is_relative_to(prefix.resolve()):
            raise SmokeRejected("bindings imported from outside the dedicated profile")
    binary = required_executable(prefix, "sumo")
    generator = required_executable(prefix, "netgenerate")
    env = child_environment(dict(os.environ))
    net = work / "diagnostic.net.xml"
    fixture = config.fixture
    with (work / "netgenerate.log").open("w") as log:
        subprocess.run([str(generator), "--grid", "--grid.number", str(fixture["grid_number"]), "--grid.length", str(fixture["grid_length_m"]), "--default.lanenumber", str(fixture["lane_count"]), "--default.speed", str(fixture["speed_m_per_s"]), "--seed", str(fixture["seed"]), "--output-file", str(net)], stdout=log, stderr=subprocess.STDOUT, env=env, check=True, timeout=config.budgets["command_timeout_seconds"])
    with socket.socket() as reservation:
        reservation.bind(("127.0.0.1", 0))
        port = reservation.getsockname()[1]
    # Reservation closes before SUMO binds: a concurrent bind fails this smoke,
    # never silently selects a different server or accepts partial connectivity.
    socket.setdefaulttimeout(config.budgets["socket_timeout_seconds"])
    with (work / "sumo.log").open("w") as log:
        process = subprocess.Popen([str(binary), "--net-file", str(net), "--remote-port", str(port), "--no-step-log", "true", "--xml-validation", "never"], stdout=log, stderr=subprocess.STDOUT, env=env)
        connection = None
        try:
            connection = traci.connect(port=port, host="127.0.0.1", numRetries=10, waitBetweenRetries=0.1, proc=process)
            version = connection.getVersion()
            check_handshake(config, packages, version)
            if traci.constants.TRACI_VERSION != config.protocol:
                raise SmokeRejected("installed client protocol constant mismatch")
            connection.close(False)
            connection = None
            if process.wait(timeout=config.budgets["socket_timeout_seconds"]) != 0:
                raise SmokeRejected("SUMO did not close successfully")
        finally:
            if process.poll() is None:
                process.kill()
            process.wait()
    return {"status": "SUMO_INSTALLATION_SMOKE_PASS", "release": config.release, "protocol": config.protocol, "packages": packages, "simulation_steps": 0, "scientific_validation": "UNVALIDATED", "simulator_support_verified": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prefix", required=True, type=Path)
    parser.add_argument("--work-dir", required=True, type=Path)
    parser.add_argument("--profile", type=Path, default=DEFAULT_PROFILE)
    parser.add_argument("--install", action="store_true", help="prepare a fresh dedicated profile before smoke")
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    created = False
    try:
        config = load_profile(args.profile)
        check_platform(config, platform.system(), platform.machine(), platform.libc_ver()[1])
        if args.install and (args.prefix.exists() or args.prefix.is_symlink()):
            raise SmokeRejected("preserve existing SUMO environment; choose a fresh owned prefix")
        if args.work_dir.is_symlink():
            raise SmokeRejected("preserve symlinked evidence location; choose a fresh owned directory")
        prefix = args.prefix.resolve()
        work = args.work_dir.resolve()
        if args.worker:
            receipt = worker(config, prefix, work)
            (work / "worker-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
            return 0
        # Preserve previous diagnostic artifacts; never truncate an earlier attempt.
        work.mkdir(parents=True, exist_ok=False)
        created = True
        if args.install:
            install_profile(config, prefix, work)
        binary = required_executable(prefix, "sumo")
        env = child_environment(dict(os.environ))
        version = subprocess.run([str(binary), "--version"], text=True, capture_output=True, env=env, timeout=config.budgets["command_timeout_seconds"], check=True)
        (work / "version.log").write_text(version.stdout + version.stderr)
        check_executable_version(version.stdout, config.release)
        result = bounded_worker([str(prefix / "bin/python"), "-I", str(Path(__file__).resolve()), "--worker", "--prefix", str(prefix), "--profile", str(args.profile.resolve()), "--work-dir", str(work)], env, config.budgets["worker_timeout_seconds"], work)
        (work / "worker.stdout").write_text(result.stdout)
        (work / "worker.stderr").write_text(result.stderr)
        if result.returncode:
            raise SmokeRejected("SUMO API worker failed; inspect retained private diagnostics")
        receipt = json.loads((work / "worker-receipt.json").read_text(), object_pairs_hook=unique_object)
        validate_receipt(config, receipt)
        receipt["profile_sha256"] = config.sha256
        receipt["executable_entry_sha256"] = hashlib.sha256(binary.read_bytes()).hexdigest()
        print(json.dumps(receipt, indent=2))
        return 0
    except (SmokeRejected, OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError, importlib.metadata.PackageNotFoundError) as exc:
        message = str(exc) if isinstance(exc, SmokeRejected) else "dependency/profile operation failed; inspect private logs and setup"
        if created:
            (work / "failure.json").write_text(json.dumps({"status": "FAILED_NOT_ACCEPTED", "reason": message}) + "\n")
        print("SUMO_SMOKE_REJECTED: " + message, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
