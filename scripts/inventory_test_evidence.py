#!/usr/bin/env python3
"""Read-only private S013 test/result inventory. Never execute/import legacy code.

Path roles are candidate hints only. Assertion syntax is not a passing test;
historical artifact claims never become scientific validation or fresh replay.
Raw paths/field names and this manifest are private. Publish sanitized counts only.
"""
import argparse
import ast
import csv
import gzip
import hashlib
import io
import json
import os
from pathlib import Path,PurePosixPath
import re
import sys
import tarfile
import time
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from scripts import inventory_legacy as intake
from scripts.validate_baseline_result import strict_json

TEXT_BYTES=1048576
SOURCE_TOTAL=8388608
RESULT_TOTAL=16777216
RESULT_SUFFIXES={'.json','.jsonl','.csv','.log','.txt','.md','.out','.png','.jpg','.jpeg','.pdf','.svg','.html'}
RESULT_PARTS={'results','outputs','output','runs','reports','campaigns','evidence','artifacts'}
UNSAFE={'unsafe_member_path','duplicate_member_path','case_collision','potential_secret','binary_content','nested_archive'}


def categories(name,prefix):
    """Return conservative candidate scopes; never infer provenance from a path."""
    try:path=PurePosixPath(name).relative_to(PurePosixPath(prefix))
    except ValueError:return set()
    parts=[x.lower() for x in path.parts];suffix=path.suffix.lower();out=set()
    retired=bool(parts and parts[0] in ('archive','retired','historical'))
    build=any(x in ('cmakefiles','build','builds','__pycache__','.git') or x.startswith(('cmake-build','build_','build-')) for x in parts)
    vendor=any(x in ('.deps','.venv','venv','vendor','third_party','node_modules','site-packages') for x in parts)
    if build:out.add('build_artifact')
    elif vendor:out.add('vendored_candidate')
    else:
        if suffix in ('.py','.cpp','.cc','.c','.hpp','.h','.sh','.bash') or path.name=='CMakeLists.txt':out.add('project_source')
        if any(x in ('tests','test') for x in parts):out.add('test_path_candidate')
        if set(parts)&RESULT_PARTS:out.add('historical_result_candidate')
        if suffix in ('.json','.xml','.csv','.yaml','.yml') and any(x in ('fixtures','fixture') for x in parts):out.add('fixture_path_candidate')
    if retired and out:out.add('retired_scope_candidate')
    return out


