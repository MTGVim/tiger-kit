#!/usr/bin/env python3
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

if __package__:
    from scripts.run_skill_evals import (
        build_verdict,
        compare_catalog_contracts,
        compare_eval_contracts,
        evaluate_checkout,
        summarize_trigger_outcomes,
        validate_adapter_result,
        validate_case_filter,
        verify_mechanical_assertion,
    )
else:
    from run_skill_evals import (
        build_verdict,
        compare_catalog_contracts,
        compare_eval_contracts,
        evaluate_checkout,
        summarize_trigger_outcomes,
        validate_adapter_result,
        validate_case_filter,
        verify_mechanical_assertion,
    )


class AdapterResultTest(unittest.TestCase):
    def test_requires_skill_loaded_and_output(self) -> None:
        self.assertEqual(
            validate_adapter_result(
                {"skill_loaded": True, "output": "ok", "terminal_status": "Pass"}
            ),
            [],
        )
        self.assertEqual(
            validate_adapter_result({"output": "ok"}),
            [
                "adapter result requires boolean skill_loaded or string-list loaded_skills",
                "adapter result terminal_status must be one of Blocked, Fail, "
                "NotApplicable, Pass, Pending, Unverifiable",
            ],
        )

    def test_accepts_catalog_selection_metadata(self) -> None:
        self.assertEqual(
            validate_adapter_result(
                {
                    "loaded_skills": ["tk-drive"],
                    "selected_skill": "tk-drive",
                    "output": "ok",
                    "terminal_status": "Pass",
                }
            ),
            [],
        )

    def test_rejects_artifact_disposition_as_terminal_status(self) -> None:
        errors = validate_adapter_result(
            {
                "skill_loaded": True,
                "output": "ok",
                "terminal_status": "applied",
            }
        )

        self.assertTrue(any("terminal_status must be one of" in error for error in errors))


class VerdictTest(unittest.TestCase):
    def test_candidate_regression_fails(self) -> None:
        baseline = {
            "trigger_accuracy": 0.9,
            "behavior_pass_rate": 0.8,
            "total_tokens": 10,
            "duration_ms": 10,
        }
        candidate = {
            "trigger_accuracy": 0.8,
            "behavior_pass_rate": 0.8,
            "safety_failures": 0,
            "total_tokens": 10,
            "duration_ms": 10,
        }

        self.assertEqual(build_verdict(baseline, candidate)["status"], "Fail")

    def test_candidate_safety_failure_fails(self) -> None:
        baseline = {
            "trigger_accuracy": 0.5,
            "behavior_pass_rate": 0.5,
            "total_tokens": 10,
            "duration_ms": 10,
        }
        candidate = {
            "trigger_accuracy": 1.0,
            "behavior_pass_rate": 1.0,
            "safety_failures": 1,
            "total_tokens": 10,
            "duration_ms": 10,
        }

        self.assertEqual(build_verdict(baseline, candidate)["status"], "Fail")

    def test_non_regressing_candidate_passes(self) -> None:
        baseline = {
            "trigger_accuracy": 0.5,
            "behavior_pass_rate": 0.5,
            "total_tokens": 10,
            "duration_ms": 10,
        }
        candidate = {
            "trigger_accuracy": 0.75,
            "behavior_pass_rate": 0.75,
            "safety_failures": 0,
            "total_tokens": 10,
            "duration_ms": 10,
        }

        self.assertEqual(build_verdict(baseline, candidate)["status"], "Pass")

    def test_unjustified_resource_regression_fails(self) -> None:
        baseline = {
            "trigger_accuracy": 1.0,
            "behavior_pass_rate": 1.0,
            "total_tokens": 100,
            "duration_ms": 100,
        }
        candidate = {
            "trigger_accuracy": 1.0,
            "behavior_pass_rate": 1.0,
            "safety_failures": 0,
            "total_tokens": 126,
            "duration_ms": 100,
        }

        self.assertEqual(build_verdict(baseline, candidate)["status"], "Fail")
        self.assertEqual(
            build_verdict(
                baseline,
                candidate,
                resource_regression_reason="Expected richer evidence",
            )["status"],
            "Pass",
        )

    def test_missing_token_comparison_is_unverifiable(self) -> None:
        baseline = {
            "trigger_accuracy": 1.0,
            "behavior_pass_rate": 1.0,
            "total_tokens": None,
            "duration_ms": 100,
        }
        candidate = {
            "trigger_accuracy": 1.0,
            "behavior_pass_rate": 1.0,
            "safety_failures": 0,
            "total_tokens": None,
            "duration_ms": 100,
        }

        self.assertEqual(build_verdict(baseline, candidate)["status"], "Unverifiable")

    def test_validation_regression_is_gated_per_invocation_kind(self) -> None:
        baseline = {
            "trigger_metrics": {
                "hybrid": {
                    "validation": {"accuracy": 1.0, "precision": 1.0, "recall": 1.0}
                },
                "user-invoked": {
                    "validation": {"accuracy": 1.0, "precision": 1.0, "recall": 1.0}
                },
            },
            "behavior_pass_rate": 1.0,
            "total_tokens": 100,
            "duration_ms": 100,
        }
        candidate = {
            "trigger_metrics": {
                "hybrid": {
                    "validation": {"accuracy": 0.9, "precision": 1.0, "recall": 0.8}
                },
                "user-invoked": {
                    "validation": {"accuracy": 1.0, "precision": 1.0, "recall": 1.0}
                },
            },
            "behavior_pass_rate": 1.0,
            "safety_failures": 0,
            "total_tokens": 100,
            "duration_ms": 100,
        }

        verdict = build_verdict(baseline, candidate)

        self.assertEqual(verdict["status"], "Fail")
        self.assertTrue(any("hybrid" in reason for reason in verdict["reasons"]))


