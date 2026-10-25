#!/usr/bin/env python3
"""Check private S012 execution/artifact evidence; never launch a baseline.

A valid result is a tested software artifact contract, not scientific validation,
license clearance or authorization. Caller must wait for target exit and use an
owner-only directory with no concurrent writers. Metadata is not proof of who
executed a program; retained command/environment/provenance evidence is separate.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import stat

MAX_BYTES=67108864  # 64 MiB cumulative private output evidence.
MAX_LINE_BYTES=1048576
BINARY_SHA='939c2bd50379e557936f0adb944dfe1e38fbad9428be8c738b6493b198097fd3'


def strict_json(data):
    """Reject duplicate keys and nonfinite JSON numbers instead of normalizing."""
    def pairs(items):
        result={}
        for key,value in items:
            if key in result:raise ValueError('duplicate JSON key')
            result[key]=value
        return result
    def constant(value):raise ValueError('nonfinite JSON constant')
    return json.loads(data,object_pairs_hook=pairs,parse_constant=constant)


def number(value):
    """Finite nonnegative numeric value; booleans are not measurements."""
    return type(value) in (int,float) and math.isfinite(value) and value>=0


def validate(record,root):
    """Return errors/digests, requiring exit success AND real regular artifacts.

Observed legacy event time_s is in simulated seconds; this checks representation,
not physical units/conservation. Summary host-runtime field is retained raw and
excluded only from a separate, explicitly named comparison projection. No other
summary fields or event bytes are removed from reproducibility comparison.
"""
    errors=[];hashes={};projection=None
    if (not isinstance(record,dict) or type(record.get('schema_version')) is not int
            or record['schema_version']!=1
            or record.get('attempted') is not True or type(record.get('process_exit')) is not int
            or record['process_exit']!=0 or record.get('termination')!='exited'
            or record.get('dependencies_verified') is not True or record.get('inputs_verified') is not True
            or record.get('binary_sha256')!=BINARY_SHA
            or type(record.get('expected_seed')) is not int
            or not isinstance(record.get('expected_run_id'),str) or not record['expected_run_id']):
        return ['incomplete/failed/unverified execution evidence'],hashes,projection
    root=Path(root)
    if root.is_symlink() or not root.is_dir():return ['invalid output directory'],hashes,projection
    try:
        total=0
        for index,path in enumerate(root.rglob('*')):
            if index>=64:raise ValueError('output count budget')
            info=path.lstat()
            if stat.S_ISDIR(info.st_mode):continue
            if not stat.S_ISREG(info.st_mode):raise ValueError('output link/special member')
            total+=info.st_size
            if total>MAX_BYTES:raise ValueError('output byte budget')
            with path.open('rb') as stream:hashes[str(path.relative_to(root))]=hashlib.file_digest(stream,'sha256').hexdigest()
        if 'failure.json' in hashes:raise ValueError('failure artifact present')
        if not {'events.jsonl','run_summary.json'} <= set(hashes):raise ValueError('missing required output')
        with (root/'run_summary.json').open('rb') as stream:data=stream.read(MAX_LINE_BYTES+1)
        if len(data)>MAX_LINE_BYTES:raise ValueError('summary byte budget')
        summary=strict_json(data)
        if (not isinstance(summary,dict) or summary.get('route_complete') is not True
                or summary.get('validation_only') is not False
                or summary.get('run_id')!=record['expected_run_id']
                or type(summary.get('seed')) is not int or summary['seed']!=record['expected_seed']
                or not number(summary.get('simulation_runtime_seconds'))):
            raise ValueError('invalid baseline summary')
        count=0
        with (root/'events.jsonl').open('rb') as stream:
            while True:
                line=stream.readline(MAX_LINE_BYTES+1)
                if not line:break
                if len(line)>MAX_LINE_BYTES:raise ValueError('event line budget')
                event=strict_json(line)
                if (not isinstance(event,dict) or event.get('run_id')!=record['expected_run_id']
                        or type(event.get('seed')) is not int or event['seed']!=record['expected_seed']
                        or not number(event.get('time_s')) or not isinstance(event.get('kind'),str)
                        or not event['kind']):raise ValueError('invalid baseline event')
                count+=1
        if not count:raise ValueError('empty event stream')
        semantic=dict(summary);semantic.pop('simulation_runtime_seconds')
        projection=hashlib.sha256(json.dumps(semantic,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
    except (OSError,ValueError,TypeError,OverflowError):
        errors.append('invalid/missing/corrupt/over-budget baseline artifacts')
    return errors,hashes,projection


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record',type=Path);parser.add_argument('output_dir',type=Path)
    args=parser.parse_args()
    try:
        with args.record.open('rb') as stream:data=stream.read(65537)
        if len(data)>65536:raise ValueError('record byte budget')
        record=strict_json(data);errors,_,_=validate(record,args.output_dir)
    except (OSError,ValueError):errors=['invalid execution record']
    print(json.dumps({'status':'INVALID_BASELINE' if errors else 'VALID_BASELINE_ARTIFACTS',
                      'scientific_validation':'UNVALIDATED','errors':errors}))
    return 1 if errors else 0


if __name__=='__main__':raise SystemExit(main())
