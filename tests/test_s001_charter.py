"""Bounded charter contract checks; these do not substitute for independent review."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def scope_rows(text):
    rows = []
    for line in text.splitlines():
        if re.match(r"\| C\d+ \|", line):
            cells = [cell.strip() for cell in line.strip('|').split('|')]
            if len(cells) != 4 or not all(cells):
                raise ValueError('incomplete scope row')
            rows.append(cells)
    if [row[0] for row in rows] != [f'C{i:02}' for i in range(1, 11)]:
        raise ValueError('missing, duplicate or reordered scope IDs')
    return rows


class CharterContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = (ROOT / 'docs/PROJECT_CHARTER.md').read_text()

    def test_objectives_have_observable_criteria_and_roadmap_owners(self):
        rows = scope_rows(self.text)
        covered = []
        for _, outcome, acceptance, roadmap in rows:
            self.assertTrue(outcome.strip())
            self.assertTrue(acceptance.strip())
            start, end = re.fullmatch(r'S(\d{3})–S(\d{3})', roadmap).groups()
            covered.extend(range(int(start), int(end) + 1))
        self.assertEqual(covered, list(range(2, 89)))

    def test_missing_duplicate_and_reordered_ids_fail(self):
        row = next(line for line in self.text.splitlines() if line.startswith('| C01 |'))
        for mutation in (self.text.replace(row, ''), self.text + '\n' + row,
                         self.text.replace('| C01 |', '| C02 |')):
            with self.subTest(mutation=mutation[-60:]), self.assertRaises(ValueError):
                scope_rows(mutation)

    def test_empty_acceptance_fails(self):
        rows = scope_rows(self.text)
        mutation = self.text.replace(rows[0][2], '')
        with self.assertRaises(ValueError):
            scope_rows(mutation)

    def test_public_charter_answers_contributor_questions(self):
        for heading in ('Purpose', 'Users and decisions', 'Scope',
                        'Non-goals in the initial phase', 'Scope map and observable acceptance',
                        'Scenario settings and hypothesis boundary',
                        'Contract conventions and failure semantics',
                        'Exclusions and approval boundary'):
            self.assertIn('## ' + heading + '\n', self.text)
        for obligation in ('units', 'simulation time', 'fail closed',
                           'configuration hashes', 'independent review'):
            self.assertIn(obligation, self.text)

    def test_required_attack_has_explicit_correction(self):
        boundary = self.text.split('## Scenario settings and hypothesis boundary\n')[1].split('\n## ')[0]
        for setting in ('City size', 'bin count', 'fleet size'):
            self.assertIn(setting, boundary)
        self.assertIn('are scenario settings', boundary)
        self.assertIn('not universal scientific hypotheses', boundary)


if __name__ == '__main__':
    unittest.main()
