"""Independent exact-rational references for representation conventions."""
import importlib.util
from fractions import Fraction
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('scripts.conventions', ROOT / 'scripts/check_conventions.py')
c = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(c)


class ConventionTests(unittest.TestCase):
    def test_dimensions_and_reference_conversions(self):
        cases = [('distance', '1', 'km', 1000), ('mass', '1000', 'g', 1),
                 ('volume', '1000', 'L', 1), ('fuel_volume', '1', 'L', Fraction(1, 1000)),
                 ('temperature', '0', 'degC', Fraction(27315, 100)),
                 ('temperature_interval', '1', 'degC', 1), ('humidity', '50', '%', Fraction(1, 2)),
                 ('speed', '36', 'km/h', 10), ('emission_mass', '1000000', 'mg', 1),
                 ('emission_rate', '1', 'g/s', Fraction(1, 1000)),
                 ('latency', '1000', 'ms', 1), ('elapsed_time', '1', 'h', 3600)]
        for name, value, unit, expected in cases:
            with self.subTest(name=name):
                result, canonical, dimension = c.normalize_quantity(name, value, unit)
                self.assertEqual(result, expected)
                self.assertTrue(canonical)
                self.assertEqual(dimension, {'distance':'L','mass':'M','volume':'L^3',
                    'fuel_volume':'L^3','temperature':'Theta','temperature_interval':'Theta',
                    'humidity':'1','speed':'L/T','emission_mass':'M','emission_rate':'M/T',
                    'latency':'T','elapsed_time':'T'}[name])
        self.assertEqual(c.normalize_quantity('distance', '1000', 'm'), c.normalize_quantity('distance', '1', 'km'))
        self.assertEqual(c.normalize_quantity('temperature', '273.15', 'K'), c.normalize_quantity('temperature', '0', 'degC'))

    def test_unknown_cross_dimension_and_extreme_inputs_fail(self):
        for name, value, unit in [('distance','1','kg'), ('temperature','0','C'),
                                 ('humidity','101','%'), ('temperature','-273.16','degC'),
                                 ('distance','NaN','m'), ('distance','Infinity','m'),
                                 ('distance',True,'m'), ('distance','1e1000000','m'),
                                 ('distance','-1','m'), ('unknown','1','m')]:
            with self.subTest(name=name, value=value, unit=unit):
                with self.assertRaises(ValueError): c.normalize_quantity(name, value, unit)
        self.assertEqual(c.normalize_quantity('temperature', '-273.15', 'degC')[0], 0)
        self.assertEqual(c.normalize_quantity('humidity', '100', '%')[0], 1)

    def test_generated_equivalences_and_global_context_independence(self):
        for value in range(0, 101):
            self.assertEqual(c.normalize_quantity('distance', str(value), 'km'),
                             c.normalize_quantity('distance', str(value * 1000), 'm'))
            self.assertEqual(c.normalize_quantity('speed', str(value * 36), 'km/h')[0], value * 10)

    def test_utc_normalization_and_ambiguous_times(self):
        expected = '2026-10-21T23:00:00.000000Z'
        self.assertEqual(c.normalize_timestamp('2026-10-22T02:00:00+03:00'), expected)
        self.assertEqual(c.normalize_timestamp('2026-10-21T23:00:00Z'), expected)
        for value in ('2026-10-22T02:00:00', '2026-10-22T02:00:00-00:00',
                      '2026-02-30T00:00:00Z', '2016-12-31T23:59:60Z',
                      '2026-10-22T00:00:00.1234567Z', '2026-10-22 00:00:00Z', '2026-10-22T00:00:00+01:99'):
            with self.assertRaises(ValueError): c.normalize_timestamp(value)

    def test_ids_do_not_depend_on_names(self):
        entities = [{'id':'bin-001', 'display_name':'Bin A'}, {'id':'bin-002','display_name':'Bin A'}]
        self.assertEqual(c.check_entities(entities), [])
        entities[0]['display_name'] = 'Renamed حاوية'
        self.assertEqual(c.check_entities(entities), [])
        self.assertEqual(entities[0]['id'], 'bin-001')
        entities[1]['id'] = 'bin-001'
        self.assertTrue(c.check_entities(entities))
        for value in ('', 'display name', '../bin', None):
            self.assertTrue(c.check_entities([{'id':value, 'display_name':'name'}]))

    def test_cli_and_catalog_versions(self):
        cmd = [sys.executable, str(ROOT / 'scripts/check_conventions.py')]
        self.assertEqual(subprocess.run(cmd + ['quantity', 'distance', '1', 'km'], capture_output=True).returncode, 0)
        bad = subprocess.run(cmd + ['quantity', 'distance', '1', 'unknown'], capture_output=True, text=True)
        self.assertEqual(bad.returncode, 1)
        self.assertNotIn('Traceback', bad.stderr)
        self.assertEqual(subprocess.run(cmd + ['timestamp', '2026-10-22T00:00:00'], capture_output=True).returncode, 1)
        with self.assertRaises(ValueError): c.load_catalog({'schema_version':2, 'quantities':{}})


if __name__ == '__main__': unittest.main()
