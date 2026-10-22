#!/usr/bin/env python3
"""Check a synthetic governance proposal against separately retained model bytes.

This boundary example is not a runtime/scenario schema or simulator. S025–S036
will define those contracts. No physical or causal validation is performed.
"""
import argparse
import hashlib
from pathlib import Path
import sys

if __package__:
    from .validate_evidence_ledger import read_json
else:
    from validate_evidence_ledger import read_json

SETTINGS = frozenset(('population', 'map', 'bin_count', 'fleet_size', 'depot_placement'))
ROLES = frozenset(('manipulated', 'held_fixed', 'blocked'))
FIELDS = frozenset(('governance_version', 'model_sha256', 'settings', 'factor_roles',
                    'measurements', 'outcomes'))


def validate(proposal, model):
    """Return diagnostics without mutating inputs; model is a caller-selected Path.

Model identity is an exact-byte SHA-256, so even whitespace changes require an
explicit baseline change. A matching hash establishes identity, not correctness.
Settings are opaque nonempty labels here; physical validation is deferred.
"""
    if (not isinstance(proposal, dict) or set(proposal) != FIELDS
            or type(proposal['governance_version']) is not int
            or proposal['governance_version'] != 1):
        return ['invalid governance proposal fields/version']
    errors = []
    try:
        if proposal['model_sha256'] != hashlib.sha256(model.read_bytes()).hexdigest():
            errors.append('model identity changed')
    except OSError:
        errors.append('model baseline unavailable')
    settings, roles = proposal['settings'], proposal['factor_roles']
    if (not isinstance(settings, dict) or set(settings) != SETTINGS
            or any(not isinstance(v, str) or not v.strip() for v in settings.values())):
        errors.append('invalid settings or forbidden model override')
    if (not isinstance(roles, dict) or set(roles) != SETTINGS
            or any(not isinstance(v, str) or v not in ROLES for v in roles.values())):
        errors.append('each setting requires an explicit experimental role')
    lists = []
    for field in ('measurements', 'outcomes'):
        items = proposal[field]
        if (not isinstance(items, list) or not items
                or any(not isinstance(v, str) or not v.strip() for v in items)):
            errors.append('invalid ' + field)
        elif len(items) != len(set(items)):
            errors.append('duplicate ' + field)
        else:
            lists.append(set(items))
    if len(lists) == 2 and lists[0] & lists[1]:
        errors.append('measurement and outcome identifiers must be distinct')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('proposal', type=Path)
    parser.add_argument('--model', required=True, type=Path)
    args = parser.parse_args()
    try:
        errors = validate(read_json(args.proposal), args.model)
    except (OSError, UnicodeError, ValueError, TypeError):
        errors = ['unreadable/malformed governance proposal']
    for error in errors:
        print('FAIL: ' + error, file=sys.stderr)
    if errors:
        return 1
    print('PASS: governance separation; model bytes unchanged. No scientific validity claim.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
