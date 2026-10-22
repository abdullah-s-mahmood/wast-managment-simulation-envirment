"""S003 contract tests use synthetic local sources, never scientific citations."""
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
SPEC = importlib.util.spec_from_file_location('evidence', ROOT / 'scripts/validate_evidence_ledger.py')
evidence = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(evidence)
CONTRACT = evidence.read_json(ROOT / 'docs/evidence/record_contract.json')


def synthetic_record():
    record = dict.fromkeys(CONTRACT['record_string_fields'], 'not_applicable: synthetic contract test')
    record.update(id='EV-SYNTHETIC-001', kind='parameter', evidence_class='E5',
                  claim='Synthetic scale factor trace', equation='scale_factor = 1',
                  citation='Local synthetic software fixture; no publication',
                  source_url='fixture:tests/fixtures/evidence/synthetic_source.json',
                  source_path='tests/fixtures/evidence/synthetic_source.json',
                  source_version='1', access_date='2026-10-22',
                  source_location='/parameters/scale_factor',
                  source_sha256=hashlib.sha256((ROOT / 'tests/fixtures/evidence/synthetic_source.json').read_bytes()).hexdigest(),
                  verification_status='synthetic',
                  verification_artifact='docs/evidence/README.md',
                  config_path='tests/fixtures/evidence/synthetic_config.json',
                  config_pointer='/scale_factor', reference_test='tests/test_evidence_ledger.py',
                  decision='synthetic', domain_transfer_required=False,
                  variables=[dict(symbol='scale_factor', definition='Synthetic identity factor', units='1', valid_range='exactly 1')])
    return record


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.record = synthetic_record()

    def check(self, production=False):
        return evidence.validate(dict(schema_version=1, records=[self.record]), CONTRACT, production=production)

    def test_source_config_reference_trace(self):
        self.assertEqual(self.check(), [])
        source = evidence.read_json(ROOT / self.record['source_url'].removeprefix('fixture:'))
        config = evidence.read_json(ROOT / self.record['config_path'])
        source_parameter = evidence.resolve_pointer(source, self.record['source_location'])
        config_parameter = evidence.resolve_pointer(config, self.record['config_pointer'])
        self.assertEqual(source_parameter['value'], config_parameter['value'])
        self.assertEqual(source_parameter['units'], config_parameter['units'])
        self.assertEqual(config_parameter['evidence_id'], self.record['id'])
        self.assertEqual(self.record['variables'][0]['units'], source_parameter['units'])

    def test_every_required_field_and_unknown_fields(self):
        for key in self.record:
            record = copy.deepcopy(self.record)
            del record[key]
            with self.subTest(key=key):
                self.assertTrue(evidence.validate(dict(schema_version=1, records=[record]), CONTRACT, production=False))
        self.record['unexpected'] = 'rejected'
        self.assertTrue(self.check())

    def test_empty_or_wrong_type_fields(self):
        for key in CONTRACT['record_string_fields']:
            for value in ('', '   ', None, 12, [], {}):
                original = self.record[key]
                self.record[key] = value
                with self.subTest(key=key, value=value):
                    self.assertTrue(self.check())
                self.record[key] = original

    def test_units_range_and_variables(self):
        for value in ([], None, [{}], [dict(symbol='x', definition='x', units='', valid_range='all')]):
            self.record['variables'] = value
            self.assertTrue(self.check())
        self.record['variables'] = [dict(symbol='x', definition='x', units='1', valid_range='all')] * 2
        self.assertTrue(self.check())

    def test_unverifiable_source_and_unsupported_acceptance(self):
        self.record.update(decision='accepted_for_implementation', verification_status='unverified', source_url='not-a-citation')
        self.assertTrue(self.check(production=True))
        self.record.update(verification_status='verified', source_url='https://example.invalid/fabricated')
        self.assertTrue(self.check(production=True))  # E5 cannot support acceptance.

    def test_domain_transfer_requires_explanation(self):
        self.record.update(domain_transfer_required=True)
        self.assertTrue(self.check())
        self.record.update(transfer_rationale='Synthetic domain comparison only; no physical claim')
        self.assertEqual(self.check(), [])
        self.record.update(evidence_class='E3', domain_transfer_required=False)
        self.assertTrue(self.check())

    def test_ids_versions_dates_and_booleans(self):
        ledger = dict(schema_version=1, records=[self.record, self.record])
        self.assertTrue(evidence.validate(ledger, CONTRACT, production=False))
        for version in (True, 0, 2, '1'):
            self.assertTrue(evidence.validate(dict(schema_version=version, records=[]), CONTRACT))
        for key, value in (('id', 'bad'), ('access_date', '2026-02-30'), ('access_date', '20261022'), ('domain_transfer_required', 1), ('doi', 'invented')):
            record = copy.deepcopy(self.record); record[key] = value
            self.assertTrue(evidence.validate(dict(schema_version=1, records=[record]), CONTRACT, production=False))

    def test_mapping_path_and_pointer_attacks(self):
        for key, value in (('config_path', '../outside.json'), ('config_path', '/absolute.json'),
                           ('reference_test', 'missing.py'), ('config_pointer', '/missing'),
                           ('config_pointer', '/~2'), ('source_sha256', '0' * 64)):
            record = copy.deepcopy(self.record); record[key] = value
            with self.subTest(key=key, value=value):
                self.assertTrue(evidence.validate(dict(schema_version=1, records=[record]), CONTRACT, production=False))

    def test_pointer_escapes_and_array_boundaries(self):
        value = {'a/b': {'~': [17]}}
        self.assertEqual(evidence.resolve_pointer(value, '/a~1b/~0/0'), 17)
        for pointer in ('', 'x', '/a~2b', '/a~1b/~0/01', '/a~1b/~0/-1', '/a~1b/~0/1'):
            with self.assertRaises((ValueError, KeyError, IndexError)):
                evidence.resolve_pointer(value, pointer)

    def test_order_invariance_and_synthetic_exclusion(self):
        self.assertTrue(self.check(production=True))
        reversed_record = dict(reversed(list(self.record.items())))
        self.assertEqual(evidence.validate(dict(records=[reversed_record], schema_version=1), CONTRACT, production=False), [])

    def test_cli_invalid_json_and_no_output_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'ledger.json'
            cmd = [sys.executable, str(ROOT / 'scripts/validate_evidence_ledger.py'), str(path)]
            for content in ('{', '{"schema_version":1,"schema_version":1,"records":[]}', '{"schema_version":1,"records":[NaN]}', '{"schema_version":1,"records":[Infinity]}'):
                path.write_text(content)
                result = subprocess.run(cmd, capture_output=True, text=True)
                self.assertEqual(result.returncode, 1)
                self.assertNotIn('Traceback', result.stderr)
                self.assertEqual(path.read_text(), content)
                self.assertEqual(list(Path(directory).iterdir()), [path])
            path.write_text('{"schema_version":1,"records":[]}')
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 0)


if __name__ == '__main__':
    unittest.main()
