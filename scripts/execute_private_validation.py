#!/usr/bin/env python3
"""Execute only ADR-0007's fresh build/five private validation cases.

Requires authenticated sudo terminal, reviewed exact source-copy receipt and
successful trusted security probes. Never accepts credentials or archived binaries.
Run as owner, not root; only namespace/watchdog setup is privileged. No full
simulation or source modification. Private root and reports stay outside repo.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from scripts.private_validation_commands import sandbox, guarded_target
from scripts.probe_private_sandbox import private_write

PLAN_SHA='6a3ee7bc8ae61c8d1060fd9a197e012d9e680f1387e2dd787988b267f2960a41'


def file_hash(path):
    """SHA-256 of complete bytes via a bounded-memory streaming read."""
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()


def verify_copy(root, plan):
    """Verify exactly 35 approved entry hashes, paths and no filesystem links."""
    receipt=json.loads((root/'prepared-copy-receipt.json').read_text())
    expected={r['entry_id']:r['sha256'] for r in plan['proposed_source_copy_entries']}
    expected.update({r['entry_id']:r['sha256'] for r in plan['inputs'].values()})
    if len(expected)!=35 or set(receipt)!=set(expected):raise ValueError('copy receipt scope')
    paths=set()
    for entry,record in receipt.items():
        path=Path(record['destination'])
        if (path.is_absolute() or '..' in path.parts or path.parts[0] not in ('source','inputs','A')
                or path.as_posix() in paths):raise ValueError('unsafe copy receipt path')
        full=root/path
        if any(p.is_symlink() for p in [full,*full.parents] if p!=root):
            raise ValueError('copy link')
        if file_hash(full)!=expected[entry] or record['sha256']!=expected[entry]:
            raise ValueError('copied bytes mismatch')
        paths.add(path.as_posix())
    observed={str(p.relative_to(root)) for name in ('source','inputs','A') for p in (root/name).rglob('*') if p.is_file()}
    if observed!=paths:raise ValueError('extra copied files')
    return receipt


def run_capture(root,label,command,timeout):
    """Capture exclusive private streams before launch; preserve every failure.

    Target wrappers enforce file-size limits. Reads into parent memory are limited
    to 1 MiB per stream and over-budget captures cannot become successful records.
    """
    start=time.monotonic()
    # Regular-file capture lets the target's RLIMIT_FSIZE bound each stream;
    # pipe capture would leave the parent vulnerable to unbounded output memory.
    fds=[]
    try:
        for suffix in ('stdout','stderr-with-trace'):
            fds.append(os.open(root/(label+'.'+suffix),
                       os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600))
        result=subprocess.run(command,stdin=subprocess.DEVNULL,stdout=fds[0],stderr=fds[1],timeout=timeout)
    finally:
        for fd in fds:os.close(fd)
    streams=[]
    for suffix in ('stdout','stderr-with-trace'):
        with (root/(label+'.'+suffix)).open('rb') as stream:data=stream.read(1048577)
        if len(data)>1048576:raise ValueError('captured output budget exceeded')
        streams.append(data)
    result.stdout,result.stderr=streams
    record={'label':label,'exit':result.returncode,'wall_seconds':time.monotonic()-start,
            'stdout_sha256':hashlib.sha256(result.stdout).hexdigest(),
            'stderr_with_trace_sha256':hashlib.sha256(result.stderr).hexdigest()}
    private_write(root/(label+'.json'),json.dumps(record,indent=2).encode())
    print(json.dumps(record),flush=True)
    return result


def consumed_build_seconds(root):
    """Account for every terminal build attempt; missing evidence blocks retries.

