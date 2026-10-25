#!/usr/bin/env python3
"""Run independently authored security probes, never legacy code (Linux x86_64).

Private root must contain the reviewed sandbox layout and be owner-only. sudo
needs an already authenticated terminal; no credentials are accepted or stored.
Each probe runs under the validation wrappers and a root watchdog. Reports and
raw stdout/stderr-with-trace are exclusively created mode 0600; preserve failures.
"""
import argparse
import json
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
from scripts.private_validation_commands import sandbox, guarded_target


def private_write(path, data):
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
    with os.fdopen(fd,'wb') as stream:
        stream.write(data)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('private_root',type=Path)
    parser.add_argument('--label',required=True,help='new alphanumeric evidence label')
    args=parser.parse_args()
    if not args.label.isalnum():parser.error('label must be alphanumeric')
    root=args.private_root
    sandbox(root,'/A')  # Fail closed on untrusted parent before compilation/writes.
    binary=root/'probes'/('audit_probe_'+args.label)
    if binary.exists():parser.error('probe binary already exists')
    compile_args=['/usr/bin/cc','-O0','-Wall','-Wextra','-Werror','-o',str(binary),
                  str(ROOT/'tests/fixtures/audit_security_probe.c')]
    compile_result=subprocess.run(compile_args,capture_output=True,timeout=30)
    private_write(root/(args.label+'-compile.log'),compile_result.stdout+compile_result.stderr)
    compile_result.check_returncode()
    records=[]
    for mode in ['security','memory','cpu','file','wall']:
        target=['/probes/'+binary.name,mode]
        command=sandbox(root,'/A')+guarded_target(target,cpu=1 if mode=='cpu' else 5)
        start=time.monotonic()
        result=subprocess.run(command,capture_output=True,stdin=subprocess.DEVNULL,timeout=15)
        for suffix,data in [('stdout',result.stdout),('stderr-with-trace',result.stderr)]:
            private_write(root/(args.label+'-'+mode+'.'+suffix),data)
        expected={'security':(0,),'memory':(0,),'cpu':(-9,137,152),'file':(-25,153),'wall':(-9,137)}
        passed=result.returncode in expected[mode]
        if mode in ('security','memory'):
            passed &= (b'SECURITY_PROBE_PASSED' if mode=='security' else b'MEMORY_DENIED') in result.stdout
        record={'mode':mode,'exit':result.returncode,'wall_seconds':time.monotonic()-start,'passed':bool(passed),'stdout_sha256':hashlib.sha256(result.stdout).hexdigest(),
                'stderr_sha256':hashlib.sha256(result.stderr).hexdigest()}
        records.append(record);print(json.dumps(record),flush=True)
        if not passed:
            private_write(root/(args.label+'-failed.json'),json.dumps(records,indent=2).encode())
            return 1
    receipt={'schema_version':1,'wrapper_sha256':hashlib.sha256((ROOT/'scripts/private_validation_commands.py').read_bytes()).hexdigest(),
             'fixture_sha256':hashlib.sha256((ROOT/'tests/fixtures/audit_security_probe.c').read_bytes()).hexdigest(),'results':records}
    private_write(root/(args.label+'-results.json'),json.dumps(receipt,indent=2).encode())
    return 0


if __name__=='__main__':raise SystemExit(main())
