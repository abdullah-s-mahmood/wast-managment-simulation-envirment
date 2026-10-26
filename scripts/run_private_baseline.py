#!/usr/bin/env python3
"""Private S012 probes/baseline runner for owner-approved ADR-0009 only.

No credentials accepted/stored. Requires an authenticated terminal for privileged
namespace setup; supervisor/targets are nonroot. All outputs are private and every
attempt is exclusive. A complete data export is distinct from a successful run.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from scripts.baseline_commands import baseline_sandbox
from scripts import baseline_transport as transport
from scripts.execute_private_validation import verify_copy,file_hash
from scripts.probe_private_sandbox import private_write
from scripts.validate_baseline_result import strict_json,validate,BINARY_SHA

PLAN_SHA='5a8ef0be672f616bd9c40e68db4ea431e82dbb54c7dcea3ac31dd18bfb893187'
TOOLS=('baseline_commands.py','baseline_supervisor.py','baseline_transport.py','run_private_baseline.py')


def tools_digest():
    """Bind runtime evidence to every independently authored execution component."""
    result={name:file_hash(ROOT/'scripts'/name) for name in TOOLS}
    result['private_validation_commands.py']=file_hash(ROOT/'scripts/private_validation_commands.py')
    result['fixture']=file_hash(ROOT/'tests/fixtures/baseline_fixture.c')
    return result


def check_staging(root):
    """Require namespace-staged code byte-identical to reviewed current source."""
    for name in ('baseline_supervisor.py','baseline_transport.py'):
        if file_hash(root/'probes'/name)!=file_hash(ROOT/'scripts'/name):raise ValueError('staged supervisor changed')


def capture(root,label,mode):
    """Retain raw packet/launcher stderr, then verify before private publication."""
    fds=[];started=time.monotonic()
    try:
        for suffix in ('packet.json','launcher.stderr'):
            fds.append(os.open(root/(label+'.'+suffix),os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600))
        result=subprocess.run(baseline_sandbox(root,mode),stdin=subprocess.DEVNULL,stdout=fds[0],stderr=fds[1],timeout=125)
    finally:
        for fd in fds:os.close(fd)
    record={'label':label,'launcher_exit':result.returncode,'wall_seconds':time.monotonic()-started,
            'packet_sha256':file_hash(root/(label+'.packet.json')),'export_complete':False,'process':None}
    private_write(root/(label+'.capture.json'),json.dumps(record,indent=2).encode())
    if result.returncode!=0:raise ValueError('namespace/supervisor failed; raw evidence retained')
    with (root/(label+'.packet.json')).open('rb') as stream:data=stream.read(transport.MAX_TRANSPORT_BYTES+1)
    if len(data)>transport.MAX_TRANSPORT_BYTES:raise ValueError('packet budget exceeded')
    packet=strict_json(data)
    process=transport.decode(packet,root/(label+'.export'))
    record.update(export_complete=True,process=process)
    private_write(root/(label+'.export.json'),json.dumps(record,indent=2).encode())
    print(json.dumps({'label':label,'export_complete':True,'target_exit':process.get('target_exit'),
                      'termination':process.get('termination'),'wall_seconds':record['wall_seconds']}),flush=True)
    return record


def preflight(root):
    """Verify immutable plan, inputs/build and all separately supplied packages."""
    if file_hash(ROOT/'docs/audit/S012_BASELINE_EXECUTION_REVIEW.json')!=PLAN_SHA:raise ValueError('baseline plan changed')
    plan=strict_json((ROOT/'docs/audit/S012_BASELINE_EXECUTION_REVIEW.json').read_bytes())
    if '- Status: Accepted' not in (ROOT/'docs/adr/ADR-0009-private-baseline-reproduction.md').read_text():
        raise ValueError('owner authority not recorded')
    verify_copy(root,strict_json((ROOT/'docs/audit/S011_EXECUTION_REVIEW_PLAN.json').read_bytes()))
    if file_hash(root/'build/sw_cosim')!=BINARY_SHA:raise ValueError('audit binary changed')
    for name,digest in strict_json((root/'dependency-package-digests.json').read_bytes()).items():
        if Path(name).name!=name or file_hash(root/'packages'/name)!=digest:raise ValueError('trusted package mismatch')
    check_staging(root)
    return plan


def probes(root,label):
    """Exercise trusted fixtures only; never select legacy baseline in this phase."""
    if not label.isalnum():raise ValueError('invalid probe evidence label')
    check_staging(root);records=[]
    for mode in ('fixture','security','memory','cpu','file','wall','quota'):
        capture_label='baseline-'+label+'-probe-'+mode;record=capture(root,capture_label,mode);process=record['process']
        raw=(root/(capture_label+'.export/process.stdout')).read_bytes()
        expected={'fixture':(0,),'security':(0,),'memory':(0,),'cpu':(137,-9,152),
                  'file':(153,-25),'wall':(-9,),'quota':(0,)}
        passed=process['target_exit'] in expected[mode]
        markers={'fixture':b'SYNTHETIC_BASELINE','security':b'BASELINE_SECURITY_PASSED',
                 'memory':b'MEMORY_DENIED','quota':b'QUOTA_DENIED'}
        if mode in markers:passed &= markers[mode] in raw
        if mode=='wall':passed &= process['termination']=='timeout'
        record['passed']=bool(passed);records.append(record)
        if not passed:
            private_write(root/('baseline-'+label+'-probes-failed.json'),json.dumps(records,indent=2).encode())
            return 1
    packet={'tools':tools_digest(),'results':records}
    private_write(root/'baseline-probes-passed.json',json.dumps(packet,indent=2).encode())
    return 0


def run(root,run_id,attempt):
    """Perform one fixed-ID bounded attempt; successful runs cannot be repeated."""
    preflight(root)
    packet=strict_json((root/'baseline-probes-passed.json').read_bytes())
    if packet['tools']!=tools_digest() or len(packet['results'])!=7 or not all(x['passed'] for x in packet['results']):
        raise ValueError('stale/failed baseline probes')
    if run_id not in ('BASELINE_A','BASELINE_B') or attempt not in (1,2):raise ValueError('unapproved baseline identity/attempt')
    if attempt==2:
        prior=strict_json((root/(run_id+'-1.result.json')).read_bytes())
        if prior.get('passed') is not False:raise ValueError('no failed first attempt to correct')
    label=run_id+'-'+str(attempt)
    private_write(root/(label+'.started.json'),json.dumps({'plan_sha256':PLAN_SHA,'authority':'ADR-0009'}).encode())
    capture_record=capture(root,label,'baseline');process=capture_record['process']
    config=strict_json((root/'inputs/config.json').read_bytes())
    result={'schema_version':1,'attempted':True,'process_exit':process['target_exit'],
            'termination':process['termination'],'dependencies_verified':True,'inputs_verified':True,
            'binary_sha256':BINARY_SHA,'expected_seed':config['seed'],'expected_run_id':'baseline'}
    output=root/(label+'.export/baseline')
    errors,hashes,projection=validate(result,output)
    preflight(root)
    result.update(passed=not errors,errors=errors,artifact_sha256=hashes,summary_projection_sha256=projection,
                  authority='ADR-0009',plan_sha256=PLAN_SHA,scientific_validation='UNVALIDATED')
    private_write(root/(label+'.result.json'),json.dumps(result,indent=2).encode())
    print(json.dumps({'run':run_id,'attempt':attempt,'passed':result['passed'],'exit':result['process_exit']}),flush=True)
    return 0 if not errors else 1


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase',choices=['probes','run']);parser.add_argument('private_root',type=Path)
    parser.add_argument('--run-id',choices=['BASELINE_A','BASELINE_B']);parser.add_argument('--attempt',type=int,choices=[1,2],default=1)
    parser.add_argument('--probe-label',default='revised1')
    args=parser.parse_args()
    if args.phase=='probes':return probes(args.private_root,args.probe_label)
    if args.run_id is None:parser.error('--run-id required')
    return run(args.private_root,args.run_id,args.attempt)


if __name__=='__main__':raise SystemExit(main())
