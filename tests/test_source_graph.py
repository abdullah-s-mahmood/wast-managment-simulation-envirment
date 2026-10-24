"""Independently authored static-analysis fixtures; no legacy code copied."""
import gzip,hashlib,importlib.util,io,json,tarfile,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('scripts.graph',ROOT/'scripts/audit_source_graph.py')
g=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(g)

class SourceGraphTests(unittest.TestCase):
 def test_python_imports_calls_entrypoints_and_dynamic_loading(self):
  result=g.analyze('import os\nfrom pkg import run\ndef start():\n    run()\n    __import__("optional")\nif __name__ == "__main__":\n    start()\n','python')
  self.assertEqual({e['target'] for e in result['edges'] if e['kind']=='import'},{'os','pkg.run'})
  self.assertTrue(any(e['kind']=='dynamic_loading' for e in result['edges']))
  self.assertEqual(result['definitions'][0]['name'],'start')
  self.assertEqual(result['entrypoints'][0]['line'],6)
 def test_native_includes_comments_and_unknown_call_semantics(self):
  text='/* #include "fiction.h" */\n#include <vector>\nint main() { dispatch(); dlopen("optional"); }\n'
  result=g.analyze(text,'native')
  self.assertEqual([e['target'] for e in result['edges'] if e['kind']=='include'],['vector'])
  self.assertTrue(result['entrypoints'])
  self.assertTrue(all(e['resolution']=='unresolved_static' for e in result['edges']))
 def test_build_declarations_ignore_commented_dependencies(self):
  result=g.analyze('# find_package(Fiction)\nfind_package(Observed)\n','cmake')
  self.assertEqual(len(result['edges']),1)
  self.assertEqual(result['edges'][0]['target'],'find_package:Observed')
 def test_no_behavior_inferred_from_filename_or_invalid_code(self):
  self.assertEqual(g.analyze('# no imports or behavior\n','python')['edges'],[])
  self.assertEqual(g.analyze('def broken(','python')['status'],'unparsed')
  self.assertEqual(g.analyze('opaque','unknown')['status'],'unsupported')
 def test_generated_imports_and_order_preserve_provenance(self):
  for n in range(1,25):
   result=g.analyze('\n'.join(f'import module_{i}' for i in range(n)),'python')
   self.assertEqual(len(result['edges']),n)
   self.assertEqual([e['line'] for e in result['edges']],list(range(1,n+1)))
 def test_archive_hash_links_and_manifest_tampering(self):
  with tempfile.TemporaryDirectory() as directory:
   path=Path(directory)/'a.tar.gz'
   with tarfile.open(path,'w:gz') as archive:
    link=tarfile.TarInfo('root/evil.py');link.type=tarfile.SYMTYPE;link.linkname='/outside';archive.addfile(link)
    data=b'import os\n';member=tarfile.TarInfo('root/plausible_behavior.py');member.size=len(data);archive.addfile(member,io.BytesIO(data))
   manifest=g.inventory.inspect(path,g.inventory.DEFAULTS)
   before=path.read_bytes();result=g.audit_archive(path,manifest,g.POLICY)
   self.assertTrue(result['complete']);self.assertEqual(len(result['nodes']),1)
   self.assertEqual(result['nodes'][0]['sha256'],hashlib.sha256(data).hexdigest())
   self.assertEqual(result['nodes'][0]['edges'][0]['target'],'os')
   self.assertEqual(before,path.read_bytes())
   manifest['members'][1]['sha256']='0'*64
   with self.assertRaises(ValueError):g.audit_archive(path,manifest,g.POLICY)
 def test_audited_python_is_never_executed(self):
  result=g.analyze('__import__("never_load_this_module")\nraise RuntimeError("never run")\n','python')
  self.assertEqual(result['status'],'parsed_static')
  self.assertTrue(any(e['kind']=='dynamic_loading' for e in result['edges']))
 def test_missing_or_malformed_inventory_rejects_before_source_access(self):
  for manifest in (None,{},dict(schema_version=2,complete=True,identity_verified=True)):
   with self.assertRaises(ValueError):g.audit_archive(Path('never-open'),manifest,g.POLICY)
 def test_source_limit_is_explicit_unknown(self):
  policy=dict(g.POLICY);policy['max_source_bytes']=1
  with tempfile.TemporaryDirectory() as directory:
   path=Path(directory)/'a.tar.gz'
   with tarfile.open(path,'w:gz') as archive:
    data=b'import os\n';member=tarfile.TarInfo('a.py');member.size=len(data);archive.addfile(member,io.BytesIO(data))
   result=g.audit_archive(path,g.inventory.inspect(path,g.inventory.DEFAULTS),policy)
   self.assertEqual(result['nodes'][0]['status'],'source_budget_not_parsed')

if __name__=='__main__':unittest.main()
