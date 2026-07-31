#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import run_release_gate
from run_skill_evals import load_catalog_contract, load_eval_contracts


class ReleaseGateContractTest(unittest.TestCase):
    def test_manifest_is_closed_and_references_existing_cases(self) -> None:
        manifest = run_release_gate.load_manifest()
        self.assertEqual(manifest["hosts"], list(run_release_gate.SUPPORTED_HOSTS))
        self.assertGreaterEqual(manifest["runs"], 2)

        contracts = load_eval_contracts(run_release_gate.ROOT, None)
        behavior = run_release_gate.behavior_case_map(contracts)
        catalog = run_release_gate.catalog_case_map(
            load_catalog_contract(run_release_gate.ROOT)
        )
        self.assertTrue(set(manifest["behavior_cases"]).issubset(behavior))
        self.assertTrue(set(manifest["catalog_cases"]).issubset(catalog))

    def test_manifest_rejects_reduced_host_or_run_matrix(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "release-critical.json"
            path.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "hosts": ["codex"],
                        "runs": 1,
                        "behavior_cases": ["x"],
                        "catalog_cases": ["y"],
                    }
                ),
                encoding="utf-8",
            )
            with patch.object(run_release_gate, "MANIFEST", path):
                with self.assertRaisesRegex(ValueError, "hosts"):
                    run_release_gate.load_manifest()

    def test_normalized_assertions_are_mechanical_and_host_neutral(self) -> None:
        rows = run_release_gate.normalized_assertions(
            {
                "id": "example",
                "assertions": [
                    {"type": "judge", "criterion": "subjective"},
                    {
                        "type": "event_order",
                        "hosts": ["codex"],
                        "before": {"type": "phase_invocation", "phase": "a"},
                        "after": {"type": "phase_invocation", "phase": "b"},
                    },
                    {"type": "git_commit_count_delta", "count": 1},
                    {"type": "terminal_status", "expected": "Pass"},
                ],
            }
        )
        self.assertEqual([row["type"] for row in rows], [
            "event_order",
            "git_commit_count_delta",
            "terminal_status",
        ])
        self.assertEqual(rows[0]["hosts"], list(run_release_gate.SUPPORTED_HOSTS))
        self.assertEqual(rows[1]["expected"], 1)
        self.assertNotIn("count", rows[1])

    def test_normalized_assertions_require_terminal_verdict(self) -> None:
        with self.assertRaisesRegex(ValueError, "mechanical terminal"):
            run_release_gate.normalized_assertions(
                {"id": "bad", "assertions": [{"type": "path_exists", "path": "x"}]}
            )


if __name__ == "__main__":
    unittest.main()
