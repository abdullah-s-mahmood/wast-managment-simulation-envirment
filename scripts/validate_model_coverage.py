#!/usr/bin/env python3
"""Cross-check S014 static extraction coverage, never physical model validity."""
import argparse
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
from scripts import inventory_legacy as intake
from scripts.review_model_spans import validate_plan
from scripts.validate_baseline_result import strict_json


def validate(candidate, auxiliary, reviewed, plan):
    """Require consistent source IDs/hashes and explicit evidence for every scope.

Completion means bounded active-path extraction coverage, not whole-archive
semantic analysis, source reuse, scientific validity or resolved dynamic calls.
    """
    validate_plan(plan)
    for value in (candidate, auxiliary, reviewed):
        if (not isinstance(value, dict) or not intake.verify_manifest(value)
                or value.get('schema_version') != 1 or type(value.get('schema_version')) is not int
                or value.get('source_reuse') != 'PROHIBITED'
                or value.get('scientific_validation') != 'UNVALIDATED'):
            raise ValueError('invalid extraction artifact')
    if (candidate.get('traversal_complete') is not True or auxiliary.get('traversal_complete') is not True
            or reviewed.get('selected_ranges_complete') is not True): raise ValueError('incomplete traversal/review')
    for key in ('archive_sha256', 'intake_manifest_sha256'):
        if len({x[key] for x in (candidate, auxiliary, reviewed)}) != 1: raise ValueError('identity disagreement')
    digest = intake.canonical_digest(plan)
    if auxiliary.get('review_plan_sha256') != digest or reviewed.get('plan_sha256') != digest:
        raise ValueError('plan disagreement')
    def unique(rows, key):
        result = {r[key]: r for r in rows}
        if len(result) != len(rows): raise ValueError('duplicate identity')
        return result
    sources = unique(candidate['sources'], 'entry_id')
    contexts = unique(auxiliary['files'], 'entry_id')
    ranges = unique(reviewed['records'], 'id')
    if set(sources) != set(contexts) or set(ranges) != {r['id'] for r in plan['records']}:
        raise ValueError('missing source/range coverage')
    selected = set()
    for row in plan['records']:
        actual = ranges[row['id']]
        if any(actual.get(k) != v for k, v in row.items()): raise ValueError('review metadata disagreement')
        if (actual.get('scientific_support') != 'UNVALIDATED' or actual.get('normalized_expression') is not None
                or actual.get('missing_constants') != 'NOT_FILLED'): raise ValueError('unsupported inference')
        if row['entry_id'] not in sources or sources[row['entry_id']]['source_sha256'] != row['source_sha256']:
            raise ValueError('unbound review source')
        selected.add(row['entry_id'])
    excluded = 0; parsed = 0
    for eid, source in sources.items():
        actual = contexts[eid]
        if source['source_sha256'] != actual['source_sha256']: raise ValueError('source hash disagreement')
        test = 'test_path_candidate' in source['scopes']
        if test != (actual['context'] == 'test_fixture_or_probe'): raise ValueError('test scope substitution')
        if test: excluded += 1; continue
        if actual['python_status'] == 'parsed_as_data': parsed += 1
        elif eid not in selected: raise ValueError('uncovered native/shell/build source')
    for expression in auxiliary['expressions']:
        source = contexts.get(expression['entry_id'])
        if (not source or source['python_status'] != 'parsed_as_data'
                or expression['source_sha256'] != source['source_sha256']
                or expression['scientific_support'] != 'UNVALIDATED'
                or expression['normalization'] is not None): raise ValueError('unbound expression/inference')
    return {'schema_version': 1, 'scope': 'BOUNDED_ACTIVE_PATH_STATIC_EXTRACTION',
            'source_files': len(sources), 'test_evidence_files_in_S013': excluded,
            'python_files_parsed': parsed, 'reviewed_source_ranges': len(ranges),
            'static_python_expressions': len(auxiliary['expressions']), 'scope_coverage_complete': True,
            'scientific_validation': 'UNVALIDATED', 'source_reuse': 'PROHIBITED',
            'whole_archive_semantic_analysis': False, 'dynamic_call_resolution': 'UNAVAILABLE'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('candidate', 'auxiliary', 'reviewed', 'plan'): parser.add_argument(name, type=Path)
    args = parser.parse_args()
    try: result = validate(*(strict_json(getattr(args, key).read_bytes()) for key in ('candidate','auxiliary','reviewed','plan')))
    except (OSError, ValueError, KeyError, TypeError, MemoryError):
        print('INCOMPLETE_MODEL_EXTRACTION_COVERAGE', file=sys.stderr); return 1
    print(json.dumps(result, indent=2)); return 0


if __name__ == '__main__': raise SystemExit(main())
