#!/usr/bin/env python3
"""Validate the custom evidence record contract, not scientific truth."""
import argparse
import hashlib
from datetime import date
import json
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key')
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError('non-finite JSON value')


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_object,
                      parse_constant=reject_constant)


def relative_file(root, name):
    if (not name or '\\' in name or PurePosixPath(name).is_absolute()
            or any(part in ('', '.', '..') for part in name.split('/'))):
        raise ValueError('unsafe path')
    path = root / name
    if not path.resolve().is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError('missing/escaping file')
    return path


def resolve_pointer(value, pointer):
    if not pointer.startswith('/'):
        raise ValueError('configuration pointer must be nonempty and start with slash')
    for part in pointer[1:].split('/'):
        if re.search(r'~(?![01])', part):
            raise ValueError('invalid pointer escape')
        key = part.replace('~1', '/').replace('~0', '~')
        if isinstance(value, dict):
            value = value[key]
        elif isinstance(value, list) and re.fullmatch(r'0|[1-9][0-9]*', key):
            value = value[int(key)]
        else:
            raise ValueError('invalid pointer component')
    return value


def validate(ledger, contract, root=ROOT, production=True):
    errors = []
    if (not isinstance(ledger, dict) or set(ledger) != set(contract['ledger_keys'])
            or type(ledger.get('schema_version')) is not int
            or ledger['schema_version'] != contract['contract_version']
            or not isinstance(ledger.get('records'), list)):
        return ['invalid ledger schema/version']
    seen = set()
    required = set(contract['record_string_fields'] + contract['record_boolean_fields'] + ['variables'])
    for index, record in enumerate(ledger['records']):
        prefix = f'record[{index}]'
        if not isinstance(record, dict) or set(record) != required:
            errors.append(prefix + ': missing/unknown fields')
            continue
        if any(not isinstance(record[k], str) or not record[k].strip()
               for k in contract['record_string_fields']):
            errors.append(prefix + ': empty/non-string field')
            continue
        if any(type(record[k]) is not bool for k in contract['record_boolean_fields']):
            errors.append(prefix + ': invalid boolean')
            continue
        if not re.fullmatch(r'EV-[A-Z0-9]+(?:-[A-Z0-9]+)*', record['id']) or record['id'] in seen:
            errors.append(prefix + ': invalid/duplicate evidence ID')
        seen.add(record['id'])
        if any(record[k] not in choices for k, choices in contract['enums'].items()):
            errors.append(prefix + ': unsupported classification/status')
        variables = record['variables']
        if not isinstance(variables, list):
            errors.append(prefix + ': invalid variables')
        else:
            symbols = set()
            for variable in variables:
                if (not isinstance(variable, dict) or set(variable) != set(contract['variable_fields'])
                        or any(not isinstance(v, str) or not v.strip() for v in variable.values())):
                    errors.append(prefix + ': incomplete variable/units/range')
                    continue
                if variable['symbol'] in symbols:
                    errors.append(prefix + ': duplicate variable symbol')
                symbols.add(variable['symbol'])
            if not variables and record['kind'] in ('parameter', 'equation', 'distribution'):
                errors.append(prefix + ': numerical record requires variables/units')
        try:
            if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', record['access_date']):
                raise ValueError('invalid date format')
            date.fromisoformat(record['access_date'])
        except ValueError:
            errors.append(prefix + ': invalid access date')
        if record['domain_transfer_required'] or record['evidence_class'] == 'E3':
            if not record['domain_transfer_required'] or record['transfer_rationale'].startswith('not_applicable:'):
                errors.append(prefix + ': domain transfer requires rationale')
        decision = record['decision']
        synthetic = decision == 'synthetic'
        if synthetic:
            if production or record['evidence_class'] != 'E5' or record['verification_status'] != 'synthetic':
                errors.append(prefix + ': synthetic evidence forbidden/inconsistently labelled')
            if not record['source_url'].startswith('fixture:'):
                errors.append(prefix + ': synthetic source must use fixture URL')
        else:
            parsed = urlparse(record['source_url'])
            if parsed.scheme not in ('https', 'http') or not parsed.hostname:
                errors.append(prefix + ': unverifiable source URL')
            if record['verification_status'] == 'synthetic':
                errors.append(prefix + ': synthetic verification cannot support real claim')
        if not (record['doi'].startswith('not_applicable: ') or re.fullmatch(r'10\.\d{4,9}/\S+', record['doi'])):
            errors.append(prefix + ': invalid DOI or missing inapplicability reason')
        if decision == 'accepted_for_implementation':
            if record['verification_status'] != 'verified' or record['evidence_class'] in ('E4', 'E5'):
                errors.append(prefix + ': unverified/unsupported acceptance')
        if synthetic or decision == 'accepted_for_implementation':
            if not re.fullmatch(r'[a-f0-9]{64}', record['source_sha256']):
                errors.append(prefix + ': retained-source SHA-256 required')
            try:
                source = relative_file(root, record['source_path'])
                if hashlib.sha256(source.read_bytes()).hexdigest() != record['source_sha256']:
                    raise ValueError('source hash mismatch')
                config = read_json(relative_file(root, record['config_path']))
                resolve_pointer(config, record['config_pointer'])
                relative_file(root, record['reference_test'])
                relative_file(root, record['verification_artifact'])
            except (OSError, UnicodeError, ValueError, KeyError, IndexError, TypeError):
                errors.append(prefix + ': broken source/config/test mapping')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('ledger', nargs='?', type=Path, default=ROOT / 'docs/evidence/ledger.json')
    args = parser.parse_args()
    try:
        contract = read_json(ROOT / 'docs/evidence/record_contract.json')
        ledger = read_json(args.ledger)
        errors = validate(ledger, contract)
    except (OSError, UnicodeError, ValueError, KeyError, TypeError):
        print('FAIL: cannot read valid evidence ledger/contract', file=sys.stderr)
        return 1
    for error in errors:
        print('FAIL: ' + error, file=sys.stderr)
    if errors:
        return 1
    print(f'PASS: {len(ledger["records"])} evidence records satisfy structural prerequisites.')
    print('NOTE: structure is not source verification or scientific validation.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
