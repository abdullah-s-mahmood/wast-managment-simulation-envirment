"""ADR completeness and declared material-change attacks, no semantic inference."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('change',ROOT/'scripts/validate_change_control.py')
c=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(c)


def synthetic(status='Accepted'):
    return '# ADR-9999 — SYNTHETIC\n\n- Status: '+status+'\n\n'+''.join('## '+h+'\nSynthetic software governance case.\n\n' for h in c.SECTIONS)


class ChangeTests(unittest.TestCase):
    def test_real_adrs_have_required_sections(self):
        self.assertEqual(c.validate_repository(ROOT),[])

    def test_every_section_nonempty_and_status_distinct(self):
        for status in ('Proposed','Provisional','Accepted','Rejected','Superseded'):
            self.assertEqual(c.inspect_adr(synthetic(status)),(status,[]))
        for section in c.SECTIONS:
            self.assertTrue(c.inspect_adr(synthetic().replace('## '+section,'## removed'))[1])
        self.assertTrue(c.inspect_adr(synthetic('unknown'))[1])
        self.assertTrue(c.inspect_adr(synthetic()+'\n- Status: unknown\n')[1])
        self.assertTrue(c.inspect_adr(synthetic()+'## Context\nDuplicate\n')[1])

    def test_hidden_dependency_and_public_contract_without_decision(self):
        for flag in c.FLAGS:
            change=dict.fromkeys(c.FLAGS,False); change.update(schema_version=1,decision_id=None,rationale='Synthetic proposed change')
            change[flag]=True
            self.assertTrue(c.check_change(change,{}))
            change['decision_id']='ADR-9999'
            for status in ('Proposed','Provisional','Rejected','Superseded'):
                self.assertTrue(c.check_change(change,{'ADR-9999':synthetic(status)}))
            self.assertEqual(c.check_change(change,{'ADR-9999':synthetic()}),[])

    def test_missing_unknown_wrong_types_and_routine(self):
        change=dict.fromkeys(c.FLAGS,False); change.update(schema_version=1,decision_id=None,rationale='Synthetic routine correction')
        self.assertEqual(c.check_change(change,{}),[])
        change[c.FLAGS[0]]=0
        self.assertTrue(c.check_change(change,{}))
        change.pop('decision_id')
        self.assertTrue(c.check_change(change,{}))

    def test_public_repository_cli(self):
        result=subprocess.run([sys.executable,str(ROOT/'scripts/validate_change_control.py')],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)


if __name__=='__main__': unittest.main()
