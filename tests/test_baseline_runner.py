"""Boundary tests use synthetic packets and trusted Python, never legacy code."""
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from scripts import baseline_transport as transport
from scripts import run_private_baseline as runner
from scripts.baseline_commands import baseline_sandbox


class BaselineRunnerTests(unittest.TestCase):
    def test_capture_retains_nonzero_target_as_failed_evidence_not_launch_failure(self):
        with tempfile.TemporaryDirectory() as d,redirect_stdout(io.StringIO()):
            root=Path(d);source=root/'source';source.mkdir();(source/'data').write_text('synthetic')
            packet=transport.pack(source,{'target_exit':3,'termination':'exited'})
            command=[sys.executable,'-c','import sys;sys.stdout.write('+repr(json.dumps(packet))+')']
            with patch.object(runner,'baseline_sandbox',return_value=command):result=runner.capture(root,'test','fixture')
            self.assertTrue(result['export_complete']);self.assertEqual(result['process']['target_exit'],3)
            self.assertEqual((root/'test.export/data').read_text(),'synthetic')

    def test_failed_launcher_or_truncated_packet_never_publishes(self):
        for name,command in [('failed',[sys.executable,'-c','raise SystemExit(1)']),
                             ('corrupt',[sys.executable,'-c','print("{broken")'])]:
            with self.subTest(name=name),tempfile.TemporaryDirectory() as d:
                root=Path(d)
                with patch.object(runner,'baseline_sandbox',return_value=command),self.assertRaises(ValueError):
                    runner.capture(root,name,'fixture')
                self.assertFalse((root/(name+'.export')).exists())
                self.assertTrue((root/(name+'.packet.json')).exists())

    def test_scope_and_exclusive_attempt_marker_stop_extra_invocations(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'baseline-probes-passed.json').write_text(json.dumps({'tools':{},'results':[{'passed':True}]*7}))
            with patch.object(runner,'preflight'),patch.object(runner,'tools_digest',return_value={}),patch.object(runner,'capture') as capture:
                for run,attempt in [('OTHER',1),('BASELINE_A',3)]:
                    with self.assertRaises(ValueError):runner.run(root,run,attempt)
                (root/'BASELINE_A-1.started.json').write_text('preserve')
                with self.assertRaises(FileExistsError):runner.run(root,'BASELINE_A',1)
                with self.assertRaises(FileNotFoundError):runner.run(root,'BASELINE_B',2)
                self.assertEqual(capture.call_count,0)

    def test_namespace_has_readonly_host_mounts_and_exact_baseline_caps(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            for name in ('deps','source','inputs','A','B','probes','build'):(root/name).mkdir()
            for name in ('baseline_supervisor.py','baseline_transport.py'):(root/'probes'/name).touch()
            args=baseline_sandbox(root,'baseline')
            self.assertNotIn('--bind',args);self.assertIn('67108864',args)
            self.assertEqual(args[args.index('/usr/bin/bwrap')-1],'120')
            self.assertIn('--as=1073741824',args);self.assertIn('--cpu=60',args)
            with self.assertRaises(ValueError):baseline_sandbox(root,'sh')


if __name__=='__main__':unittest.main()
