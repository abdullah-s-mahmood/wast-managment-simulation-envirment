#!/usr/bin/env python3
"""Check evidence completeness; never execute commands, accept or merge a sprint."""
import argparse
import hashlib
from pathlib import Path
import re
import sys

if __package__:
    from .validate_evidence_ledger import read_json, relative_file
else:
    from validate_evidence_ledger import read_json, relative_file

ROOT = Path(__file__).resolve().parents[1]
POLICY = read_json(ROOT / 'docs/quality/gates.json')
TEXT = {'id', 'status', 'command', 'assertion', 'artifact', 'sha256', 'platform',
        'versions', 'rationale', 'head_sha'}


def validate(manifest, root, head):
    """Validate exact-head records and retained artifacts, without trusting narrative.

A caller supplies the head independently from the manifest. This checks internal
consistency, not authenticity of commands, artifacts, CI or applicability claims.
Those require actual observations and ADR-0005 author self-audit before merge.
"""
    if (not isinstance(head, str) or not re.fullmatch(r'[a-f0-9]{40}', head)
            or not isinstance(manifest, dict)
            or set(manifest) != {'schema_version', 'head_sha', 'checks'}
            or type(manifest['schema_version']) is not int or manifest['schema_version'] != 1
            or manifest['head_sha'] != head or not isinstance(manifest['checks'], list)):
        return ['invalid/stale evidence manifest']
    errors, seen = [], set()
    for check in manifest['checks']:
        if (not isinstance(check, dict) or set(check) != TEXT | {'exit_code'}
                or any(not isinstance(check[k], str) or not check[k].strip() for k in TEXT)):
            errors.append('missing/invalid check record')
            continue
        key = check['id']
        if key not in POLICY or key in seen:
            errors.append('unknown/duplicate criterion')
            continue
        seen.add(key)
        if check['head_sha'] != head:
            errors.append(key + ': stale check head')
        if check['status'] == 'PASS':
            if type(check['exit_code']) is not int or check['exit_code'] != 0:
                errors.append(key + ': passing check requires recorded zero exit')
        elif check['status'] == 'NOT_APPLICABLE':
            if not POLICY[key]['allows_not_applicable'] or check['exit_code'] is not None:
                errors.append(key + ': mandatory/contradictory applicability')
        else:
            errors.append(key + ': failed/unexecuted/unknown status')
        try:
            artifact = relative_file(root, check['artifact'])
            if hashlib.sha256(artifact.read_bytes()).hexdigest() != check['sha256']:
                errors.append(key + ': artifact hash mismatch')
        except (OSError, ValueError):
            errors.append(key + ': missing/unsafe artifact')
    if seen != set(POLICY):
        errors.append('criteria missing')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--head', required=True)
    args = parser.parse_args()
    try:
        errors = validate(read_json(args.manifest), args.root, args.head)
    except (OSError, UnicodeError, ValueError, TypeError):
        errors = ['unreadable/malformed gate evidence']
    for error in errors:
        print('FAIL: ' + error, file=sys.stderr)
    if errors:
        return 1
    print('PASS: evidence completeness only; verify authenticity/applicability and GitHub CI before acceptance.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
