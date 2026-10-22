"""Synthetic archives only: no legacy content or real credential fixtures."""
import gzip,hashlib,importlib.util,io,json,subprocess,sys,tarfile,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
S=importlib.util.spec_from_file_location('inventory',ROOT/'scripts/inventory_legacy.py')
m=importlib.util.module_from_spec(S);S.loader.exec_module(m)

class InventoryTests(unittest.TestCase):
 def scan(self,entries,limits=None):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'a.tar.gz'
   with tarfile.open(p,'w:gz') as t:
    for name,data,kind in entries:
     info=tarfile.TarInfo(name);info.size=len(data)
     if kind: info.type=kind;info.linkname='../outside'
     t.addfile(info,io.BytesIO(data))
   before=p.read_bytes();result=m.inspect(p,limits or m.DEFAULTS)
   self.assertEqual(before,p.read_bytes());return result
 def test_hashes_roles_and_replay(self):
  entries=[('src/a.py',b'print(1)',None),('include/a.h',b'// header',None),('tests/a.py',b'assert 1',None),('results/a.csv',b'a,b',None),('vendor/a.py',b'x',None),('cache/a.txt',b'x',None),('a.json',b'{}',None),('data/a.csv',b'x',None)]
  a=self.scan(entries);b=self.scan(entries)
  self.assertTrue(a['complete']);self.assertFalse(a['findings'])
  self.assertEqual(a['members'],b['members'])
  self.assertEqual({x['role'] for x in a['members']},{'source','header','test','generated_output','dependency','cache','configuration','dataset'})
  self.assertEqual(a['members'][0]['sha256'],hashlib.sha256(b'print(1)').hexdigest())
 def test_path_link_duplicate_and_case_collisions(self):
  for name in ('../x','/x','C:/x','a\\x','a/../x'):
   self.assertTrue(self.scan([(name,b'x',None)])['findings'])
  for kind in (tarfile.SYMTYPE,tarfile.LNKTYPE,tarfile.FIFOTYPE):
   self.assertTrue(self.scan([('x',b'',kind)])['findings'])
  for names in (('a','a'),('A','a')):
   self.assertTrue(self.scan([(x,b'x',None) for x in names])['findings'])
 def test_secrets_executables_and_nested_archive(self):
  for data in (b'\x7fELF\x00',b'-----BEGIN '+b'PRIVATE KEY-----',b'gh'+b'p_'+b'x'*36,b'PK\x03\x04'):
   result=self.scan([('a.dat',data,None)])
   self.assertTrue(result['findings']);self.assertNotIn(data.decode('latin1'),str(result))
 def test_limits_and_corruption(self):
  for key,value in (('max_members',1),('max_member_bytes',1),('max_expanded_bytes',512)):
   limits=dict(m.DEFAULTS);limits[key]=value
   r=self.scan([('a',b'abc',None),('b',b'abc',None)],limits)
   self.assertFalse(r['complete']);self.assertTrue(r['findings'])
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'a';p.write_bytes(b'broken')
   self.assertFalse(m.inspect(p,m.DEFAULTS)['complete'])
 def test_cli_corruption_fails_without_extraction(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"broken";p.write_bytes(b"broken");limits=Path(d)/"limits.json";limits.write_text(json.dumps(m.DEFAULTS))
   r=subprocess.run([sys.executable,str(ROOT/"scripts/inventory_legacy.py"),str(p),"--limits",str(limits)],capture_output=True,text=True)
   self.assertEqual(r.returncode,1);self.assertFalse(json.loads(r.stdout)["complete"]);self.assertEqual(len(list(Path(d).iterdir())),2)
 def test_invalid_limits(self):
  with self.assertRaises(ValueError):m.inspect(Path('missing'),{})

if __name__=='__main__':unittest.main()
