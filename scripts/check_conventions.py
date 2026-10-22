#!/usr/bin/env python3
"""Read-only reference checker for S005 conventions, not a runtime unit library."""
import argparse
from datetime import datetime, timezone
from fractions import Fraction
import json
from pathlib import Path
import re
import sys

if __package__:
    from .validate_evidence_ledger import read_json
else:
    from validate_evidence_ledger import read_json

ROOT = Path(__file__).resolve().parents[1]


def load_catalog(data=None):
    """Load the versioned project-owned unit policy; reject unknown versions."""
    data = read_json(ROOT / 'docs/conventions/units.json') if data is None else data
    if (not isinstance(data, dict) or set(data) != {'schema_version', 'quantities'}
            or type(data['schema_version']) is not int or data['schema_version'] != 1
            or not isinstance(data['quantities'], dict)):
        raise ValueError('unsupported conventions catalog')
    return data['quantities']


def normalize_quantity(quantity, value, unit):
    """Return exact (Fraction value, canonical unit, dimension) or raise ValueError.

Inputs are decimal strings, at most 80 characters with exponent magnitude at
most 100. These computational limits are not applicability ranges for a model.
Conversions and quantity bounds are declared in the external policy catalog.
"""
    if not isinstance(value, str) or len(value) > 80:
        raise ValueError('value must be a bounded decimal string')
    match = re.fullmatch(r'[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE]([+-]?[0-9]+))?', value)
    if not match or (match[1] is not None and abs(int(match[1])) > 100):
        raise ValueError('invalid/nonfinite/oversized decimal')
    try:
        definition = load_catalog()[quantity]
        conversion = definition['units'][unit]
        result = Fraction(value) * Fraction(conversion['scale']) + Fraction(conversion['offset'])
        for key, violates in (('minimum', lambda bound: result < bound),
                              ('maximum', lambda bound: result > bound)):
            if definition[key] is not None and violates(Fraction(definition[key])):
                raise ValueError('quantity outside convention bounds')
        return result, definition['canonical_unit'], definition['dimension']
    except (KeyError, TypeError, ZeroDivisionError) as error:
        raise ValueError('unknown quantity/unit or invalid unit policy') from error


def normalize_timestamp(value):
    """Normalize the documented explicit-offset, microsecond RFC3339 subset to UTC."""
    if (not isinstance(value, str) or not re.fullmatch(
            r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?(?:Z|[+-](?:[01][0-9]|2[0-3]):[0-5][0-9])', value)
            or value.endswith('-00:00')):
        raise ValueError('explicit known offset required; unsupported timestamp precision')
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(timezone.utc).isoformat(timespec='microseconds').replace('+00:00', 'Z')
    except (ValueError, OverflowError) as error:
        raise ValueError('invalid calendar/offset or unsupported leap second') from error


def check_entities(entities):
    """Check synthetic entity identity without deriving IDs from mutable labels."""
    if not isinstance(entities, list):
        return ['entities must be a list']
    seen = set()
    for item in entities:
        if (not isinstance(item, dict) or set(item) != {'id', 'display_name'}
                or not isinstance(item['id'], str)
                or not re.fullmatch(r'[a-z][a-z0-9_]*-[A-Za-z0-9][A-Za-z0-9_-]{0,63}', item['id'])
                or not isinstance(item['display_name'], str) or not item['display_name'].strip()):
            return ['invalid entity ID/label']
        if item['id'] in seen:
            return ['duplicate entity ID']
        seen.add(item['id'])
    return []


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    quantity = sub.add_parser('quantity')
    quantity.add_argument('quantity'); quantity.add_argument('value'); quantity.add_argument('unit')
    timestamp = sub.add_parser('timestamp'); timestamp.add_argument('value')
    args = parser.parse_args()
    try:
        if args.command == 'quantity':
            value, unit, dimension = normalize_quantity(args.quantity, args.value, args.unit)
            print(json.dumps({'numerator':value.numerator,'denominator':value.denominator,'unit':unit,'dimension':dimension}))
        else:
            print(normalize_timestamp(args.value))
    except (OSError, UnicodeError, ValueError, TypeError) as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