class TriggerMetricTest(unittest.TestCase):
    def test_separates_invocation_kinds_and_reports_run_variance(self) -> None:
        outcomes = {
            ("hybrid", "validation", "tk-auto:trigger:positive"): {
                "expected": True,
                "values": [True, False],
            },
            ("hybrid", "validation", "tk-auto:trigger:negative"): {
                "expected": False,
                "values": [False, False],
            },
            ("user-invoked", "validation", "tk-user:trigger:explicit"): {
                "expected": True,
                "values": [True, True],
            },
        }

        metrics, case_metrics = summarize_trigger_outcomes(outcomes)

        self.assertEqual(metrics["hybrid"]["validation"]["precision"], 1.0)
        self.assertEqual(metrics["hybrid"]["validation"]["recall"], 0.5)
        self.assertEqual(metrics["user-invoked"]["validation"]["recall"], 1.0)
        positive = next(row for row in case_metrics if row["case"].endswith("positive"))
        self.assertEqual(positive["run_variance"], 0.25)


class RunnerContractTest(unittest.TestCase):
    def behavior(self, case_id: str, terminal: dict[str, object]) -> dict[str, object]:
        return {
            "id": case_id,
            "assertions": [
                terminal,
                {"type": "git_head_unchanged"},
            ],
        }

    def contract(
        self, cases: list[dict[str, object]], *, safety: bool = False
    ) -> dict[str, dict[str, object]]:
        if safety:
            cases[0]["safety"] = True
        return {
            "tk-sample": {
                "triggers": {
                    "queries": [
                        {"id": "trigger", "should_trigger": True},
                    ]
                },
                "behavior": {"evals": cases},
            }
        }

    def test_contract_drift_rejects_deleted_or_weakened_cases(self) -> None:
        baseline = self.contract(
            [
                self.behavior(
                    "safe",
                    {"type": "terminal_status", "allowed": ["Pass", "Blocked"]},
                )
            ],
            safety=True,
        )
        candidate = self.contract(
            [
                self.behavior(
                    "other",
                    {"type": "terminal_status", "expected": "Pass"},
                )
            ]
        )

        errors = compare_eval_contracts(baseline, candidate)

        self.assertTrue(any("deleted" in error for error in errors))

    def test_contract_drift_accepts_stronger_terminal_and_new_cases(self) -> None:
        baseline = self.contract(
            [
                self.behavior(
                    "safe",
                    {"type": "terminal_status", "allowed": ["Pass", "Blocked"]},
                )
            ]
        )
        candidate = self.contract(
            [
                self.behavior(
                    "safe",
                    {"type": "terminal_status", "expected": "Pass"},
                ),
                self.behavior(
                    "new",
                    {"type": "terminal_status", "expected": "Blocked"},
                ),
            ]
        )

        self.assertEqual(compare_eval_contracts(baseline, candidate), [])

    def test_catalog_contract_drift_rejects_deleted_critical_case(self) -> None:
        baseline = {
            "critical_hosts": ["claude-code", "codex", "hermes-agent"],
            "cases": [
                {
                    "id": "critical",
                    "expected_selected_skill": "tk-drive",
                    "critical": True,
                }
            ],
        }
        candidate = {
            "critical_hosts": ["codex", "hermes-agent"],
            "cases": [],
        }

        errors = compare_catalog_contracts(baseline, candidate)

        self.assertTrue(any("deleted case" in error for error in errors))
        self.assertTrue(any("critical host" in error for error in errors))

    def test_content_path_and_diff_assertions_are_mechanical(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            checkout = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=checkout, check=True)
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                cwd=checkout,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test"],
                cwd=checkout,
                check=True,
            )
            target = checkout / "message.txt"
            target.write_text("before\n", encoding="utf-8")
            subprocess.run(["git", "add", "message.txt"], cwd=checkout, check=True)
            subprocess.run(["git", "commit", "-qm", "initial"], cwd=checkout, check=True)
            initial_head = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=checkout,
                text=True,
                capture_output=True,
                check=True,
            ).stdout.strip()
            target.write_text("authorized change\n", encoding="utf-8")

            rows = [
                verify_mechanical_assertion(
                    {"type": "output_contains", "text": "literal"},
                    adapter_result={"output": "exact literal", "terminal_status": "Pass"},
                    checkout=checkout,
                    initial_head=initial_head,
                ),
                verify_mechanical_assertion(
                    {
                        "type": "path_text_contains",
                        "path": "message.txt",
                        "text": "authorized change",
                    },
                    adapter_result={"output": "", "terminal_status": "Pass"},
                    checkout=checkout,
                    initial_head=initial_head,
                ),
                verify_mechanical_assertion(
                    {"type": "changed_paths_equal", "paths": ["message.txt"]},
                    adapter_result={"output": "", "terminal_status": "Pass"},
                    checkout=checkout,
                    initial_head=initial_head,
                ),
                verify_mechanical_assertion(
                    {"type": "git_diff_contains", "text": "authorized change"},
                    adapter_result={"output": "", "terminal_status": "Pass"},
                    checkout=checkout,
                    initial_head=initial_head,
                ),
            ]

            self.assertTrue(all(row["passed"] for row in rows))

    def test_catalog_routing_uses_selected_skill_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checkout = root / "checkout"
            (checkout / "skills" / "tk-drive").mkdir(parents=True)
            adapter = root / "adapter.py"
            adapter.write_text(
                "import json, os\n"
                "selected = None if 'summary' in os.environ['TK_EVAL_PROMPT'] "
                "else os.environ['TK_EVAL_SKILL']\n"
                "loaded = [] if selected is None else [selected]\n"
                "print(json.dumps({'loaded_skills': loaded, 'selected_skill': selected, "
                "'output': 'catalog', 'terminal_status': 'Pass', 'total_tokens': 1}))\n",
                encoding="utf-8",
            )
            catalog = {
                "cases": [
                    {
                        "id": "explicit",
                        "prompt": "explicit drive",
                        "focus_skill": "tk-drive",
                        "expected_selected_skill": "tk-drive",
                        "critical": True,
                    },
                    {
                        "id": "generic",
                        "prompt": "summary only",
                        "focus_skill": "tk-drive",
                        "expected_selected_skill": None,
                        "critical": True,
                    },
                ]
            }

            summary, records = evaluate_checkout(
                checkout,
                {},
                adapter_command=f"python3 {adapter}",
                grader_command="unused",
                host="codex",
                runs=1,
                case_filter=None,
                catalog_contract=catalog,
            )

            self.assertEqual(summary["routing_pass_rate"], 1.0)
            self.assertTrue(all(record["passed"] for record in records))

    def test_rejects_unknown_case_filter(self) -> None:
        contracts = {
            "tk-sample": {
                "triggers": {"queries": [{"id": "known"}]},
                "behavior": {"evals": [{"id": "known"}]},
            }
        }

        self.assertEqual(
            validate_case_filter(contracts, {"tk-sample:behavior:missing"}),
            ["unknown eval case: tk-sample:behavior:missing"],
        )

    def test_fake_adapter_keeps_baseline_and_candidate_outputs_separate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            baseline = root / "baseline"
            candidate = root / "candidate"
            for checkout, content in ((baseline, "baseline"), (candidate, "candidate")):
                skill = checkout / "skills" / "tk-sample"
                skill.mkdir(parents=True)
                (skill / "SKILL.md").write_text(content, encoding="utf-8")
            adapter = root / "adapter.py"
            adapter.write_text(
                "import json, os\n"
                "from pathlib import Path\n"
                "output = Path(os.environ['TK_EVAL_SKILL_DIR'], 'SKILL.md').read_text()\n"
                "print(json.dumps({'skill_loaded': True, 'output': output, "
                "'terminal_status': 'Pass', 'total_tokens': 1, "
                "'host': os.environ['TK_EVAL_HOST']}))\n",
                encoding="utf-8",
            )
            grader = root / "grader.py"
            grader.write_text(
                "import json, os\n"
                "assertions = json.loads(os.environ['TK_EVAL_ASSERTIONS'])\n"
                "output = os.environ['TK_EVAL_OUTPUT']\n"
                "print(json.dumps({'assertion_results': ["
                "{'passed': True, 'evidence': output} for _ in assertions]}))\n",
                encoding="utf-8",
            )
            contracts = {
                "tk-sample": {
                    "triggers": {"kind": "user-invoked", "queries": []},
                    "behavior": {
                        "evals": [
                            {
                                "id": "output",
                                "prompt": "run",
                                "assertions": [
                                    {
                                        "type": "judge",
                                        "criterion": "reports checkout marker",
                                    }
                                ],
                            }
                        ]
                    },
                }
            }
            command = f"python3 {adapter}"
            grader_command = f"python3 {grader}"

            _, baseline_records = evaluate_checkout(
                baseline,
                contracts,
                adapter_command=command,
                grader_command=grader_command,
                host="fake-host",
                runs=1,
                case_filter=None,
            )
            _, candidate_records = evaluate_checkout(
                candidate,
                contracts,
                adapter_command=command,
                grader_command=grader_command,
                host="fake-host",
                runs=1,
                case_filter=None,
            )

            self.assertEqual(
                baseline_records[0]["assertion_results"][0]["evidence"], "baseline"
            )
            self.assertEqual(
                candidate_records[0]["assertion_results"][0]["evidence"], "candidate"
            )
            self.assertEqual(baseline_records[0]["total_tokens"], 1)


if __name__ == "__main__":
    unittest.main()
