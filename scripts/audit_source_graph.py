#!/usr/bin/env python3
"""Static private source graph: source is parsed as data, never imported/executed."""
import argparse
import ast
import gzip
import hashlib
import json
from pathlib import Path
import re
import tarfile
import time

if __package__:
    from . import inventory_legacy as inventory
else:
    import inventory_legacy as inventory

ROOT=Path(__file__).resolve().parents[1]
POLICY=json.loads((ROOT/'docs/audit/static_graph_policy.json').read_text())


def target_name(node):
    if isinstance(node,ast.Name):return node.id
    if isinstance(node,ast.Attribute):return target_name(node.value)+'.'+node.attr
    return '<dynamic-expression>'


def analyze(text,language):
    """Record observed syntax and source lines; resolution/execution stays unknown.

Python AST edges are syntax, not actual runtime calls. Native call patterns may
also be declarations, macros or casts; explicitly labeled candidates. No behavior
or dependency installation is inferred from a filename, import name or comment.
"""
    out=dict(status='parsed_static',edges=[],definitions=[],entrypoints=[],unknowns=[])
    def edge(kind,target,line):
        out['edges'].append(dict(kind=kind,target=target,line=line,resolution='unresolved_static'))
    if language=='python':
        try:tree=ast.parse(text)
        except (SyntaxError,ValueError,RecursionError,MemoryError):
            out.update(status='unparsed',unknowns=['invalid_or_unsupported_python']);return out
        for node in ast.walk(tree):
            if isinstance(node,ast.Import):
                for name in node.names:edge('import',name.name,node.lineno)
            elif isinstance(node,ast.ImportFrom):
                for name in node.names:edge('import','.'*node.level+(node.module or '')+'.'+name.name,node.lineno)
            elif isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
                out['definitions'].append(dict(name=node.name,line=node.lineno,end_line=node.end_lineno))
            elif isinstance(node,ast.Call):
                target=target_name(node.func)
                edge('call_ast',target,node.lineno)
                if target in ('__import__','importlib.import_module','ctypes.CDLL','ctypes.cdll.LoadLibrary'):
                    edge('dynamic_loading',target,node.lineno)
            elif isinstance(node,ast.If) and isinstance(node.test,ast.Compare):
                test=node.test
                if (isinstance(test.left,ast.Name) and test.left.id=='__name__'
                        and len(test.ops)==1 and isinstance(test.ops[0],ast.Eq)
                        and len(test.comparators)==1 and isinstance(test.comparators[0],ast.Constant)
                        and test.comparators[0].value=='__main__'):
                    out['entrypoints'].append(dict(kind='python_main_guard',line=node.lineno))
        out['unknowns'].append('runtime_paths_dynamic_dispatch_import_availability_unverified')
    elif language=='native':
        # Preserve line counts while removing comments; quoted strings remain
        # intact for includes, then are masked before lexical call detection.
        tokens=r'//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\''
        stripped=re.sub(tokens,lambda m:'\n'*m[0].count('\n') if m[0].startswith(('//','/*')) else m[0],text,flags=re.S)
        for line_no,line in enumerate(stripped.splitlines(),1):
            include=re.match(r'\s*#\s*include\s*[<"]([^>"]+)[>"]',line)
            if include:edge('include',include[1],line_no)
            elif re.match(r'\s*#\s*include\b',line):edge('dynamic_include','<macro>',line_no)
        masked=re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'',lambda m:' '*len(m[0]),stripped)
        for match in re.finditer(r'(?<![\w:])([A-Za-z_]\w*(?:::\w+)*)\s*\(',masked):
            name=match[1]
            if name in ('if','for','while','switch','sizeof','return','catch','alignof','decltype'):continue
            line=masked.count('\n',0,match.start())+1
            edge('lexical_call_candidate',name,line)
            if name in ('dlopen','LoadLibrary','LoadLibraryA','LoadLibraryW'):edge('dynamic_loading',name,line)
        for match in re.finditer(r'\b(?:int|auto)\s+main\s*\([^)]*\)\s*\{',masked):
            out['entrypoints'].append(dict(kind='native_main_candidate',line=masked.count('\n',0,match.start())+1))
        out['unknowns'].append('native_calls_declarations_macros_templates_and_dispatch_not_resolved')
    elif language=='cmake':
        clean=re.sub(r'"(?:\\.|[^"\\])*"|#[^\n]*',lambda m:m[0] if m[0].startswith(chr(34)) else ' '*len(m[0]),text)
        for match in re.finditer(r'\b(find_package|add_subdirectory|target_link_libraries|add_executable|add_library)\s*\(([^)]*)\)',clean,re.I):
            # Store declarative tokens only in private evidence; no configure/build.
            edge('build_declaration',match[1].lower()+':'+match[2].strip(),text.count('\n',0,match.start())+1)
        out['unknowns'].append('cmake_variables_conditionals_and_transitive_dependencies_unresolved')
    else:out.update(status='unsupported',unknowns=['language_not_statically_parsed'])
    out['edges'].sort(key=lambda e:(e['line'],e['kind'],e['target']))
    return out


