"""Generated archive properties exercise private quarantine without target access."""
import gzip
import hashlib
import importlib.util
import io
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('inventory_v2', ROOT/'scripts/inventory_legacy.py')
m = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(m)


def make_archive(path, entries):
    """Entries: name, type, payload, link target. Never creates link objects."""
    with tarfile.open(path, 'w:gz') as archive:
        for name, kind, data, target in entries:
            member = tarfile.TarInfo(name)
            member.type, member.linkname = kind, target
            member.size = len(data)
            archive.addfile(member, io.BytesIO(data))


FILE = ('root/good.py', tarfile.REGTYPE, b'identity = 1\n', '')
LINK = ('root/bad', tarfile.SYMTYPE, b'', '../../outside')


class QuarantineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name)/'fixture.tar.gz'

    def scan(self, entries, limits=None):
        make_archive(self.path, entries)
        before = self.path.read_bytes()
        original = tarfile.TarFile.extractfile
        def guarded(archive, member):
            self.assertTrue(member.isfile(), 'target dereference attempted')
            return original(archive, member)
        with patch.object(tarfile.TarFile, 'extractfile', guarded):
            result = m.inspect(self.path, limits or m.DEFAULTS)
        self.assertEqual(before, self.path.read_bytes())
        if len(before) <= (limits or m.DEFAULTS)['max_compressed_bytes']:
            self.assertEqual(result['archive_sha256'], hashlib.sha256(before).hexdigest())
        return result

    def test_links_at_every_position_and_relative_absolute_targets(self):
        for position, target in itertools.product(range(3), ('../../outside','/private/target','neighbor','C:/outside')):
            entries = [(f'root/{i}.py',tarfile.REGTYPE,b'x','') for i in range(2)]
            entries.insert(position, ('root/link',tarfile.SYMTYPE,b'',target))
            with self.subTest(position=position,target=target):
                result = self.scan(entries)
                self.assertTrue(result['complete'])
                self.assertEqual(len(result['members']),3)
                self.assertEqual(result['quarantine_count'],1)
                self.assertEqual(result['members'][position]['link_target'],target)
                self.assertIsNone(result['members'][position]['sha256'])

    def test_generated_quarantine_sequences_preserve_later_files(self):
        attacks = [LINK, ('root/hard',tarfile.LNKTYPE,b'','../../outside'),
                   ('../escape',tarfile.REGTYPE,b'private',''),
                   ('root/device',tarfile.CHRTYPE,b'','')]
        for sequence in itertools.product(range(4), repeat=3):
            entries = [(f'{attacks[i][0]}{j}', *attacks[i][1:]) for j,i in enumerate(sequence)] + [FILE]
            result = self.scan(entries)
            self.assertTrue(result['complete'])
            self.assertEqual(result['quarantine_count'],3)
            self.assertEqual(result['members'][-1]['sha256'],hashlib.sha256(FILE[2]).hexdigest())
            self.assertEqual(result['source_reuse_authorization'],'prohibited')
            self.assertEqual(result['scientific_model_validation'],'unvalidated')
            self.assertTrue(result['security_findings_present'])
            self.assertEqual(result['security_clearance'],'not_granted')

    def test_duplicates_case_collisions_and_manifest_integrity(self):
        result = self.scan([FILE,FILE,('root/GOOD.py',tarfile.REGTYPE,b'x',''),LINK])
        self.assertTrue(result['complete'])
        self.assertEqual(result['quarantine_count'],4)
        self.assertEqual(len({x['entry_id'] for x in result['members']}),4)
        self.assertTrue(m.verify_manifest(result))
        result['members'][0]['bytes'] += 1
        self.assertFalse(m.verify_manifest(result))

    def test_security_findings_are_not_parse_failure_or_clearance(self):
        result = self.scan([('root/tool',tarfile.REGTYPE,b'\x7fELF\0',''),
                            ('root/nested.zip',tarfile.REGTYPE,b'PK\x03\x04',''),FILE])
        self.assertTrue(result['complete'])
        self.assertEqual(result['inventory_status'],'completed')
        self.assertEqual(result['quarantine_count'],2)
        self.assertTrue(result['security_findings_present'])
        clean = self.scan([FILE])
        self.assertEqual(clean['quarantine_count'],0)
        self.assertFalse(clean['security_findings_present'])
        self.assertEqual(clean['security_clearance'],'not_granted')

    def test_truncated_payload_footer_header_and_crc_are_incomplete(self):
        make_archive(self.path,[FILE]);data=self.path.read_bytes()
        for mutation in (data[:-8], data[:-20], data[:10], data[:-8]+bytes([data[-8]^1])+data[-7:], gzip.compress(b'x'*512)):
            self.path.write_bytes(mutation)
            result=m.inspect(self.path,m.DEFAULTS)
            self.assertFalse(result['complete'])
            self.assertEqual(result['inventory_status'],'incomplete')
            self.assertTrue(m.verify_manifest(result))
        make_archive(self.path,[FILE]);raw=gzip.decompress(self.path.read_bytes())
        for mutation in (raw[:1024],raw[:1024]+b'x'*1024,raw[:1024]):
            self.path.write_bytes(gzip.compress(mutation))
            self.assertFalse(m.inspect(self.path,m.DEFAULTS)['complete'])

    def test_resource_exhaustion_identity_mismatch_and_timeout(self):
        for key, bound in [('max_members',1),('max_member_bytes',1),('max_expanded_bytes',512),('max_compressed_bytes',1)]:
            limits=dict(m.DEFAULTS);limits[key]=bound
            result=self.scan([LINK,FILE],limits)
            self.assertFalse(result['complete'])
        make_archive(self.path,[FILE])
        self.assertFalse(m.inspect(self.path,m.DEFAULTS,expected_sha256='0'*64)['complete'])
        self.assertFalse(m.inspect(self.path,m.DEFAULTS,expected_size=1)['complete'])
        with patch.object(m.time,'monotonic',side_effect=itertools.count(step=1000)):
            self.assertFalse(m.inspect(self.path,m.DEFAULTS)['complete'])

    def test_non_utf8_binary_and_split_secret_detection(self):
        data=b'x'*65530+b'-----BEGIN '+b'PRIVATE KEY-----'
        result=self.scan([('root/binary',tarfile.REGTYPE,b'\xff',''),
                          ('root/secret',tarfile.REGTYPE,data,''),FILE])
        self.assertTrue(result['complete'])
        self.assertIn('binary_content',result['members'][0]['flags'])
        self.assertIn('potential_secret',result['members'][1]['flags'])
        self.assertNotIn('PRIVATE KEY',json.dumps(result))

    def test_cli_memory_budget_exhaustion_cannot_report_completion(self):
        make_archive(self.path,[FILE])
        limits=dict(m.DEFAULTS);limits['max_memory_bytes']=1
        policy=Path(self.tmp.name)/'tiny-memory.json';policy.write_text(json.dumps(limits))
        result=subprocess.run([sys.executable,str(ROOT/'scripts/inventory_legacy.py'),str(self.path),'--limits',str(policy)],capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0)
        if result.stdout.strip():
            self.assertFalse(json.loads(result.stdout)['complete'])

    def test_public_cli_completed_with_quarantine(self):
        make_archive(self.path,[LINK,FILE]);before=self.path.read_bytes()
        limits=Path(self.tmp.name)/'limits.json';limits.write_text(json.dumps(m.DEFAULTS))
        result=subprocess.run([sys.executable,str(ROOT/'scripts/inventory_legacy.py'),str(self.path),'--limits',str(limits)],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        manifest=json.loads(result.stdout)
        self.assertTrue(manifest['complete']);self.assertTrue(manifest['security_findings_present'])
        self.assertTrue(m.verify_manifest(manifest));self.assertEqual(before,self.path.read_bytes())
        self.assertEqual(len(list(Path(self.tmp.name).iterdir())),2)


if __name__=='__main__': unittest.main()
