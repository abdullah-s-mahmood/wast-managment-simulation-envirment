#!/usr/bin/env python3
"""Probe Linux Bubblewrap namespaces with trusted true; never run legacy code.

Exit 0 means ONLY that this namespace probe passed; 1 means it was blocked;
2 means invocation/report failure. No result authorizes or clears execution.
Raw diagnostics belong in an optional private, exclusively created JSON report.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess

# Fixed trusted OS executables, no user-selected command or inherited environment.
# Mirrors E-S011-04; every mount is read-only except disposable process/dev/tmp.
COMMAND = ['/usr/bin/bwrap', '--unshare-user', '--unshare-net', '--unshare-pid',
           '--unshare-ipc', '--unshare-uts', '--die-with-parent', '--new-session',
           '--ro-bind', '/usr', '/usr', '--ro-bind', '/bin', '/bin',
           '--ro-bind', '/lib', '/lib', '--ro-bind', '/lib64', '/lib64',
           '--proc', '/proc', '--dev', '/dev', '--tmpfs', '/tmp',
           '--chdir', '/tmp', '--', '/usr/bin/true']
MAX_DIAGNOSTIC_BYTES = 4096


def probe(run=subprocess.run):
    """Return probe evidence, never readiness; run is injected for synthetic tests.

Wall timeout is five seconds, stdin is closed and the environment has only PATH
and C locale. Output is from trusted installed Bubblewrap/true only; retained
stdout/stderr are limited to 4096 bytes each. This is not a hostile-target runner
or a proof of all mount, network, subprocess or resource-limit properties.
"""
    report = {'schema_version':1, 'purpose':'TRUSTED_NAMESPACE_PREFLIGHT',
              'argv':list(COMMAND), 'timeout_seconds':5, 'returncode':None,
              'failure_kind':None, 'namespace_probe_status':'BLOCKED',
              'ready_for_legacy_execution':False, 'legacy_cases_status':'NOT_RUN',
              'source_reuse':'PROHIBITED', 'scientific_validation':'UNVALIDATED',
              'unverified_requirements':['network_denial_behavior',
                  'read_only_target_inputs_cwd', 'child_execution_denial',
                  'resource_limit_enforcement', 'dependency_provenance_licenses',
                  'source_input_binary_identity'],
              'stdout':'', 'stderr':'', 'diagnostics_truncated':False}
    stdout, stderr = b'', b''
    try:
        result = run(list(COMMAND), stdin=subprocess.DEVNULL, capture_output=True,
                     timeout=5, env={'PATH':'/usr/bin:/bin','LC_ALL':'C'}, check=False)
        report['returncode'] = result.returncode
        stdout, stderr = result.stdout, result.stderr
        if result.returncode == 0:
            report['namespace_probe_status'] = 'PASSED'
        else:
            report['failure_kind'] = 'NONZERO_EXIT'
    except subprocess.TimeoutExpired as error:
        report['failure_kind'] = 'TIMEOUT'
        stdout, stderr = error.stdout or b'', error.stderr or b''
    except OSError:
        # Exception messages can contain private paths; expose only the category.
        report['failure_kind'] = 'OS_ERROR'
    report['diagnostics_truncated'] = any(len(x)>MAX_DIAGNOSTIC_BYTES for x in (stdout, stderr))
    report['stdout'] = stdout[:MAX_DIAGNOSTIC_BYTES].decode('utf-8', errors='replace')
    report['stderr'] = stderr[:MAX_DIAGNOSTIC_BYTES].decode('utf-8', errors='replace')
    return report


def write_private_report(path, report):
    """Exclusively create a mode-0600 report; refuse existing files and symlinks.

The caller must supply a trusted private parent directory. No parent directory
is created or made private by this helper. A failed write may leave partial
private evidence; never overwrite it or silently call it a completed report.
"""
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'w', encoding='utf-8') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path, help='new private JSON report; existing paths refused')
    args = parser.parse_args(argv)
    report = probe()
    if args.report:
        try:
            write_private_report(args.report, report)
        except (OSError, ValueError):
            parser.exit(2, 'FAIL: private report could not be created; no legacy execution.\n')
    # Do not publish raw diagnostics or private report paths to ordinary stdout.
    print(json.dumps({k:report[k] for k in ['namespace_probe_status',
                      'ready_for_legacy_execution','legacy_cases_status','failure_kind']}))
    return 0 if report['namespace_probe_status']=='PASSED' else 1


if __name__ == '__main__':
    raise SystemExit(main())
