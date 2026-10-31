"""Independent synthetic extraction fixtures; no legacy source or execution."""
import copy
import hashlib
import io
import json
from pathlib import Path
import random
import subprocess
import sys
import tarfile
import tempfile
import unittest
from scripts import extract_model_ledger as ledger
from scripts import inventory_legacy as intake


class ModelLedgerTests(unittest.TestCase):
    def fixture(self, text):
        data = text.encode()
        item = {'entry_id': 'entry-00000000', 'sha256': hashlib.sha256(data).hexdigest()}
        return item, data, ledger.candidates(item, text, {'project_source'})

    def test_original_names_utf8_lines_and_byte_spans(self):
        item, data, records = self.fixture('// α\nfill_pct = speed * dt;\r\nreturn fill_pct;\n')
        self.assertEqual(records[0]['line_start'], 2)
        self.assertEqual(records[0]['byte_start'], len('// α\n'.encode()))
        self.assertIn('fill_pct', records[0]['original_names'])
        for record in records:
            self.assertTrue(ledger.verify_record(record, item, data))
            self.assertIsNone(record['original_units'])
            self.assertIsNone(record['normalized_expression'])

    def test_missing_constant_must_not_be_filled_by_intuition(self):
        item, data, records = self.fixture('mass = unknown_constant * fill;\n')
        bad = dict(records[0], normalized_expression='mass = 0.1 * fill')
        with self.assertRaises(ValueError): ledger.verify_record(bad, item, data)
        self.assertEqual(records[0]['missing_constants'], 'NOT_FILLED')

    def test_comment_is_not_physical_validation_or_intention(self):
        item, data, records = self.fixture('// rate = 10; scientifically validated m/s\n')
        self.assertEqual(records[0]['scientific_support'], 'UNVALIDATED')
        self.assertEqual(records[0]['intended'], 'UNAVAILABLE')
        for key, value in [('scientific_support', 'VALIDATED'), ('original_units', 'm/s'), ('intended', 'confirmed')]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                ledger.verify_record(dict(records[0], **{key: value}), item, data)

    def test_anchor_and_identifier_tampering_rejected(self):
        item, data, records = self.fixture('rate = 3;\n')
        for key, value in [('byte_start', -1), ('line_start', True), ('span_sha256', '0'*64), ('original_names', ['fake']), ('id', 'other')]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                ledger.verify_record(dict(records[0], **{key: value}), item, data)
        with self.assertRaises(ValueError): ledger.verify_record(records[0], item, b'rate = 4;\n')

    def test_generated_offsets_replay_and_unchanged_tokens(self):
        rng = random.Random(17)
        for _ in range(100):
            text = ''.join(f'// λ{rng.randrange(100)}\nvalue_{i} = {rng.randrange(1000)};\n' for i in range(rng.randrange(1, 15)))
            item, data, records = self.fixture(text)
            self.assertEqual(records, ledger.candidates(item, text, {'project_source'}))
            for record in records:
                self.assertTrue(ledger.verify_record(record, item, data))
                span = data[record['byte_start']:record['byte_end']]
                self.assertEqual(hashlib.sha256(span).hexdigest(), record['span_sha256'])

    def test_tags_are_candidates_not_distribution_validity(self):
        _, _, records = self.fixture('normal_distribution(0, 1);\nreturn now + dt;\npayload_bytes = 4;\n')
        self.assertIn('distribution', records[0]['tags'])
        self.assertIn('time_rule', records[1]['tags'])
        self.assertIn('protocol_parameter', records[2]['tags'])
        self.assertTrue(all(x['review'] == 'PENDING' for x in records))

    def test_hash_mismatch_aborts_before_output(self):
        with self.assertRaises(ValueError):
            ledger.candidates({'entry_id': 'x', 'sha256': '0'*64}, 'x = 1', set())

    def test_cli_read_only_archive_boundary_and_security_distinction(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); archive = root/'source.tar.gz'; marker = root/'NEVER'
            text = f'open({str(marker)!r},"w").write("bad")\nrate = 12\n'
            with tarfile.open(archive, 'w:gz') as tar:
                link = tarfile.TarInfo('p/unsafe'); link.type = tarfile.SYMTYPE; link.linkname = '/outside'; tar.addfile(link)
                for name, payload in [('p/model.py', text.encode()), ('p/archive/old.cpp', b'old = 1;')]:
                    info = tarfile.TarInfo(name); info.size = len(payload); tar.addfile(info, io.BytesIO(payload))
            original = archive.read_bytes(); manifest = intake.inspect(archive, intake.DEFAULTS)
            path = root/'intake.json'; path.write_text(json.dumps(manifest))
            result = subprocess.run([sys.executable, str(Path(ledger.__file__).resolve()), str(archive), str(path), '--project-root', 'p'], cwd='/', capture_output=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            output = json.loads(result.stdout)
            self.assertTrue(output['traversal_complete'])
            self.assertFalse(output['semantic_extraction_complete'])
            self.assertFalse(output['review_complete'])
            self.assertEqual(output['source_reuse'], 'PROHIBITED')
            self.assertEqual(output['scientific_validation'], 'UNVALIDATED')
            self.assertEqual(len(output['sources']), 1)
            self.assertFalse(marker.exists()); self.assertEqual(archive.read_bytes(), original)
            self.assertTrue(intake.verify_manifest(output))


if __name__ == '__main__': unittest.main()