def audit_archive(path,manifest,policy):
    """Cross-check every selected payload against the accepted S009 manifest.

Output contains private member names/symbols. Caller keeps it restricted. Unknown
coverage is explicit; links, special types and unsafe/ambiguous names are never
selected. Quarantined executable-permission regular text may be statically parsed
as data; secret/binary/nested payloads are excluded, never executed or opened.
"""
    if (not isinstance(policy,dict) or set(policy)!=set(POLICY)
            or any(type(x) is not int or x<=0 for x in policy.values())
            or not isinstance(manifest,dict) or manifest.get('schema_version')!=2
            or manifest.get('complete') is not True or manifest.get('identity_verified') is not True
            or not isinstance(manifest.get('members'),list)
            or not isinstance(manifest.get('archive_sha256'),str)
            or not re.fullmatch(r'[0-9a-f]{64}',manifest['archive_sha256'])
            or not inventory.verify_manifest(manifest)):
        raise ValueError('unverified policy/inventory')
    result=dict(schema_version=1,complete=False,archive_sha256=manifest['archive_sha256'],
                inventory_sha256=manifest['manifest_sha256'],nodes=[],unknowns=[],source_reuse='prohibited',scientific_validation='unvalidated')
    limits=dict(inventory.DEFAULTS);limits['max_seconds']=policy['max_seconds']
    start=time.monotonic();total_edges=0
    unsafe={'unsafe_member_path','duplicate_member_path','case_collision','potential_secret','binary_content','nested_archive'}
    with Path(path).open('rb') as raw:
        if inventory.full_hash(raw,limits,start)!=manifest['archive_sha256']:raise ValueError('baseline changed')
        raw.seek(0)
        with gzip.GzipFile(fileobj=raw) as expanded:
            bounded=inventory.Bounded(expanded,limits,start)
            with tarfile.open(fileobj=bounded,mode='r|') as archive:
                count=0
                for index,member in enumerate(archive):
                    inventory.deadline(limits,start)
                    if index>=len(manifest['members']):raise ValueError('unexpected member')
                    item=manifest['members'][index];count+=1
                    if member.name!=item['path'] or member.size!=item['bytes']:raise ValueError('member metadata mismatch')
                    if not member.isfile() or item['kind']!='file':continue
                    suffix=Path(member.name).suffix.lower()
                    language='python' if suffix=='.py' else 'native' if suffix in ('.c','.cc','.cpp','.h','.hpp') else 'cmake' if Path(member.name).name=='CMakeLists.txt' or suffix=='.cmake' else None
                    if language is None:continue
                    node=dict(entry_id=item['entry_id'],path=item['path'],sha256=item['sha256'],language=language)
                    if unsafe.intersection(item['flags']):node['status']='quarantined_not_parsed'
                    elif member.size>policy['max_source_bytes']:node['status']='source_budget_not_parsed'
                    else:
                        data=archive.extractfile(member).read(policy['max_source_bytes']+1)
                        if hashlib.sha256(data).hexdigest()!=item['sha256']:raise ValueError('source hash mismatch')
                        try:parsed=analyze(data.decode('utf-8'),language)
                        except UnicodeDecodeError:parsed=dict(status='unparsed',unknowns=['non_utf8_source'])
                        node.update(parsed)
                        if len(node.get('edges',[]))>policy['max_edges_per_file']:raise ValueError('edge budget exhausted')
                        total_edges+=len(node.get('edges',[]))
                        if total_edges>policy['max_total_edges']:raise ValueError('total edge budget exhausted')
                    result['nodes'].append(node)
                if count!=len(manifest['members']):raise ValueError('missing members')
            while bounded.read(65536):pass
        if inventory.full_hash(raw,limits,start)!=manifest['archive_sha256']:raise ValueError('baseline changed')
    result['complete']=True
    result['graph_sha256']=inventory.canonical_digest(result)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive',type=Path);parser.add_argument('--inventory',type=Path,required=True)
    parser.add_argument('--policy',type=Path,required=True);parser.add_argument('--expected-manifest-sha256',required=True)
    args=parser.parse_args()
    policy=json.loads(args.policy.read_text())
    import resource
    resource.setrlimit(resource.RLIMIT_AS,(policy['max_memory_bytes'],policy['max_memory_bytes']))
    resource.setrlimit(resource.RLIMIT_CPU,(policy['max_cpu_seconds'],policy['max_cpu_seconds']))
    manifest=json.loads(args.inventory.read_text())
    if manifest['manifest_sha256']!=args.expected_manifest_sha256:parser.exit(1,'FAIL: wrong inventory identity\n')
    try:result=audit_archive(args.archive,manifest,policy)
    except (ValueError,OSError,EOFError,tarfile.TarError,MemoryError):parser.exit(1,'FAIL: incomplete static audit; private diagnostics required\n')
    print(json.dumps(result,sort_keys=True,indent=2))
