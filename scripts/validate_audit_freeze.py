#!/usr/bin/env python3
"""Validate a source-audit freeze against immutable Git blobs, never model validity."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from scripts import inventory_legacy as intake
from scripts.validate_baseline_result import strict_json


def git_blob(root,commit,path):
    """Read bounded public documentation at a pinned commit without a shell."""
    part=PurePosixPath(path)
    if (not re.fullmatch('[0-9a-f]{40}',commit) or not isinstance(path,str)
            or not re.fullmatch(r'[A-Za-z0-9_./-]+',path) or part.is_absolute()
            or '..' in part.parts or str(part)!=path
            or not (path.startswith('docs/') or path in ('README.md','AGENTS.md'))
            or part.suffix not in ('.md','.json')):raise ValueError('unsafe freeze reference')
    spec=commit+':'+path
    size=subprocess.run(['git','cat-file','-s',spec],cwd=root,capture_output=True,timeout=10,check=True)
    if not 0<=int(size.stdout)<=1048576:raise ValueError('frozen blob budget')
    result=subprocess.run(['git','show',spec],cwd=root,capture_output=True,timeout=10,check=True)
    if len(result.stdout)!=int(size.stdout):raise ValueError('frozen blob size mismatch')
    return result.stdout


def validate(data,root):
    """Check identity, complete source references and explicit unresolved gates.

Checksums establish consistency, not authenticity or correctness of prose.
The owner-authorized substantive self-audit remains a separate acceptance gate.
    """
    if (not isinstance(data,dict) or type(data.get('schema_version')) is not int or data['schema_version']!=1
            or data.get('freeze_id')!='AUDIT-FREEZE-001' or not intake.verify_manifest(data)
            or data.get('scientific_validation')!='UNVALIDATED' or data.get('source_reuse')!='PROHIBITED'
            or data.get('accepted_models')!=[] or data.get('accepted_platform_versions')!=[]):raise ValueError('invalid freeze/trust promotion')
    source=data['source_manifest']
    standalone=strict_json((Path(root)/'docs/audit/S016_SOURCE_MANIFEST.json').read_bytes())
    if intake.canonical_digest(standalone)!=data['source_manifest_sha256']:raise ValueError('standalone source manifest disagreement')
    if (intake.canonical_digest(source)!=data['source_manifest_sha256']
            or source.get('source_id')!='LEGACY-CANDIDATE-001'
            or type(source.get('compressed_bytes')) is not int or source['compressed_bytes']!=487062036
            or source.get('archive_sha256')!='da08e1a78e73215ddf9d165e32a07f262a0b8379b3b04f4b17b27d5b6b525da8'
            or source.get('source_reuse')!='PROHIBITED' or source.get('license_status')!='UNRESOLVED'
            or source.get('scientific_validation')!='UNVALIDATED'
            or source.get('security_clearance')!='NOT_GRANTED' or source.get('inventory_complete') is not True):raise ValueError('source manifest or clearance promotion')
    if not isinstance(data.get('artifacts'),list) or not data['artifacts']:raise ValueError('missing artifacts')
    ids=set();paths=set()
    for row in data['artifacts']:
        if row['id'] in ids or row['path'] in paths:raise ValueError('duplicate artifact')
        blob=git_blob(root,data['source_state_commit'],row['path'])
        if hashlib.sha256(blob).hexdigest()!=row['sha256']:raise ValueError('frozen artifact changed')
        ids.add(row['id']);paths.add(row['path'])
    rows=data.get('conclusions')
    required_topics={'identity','execution','historical_trust','model_extraction','discrepancies','scientific_models','licensing','platform_versions','dynamic_semantics'}
    if (not isinstance(rows,list) or len(rows)!=len(required_topics)
            or {row['topic'] for row in rows}!=required_topics):raise ValueError('missing/duplicated conclusion topic')
    seen=set()
    for row in rows:
        if row['id'] in seen or row['status'] not in ('OBSERVED','UNRESOLVED'):raise ValueError('conclusion status')
        if not isinstance(row['claim'],str) or not row['claim'].strip():raise ValueError('missing claim')
        if not set(row['evidence']).issubset(ids):raise ValueError('unknown evidence reference')
        if row['status']=='OBSERVED' and not row['evidence']:raise ValueError('unsupported conclusion')
        if row['status']=='UNRESOLVED' and not row.get('remaining_evidence'):raise ValueError('hidden unresolved gate')
        if row['topic'] in ('scientific_models','licensing','platform_versions','dynamic_semantics') and row['status']!='UNRESOLVED':raise ValueError('unresolved topic promoted')
        seen.add(row['id'])
    for version in data['observed_versions']:
        if version['decision']!='AUDIT_OBSERVATION_ONLY' or version['evidence'] not in ids:raise ValueError('version promoted')
    progress=strict_json(git_blob(root,data['source_state_commit'],'docs/STATE/PROGRESS.json'))
    statuses={row['id']:row['status'] for row in progress['sprints']}
    if data['frozen_sprints']!=[f'S{i:03d}' for i in range(9,16)] or any(statuses.get(s)!='completed' for s in data['frozen_sprints']):raise ValueError('unaccepted audit phase')
    return {'freeze_id':data['freeze_id'],'manifest_sha256':data['manifest_sha256'],
            'source_state_commit':data['source_state_commit'],'verified_artifacts':len(ids),
            'verified_conclusions':len(seen),'status':'VALID_SOURCE_AUDIT_FREEZE',
            'scientific_validation':'UNVALIDATED','source_reuse':'PROHIBITED'}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('freeze',type=Path);parser.add_argument('--repository',type=Path,default=ROOT);args=parser.parse_args()
    try:result=validate(strict_json(args.freeze.read_bytes()),args.repository)
    except (OSError,ValueError,KeyError,TypeError,AttributeError,subprocess.SubprocessError):
        print('INVALID_OR_UNAVAILABLE_AUDIT_FREEZE',file=sys.stderr);return 1
    print(json.dumps(result,indent=2));return 0


if __name__=='__main__':raise SystemExit(main())
