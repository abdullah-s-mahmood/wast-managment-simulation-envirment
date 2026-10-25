"""Synthetic metadata only: no legacy program/build is ever invoked."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('scripts.plan',ROOT/'scripts/validate_execution_review_plan.py')
p = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(p)


def fixture():
    plan=json.loads((ROOT/'docs/audit/S011_EXECUTION_REVIEW_PLAN.json').read_text())
    refs=list(plan['inputs'].values())+list(plan['source_anchors'].values())+plan['proposed_source_copy_entries']
    members={r['entry_id']:{'entry_id':r['entry_id'],'sha256':r['sha256'],'kind':'file','quarantined':False} for r in refs}
    inventory={'schema_version':2,'complete':True,'identity_verified':True,
               'archive_sha256':'a'*64,'compressed_bytes':123,'members':list(members.values()),
               'notice':'SYNTHETIC TEST METADATA; no source bytes, execution or actual archive identity'}
    inventory['manifest_sha256']=p.inventory.canonical_digest(inventory)
    plan.update(archive_sha256=inventory['archive_sha256'],archive_bytes=inventory['compressed_bytes'],inventory_sha256=inventory['manifest_sha256'])
    return plan,inventory


class ReviewPlanTests(unittest.TestCase):
    def test_static_packet_validates_without_mutation(self):
        plan,inv=fixture();before=copy.deepcopy((plan,inv))
        self.assertEqual(p.validate(plan,inv),[])
        self.assertEqual((plan,inv),before)

    def test_never_promotes_preparation_or_runtime_success(self):
        for key,value in [('execution_authorized',True),('working_copy_prepared',True),
                          ('runtime_status','PASSED'),('source_reuse','AUTHORIZED'),
                          ('scientific_validation','VALIDATED'),('network_access','ALLOWED')]:
            plan,inv=fixture();plan[key]=value
            with self.subTest(key=key):self.assertTrue(p.validate(plan,inv))
        plan,inv=fixture();plan['cases'][0]['status']='PASSED'
        self.assertTrue(p.validate(plan,inv))

    def test_changed_cwd_keeps_identical_argv_and_declared_outcomes(self):
        plan,inv=fixture();plan['cases'][1]['argv'][-1]='CITY_REL'
        self.assertTrue(p.validate(plan,inv))
        plan,inv=fixture();plan['cases'][1]['cwd']='A'
        self.assertTrue(p.validate(plan,inv))
        plan,inv=fixture();plan['cases'][3]['expected_exit']=0
        self.assertTrue(p.validate(plan,inv))

    def test_no_arbitrary_command_or_full_simulation_case(self):
        for argv in (['sh','-c','anything'],['BIN_ABS','CFG_ABS','CITY_ABS','OUT'],
                     ['BIN_ABS','--validate-config','CFG_ABS','CITY_ABS','extra']):
            plan,inv=fixture();plan['cases'][0]['argv']=argv
            self.assertTrue(p.validate(plan,inv))

    def test_corrupt_inventory_stale_sources_unknowns_and_quarantine(self):
        plan,inv=fixture();inv['members'][0]['sha256']='0'*64
        self.assertTrue(p.validate(plan,inv))
        plan,inv=fixture();plan['inputs']['config']['sha256']='0'*64
        self.assertTrue(p.validate(plan,inv))
        plan,inv=fixture();inv['members'][0]['quarantined']=True
        inv['manifest_sha256']=p.inventory.canonical_digest({k:v for k,v in inv.items() if k!='manifest_sha256'})
        plan['inventory_sha256']=inv['manifest_sha256']
        self.assertTrue(p.validate(plan,inv))
        for change in ({},None,{'schema_version':True}):
            self.assertTrue(p.validate(change,inv))

    def test_order_property_and_duplicate_case_ids(self):
        plan,inv=fixture()
        for count in range(len(plan['cases'])):
            rotated=copy.deepcopy(plan);rotated['cases']=plan['cases'][count:]+plan['cases'][:count]
            self.assertEqual(p.validate(rotated,inv),[])
        plan['cases'].append(copy.deepcopy(plan['cases'][0]))
        self.assertTrue(p.validate(plan,inv))

    def test_cli_from_other_cwd_is_only_plan_lint(self):
        plan,inv=fixture()
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);a=root/'plan.json';b=root/'inventory.json'
            a.write_text(json.dumps(plan));b.write_text(json.dumps(inv))
            cmd=[sys.executable,str(ROOT/'scripts/validate_execution_review_plan.py'),str(a),'--inventory',str(b)]
            result=subprocess.run(cmd,cwd=root,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            out=json.loads(result.stdout);self.assertFalse(out['execution_authorized'])
            self.assertEqual(out['runtime_status'],'NOT_RUN')
            a.write_text('{');bad=subprocess.run(cmd,cwd=root,capture_output=True,text=True)
            self.assertEqual(bad.returncode,1);self.assertNotIn('Traceback',bad.stderr)
            self.assertEqual(sorted(x.name for x in root.iterdir()),['inventory.json','plan.json'])


if __name__=='__main__':unittest.main()
