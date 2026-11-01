"""S019 fail-closed installation contracts; real dependency smoke runs separately."""
from __future__ import annotations

import copy
import json
import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import sumo_smoke as smoke


class SumoSmokeTests(unittest.TestCase):
    def test_profile_and_hash_checked_requirements_agree(self):
        config = smoke.load_profile(smoke.DEFAULT_PROFILE)
        self.assertEqual(config.release, "1.28.0")
        self.assertEqual(config.protocol, 22)
        self.assertEqual(set(config.packages), {"eclipse-sumo", "sumo-data", "traci", "sumolib"})

    def test_executable_version_is_exact_not_substring(self):
        for text in ("Eclipse SUMO sumo 1.28.0\n Build features: test", "Eclipse SUMO sumo Version 1.28.0\n"):
            smoke.check_executable_version(text, "1.28.0")
        for text in ("", "1.28.0", "Eclipse SUMO sumo 1.28.01", "Eclipse SUMO sumo 1.28.0-dev", "Eclipse SUMO sumo 1.27.1", "noise\nEclipse SUMO sumo 1.28.0"):
            with self.subTest(text=text), self.assertRaises(smoke.SmokeRejected):
                smoke.check_executable_version(text, "1.28.0")

    def test_generated_versions_do_not_accept_neighbor_release(self):
        rng = random.Random(19)
        for _ in range(100):
            parts = [rng.randrange(100) for _ in range(3)]
            release = ".".join(map(str, parts))
            smoke.check_executable_version("Eclipse SUMO sumo " + release, release)
            parts[-1] += 1
            with self.assertRaises(smoke.SmokeRejected):
                smoke.check_executable_version("Eclipse SUMO sumo " + ".".join(map(str, parts)), release)

    def test_binding_protocol_and_server_version_must_all_match(self):
        config = smoke.load_profile(smoke.DEFAULT_PROFILE)
        versions = dict(config.packages)
        smoke.check_handshake(config, versions, (22, "SUMO 1.28.0"))
        for protocol, server in ((21, "SUMO 1.28.0"), (True, "SUMO 1.28.0"), (22, "SUMO 1.27.1"), (22, "SUMO 1.28.0-dev")):
            with self.assertRaises(smoke.SmokeRejected):
                smoke.check_handshake(config, versions, (protocol, server))
        for name in versions:
            bad = dict(versions, **{name: "1.27.1"})
            with self.assertRaises(smoke.SmokeRejected):
                smoke.check_handshake(config, bad, (22, "SUMO 1.28.0"))
        with self.assertRaises(smoke.SmokeRejected):
            smoke.check_handshake(config, {}, (22, "SUMO 1.28.0"))

    def test_malformed_duplicate_or_unbounded_profiles_rejected(self):
        original = json.loads(smoke.DEFAULT_PROFILE.read_text())
        changes = [("schema_version", True), ("release", "1.28.0-dev"), ("traci_protocol", True), ("python", "3.11.0"), ("scientific_validation", "VALIDATED"), ("simulator_support_verified", True)]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "profile.json"
            (path.parent / "requirements-sumo-linux.txt").write_text((smoke.DEFAULT_PROFILE.parent / "requirements-sumo-linux.txt").read_text())
            for key, value in changes:
                bad = copy.deepcopy(original)
                bad[key] = value
                path.write_text(json.dumps(bad))
                with self.subTest(key=key), self.assertRaises(smoke.SmokeRejected):
                    smoke.load_profile(path)
            for value in (0, -1, True, 10**9):
                bad = copy.deepcopy(original)
                bad["budgets"]["worker_timeout_seconds"] = value
                path.write_text(json.dumps(bad))
                with self.assertRaises(smoke.SmokeRejected):
                    smoke.load_profile(path)
            path.write_text('{"schema_version":1,"schema_version":1}')
            with self.assertRaises(smoke.SmokeRejected):
                smoke.load_profile(path)

    def test_foreign_platform_rejected_before_execution(self):
        config = smoke.load_profile(smoke.DEFAULT_PROFILE)
        for system, machine, libc in (("Windows", "AMD64", ""), ("Linux", "aarch64", "2.39"), ("Linux", "x86_64", "2.17"), ("Linux", "x86_64", "")):
            with self.assertRaises(smoke.SmokeRejected):
                smoke.check_platform(config, system, machine, libc)
        smoke.check_platform(config, "Linux", "x86_64", "2.39")

    def test_missing_executable_does_not_fall_back_to_path(self):
        with tempfile.TemporaryDirectory() as directory, patch("subprocess.run") as run:
            with self.assertRaises(smoke.SmokeRejected):
                smoke.required_executable(Path(directory), "sumo")
            run.assert_not_called()

    def test_child_timeout_is_failure_and_process_is_reaped(self):
        with self.assertRaises(smoke.SmokeRejected):
            smoke.bounded_worker([sys.executable, "-I", "-c", "import time; time.sleep(10)"], {}, 0.05)

    def test_timeout_retains_partial_diagnostics(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            with self.assertRaises(smoke.SmokeRejected):
                smoke.bounded_worker([sys.executable, "-I", "-c", "import time; print('before-timeout', flush=True); time.sleep(10)"], {}, 0.2, work)
            self.assertIn("before-timeout", (work / "worker.stdout").read_text())

    def test_public_missing_profile_executable_records_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            prefix = Path(directory) / "missing profile α"
            work = Path(directory) / "new diagnostics"
            result = subprocess.run([sys.executable, "-I", str(smoke.ROOT / "scripts/sumo_smoke.py"), "--prefix", str(prefix), "--work-dir", str(work)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn("missing/outside-profile executable", result.stderr)
            self.assertEqual(json.loads((work / "failure.json").read_text())["status"], "FAILED_NOT_ACCEPTED")
            self.assertFalse(prefix.exists())

    def test_public_existing_evidence_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            (work / "sentinel").write_text("preserve")
            result = subprocess.run([sys.executable, "-I", str(smoke.ROOT / "scripts/sumo_smoke.py"), "--prefix", str(work / "absent"), "--work-dir", str(work)], capture_output=True)
            self.assertEqual(result.returncode, 1)
            self.assertEqual((work / "sentinel").read_text(), "preserve")
            self.assertFalse((work / "failure.json").exists())

    def test_symlink_to_foreign_executable_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "prefix/bin").mkdir(parents=True)
            executable = root / "foreign"
            executable.write_text("not executed")
            executable.chmod(0o700)
            (root / "prefix/bin/sumo").symlink_to(executable)
            with self.assertRaises(smoke.SmokeRejected):
                smoke.required_executable(root / "prefix", "sumo")

    def test_artifact_duplicates_and_hash_tampering_fail_closed(self):
        original = json.loads(smoke.DEFAULT_PROFILE.read_text())
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "profile.json"
            (path.parent / "requirements-sumo-linux.txt").write_text((smoke.DEFAULT_PROFILE.parent / "requirements-sumo-linux.txt").read_text())
            for kind in ("duplicate", "hash", "registry", "size"):
                bad = copy.deepcopy(original)
                if kind == "duplicate":
                    bad["packages"].append(bad["packages"][0])
                elif kind == "hash":
                    bad["packages"][0]["sha256"] = "0" * 64
                elif kind == "registry":
                    bad["packages"][0]["url"] = "https://invalid.example/package.whl"
                else:
                    bad["packages"][0]["size_bytes"] = True
                path.write_text(json.dumps(bad))
                with self.subTest(kind=kind), self.assertRaises(smoke.SmokeRejected):
                    smoke.load_profile(path)

    def test_global_sumo_and_binding_overrides_are_removed(self):
        self.assertEqual(smoke.child_environment({"PATH": "retained", "SUMO_HOME": "foreign", "LIBSUMO_AS_TRACI": "1", "LIBTRACI_AS_TRACI": "1", "PYTHONPATH": "foreign", "UV_INDEX_URL": "foreign"}), {"PATH": "retained"})

    def test_install_never_overwrites_an_existing_prefix(self):
        config = smoke.load_profile(smoke.DEFAULT_PROFILE)
        with tempfile.TemporaryDirectory() as directory, patch("subprocess.run") as run:
            prefix = Path(directory)
            (prefix / "unrelated.txt").write_text("preserve")
            with self.assertRaises(smoke.SmokeRejected):
                smoke.install_profile(config, prefix, prefix)
            self.assertEqual((prefix / "unrelated.txt").read_text(), "preserve")
            run.assert_not_called()

    def test_public_install_preserves_dangling_prefix_symlink(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prefix = root / "link"
            target = root / "must-remain-absent"
            prefix.symlink_to(target, target_is_directory=True)
            result = subprocess.run([sys.executable, "-I", str(smoke.ROOT / "scripts/sumo_smoke.py"), "--install", "--prefix", str(prefix), "--work-dir", str(root / "evidence")], capture_output=True)
            self.assertEqual(result.returncode, 1)
            self.assertTrue(prefix.is_symlink())
            self.assertFalse(target.exists())

    def test_incomplete_or_clearance_claiming_worker_receipt_rejected(self):
        config = smoke.load_profile(smoke.DEFAULT_PROFILE)
        good = {"status": "SUMO_INSTALLATION_SMOKE_PASS", "release": config.release, "protocol": config.protocol, "packages": config.packages, "simulation_steps": 0, "scientific_validation": "UNVALIDATED", "simulator_support_verified": False}
        smoke.validate_receipt(config, good)
        for key, value in (("status", "PARTIAL"), ("simulation_steps", True), ("simulation_steps", 1), ("scientific_validation", "VALIDATED"), ("simulator_support_verified", True)):
            bad = dict(good, **{key: value})
            with self.assertRaises(smoke.SmokeRejected):
                smoke.validate_receipt(config, bad)
        with self.assertRaises(smoke.SmokeRejected):
            smoke.validate_receipt(config, {})


if __name__ == "__main__":
    unittest.main()
