"""Audit-driver boundary tests with synthetic data and trusted Python only."""
from contextlib import redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from scripts.execute_private_validation import verify_copy,run_capture,consumed_build_seconds,verify_probes,ROOT,file_hash


class PrivateExecutionTests(unittest.TestCase):
    def test_copy_scope_hash_and_extra_file_guard(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);receipt={};sources=[];inputs={}
            for i in range(35):
                entry='synthetic-'+str(i);data=str(i).encode();digest=hashlib.sha256(data).hexdigest()
                name=('source/' if i<32 else 'inputs/')+str(i)
                path=root/name;path.parent.mkdir(exist_ok=True);path.write_bytes(data)
                ref={'entry_id':entry,'sha256':digest}
                if i<32:sources.append(ref)
                else:inputs[entry]=ref
                receipt[entry]={'destination':name,'sha256':digest}
            (root/'prepared-copy-receipt.json').write_text(json.dumps(receipt))
            plan={'proposed_source_copy_entries':sources,'inputs':inputs}
            self.assertEqual(verify_copy(root,plan),receipt)
            (root/'source/extra').write_text('unapproved')
            with self.assertRaises(ValueError):verify_copy(root,plan)
            (root/'source/extra').unlink();(root/'source/0').write_text('changed')
            with self.assertRaises(ValueError):verify_copy(root,plan)

    def test_build_retries_account_for_all_attempts_and_unknown_consumption_blocks(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            with self.assertRaises(ValueError):consumed_build_seconds(root)
            for i,value in enumerate([0.5,11.5,2.0]):
                (root/f'build-step-{i}.json').write_text(json.dumps({'wall_seconds':value}))
            self.assertEqual(consumed_build_seconds(root),14.0)
            (root/'build-step-incomplete.stdout').write_text('partial')
            with self.assertRaises(ValueError):consumed_build_seconds(root)

    def test_invalid_or_exhausted_build_budget_is_never_relaxed(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            for value in [-1,300,float('nan'),float('inf'),True]:
                (root/'build-step-1.json').write_text(json.dumps({'wall_seconds':value}))
                with self.subTest(value=value),self.assertRaises(ValueError):consumed_build_seconds(root)

    def test_enforcement_receipt_rejects_stale_wrapper_changed_logs_and_false_success(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);records=[]
            for mode,code in [('security',0),('memory',0),('cpu',137),('file',153),('wall',-9)]:
                for suffix in ['stdout','stderr-with-trace']:(root/f'test-{mode}.{suffix}').write_bytes(b'synthetic')
                records.append({'mode':mode,'exit':code,'passed':True,
                                'stdout_sha256':hashlib.sha256(b'synthetic').hexdigest(),
                                'stderr_sha256':hashlib.sha256(b'synthetic').hexdigest()})
            packet={'schema_version':1,'wrapper_sha256':file_hash(ROOT/'scripts/private_validation_commands.py'),
                    'fixture_sha256':file_hash(ROOT/'tests/fixtures/audit_security_probe.c'),'results':records}
            path=root/'test-results.json';path.write_text(json.dumps(packet))
            self.assertEqual(verify_probes(root,'test'),packet)
            packet['wrapper_sha256']='0'*64;path.write_text(json.dumps(packet))
            with self.assertRaises(ValueError):verify_probes(root,'test')
            packet['wrapper_sha256']=file_hash(ROOT/'scripts/private_validation_commands.py')
            packet['results'][0]['exit']=1;path.write_text(json.dumps(packet))
            with self.assertRaises(ValueError):verify_probes(root,'test')
            packet['results'][0]['exit']=0;path.write_text(json.dumps(packet))
            (root/'test-security.stdout').write_text('changed')
            with self.assertRaises(ValueError):verify_probes(root,'test')

    def test_capture_separates_streams_and_preserves_originals(self):
        with tempfile.TemporaryDirectory() as d,redirect_stdout(io.StringIO()):
            root=Path(d);argv=[sys.executable,'-c','import sys;print("ok");print("err",file=sys.stderr)']
            result=run_capture(root,'case',argv,5)
            self.assertEqual((result.returncode,result.stdout,result.stderr),(0,b'ok\n',b'err\n'))
            self.assertEqual((root/'case.stdout').stat().st_mode & 0o777,0o600)
            # Preexisting stream blocks execution, rather than running and later
            # discovering that evidence would be overwritten.
            marker=root/'unexpected'
            with self.assertRaises(FileExistsError):
                run_capture(root,'case',[sys.executable,'-c',f'open({str(marker)!r},"w").close()'],5)
            self.assertFalse(marker.exists())
            self.assertEqual((root/'case.stdout').read_bytes(),b'ok\n')

    def test_output_limit_is_not_silently_truncated_to_success(self):
        with tempfile.TemporaryDirectory() as d,redirect_stdout(io.StringIO()):
            root=Path(d)
            with self.assertRaises(ValueError):
                run_capture(root,'large',[sys.executable,'-c','import os;os.write(1,b"x"*1048577)'],5)
            self.assertEqual((root/'large.stdout').stat().st_size,1048577)
            self.assertFalse((root/'large.json').exists())


if __name__=='__main__':unittest.main()
