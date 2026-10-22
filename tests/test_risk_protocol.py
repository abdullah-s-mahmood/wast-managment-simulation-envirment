"""Risk completeness and exhaustive six-flag fail-closed escalation checks."""
import importlib.util
import itertools
from pathlib import Path
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('scripts.risk',ROOT/'scripts/validate_risk_protocol.py')
r=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(r)


class RiskTests(unittest.TestCase):
    def test_register_and_public_cli(self):
        self.assertEqual(r.validate_register(r.read_json(ROOT/'docs/quality/risks.json')),[])
        result=subprocess.run([sys.executable,str(ROOT/'scripts/validate_risk_protocol.py')],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)

    def test_all_flag_combinations_never_bypass_critical_stop(self):
        for values in itertools.product((False,True),repeat=len(r.FACTS)):
            facts=dict(zip(r.FACTS,values)); action=r.next_action(facts)
            if facts['corrupt_results']:
                self.assertEqual(action,'stop_pipeline_preserve_failed_run')
            elif not facts['scientific_evidence_available'] or facts['guessed_scientific_value']:
                self.assertEqual(action,'stop_and_record_blocker')
            elif facts['irreversible'] and not facts['explicit_authorization']:
                self.assertEqual(action,'request_specific_authorization')
            elif facts['test_failure']:
                self.assertEqual(action,'investigate_and_retest')
            else: self.assertEqual(action,'continue_within_contract')

    def test_guessed_value_or_irreversible_change_cannot_escape_blocker(self):
        facts=dict.fromkeys(r.FACTS,False)
        self.assertEqual(r.next_action(facts),'stop_and_record_blocker')
        facts.update(guessed_scientific_value=True,irreversible=True,explicit_authorization=True)
        self.assertEqual(r.next_action(facts),'stop_and_record_blocker')
        facts.update(scientific_evidence_available=True,guessed_scientific_value=False,explicit_authorization=False)
        self.assertEqual(r.next_action(facts),'request_specific_authorization')

    def test_malformed_missing_unknown_and_wrong_types(self):
        for facts in ({},None,dict.fromkeys(r.FACTS,0),dict.fromkeys(r.FACTS,False)|{'unknown':False}):
            with self.assertRaises(ValueError): r.next_action(facts)
        data=r.read_json(ROOT/'docs/quality/risks.json')
        for key in data['risks'][0]:
            changed=r.read_json(ROOT/'docs/quality/risks.json'); del changed['risks'][0][key]
            self.assertTrue(r.validate_register(changed))
        data['risks'].append(data['risks'][0]); self.assertTrue(r.validate_register(data))
        data['schema_version']=True; self.assertTrue(r.validate_register(data))


if __name__=='__main__': unittest.main()
