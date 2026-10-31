#!/usr/bin/env python3
"""Classify active source context and index Python expressions as private data.

AST parsing is not execution, physical validation or proof of semantic coverage.
Expressions retain original UTF-8 byte ranges; no unparse/eval/import is used.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts import inventory_test_evidence as inventory
from scripts import inventory_legacy as intake
from scripts.review_model_spans import validate_plan
from scripts.validate_baseline_result import strict_json


def context(path, prefix, scopes):
    """Path context is a scope hint, not authorship, validity or absence of models."""
    relative = PurePosixPath(path).relative_to(PurePosixPath(prefix))
    parts = relative.parts
    if 'test_path_candidate' in scopes: return 'test_fixture_or_probe'
    if relative.name == 'CMakeLists.txt': return 'build_registration'
    if relative.suffix in ('.sh', '.bash'): return 'shell_orchestration'
    if parts[0] == 'include': return 'native_interface_or_inline_behavior'
    if parts[0] == 'src': return 'native_runtime_or_tool'
    if parts[0] == 'rl': return 'training_or_export'
    if parts[0] == 'experiments': return 'experiment_or_analysis'
    return 'auxiliary_tool_or_scenario'


def python_expressions(text, source):
    """Extract syntactic assignments/defaults/returns/guards without evaluation.

Python AST columns count UTF-8 bytes. Source offsets retain CRLF/CR spelling;
Unicode line separators inside strings are not physical Python newlines.
Calls, aliases, external files and imported definitions remain unresolved.
    """
    data = text.encode('utf-8')
    if hashlib.sha256(data).hexdigest() != source['sha256']:
        raise ValueError('source identity mismatch')
    tree = ast.parse(text)
    starts = [0] + [m.end() for m in re.finditer(rb'\r\n|\r|\n', data)]
    selected = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.NamedExpr)) and node.value is not None:
            selected.append(('assignment_value', node.value))
        elif isinstance(node, ast.AugAssign): selected.append(('augmented_assignment', node))
        elif isinstance(node, ast.Return) and node.value is not None: selected.append(('return_value', node.value))
        elif isinstance(node, (ast.If, ast.While, ast.Assert)): selected.append(('guard', node.test))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            selected.extend(('parameter_default', x) for x in node.args.defaults)
            selected.extend(('parameter_default', x) for x in node.args.kw_defaults if x is not None)
        elif isinstance(node, ast.Call):
            selected.append(('call_expression', node))
            # Keyword spelling is observed; aliases/positional defaults unresolved.
            selected.extend(('keyword_default', x.value) for x in node.keywords if x.arg == 'default')
    if len(selected) > 10000: raise ValueError('expression count budget')
    records = []
    for role, node in selected:
        start = starts[node.lineno - 1] + node.col_offset
        end = starts[node.end_lineno - 1] + node.end_col_offset
        if not 0 <= start < end <= len(data): raise ValueError('AST coordinate mismatch')
        span = data[start:end]
        spelling = span.decode('utf-8')
        records.append({'entry_id': source['entry_id'], 'source_sha256': source['sha256'],
                        'line_start': node.lineno, 'line_end': node.end_lineno,
                        'byte_start': start, 'byte_end': end, 'span_sha256': hashlib.sha256(span).hexdigest(),
                        'syntax_role': role, 'ast_type': type(node).__name__,
                        'original_names': sorted(set(re.findall(r'\b[^\W\d]\w*\b', spelling))),
                        'observed': 'STATIC_EXPRESSION_NOT_EXECUTED', 'evidence_class': 'E4',
                        'intended_behavior': 'UNAVAILABLE', 'scientific_support': 'UNVALIDATED',
                        'original_units': 'SOURCE_RANGE_RETAINED_NOT_INFERRED',
                        'normalization': None, 'missing_constants': 'NOT_FILLED'})
    records.sort(key=lambda x: (x['byte_start'], x['byte_end'], x['syntax_role']))
    for i, row in enumerate(records): row['id'] = f"{source['entry_id']}:AST{i:05d}"
    return records


def audit(path, manifest, prefix, plan):
    """Inherit full archive integrity/budgets; classify every inspected active file."""
    validate_plan(plan)
    reviewed = {x['entry_id'] for x in plan['records']}
    files = []; expressions = []

    def observe(item, text, scopes):
        if 'retired_scope_candidate' in scopes: return
        role = context(item['path'], prefix, scopes)
        row = {'entry_id': item['entry_id'], 'source_sha256': item['sha256'],
               'context': role, 'selected_review_ranges': item['entry_id'] in reviewed,
               'python_status': 'not_python', 'expression_count': 0}
        if PurePosixPath(item['path']).suffix == '.py' and role != 'test_fixture_or_probe':
            records = python_expressions(text, item)
            if len(expressions) + len(records) > 20000: raise ValueError('total expression budget')
            expressions.extend(records)
            row.update(python_status='parsed_as_data', expression_count=len(records))
        elif role == 'test_fixture_or_probe': row['python_status'] = 'test_evidence_in_S013_not_model_definition'
        files.append(row)

    parent = inventory.audit(path, manifest, prefix, source_observer=observe)
    result = {'schema_version': 1, 'archive_sha256': parent['archive_sha256'],
              'intake_manifest_sha256': parent['intake_manifest_sha256'],
              'review_plan_sha256': intake.canonical_digest(plan),
              'files': files, 'expressions': expressions, 'traversal_complete': True,
              'scientific_validation': 'UNVALIDATED', 'source_reuse': 'PROHIBITED',
              'limitations': ['Path contexts are hints, not semantic absence-of-model proofs.',
                              'AST calls/aliases/imports/external inputs are unresolved.',
                              'Test assertions are inventoried in S013, not physical model definitions.',
                              'Native/shell behavior still requires reviewed ranges or candidate index.',
                              'Retired context remains indexed in S009/S013, not silently current.']}
    result['manifest_sha256'] = intake.canonical_digest(result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path); parser.add_argument('intake', type=Path)
    parser.add_argument('plan', type=Path); parser.add_argument('--project-root', required=True)
    args = parser.parse_args()
    import resource
    resource.setrlimit(resource.RLIMIT_AS, (268435456, 268435456)); resource.setrlimit(resource.RLIMIT_CPU, (120, 120))
    try:
        result = audit(args.archive, strict_json(args.intake.read_bytes()), args.project_root,
                       strict_json(args.plan.read_bytes()))
    except (OSError, ValueError, SyntaxError, RecursionError, EOFError, MemoryError, inventory.tarfile.TarError):
        print('INCOMPLETE_PRIVATE_AUXILIARY_AUDIT', file=sys.stderr); return 1
    print(json.dumps(result, indent=2)); return 0


if __name__ == '__main__': raise SystemExit(main())
