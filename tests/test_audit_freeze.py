"""Freeze references protect unknowns and historical blobs, not scientific truth."""
import copy
import json
import random
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from scripts import inventory_legacy as intake
from scripts import validate_audit_freeze as freeze


class FreezeTests(unittest.TestCase):
    def fixture(self):return json.loads((freeze.ROOT/'docs/audit/S016_AUDIT_FREEZE.json').read_text())
    def seal(self,data):
        data.pop('manifest_sha256',None);data['manifest_sha256']=intake.canonical_digest(data);return data
    def test_real_freeze_has_evidence_and_retains_unknowns(self):
        result=freeze.validate(self.fixture(),freeze.ROOT)
        self.assertEqual(result['verified_artifacts'],24);self.assertEqual(result['scientific_validation'],'UNVALIDATED')
    def test_unresolved_equation_cannot_be_promoted_to_unblock(self):
        data=self.fixture();row=next(x for x in data['conclusions'] if x['topic']=='scientific_models');row['status']='OBSERVED'
        with self.assertRaises(ValueError):freeze.validate(self.seal(data),freeze.ROOT)
        data=self.fixture();data['accepted_models']=['guessed_equation']
        with self.assertRaises(ValueError):freeze.validate(self.seal(data),freeze.ROOT)
    def test_observed_version_is_not_an_accepted_platform_version(self):
        data=self.fixture();data['observed_versions'][0]['decision']='ACCEPTED'
        with self.assertRaises(ValueError):freeze.validate(self.seal(data),freeze.ROOT)
    def test_missing_evidence_duplicate_or_mutated_hash_rejected(self):
        for mutate in [lambda d:d['conclusions'][0].update(evidence=[]),lambda d:d['artifacts'].append(copy.deepcopy(d['artifacts'][0])),lambda d:d['artifacts'][0].update(sha256='0'*64),lambda d:d['conclusions'].pop(),lambda d:d['conclusions'][0].update(topic='hidden')]:
            data=self.fixture();mutate(data)
            with self.assertRaises(ValueError):freeze.validate(self.seal(data),freeze.ROOT)
    def test_archive_identity_or_clearance_promotion_rejected(self):
        for key,value in [('archive_sha256','0'*64),('security_clearance','SAFE'),('license_status','CLEARED')]:
            data=self.fixture();data['source_manifest'][key]=value;data['source_manifest_sha256']=intake.canonical_digest(data['source_manifest'])
            with self.assertRaises(ValueError):freeze.validate(self.seal(data),freeze.ROOT)
    def test_traversal_and_unknown_schema_fail_before_blob_read(self):
        for path in ('../secret','/secret','docs/../../secret','docs/x.md;echo BAD'):
            with self.assertRaises(ValueError):freeze.git_blob(freeze.ROOT,'0'*40,path)
        data=self.fixture();data['schema_version']=True
        with self.assertRaises(ValueError):freeze.validate(self.seal(data),freeze.ROOT)
    def test_standalone_source_manifest_must_agree_with_freeze(self):
        data=self.fixture()
        with patch.object(Path,'read_bytes',return_value=b'{"tampered":true}'),self.assertRaises(ValueError):
            freeze.validate(data,freeze.ROOT)

    def test_generated_order_changes_keep_evidence_links_and_unknowns(self):
        rng=random.Random(16)
        for _ in range(5):
            data=self.fixture();rng.shuffle(data['artifacts']);rng.shuffle(data['conclusions'])
            result=freeze.validate(self.seal(data),freeze.ROOT)
            self.assertEqual(result['verified_artifacts'],24);self.assertEqual(result['verified_conclusions'],9)
            self.assertEqual(result['scientific_validation'],'UNVALIDATED')

    def test_cli_from_other_cwd_needs_no_chat_or_private_archive(self):
        result=subprocess.run([sys.executable,str(Path(freeze.__file__).resolve()),str(freeze.ROOT/'docs/audit/S016_AUDIT_FREEZE.json')],cwd='/',capture_output=True,timeout=30)
        self.assertEqual(result.returncode,0,result.stderr);self.assertEqual(json.loads(result.stdout)['status'],'VALID_SOURCE_AUDIT_FREEZE')
    def test_frozen_git_blob_survives_working_file_change(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);subprocess.run(['git','init','-q'],cwd=root,check=True)
            (root/'docs').mkdir();path=root/'docs/item.md';path.write_text('original audit evidence\n')
            subprocess.run(['git','add','docs/item.md'],cwd=root,check=True)
            subprocess.run(['git','-c','user.name=Test','-c','user.email=test@example.invalid','commit','-qm','fixture'],cwd=root,check=True)
            commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip();path.write_text('later mutable state\n')
            self.assertEqual(freeze.git_blob(root,commit,'docs/item.md'),b'original audit evidence\n')
            self.assertEqual(path.read_text(),'later mutable state\n')


if __name__=='__main__':unittest.main()
