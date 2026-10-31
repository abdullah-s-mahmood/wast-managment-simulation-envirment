"""Independent negative-evidence fixtures; never execute or repair legacy code."""
import copy
import hashlib
import json
import random
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from scripts import audit_discrepancies as audit


class DiscrepancyTests(unittest.TestCase):
    def fixture(self,root):
        outcome={'audit_report_status':'ACCEPTED_FAILED_REPRODUCTION_REPORT','scientific_validation':'UNVALIDATED','source_changes':False,'actual_exits':[3,3],'route_complete':[False,False],'validation_only_flags':[True,True],'raw_output_sha256':[],'private_evidence_receipts':{},'event_difference_inventory':{'different_field_paths':{'/wall':1}},'raw_summary_different_keys':['runtime']}
        for i,label in enumerate(('BASELINE_A-1','BASELINE_B-1')):
            result=root/(label+'.result.json');result.write_text(json.dumps({'attempted':True,'termination':'exited','process_exit':3}));outcome['private_evidence_receipts'][result.name]=hashlib.sha256(result.read_bytes()).hexdigest()
            folder=root/(label+'.export')/'baseline';folder.mkdir(parents=True)
            (folder/'events.jsonl').write_text(json.dumps({'wall':i,'semantic_value':7})+'\n')
            (folder/'run_summary.json').write_text(json.dumps({'route_complete':False,'validation_only':True,'runtime':i}))
            outcome['raw_output_sha256'].append({name:hashlib.sha256((folder/name).read_bytes()).hexdigest() for name in ('events.jsonl','run_summary.json')})
        return outcome
    def test_retained_reproduction_is_read_only_and_not_new_simulation(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);outcome=self.fixture(root);before={str(p):p.read_bytes() for p in root.rglob('*') if p.is_file()}
            out=audit.reproduce(root,outcome)
            self.assertTrue(all(out['findings'].values()));self.assertEqual(out['normal_runs_executed_now'],0)
            self.assertFalse(out['legacy_changes']);self.assertFalse(out['historical_results_imported'])
            self.assertEqual(before,{str(p):p.read_bytes() for p in root.rglob('*') if p.is_file()})
            self.assertEqual(out['scientific_validation'],'UNVALIDATED')
    def test_changed_artifact_and_unverified_history_cannot_be_imported(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);outcome=self.fixture(root)
            with self.assertRaises(ValueError):audit.reproduce(root,dict(outcome,audit_report_status='HISTORICAL_PASSED'))
            result=root/'BASELINE_A-1.result.json';original=result.read_bytes();modified=json.loads(original);modified['process_exit']=3.0;result.write_text(json.dumps(modified));changed=copy.deepcopy(outcome);changed['private_evidence_receipts'][result.name]=hashlib.sha256(result.read_bytes()).hexdigest()
            with self.assertRaises(ValueError):audit.reproduce(root,changed)
            result.write_bytes(original)
            path=root/'BASELINE_A-1.export/baseline/events.jsonl';path.write_text('{"new":true}\n')
            with self.assertRaises(ValueError):audit.reproduce(root,outcome)
    def test_symlink_and_budget_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);target=root/'target';target.write_bytes(b'x');link=root/'link';link.symlink_to(target)
            with self.assertRaises(OSError):audit.frozen_bytes(link,hashlib.sha256(b'x').hexdigest())
            with self.assertRaises(ValueError):audit.frozen_bytes(target,'0'*64)
            with patch.object(audit,'MAX_BYTES',0),self.assertRaises(ValueError):audit.frozen_bytes(target,hashlib.sha256(b'x').hexdigest())
    def test_register_disallows_repair_import_promotion_and_duplicates(self):
        original=json.loads((Path(audit.ROOT)/'docs/audit/S015_DISCREPANCY_REGISTER.json').read_text())
        self.assertEqual(audit.validate_register(original)['issues'],3)
        for key,value in [('mode','REPAIR'),('legacy_action','PATCH'),('historical_results_use','IMPORT_AS_VALIDATED'),('scientific_validation','VALIDATED')]:
            with self.subTest(key=key),self.assertRaises(ValueError):audit.validate_register(dict(original,**{key:value}))
        data=copy.deepcopy(original);data['issues'].append(data['issues'][0])
        with self.assertRaises(ValueError):audit.validate_register(data)
        data=copy.deepcopy(original);data['issues'][0]['impacts'].pop('random_streams')
        with self.assertRaises(ValueError):audit.validate_register(data)
    def test_structural_difference_does_not_normalize_semantic_change(self):
        self.assertEqual(audit.differences({'state':7,'wall':1},{'state':8,'wall':2}),['/state','/wall'])
        self.assertEqual(audit.differences({'a/b':1},{'a/b':True}),['/a~1b'])
        self.assertEqual(audit.differences([1],[1,2]),[''])
    def test_generated_difference_paths_are_order_invariant_without_hiding_change(self):
        rng=random.Random(15)
        for _ in range(100):
            original={f'field_{i}':rng.randrange(100) for i in range(10)}
            reordered=dict(reversed(list(original.items())))
            self.assertEqual(audit.differences(original,reordered),[])
            key=rng.choice(list(original));reordered[key]+=1
            self.assertEqual(audit.differences(original,reordered),['/'+key])

    def test_cli_has_no_repair_or_import_feature(self):
        for flag in ('--repair-legacy','--import-results'):
            result=subprocess.run([sys.executable,str(Path(audit.__file__).resolve()),flag],cwd='/',capture_output=True)
            self.assertEqual(result.returncode,2);self.assertEqual(result.stdout,b'')


if __name__=='__main__':unittest.main()
