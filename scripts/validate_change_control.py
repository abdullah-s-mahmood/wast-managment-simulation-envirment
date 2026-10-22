#!/usr/bin/env python3
"""Read-only ADR completeness and declared material-change decision checks."""
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
SECTIONS=('Context','Options considered','Decision','Evidence and assumptions',
          'Consequences','Validation and revisit conditions')
FLAGS=('adds_dependency','changes_public_contract','changes_science','irreversible')
STATUSES=('Proposed','Provisional','Accepted','Rejected','Superseded')


def inspect_adr(text):
    """Return explicit status and missing/empty/duplicate section diagnostics.

Qualifiers such as 'Accepted in principle' stay visible in source and require
scope review. A parsed Accepted token never accepts the qualified details.
"""
    errors=[]
    declarations=re.findall(r'^- (?:\*\*)?Status:\s*(.+)$',text,re.M)
    match=re.match(r'('+'|'.join(STATUSES)+r')\b',declarations[0]) if len(declarations)==1 else None
    status=match[1] if match else None
    if status is None: errors.append('missing/ambiguous decision status')
    headings=list(re.finditer(r'^## (.+)$',text,re.M))
    for section in SECTIONS:
        found=[i for i,h in enumerate(headings) if h[1]==section]
        if len(found)!=1:
            errors.append('missing/duplicate '+section); continue
        index=found[0]; start=headings[index].end()
        end=headings[index+1].start() if index+1<len(headings) else len(text)
        if not text[start:end].strip(): errors.append('empty '+section)
    return status,errors


def check_change(change,decisions):
    """Require an accepted complete ADR for declared material changes.

This does not discover undeclared dependencies or contract changes in code;
full diff/dependency review must independently validate the declaration.
"""
    if (not isinstance(change,dict) or set(change)!=set(FLAGS)|{'schema_version','decision_id','rationale'}
            or type(change['schema_version']) is not int or change['schema_version']!=1
            or any(type(change[k]) is not bool for k in FLAGS)
            or not isinstance(change['rationale'],str) or not change['rationale'].strip()):
        return ['invalid change declaration']
    if not any(change[k] for k in FLAGS):
        return [] if change['decision_id'] is None else ['routine declaration must identify no decision']
    key=change['decision_id']
    if not isinstance(key,str) or not re.fullmatch(r'ADR-[0-9]{4}',key) or key not in decisions: return ['material change lacks decision record']
    status,errors=inspect_adr(decisions[key])
    return errors + ([] if status=='Accepted' else ['decision not accepted for implementation'])


def validate_repository(root):
    errors=[]; seen=set()
    paths=sorted((root/'docs/adr').glob('ADR-*.md'))
    if not paths: return ['no decision records']
    for path in paths:
        match=re.fullmatch(r'(ADR-[0-9]{4})-.+\.md',path.name)
        if not match or match[1] in seen:
            errors.append('invalid/duplicate ADR ID'); continue
        seen.add(match[1])
        try:
            _,issues=inspect_adr(path.read_text(encoding='utf-8'))
            errors.extend(path.name+': '+issue for issue in issues)
        except (OSError,UnicodeError): errors.append(path.name+': unreadable ADR')
    return errors


if __name__=='__main__':
    failures=validate_repository(ROOT)
    for failure in failures: print('FAIL: '+failure,file=sys.stderr)
    if not failures: print('PASS: ADR status/section completeness only; substantive change review still required.')
    raise SystemExit(bool(failures))
