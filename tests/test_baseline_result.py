"""Synthetic artifacts, no legacy execution or scientific measurements."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from scripts import validate_baseline_result as b


class BaselineResultTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.record={'schema_version':1,'attempted':True,'process_exit':0,'termination':'exited',
                     'dependencies_verified':True,'inputs_verified':True,'binary_sha256':b.BINARY_SHA,
                     'expected_seed':7,'expected_run_id':'synthetic'}
        self.summary={'route_complete':True,'validation_only':False,'seed':7,'run_id':'synthetic',
                      'simulation_runtime_seconds':0.1,'unmodified_metric':123}
        self.event={'seed':7,'run_id':'synthetic','time_s':0,'kind':'synthetic'}
        (self.root/'run_summary.json').write_text(json.dumps(self.summary))
        (self.root/'events.jsonl').write_text(json.dumps(self.event)+'\n')

    def test_complete_synthetic_evidence_and_files_remain_unchanged(self):
        before={p.name:p.read_bytes() for p in self.root.iterdir()}
        errors,hashes,projection=b.validate(self.record,self.root)
        self.assertEqual(errors,[]);self.assertEqual(set(hashes),set(before));self.assertEqual(len(projection),64)
        self.assertEqual(before,{p.name:p.read_bytes() for p in self.root.iterdir()})

    def test_no_launch_missing_dependencies_nonzero_or_signalled_never_success(self):
        for key,values in {'schema_version':[True,'1'],'attempted':[False,None],'dependencies_verified':[False,'true'],
                           'inputs_verified':[False],'process_exit':[1,3,-9,True],
                           'termination':['timeout','signal'],'binary_sha256':['0'*64]}.items():
            for value in values:
                record=copy.deepcopy(self.record);record[key]=value
                with self.subTest(key=key,value=value):self.assertTrue(b.validate(record,self.root)[0])

    def test_success_exit_without_artifacts_fails(self):
        (self.root/'run_summary.json').unlink()
        self.assertTrue(b.validate(self.record,self.root)[0])

    def test_summary_noncompletion_or_validation_mode_is_not_normal_baseline(self):
        for key,value in [('route_complete',False),('validation_only',True),('seed',True),
                          ('simulation_runtime_seconds',float('nan')),('run_id','other')]:
            summary=dict(self.summary);summary[key]=value
            (self.root/'run_summary.json').write_text(json.dumps(summary))
            with self.subTest(key=key):self.assertTrue(b.validate(self.record,self.root)[0])

    def test_failure_artifact_links_and_empty_events_rejected(self):
        (self.root/'failure.json').write_text('{}');self.assertTrue(b.validate(self.record,self.root)[0])
        (self.root/'failure.json').unlink();(self.root/'link').symlink_to('/outside')
        self.assertTrue(b.validate(self.record,self.root)[0]);(self.root/'link').unlink()
        (self.root/'events.jsonl').write_text('');self.assertTrue(b.validate(self.record,self.root)[0])

    def test_duplicate_keys_and_nonfinite_constants_rejected(self):
        for data in ['{"a":1,"a":2}','{"a":NaN}','{"a":Infinity}']:
            with self.assertRaises(ValueError):b.strict_json(data)

    def test_output_budgets_fail_instead_of_truncating(self):
        with patch.object(b,'MAX_BYTES',1):self.assertTrue(b.validate(self.record,self.root)[0])
        with patch.object(b,'MAX_LINE_BYTES',2):self.assertTrue(b.validate(self.record,self.root)[0])

    def test_excessive_output_entries_fail_closed(self):
        for i in range(65):(self.root/('extra'+str(i))).touch()
        self.assertTrue(b.validate(self.record,self.root)[0])

    def test_wrong_event_identity_time_and_malformed_json_fail_closed(self):
        for key,value in [('run_id','other'),('seed',True),('time_s',-1),('time_s',float('inf')),('kind','')]:
            event=dict(self.event);event[key]=value
            (self.root/'events.jsonl').write_text(json.dumps(event)+'\n')
            with self.subTest(key=key,value=value):self.assertTrue(b.validate(self.record,self.root)[0])
        (self.root/'events.jsonl').write_text('{broken')
        self.assertTrue(b.validate(self.record,self.root)[0])

    def test_only_host_runtime_is_projected_out_raw_hash_still_changes(self):
        first=b.validate(self.record,self.root)
        summary=dict(self.summary);summary['simulation_runtime_seconds']=0.2
        (self.root/'run_summary.json').write_text(json.dumps(summary));second=b.validate(self.record,self.root)
        self.assertNotEqual(first[1]['run_summary.json'],second[1]['run_summary.json'])
        self.assertEqual(first[2],second[2])
        summary['unmodified_metric']=124;(self.root/'run_summary.json').write_text(json.dumps(summary))
        self.assertNotEqual(second[2],b.validate(self.record,self.root)[2])

    def test_cli_from_other_cwd_rejects_nonattempt_without_execution(self):
        record=dict(self.record,attempted=False);path=self.root/'record.json';path.write_text(json.dumps(record))
        script=Path(b.__file__).resolve()
        result=subprocess.run([sys.executable,str(script),str(path),str(self.root)],cwd='/',capture_output=True)
        self.assertEqual(result.returncode,1)
        self.assertEqual(json.loads(result.stdout)['status'],'INVALID_BASELINE')


if __name__=='__main__':unittest.main()
