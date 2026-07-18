#!/usr/bin/env python3
import json
import tempfile
import unittest
from pathlib import Path

from run_skill_evals import (
    build_verdict,
    evaluate_checkout,
    summarize_trigger_outcomes,
    validate_adapter_result,
    validate_case_filter,
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
                "adapter result requires boolean skill_loaded",
                "adapter result requires non-empty string terminal_status",
            ],
        )


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
