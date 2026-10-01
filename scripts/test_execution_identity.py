"""Regression coverage for observed execution identity and resource honesty."""
import copy
import math
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

try:
    from . import run_skill_evals as runner
except ImportError:
    import run_skill_evals as runner

build_verdict = runner.build_verdict
validate_adapter_result = runner.validate_adapter_result
comparison_errors = runner.comparison_errors


class ExecutionIdentityTest(unittest.TestCase):
    def summary(self, model="actual-model"):
        return {"trigger_accuracy": 1, "behavior_pass_rate": 1,
                "duration_ms": 10, "total_tokens": 10,
                "execution_runs": [{"host": "codex", "case": "case-1", "run": 1,
                                    "prompt_sha256": "a" * 64,
                                    "execution_identity": {"model": model}}]}

    def test_same_observed_model_compares(self):
        self.assertEqual(build_verdict(self.summary(), self.summary())["status"], "Pass")

    def test_mismatch_and_missing_model_do_not_compare(self):
        for identity in ({"model": "different-model"}, None, {"model": "unknown"}):
            candidate = self.summary()
            candidate["execution_runs"][0]["execution_identity"] = identity
            verdict = build_verdict(self.summary(), candidate)
            self.assertEqual(verdict["status"], "Unverifiable")
            self.assertEqual(verdict["reasons"], [])
        baseline, candidate = self.summary(), self.summary()
        for summary in (baseline, candidate):
            summary["execution_runs"][0]["execution_identity"] = None
        self.assertEqual(build_verdict(baseline, candidate)["status"], "Unverifiable")

    def test_config_mismatch_and_one_sided_observation(self):
        baseline = self.summary()
        baseline["execution_runs"][0]["execution_identity"]["config"] = {"reasoning_effort": "high"}
        for config in ({}, {"reasoning_effort": "low"}):
            candidate = self.summary()
            candidate["execution_runs"][0]["execution_identity"]["config"] = config
            self.assertTrue(comparison_errors(baseline, candidate))
        self.assertEqual(build_verdict(baseline, copy.deepcopy(baseline))["status"], "Pass")

    def test_case_trial_prompt_and_duplicate_mismatches(self):
        for field, value in (("case", "case-2"), ("run", 2), ("host", "claude-code"),
                             ("prompt_sha256", "b" * 64)):
            candidate = self.summary()
            candidate["execution_runs"][0][field] = value
            self.assertTrue(comparison_errors(self.summary(), candidate))
        candidate = self.summary()
        candidate["execution_runs"].append(copy.deepcopy(candidate["execution_runs"][0]))
        self.assertTrue(comparison_errors(self.summary(), candidate))

    def test_invalid_and_missing_metrics(self):
        base = {"skill_loaded": True, "output": "done", "terminal_status": "Pass"}
        for field in ("total_tokens", "duration_ms", "cost_usd"):
            for value in (-1, True, False, math.nan, math.inf, "10"):
                self.assertTrue(validate_adapter_result({**base, field: value}), (field, value))
            self.assertEqual(validate_adapter_result({**base, field: None}), [])
        candidate = self.summary()
        candidate["total_tokens"] = None
        self.assertEqual(build_verdict(self.summary(), candidate)["status"], "Unverifiable")

    def test_untrusted_or_broad_config_is_rejected(self):
        base = {"skill_loaded": True, "output": "done", "terminal_status": "Pass"}
        for identity in ({"model": ""}, {"model": "a", "config": {"settings_dump": "private"}},
                         {"model": "a", "config": {"temperature": math.nan}}):
            self.assertTrue(validate_adapter_result({**base, "execution_identity": identity}))

    def test_candidate_safety_failures_survive_noncomparability(self):
        candidate = self.summary("different-model")
        candidate["safety_failures"] = 1
        verdict = build_verdict(self.summary(), candidate)
        self.assertEqual(verdict["status"], "Fail")
        self.assertTrue(verdict["unverifiable"])
        self.assertIn("safety", verdict["reasons"][0])

    def test_diagnostic_unknown_identity_keeps_profile_without_relative_claims(self):
        base = {"execution_runs": self.summary()["execution_runs"]}
        candidate = {"execution_runs": self.summary("different-model")["execution_runs"],
                     "resource_metrics": {"total_tokens": 1}}
        verdict = runner.compare_diagnostics(base, candidate)
        self.assertEqual(verdict["status"], "Unverifiable")
        self.assertEqual(verdict["resource_metrics"], candidate["resource_metrics"])
        self.assertEqual(verdict["phase_regressions"], [])
        candidate["holdout_failures"] = ["holdout"]
        self.assertEqual(runner.compare_diagnostics(base, candidate)["status"], "Fail")

    def test_runner_preserves_observed_identity_and_null_resources(self):
        contracts = {"tk-example": {
            "triggers": {"kind": "hybrid", "queries": [{"id": "one", "split": "validation",
                         "query": "same prompt", "should_trigger": True}]},
            "behavior": {"evals": []}}}
        result = {"skill_loaded": True, "output": "done", "terminal_status": "Pass",
                  "total_tokens": None, "duration_ms": None, "cost_usd": None,
                  "execution_identity": {"model": "actual-model"}}
        with tempfile.TemporaryDirectory() as directory, patch.object(runner, "run_adapter", return_value=result):
            summary, records = runner.evaluate_checkout(Path(directory), contracts, adapter_command="unused",
                grader_command="unused", host="codex", runs=1, case_filter=None)
        self.assertIsNone(summary["duration_ms"])
        self.assertIsNone(summary["total_tokens"])
        self.assertIsNone(records[0]["cost_usd"])
        self.assertEqual(summary["execution_runs"][0]["execution_identity"], result["execution_identity"])
        self.assertEqual(comparison_errors(summary, summary), [])


if __name__ == "__main__":
    unittest.main()
