#!/usr/bin/env python3
"""Recheck retained S012 negative evidence and validate an audit-only register.

No legacy execution, repair, source patch or historical-result import exists.
CLI reproduces comparisons against accepted S012 hashes, not a new simulation.
"""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from scripts.validate_baseline_result import strict_json

MAX_BYTES=16777216


def frozen_bytes(path, expected):
    """Read a bounded regular file without following its final symlink."""
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    with os.fdopen(fd,'rb') as stream:
        before=os.fstat(stream.fileno())
        if not stat.S_ISREG(before.st_mode) or before.st_size>MAX_BYTES:raise ValueError('artifact budget/type')
        data=stream.read(MAX_BYTES+1);after=os.fstat(stream.fileno())
        key=lambda s:(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns)
        if key(before)!=key(after) or key(after)!=key(Path(path).lstat()):raise ValueError('artifact changed')
    if len(data)>MAX_BYTES or hashlib.sha256(data).hexdigest()!=expected:raise ValueError('artifact identity')
    return data


def differences(a,b,path=''):
    """Count structural/value differences; no normalization or value publication."""
    if type(a) is not type(b):return [path]
    if isinstance(a,dict):
        out=[]
        for key in sorted(set(a)|set(b)):
            here=path+'/'+key.replace('~','~0').replace('/','~1')
            out.extend([here] if key not in a or key not in b else differences(a[key],b[key],here))
        return out
    if isinstance(a,list):
        if len(a)!=len(b):return [path]
        return [p for i,(x,y) in enumerate(zip(a,b)) for p in differences(x,y,path+'/'+str(i))]
    return [] if a==b else [path]


def reproduce(root,outcome):
    """Reproduce three recorded failures from hash-bound retained audit artifacts."""
    if (outcome.get('audit_report_status')!='ACCEPTED_FAILED_REPRODUCTION_REPORT'
            or outcome.get('scientific_validation')!='UNVALIDATED'
            or outcome.get('source_changes') is not False):raise ValueError('unaccepted evidence provenance')
    events=[];summaries=[];exits=[];hashes=[]
    for i,label in enumerate(('BASELINE_A-1','BASELINE_B-1')):
        result=strict_json(frozen_bytes(Path(root)/(label+'.result.json'),outcome['private_evidence_receipts'][label+'.result.json']))
        if result['attempted'] is not True or result['termination']!='exited' or type(result['process_exit']) is not int:raise ValueError('no retained normal exit')
        exits.append(result['process_exit'])
        folder=Path(root)/(label+'.export')/'baseline'
        raw=frozen_bytes(folder/'events.jsonl',outcome['raw_output_sha256'][i]['events.jsonl'])
        hashes.append(hashlib.sha256(raw).hexdigest())
        lines=raw.splitlines()
        if not 1<=len(lines)<=100000 or any(len(line)>1048576 for line in lines):raise ValueError('event budget')
        parsed=[strict_json(line) for line in lines]
        if not all(isinstance(x,dict) for x in parsed):raise ValueError('event schema')
        events.append(parsed)
        summary=strict_json(frozen_bytes(folder/'run_summary.json',outcome['raw_output_sha256'][i]['run_summary.json']))
        if not isinstance(summary,dict):raise ValueError('summary schema')
        summaries.append(summary)
    if exits!=outcome['actual_exits']:raise ValueError('exit disagreement')
    route=[x.get('route_complete') for x in summaries];markers=[x.get('validation_only') for x in summaries]
    if any(type(x) is not bool for x in route+markers):raise ValueError('summary flag types')
    if route!=outcome['route_complete'] or markers!=outcome['validation_only_flags']:raise ValueError('summary disagreement')
    if len(events[0])!=len(events[1]):raise ValueError('unexpected event count difference')
    delta=Counter(p for x,y in zip(*events) for p in differences(x,y))
    if dict(delta)!=outcome['event_difference_inventory']['different_field_paths']:raise ValueError('event differences changed')
    summary_delta=differences(*summaries)
    if summary_delta!=['/'+x for x in outcome['raw_summary_different_keys']]:raise ValueError('summary differences changed')
    return {'schema_version':1,'evidence_origin':'HASH_BOUND_RETAINED_S012_AUDIT_NOT_NEW_RUN',
            'normal_runs_executed_now':0,'legacy_changes':False,'historical_results_imported':False,
            'findings':{'D-S015-001':exits==[3,3] and route==[False,False],
                        'D-S015-002':markers==[True,True],
                        'D-S015-003':hashes[0]!=hashes[1]},
            'actual_exits':exits,'route_complete':route,'validation_only_flags':markers,
            'event_count':len(events[0]),'different_field_paths':dict(sorted(delta.items())),
            'summary_different_paths':summary_delta,'scientific_validation':'UNVALIDATED',
            'source_reuse':'PROHIBITED'}


def validate_register(data):
    """Require prioritized, reproduced observations and explicit impact/authority."""
    if (not isinstance(data,dict) or type(data.get('schema_version')) is not int or data['schema_version']!=1
            or data.get('mode')!='AUDIT_ONLY' or data.get('legacy_action')!='NO_CHANGE'
            or data.get('historical_results_use')!='PROHIBITED_AS_VALIDATED_RESULTS'
            or data.get('scientific_validation')!='UNVALIDATED'
            or data.get('source_reuse')!='PROHIBITED'):raise ValueError('audit scope/trust violation')
    rows=data.get('issues');ids=set()
    if not isinstance(rows,list) or not rows:raise ValueError('missing issues')
    for row in rows:
        if not isinstance(row,dict) or row.get('id') in ids:raise ValueError('duplicate/malformed issue')
        if row.get('priority') not in ('P1','P2','P3') or row.get('status')!='OBSERVED_OPEN':raise ValueError('issue status')
        for key in ('id','classification','expected_basis','observed','minimal_reproducer','observable_consequence','source_reference','test_reference','resolution_boundary'):
            if not isinstance(row.get(key),str) or not row[key].strip():raise ValueError('missing issue evidence')
        if row.get('reproduction')!='RECHECKED_RETAINED_S012_EVIDENCE':raise ValueError('unreproduced issue')
        if set(row.get('impacts',{}))!={'state','random_streams','outputs','metrics'}:raise ValueError('missing impact mapping')
        if any(not isinstance(x,str) or not x for x in row['impacts'].values()):raise ValueError('unknown impact must be explicit')
        ids.add(row['id'])
    return {'issues':len(rows),'status':'VALID_AUDIT_REGISTER_NOT_FIXED_LEGACY','scientific_validation':'UNVALIDATED'}


def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='mode',required=True)
    check=sub.add_parser('check');check.add_argument('register',type=Path)
    repro=sub.add_parser('reproduce');repro.add_argument('retained_evidence_root',type=Path)
    args=parser.parse_args()
    import resource
    resource.setrlimit(resource.RLIMIT_AS,(268435456,268435456));resource.setrlimit(resource.RLIMIT_CPU,(60,60))
    try:
        if args.mode=='check':result=validate_register(strict_json(args.register.read_bytes()))
        else:result=reproduce(args.retained_evidence_root,strict_json((ROOT/'docs/audit/S012_BASELINE_OUTCOME.json').read_bytes()))
    except (OSError,ValueError,TypeError,KeyError,RecursionError,MemoryError):
        print('DISCREPANCY_AUDIT_INCOMPLETE',file=sys.stderr);return 1
    print(json.dumps(result,indent=2));return 0


if __name__=='__main__':raise SystemExit(main())
