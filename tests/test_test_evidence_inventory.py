"""Synthetic source/artifact data; never import/execute archived tests."""
import hashlib
import copy
import io
import json
import subprocess
import sys
from pathlib import Path
import tarfile
import tempfile
import unittest
from unittest.mock import patch
from scripts import inventory_legacy as intake
from scripts import inventory_test_evidence as audit


class TestEvidenceTests(unittest.TestCase):
    def test_python_execution_only_behavioral_and_trivial_are_separate(self):
        self.assertEqual(audit.test_syntax('import subprocess\nsubprocess.run(["true"],check=True)','.py')['classification'],'execution_status_only_unexecuted')
        self.assertEqual(audit.test_syntax('assert data["count"]==4','.py')['classification'],'behavioral_assertion_syntax_unexecuted')
        self.assertEqual(audit.test_syntax('assert True','.py')['classification'],'trivial_assertion_only')
        self.assertEqual(audit.test_syntax('subprocess.run(["false"])','.py')['classification'],'unchecked_execution_only_unexecuted')
        self.assertEqual(audit.test_syntax('assert result.returncode==0','.py')['classification'],'execution_status_only_unexecuted')
        mixed=audit.test_syntax('assert result.returncode==0 and payload["count"]==4','.py')
        self.assertEqual(mixed['status_check_lines'],[1]);self.assertEqual(mixed['assertion_lines'],[1])
        self.assertEqual(mixed['classification'],'behavioral_assertion_syntax_unexecuted')

    def test_source_is_data_no_side_effects_and_comments_not_assertions(self):
        with tempfile.TemporaryDirectory() as d:
            marker=Path(d)/'never'
            parsed=audit.test_syntax(f'open({str(marker)!r},"w").write("NO")\nassert x==1','.py')
            self.assertFalse(marker.exists());self.assertEqual(parsed['runtime_status'],'NOT_RUN')
        parsed=audit.test_syntax('// CHECK(false)\nconst char*s="REQUIRE(false)";\nTEST_CASE("x"){CHECK(x==1);}','.cpp')
        self.assertEqual(parsed['assertion_lines'],[3]);self.assertEqual(parsed['test_definition_lines'],[3])

    def test_stale_screenshot_and_self_reported_success_never_validate_science(self):
        for suffix,text in [('.png','OLD SCREENSHOT VALIDATED'),('.json',json.dumps({'status':'passed','reproduced':True,'scientific_validation':'VALIDATED'})),('.md','All tests passed!')]:
            out=audit.result_syntax(text,suffix)
            self.assertEqual(out['result_state'],'unverifiable');self.assertEqual(out['scientific_validation'],'UNVALIDATED')

    def test_full_self_reported_provenance_is_still_unreproduced(self):
        data={k:'a'*64 for k in ['source_sha256','config_sha256','dependency_manifest_sha256']}
        data.update(seed=1,command=['sim','input.json'],status='passed')
        out=audit.result_syntax(json.dumps(data),'.json')
        self.assertEqual(out['result_state'],'unreproduced');self.assertEqual(out['fresh_comparison'],'NOT_RUN')

    def test_build_vendor_results_and_fixture_scopes_are_not_confused(self):
        self.assertEqual(audit.categories('p/build/tests/test.cpp','p'),{'build_artifact'})
        self.assertEqual(audit.categories('p/.deps/tests/test.py','p'),{'vendored_candidate'})
        self.assertIn('historical_result_candidate',audit.categories('p/results/old.png','p'))
        self.assertIn('fixture_path_candidate',audit.categories('p/tests/fixtures/a.json','p'))

    def test_cli_from_other_cwd_is_not_a_legacy_launcher(self):
        with tempfile.TemporaryDirectory() as d:
            result=subprocess.run([sys.executable,str(Path(audit.__file__).resolve()),'--help'],cwd=d,capture_output=True)
            self.assertEqual(result.returncode,0);self.assertEqual(list(Path(d).iterdir()),[])

    def test_cmake_registration_is_not_execution(self):
        result=audit.test_syntax('# add_test(fake)\nadd_test(NAME check COMMAND native)\nmessage("add_test(not_real)")','.cmake')
        self.assertEqual(result['test_registration_lines'],[2]);self.assertEqual(result['runtime_status'],'NOT_RUN')

    def test_retired_scope_is_explicit_not_current_test_provenance(self):
        retired=audit.categories('p/archive/retired_model/source/tests/test.py','p')
        self.assertIn('retired_scope_candidate',retired);self.assertIn('test_path_candidate',retired)
        current=audit.categories('p/tests/test.py','p');self.assertNotIn('retired_scope_candidate',current)

    def test_corrupt_or_reordered_self_reports_never_gain_validation(self):
        for data in ['{"status":"passed","status":"validated"}', '{"status":NaN}', '{broken']:
            result=audit.result_syntax(data,'.json')
            self.assertEqual(result['result_state'],'unverifiable')
            self.assertEqual(result['scientific_validation'],'UNVALIDATED')

    def test_shell_runner_references_are_not_executed_or_claimed_resolved(self):
        out=audit.test_syntax('# pytest example\nctest --output-on-failure','.sh')
        self.assertEqual(out['test_runner_reference_lines'],[2])
        self.assertEqual(out['classification'],'shell_semantics_unresolved')
        self.assertEqual(out['runtime_status'],'NOT_RUN')

    def test_public_cli_inventory_labels_old_result_without_executing_test(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);arc=root/'fixture.tar.gz';marker=root/'must_not_exist'
            with tarfile.open(arc,'w:gz') as tar:
                for name,data in [('p/tests/test.py',f'open({str(marker)!r},"w").write("NO")\nassert x==1'.encode()),('p/results/old.json',b'{"status":"passed","scientific_validation":"VALIDATED"}')]:
                    member=tarfile.TarInfo(name);member.size=len(data);tar.addfile(member,io.BytesIO(data))
            manifest=intake.inspect(arc,intake.DEFAULTS);path=root/'intake.json';path.write_text(json.dumps(manifest))
            result=subprocess.run([sys.executable,str(Path(audit.__file__).resolve()),str(arc),str(path),'--project-root','p'],cwd='/',capture_output=True,timeout=5)
            self.assertEqual(result.returncode,0)
            inventory=json.loads(result.stdout);self.assertTrue(inventory['inventory_complete'])
            historical=next(x for x in inventory['records'] if 'historical_result_candidate' in x['scopes'])
            self.assertEqual(historical['result_state'],'unverifiable')
            self.assertEqual(historical['scientific_validation'],'UNVALIDATED')
            self.assertFalse(marker.exists())

    def test_archive_roundtrip_identity_all_results_labeled_and_links_unread(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'input.tar.gz'
            with tarfile.open(path,'w:gz') as tar:
                for name,data in [('p/tests/test.py',b'assert result==2'),('p/results/old.json',b'{"status":"passed"}')]:
                    item=tarfile.TarInfo(name);item.size=len(data);tar.addfile(item,io.BytesIO(data))
                item=tarfile.TarInfo('p/results/escaping');item.type=tarfile.SYMTYPE;item.linkname='/outside';tar.addfile(item)
            before=path.read_bytes();manifest=intake.inspect(path,intake.DEFAULTS);result=audit.audit(path,manifest,'p')
            self.assertTrue(result['inventory_complete']);self.assertEqual(path.read_bytes(),before)
            results=[x for x in result['records'] if 'historical_result_candidate' in x['scopes']]
            self.assertEqual(len(results),2)
            self.assertTrue(all(x['result_state']=='unverifiable' for x in results))
            self.assertEqual(results[1]['content_status'],'quarantined_not_read')
            changed=dict(manifest,identity_verified=False)
            with self.assertRaises(ValueError):audit.audit(path,changed,'p')
            for key,value in [('schema_version',3),('members',None),('compressed_bytes',True)]:
                bad=copy.deepcopy(manifest);bad[key]=value
                bad.pop('manifest_sha256');bad['manifest_sha256']=intake.canonical_digest(bad)
                with self.subTest(key=key),self.assertRaises(ValueError):audit.audit(path,bad,'p')
            for key in ['max_members','max_member_bytes','max_compressed_bytes']:
                policy=dict(intake.DEFAULTS);policy[key]=1
                with patch.object(intake,'DEFAULTS',policy),self.subTest(limit=key),self.assertRaises(ValueError):
                    audit.audit(path,manifest,'p')


if __name__=='__main__':unittest.main()
