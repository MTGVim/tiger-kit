#!/usr/bin/env python3
from __future__ import annotations

import unittest

import run_drive_experiment


class DriveExperimentTest(unittest.TestCase):
    def test_manifest_has_matched_scenarios(self) -> None:
        manifest = run_drive_experiment.load_manifest()
        self.assertEqual(manifest["hosts"], list(run_drive_experiment.HOST_ORDER))
        self.assertGreaterEqual(len(manifest["scenarios"]), 3)
        self.assertGreaterEqual(manifest["runs"], 2)

    def test_required_phases_must_precede_final_output(self) -> None:
        events = [
            {"type": "phase_invocation", "phase": "tk-drive"},
            {"type": "phase_invocation", "phase": "tk-to-spec"},
            {"type": "final_output", "terminal_status": "Pass"},
        ]
        self.assertTrue(run_drive_experiment.ordered_phases(events, ["tk-drive", "tk-to-spec"]))
        self.assertFalse(run_drive_experiment.ordered_phases(events, ["tk-drive", "tk-implement"]))

    def test_drive_is_kept_when_quality_is_not_worse(self) -> None:
        records = []
        for arm in run_drive_experiment.ARMS:
            records.extend(
                [
                    {"arm": arm, "passed": True, "continuation_ok": True, "total_tokens": 10, "duration_ms": 20},
                    {"arm": arm, "passed": True, "continuation_ok": True, "total_tokens": 10, "duration_ms": 20},
                ]
            )
        self.assertEqual(run_drive_experiment.summarize(records)["decision"], "Keep")

    def test_drive_becomes_remove_candidate_only_on_clear_gap(self) -> None:
        records = [
            {"arm": "drive", "passed": False, "continuation_ok": False},
            {"arm": "drive", "passed": False, "continuation_ok": False},
            {"arm": "composition", "passed": True, "continuation_ok": True},
            {"arm": "composition", "passed": True, "continuation_ok": True},
        ]
        self.assertEqual(run_drive_experiment.summarize(records)["decision"], "RemoveCandidate")

    def test_composition_prompt_explicitly_excludes_drive(self) -> None:
        prompt = run_drive_experiment.prompt_for("composition", "source")
        self.assertIn("Do not invoke tk-drive", prompt)
        self.assertIn("$tk-to-spec", prompt)


if __name__ == "__main__":
    unittest.main()
