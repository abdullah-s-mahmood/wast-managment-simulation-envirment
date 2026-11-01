"""S020 build/install contracts; independent real build runs in CI and privately."""
from __future__ import annotations

import copy
import io
import json
import random
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path

from scripts import ns3_smoke as smoke


class Ns3SmokeTests(unittest.TestCase):
    def test_profile_and_version_requirements(self):
        config = smoke.read_profile(smoke.DEFAULT_PROFILE)
        self.assertEqual(config["release"], "3.47")
        smoke.version_at_least("13.3.0", "11.1")
        for text in ("", "unknown", "11.0", "10.9.9", "13.3.0-dev"):
            with self.assertRaises(smoke.BuildRejected):
                smoke.version_at_least(text, "11.1")

    def test_generated_version_order_reference(self):
        rng = random.Random(20)
        for _ in range(100):
            major, minor = rng.randrange(1, 50), rng.randrange(1, 50)
            smoke.version_at_least(f"{major}.{minor}", f"{major}.{minor}")
            with self.assertRaises(smoke.BuildRejected):
                smoke.version_at_least(f"{major}.{minor-1}", f"{major}.{minor}")

    def test_malformed_profile_and_budget_are_rejected(self):
        original = json.loads(smoke.DEFAULT_PROFILE.read_text())
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "profile.json"
            for key, value in (("schema_version", True), ("release", "3.46"), ("scientific_validation", "VALIDATED"), ("simulator_support_verified", True), ("fixture_sha256", "0" * 64)):
                bad = copy.deepcopy(original)
                bad[key] = value
                path.write_text(json.dumps(bad))
                with self.subTest(key=key), self.assertRaises(smoke.BuildRejected):
                    smoke.read_profile(path)
            for value in (0, -1, True, 10**12):
                bad = copy.deepcopy(original)
                bad["budgets"]["build_seconds"] = value
                path.write_text(json.dumps(bad))
                with self.assertRaises(smoke.BuildRejected):
                    smoke.read_profile(path)

    def test_source_size_and_hash_mismatch_rejected(self):
        config = smoke.read_profile(smoke.DEFAULT_PROFILE)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "wrong.tar.bz2"
            path.write_bytes(b"not the designated upstream source")
            with self.assertRaisesRegex(smoke.BuildRejected, "size mismatch"):
                smoke.verify_archive(path, config)
            with path.open("r+b") as stream:
                stream.truncate(config["archive"]["size_bytes"])
            with self.assertRaisesRegex(smoke.BuildRejected, "SHA256 mismatch"):
                smoke.verify_archive(path, config)

    def test_stale_cache_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            cache = work / "CMakeCache.txt"
            cache.write_text("CMAKE_HOME_DIRECTORY:INTERNAL=foreign\n")
            with self.assertRaises(smoke.BuildRejected):
                smoke.reserve_work(work)
            self.assertIn("foreign", cache.read_text())

    def test_missing_compiler_is_actionable(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(smoke.BuildRejected, "missing tool"):
                smoke.require_tool(Path(directory) / "absent-g++")

    def test_nonzero_run_is_failure_with_retained_command(self):
        with tempfile.TemporaryDirectory() as directory:
            log = Path(directory) / "negative.log"
            with self.assertRaises(smoke.BuildRejected):
                smoke.checked([sys.executable, "-I", "-c", "raise SystemExit(7)"], log, {}, 5)
            self.assertEqual(json.loads(log.with_suffix(".command.json").read_text())["exit_code"], 7)

    def test_public_global_python_mode_is_rejected_before_build(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = subprocess.run([sys.executable, "-I", "-S", str(smoke.ROOT / "scripts/ns3_smoke.py"), "--archive", str(root / "absent.tar.bz2"), "--work-dir", str(root / "must-not-exist")], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn("isolated pinned project Python", result.stderr)
            self.assertFalse((root / "must-not-exist").exists())

    def test_timeout_is_failure_and_retained(self):
        with tempfile.TemporaryDirectory() as directory:
            log = Path(directory) / "timeout.log"
            with self.assertRaises(smoke.BuildRejected):
                smoke.checked([sys.executable, "-I", "-c", "import time; time.sleep(10)"], log, {}, 0.05)
            self.assertEqual(json.loads(log.with_suffix(".command.json").read_text())["status"], "TIMED_OUT_KILLED_REAPED")

    def test_configuration_injection_is_removed(self):
        source = {"PATH": "retained", "CXX": "foreign", "CXXFLAGS": "foreign", "CMAKE_PREFIX_PATH": "foreign", "PYTHONPATH": "foreign", "LD_LIBRARY_PATH": "foreign", "NS3_MODULES": "foreign"}
        self.assertEqual(smoke.clean_environment(source), {"PATH": "retained"})

    def test_build_cache_source_compiler_and_modules_must_agree(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, compiler = root / "source", root / "g++"
            cache = root / "CMakeCache.txt"
            good = f"CMAKE_HOME_DIRECTORY:INTERNAL={source}\nCMAKE_CXX_COMPILER:FILEPATH={compiler}\nNS3_ENABLED_MODULES:STRING=core\nCMAKE_BUILD_TYPE:STRING=Release\n"
            good += "".join(key + ":BOOL=OFF\n" for key in ("NS3_EXAMPLES", "NS3_TESTS", "NS3_PYTHON_BINDINGS", "NS3_ENABLE_BUILD_VERSION", "NS3_CCACHE", "NS3_PRECOMPILE_HEADERS", "NS3_VISUALIZER", "NS3_GSL", "NS3_SQLITE", "NS3_EIGEN"))
            cache.write_text(good)
            smoke.check_cache(cache, source, compiler)
            for text in (good.replace("=core", "=core;network"), good.replace("Release", "Debug"), good.replace(str(source), "foreign"), good + "NS3_ENABLED_MODULES:STRING=core\n", good.replace("NS3_TESTS:BOOL=OFF", "NS3_TESTS:BOOL=ON"), good.replace("NS3_GSL:BOOL", "NS3_GSL:UNINITIALIZED")):
                cache.write_text(text)
                with self.assertRaises(smoke.BuildRejected):
                    smoke.check_cache(cache, source, compiler)

    def test_reference_output_is_exact_and_not_scientific_clearance(self):
        config = smoke.read_profile(smoke.DEFAULT_PROFILE)
        smoke.check_output(config, '{"status":"NS3_CORE_SMOKE_PASS","event_time_ns":1}\n')
        for value in (True, 0, 2, 1.0):
            with self.assertRaises(smoke.BuildRejected):
                smoke.check_output(config, json.dumps({"status": "NS3_CORE_SMOKE_PASS", "event_time_ns": value}))
        for text in ("partial", '{"status":"NS3_CORE_SMOKE_PASS","event_time_ns":1,"scientific_validation":"VALIDATED"}', '{"event_time_ns":1,"event_time_ns":1}'):
            with self.assertRaises(smoke.BuildRejected):
                smoke.check_output(config, text)

    def test_archive_preflight_rejects_traversal_duplicates_and_unsafe_links(self):
        config = smoke.read_profile(smoke.DEFAULT_PROFILE)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for kind in ("traversal", "duplicate", "link", "special", "large"):
                path = root / (kind + ".tar.bz2")
                with tarfile.open(path, "w:bz2") as tar:
                    item = tarfile.TarInfo("ns-3.47/safe")
                    if kind == "traversal":
                        item.name = "ns-3.47/../../outside"
                    elif kind == "link":
                        item.type, item.linkname = tarfile.SYMTYPE, "../../outside"
                    elif kind == "special":
                        item.type = tarfile.FIFOTYPE
                    elif kind == "large":
                        item.size = config["budgets"]["member_bytes"] + 1
                    tar.addfile(item, io.BytesIO(b"\0" * item.size) if item.size else None)
                    if kind == "duplicate":
                        tar.addfile(item)
                with self.assertRaises(smoke.BuildRejected):
                    smoke.preflight(path, config, root / "destination")
                self.assertFalse((root / "destination").exists())


if __name__ == "__main__":
    unittest.main()
