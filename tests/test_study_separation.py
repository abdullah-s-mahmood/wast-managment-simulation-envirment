"""Documented governance boundary; does not execute a simulation."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('scripts.separation', ROOT / 'scripts/validate_study_separation.py')
separation = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(separation)
MODEL = ROOT / 'tests/fixtures/classification/model.json'


def proposal():
    return {'governance_version': 1,
            'model_sha256': hashlib.sha256(MODEL.read_bytes()).hexdigest(),
            'settings': {'population': 'synthetic population A', 'map': 'synthetic map A',
                         'bin_count': 'synthetic count A', 'fleet_size': 'synthetic fleet A',
                         'depot_placement': 'synthetic placement A'},
            'factor_roles': {key: 'manipulated' for key in separation.SETTINGS},
            'measurements': ['internal_event_count'], 'outcomes': ['derived_event_total']}


class SeparationTests(unittest.TestCase):
    def test_settings_vary_without_model_rewrite(self):
        baseline = MODEL.read_bytes()
        before = proposal()
        for key in separation.SETTINGS:
            after = copy.deepcopy(before)
            after['settings'][key] = 'synthetic alternative B'
            self.assertEqual(separation.validate(after, MODEL), [])
            self.assertEqual(MODEL.read_bytes(), baseline)
            self.assertEqual(after['model_sha256'], before['model_sha256'])

    def test_model_override_or_hash_change_fails(self):
        for section in ('settings', None):
            value = proposal()
            target = value if section is None else value[section]
            target['hypotheses'] = ['rewritten scientific behavior']
            self.assertTrue(separation.validate(value, MODEL))
        value = proposal(); value['model_sha256'] = '0' * 64
        self.assertTrue(separation.validate(value, MODEL))
        with tempfile.TemporaryDirectory() as directory:
            changed = Path(directory) / 'model.json'
            changed.write_bytes(MODEL.read_bytes() + b' ')
            self.assertTrue(separation.validate(proposal(), changed))

    def test_missing_extra_duplicate_and_wrong_fields(self):
        for key in proposal():
            value = proposal(); del value[key]
            self.assertTrue(separation.validate(value, MODEL))
        for key, item in (('governance_version', True), ('governance_version', 2),
                          ('settings', None), ('factor_roles', {}), ('measurements', []),
                          ('outcomes', ['x', 'x']), ('outcomes', ['internal_event_count'])):
            value = proposal(); value[key] = item
            self.assertTrue(separation.validate(value, MODEL))
        value = proposal(); value['factor_roles']['population'] = 'causal_effect'
        self.assertTrue(separation.validate(value, MODEL))

    def test_order_metamorphism_and_cli(self):
        value = proposal()
        value['settings'] = dict(reversed(list(value['settings'].items())))
        self.assertEqual(separation.validate(value, MODEL), [])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'proposal.json'
            cmd = [sys.executable, str(ROOT / 'scripts/validate_study_separation.py'), str(path), '--model', str(MODEL)]
            path.write_text(json.dumps(value))
            result = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            for data in ('{', '{"governance_version":1,"governance_version":1}', '{"settings":NaN}'):
                path.write_text(data)
                result = subprocess.run(cmd, capture_output=True, text=True)
                self.assertEqual(result.returncode, 1)
                self.assertNotIn('Traceback', result.stderr)
                self.assertEqual(path.read_text(), data)

    def test_classification_table_coverage(self):
        text = (ROOT / 'docs/HYPOTHESES_AND_SETTINGS.md').read_text()
        for item in ('population', 'map', 'bin_count', 'fleet_size', 'depot_placement',
                     'hypothesis', 'control', 'measurement', 'outcome', 'telemetry',
                     'specification', 'runtime_state', 'not a causal inference'):
            self.assertIn(item, text)


if __name__ == '__main__':
    unittest.main()
