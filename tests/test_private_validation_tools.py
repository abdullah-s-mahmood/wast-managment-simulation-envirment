"""Synthetic archive/wrapper tests; no owner archive or legacy target is accessed."""
import copy
import hashlib
import io
import json
import os
from pathlib import Path
import tarfile
import tempfile
import unittest
from scripts import inventory_legacy as inventory
from scripts import prepare_validation_copy as prep
from scripts import private_validation_commands as commands


class PrivateValidationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.arc=self.root/'fixture.tar.gz'
        with tarfile.open(self.arc,'w:gz') as arc:
            link=tarfile.TarInfo('badlink');link.type=tarfile.SYMTYPE;link.linkname='/outside';arc.addfile(link)
            for name,data in [('src/a.cpp',b'// synthetic\n'),('city.json',b'{}')]:
                info=tarfile.TarInfo(name);info.size=len(data);arc.addfile(info,io.BytesIO(data))
        self.limits=dict(inventory.DEFAULTS)
        self.manifest=inventory.inspect(self.arc,self.limits)
        self.assertTrue(self.manifest['complete'])
        self.dest={'entry-00000001':'source/a.cpp','entry-00000002':'inputs/city.json'}

    def test_verified_exact_copy_and_archive_immutability(self):
        before=self.arc.read_bytes();m=copy.deepcopy(self.manifest)
        result=prep.prepare(self.arc,m,self.dest,self.root/'copy',self.limits)
        self.assertEqual((self.root/'copy/source/a.cpp').read_bytes(),b'// synthetic\n')
        self.assertEqual(result['entry-00000002']['sha256'],hashlib.sha256(b'{}').hexdigest())
        self.assertEqual((self.root/'copy/inputs/city.json').stat().st_mode & 0o777,0o400)
        self.assertEqual(self.arc.read_bytes(),before);self.assertEqual(m,self.manifest)
        self.assertFalse((self.root/'copy/badlink').exists())

    def test_link_unknown_and_quarantined_members_rejected(self):
        for entry in ['entry-00000000','entry-99999999']:
            with self.subTest(entry=entry),self.assertRaises(ValueError):
                prep.prepare(self.arc,self.manifest,{entry:'a'},self.root/'copy',self.limits)
        self.assertFalse((self.root/'copy').exists())

    def test_unsafe_generated_destinations_fail_before_copy(self):
        for name in ['/abs','../escape','a/../escape','a//b','a/./b','a\\b','']:
            with self.subTest(name=name),self.assertRaises(ValueError):
                prep.prepare(self.arc,self.manifest,{'entry-00000001':name},self.root/'copy',self.limits)
        self.assertFalse((self.root/'copy').exists())

    def test_changed_archive_or_manifest_never_publishes_partial_copy(self):
        self.arc.write_bytes(self.arc.read_bytes()+b'corrupt')
        with self.assertRaises(ValueError):
            prep.prepare(self.arc,self.manifest,self.dest,self.root/'copy',self.limits)
        self.assertFalse((self.root/'copy').exists())
        bad=copy.deepcopy(self.manifest);bad['members'][1]['sha256']='0'*64
        with self.assertRaises(ValueError):
            prep.prepare(self.arc,bad,self.dest,self.root/'copy',self.limits)

    def test_staging_and_expansion_budget_fail_closed(self):
        from unittest.mock import patch
        with patch.object(prep,'MAX_COPY_BYTES',1),self.assertRaises(ValueError):
            prep.prepare(self.arc,self.manifest,self.dest,self.root/'copy',self.limits)
        limited=dict(self.limits,max_expanded_bytes=100)
        with self.assertRaises(ValueError):
            prep.prepare(self.arc,self.manifest,self.dest,self.root/'copy',limited)
        self.assertFalse((self.root/'copy').exists())

    def test_existing_destination_and_case_collision_refused(self):
        copyroot=self.root/'copy';copyroot.mkdir();(copyroot/'keep').write_text('keep')
        with self.assertRaises(ValueError):
            prep.prepare(self.arc,self.manifest,self.dest,copyroot,self.limits)
        self.assertEqual((copyroot/'keep').read_text(),'keep')
        with self.assertRaises(ValueError):
            prep.prepare(self.arc,self.manifest,{'entry-00000001':'a','entry-00000002':'A'},self.root/'new',self.limits)


    def test_corrupt_footer_never_publishes_copy_even_with_matching_outer_hash(self):
        data=bytearray(self.arc.read_bytes());data[-8]^=1;self.arc.write_bytes(data)
        m=copy.deepcopy(self.manifest);m['archive_sha256']=hashlib.sha256(data).hexdigest()
        m['manifest_sha256']=inventory.canonical_digest({k:v for k,v in m.items() if k!='manifest_sha256'})
        with self.assertRaises((ValueError,OSError,EOFError)):
            prep.prepare(self.arc,m,self.dest,self.root/'copy',self.limits)
        self.assertFalse((self.root/'copy').exists())

    def test_invalid_budget_and_nonprivate_parent_fail_closed(self):
        for limits in [dict(self.limits,max_seconds=True),dict(self.limits,max_compressed_bytes=1)]:
            with self.assertRaises(ValueError):
                prep.prepare(self.arc,self.manifest,self.dest,self.root/'copy',limits)
        self.root.chmod(0o755)
        with self.assertRaises(ValueError):
            prep.prepare(self.arc,self.manifest,self.dest,self.root/'copy',self.limits)
        self.root.chmod(0o700)

    def test_sandbox_mounts_and_nonprivileged_target_uid(self):
        for name in ('deps','source','inputs','A','B','probes','build'):
            (self.root/name).mkdir()
        args=commands.sandbox(self.root,'/A')
        self.assertEqual(args[:3],['/usr/bin/sudo','-n','/usr/bin/timeout'])
        self.assertIn('--unshare-net',args);self.assertIn('--no-new-privs',args)
        self.assertNotIn('--bind',args)
        self.assertEqual(args[args.index('--reuid')+1],str(os.getuid()))
        build=commands.sandbox(self.root,'/build',build=True)
        self.assertEqual(build.count('--bind'),1)
        self.assertEqual(build[build.index('--bind')+2],'/build')

    def test_guarded_target_cannot_silently_relax_limits(self):
        args=commands.guarded_target(['/build/sw_cosim','--validate-config'])
        self.assertIn('--kill-on-exit',args)
        self.assertIn('--inject=execve:error=EPERM',args)
        self.assertIn('--inject=%network:error=EPERM',args)
        self.assertNotIn('--detach-on=execve',args)
        for kw in [{'cpu':6},{'memory':268435457},{'cpu':True}]:
            with self.assertRaises(ValueError):commands.guarded_target(['/build/sw_cosim'],**kw)
        for argv in [['/usr/bin/sh'],['/build/../usr/bin/sh'],[123]]:
            with self.assertRaises(ValueError):commands.guarded_target(argv)


if __name__=='__main__':unittest.main()
