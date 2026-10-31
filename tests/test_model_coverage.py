"""Independent synthetic completeness checks prevent false scope acceptance."""
import copy
import hashlib
import unittest
from scripts import inventory_legacy as intake
from scripts import review_model_spans as review
from scripts import validate_model_coverage as coverage


class CoverageTests(unittest.TestCase):
    def fixture(self):
        text='default = 1\n';sha=hashlib.sha256(text.encode()).hexdigest()
        row={'id':'R1','entry_id':'entry-00000001','source_sha256':sha,'line_start':1,'line_end':1,'category':'default','observation':'Synthetic default'}
        plan={'schema_version':1,'records':[row]}
        common={'schema_version':1,'archive_sha256':'a'*64,'intake_manifest_sha256':'b'*64,'source_reuse':'PROHIBITED','scientific_validation':'UNVALIDATED'}
        candidate={**common,'traversal_complete':True,'sources':[{'entry_id':row['entry_id'],'source_sha256':sha,'scopes':['project_source']}]}
        auxiliary={**common,'traversal_complete':True,'review_plan_sha256':intake.canonical_digest(plan),'files':[{'entry_id':row['entry_id'],'source_sha256':sha,'context':'native_runtime_or_tool','python_status':'not_python'}],'expressions':[]}
        reviewed={**common,'selected_ranges_complete':True,'plan_sha256':intake.canonical_digest(plan),'records':[review.resolve(row,{'entry_id':row['entry_id'],'sha256':sha},text)]}
        return candidate,auxiliary,reviewed,plan
    def seal(self, args):
        for value in args[:3]:
            value.pop('manifest_sha256',None);value['manifest_sha256']=intake.canonical_digest(value)
        return args
    def test_complete_scope_does_not_validate_science(self):
        result=coverage.validate(*self.seal(self.fixture()))
        self.assertTrue(result['scope_coverage_complete']);self.assertFalse(result['whole_archive_semantic_analysis'])
        self.assertEqual(result['scientific_validation'],'UNVALIDATED');self.assertEqual(result['source_reuse'],'PROHIBITED')
    def test_missing_duplicate_and_unreviewed_sources_rejected(self):
        for mutate in [lambda a:a[1]['files'].clear(),lambda a:a[1]['files'].append(copy.deepcopy(a[1]['files'][0])),lambda a:a[2]['records'].clear()]:
            args=self.fixture();mutate(args)
            with self.assertRaises(ValueError):coverage.validate(*self.seal(args))
    def test_hash_plan_or_scientific_promotion_rejected(self):
        for mutate in [lambda a:a[1].update(review_plan_sha256='0'*64),lambda a:a[1]['files'][0].update(source_sha256='0'*64),lambda a:a[2]['records'][0].update(scientific_support='VALIDATED')]:
            args=self.fixture();mutate(args)
            with self.assertRaises(ValueError):coverage.validate(*self.seal(args))
    def test_model_cannot_be_hidden_as_test(self):
        args=self.fixture();args[1]['files'][0]['context']='test_fixture_or_probe'
        with self.assertRaises(ValueError):coverage.validate(*self.seal(args))


if __name__=='__main__':unittest.main()
