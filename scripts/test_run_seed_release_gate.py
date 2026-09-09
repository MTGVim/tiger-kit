from __future__ import annotations

import copy
import unittest

import run_seed_release_gate as gate


class SeedReleaseGateTests(unittest.TestCase):
    def setUp(self):
        self.contracts = {'tk-prep': {
            'triggers': {'queries': []},
            'behavior': {'evals': [{'id': 'protected', 'assertions': [
                {'type': 'git_head_unchanged'}, {'type': 'judge', 'criterion': 'preserve work'}
            ]}]},
        }}

    def test_current_contract_is_preserved(self):
        self.assertEqual(gate.preservation_errors(self.contracts, self.contracts, {}, set()), [])

    def test_removed_mechanical_protection_is_not_exempt(self):
        candidate = copy.deepcopy(self.contracts)
        candidate['tk-prep']['behavior']['evals'][0]['assertions'].pop(0)
        errors = gate.preservation_errors(self.contracts, candidate, {}, set())
        self.assertTrue(any('mechanical' in e for e in errors), errors)
        self.assertEqual(len(self.contracts['tk-prep']['behavior']['evals'][0]['assertions']), 2)

    def test_legacy_skill_wide_exemption_fails_closed(self):
        errors = gate.preservation_errors(self.contracts, {}, {
            'replaced_skill_eval_contracts': ['tk-prep']}, set())
        self.assertTrue(any('replaced_skill_eval_contracts' in e for e in errors), errors)
        self.assertTrue(any('deleted' in e for e in errors), errors)

    def test_catalog_wide_exemption_fails_closed(self):
        errors = gate.preservation_errors(self.contracts, self.contracts, {
            'replace_catalog_contract': True}, set())
        self.assertTrue(any('replace_catalog_contract' in e for e in errors), errors)

    def test_explicit_retirement_remains_available(self):
        self.assertEqual(gate.preservation_errors(self.contracts, {}, {}, {'tk-prep'}), [])


if __name__ == '__main__':
    unittest.main()
