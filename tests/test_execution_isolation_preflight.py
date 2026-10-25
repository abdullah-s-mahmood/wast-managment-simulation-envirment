"""Trusted-tool preflight tests; never prepare or execute legacy code."""
import importlib.util
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('isolation', ROOT/'scripts/check_execution_isolation.py')
p = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(p)


class IsolationPreflightTests(unittest.TestCase):
    def test_namespace_success_is_never_execution_clearance(self):
        run = Mock(return_value=subprocess.CompletedProcess([], 0, b'', b''))
        report = p.probe(run)
        self.assertEqual(report['namespace_probe_status'], 'PASSED')
        self.assertFalse(report['ready_for_legacy_execution'])
        self.assertEqual(report['legacy_cases_status'], 'NOT_RUN')
        self.assertIn('child_execution_denial', report['unverified_requirements'])
        self.assertEqual(run.call_count, 1)
        args, kw = run.call_args
        self.assertEqual(args[0][-1], '/usr/bin/true')
        self.assertIn('--unshare-net', args[0])
        self.assertEqual(kw['timeout'], 5)
        self.assertEqual(kw['env'], {'PATH':'/usr/bin:/bin','LC_ALL':'C'})
        self.assertFalse(kw.get('shell', False))

    def test_nonzero_and_signals_fail_closed_generated(self):
        values = [-9, -15, 1, 2, 125, 127, 255]
        values += random.Random(11).sample(range(1, 256), 40)
        for code in values:
            with self.subTest(code=code):
                run = Mock(return_value=subprocess.CompletedProcess([], code, b'', b'denied'))
                report = p.probe(run)
                self.assertEqual(report['namespace_probe_status'], 'BLOCKED')
                self.assertFalse(report['ready_for_legacy_execution'])
                self.assertEqual(report['returncode'], code)
                self.assertEqual(run.call_count, 1)  # No fallback or retry.

    def test_missing_tool_and_permission_failure(self):
        for error in [FileNotFoundError(), PermissionError()]:
            run = Mock(side_effect=error)
            report = p.probe(run)
            self.assertEqual(report['namespace_probe_status'], 'BLOCKED')
            self.assertEqual(report['failure_kind'], 'OS_ERROR')
            self.assertEqual(run.call_count, 1)

    def test_timeout_is_not_an_exit_result(self):
        report = p.probe(Mock(side_effect=subprocess.TimeoutExpired(p.COMMAND, 5,
                         output=b'partial', stderr=b'blocked')))
        self.assertEqual(report['failure_kind'], 'TIMEOUT')
        self.assertIsNone(report['returncode'])
        self.assertEqual(report['namespace_probe_status'], 'BLOCKED')
        self.assertEqual(report['stdout'], 'partial')

    def test_diagnostics_are_bounded_and_decode_safely(self):
        report = p.probe(Mock(return_value=subprocess.CompletedProcess([], 1,
                           b'x'*10000, b'\xff'*10000)))
        self.assertTrue(report['diagnostics_truncated'])
        self.assertLessEqual(len(report['stdout']), p.MAX_DIAGNOSTIC_BYTES)
        self.assertLessEqual(len(report['stderr']), p.MAX_DIAGNOSTIC_BYTES)
        self.assertEqual(report['namespace_probe_status'], 'BLOCKED')

    def test_private_report_permissions_roundtrip_and_no_overwrite(self):
        report = p.probe(Mock(return_value=subprocess.CompletedProcess([], 1,b'',b'denied')))
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/'report.json'
            p.write_private_report(path, report)
            self.assertEqual(json.loads(path.read_text()), report)
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            before = path.read_bytes()
            with self.assertRaises(FileExistsError):
                p.write_private_report(path, {})
            self.assertEqual(path.read_bytes(), before)

    def test_report_symlink_is_never_followed(self):
        with tempfile.TemporaryDirectory() as d:
            target = Path(d)/'target'; target.write_text('preserve')
            link = Path(d)/'link'; link.symlink_to(target)
            with self.assertRaises(FileExistsError):
                p.write_private_report(link, {})
            self.assertEqual(target.read_text(), 'preserve')

    def test_cli_help_from_other_cwd_does_not_probe(self):
        with tempfile.TemporaryDirectory() as d:
            result = subprocess.run([sys.executable,str(ROOT/'scripts/check_execution_isolation.py'),
                                     '--help'], cwd=d, capture_output=True, timeout=5)
            self.assertEqual(result.returncode, 0)
            self.assertIn(b'namespace', result.stdout)
            self.assertEqual(list(Path(d).iterdir()), [])

    def test_cli_does_not_accept_target_or_custom_command(self):
        with tempfile.TemporaryDirectory() as d:
            result = subprocess.run([sys.executable,str(ROOT/'scripts/check_execution_isolation.py'),
                                     '--target','sw_cosim'], cwd=d, capture_output=True, timeout=5)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(list(Path(d).iterdir()), [])

    def test_cli_reports_probe_only_without_private_diagnostic_leak(self):
        from contextlib import redirect_stdout, redirect_stderr
        import io
        report = p.probe(Mock(return_value=subprocess.CompletedProcess([],1,b'',b'PRIVATE_MARKER')))
        out, err = io.StringIO(), io.StringIO()
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/'private.json'
            with unittest.mock.patch.object(p, 'probe', return_value=report), redirect_stdout(out), redirect_stderr(err):
                code = p.main(['--report', str(path)])
            self.assertEqual(code, 1)
            self.assertNotIn('PRIVATE_MARKER', out.getvalue()+err.getvalue())
            self.assertIn('PRIVATE_MARKER', path.read_text())
            self.assertFalse(json.loads(out.getvalue())['ready_for_legacy_execution'])


if __name__ == '__main__':
    unittest.main()