Only recorded command-running wall time consumes this execution budget, not idle
inspection time. Every compiler process inherits one CPU affinity, so command wall
bounds aggregate build CPU as well. An incomplete capture has unknown consumption
and cannot be retried under an assumed remaining budget.
"""
    records=list(root.glob('build-step-*.json'))
    for stream in [*root.glob('build-step-*.stdout'),*root.glob('build-step-*.stderr-with-trace')]:
        label=stream.name.split('.',1)[0]
        if not (root/(label+'.json')).is_file():raise ValueError('unknown prior build consumption')
    total=0.0
    for path in records:
        value=json.loads(path.read_text())['wall_seconds']
        if type(value) not in (int,float) or not math.isfinite(value) or value<0:
            raise ValueError('invalid build duration')
        total+=value
    if not records or total>=300:raise ValueError('no verified remaining build budget')
    return total


def verify_probes(root,label):
    """Bind successful enforcement evidence to current wrapper/fixture and raw logs."""
    if not label.isalnum():raise ValueError('invalid probe label')
    packet=json.loads((root/(label+'-results.json')).read_text())
    if (packet.get('schema_version')!=1
            or packet.get('wrapper_sha256')!=file_hash(ROOT/'scripts/private_validation_commands.py')
            or packet.get('fixture_sha256')!=file_hash(ROOT/'tests/fixtures/audit_security_probe.c')):
        raise ValueError('stale enforcement evidence')
    records=packet['results']
    if [x['mode'] for x in records]!=['security','memory','cpu','file','wall']:
        raise ValueError('incomplete enforcement evidence')
    exits={'security':(0,),'memory':(0,),'cpu':(-9,137,152),'file':(-25,153),'wall':(-9,137)}
    for record in records:
        if record['passed'] is not True or record['exit'] not in exits[record['mode']]:
            raise ValueError('failed enforcement evidence')
        for suffix,key in [('stdout','stdout_sha256'),('stderr-with-trace','stderr_sha256')]:
            if file_hash(root/(label+'-'+record['mode']+'.'+suffix))!=record[key]:
                raise ValueError('enforcement log changed')
    return packet


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase',choices=['build','resume-build','cases'])
    parser.add_argument('private_root',type=Path)
    parser.add_argument('--probe-label',default='verified5')
    parser.add_argument('--attempt',choices=['initial','serialdeps'],default='initial',
                        help='one retained retry after the observed OpenBLAS initialization failure')
    args=parser.parse_args();root=args.private_root
    sandbox(root,'/A')
    plan_path=ROOT/'docs/audit/S011_EXECUTION_REVIEW_PLAN.json'
    if file_hash(plan_path)!=PLAN_SHA:raise ValueError('reviewed plan changed')
    plan=json.loads(plan_path.read_text());verify_copy(root,plan)
    verify_probes(root,args.probe_label)
    if args.phase in ('build','resume-build'):
        resume=args.phase=='resume-build'
        if resume:
            if (root/'build-receipt.json').exists() or (root/'cases-started.json').exists():
                raise ValueError('build already complete or cases started')
            if not (root/'build-started.json').exists():raise ValueError('no interrupted build')
        else:
            private_write(root/'build-started.json',b'{"authority":"ADR-0007"}\n')
        start=time.monotonic();cpu=min(os.sched_getaffinity(0))
        commands=[['/usr/bin/cmake','-S','/source','-B','/build','-DSW_BUILD_COSIM=ON'],
                  ['/usr/bin/cmake','--build','/build','--target','sw_cosim','--parallel','2']]
        consumed=consumed_build_seconds(root) if resume else 0
        if resume:commands=commands[1:]
        for i,command in enumerate(commands):
            remaining=int(300-consumed-(time.monotonic()-start))
            if remaining<1:raise ValueError('cumulative build wall budget exhausted')
            wrapped=sandbox(root,'/build',build=True,wall_seconds=remaining)+[
                '/usr/bin/taskset','-c',str(cpu),'/usr/bin/prlimit','--as=1073741824',
                '--cpu=300','--core=0','--',*command]
            label='build-step-2-retry'+str(len(list(root.glob('build-step-2-retry*.json')))+1) if resume else 'build-step-'+str(i+1)
            result=run_capture(root,label,wrapped,remaining+5)
            if result.returncode:return 1
        verify_copy(root,plan)
        binary=root/'build/sw_cosim'
        private_write(root/'build-receipt.json',json.dumps({'binary_sha256':file_hash(binary),
                      'wall_seconds':consumed+time.monotonic()-start,'cpu_affinity':[cpu],
                      'address_space_bytes':1073741824,'authority':'ADR-0007'},indent=2).encode())
        return 0
    build=json.loads((root/'build-receipt.json').read_text())
    binary=root/'build/sw_cosim'
    if file_hash(binary)!=build['binary_sha256']:raise ValueError('binary changed')
    retry=args.attempt=='serialdeps'
    if retry:
        prior=json.loads((root/'cases-failed.json').read_text())
        if prior!=[{'id':'ABS_A','passed':False,'actual_exit':130}]:
            raise ValueError('retry does not match reviewed initialization failure')
    prefix='serialdeps-' if retry else ''
    private_write(root/(prefix+'cases-started.json'),b'{"max_cases":5,"authority":"ADR-0007"}\n')
    config=json.loads((root/'inputs/config.json').read_text())
    city=json.loads((root/'A/city_fixture/city.json').read_text())
    source=(root/'source/src/cosim/main.cpp').read_text()
    binding=re.search(r'\{"map_id",\s*city.value\("([^"]+)",\s*"([^"]*)"\)\}',source)
    if binding is None:raise ValueError('source map default binding changed')
    expected={'status':'VALID_RUNTIME_CONFIG','policy':config['policy'],'seed':config['seed'],
              'map_id':city.get(binding[1],binding[2]),'bin_count':len(city['bins']),
              'profile_id':config['plc_profile_id']}
    tokens={'BIN_ABS':'/build/sw_cosim','CFG_ABS':'/inputs/config.json',
            'CITY_ABS':'/A/city_fixture','CITY_REL':'city_fixture'}
    successes=[];records=[]
    for case in plan['cases']:
        argv=[tokens.get(x,x) for x in case['argv']]
        result=run_capture(root,prefix+'case-'+case['id'],sandbox(root,'/'+case['cwd'])+guarded_target(argv),15)
        passed=result.returncode==case['expected_exit']
        if case['expected_exit']==0:
            try:passed &= json.loads(result.stdout)==expected
            except (ValueError,UnicodeError):passed=False
            successes.append(result.stdout)
        else:passed &= bool(result.stderr)
        verify_copy(root,plan)
        passed &= file_hash(binary)==build['binary_sha256']
        records.append({'id':case['id'],'passed':bool(passed),'actual_exit':result.returncode})
        if not passed:
            private_write(root/(prefix+'cases-failed.json'),json.dumps(records,indent=2).encode())
            return 1
    if len(successes)!=3 or len(set(successes))!=1:raise ValueError('validation stdout differs')
    private_write(root/(prefix+'cases-results.json'),json.dumps(records,indent=2).encode())
    return 0


if __name__=='__main__':raise SystemExit(main())
