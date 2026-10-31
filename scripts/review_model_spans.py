#!/usr/bin/env python3
"""Resolve reviewed source ranges privately without copying executable source.

The public plan describes observations, not scientific model acceptance. Exact
expressions remain content-addressed byte ranges in the immutable archive.
Identifiers and numeric spellings are retained privately before normalization.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts import inventory_test_evidence as inventory
from scripts import inventory_legacy as intake
from scripts.validate_baseline_result import strict_json

FIELDS = {'id', 'entry_id', 'source_sha256', 'line_start', 'line_end', 'category', 'observation'}
CATEGORIES = {'equation', 'default', 'distribution', 'time_rule', 'protocol', 'seed_rule', 'boundary'}


def validate_plan(plan):
    """Fail closed on unsupported/ambiguous plans; never accept trust promotions."""
    if (not isinstance(plan, dict) or set(plan) != {'schema_version', 'records'}
            or type(plan['schema_version']) is not int or plan['schema_version'] != 1
            or not isinstance(plan['records'], list) or not 1 <= len(plan['records']) <= 1024):
        raise ValueError('invalid review plan')
    ids = set()
    for row in plan['records']:
        if not isinstance(row, dict) or set(row) != FIELDS:
            raise ValueError('invalid record fields')
        if (not isinstance(row['id'], str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,64}', row['id'])
                or row['id'] in ids or not isinstance(row['entry_id'], str)
                or not re.fullmatch(r'entry-\d{8}', row['entry_id'])
                or not isinstance(row['source_sha256'], str)
                or not re.fullmatch('[0-9a-f]{64}', row['source_sha256'])
                or not isinstance(row['category'], str) or row['category'] not in CATEGORIES
                or not isinstance(row['observation'], str) or not 1 <= len(row['observation']) <= 1024):
            raise ValueError('invalid review metadata')
        if (any(type(row[k]) is not int for k in ('line_start', 'line_end'))
                or row['line_start'] < 1 or not row['line_start'] <= row['line_end']
                or row['line_end'] - row['line_start'] >= 80):
            raise ValueError('invalid source line range')
        ids.add(row['id'])
    return plan


def resolve(row, item, text):
    """Bind an observation to exact source bytes; do not evaluate any expression.

Observation text is a reviewer's E4 interpretation, not a machine-proven theorem.
Hash checks prove identity, not the correctness of that interpretation.
    """
    validate_plan({'schema_version': 1, 'records': [row]})
    data = text.encode('utf-8')
    if (row['entry_id'] != item['entry_id'] or row['source_sha256'] != item['sha256']
            or hashlib.sha256(data).hexdigest() != row['source_sha256']):
        raise ValueError('review source identity mismatch')
    lines = [line.encode('utf-8') for line in text.splitlines(keepends=True)]
    if row['line_end'] > len(lines):
        raise ValueError('source range exceeds file')
    start = sum(map(len, lines[:row['line_start'] - 1]))
    end = start + sum(map(len, lines[row['line_start'] - 1:row['line_end']]))
    if end - start > 8192:
        raise ValueError('source span budget')
    span = data[start:end]
    spelling = span.decode('utf-8')
    return {**row, 'byte_start': start, 'byte_end': end,
            'span_sha256': hashlib.sha256(span).hexdigest(),
            'original_names': sorted(set(re.findall(r'\b[A-Za-z_]\w*\b', spelling))),
            'original_numeric_spellings': re.findall(r"(?<![\w.])(?:\d[\d'_]*(?:\.[\d'_]*)?|\.\d[\d'_]*)(?:[eE][+-]?\d[\d'_]*)?", spelling),
            'expression_storage': 'EXACT_IMMUTABLE_SOURCE_RANGE_NOT_RECONSTRUCTED',
            'observation_status': 'SOURCE_RANGE_REVIEWED', 'evidence_class': 'E4',
            'intended_behavior': 'UNAVAILABLE', 'scientific_support': 'UNVALIDATED',
            'original_unit_status': 'SOURCE_SPELLINGS_RETAINED_UNITS_NOT_INFERRED',
            'normalized_expression': None, 'missing_constants': 'NOT_FILLED'}


def audit(path, manifest, prefix, plan):
    """Require every selected review range; inherit bounded full-archive checks."""
    validate_plan(plan)
    by_source = {}
    for row in plan['records']:
        by_source.setdefault(row['entry_id'], []).append(row)
    found = {}

    def observe(item, text, scopes):
        if item['entry_id'] not in by_source:
            return
        if 'retired_scope_candidate' in scopes or 'test_path_candidate' in scopes:
            raise ValueError('review scope requires separate retired/test classification')
        for row in by_source[item['entry_id']]:
            found[row['id']] = resolve(row, item, text)

    parent = inventory.audit(path, manifest, prefix, source_observer=observe)
    if set(found) != {row['id'] for row in plan['records']}:
        raise ValueError('required source not inspected')
    result = {'schema_version': 1, 'archive_sha256': parent['archive_sha256'],
              'intake_manifest_sha256': parent['intake_manifest_sha256'],
              'plan_sha256': hashlib.sha256(json.dumps(plan, sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
              'records': [found[row['id']] for row in plan['records']],
              'selected_ranges_complete': True, 'whole_project_extraction_complete': False,
              'source_reuse': 'PROHIBITED', 'scientific_validation': 'UNVALIDATED',
              'notice': 'REVIEWED_E4_OBSERVATIONS_NOT_INTENT_OR_PHYSICAL_VALIDATION'}
    result['manifest_sha256'] = intake.canonical_digest(result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path); parser.add_argument('intake', type=Path)
    parser.add_argument('plan', type=Path); parser.add_argument('--project-root', required=True)
    args = parser.parse_args()
    import resource
    resource.setrlimit(resource.RLIMIT_AS, (268435456, 268435456))
    resource.setrlimit(resource.RLIMIT_CPU, (120, 120))
    try:
        result = audit(args.archive, strict_json(args.intake.read_bytes()), args.project_root,
                       strict_json(args.plan.read_bytes()))
    except (OSError, ValueError, EOFError, MemoryError, inventory.tarfile.TarError):
        print('INCOMPLETE_PRIVATE_REVIEW', file=sys.stderr); return 1
    print(json.dumps(result, indent=2)); return 0


if __name__ == '__main__': raise SystemExit(main())
