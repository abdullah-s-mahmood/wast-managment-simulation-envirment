#!/usr/bin/env python3
"""Preparation, read-only validation and checks for the locked dev environment.

The bootstrap interpreter may differ; development checks require the exact pin,
an isolated project venv, and uv's non-mutating exact-environment check.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import re
import site
import subprocess
import sys
import tomllib
import unittest
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class EnvironmentRejected(RuntimeError):
    """An incompatible, polluted, or unlocked environment cannot run checks."""


@dataclass(frozen=True)
class Settings:
    """Explicit release identifiers; these are not scientific model parameters."""

    root: Path
    python: str
    uv: str
    development: dict[str, str]


def settings(root: Path = ROOT) -> Settings:
    """Read standard tooling contracts without resolving or installing packages."""
    data = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    pin = (root / ".python-version").read_text(encoding="utf-8").strip()
    manager = data["tool"]["uv"]["required-version"]
    if (
        not re.fullmatch(r"3\.12\.\d+", pin)
        or data["project"]["requires-python"] != ">=3.12,<3.13"
        or data["project"]["dependencies"] != []
        or not isinstance(manager, str)
        or not re.fullmatch(r"==\d+\.\d+\.\d+", manager)
    ):
        raise EnvironmentRejected("unsupported interpreter/project/manager contract")
    tools: dict[str, str] = {}
    for entry in data["dependency-groups"]["dev"]:
        if not isinstance(entry, str):
            raise EnvironmentRejected("invalid development dependency")
        match = re.fullmatch(r"([a-z][a-z0-9_-]*)==(\d+\.\d+\.\d+)", entry)
        if match is None or match[1] in tools:
            raise EnvironmentRejected("development dependencies must be unique exact pins")
        tools[match[1]] = match[2]
    if set(tools) != {"uv", "ruff", "mypy"} or tools.get("uv") != manager[2:]:
        raise EnvironmentRejected("unreviewed development tool set")
    if type(data["tool"]["mypy"].get("strict")) is not bool or data["tool"]["mypy"] != {"python_version": "3.12", "strict": True, "files": ["scripts/python_environment.py", "scripts/sumo_smoke.py"]}:
        raise EnvironmentRejected("type-check scope/strictness changed without a contract revision")
    if data["tool"]["ruff"] != {"target-version": "py312", "include": ["scripts/python_environment.py", "tests/test_python_environment.py", "scripts/sumo_smoke.py", "tests/test_sumo_smoke.py"], "lint": {"select": ["E4", "E7", "E9", "F", "I", "UP"]}}:
        raise EnvironmentRejected("lint scope/rules changed without a contract revision")
    return Settings(root, pin, manager[2:], tools)


def clean_environment(original: dict[str, str]) -> dict[str, str]:
    """Ignore ambient Python, package-index, and active-environment overrides."""
    return {
        key: value
        for key, value in original.items()
        if not key.startswith(("PYTHON", "PIP_", "UV_"))
        and key not in {"VIRTUAL_ENV", "CONDA_PREFIX"}
    }


def validate_interpreter(
    config: Settings,
    version: str,
    implementation: str,
    prefix: Path,
    base_prefix: Path,
    isolated: int,
    user_site: bool | None,
    paths: list[str],
) -> None:
    """Reject wrong Python, global/site pollution and unsafe startup modes."""
    expected = config.root / ".venv"
    if version != config.python or implementation != "cpython":
        raise EnvironmentRejected("development Python does not match .python-version")
    if expected.is_symlink() or prefix.resolve() != expected.resolve() or prefix == base_prefix:
        raise EnvironmentRejected("use this checkout's isolated .venv")
    if isolated != 1 or user_site is not False:
        raise EnvironmentRejected("run development Python with -I and no user site")
    cfg = (prefix / "pyvenv.cfg").read_text(encoding="utf-8")
    values: dict[str, str] = {}
    for line in cfg.splitlines():
        key, separator, value = line.partition("=")
        if separator:
            key = key.strip()
            if key in values:
                raise EnvironmentRejected("ambiguous virtual environment configuration")
            values[key] = value.strip()
    if values.get("include-system-site-packages") != "false":
        raise EnvironmentRejected("system site packages must be disabled explicitly")
    for entry in paths:
        path = Path(entry).resolve()
        if {"site-packages", "dist-packages"}.intersection(path.parts) and not path.is_relative_to(prefix.resolve()):
            raise EnvironmentRejected("external site packages present")


def validate_lock(config: Settings) -> str:
    """Require public-registry release artifacts with SHA-256, not private sources."""
    raw = (config.root / "uv.lock").read_bytes()
    data = tomllib.loads(raw.decode("utf-8"))
    if type(data.get("version")) is not int or data["version"] != 1:
        raise EnvironmentRejected("unsupported lock format")
    selected: dict[str, str] = {}
    manager_hashes: set[str] = set()
    for package in data["package"]:
        if package["source"] == {"virtual": "."}:
            continue
        if package["source"] != {"registry": "https://pypi.org/simple"}:
            raise EnvironmentRejected("unapproved lock source")
        selected[package["name"]] = package["version"]
        if package["name"] == "uv":
            manager_hashes = {item["hash"] for item in package.get("wheels", [])}
        artifacts = list(package.get("wheels", []))
        if "sdist" in package:
            artifacts.append(package["sdist"])
        if not artifacts:
            raise EnvironmentRejected("missing distribution artifacts")
        for artifact in artifacts:
            if not artifact["url"].startswith("https://files.pythonhosted.org/") or not re.fullmatch(r"sha256:[0-9a-f]{64}", artifact["hash"]):
                raise EnvironmentRejected("unhashed or nonpublic distribution")
    if any(selected.get(name) != version for name, version in config.development.items()):
        raise EnvironmentRejected("direct dependency pin/lock disagreement")
    continuation = " " + chr(92) + "\n"
    expected_bootstrap = "# Bootstrap manager only; generated from uv.lock wheel hashes.\nuv==" + config.uv + continuation
    expected_bootstrap += continuation.join("    --hash=" + value for value in sorted(manager_hashes)) + "\n"
    if (config.root / "requirements-bootstrap.txt").read_text(encoding="utf-8") != expected_bootstrap:
        raise EnvironmentRejected("bootstrap manager pin/hashes differ from uv.lock")
    return hashlib.sha256(raw).hexdigest()


def synchronize(config: Settings, uv: str) -> dict[str, object]:
    """Prepare only a fresh or explicitly S018-owned project venv, never globals."""
    target = config.root / ".venv"
    marker = target / ".wm-development-environment.json"
    if target.is_symlink():
        raise EnvironmentRejected("virtual environment symlink refused")
    if target.exists():
        if not marker.is_file() or marker.is_symlink():
            raise EnvironmentRejected("preserve unrecognized existing virtual environment")
        ownership = json.loads(marker.read_text(encoding="utf-8"))
        if not isinstance(ownership, dict) or type(ownership.get("schema_version")) is not int or ownership != {"schema_version": 1, "managed_by": "S018", "project": "wast-managment-simulation-envirment"}:
            raise EnvironmentRejected("virtual environment ownership mismatch")
    lock_hash = validate_lock(config)
    env = clean_environment(dict(os.environ))
    version = subprocess.run([uv, "--version"], check=True, capture_output=True, text=True, env=env, timeout=30)
    if version.stdout.split()[:2] != ["uv", config.uv]:
        raise EnvironmentRejected("bootstrap uv manager does not match the pin")
    git_directory = subprocess.check_output(["git", "rev-parse", "--git-common-dir"], cwd=config.root, text=True).strip()
    storage = (config.root / git_directory).resolve() / "private-development/S018"
    storage.mkdir(mode=0o700, parents=True, exist_ok=True)
    env["UV_CACHE_DIR"] = str(storage / "cache")
    env["UV_PYTHON_INSTALL_DIR"] = str(storage / "python")
    subprocess.run(
        [uv, "--no-config", "sync", "--locked", "--managed-python", "--python", config.python,
         "--default-index", "https://pypi.org/simple", "--no-build"],
        cwd=config.root, env=env, check=True, timeout=180,
    )
    marker.write_text(json.dumps({"schema_version": 1, "managed_by": "S018", "project": "wast-managment-simulation-envirment"}, indent=2) + "\n", encoding="utf-8")
    return {"status": "PREPARED_LOCKED_ENVIRONMENT_NOT_YET_TESTED", "python": config.python,
            "uv": config.uv, "lock_sha256": lock_hash}


def doctor(config: Settings, uv: str) -> dict[str, object]:
    """Validate identity/isolation and ask pinned uv to check without modifying."""
    validate_interpreter(
        config,
        ".".join(map(str, sys.version_info[:3])),
        sys.implementation.name,
        Path(sys.prefix),
        Path(sys.base_prefix),
        sys.flags.isolated,
        site.ENABLE_USER_SITE,
        sys.path,
    )
    lock_hash = validate_lock(config)
    env = clean_environment(dict(os.environ))
    version = subprocess.run([uv, "--version"], check=True, capture_output=True, text=True, env=env, timeout=30)
    if version.stdout.split()[:2] != ["uv", config.uv]:
        raise EnvironmentRejected("uv manager does not match the exact pin")
    subprocess.run(
        [uv, "--no-config", "--no-cache", "sync", "--check", "--locked", "--offline", "--no-python-downloads", "--python", sys.executable, "--default-index", "https://pypi.org/simple"],
        cwd=config.root, env=env, check=True, capture_output=True, timeout=120,
    )
    actual = {name: importlib.metadata.version(name) for name in config.development}
    if actual != config.development:
        raise EnvironmentRejected("installed development tool versions differ")
    with Path(sys.executable).open("rb") as executable:
        executable_hash = hashlib.file_digest(executable, "sha256").hexdigest()
    return {"python_executable_sha256": executable_hash, "status": "VALID_ISOLATED_DEVELOPMENT_ENVIRONMENT", "python": config.python,
            "uv": config.uv, "development_tools": actual, "lock_sha256": lock_hash,
            "global_site_packages": False, "isolated_startup": True,
            "scientific_validation": "UNVALIDATED", "simulator_support_verified": False}


def checks(config: Settings) -> bool:
    """Run scoped lint/types and every existing test without ambient import paths."""
    env = clean_environment(dict(os.environ))
    commands = [
        [sys.executable, "-I", "-m", "ruff", "check", "--no-cache", "scripts/python_environment.py", "tests/test_python_environment.py", "scripts/sumo_smoke.py", "tests/test_sumo_smoke.py"],
        [sys.executable, "-I", "-m", "mypy", "--config-file", "pyproject.toml"],
    ]
    for command in commands:
        subprocess.run(command, cwd=config.root, env=env, check=True, timeout=120)
    sys.path.insert(0, str(config.root))
    suite = unittest.defaultTestLoader.discover(str(config.root / "tests"))
    return unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()


def main() -> int:
    """Print sanitized readiness or fail before running development checks."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("sync", "doctor", "check"))
    parser.add_argument("--uv")
    args = parser.parse_args()
    try:
        config = settings()
        local_manager = config.root / ".venv" / ("Scripts/uv.exe" if os.name == "nt" else "bin/uv")
        manager = args.uv or (str(local_manager) if local_manager.is_file() else "uv")
        if args.mode == "sync":
            print(json.dumps(synchronize(config, manager), indent=2))
            return 0
        result = doctor(config, manager)
        if args.mode == "check" and not checks(config):
            return 1
    except (OSError, ValueError, KeyError, TypeError, EnvironmentRejected, subprocess.SubprocessError):
        print("DEVELOPMENT_ENVIRONMENT_REJECTED", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
