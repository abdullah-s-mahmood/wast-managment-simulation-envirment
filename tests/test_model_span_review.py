"""Synthetic source-span review fixtures, independent of legacy implementation."""
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest
from scripts import inventory_legacy as intake
from scripts import review_model_spans as review


class SpanReviewTests(unittest.TestCase):
    def fixture(self):
        text = '// α unit not specified\nvalue = (source +\n    1.25e-3) / dt;\n'
        item = {'entry_id': 'entry-00000000', 'sha256': hashlib.sha256(text.encode()).hexdigest()}
        row = {'id': 'OBS_1', 'entry_id': item['entry_id'], 'source_sha256': item['sha256'],
               'line_start': 2, 'line_end': 3, 'category': 'equation', 'observation': 'Synthetic multiline update; units unresolved.'}
        return text, item, row

    def test_multiline_exact_byte_span_and_original_names(self):
        text, item, row = self.fixture(); out = review.resolve(row, item, text)
        span = text.encode()[out['byte_start']:out['byte_end']]
        self.assertEqual(span, b'value = (source +\n    1.25e-3) / dt;\n')
        self.assertEqual(out['span_sha256'], hashlib.sha256(span).hexdigest())
        self.assertEqual(out['original_numeric_spellings'], ['1.25e-3'])
        self.assertIn('value', out['original_names']); self.assertIsNone(out['normalized_expression'])

    def test_unicode_line_boundaries_and_digit_separators(self):
        text = "// α\u2028value = 37'000 + 1_000;\n"
        _, item, row = self.fixture()
        item['sha256'] = hashlib.sha256(text.encode()).hexdigest()
        row.update(source_sha256=item['sha256'], line_start=2, line_end=2)
        out = review.resolve(row, item, text)
        self.assertEqual(out['byte_start'], len("// α\u2028".encode()))
        self.assertEqual(out['original_numeric_spellings'], ["37'000", '1_000'])
        for key, value in [('category', []), ('category', None), ('line_end', float('inf'))]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                review.validate_plan({'schema_version': 1, 'records': [dict(row, **{key: value})]})

    def test_duplicate_missing_unsupported_and_boolean_plan_rejected(self):
        _, _, row = self.fixture()
        for plan in [{'schema_version': True, 'records': [row]}, {'schema_version': 2, 'records': [row]},
                     {'schema_version': 1, 'records': []}, {'schema_version': 1, 'records': [row, row]}]:
            with self.subTest(plan=plan), self.assertRaises(ValueError): review.validate_plan(plan)
        for key, value in [('line_start', True), ('line_end', 1000), ('line_start', 0), ('source_sha256', 'bad')]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                review.validate_plan({'schema_version': 1, 'records': [dict(row, **{key: value})]})

    def test_no_intuitive_constant_or_comment_validation(self):
        text, item, row = self.fixture()
        for key, value in [('scientific_support', 'VALIDATED'), ('normalized_expression', 'value=10'), ('units', 'kg')]:
            with self.subTest(key=key), self.assertRaises(ValueError): review.resolve(dict(row, **{key: value}), item, text)
        out = review.resolve(dict(row, observation='Comment claims scientific validation'), item, text)
        self.assertEqual(out['scientific_support'], 'UNVALIDATED')
        self.assertEqual(out['intended_behavior'], 'UNAVAILABLE')

    def test_changed_source_out_of_bounds_and_span_budget(self):
        text, item, row = self.fixture()
        with self.assertRaises(ValueError): review.resolve(row, item, text + 'changed')
        with self.assertRaises(ValueError): review.resolve(dict(row, line_end=4), item, text)
        text = 'x=' + '1'*8192; item['sha256'] = hashlib.sha256(text.encode()).hexdigest()
        row.update(source_sha256=item['sha256'], line_start=1, line_end=1)
        with self.assertRaises(ValueError): review.resolve(row, item, text)

    def test_cli_full_archive_identity_missing_source_and_no_execution(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); archive = root/'a.tar.gz'; marker = root/'NEVER'
            text = f'open({str(marker)!r},"w").write("NO")\nvalue = 7\n'
            with tarfile.open(archive, 'w:gz') as tar:
                info = tarfile.TarInfo('p/model.py'); info.size = len(text.encode()); tar.addfile(info, io.BytesIO(text.encode()))
            before = archive.read_bytes(); manifest = intake.inspect(archive, intake.DEFAULTS)
            _, _, row = self.fixture(); row.update(source_sha256=hashlib.sha256(text.encode()).hexdigest(), line_start=2, line_end=2)
            plan = {'schema_version': 1, 'records': [row]}; ip = root/'intake.json'; pp = root/'plan.json'
            ip.write_text(json.dumps(manifest)); pp.write_text(json.dumps(plan))
            command = [sys.executable, str(Path(review.__file__).resolve()), str(archive), str(ip), str(pp), '--project-root', 'p']
            result = subprocess.run(command, cwd='/', capture_output=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr); out = json.loads(result.stdout)
            self.assertTrue(out['selected_ranges_complete']); self.assertFalse(out['whole_project_extraction_complete'])
            self.assertTrue(intake.verify_manifest(out)); self.assertEqual(before, archive.read_bytes()); self.assertFalse(marker.exists())
            plan['records'][0]['entry_id'] = 'entry-99999999'; pp.write_text(json.dumps(plan))
            result = subprocess.run(command, cwd='/', capture_output=True, timeout=10)
            self.assertEqual(result.returncode, 1); self.assertEqual(result.stdout, b'')
            self.assertIn(b'INCOMPLETE_PRIVATE_REVIEW', result.stderr)


if __name__ == '__main__': unittest.main()
