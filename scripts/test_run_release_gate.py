#!/usr/bin/env python3
from __future__ import annotations

import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

import run_release_gate
from run_skill_evals import load_catalog_contract, load_eval_contracts


class ReleaseGateContractTest(unittest.TestCase):
    def test_release_gate_rejects_non_portable_absolute_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            artifact = root / "skills/tk-example/SKILL.md"
            artifact.parent.mkdir(parents=True)
            artifact.write_text("path = /" + "home/alice/private-app\n", encoding="utf-8")
            errors = run_release_gate.validate_portable_artifacts(root)
        self.assertTrue(any("non-portable absolute path" in error for error in errors))

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

    def test_ledger_cases_check_existence_and_korean_prose(self) -> None:
        contracts = load_eval_contracts(run_release_gate.ROOT, None)
        errors, coverage = run_release_gate.validate_ledger_eval_coverage(contracts)
        self.assertEqual(errors, [])
        self.assertTrue(coverage)
        self.assertTrue(all(row["hangul_assertions"] for row in coverage.values()))
        self.assertTrue(all(row["korean_prose_assertions"] for row in coverage.values()))

        missing = {
            "tk-example": {
                "behavior": {
                    "evals": [
                        {
                            "id": "writes-ledger",
                            "assertions": [
                                {"type": "path_exists", "path": ".tigerkit/example.md"}
                            ],
                        }
                    ]
                }
            }
        }
        missing_errors, _ = run_release_gate.validate_ledger_eval_coverage(missing)
        self.assertTrue(any("writes-ledger" in error for error in missing_errors))
        self.assertTrue(any("path_text_has_hangul" in error for error in missing_errors))

        missing_prose = {
            "tk-example": {
                "behavior": {
                    "evals": [
                        {
                            "id": "writes-ledger",
                            "assertions": [
                                {"type": "path_exists", "path": ".tigerkit/example.md"},
                                {
                                    "type": "path_text_has_hangul",
                                    "path": ".tigerkit/example.md",
                                },
                            ],
                        }
                    ]
                }
            }
        }
        prose_errors, _ = run_release_gate.validate_ledger_eval_coverage(missing_prose)
        self.assertTrue(any("path_text_has_korean_prose" in error for error in prose_errors))

    def test_language_regression_rejects_new_violation(self) -> None:
        baseline = {"files": 1, "violations": []}
        candidate = {
            "files": 1,
            "violations": [
                {
                    "fingerprint": "AGENTS.md|new English prose",
                    "location": "AGENTS.md:1",
                    "words": ["English", "prose"],
                }
            ],
        }
        errors = run_release_gate.compare_language_regression(baseline, candidate)
        self.assertGreaterEqual(len(errors), 2)
        self.assertTrue(any("new English prose" in error for error in errors))

    def test_language_regression_rejects_duplicate_existing_violation(self) -> None:
        row_a = {"fingerprint": "AGENTS.md|A", "location": "AGENTS.md:1"}
        row_b = {"fingerprint": "AGENTS.md|B", "location": "AGENTS.md:2"}
        errors = run_release_gate.compare_language_regression(
            {"violations": [row_a, row_b]},
            {"violations": [row_b, row_b]},
        )
        self.assertTrue(any("duplicated" in error for error in errors))

    def test_language_regression_ignores_json_index_shift(self) -> None:
        baseline = {
            "violations": [
                {
                    "fingerprint": "skills/tk-example/evals/evals.json.evals[].prompt|English prose",
                    "location": "skills/tk-example/evals/evals.json.evals[0].prompt:1",
                }
            ]
        }
        candidate = {
            "violations": [
                {
                    "fingerprint": "skills/tk-example/evals/evals.json.evals[].prompt|English prose",
                    "location": "skills/tk-example/evals/evals.json.evals[4].prompt:1",
                }
            ]
        }
        self.assertEqual(run_release_gate.compare_language_regression(baseline, candidate), [])

    def test_language_regression_allows_translation_with_less_english(self) -> None:
        baseline = {
            "violations": [
                {
                    "fingerprint": "AGENTS.md|English prose remains",
                    "location": "AGENTS.md:1",
                    "words": ["English", "prose", "remains"],
                }
            ]
        }
        candidate = {
            "violations": [
                {
                    "fingerprint": "AGENTS.md|한국어 prose",
                    "location": "AGENTS.md:1",
                    "words": ["prose"],
                }
            ]
        }
        self.assertEqual(run_release_gate.compare_language_regression(baseline, candidate), [])

    def test_language_scan_ignores_literals_but_flags_prose(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "AGENTS.md").write_text(
                "argument-hint: \"[--recover-publication] [--repo owner/name]...\"\n한국어 설명\n\n`keep exact command`\n\n```text\nEnglish code sample\n```\n\nNew English sentence\n",
                encoding="utf-8",
            )
            evals = root / "skills/tk-example/evals"
            evals.mkdir(parents=True)
            (evals / "evals.json").write_text(
                '{"evals":[{"assertions":[{"type":"judge","criterion":"English criterion"},{"type":"path_text_contains","text":"English literal"}]}]}',
                encoding="utf-8",
            )
            agents = root / "skills/tk-example/agents"
            agents.mkdir(parents=True)
            (agents / "openai.yaml").write_text(
                "name: tk-example\ndescription: 한국어 설명\ndisable-model-invocation: false\nkind: hybrid\nrelationship: native\ntrigger: user-invoked\nsource: tigerkit\n",
                encoding="utf-8",
            )
            (root / "skills/tk-example/SKILL.md").write_text(
                "# English model-facing contract\nAlways verify the current head before publication.\n",
                encoding="utf-8",
            )
            report = run_release_gate.scan_language(root)
        self.assertEqual(report["files"], 4)
        rows = report["violations"]
        self.assertEqual(len(rows), 2)
        self.assertTrue(any("New English sentence" in row["fingerprint"] for row in rows))
        self.assertTrue(any("English criterion" in row["fingerprint"] for row in rows))


if __name__ == "__main__":
    unittest.main()
