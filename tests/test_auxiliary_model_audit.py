"""Synthetic, independent fixtures for non-executing auxiliary expression audit."""
import hashlib
import io
import json
import subprocess
import sys
import tarfile
from pathlib import Path
import random
import tempfile
import unittest
from scripts import audit_auxiliary_models as audit
from scripts import inventory_legacy as intake


class AuxiliaryAuditTests(unittest.TestCase):
    def extract(self, text):
        return audit.python_expressions(text, {'entry_id':'entry-00000001', 'sha256':hashlib.sha256(text.encode()).hexdigest()})

    def test_defaults_guards_and_multiline_formula_have_exact_source(self):
        text='def f(x=7, *, y=3):\n if x<0: raise ValueError()\n result=(x +\n         y) / 2\n return result\n'
        rows=self.extract(text);data=text.encode()
        defaults=[data[r['byte_start']:r['byte_end']] for r in rows if r['syntax_role']=='parameter_default']
        self.assertEqual(defaults,[b'7',b'3'])
        formula=next(r for r in rows if r['syntax_role']=='assignment_value')
        self.assertEqual(data[formula['byte_start']:formula['byte_end']],b'(x +\n         y) / 2')
        self.assertEqual(formula['scientific_support'],'UNVALIDATED')

    def test_unicode_crlf_and_string_line_separator_do_not_shift_spans(self):
        for newline in ['\n','\r\n','\r']:
            text='label="α\u2028β"'+newline+'λ_mass = 3'+newline
            rows=self.extract(text);data=text.encode();last=rows[-1]
            self.assertEqual(data[last['byte_start']:last['byte_end']],b'3')
            self.assertEqual(last['line_start'],2)

    def test_source_comment_and_missing_constant_never_validate_or_normalize(self):
        rows=self.extract('# physically validated!\nmass=missing_constant * fill\n')
        self.assertIn('missing_constant',rows[0]['original_names'])
        self.assertEqual(rows[0]['missing_constants'],'NOT_FILLED')
        self.assertIsNone(rows[0]['normalization']);self.assertEqual(rows[0]['scientific_support'],'UNVALIDATED')

    def test_import_and_side_effect_code_are_not_executed(self):
        with tempfile.TemporaryDirectory() as d:
            marker=Path(d)/'NEVER'
            rows=self.extract(f'import absent_package\nopen({str(marker)!r},"w").write("BAD")\nx=5\n')
            self.assertTrue(rows);self.assertFalse(marker.exists())

    def test_generated_expression_hashes_replay_and_uniqueness(self):
        rng=random.Random(71)
        for _ in range(100):
            text=''.join(f'x{i}=({rng.randrange(100)} + {rng.randrange(100)})/2\n' for i in range(rng.randrange(1,30)))
            rows=self.extract(text);self.assertEqual(rows,self.extract(text));self.assertEqual(len(rows),len({r['id'] for r in rows}))
            for row in rows:self.assertEqual(row['span_sha256'],hashlib.sha256(text.encode()[row['byte_start']:row['byte_end']]).hexdigest())

    def test_bad_source_hash_and_malformed_syntax_fail_closed(self):
        with self.assertRaises(ValueError):audit.python_expressions('x=1',{'entry_id':'entry-00000001','sha256':'0'*64})
        with self.assertRaises(SyntaxError):self.extract('def broken(:')

    def test_cli_archive_boundary_and_parse_failure_emit_no_partial_manifest(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);arc=root/'a.tar.gz';ip=root/'intake.json';pp=root/'plan.json'
            for text,expected in [('default = 12\n',0),('def invalid(:',1)]:
                with tarfile.open(arc,'w:gz') as tar:
                    link=tarfile.TarInfo('p/unsafe');link.type=tarfile.SYMTYPE;link.linkname='/outside';tar.addfile(link)
                    item=tarfile.TarInfo('p/scenario.py');item.size=len(text.encode());tar.addfile(item,io.BytesIO(text.encode()))
                before=arc.read_bytes();manifest=intake.inspect(arc,intake.DEFAULTS);ip.write_text(json.dumps(manifest))
                plan={'schema_version':1,'records':[{'id':'fixture','entry_id':'entry-00000001','source_sha256':hashlib.sha256(text.encode()).hexdigest(),'line_start':1,'line_end':1,'category':'default','observation':'Synthetic fixture'}]};pp.write_text(json.dumps(plan))
                result=subprocess.run([sys.executable,str(Path(audit.__file__).resolve()),str(arc),str(ip),str(pp),'--project-root','p'],cwd='/',capture_output=True,timeout=10)
                self.assertEqual(result.returncode,expected,result.stderr);self.assertEqual(before,arc.read_bytes())
                if expected:self.assertEqual(result.stdout,b'')
                else:
                    out=json.loads(result.stdout);self.assertTrue(intake.verify_manifest(out));self.assertEqual(len(out['files']),1);self.assertEqual(out['scientific_validation'],'UNVALIDATED')

    def test_unassigned_call_arguments_remain_traceable(self):
        text='configure("--rate", "123", fallback=7)\n'
        rows=self.extract(text)
        call=next(r for r in rows if r['syntax_role']=='call_expression')
        self.assertEqual(text.encode()[call['byte_start']:call['byte_end']],text.strip().encode())
        self.assertEqual(call['intended_behavior'],'UNAVAILABLE')

    def test_expression_budget_aborts(self):
        with self.assertRaises(ValueError):self.extract('x=1\n'*10001)

    def test_contexts_keep_scenarios_tests_and_analysis_separate(self):
        self.assertEqual(audit.context('p/tests/core.cpp','p',{'test_path_candidate'}),'test_fixture_or_probe')
        self.assertEqual(audit.context('p/experiments/stats.py','p',set()),'experiment_or_analysis')
        self.assertEqual(audit.context('p/scripts/map.py','p',set()),'auxiliary_tool_or_scenario')
        self.assertEqual(audit.context('p/run.sh','p',set()),'shell_orchestration')
        self.assertEqual(audit.context('p/CMakeLists.txt','p',set()),'build_registration')


if __name__=='__main__':unittest.main()
