#!/usr/bin/env python3
"""Validate risk completeness and choose a safe action from explicit facts."""
from pathlib import Path
import re
import sys

if __package__:
    from .validate_evidence_ledger import read_json, relative_file
else:
    from validate_evidence_ledger import read_json, relative_file

ROOT=Path(__file__).resolve().parents[1]
FACTS=('scientific_evidence_available','guessed_scientific_value','irreversible',
       'explicit_authorization','test_failure','corrupt_results')
FIELDS={'id','affected_sprints','impact','trigger','mitigation','owner_action',
        'unblock_condition','source','status'}


def next_action(facts):
    """Return action without changing files, progress or authorization.

Evidence available means all evidence required by the current task is available;
for a task introducing no scientific claim, it is true only with a scope rationale.
These are explicit observed declarations, never guessed defaults. Actual source,
authorization and test observations must substantiate them outside this helper.
"""
    if (not isinstance(facts,dict) or set(facts)!=set(FACTS)
            or any(type(facts[key]) is not bool for key in FACTS)):
        raise ValueError('all observed facts must be explicitly declared booleans')
    if facts['corrupt_results']: return 'stop_pipeline_preserve_failed_run'
    if not facts['scientific_evidence_available'] or facts['guessed_scientific_value']:
        return 'stop_and_record_blocker'
    if facts['irreversible'] and not facts['explicit_authorization']:
        return 'request_specific_authorization'
    if facts['test_failure']: return 'investigate_and_retest'
    return 'continue_within_contract'


def validate_register(data):
    """Check every risk has an affected sprint, action and resume condition."""
    if (not isinstance(data,dict) or set(data)!={'schema_version','risks'}
            or type(data['schema_version']) is not int or data['schema_version']!=1
            or not isinstance(data['risks'],list) or not data['risks']):
        return ['invalid risk register/version']
    errors=[]; seen=set()
    for risk in data['risks']:
        if (not isinstance(risk,dict) or set(risk)!=FIELDS
                or any(not isinstance(risk[k],str) or not risk[k].strip() for k in FIELDS-{'affected_sprints'})):
            errors.append('incomplete risk record'); continue
        if (not re.fullmatch(r'R-[A-Z0-9]+(?:-[A-Z0-9]+)*',risk['id'])
                or risk['id'] in seen): errors.append('invalid/duplicate risk ID')
        seen.add(risk['id'])
        sprints=risk['affected_sprints']
        if (not isinstance(sprints,list) or not sprints
                or any(not isinstance(x,str) or not re.fullmatch(r'S[0-9]{3}',x)
                       or not 1<=int(x[1:])<=88 for x in sprints)
                or len(sprints)!=len(set(sprints))): errors.append('invalid affected sprints')
        if risk['status'] not in ('monitored','triggered','resolved'): errors.append('unknown risk status')
        try: relative_file(ROOT,risk['source'])
        except (OSError,ValueError): errors.append('missing/unsafe risk authority')
    return errors


if __name__=='__main__':
    try: errors=validate_register(read_json(ROOT/'docs/quality/risks.json'))
    except (OSError,UnicodeError,ValueError): errors=['unreadable/malformed risk register']
    for error in errors: print('FAIL: '+error,file=sys.stderr)
    if not errors: print('PASS: risk completeness; observed triggers/authorization require substantive verification.')
    raise SystemExit(bool(errors))
