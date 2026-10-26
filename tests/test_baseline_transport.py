"""Synthetic hostile output packets, never legacy code or owner archive."""
import copy
import hashlib
import os
import random
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from scripts import baseline_transport as t
from scripts.baseline_supervisor import command


class BaselineTransportTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.out=self.root/'out';self.out.mkdir()
        (self.out/'events.jsonl').write_bytes(b'{"synthetic":true}\n')
        self.process={'target_exit':3,'termination':'exited'}

    def test_roundtrip_retains_failed_exit_and_exact_bytes(self):
        packet=t.pack(self.out,self.process);dest=self.root/'copy'
        self.assertEqual(t.decode(packet,dest),self.process)
        self.assertEqual((dest/'events.jsonl').read_bytes(),(self.out/'events.jsonl').read_bytes())
        self.assertEqual((dest/'events.jsonl').stat().st_mode&0o777,0o400)

    def test_pack_refuses_symlinks_hardlinks_and_special_files(self):
        for kind in ('symlink','hardlink','fifo'):
            link=self.out/'unsafe'
            if kind=='symlink':link.symlink_to('/outside')
            elif kind=='hardlink':os.link(self.out/'events.jsonl',link)
            else:os.mkfifo(link)
            with self.subTest(kind=kind),self.assertRaises(ValueError):t.pack(self.out,self.process)
            link.unlink()

    def test_generated_bad_names_never_publish(self):
        for name in ('/abs','../escape','a/../escape','a//b','a/./b','a\\b','', 'x'*1025):
            packet=t.pack(self.out,self.process);packet['files'][0]['path']=name
            with self.subTest(name=name),self.assertRaises(ValueError):t.decode(packet,self.root/'copy')
            self.assertFalse((self.root/'copy').exists())

    def test_duplicate_case_collision_conflict_corruption_and_incomplete_refused(self):
        for attack in ('duplicate','case','conflict','hash','size','base64','incomplete'):
            packet=t.pack(self.out,self.process);r=packet['files'][0]
            if attack in ('duplicate','case','conflict'):
                extra=copy.deepcopy(r)
                extra['path']=r['path'] if attack=='duplicate' else r['path'].upper() if attack=='case' else r['path']+'/child'
                packet['files'].append(extra)
            elif attack=='hash':r['sha256']='0'*64
            elif attack=='size':r['bytes']+=1
            elif attack=='base64':r['base64']='!!'
            else:packet['complete']=False
            with self.subTest(attack=attack),self.assertRaises(ValueError):t.decode(packet,self.root/'copy')
            self.assertFalse((self.root/'copy').exists())

    def test_budgets_and_existing_output_never_overwritten(self):
        packet=t.pack(self.out,self.process)
        with patch.object(t,'MAX_FILE_BYTES',1),self.assertRaises(ValueError):t.pack(self.out,self.process)
        with patch.object(t,'MAX_BYTES',1),self.assertRaises(ValueError):t.decode(packet,self.root/'copy')
        dest=self.root/'copy';dest.mkdir();(dest/'keep').write_text('keep')
        with self.assertRaises(ValueError):t.decode(packet,dest)
        self.assertEqual((dest/'keep').read_text(),'keep')

    def test_seeded_binary_payloads_and_member_order_preserve_exact_bytes(self):
        rng=random.Random(120)
        expected={'events.jsonl':(self.out/'events.jsonl').read_bytes()}
        for i in range(12):
            data=rng.randbytes(rng.randrange(0,2048));name='sample'+str(i)
            (self.out/name).write_bytes(data);expected[name]=data
        packet=t.pack(self.out,self.process);rng.shuffle(packet['files'])
        dest=self.root/'copy';t.decode(packet,dest)
        self.assertEqual({p.name:p.read_bytes() for p in dest.iterdir()},expected)

    def test_case_collision_in_parent_directory_is_also_rejected(self):
        packet=t.pack(self.out,self.process);a=packet['files'][0];a['path']='A/first'
        b=copy.deepcopy(a);b['path']='a/second';packet['files'].append(b)
        with self.assertRaises(ValueError):t.decode(packet,self.root/'copy')
        self.assertFalse((self.root/'copy').exists())

    def test_normal_command_and_denials_are_fixed_not_shell(self):
        args=command('baseline')
        self.assertEqual(args[-4:],['/build/sw_cosim','/inputs/config.json','/A/city_fixture','/outputs/baseline'])
        self.assertIn('--cpu=60',args);self.assertIn('--as=1073741824',args)
        self.assertIn('--inject=execve:error=EPERM',args);self.assertIn('--kill-on-exit',args)
        with self.assertRaises(ValueError):command('/usr/bin/sh')


if __name__=='__main__':unittest.main()
