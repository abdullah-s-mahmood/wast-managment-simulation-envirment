#!/usr/bin/env python3
"""Private source-anchored candidate ledger; never evaluate legacy expressions.

Offsets are zero-based UTF-8 bytes, end exclusive; lines are one-based inclusive.
Candidate syntax is deliberately broad, not a semantic completeness guarantee.
No units, missing constants, intention or scientific support are inferred.
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
from scripts import inventory_legacy as intake
from scripts import inventory_test_evidence as inventory
from scripts.validate_baseline_result import strict_json

PATTERNS = {
    'assignment_or_default': r'(?<![=!<>])=(?!=)',
    'return_expression': r'\breturn\s+[^;\s]',
    'distribution': r'\b(?:\w*distribution|random|randint|uniform|normal|bernoulli|exponential)\b',
    'time_rule': r'\b(?:dt|now|time|timestamp|deadline|period|duration)\w*\b',
    'protocol_parameter': r'\b(?:payload|bitrate|bandwidth|packet|rate|latency|loss|robo)\w*\b',
}
TRUST = {'observed': 'STATIC_SOURCE_CANDIDATE', 'intended': 'UNAVAILABLE',
         'scientific_support': 'UNVALIDATED', 'original_units': None,
         'normalized_expression': None, 'missing_constants': 'NOT_FILLED'}


def candidates(item, text, scopes):
    """Produce line anchors and original identifier tokens, not reconstructed code.

A line can contain multiple/multiline expressions; review must resolve exact
    expression boundaries against the immutable archive before acceptance.
    Strings/comments may match. Tags are search hints, never physical evidence.
    """
    data = text.encode('utf-8')
    if hashlib.sha256(data).hexdigest() != item['sha256']:
        raise ValueError('source hash mismatch')
    records = []
    offset = 0
    for number, line in enumerate(text.splitlines(keepends=True), 1):
        raw = line.encode('utf-8')
        tags = sorted(key for key, pattern in PATTERNS.items() if re.search(pattern, line, re.I))
        if tags:
            records.append({
                'id': f"{item['entry_id']}:L{number}", 'entry_id': item['entry_id'],
                'source_sha256': item['sha256'], 'line_start': number, 'line_end': number,
                'byte_start': offset, 'byte_end': offset + len(raw),
                'span_sha256': hashlib.sha256(raw).hexdigest(),
                'original_names': sorted(set(re.findall(r'\b[A-Za-z_]\w*\b', line))),
                'tags': tags, 'scopes': sorted(scopes), 'review': 'PENDING', **TRUST,
            })
        offset += len(raw)
    return records


def verify_record(record, item, data):
    """Reject guessed values, changed source/anchors and unsupported trust upgrades.

This verifies provenance and conservative labels, not equation correctness or
    physical validity. A future reviewed ledger requires a separate contract.
    """
    if not isinstance(record, dict) or any(record.get(k) != v for k, v in TRUST.items()):
        raise ValueError('unsupported inference or trust promotion')
    if (record.get('review') != 'PENDING' or record.get('entry_id') != item['entry_id']
            or record.get('source_sha256') != item['sha256']
            or hashlib.sha256(data).hexdigest() != item['sha256']):
        raise ValueError('source binding mismatch')
    if any(type(record.get(k)) is not int for k in ('line_start', 'line_end', 'byte_start', 'byte_end')):
        raise ValueError('integer anchor required')
    expected = candidates(item, data.decode('utf-8'), set(record.get('scopes', [])))
    if record not in expected:
        raise ValueError('candidate anchor or metadata mismatch')
    return True


def audit(path, manifest, prefix):
    """Reuse accepted bounded intake traversal; retain no source payload copies."""
    records = []
    sources = []

    def observe(item, text, scopes):
        if 'retired_scope_candidate' in scopes:
            return
        found = candidates(item, text, scopes)
        records.extend(found)
        sources.append({'entry_id': item['entry_id'], 'source_sha256': item['sha256'],
                        'bytes': item['bytes'], 'candidate_lines': len(found),
                        'scopes': sorted(scopes)})

    parent = inventory.audit(path, manifest, prefix, source_observer=observe)
    result = {'schema_version': 1, 'archive_sha256': parent['archive_sha256'],
              'intake_manifest_sha256': parent['intake_manifest_sha256'],
              'traversal_complete': parent['inventory_complete'],
              'semantic_extraction_complete': False, 'review_complete': False,
              'source_reuse': 'PROHIBITED', 'scientific_validation': 'UNVALIDATED',
              'source_bytes_inspected': sum(x['bytes'] for x in sources),
              'sources': sources, 'records': records,
              'coverage': 'ACTIVE_PATH_SOURCE_CANDIDATES_ONLY; RETIRED_METADATA_IN_S013',
              'limitations': ['Lexical hints can miss indirect/multiline expressions.',
                              'Names preserve original spelling, not resolved variable identity.',
                              'Original units unresolved; no normalization or constant imputation.',
                              'Tests/build/tool scripts distinguished by scopes, not model evidence.']}
    result['manifest_sha256'] = intake.canonical_digest(result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('intake', type=Path)
    parser.add_argument('--project-root', required=True)
    args = parser.parse_args()
    import resource
    resource.setrlimit(resource.RLIMIT_AS, (268435456, 268435456))
    resource.setrlimit(resource.RLIMIT_CPU, (120, 120))
    try:
        result = audit(args.archive, strict_json(args.intake.read_bytes()), args.project_root)
    except (OSError, ValueError, EOFError, MemoryError, inventory.tarfile.TarError):
        print('INCOMPLETE_PRIVATE_EXTRACTION', file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
