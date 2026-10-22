"""Synthetic boundary attacks; no real credentials or legacy source fixtures."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('boundary', ROOT / 'scripts/validate_repository_boundary.py')
boundary = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(boundary)


class BoundaryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'README.md').write_text('Synthetic governance fixture\n')
        self.manifest = {'schema_version': 1, 'groups': {'governance': ['README.md']}}

    def check(self, paths=None):
        return boundary.validate(self.root, self.manifest, paths or ['README.md'])

    def test_approved_fixture_and_order_invariance(self):
        (self.root / 'AGENTS.md').write_text('Synthetic rules')
        self.manifest['groups']['governance'].append('AGENTS.md')
        paths = ['README.md', 'AGENTS.md']
        self.assertEqual(self.check(paths), [])
        self.assertEqual(self.check(paths[::-1]), [])

    def test_unapproved_legacy_source_and_results(self):
        for name in ('legacy/model.cpp', 'results/summary.json', 'cache/state.bin'):
            with self.subTest(name=name):
                self.assertTrue(self.check(['README.md', name]))

    def test_allowlisting_cannot_override_forbidden_artifacts(self):
        for name in ('results/out.json', 'build/tool.exe', '.env', 'cache/item.pyc'):
            with self.subTest(name=name):
                self.manifest['groups']['governance'] = [name]
                self.assertTrue(self.check([name]))

    def test_secret_local_path_binary_and_invalid_utf8(self):
        values = ['gh' + 'p_' + 'x' * 36, '-----BEGIN ' + 'PRIVATE KEY-----',
                  '/' + 'home/person/private', 'C:' + '\\Users\\person\\private']
        for value in values:
            with self.subTest(kind=value[:8]):
                (self.root / 'README.md').write_text(value)
                errors = self.check()
                self.assertTrue(errors)
                self.assertNotIn(value, '\n'.join(errors))
        for value in (b'hello\x00world', b'\xff'):
            (self.root / 'README.md').write_bytes(value)
            self.assertTrue(self.check())

    def test_manifest_errors_and_path_traversal_fail_closed(self):
        for mutation in ({}, {'schema_version': 2, 'groups': {}},
                         {'schema_version': 1, 'groups': {'unknown': ['README.md']}},
                         {'schema_version': 1, 'groups': {'governance': ['README.md', 'README.md']}},
                         {'schema_version': 1, 'groups': {'governance': ['../outside']}}):
            with self.subTest(mutation=mutation):
                self.assertTrue(boundary.validate(self.root, mutation, ['README.md']))

    def test_missing_file_symlink_and_inventory_duplicates(self):
        (self.root / 'README.md').unlink()
        self.assertTrue(self.check())
        (self.root / 'README.md').symlink_to('missing-target')
        self.assertTrue(self.check())
        self.assertTrue(self.check(['README.md', 'README.md']))

    def test_cli_valid_invalid_and_malformed_manifest(self):
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        manifest = self.root / 'inventory.json'
        self.manifest['groups']['governance'].append('inventory.json')
        manifest.write_text(json.dumps(self.manifest))
        cmd = [sys.executable, str(ROOT / 'scripts/validate_repository_boundary.py'),
               '--root', str(self.root), '--manifest', 'inventory.json']
        good = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(good.returncode, 0, good.stderr)
        (self.root / 'unapproved.cpp').write_text('synthetic rejected fixture')
        bad = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(bad.returncode, 1)
        self.assertIn('unapproved path', bad.stderr)
        manifest.write_text('{')
        malformed = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(malformed.returncode, 1)
        self.assertNotIn('Traceback', malformed.stderr)


if __name__ == '__main__':
    unittest.main()