def test_syntax(text,suffix):
    """Classify syntax evidence, not runtime semantics/coverage/success.

Execution-only checks are counted separately from nontrivial behavioral assertion
candidates. Native macro counting is lexical and may include unresolved macros;
Python assert expressions are parsed as AST data with no import/eval/exec.
"""
    out={'parse_status':'parsed_static','assertion_lines':[],'status_check_lines':[],
         'trivial_assertion_lines':[],'test_definition_lines':[],'execution_call_lines':[],
         'fixture_literal_lines':[],'test_registration_lines':[],'test_runner_reference_lines':[],'classification':'no_assertion_observed','runtime_status':'NOT_RUN'}
    if suffix=='.py':
        try:tree=ast.parse(text)
        except (SyntaxError,ValueError,RecursionError,MemoryError):
            out.update(parse_status='unparsed',classification='unknown');return out
        def dotted(node):
            if isinstance(node,ast.Name):return node.id
            if isinstance(node,ast.Attribute):return dotted(node.value)+'.'+node.attr
            return '<dynamic>'
        for node in ast.walk(tree):
            if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)) and node.name.startswith('test_'):
                out['test_definition_lines'].append(node.lineno)
            elif isinstance(node,ast.Assert):
                attrs={x.attr for x in ast.walk(node.test) if isinstance(x,ast.Attribute)}
                if 'returncode' in attrs:
                    out['status_check_lines'].append(node.lineno)
                    direct=(isinstance(node.test,ast.Compare) and isinstance(node.test.left,ast.Attribute)
                            and node.test.left.attr=='returncode' and len(node.test.ops)==1
                            and all(isinstance(x,ast.Constant) for x in node.test.comparators))
                    if not direct:out['assertion_lines'].append(node.lineno)
                else:
                    key='trivial_assertion_lines' if isinstance(node.test,ast.Constant) else 'assertion_lines'
                    out[key].append(node.lineno)
            elif isinstance(node,ast.Call):
                target=dotted(node.func);last=target.rsplit('.',1)[-1]
                if target.startswith('subprocess.'):
                    out['execution_call_lines'].append(node.lineno)
                    if last in ('check_call','check_output') or any(k.arg=='check' and isinstance(k.value,ast.Constant) and k.value.value is True for k in node.keywords):
                        out['status_check_lines'].append(node.lineno)
                if last.startswith('assert') or target in ('pytest.raises','unittest.TestCase.assertRaises'):
                    out['assertion_lines'].append(node.lineno)
                if last=='check_returncode':out['status_check_lines'].append(node.lineno)
            elif isinstance(node,ast.Constant) and isinstance(node.value,str) and node.value.lower().endswith(('.json','.xml','.csv','.yaml','.yml')):
                out['fixture_literal_lines'].append(node.lineno)
    elif suffix in ('.sh','.bash'):
        out['parse_status']='shell_lexical_only'
        out['classification']='shell_semantics_unresolved'
        out['test_runner_reference_lines']=[i for i,line in enumerate(text.splitlines(),1) if not line.lstrip().startswith('#') and re.search(r'\b(ctest|pytest|unittest)\b',line)]
        return out
    elif suffix=='.cmake':
        clean=re.sub(r'"(?:\\.|[^"\\])*"|#[^\n]*',lambda m:'\n'*m[0].count('\n'),text)
        out['test_registration_lines']=[clean.count('\n',0,m.start())+1 for m in re.finditer(r'\badd_test\s*\(',clean,re.I)]
        out['classification']='declared_test_registration_unexecuted'
        return out
    elif suffix in ('.cpp','.cc','.c','.hpp','.h'):
        tokens=r'//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\''
        masked=re.sub(tokens,lambda m:'\n'*m[0].count('\n')+' '*(len(m[0])-m[0].count('\n')),text,flags=re.S)
        for match in re.finditer(r'\b(TEST_CASE|TEST_F|TEST|CHECK|CHECK_FALSE|REQUIRE|REQUIRE_FALSE|REQUIRE_THROWS|REQUIRE_NOTHROW|assert)\s*\(',masked):
            line=masked.count('\n',0,match.start())+1
            out['test_definition_lines' if match[1] in ('TEST_CASE','TEST_F','TEST') else 'assertion_lines'].append(line)
    else:out.update(parse_status='not_source',classification='not_source');return out
    for key in out:
        if key.endswith('_lines'):out[key]=sorted(set(out[key]))
    if out['assertion_lines']:out['classification']='behavioral_assertion_syntax_unexecuted'
    elif out['status_check_lines']:out['classification']='execution_status_only_unexecuted'
    elif out['execution_call_lines']:out['classification']='unchecked_execution_only_unexecuted'
    elif out['trivial_assertion_lines']:out['classification']='trivial_assertion_only'
    return out


def result_syntax(text,suffix):
    """Trust labels ignore self-reported passed/validated/reproduced claims.

Unreproduced means syntactically complete run-provenance fields are present, not
that those fields are authenticated. Otherwise historical evidence is unverifiable.
This inventory can never grant reproduced status or scientific validation.
"""
    out={'result_state':'unverifiable','scientific_validation':'UNVALIDATED','parse_status':'not_machine_provenance',
         'metric_fields':[],'field_units':'UNVERIFIED','fresh_comparison':'NOT_RUN'}
    try:
        if suffix=='.json':
            data=strict_json(text)
            if not isinstance(data,dict):return out
            out['parse_status']='json_object_static'
            out['metric_fields']=sorted(str(k)[:256] for k in data)[:256]
            required=('source_sha256','config_sha256','dependency_manifest_sha256')
            if (all(isinstance(data.get(k),str) and re.fullmatch('[0-9a-f]{64}',data[k]) for k in required)
                    and type(data.get('seed')) is int and isinstance(data.get('command'),list)
                    and data['command'] and all(isinstance(x,str) for x in data['command'])):
                out['result_state']='unreproduced'
        elif suffix=='.csv':
            row=next(csv.reader(io.StringIO(text)),[])
            out['metric_fields']=[x[:256] for x in row[:256]];out['parse_status']='csv_header_only'
        elif suffix=='.jsonl':out['parse_status']='jsonl_not_run_provenance'
    except (ValueError,csv.Error,RecursionError):out['parse_status']='unparsed_or_corrupt'
    return out


