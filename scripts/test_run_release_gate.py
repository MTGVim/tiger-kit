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
        self.assertEqual(manifest["hosts"], list(run_release_gate.HOST_ORDER))
        self.assertEqual(run_release_gate.HOST_ORDER, ("codex", "claude-code", "hermes-agent"))
        self.assertGreaterEqual(manifest["runs"], 2)
        contracts = load_eval_contracts(run_release_gate.ROOT, None)
        catalog = load_catalog_contract(run_release_gate.ROOT)
        self.assertEqual(run_release_gate.validate_manifest_cases(contracts, catalog, manifest), [])

    def test_manifest_rejects_wrong_host_order(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "release-critical.json"
            path.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "hosts": ["claude-code", "codex", "hermes-agent"],
                        "runs": 2,
                        "behavior_cases": ["x"],
                        "catalog_cases": ["y"],
                    }
                ),
                encoding="utf-8",
            )
            with patch.object(run_release_gate, "MANIFEST", path):
                with self.assertRaisesRegex(ValueError, "ordered"):
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
        self.assertEqual([row["type"] for row in rows], ["event_order", "git_commit_count_delta", "terminal_status"])
        self.assertEqual(rows[0]["hosts"], list(run_release_gate.HOST_ORDER))
        self.assertEqual(rows[1]["expected"], 1)

    def test_builtin_adapter_is_the_default_command(self) -> None:
        command = run_release_gate.default_adapter_command()
        self.assertIn("tigerkit_host_adapter.py", command)
        self.assertTrue(run_release_gate.BUILTIN_ADAPTER.is_file())

    def test_live_gate_uses_ordered_fallback_and_stops_after_first_pass(self) -> None:
        outcomes = {
            "codex": ([], [], "codex unavailable"),
            "claude-code": ([{"host": "claude-code"}], [], None),
        }

        def fake_run_one_host(host: str, *args: object, **kwargs: object):
            return outcomes[host]

        with patch.object(run_release_gate, "run_one_host", side_effect=fake_run_one_host) as run:
            records, hosts, selected = run_release_gate.run_live_gate(
                Path("."),
                {},
                None,
                adapter_command="adapter",
                manifest={"runs": 2, "behavior_cases": [], "catalog_cases": []},
            )

        self.assertEqual(selected, "claude-code")
        self.assertEqual([call.args[0] for call in run.call_args_list], ["codex", "claude-code"])
        self.assertEqual(records, [{"host": "claude-code"}])
        self.assertEqual(
            [(row["host"], row["status"]) for row in hosts],
            [("codex", "unavailable"), ("claude-code", "passed"), ("hermes-agent", "not-run")],
        )

    def test_live_gate_all_failed_remains_advisory(self) -> None:
        def fake_run_one_host(host: str, *args: object, **kwargs: object):
            return [], [f"{host} failed"], None

        with patch.object(run_release_gate, "run_one_host", side_effect=fake_run_one_host):
            _, hosts, selected = run_release_gate.run_live_gate(
                Path("."),
                {},
                None,
                adapter_command="adapter",
                manifest={"runs": 2, "behavior_cases": [], "catalog_cases": []},
            )
        self.assertIsNone(selected)
        self.assertTrue(all(row["status"] == "failed" for row in hosts))


if __name__ == "__main__":
    unittest.main()
