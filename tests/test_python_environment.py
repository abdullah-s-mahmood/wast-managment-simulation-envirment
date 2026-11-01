"""Independent fixtures for exact Python/lock/isolation setup contracts."""
from __future__ import annotations

import json
import os
import random
import shutil
import subprocess
import sys
import sysconfig
import tempfile
import unittest
from pathlib import Path

from scripts import python_environment as tooling


class PythonEnvironmentTests(unittest.TestCase):
    def fixture(self, root: Path) -> tooling.Settings:
        current = tooling.settings()
        prefix = root / ".venv"
        prefix.mkdir()
        (prefix / "pyvenv.cfg").write_text("include-system-site-packages = false\n")
        return tooling.Settings(root, current.python, current.uv, current.development)

    def validate(self, config: tooling.Settings, **changes: object) -> None:
        values = {
            "version": config.python,
            "implementation": "cpython",
            "prefix": config.root / ".venv",
            "base_prefix": config.root / "base",
            "isolated": 1,
            "user_site": False,
            "paths": [str(config.root / ".venv/lib/python3.12/site-packages")],
        }
        values.update(changes)
        tooling.validate_interpreter(config, **values)

    def test_exact_configuration_and_no_application_dependencies(self):
        config = tooling.settings()
        self.assertEqual(set(config.development), {"uv", "ruff", "mypy"})
        self.assertEqual(config.development["uv"], config.uv)
        self.assertEqual(len(tooling.validate_lock(config)), 64)

    def test_incompatible_python_or_implementation_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            config = self.fixture(Path(directory))
            for changes in ({"version": "3.11.99"}, {"implementation": "pypy"}):
                with self.subTest(changes=changes), self.assertRaises(tooling.EnvironmentRejected):
                    self.validate(config, **changes)

    def test_global_interpreter_and_nonisolated_startup_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            config = self.fixture(Path(directory))
            for changes in ({"base_prefix": config.root / ".venv"}, {"isolated": 0}, {"user_site": True}):
                with self.subTest(changes=changes), self.assertRaises(tooling.EnvironmentRejected):
                    self.validate(config, **changes)

    def test_system_site_and_duplicate_configuration_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            config = self.fixture(Path(directory))
            self.validate(config)
            path = config.root / ".venv/pyvenv.cfg"
            for text in ("include-system-site-packages = true\n", "", "include-system-site-packages = false\ninclude-system-site-packages = false\n"):
                path.write_text(text)
                with self.assertRaises(tooling.EnvironmentRejected):
                    self.validate(config)

    def test_external_site_path_is_not_a_venv_dependency(self):
        with tempfile.TemporaryDirectory() as directory:
            config = self.fixture(Path(directory))
            with self.assertRaises(tooling.EnvironmentRejected):
                self.validate(config, paths=[str(config.root / "base/lib/python3.12/site-packages")])

    def test_venv_symlink_cannot_redirect_checks(self):
        with tempfile.TemporaryDirectory() as directory:
            config = self.fixture(Path(directory))
            (config.root / ".venv").rename(config.root / "original")
            (config.root / ".venv").symlink_to(config.root / "original", target_is_directory=True)
            with self.assertRaises(tooling.EnvironmentRejected):
                self.validate(config)

    def test_index_python_and_active_environment_overrides_removed(self):
        result = tooling.clean_environment({"PATH": "trusted", "UV_PROJECT_ENVIRONMENT": "other", "UV_INDEX_URL": "https://invalid.example/simple", "PYTHONPATH": "global", "PIP_CONFIG_FILE": "other", "VIRTUAL_ENV": "other"})
        self.assertEqual(result, {"PATH": "trusted"})

    def test_private_or_unhashed_lock_sources_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("pyproject.toml", ".python-version", "uv.lock", "requirements-bootstrap.txt"):
                shutil.copyfile(tooling.ROOT / name, root / name)
            original = (root / "uv.lock").read_text()
            for changed in (original.replace("https://pypi.org/simple", "https://invalid.example/simple"), original.replace("sha256:", "unsupported:")):
                (root / "uv.lock").write_text(changed)
                with self.assertRaises(tooling.EnvironmentRejected):
                    tooling.validate_lock(tooling.settings(root))

    def test_sync_refuses_unrecognized_or_symlinked_environment(self):
        with tempfile.TemporaryDirectory() as directory:
            config = self.fixture(Path(directory))
            with self.assertRaises(tooling.EnvironmentRejected):
                tooling.synchronize(config, "never-execute-this-manager")
            (config.root / ".venv/.wm-development-environment.json").write_text(json.dumps({"schema_version": True, "managed_by": "S018", "project": "wast-managment-simulation-envirment"}))
            with self.assertRaises(tooling.EnvironmentRejected):
                tooling.synchronize(config, "never-execute-this-manager")
            (config.root / ".venv").rename(config.root / "saved")
            (config.root / ".venv").symlink_to(config.root / "saved", target_is_directory=True)
            with self.assertRaises(tooling.EnvironmentRejected):
                tooling.synchronize(config, "never-execute-this-manager")

    def test_lint_and_type_contract_cannot_be_weakened(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copyfile(tooling.ROOT / ".python-version", root / ".python-version")
            original = (tooling.ROOT / "pyproject.toml").read_text()
            for changed in (original.replace("strict = true", "strict = false"), original.replace('"E4", "E7", "E9", "F", "I", "UP"', '"E9"')):
                (root / "pyproject.toml").write_text(changed)
                with self.assertRaises(tooling.EnvironmentRejected):
                    tooling.settings(root)

    def test_bootstrap_manager_hashes_are_bound_to_lock(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("pyproject.toml", ".python-version", "uv.lock", "requirements-bootstrap.txt"):
                shutil.copyfile(tooling.ROOT / name, root / name)
            (root / "requirements-bootstrap.txt").write_text("uv==0.0.0\n")
            with self.assertRaises(tooling.EnvironmentRejected):
                tooling.validate_lock(tooling.settings(root))

    def test_generated_overrides_are_removed_without_touching_input(self):
        rng = random.Random(18)
        for _ in range(100):
            original = {"PATH": "retained"}
            original.update({rng.choice(["UV_", "PIP_", "PYTHON"]) + str(i): str(rng.randrange(100)) for i in range(20)})
            before = dict(original)
            clean = tooling.clean_environment(original)
            self.assertEqual(clean, {"PATH": "retained"})
            self.assertEqual(original, before)
            self.assertEqual(tooling.clean_environment(clean), clean)

    def test_actual_doctor_from_other_cwd(self):
        result = subprocess.run([sys.executable, "-I", str(tooling.ROOT / "scripts/python_environment.py"), "doctor"], cwd="/", capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "VALID_ISOLATED_DEVELOPMENT_ENVIRONMENT")

    def test_actual_global_mode_is_rejected(self):
        result = subprocess.run([sys.executable, "-I", "-S", str(tooling.ROOT / "scripts/python_environment.py"), "doctor"], capture_output=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn(b"DEVELOPMENT_ENVIRONMENT_REJECTED", result.stderr)

    def test_pythonpath_pollution_does_not_supply_global_module(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "wm_global_pollution_fixture.py").write_text("raise RuntimeError('must not import')\n")
            environment = dict(os.environ, PYTHONPATH=directory, PYTHONUSERBASE=directory)
            result = subprocess.run([sys.executable, "-I", "-c", "import importlib.util; assert importlib.util.find_spec('wm_global_pollution_fixture') is None"], env=environment, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_extra_package_in_managed_venv_is_rejected_without_cleanup(self):
        self.assertEqual(Path(sys.prefix).resolve(), (tooling.ROOT / ".venv").resolve())
        folder = Path(sysconfig.get_path("purelib")) / "wm_s018_pollution_fixture-0.0.0.dist-info"
        folder.mkdir()
        try:
            (folder / "METADATA").write_text("Metadata-Version: 2.1\nName: wm-s018-pollution-fixture\nVersion: 0.0.0\n")
            result = subprocess.run([sys.executable, "-I", str(tooling.ROOT / "scripts/python_environment.py"), "doctor"], capture_output=True)
            self.assertEqual(result.returncode, 1)
            self.assertTrue(folder.exists(), "doctor must not silently repair the environment")
        finally:
            shutil.rmtree(folder)


if __name__ == "__main__":
    unittest.main()
