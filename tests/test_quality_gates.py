"""Synthetic gate attacks; metadata is never presented as a real execution."""
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
SPEC = importlib.util.spec_from_file_location('scripts.quality', ROOT / 'scripts/validate_quality_gates.py')
q = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(q)


class QualityGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'evidence.txt').write_text('SYNTHETIC gate evidence; no command was run')
        digest = hashlib.sha256((self.root / 'evidence.txt').read_bytes()).hexdigest()
        self.head = 'a' * 40
        self.manifest = {'schema_version':1,'head_sha':self.head,'checks':[
            {'id':key,'status':'PASS','command':'synthetic command, not executed',
             'assertion':'synthetic assertion','artifact':'evidence.txt','sha256':digest,
             'exit_code':0,'platform':'synthetic','versions':'synthetic',
             'rationale':'synthetic case', 'head_sha':self.head} for key in q.POLICY]}

    def check(self): return q.validate(self.manifest, self.root, self.head)

    def test_positive_and_order_independence(self):
        self.assertEqual(self.check(), [])
        self.manifest['checks'].reverse()
        self.assertEqual(self.check(), [])

    def test_failing_unrecorded_missing_or_corrupted_evidence(self):
        for key, value in [('status','FAIL'),('status','NOT_RUN'),('exit_code',1),
                           ('exit_code',False),('command',''),('artifact','missing.txt'),
                           ('artifact','../outside'),('sha256','0'*64),('head_sha','b'*40)]:
            old = copy.deepcopy(self.manifest)
            self.manifest['checks'][0][key] = value
            with self.subTest(key=key,value=value): self.assertTrue(self.check())
            self.manifest = old
        self.manifest['checks'][0].pop('command')
        self.assertTrue(self.check())

    def test_inapplicability_cannot_waive_mandatory_tests(self):
        self.manifest['checks'][0].update(status='NOT_APPLICABLE',exit_code=None)
        self.assertTrue(self.check())
        candidate = next(x for x in self.manifest['checks'] if q.POLICY[x['id']]['allows_not_applicable'])
        self.manifest['checks'][0].update(status='PASS',exit_code=0)
        candidate.update(status='NOT_APPLICABLE',exit_code=None,rationale='No physical model in this scope')
        self.assertEqual(self.check(), [])
        candidate['rationale']=''
        self.assertTrue(self.check())

    def test_versions_ids_and_stale_head(self):
        for mutate in ('missing','duplicate','unknown','version','head'):
            old = copy.deepcopy(self.manifest)
            if mutate == 'missing': self.manifest['checks'].pop()
            elif mutate == 'duplicate': self.manifest['checks'].append(self.manifest['checks'][0])
            elif mutate == 'unknown': self.manifest['checks'][0]['id']='UNKNOWN'
            elif mutate == 'version': self.manifest['schema_version']=True
            else: self.manifest['head_sha']='b'*40
            self.assertTrue(self.check()); self.manifest=old

    def test_public_cli_readonly_and_truncated_input(self):
        path = self.root/'manifest.json'; path.write_text(json.dumps(self.manifest))
        cmd = [sys.executable,str(ROOT/'scripts/validate_quality_gates.py'),str(path),
               '--root',str(self.root),'--head',self.head]
        self.assertEqual(subprocess.run(cmd,capture_output=True).returncode,0)
        path.write_text('{')
        result = subprocess.run(cmd,capture_output=True,text=True)
        self.assertEqual(result.returncode,1); self.assertNotIn('Traceback',result.stderr)
        self.assertEqual(path.read_text(),'{')


if __name__ == '__main__': unittest.main()
