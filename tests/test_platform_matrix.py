"""Platform-plan evidence must never imply Windows/Linux runtime parity."""
import copy
import json
import hashlib
import tempfile
from pathlib import Path
import random
import subprocess
import sys
import unittest
from unittest.mock import patch
from scripts import validate_platform_matrix as matrix


class PlatformMatrixTests(unittest.TestCase):
    def fixture(self):return json.loads((matrix.ROOT/'docs/platforms/S017_MATRIX.json').read_text())
    def test_real_plan_remains_unverified_runtime(self):
        result=matrix.validate(self.fixture(),matrix.ROOT)
        self.assertEqual(result['targets'],3);self.assertEqual(result['verified_simulator_targets'],0)
        self.assertEqual(result['later_platform_gates'],'OPEN')
    def test_required_windows_cannot_reuse_linux_pass(self):
        data=self.fixture();target=data['platforms'][1];target['gates']['host_probe']={'status':'PASS','evidence_id':'E-S017-HOST-01'}
        with self.assertRaises(ValueError):matrix.validate(data,matrix.ROOT)
    def test_relabelled_linux_observations_cannot_be_windows_receipt(self):
        data=self.fixture();data['platforms'][0]['gates']['host_probe']={'status':'NOT_RUN','evidence_id':None}
        data['platforms'][1]['gates']['host_probe']={'status':'PASS','evidence_id':'E-S017-HOST-01'}
        receipt=json.loads((matrix.ROOT/data['evidence'][0]['artifact']).read_text())
        receipt['platform_id']='WIN11_WSL2_UBUNTU2404_X86_64'
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);path=root/data['evidence'][0]['artifact'];path.parent.mkdir(parents=True);path.write_text(json.dumps(receipt))
            data['evidence'][0]['sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
            with self.assertRaises(ValueError):matrix.validate(data,root)

    def test_host_probe_is_not_adapter_or_replay_proof(self):
        for scope in ['governance','dependency_smoke','adapter_integration','deterministic_replay']:
            data=self.fixture();data['platforms'][0]['gates'][scope]={'status':'PASS','evidence_id':'E-S017-HOST-01'}
            with self.subTest(scope=scope),self.assertRaises(ValueError):matrix.validate(data,matrix.ROOT)
    def test_missing_duplicate_or_pinned_dependency_rejected(self):
        for mutate in [lambda d:d['platforms'][0]['dependencies'].pop(),lambda d:d['platforms'][0]['dependencies'].append(copy.deepcopy(d['platforms'][0]['dependencies'][0])),lambda d:d['platforms'][0]['dependencies'][0].update(version_pin='guessed'),lambda d:d['platforms'][0]['dependencies'][0].update(verification_status='PASS')]:
            data=self.fixture();mutate(data)
            with self.assertRaises(ValueError):matrix.validate(data,matrix.ROOT)
    def test_runtime_support_tuple_and_schema_promotion_rejected(self):
        for mutate in [lambda d:d.update(schema_version=True),lambda d:d['platforms'][0].update(simulator_support_verified=True),lambda d:d['platforms'][0].update(host_os='Windows 11'),lambda d:d['platforms'][1].update(runtime_kind='native_msys2'),lambda d:d.update(accepted_dependency_versions=['legacy_version'])]:
            data=self.fixture();mutate(data)
            with self.assertRaises(ValueError):matrix.validate(data,matrix.ROOT)
    def test_corrupted_receipt_and_private_path_rejected(self):
        for value in ['../private.json','/private.json']:
            data=self.fixture();data['evidence'][0]['artifact']=value
            with self.assertRaises(ValueError):matrix.validate(data,matrix.ROOT)
        data=self.fixture();data['evidence'][0]['sha256']='0'*64
        with self.assertRaises(ValueError):matrix.validate(data,matrix.ROOT)
    def test_generated_ordering_keeps_required_targets_and_open_gates(self):
        rng=random.Random(17)
        for _ in range(100):
            data=self.fixture();rng.shuffle(data['platforms'])
            for row in data['platforms']:rng.shuffle(row['dependencies'])
            result=matrix.validate(data,matrix.ROOT)
            self.assertEqual(result['required_targets'],2);self.assertEqual(result['verified_simulator_targets'],0)
    def test_non_linux_host_is_not_assigned_linux_evidence(self):
        with patch.object(matrix.platform,'system',return_value='Windows'),patch.object(matrix.platform,'machine',return_value='AMD64'):
            report=matrix.host_probe()
        self.assertEqual(report['platform_id'],'UNCLASSIFIED_HOST');self.assertFalse(report['simulator_support_verified'])
    def test_cli_plan_from_other_cwd_needs_no_simulator_or_private_inputs(self):
        result=subprocess.run([sys.executable,str(Path(matrix.__file__).resolve()),'check',str(matrix.ROOT/'docs/platforms/S017_MATRIX.json')],cwd='/',capture_output=True)
        self.assertEqual(result.returncode,0,result.stderr);self.assertEqual(json.loads(result.stdout)['status'],'VALID_PLATFORM_PLAN_UNVERIFIED_RUNTIME')


if __name__=='__main__':unittest.main()