def audit(path,manifest,prefix,source_observer=None):
    """Inventory candidates and bounded text; caller must enforce process limits.

The Linux CLI supplies address-space/CPU limits. Unknown coverage is retained.
    Optional trusted source_observer receives hash-verified UTF-8 data only; it
    must not execute source. Exceptions abort before a completed artifact exists.
"""
    if (not intake.verify_manifest(manifest) or type(manifest.get('schema_version')) is not int
            or manifest['schema_version']!=2 or manifest.get('complete') is not True
            or manifest.get('identity_verified') is not True or not isinstance(manifest.get('members'),list)
            or type(manifest.get('compressed_bytes')) is not int
            or not isinstance(manifest.get('archive_sha256'),str)
            or not re.fullmatch('[0-9a-f]{64}',manifest['archive_sha256'])):
        raise ValueError('unverified intake')
    for index,item in enumerate(manifest['members']):
        if (not isinstance(item,dict) or item.get('entry_id')!=f'entry-{index:08d}'
                or not isinstance(item.get('path'),str) or type(item.get('bytes')) is not int
                or item['bytes']<0 or item.get('kind') not in ('file','directory','symlink','hardlink','special')
                or not isinstance(item.get('flags'),list) or not all(isinstance(x,str) for x in item['flags'])):
            raise ValueError('invalid intake member')
    limits=dict(intake.DEFAULTS);start=time.monotonic();records=[];used_source=0;used_result=0
    if not any(PurePosixPath(x['path']).is_relative_to(PurePosixPath(prefix)) for x in manifest['members']):
        raise ValueError('project prefix not present')
    with Path(path).open('rb') as raw:
        stamp_before=os.fstat(raw.fileno())
        if stamp_before.st_size>limits['max_compressed_bytes'] or stamp_before.st_size!=manifest['compressed_bytes']:
            raise ValueError('compressed size budget/identity')
        if intake.full_hash(raw,limits,start)!=manifest['archive_sha256']:raise ValueError('archive identity mismatch')
        raw.seek(0)
        class GuardedInfo(tarfile.TarInfo):
            def _proc_pax(self,archive):
                if self.size>limits['max_metadata_bytes']:raise ValueError('metadata budget')
                return super()._proc_pax(archive)
            def _proc_gnulong(self,archive):
                if self.size>limits['max_metadata_bytes']:raise ValueError('metadata budget')
                return super()._proc_gnulong(archive)
            def _proc_sparse(self,archive):raise ValueError('sparse unsupported')
        with gzip.GzipFile(fileobj=raw) as expanded:
            bounded=intake.Bounded(expanded,limits,start)
            with tarfile.open(fileobj=bounded,mode='r|',tarinfo=GuardedInfo) as archive:
                count=0
                for index,member in enumerate(archive):
                    intake.deadline(limits,start)
                    if index>=limits['max_members'] or member.size>limits['max_member_bytes'] or member.issparse():
                        raise ValueError('member budget or sparse encoding')
                    if index>=len(manifest['members']):raise ValueError('extra member')
                    item=manifest['members'][index];count+=1
                    if member.name!=item['path'] or member.size!=item['bytes']:raise ValueError('member mismatch')
                    scope=categories(item['path'],prefix)
                    if not scope or item['kind']=='directory':continue
                    record={'entry_id':item['entry_id'],'path':item['path'],'sha256':item['sha256'],
                            'kind':item['kind'],'scopes':sorted(scope),'content_status':'not_selected',
                            'scientific_validation':'UNVALIDATED'}
                    if 'historical_result_candidate' in scope:record.update(result_state='unverifiable',fresh_comparison='NOT_RUN')
                    records.append(record)
                    relevant=scope&{'project_source','historical_result_candidate','fixture_path_candidate','test_path_candidate'}
                    if not relevant:continue
                    if 'retired_scope_candidate' in scope and 'test_path_candidate' not in scope:
                        record['content_status']='retired_context_metadata_only';continue
                    if not member.isfile() or UNSAFE.intersection(item['flags']):record['content_status']='quarantined_not_read';continue
                    if member.size>TEXT_BYTES:record['content_status']='member_text_budget_not_read';continue
                    source='project_source' in scope
                    if (source and used_source+member.size>SOURCE_TOTAL) or (not source and used_result+member.size>RESULT_TOTAL):
                        record['content_status']='cumulative_text_budget_not_read';continue
                    data=archive.extractfile(member).read(TEXT_BYTES+1)
                    if len(data)!=member.size or hashlib.sha256(data).hexdigest()!=item['sha256']:raise ValueError('payload hash mismatch')
                    if source:used_source+=len(data)
                    else:used_result+=len(data)
                    try:text=data.decode('utf-8')
                    except UnicodeError:record['content_status']='non_utf8_not_parsed';continue
                    record['content_status']='hash_verified_text'
                    suffix=PurePosixPath(member.name).suffix.lower()
                    if source:
                        record['test_syntax']=test_syntax(text,'.cmake' if PurePosixPath(member.name).name=='CMakeLists.txt' else suffix)
                        if source_observer is not None:source_observer(item,text,scope)
                    if 'historical_result_candidate' in scope:record.update(result_syntax(text,suffix))
                end=archive.offset
                if any(bounded.suffix_at(end)):raise ValueError('nonzero tar trailer')
            while True:
                chunk=bounded.read(65536)
                if not chunk:break
                if any(chunk):raise ValueError('nonzero tar trailer')
            if bounded.count<end+1024:raise ValueError('missing tar terminator')
            if count!=len(manifest['members']):raise ValueError('missing member')
        if intake.full_hash(raw,limits,start)!=manifest['archive_sha256']:raise ValueError('archive changed')
        stamp=lambda s:(s.st_size,s.st_mtime_ns,s.st_ino,s.st_dev)
        if stamp(stamp_before)!=stamp(os.fstat(raw.fileno())) or stamp(stamp_before)!=stamp(Path(path).stat()):raise ValueError('archive changed')
    result={'schema_version':1,'inventory_complete':True,'archive_sha256':manifest['archive_sha256'],
            'intake_manifest_sha256':manifest['manifest_sha256'],'records':records,
            'source_text_bytes':used_source,'result_text_bytes':used_result,
            'notice':'CANDIDATES_AND_STATIC_SYNTAX_ONLY_NOT_EXECUTION_OR_SCIENTIFIC_VALIDATION',
            'source_reuse':'PROHIBITED','scientific_validation':'UNVALIDATED'}
    result['manifest_sha256']=intake.canonical_digest(result)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive',type=Path);parser.add_argument('intake',type=Path);parser.add_argument('--project-root',required=True)
    args=parser.parse_args()
    import resource
    resource.setrlimit(resource.RLIMIT_AS,(268435456,268435456));resource.setrlimit(resource.RLIMIT_CPU,(120,120))
    try:result=audit(args.archive,strict_json(args.intake.read_bytes()),args.project_root)
    except (OSError,ValueError,tarfile.TarError,EOFError,MemoryError):
        print('INCOMPLETE_PRIVATE_INVENTORY',file=sys.stderr);return 1
    print(json.dumps(result,indent=2));return 0


if __name__=='__main__':raise SystemExit(main())
