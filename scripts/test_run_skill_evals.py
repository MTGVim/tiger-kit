#!/usr/bin/env python3
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

if __package__:
    from scripts.run_skill_evals import (
        DIAGNOSTIC_MARKER_END,
        DIAGNOSTIC_MARKER_START,
        build_verdict,
        build_diagnostic_ledger,
        compare_catalog_contracts,
        compare_diagnostics,
        compare_eval_contracts,
        compose_diagnostic_prompt,
        evaluate_diagnostic_checkout,
        evaluate_checkout,
        parse_diagnostic_output,
        summarize_diagnostic_records,
        summarize_trigger_outcomes,
        validate_adapter_result,
        validate_case_filter,
        verify_mechanical_assertion,
    )
else:
    from run_skill_evals import (
        DIAGNOSTIC_MARKER_END,
        DIAGNOSTIC_MARKER_START,
        build_verdict,
        build_diagnostic_ledger,
        compare_catalog_contracts,
        compare_diagnostics,
        compare_eval_contracts,
        compose_diagnostic_prompt,
        evaluate_diagnostic_checkout,
        evaluate_checkout,
        parse_diagnostic_output,
        summarize_diagnostic_records,
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

    def test_diagnostic_only_metrics_do_not_change_normal_adapter_contract(self) -> None:
        result = {
            "skill_loaded": True,
            "output": "ok",
            "terminal_status": "Pass",
            "tool_uses": "legacy-extra-field",
        }

        self.assertEqual(validate_adapter_result(result), [])
        self.assertIn(
            "adapter result tool_uses must be numeric or null",
            validate_adapter_result(result, diagnostic=True),
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

    def test_accepts_optional_ordered_events_and_rejects_malformed_events(self) -> None:
        result = {
            "skill_loaded": True,
            "output": "done",
            "terminal_status": "Pass",
            "events": [
                {"type": "phase_invocation", "phase": "tk-to-spec"},
                {"type": "phase_invocation", "phase": "tk-to-spec"},
                {"type": "phase_invocation", "phase": "tk-implement"},
                {"type": "final_output", "terminal_status": "Pass"},
            ],
        }

        self.assertEqual(validate_adapter_result(result), [])

        for events in (
            [],
            ["unknown"],
            [{"type": "phase_invocation"}],
            [
                {
                    "type": "unknown",
                    "phase": "tk-to-spec",
                },
                {"type": "final_output", "terminal_status": "Pass"},
            ],
            [{"type": "final_output", "terminal_status": "applied"}],
            [{"type": "unknown"}],
        ):
            malformed = dict(result)
            malformed["events"] = events
            with self.subTest(events=events):
                self.assertTrue(
                    any(
                        "adapter result events" in error
                        for error in validate_adapter_result(malformed)
                    )
                )
        mismatch = dict(result)
        mismatch["terminal_status"] = "Blocked"
        self.assertTrue(
            any(
                "final_output terminal_status must match" in error
                for error in validate_adapter_result(mismatch)
            )
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


class DiagnosticRunnerTest(unittest.TestCase):
    def payload(
        self,
        *,
        phase: str = "ok",
        points: list[dict[str, str]] | None = None,
        fill_ins: list[str] | None = None,
        retries: int = 0,
    ) -> dict[str, object]:
        return {
            "trace": {
                "understanding": phase,
                "planning": "ok",
                "execution": "ok",
                "formatting": "ok",
            },
            "unclear_points": points or [],
            "discretionary_fill_ins": fill_ins or [],
            "retries": retries,
        }

    def marked(self, payload: dict[str, object], deliverable: str = "deliverable") -> str:
        return (
            deliverable
            + "\n"
            + DIAGNOSTIC_MARKER_START
            + "\n```json\n"
            + json.dumps(payload)
            + "\n```\n"
            + DIAGNOSTIC_MARKER_END
        )

    def record(
        self,
        payload: dict[str, object] | None,
        *,
        case: str = "tk-sample:behavior:incident",
        normal_passed: bool = True,
        safety: bool = False,
        role: str = "incident",
        parse_error: str | None = None,
        tokens: int = 10,
    ) -> dict[str, object]:
        return {
            "case": case,
            "host": "codex",
            "scenario_role": role,
            "normal_passed": normal_passed,
            "safety": safety,
            "diagnostic": payload,
            "parse_error": parse_error,
            "total_tokens": tokens,
            "duration_ms": 10,
            "tool_uses": 1,
            "nested_calls": 0,
        }

    def test_parses_marker_json_and_keeps_deliverable_separate(self) -> None:
        deliverable, payload, error = parse_diagnostic_output(
            self.marked(self.payload(), "normal result")
        )

        self.assertEqual(deliverable, "normal result")
        self.assertEqual(payload, self.payload())
        self.assertIsNone(error)

    def test_missing_and_malformed_diagnostics_are_parse_errors(self) -> None:
        _, missing, missing_error = parse_diagnostic_output("normal result")
        malformed = (
            "normal\n"
            + DIAGNOSTIC_MARKER_START
            + "\n{bad json}\n"
            + DIAGNOSTIC_MARKER_END
        )
        _, invalid, invalid_error = parse_diagnostic_output(malformed)

        self.assertIsNone(missing)
        self.assertIn("markers", str(missing_error))
        self.assertIsNone(invalid)
        self.assertIn("malformed", str(invalid_error))

    def test_repeated_diagnostic_markers_do_not_pollute_deliverable(self) -> None:
        output = (
            "normal result\n"
            + DIAGNOSTIC_MARKER_START
            + "\n{}\n"
            + DIAGNOSTIC_MARKER_START
            + "\n{}\n"
            + DIAGNOSTIC_MARKER_END
        )

        deliverable, payload, error = parse_diagnostic_output(output)

        self.assertEqual(deliverable, "normal result")
        self.assertIsNone(payload)
        self.assertIn("repeated", str(error))

    def test_rejects_noncanonical_diagnostic_fields(self) -> None:
        payload = self.payload()
        payload["unexpected"] = "value"

        _, parsed, error = parse_diagnostic_output(self.marked(payload))

        self.assertIsNone(parsed)
        self.assertIn("canonical fields", str(error))

    def test_prompt_composition_does_not_add_case_expectations(self) -> None:
        prompt = compose_diagnostic_prompt("incident prompt", "diagnostic suffix")

        self.assertIn("incident prompt", prompt)
        self.assertIn("diagnostic suffix", prompt)
        self.assertNotIn("SECRET_EXPECTED_OUTPUT", prompt)
        self.assertNotIn("SECRET_ASSERTION_ANSWER", prompt)

    def test_repeated_and_one_off_unclear_points_are_separate(self) -> None:
        repeated = {
            "issue": "loop",
            "cause": "missing blocker key",
            "general_fix_rule": "fingerprint blockers",
        }
        one_off = {
            "issue": "wording",
            "cause": "rare alias",
            "general_fix_rule": "name the alias",
        }
        records = [
            self.record(self.payload(points=[repeated, one_off])),
            self.record(self.payload(points=[repeated])),
        ]

        summary = summarize_diagnostic_records(records)

        self.assertEqual(len(summary["new_unclear_points"]), 2)
        self.assertEqual(len(summary["repeated_unclear_points"]), 1)
        self.assertEqual(summary["status"], "Concern")

    def test_critical_and_holdout_regressions_beat_resource_savings(self) -> None:
        baseline = summarize_diagnostic_records(
            [self.record(self.payload(), tokens=100), self.record(self.payload(), tokens=100)]
        )
        candidate = summarize_diagnostic_records(
            [
                self.record(
                    self.payload(),
                    case="tk-sample:behavior:holdout",
                    normal_passed=False,
                    role="holdout",
                    tokens=10,
                )
            ]
        )

        verdict = compare_diagnostics(baseline, candidate)

        self.assertEqual(verdict["status"], "Fail")
        self.assertTrue(any("holdout" in reason for reason in verdict["reasons"]))

    def test_repeated_new_phase_and_retry_regression_fail(self) -> None:
        baseline = summarize_diagnostic_records(
            [self.record(self.payload()), self.record(self.payload())]
        )
        candidate = summarize_diagnostic_records(
            [
                self.record(self.payload(phase="stuck", retries=1)),
                self.record(self.payload(phase="stuck", retries=1)),
            ]
        )

        verdict = compare_diagnostics(baseline, candidate)

        self.assertEqual(verdict["status"], "Fail")
        self.assertTrue(verdict["phase_regressions"])
        self.assertTrue(verdict["retry_regressions"])

    def test_one_off_phase_retry_and_parse_regressions_are_concerns(self) -> None:
        baseline = summarize_diagnostic_records(
            [self.record(self.payload()), self.record(self.payload())]
        )
        candidate = summarize_diagnostic_records(
            [
                self.record(self.payload(phase="stuck", retries=1)),
                self.record(None, parse_error="missing diagnostic markers"),
            ]
        )

        verdict = compare_diagnostics(baseline, candidate)

        self.assertEqual(verdict["status"], "Concern")
        self.assertTrue(any("one-off new" in item for item in verdict["concerns"]))
        self.assertTrue(any("one-off retry" in item for item in verdict["concerns"]))
        self.assertTrue(any("malformed" in item for item in verdict["concerns"]))

    def test_evaluate_diagnostics_keeps_metrics_out_of_normal_summary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checkout = root / "checkout"
            (checkout / "skills" / "tk-sample").mkdir(parents=True)
            adapter = root / "adapter.py"
            payload = json.dumps(self.payload())
            adapter.write_text(
                "import json\n"
                f"marker = {self.marked(self.payload(), 'normal').__repr__()}\n"
                "print(json.dumps({'skill_loaded': True, 'output': marker, "
                "'terminal_status': 'Pass', 'total_tokens': 7, "
                "'tool_uses': 2, 'nested_calls': 0}))\n",
                encoding="utf-8",
            )
            contracts = {
                "tk-sample": {
                    "triggers": {"kind": "hybrid", "queries": []},
                    "behavior": {
                        "evals": [
                            {
                                "id": "incident",
                                "prompt": "run incident",
                                "assertions": [
                                    {"type": "terminal_status", "expected": "Pass"}
                                ],
                            }
                        ]
                    },
                }
            }

            diagnostic, records = evaluate_diagnostic_checkout(
                checkout,
                contracts,
                adapter_command=f"python3 {adapter}",
                grader_command="unused",
                host="codex",
                runs=2,
                case_filter=None,
                scenario_limit=1,
                suffix="diagnostic suffix",
            )

            self.assertEqual(diagnostic["status"], "Pass")
            self.assertEqual(diagnostic["resource_metrics"]["total_tokens"], 14.0)
            self.assertTrue(diagnostic["minimum_trials_met"])
            self.assertEqual(len(records), 2)

    def test_resource_comparison_requires_two_matched_trials(self) -> None:
        baseline = summarize_diagnostic_records([self.record(self.payload())])
        candidate = summarize_diagnostic_records([self.record(self.payload(), tokens=1)])

        verdict = compare_diagnostics(baseline, candidate)

        self.assertEqual(verdict["resource_comparison_status"], "Unverifiable")
        self.assertFalse(
            any("total_tokens" in concern for concern in verdict["concerns"])
        )

    def test_available_tool_regression_is_reported_after_matched_trials(self) -> None:
        baseline_records = [
            self.record(self.payload()),
            self.record(self.payload()),
        ]
        candidate_records = [
            self.record(self.payload()),
            self.record(self.payload()),
        ]
        for record in baseline_records:
            record["tool_uses"] = 0
        for record in candidate_records:
            record["tool_uses"] = 2

        verdict = compare_diagnostics(
            summarize_diagnostic_records(baseline_records),
            summarize_diagnostic_records(candidate_records),
        )

        self.assertEqual(verdict["resource_comparison_status"], "verified")
        self.assertTrue(
            any("tool_uses" in concern for concern in verdict["concerns"])
        )

    def test_diagnostic_ledger_separates_baseline_and_candidate_counts(self) -> None:
        point = {
            "issue": "loop",
            "cause": "missing key",
            "general_fix_rule": "fingerprint blockers",
        }
        records = [
            {"ref": "baseline", "diagnostic": self.payload(points=[point])},
            {"ref": "candidate", "diagnostic": self.payload(points=[point])},
            {"ref": "candidate", "diagnostic": self.payload(points=[point])},
        ]

        ledger = build_diagnostic_ledger(records)
        entry = ledger["entries"][0]

        self.assertEqual(entry["baseline_seen"], 1)
        self.assertEqual(entry["candidate_seen"], 2)

    def test_dry_run_schema_changes_only_when_diagnose_is_enabled(self) -> None:
        script = Path(__file__).resolve().parent / "run_skill_evals.py"
        root = script.parent.parent
        base = [
            "python3",
            str(script),
            "--baseline",
            "HEAD",
            "--candidate",
            "HEAD",
            "--host",
            "codex",
            "--dry-run",
        ]
        normal = json.loads(
            subprocess.run(
                base,
                cwd=root,
                text=True,
                capture_output=True,
                check=True,
            ).stdout
        )
        diagnostic = json.loads(
            subprocess.run(
                [*base, "--runs", "1", "--diagnose"],
                cwd=root,
                text=True,
                capture_output=True,
                check=True,
            ).stdout
        )

        self.assertNotIn("diagnostics", normal["plan"])
        self.assertEqual(diagnostic["plan"]["diagnostics"]["enabled"], True)
        self.assertEqual(diagnostic["plan"]["diagnostics"]["runs"], 2)

    def test_live_diagnostic_run_writes_separate_record_files(self) -> None:
        script = Path(__file__).resolve().parent / "run_skill_evals.py"
        repository = script.parent.parent
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            adapter = root / "adapter.py"
            grader = root / "grader.py"
            output = root / "output"
            diagnostic_payload = json.dumps(self.payload())
            adapter.write_text(
                "import json, os\n"
                "mode = os.environ['TK_EVAL_MODE']\n"
                "output = 'normal deliverable'\n"
                "if mode == 'diagnostic':\n"
                f"    output += '\\n{DIAGNOSTIC_MARKER_START}\\n'\n"
                f"    output += {diagnostic_payload!r}\n"
                f"    output += '\\n{DIAGNOSTIC_MARKER_END}'\n"
                "print(json.dumps({\n"
                "    'skill_loaded': True,\n"
                "    'output': output,\n"
                "    'terminal_status': 'Pending',\n"
                "    'total_tokens': 7 if mode == 'diagnostic' else 3,\n"
                "    'duration_ms': 11 if mode == 'diagnostic' else 5,\n"
                "    'tool_uses': 1,\n"
                "    'nested_calls': 0,\n"
                "}))\n",
                encoding="utf-8",
            )
            grader.write_text(
                "import json, os\n"
                "assertions = json.loads(os.environ['TK_EVAL_ASSERTIONS'])\n"
                "print(json.dumps({'assertion_results': [\n"
                "    {'passed': True, 'evidence': 'integration fixture'}\n"
                "    for _ in assertions\n"
                "]}))\n",
                encoding="utf-8",
            )
            completed = subprocess.run(
                [
                    "python3",
                    str(script),
                    "--baseline",
                    "HEAD",
                    "--candidate",
                    "HEAD",
                    "--host",
                    "codex",
                    "--runs",
                    "2",
                    "--skill",
                    "tk-reflect",
                    "--case",
                    "tk-reflect:behavior:legacy-1",
                    "--adapter-command",
                    f"python3 {adapter}",
                    "--grader-command",
                    f"python3 {grader}",
                    "--diagnose",
                    "--diagnostic-scenario-limit",
                    "1",
                    "--output",
                    str(output),
                ],
                cwd=repository,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr + completed.stdout)
            expected_files = {
                "baseline-records.json",
                "candidate-records.json",
                "normal-records.json",
                "diagnostic-records.json",
                "diagnostic-ledger.json",
                "summary.json",
            }
            self.assertEqual(
                {path.name for path in output.iterdir()},
                expected_files,
            )
            summary = json.loads((output / "summary.json").read_text(encoding="utf-8"))
            normal = json.loads(
                (output / "normal-records.json").read_text(encoding="utf-8")
            )
            diagnostic = json.loads(
                (output / "diagnostic-records.json").read_text(encoding="utf-8")
            )
            self.assertEqual(summary["diagnostics"]["status"], "Pass")
            self.assertEqual({record["total_tokens"] for record in normal}, {3})
            self.assertEqual({record["total_tokens"] for record in diagnostic}, {7})
            self.assertEqual({record["duration_ms"] for record in normal}, {5})
            self.assertEqual({record["duration_ms"] for record in diagnostic}, {11})
            self.assertEqual(
                {record["ref"] for record in diagnostic},
                {"baseline", "candidate"},
            )

    def test_output_directory_inside_repository_remains_rejected(self) -> None:
        script = Path(__file__).resolve().parent / "run_skill_evals.py"
        repository = script.parent.parent

        completed = subprocess.run(
            [
                "python3",
                str(script),
                "--baseline",
                "HEAD",
                "--candidate",
                "HEAD",
                "--host",
                "codex",
                "--dry-run",
                "--diagnose",
                "--output",
                str(repository / "forbidden-eval-output"),
            ],
            cwd=repository,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("--output must be outside the repository", completed.stderr)


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

    def test_contract_drift_rejects_restricting_an_existing_case_to_fewer_hosts(
        self,
    ) -> None:
        baseline = self.contract(
            [self.behavior("safe", {"type": "terminal_status", "expected": "Pass"})]
        )
        candidate = self.contract(
            [self.behavior("safe", {"type": "terminal_status", "expected": "Pass"})]
        )
        candidate["tk-sample"]["behavior"]["evals"][0]["hosts"] = ["claude-code"]

        errors = compare_eval_contracts(baseline, candidate)

        self.assertTrue(any("restricted host coverage" in error for error in errors))

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

    def test_exact_content_and_commit_count_assertions_are_mechanical(self) -> None:
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
            target = checkout / "canary.txt"
            target.write_text("before\n", encoding="utf-8")
            subprocess.run(["git", "add", "canary.txt"], cwd=checkout, check=True)
            subprocess.run(["git", "commit", "-qm", "initial"], cwd=checkout, check=True)
            initial_head = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=checkout,
                text=True,
                capture_output=True,
                check=True,
            ).stdout.strip()
            target.write_text("ready\n", encoding="utf-8")
            subprocess.run(["git", "add", "canary.txt"], cwd=checkout, check=True)
            subprocess.run(["git", "commit", "-qm", "prepared unit"], cwd=checkout, check=True)

            exact = verify_mechanical_assertion(
                {
                    "type": "path_text_equals",
                    "path": "canary.txt",
                    "text": "ready\n",
                },
                adapter_result={"output": "", "terminal_status": "Pass"},
                checkout=checkout,
                initial_head=initial_head,
            )
            count = verify_mechanical_assertion(
                {"type": "git_commit_count_delta", "expected": 1},
                adapter_result={"output": "", "terminal_status": "Pass"},
                checkout=checkout,
                initial_head=initial_head,
            )
            wrong_count = verify_mechanical_assertion(
                {"type": "git_commit_count_delta", "expected": 2},
                adapter_result={"output": "", "terminal_status": "Pass"},
                checkout=checkout,
                initial_head=initial_head,
            )

            self.assertTrue(exact["passed"])
            self.assertTrue(count["passed"])
            self.assertFalse(wrong_count["passed"])

    def test_event_order_requires_consecutive_phases_without_final_output(self) -> None:
        assertion = {
            "type": "event_order",
            "hosts": ["claude-code"],
            "before": {"type": "phase_invocation", "phase": "tk-to-spec"},
            "after": {"type": "phase_invocation", "phase": "tk-implement"},
            "forbidden_between": [{"type": "final_output"}],
        }
        valid = [
            {"type": "phase_invocation", "phase": "tk-to-spec"},
            {"type": "phase_invocation", "phase": "tk-implement"},
            {"type": "final_output", "terminal_status": "Pass"},
        ]

        with tempfile.TemporaryDirectory() as directory:
            checkout = Path(directory)
            passing = verify_mechanical_assertion(
                assertion,
                adapter_result={"events": valid},
                checkout=checkout,
                initial_head=None,
                host="claude-code",
            )
            skipped = verify_mechanical_assertion(
                assertion,
                adapter_result={},
                checkout=checkout,
                initial_head=None,
                host="codex",
            )
            missing_host = verify_mechanical_assertion(
                assertion,
                adapter_result={"events": valid},
                checkout=checkout,
                initial_head=None,
            )

            failures = []
            for events in (
                None,
                valid[:1],
                [valid[1], valid[0], valid[2]],
                [
                    valid[0],
                    {"type": "final_output", "terminal_status": "Pass"},
                    valid[1],
                    valid[2],
                ],
                [
                    {
                        **valid[0],
                        "phase": "tk-grill-me",
                    },
                    valid[1],
                    valid[2],
                ],
            ):
                adapter_result = {} if events is None else {"events": events}
                failures.append(
                    verify_mechanical_assertion(
                        assertion,
                        adapter_result=adapter_result,
                        checkout=checkout,
                        initial_head=None,
                        host="claude-code",
                    )
                )

        self.assertTrue(passing["passed"])
        self.assertTrue(skipped["passed"])
        self.assertFalse(missing_host["passed"])
        self.assertTrue(all(not row["passed"] for row in failures))

    def test_event_absent_requires_event_evidence_and_honors_host_scope(self) -> None:
        assertion = {
            "type": "event_absent",
            "hosts": ["claude-code"],
            "event": {"type": "phase_invocation", "phase": "tk-implement"},
        }
        without_implementation = [
            {"type": "phase_invocation", "phase": "tk-grill-me"},
            {"type": "final_output", "terminal_status": "Pending"},
        ]
        with_implementation = [
            *without_implementation[:1],
            {"type": "phase_invocation", "phase": "tk-implement"},
            without_implementation[-1],
        ]

        with tempfile.TemporaryDirectory() as directory:
            checkout = Path(directory)
            passing = verify_mechanical_assertion(
                assertion,
                adapter_result={"events": without_implementation},
                checkout=checkout,
                initial_head=None,
                host="claude-code",
            )
            failing = verify_mechanical_assertion(
                assertion,
                adapter_result={"events": with_implementation},
                checkout=checkout,
                initial_head=None,
                host="claude-code",
            )
            missing = verify_mechanical_assertion(
                assertion,
                adapter_result={},
                checkout=checkout,
                initial_head=None,
                host="claude-code",
            )
            skipped = verify_mechanical_assertion(
                assertion,
                adapter_result={},
                checkout=checkout,
                initial_head=None,
                host="codex",
            )

        self.assertTrue(passing["passed"])
        self.assertFalse(failing["passed"])
        self.assertFalse(missing["passed"])
        self.assertTrue(skipped["passed"])

    def test_behavior_records_preserve_adapter_events(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checkout = root / "checkout"
            (checkout / "skills" / "tk-sample").mkdir(parents=True)
            adapter = root / "adapter.py"
            events = [
                {"type": "phase_invocation", "phase": "tk-to-spec"},
                {"type": "phase_invocation", "phase": "tk-implement"},
                {"type": "final_output", "terminal_status": "Pass"},
            ]
            adapter.write_text(
                "import json\n"
                f"events = {events!r}\n"
                "print(json.dumps({'skill_loaded': True, 'output': 'Status: Pass', "
                "'terminal_status': 'Pass', 'total_tokens': 1, 'events': events}))\n",
                encoding="utf-8",
            )
            contracts = {
                "tk-sample": {
                    "triggers": {"kind": "user-invoked", "queries": []},
                    "behavior": {
                        "evals": [
                            {
                                "id": "ordered",
                                "prompt": "run ordered continuation",
                                "assertions": [
                                    {
                                        "type": "event_order",
                                        "before": events[0],
                                        "after": events[1],
                                        "forbidden_between": [
                                            {"type": "final_output"}
                                        ],
                                    },
                                    {
                                        "type": "terminal_status",
                                        "expected": "Pass",
                                    },
                                ],
                            }
                        ]
                    },
                }
            }

            _, records = evaluate_checkout(
                checkout,
                contracts,
                adapter_command=f"python3 {adapter}",
                grader_command="unused",
                host="claude-code",
                runs=1,
                case_filter=None,
            )
            contracts["tk-sample"]["behavior"]["evals"][0]["hosts"] = [
                "claude-code"
            ]
            skipped_summary, skipped_records = evaluate_checkout(
                checkout,
                contracts,
                adapter_command=f"python3 {adapter}",
                grader_command="unused",
                host="codex",
                runs=1,
                case_filter=None,
            )

        self.assertEqual(records[0]["events"], events)
        self.assertEqual(records[0]["terminal_status"], "Pass")
        self.assertEqual(skipped_summary["behavior_runs"], 0)
        self.assertEqual(skipped_records, [])

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
