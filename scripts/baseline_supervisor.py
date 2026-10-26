#!/usr/bin/env python3
"""Trusted in-namespace S012 supervisor; no host write mounts or credentials.

A 100-second child deadline leaves export time within the outer 120-second
watchdog. A complete output packet may contain a FAILED target; never equate it
with baseline success. Test modes run only an independently authored fixture.
"""
import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
sys.path.insert(0,str(Path(__file__).resolve().parent))
import baseline_transport as transport


def command(mode):
    """Return exactly one approved target or one fixed trusted-fixture invocation."""
    if mode=='baseline':
        argv=['/build/sw_cosim','/inputs/config.json','/A/city_fixture','/outputs/baseline']
    elif mode in ('fixture','security','memory','cpu','file','wall','quota'):
        argv=['/probes/baseline_fixture',mode]
    else:raise ValueError('unsupported mode')
    return ['/usr/bin/prlimit','--as=1073741824','--cpu='+('1' if mode=='cpu' else '60'),
            '--fsize=16777216','--core=0','--nofile=128','--','/usr/bin/strace',
            '--kill-on-exit','--inject=execve:error=EPERM',
            '--inject=execveat,fork,vfork,clone,clone3,unshare,setns,ptrace,io_uring_setup:error=EPERM',
            '--inject=%network:error=EPERM','-e','trace=%process,%network,%file','--',*argv]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode',choices=['baseline','fixture','security','memory','cpu','file','wall','quota'],required=True)
    args=parser.parse_args()
    if os.getuid()==0:raise ValueError('target supervisor must be nonroot')
    out=Path('/outputs');fds=[];start=time.monotonic();timed_out=False
    try:
        for name in ('process.stdout','process.stderr-with-trace'):
            fds.append(os.open(out/name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600))
        child=subprocess.Popen(command(args.mode),stdin=subprocess.DEVNULL,stdout=fds[0],stderr=fds[1],start_new_session=True)
        try:code=child.wait(timeout=1 if args.mode=='wall' else 100)
        except subprocess.TimeoutExpired:
            timed_out=True;os.killpg(child.pid,signal.SIGKILL);code=child.wait()
    finally:
        for fd in fds:os.close(fd)
    process={'mode':args.mode,'target_exit':code,'termination':'timeout' if timed_out else 'signal' if code<0 else 'exited',
             'wall_seconds':time.monotonic()-start,'target_cpu_seconds':1 if args.mode=='cpu' else 60,
             'target_address_space_bytes':1073741824,'target_inner_wall_seconds':1 if args.mode=='wall' else 100}
    try:packet=transport.pack(out,process)
    except (OSError,ValueError):packet={'schema_version':1,'complete':False,'process':process,'error':'UNSAFE_OR_INCOMPLETE_EXPORT'}
    sys.stdout.write(json.dumps(packet,separators=(',',':'))+'\n');sys.stdout.flush()
    return 0 if packet['complete'] else 1


if __name__=='__main__':raise SystemExit(main())
