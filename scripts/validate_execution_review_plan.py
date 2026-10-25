#!/usr/bin/env python3
"""Validate S011 review metadata only. Never prepare, build or execute a target."""
import argparse
import json
import re
from pathlib import Path
import sys

if __package__:
    from . import inventory_legacy as inventory
    from .validate_evidence_ledger import read_json
else:
    import inventory_legacy as inventory
    from validate_evidence_ledger import read_json

FIELDS = {'schema_version','purpose','archive_sha256','archive_bytes','inventory_sha256',
          'target','execution_authorized','working_copy_prepared','runtime_status','inputs',
          'source_anchors','proposed_source_copy_entries','cases','limits','network_access',
          'dependency_status','source_reuse','scientific_validation'}
ANCHORS = {'build_target','main','validation_branch','runtime_inputs','timesteps',
           'seed_derivation','mobility_boundary','network_boundary','event_writer','summary_writer'}
LIMITS = {'max_cases','validation_wall_seconds','validation_cpu_seconds','validation_memory_bytes',
          'build_wall_seconds','build_cpu_seconds','build_memory_bytes'}
# Intentional fixed review scope, derived from the inspected argc/argv branches.
# These are predictions to test later, not observations of a legacy execution.
CASES = {
    'ABS_A':('A',['BIN_ABS','--validate-config','CFG_ABS','CITY_ABS'],0),
    'ABS_B':('B',['BIN_ABS','--validate-config','CFG_ABS','CITY_ABS'],0),
    'REL_A':('A',['BIN_ABS','--validate-config','CFG_ABS','CITY_REL'],0),
    'REL_B':('B',['BIN_ABS','--validate-config','CFG_ABS','CITY_REL'],1),
    'MISSING_CITY':('A',['BIN_ABS','--validate-config','CFG_ABS'],2),
}


def validate(plan, manifest):
    """Return diagnostics; a valid static plan grants no permission or clearance.

This checks metadata identity and limited proposed invocations. It does not
certify source semantics, licenses, a binary, an isolation boundary or actual
outcomes. Source-line claims require the separately recorded read-only review.
"""
    if (not isinstance(plan,dict) or set(plan)!=FIELDS
            or type(plan.get('schema_version')) is not int or plan['schema_version']!=1):
        return ['invalid review plan schema/version']
    if (not isinstance(manifest,dict) or manifest.get('schema_version')!=2
            or manifest.get('complete') is not True or manifest.get('identity_verified') is not True
            or not isinstance(manifest.get('members'),list) or not inventory.verify_manifest(manifest)):
        return ['unverified inventory']
    errors=[]
    if (type(plan['archive_bytes']) is not int or plan['archive_bytes']<=0
            or plan['archive_bytes']!=manifest.get('compressed_bytes')
            or plan['archive_sha256']!=manifest.get('archive_sha256')
            or plan['inventory_sha256']!=manifest.get('manifest_sha256')):
        errors.append('baseline/inventory identity mismatch')
    expected = {'purpose':'STATIC_REVIEW_ONLY','target':'sw_cosim','execution_authorized':False,
                'working_copy_prepared':False,'runtime_status':'NOT_RUN','network_access':'DENIED',
                'dependency_status':'UNVERIFIED_TRUSTED_PACKAGES_REQUIRED',
                'source_reuse':'PROHIBITED','scientific_validation':'UNVALIDATED'}
    for key,value in expected.items():
        if type(plan[key]) is not type(value) or plan[key]!=value:
            errors.append('static scope/status violation: '+key)
    entries={}
    for member in manifest['members']:
        if not isinstance(member,dict) or not isinstance(member.get('entry_id'),str):
            return ['malformed inventory member']
        if member['entry_id'] in entries:return ['duplicate inventory member ID']
        entries[member['entry_id']]=member

    def reference(ref, anchor=False):
        keys={'entry_id','sha256'}|({'line_start','line_end'} if anchor else set())
        if (not isinstance(ref,dict) or set(ref)!=keys
                or not isinstance(ref.get('entry_id'),str)
                or not isinstance(ref.get('sha256'),str)
                or not re.fullmatch(r'[0-9a-f]{64}',ref['sha256'])):
            errors.append('invalid source/input reference');return
        member=entries.get(ref['entry_id'])
        if (not member or member.get('kind')!='file' or member.get('quarantined') is not False
                or member.get('sha256')!=ref['sha256']):
            errors.append('missing/stale/quarantined source reference')
        if anchor and (type(ref['line_start']) is not int or type(ref['line_end']) is not int
                       or not 1<=ref['line_start']<=ref['line_end']):
            errors.append('invalid source-line range')

    for key,required in (('inputs',{'config','city_json','road_network'}),('source_anchors',ANCHORS)):
        section=plan[key]
        if not isinstance(section,dict) or set(section)!=required:
            errors.append('missing/unknown '+key);continue
        for ref in section.values():reference(ref,anchor=key=='source_anchors')
    copies=plan['proposed_source_copy_entries']
    if not isinstance(copies,list) or not copies:
        errors.append('missing proposed preparation scope')
    else:
        seen=set()
        for ref in copies:
            reference(ref)
            if isinstance(ref,dict) and isinstance(ref.get('entry_id'),str):
                if ref['entry_id'] in seen:errors.append('duplicate preparation member')
                seen.add(ref['entry_id'])
    cases=plan['cases']
    if not isinstance(cases,list):return errors+['invalid cases']
    seen=set()
    for case in cases:
        if (not isinstance(case,dict) or set(case)!={'id','cwd','argv','expected_exit','status'}
                or not isinstance(case.get('id'),str) or case['id'] not in CASES):
            errors.append('invalid/unknown case');continue
        key=case['id']
        if key in seen:errors.append('duplicate case')
        seen.add(key);cwd,argv,expected_exit=CASES[key]
        if (case['cwd']!=cwd or case['argv']!=argv or type(case['expected_exit']) is not int
                or case['expected_exit']!=expected_exit or case['status']!='NOT_RUN'):
            errors.append('out-of-scope invocation or unsupported result claim')
    if seen!=set(CASES):errors.append('required review cases missing')
    limits=plan['limits']
    if (not isinstance(limits,dict) or set(limits)!=LIMITS
            or any(type(x) is not int or x<=0 for x in limits.values())
            or limits['max_cases']!=len(CASES)):
        errors.append('invalid planned resource limits')
    return errors


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan',type=Path)
    parser.add_argument('--inventory',type=Path,required=True)
    args=parser.parse_args()
    try:errors=validate(read_json(args.plan),read_json(args.inventory))
    except (OSError,UnicodeError,ValueError,TypeError,KeyError):
        errors=['unreadable/malformed review packet']
    if errors:
        for error in errors:print('FAIL: '+error,file=sys.stderr)
        return 1
    print(json.dumps({'status':'VALID_STATIC_PLAN','execution_authorized':False,
                      'runtime_status':'NOT_RUN','case_count':len(CASES)},sort_keys=True))
    return 0


if __name__=='__main__':
    raise SystemExit(main())
