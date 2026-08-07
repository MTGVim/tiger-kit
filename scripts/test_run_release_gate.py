#!/usr/bin/env python3
from __future__ import annotations

import unittest
from unittest.mock import patch

import run_release_gate
from run_skill_evals import load_catalog_contract, load_eval_contracts


class ReleaseGateContractTest(unittest.TestCase):
    def test_release_gate_rejects_dirty_worktree(self) -> None:
        completed = run_release_gate.subprocess.CompletedProcess(
            args=["git", "status"], returncode=0, stdout=" M README.md\n", stderr=""
        )
        with patch.object(run_release_gate.subprocess, "run", return_value=completed):
            with self.assertRaisesRegex(ValueError, "clean worktree"):
                run_release_gate.ensure_clean_worktree()

    def test_manifest_is_closed_and_references_existing_cases(self) -> None:
        manifest = run_release_gate.load_manifest()
        contracts = load_eval_contracts(run_release_gate.ROOT, None)
        catalog = load_catalog_contract(run_release_gate.ROOT)
        self.assertEqual(run_release_gate.validate_manifest_cases(contracts, catalog, manifest), [])


if __name__ == "__main__":
    unittest.main()
