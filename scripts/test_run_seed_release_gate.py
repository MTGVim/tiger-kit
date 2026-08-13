from __future__ import annotations

import unittest

import run_seed_release_gate


class SeedReleaseGateTests(unittest.TestCase):
    def test_filter_replaced_baseline_only_removes_declared_skills(self) -> None:
        baseline = {
            "tk-a": {"triggers": {"queries": []}, "behavior": {"evals": []}},
            "tk-b": {"triggers": {"queries": []}, "behavior": {"evals": []}},
        }
        result = run_seed_release_gate.filter_replaced_baseline(baseline, {"tk-b"})
        self.assertEqual(set(result), {"tk-a"})
        self.assertEqual(set(baseline), {"tk-a", "tk-b"})

    def test_replaced_eval_contracts_requires_strings(self) -> None:
        with self.assertRaises(ValueError):
            run_seed_release_gate.replaced_eval_contracts(
                {"replaced_skill_eval_contracts": ["tk-a", 1]}
            )


if __name__ == "__main__":
    unittest.main()
