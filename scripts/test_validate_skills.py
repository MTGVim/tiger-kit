#!/usr/bin/env python3
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

if __package__:
    from scripts.validate_skills import (
        ACTIONABLE_OUTPUT_GATE,
        EXPECTED_SKILLS,
        REQUIRED_BEHAVIOR_CASES,
        RESULT_BUDGET_TOKENS,
        TERMINAL_SUMMARY_GATE,
        USER_INVOKED_SKILLS,
        parse_latest_changelog_version,
        validate_actionable_output_contract,
        validate_local_only_workflows,
        validate_catalog_routing,
        validate_release_alignment,
        validate_release_version_contract,
        validate_response_language_contract,
        validate_runtime_scratch,
        validate_skill_language,
        validate_terminal_summary_contract,
        validate_user_decision_contract,
        validate_skill,
        validate_skill_eval_files,
    )
else:
    from validate_skills import (
        ACTIONABLE_OUTPUT_GATE,
        EXPECTED_SKILLS,
        REQUIRED_BEHAVIOR_CASES,
        RESULT_BUDGET_TOKENS,
        TERMINAL_SUMMARY_GATE,
        USER_INVOKED_SKILLS,
        parse_latest_changelog_version,
        validate_actionable_output_contract,
        validate_local_only_workflows,
        validate_catalog_routing,
        validate_release_alignment,
        validate_release_version_contract,
        validate_response_language_contract,
        validate_runtime_scratch,
        validate_skill_language,
        validate_terminal_summary_contract,
        validate_user_decision_contract,
        validate_skill,
        validate_skill_eval_files,
    )


class CanonicalSkillContractTest(unittest.TestCase):
    def test_canonical_skill_distribution_and_phase_owner_behaviors(self) -> None:
        self.assertEqual(
            EXPECTED_SKILLS,
            {
                "tk-ask-repo",
                "tk-browser-verify",
                "tk-drive",
                "tk-grill-me",
                "tk-grooming",
                "tk-handoff",
                "tk-implement",
                "tk-learn",
                "tk-merge-conflict",
                "tk-prototype",
                "tk-reflect",
                "tk-skill-diagnose",
                "tk-to-spec",
                "tk-to-tickets",
            },
        )
        self.assertEqual(USER_INVOKED_SKILLS, {"tk-ask-repo", "tk-drive"})
        self.assertTrue(
            {
                "ask-repo-value-finds-assignment-origin",
                "ask-repo-impact-sweeps-consumers",
                "ask-repo-existence-distinguishes-states",
                "ask-repo-attribution-uses-transport",
                "ask-repo-blocks-two-candidate-ambiguity",
                "ask-repo-refuses-implementation-diff",
                "ask-repo-refuses-effort-estimate",
                "ask-repo-search-failure-is-unverifiable",
                "ask-repo-blocks-contradicted-premise",
                "ask-repo-bounds-result-cardinality",
                "drive-requires-explicit-start",
                "drive-resumes-pending-answer",
                "drive-bounds-result-cardinality",
                "drive-response-language-explicit-korean",
                "drive-response-language-explicit-english",
                "drive-reflects-once-after-aggregate-pass",
                "drive-invokes-phase-owners",
                "drive-continues-after-ready-spec",
                "drive-rejects-missing-transition-echo",
                "drive-requires-spec-for-trivial-task",
                "drive-invokes-grill-on-unresolved-decision",
                "drive-skips-grill-for-ready-source",
                "drive-reruns-spec-after-grill",
                "drive-blocks-repeated-decision-return",
                "drive-commits-per-ticket",
                "drive-blocks-source-current-ui-mismatch",
                "drive-scopes-approval-to-asked-axis",
                "drive-reads-complete-remote-source",
                "grill-accepts-active-drive-handoff",
                "grill-echoes-drive-transition",
                "grill-returns-control-to-drive",
                "grill-uses-native-question-tool",
                "grill-bounds-confirmed-results",
                "to-spec-echoes-drive-transition",
                "to-spec-returns-decision-blocker-to-drive",
                "to-spec-blocks-source-current-ui-mismatch",
                "to-tickets-echoes-drive-transition",
                "to-tickets-returns-decision-blocker-to-drive",
                "to-tickets-blocks-source-current-ui-mismatch",
                "implement-reviews-every-standalone-run",
                "implement-audits-postcommit-hook-drift",
                "implement-blocks-semantic-hook-drift",
                "implement-allows-bounded-hook-bypass",
                "implement-diagnoses-unknown-cause-failure",
                "implement-active-drive-handoff-triggers",
                "implement-echoes-drive-transition",
                "implement-blocks-source-current-ui-mismatch",
                "implement-production-behavior-requires-durable-test",
                "implement-reports-bounded-behavior-summary",
                "grooming-vendor-artifact-remains-report-only",
                "grooming-unknown-ownership-asks-before-proposal",
                "grooming-honors-declared-exclusions",
                "grooming-bounds-result-cardinality",
                "reflect-checks-persistent-memory-prior-art",
                "reflect-separates-adjacent-memory-scope",
                "reflect-bounds-summary-cell-length",
                "reflect-bounds-result-cardinality",
                "skill-diagnose-reproduces-overtrigger-selection",
                "skill-diagnose-isolates-approval-bypass",
                "skill-diagnose-separates-grader-false-negative",
                "skill-diagnose-classifies-host-loading-difference",
                "skill-diagnose-verifies-efficiency-regression",
                "skill-diagnose-requires-resource-anchor",
                "skill-diagnose-rejects-cheaper-incorrect-candidate",
                "skill-diagnose-does-not-patch-unreproduced-incident",
                "skill-diagnose-bounds-one-theme-and-holdout",
                "skill-diagnose-never-mutates-canonical-path",
                "skill-diagnose-drafts-anonymized-upstream-issue",
                "skill-diagnose-keeps-consumer-drift-local",
                "skill-diagnose-withholds-draft-without-exact-ref",
                "skill-diagnose-withholds-draft-without-two-upstream-runs",
                "skill-diagnose-withholds-draft-without-control-holdout",
                "skill-diagnose-withholds-draft-for-matching-open-issue",
                "skill-diagnose-withholds-draft-for-unverified-closed-regression",
                "skill-diagnose-withholds-draft-when-issue-search-unavailable",
                "skill-diagnose-redacts-private-upstream-evidence",
                "reflect-hands-off-qualified-skill-incident-once",
                "reflect-skips-diagnosis-without-four-gate",
                "reflect-blocks-repeated-diagnosis-handoff",
                "reflect-response-language-preserves-machine-tokens",
                "reflect-drive-applies-eligible-tracked-repo-rule",
                "reflect-drive-never-creates-local-rule-target",
                "reflect-drive-skill-candidate-is-promotion-packet-only",
                "reflect-drive-blocks-target-drift",
                "browser-bounds-instrumented-evidence",
                "browser-instrumentation-residue-failure-is-unverifiable",
                "browser-proves-current-serving-source",
                "browser-classifies-failure-origin",
                "browser-causal-fix-requires-negative-control",
                "browser-bounds-result-cardinality",
                "handoff-bounds-result-cardinality",
                "learn-bounds-result-cardinality",
                "merge-conflict-bounds-result-cardinality",
                "prototype-bounds-result-cardinality",
                "skill-diagnose-bounds-result-cardinality",
                "to-spec-bounds-result-cardinality",
                "to-tickets-bounds-result-cardinality",
            }.issubset(REQUIRED_BEHAVIOR_CASES)
        )
        self.assertFalse(
            any(
                case.startswith(("code-review-", "diagnosing-bugs-"))
                for case in REQUIRED_BEHAVIOR_CASES
            )
        )

    def test_drive_success_receipts_echo_the_outstanding_transition(self) -> None:
        root = Path(__file__).resolve().parents[1]
        drive = (root / "skills/tk-drive/SKILL.md").read_text(encoding="utf-8")
        phases = (root / "skills/tk-drive/references/phases.md").read_text(
            encoding="utf-8"
        )

        for text in (drive, phases):
            self.assertIn("`Success state`", text)
            self.assertIn("`Outstanding transition`", text)
            self.assertIn("missing or mismatched", text)

        for skill in (
            "tk-grill-me",
            "tk-to-spec",
            "tk-to-tickets",
            "tk-implement",
        ):
            with self.subTest(skill=skill):
                text = (root / f"skills/{skill}/SKILL.md").read_text(
                    encoding="utf-8"
                )
                self.assertIn("`Return to: tk-drive`", text)
                self.assertIn("`Outstanding transition`", text)
                self.assertIn("verbatim", text)

    def test_drive_requires_spec_for_trivial_tasks(self) -> None:
        root = Path(__file__).resolve().parents[1]
        drive = (root / "skills/tk-drive/SKILL.md").read_text(encoding="utf-8")
        phases = (root / "skills/tk-drive/references/phases.md").read_text(
            encoding="utf-8"
        )

        for text in (drive, phases):
            self.assertIn("every active drive run", text)
            self.assertIn("no small-task exception", text)
            self.assertIn("`tk-to-spec`", text)

    def test_drive_risk_profile_is_deterministic_and_owner_preserving(self) -> None:
        root = Path(__file__).resolve().parents[1]
        drive = (root / "skills/tk-drive/SKILL.md").read_text(encoding="utf-8")
        phases = (root / "skills/tk-drive/references/phases.md").read_text(
            encoding="utf-8"
        )
        implement = (root / "skills/tk-implement/SKILL.md").read_text(
            encoding="utf-8"
        )
        review = (
            root / "skills/tk-implement/references/review-boundary.md"
        ).read_text(encoding="utf-8")

        signals = (
            "security-data",
            "state-compatibility",
            "public-blast-radius",
            "browser-network",
            "concurrency-side-effect",
            "evidence-recovery",
        )
        obligations = (
            "evidence-closure",
            "regression-seam",
            "compatibility",
            "browser-verdict",
            "side-effect-recovery",
            "independent-review",
        )
        mappings = (
            ("security-data", "regression-seam", "side-effect-recovery", "independent-review"),
            ("state-compatibility", "regression-seam", "compatibility", "side-effect-recovery", "independent-review"),
            ("public-blast-radius", "regression-seam", "compatibility", "independent-review"),
            ("browser-network", "regression-seam", "browser-verdict"),
            ("concurrency-side-effect", "regression-seam", "side-effect-recovery", "independent-review"),
            ("evidence-recovery", "evidence-closure"),
        )

        self.assertIn("### 🔴 HARD GATE · risk-based verification profile", drive)
        signal_positions = [phases.index(f"`{signal}`") for signal in signals]
        normalized_phases = " ".join(phases.split())
        obligation_order = "De-duplicate derived obligations and emit them in this order"
        obligations_text = normalized_phases[normalized_phases.index(obligation_order) :]
        obligation_positions = [
            obligations_text.index(f"`{obligation}`") for obligation in obligations
        ]
        self.assertEqual(signal_positions, sorted(signal_positions))
        self.assertEqual(obligation_positions, sorted(obligation_positions))
        self.assertTrue(all(signal in phases for signal in signals))
        self.assertTrue(all(obligation in phases for obligation in obligations))
        for mapping in mappings:
            row = next(line for line in phases.splitlines() if f"`{mapping[0]}`" in line)
            with self.subTest(signal=mapping[0]):
                self.assertTrue(all(f"`{token}`" in row for token in mapping))
        self.assertIn("With no material signal, keep the baseline path silent", drive)
        self.assertIn("Never create a dedicated risk document", phases)
        self.assertIn("never justifies a ticket ledger", normalized_phases)
        self.assertIn("material verification profile's four fields", implement)
        self.assertTrue(all(obligation in review for obligation in obligations))
        self.assertIn("unavailable review capability is", implement)
        self.assertIn("`Unverifiable`", review)

    def test_active_drive_success_fixtures_include_transition_envelope(self) -> None:
        root = Path(__file__).resolve().parents[1]
        fixtures = {
            "tk-drive": (
                "drive-resumes-pending-answer",
                "drive-continues-after-ready-spec",
                "drive-reruns-spec-after-grill",
            ),
            "tk-grill-me": ("grill-returns-control-to-drive",),
            "tk-to-spec": ("to-spec-active-drive-handoff",),
            "tk-to-tickets": ("to-tickets-active-drive-handoff",),
            "tk-implement": ("implement-active-drive-handoff-triggers",),
        }

        for skill, case_ids in fixtures.items():
            payload = json.loads(
                (root / f"skills/{skill}/evals/evals.json").read_text(
                    encoding="utf-8"
                )
            )
            cases = {case["id"]: case for case in payload["evals"]}
            for case_id in case_ids:
                with self.subTest(skill=skill, case=case_id):
                    case = cases[case_id]
                    prompt = case["prompt"]
                    self.assertIn("Success state:", prompt)
                    self.assertIn("Outstanding transition:", prompt)

    def test_drive_live_canary_matrix_is_codex_scoped(self) -> None:
        root = Path(__file__).resolve().parents[1]
        payload = json.loads(
            (root / "skills/tk-drive/evals/evals.json").read_text(
                encoding="utf-8"
            )
        )
        cases = {case["id"]: case for case in payload["evals"]}

        for case_id in (
            "drive-live-continues-after-ready-spec",
            "drive-live-implementation-holdout",
            "drive-live-initial-ssot-stop-control",
        ):
            with self.subTest(case=case_id):
                self.assertEqual(cases[case_id]["hosts"], ["codex"])
                self.assertTrue(cases[case_id]["prompt"].startswith("/tk-drive "))

        holdout_types = [
            assertion["type"]
            for assertion in cases["drive-live-implementation-holdout"][
                "assertions"
            ]
        ]
        self.assertEqual(holdout_types, ["event_order", "terminal_status"])
        self.assertEqual(
            cases["drive-live-implementation-holdout"]["assertions"][0][
                "before"
            ],
            {
                "type": "phase_receipt",
                "phase": "tk-implement",
                "state": "Pass",
            },
        )
        self.assertEqual(
            cases["drive-live-initial-ssot-stop-control"]["path"], "boundary"
        )
        self.assertEqual(
            [
                assertion["type"]
                for assertion in cases["drive-live-initial-ssot-stop-control"][
                    "assertions"
                ]
            ],
            [
                "terminal_status",
                "git_head_unchanged",
                "event_absent",
                "path_absent",
            ],
        )

    def test_skill_diagnose_upstream_proposal_matrix_is_fail_closed(self) -> None:
        root = Path(__file__).resolve().parents[1]
        payload = json.loads(
            (root / "skills/tk-skill-diagnose/evals/evals.json").read_text(
                encoding="utf-8"
            )
        )
        cases = {case["id"]: case for case in payload["evals"]}
        positive = cases["skill-diagnose-drafts-anonymized-upstream-issue"]
        positive_assertions = positive["assertions"]

        self.assertIn(
            {
                "type": "output_contains",
                "text": "## Summary",
            },
            positive_assertions,
        )
        self.assertIn(
            {
                "type": "output_contains",
                "text": "## Privacy note",
            },
            positive_assertions,
        )

        expected = {
            "skill-diagnose-keeps-consumer-drift-local": ("local-only", "Pass"),
            "skill-diagnose-withholds-draft-without-exact-ref": (
                "upstream-unverifiable",
                "Unverifiable",
            ),
            "skill-diagnose-withholds-draft-without-two-upstream-runs": (
                "upstream-unverifiable",
                "Unverifiable",
            ),
            "skill-diagnose-withholds-draft-without-control-holdout": (
                "upstream-unverifiable",
                "Unverifiable",
            ),
            "skill-diagnose-withholds-draft-for-matching-open-issue": (
                "upstream-candidate",
                "Pass",
            ),
            "skill-diagnose-withholds-draft-for-unverified-closed-regression": (
                "upstream-unverifiable",
                "Unverifiable",
            ),
            "skill-diagnose-withholds-draft-when-issue-search-unavailable": (
                "upstream-unverifiable",
                "Unverifiable",
            ),
        }
        for case_id, (disposition, terminal_status) in expected.items():
            with self.subTest(case=case_id):
                case = cases[case_id]
                assertions = case["assertions"]
                self.assertEqual(case["path"], "boundary")
                self.assertIn(
                    {"type": "output_contains", "text": disposition},
                    assertions,
                )
                self.assertIn(
                    {"type": "output_absent", "text": "## Summary"},
                    assertions,
                )
                self.assertIn(
                    {"type": "output_absent", "text": "## Environment"},
                    assertions,
                )
                self.assertIn(
                    {"type": "terminal_status", "expected": terminal_status},
                    assertions,
                )
                self.assertIn({"type": "git_head_unchanged"}, assertions)

        skill_text = (
            root / "skills/tk-skill-diagnose/SKILL.md"
        ).read_text(encoding="utf-8")
        reference_text = (
            root
            / "skills/tk-skill-diagnose/references/upstream-issue-anonymization.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "Only `upstream-draft-ready` may include an upstream issue title or body",
            " ".join(skill_text.split()),
        )
        self.assertIn(
            "accessible open and closed upstream issue search",
            " ".join(reference_text.split()),
        )

    def test_drive_reflection_tail_is_fixed_point_and_bounded(self) -> None:
        root = Path(__file__).resolve().parents[1]
        drive = (root / "skills/tk-drive/SKILL.md").read_text(encoding="utf-8")
        phases = (
            root / "skills/tk-drive/references/phases.md"
        ).read_text(encoding="utf-8")
        reflect = (
            root / "skills/tk-reflect/SKILL.md"
        ).read_text(encoding="utf-8")
        tail = (
            root / "skills/tk-reflect/references/drive-optimistic.md"
        ).read_text(encoding="utf-8")

        required = (
            "Mode: drive-optimistic",
            "Success state: Pass",
            "Outstanding transition: final receipt",
            "Return to: tk-drive",
        )
        for text in (phases, reflect, tail):
            with self.subTest(source=text[:40]):
                self.assertTrue(all(token in text for token in required[:3]))
        self.assertIn("reflect exactly once", drive)
        self.assertIn("Return to: tk-drive", phases)
        self.assertIn("Return to: tk-drive", tail)
        self.assertIn("product verification HEAD", phases)
        self.assertIn("tracked reflection commit", tail)
        self.assertIn("reflect-backup", tail)
        self.assertIn("never mutates a skill", " ".join(tail.split()))

    def test_reflect_and_grooming_share_exact_placement_rubric(self) -> None:
        root = Path(__file__).resolve().parents[1]
        reflect = (
            root / "skills/tk-reflect/references/repository-placement.md"
        ).read_text(encoding="utf-8")
        grooming = (
            root / "skills/tk-grooming/references/repository-placement.md"
        ).read_text(encoding="utf-8")

        self.assertEqual(reflect, grooming)

    def test_canonical_skill_contracts_use_english_and_preserve_user_output_language(
        self,
    ) -> None:
        root = Path(__file__).resolve().parents[1]

        self.assertEqual(validate_skill_language(root), [])
        self.assertEqual(validate_response_language_contract(root), [])
        self.assertEqual(validate_actionable_output_contract(root), [])
        self.assertEqual(validate_terminal_summary_contract(root), [])

    def test_response_language_gate_rejects_one_weakened_skill(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_root = Path(__file__).resolve().parents[1]
            for skill in EXPECTED_SKILLS:
                target = root / "skills" / skill / "SKILL.md"
                target.parent.mkdir(parents=True)
                text = (source_root / "skills" / skill / "SKILL.md").read_text(
                    encoding="utf-8"
                )
                if skill == "tk-ask-repo":
                    text = text.replace(
                        "latest explicit user language instruction",
                        "current source language",
                        1,
                    )
                target.write_text(text, encoding="utf-8")

            errors = validate_response_language_contract(root)

            self.assertEqual(len(errors), 1)
            self.assertIn("tk-ask-repo", errors[0])

    def test_actionable_output_gate_rejects_one_weakened_skill(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_root = Path(__file__).resolve().parents[1]
            for skill in EXPECTED_SKILLS:
                target = root / "skills" / skill / "SKILL.md"
                target.parent.mkdir(parents=True)
                text = (source_root / "skills" / skill / "SKILL.md").read_text(
                    encoding="utf-8"
                )
                if skill == "tk-ask-repo":
                    text = text.replace(
                        "first available free-form prose slot",
                        "last available free-form prose slot",
                        1,
                    )
                target.write_text(text, encoding="utf-8")

            errors = validate_actionable_output_contract(root)

            self.assertEqual(len(errors), 1)
            self.assertIn("tk-ask-repo", errors[0])

    def test_actionable_output_gate_rejects_one_duplicate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_root = Path(__file__).resolve().parents[1]
            for skill in EXPECTED_SKILLS:
                target = root / "skills" / skill / "SKILL.md"
                target.parent.mkdir(parents=True)
                text = (source_root / "skills" / skill / "SKILL.md").read_text(
                    encoding="utf-8"
                )
                if skill == "tk-ask-repo":
                    start = text.index("### 🔴 HARD GATE · actionable user output")
                    end = text.index("### 🔴 HARD GATE · response language", start)
                    text = text[:end] + text[start:end] + text[end:]
                target.write_text(text, encoding="utf-8")

            errors = validate_actionable_output_contract(root)

            self.assertEqual(len(errors), 1)
            self.assertIn("tk-ask-repo", errors[0])

    def test_actionable_output_gate_rejects_one_missing_gate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_root = Path(__file__).resolve().parents[1]
            for skill in EXPECTED_SKILLS:
                target = root / "skills" / skill / "SKILL.md"
                target.parent.mkdir(parents=True)
                text = (source_root / "skills" / skill / "SKILL.md").read_text(
                    encoding="utf-8"
                )
                if skill == "tk-ask-repo":
                    text = text.replace(ACTIONABLE_OUTPUT_GATE, "", 1)
                target.write_text(text, encoding="utf-8")

            errors = validate_actionable_output_contract(root)

            self.assertEqual(len(errors), 1)
            self.assertIn("tk-ask-repo", errors[0])

    def test_actionable_output_gate_rejects_exact_plus_weakened_duplicate(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_root = Path(__file__).resolve().parents[1]
            for skill in EXPECTED_SKILLS:
                target = root / "skills" / skill / "SKILL.md"
                target.parent.mkdir(parents=True)
                text = (source_root / "skills" / skill / "SKILL.md").read_text(
                    encoding="utf-8"
                )
                if skill == "tk-ask-repo":
                    weakened = ACTIONABLE_OUTPUT_GATE.replace(
                        "first available free-form prose slot",
                        "last available free-form prose slot",
                        1,
                    )
                    text = text.replace(
                        ACTIONABLE_OUTPUT_GATE,
                        ACTIONABLE_OUTPUT_GATE + "\n\n" + weakened,
                        1,
                    )
                target.write_text(text, encoding="utf-8")

            errors = validate_actionable_output_contract(root)

            self.assertEqual(len(errors), 1)
            self.assertIn("tk-ask-repo", errors[0])

    def test_terminal_summary_gate_rejects_one_weakened_skill(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_root = Path(__file__).resolve().parents[1]
            for skill in EXPECTED_SKILLS:
                target = root / "skills" / skill / "SKILL.md"
                target.parent.mkdir(parents=True)
                text = (source_root / "skills" / skill / "SKILL.md").read_text(
                    encoding="utf-8"
                )
                if skill == "tk-ask-repo":
                    text = text.replace(
                        "exactly one standalone `---` line",
                        "an optional standalone `---` line",
                        1,
                    )
                target.write_text(text, encoding="utf-8")

            errors = validate_terminal_summary_contract(root)

            self.assertEqual(len(errors), 1)
            self.assertIn("tk-ask-repo", errors[0])

    def test_terminal_summary_gate_rejects_one_duplicate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_root = Path(__file__).resolve().parents[1]
            for skill in EXPECTED_SKILLS:
                target = root / "skills" / skill / "SKILL.md"
                target.parent.mkdir(parents=True)
                text = (source_root / "skills" / skill / "SKILL.md").read_text(
                    encoding="utf-8"
                )
                if skill == "tk-ask-repo":
                    text = text.replace(
                        TERMINAL_SUMMARY_GATE,
                        TERMINAL_SUMMARY_GATE + "\n\n" + TERMINAL_SUMMARY_GATE,
                        1,
                    )
                target.write_text(text, encoding="utf-8")

            errors = validate_terminal_summary_contract(root)

            self.assertEqual(len(errors), 1)
            self.assertIn("tk-ask-repo", errors[0])

    def test_terminal_summary_gate_rejects_one_missing_gate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_root = Path(__file__).resolve().parents[1]
            for skill in EXPECTED_SKILLS:
                target = root / "skills" / skill / "SKILL.md"
                target.parent.mkdir(parents=True)
                text = (source_root / "skills" / skill / "SKILL.md").read_text(
                    encoding="utf-8"
                )
                if skill == "tk-ask-repo":
                    text = text.replace(TERMINAL_SUMMARY_GATE, "", 1)
                target.write_text(text, encoding="utf-8")

            errors = validate_terminal_summary_contract(root)

            self.assertEqual(len(errors), 1)
            self.assertIn("tk-ask-repo", errors[0])

    def test_terminal_summary_gate_rejects_one_misplaced_gate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_root = Path(__file__).resolve().parents[1]
            for skill in EXPECTED_SKILLS:
                target = root / "skills" / skill / "SKILL.md"
                target.parent.mkdir(parents=True)
                text = (source_root / "skills" / skill / "SKILL.md").read_text(
                    encoding="utf-8"
                )
                if skill == "tk-ask-repo":
                    text = text.replace(TERMINAL_SUMMARY_GATE + "\n\n", "", 1)
                    response_start = text.index(
                        "### 🔴 HARD GATE · response language"
                    )
                    response_end = text.index(
                        "\n## User decision questions", response_start
                    )
                    text = (
                        text[:response_end]
                        + "\n\n"
                        + TERMINAL_SUMMARY_GATE
                        + text[response_end:]
                    )
                target.write_text(text, encoding="utf-8")

            errors = validate_terminal_summary_contract(root)

            self.assertEqual(len(errors), 1)
            self.assertIn("tk-ask-repo", errors[0])

    def test_terminal_summary_gate_rejects_reintroduced_receipt_rendering(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_root = Path(__file__).resolve().parents[1]
            for skill in EXPECTED_SKILLS:
                target = root / "skills" / skill / "SKILL.md"
                target.parent.mkdir(parents=True)
                text = (source_root / "skills" / skill / "SKILL.md").read_text(
                    encoding="utf-8"
                )
                if skill == "tk-ask-repo":
                    text = text.replace(
                        TERMINAL_SUMMARY_GATE,
                        "`Outcome: <one user-facing sentence>`\n\n"
                        + TERMINAL_SUMMARY_GATE,
                        1,
                    )
                target.write_text(text, encoding="utf-8")

            errors = validate_terminal_summary_contract(root)

            self.assertEqual(len(errors), 1)
            self.assertIn("tk-ask-repo", errors[0])

    def test_canonical_skills_embed_native_user_decision_contract(self) -> None:
        root = Path(__file__).resolve().parents[1]
        required = (
            "## User decision questions",
            "`Question`",
            "`Recommendation`",
            "decision-relevant evidence",
            "two or three",
            "mutually exclusive options",
            "exactly one label",
            "`(Recommended)` or `(추천)`",
            "native structured input",
            "Plain text is allowed only",
            "failed or rejected call is not absence",
            "`AskUserQuestion`",
            "`request_user_input`",
            "Hermes Agent",
            "`clarify`",
        )

        for skill in EXPECTED_SKILLS:
            with self.subTest(skill=skill):
                text = (root / "skills" / skill / "SKILL.md").read_text(
                    encoding="utf-8"
                )
                self.assertTrue(
                    all(token in text for token in required),
                    f"{skill} is missing the native user-decision question contract",
                )
                start = text.index("## User decision questions")
                end = text.find("\n## ", start + 4)
                section = text[start:] if end < 0 else text[start:end]
                self.assertLess(
                    len(section.encode("utf-8")),
                    900,
                    f"{skill} user-decision contract is not compact",
                )
                self.assertNotIn("option previews, prototype cards", section)
        self.assertEqual(validate_user_decision_contract(root), [])

    def test_canonical_skill_outputs_are_decision_first_and_nonduplicative(self) -> None:
        root = Path(__file__).resolve().parents[1]
        required = {
            "tk-ask-repo": ("Lead with `Answer`", "Do not echo the inbound question"),
            "tk-browser-verify": ("Never paste or store raw console", "do not add a receipt heading"),
            "tk-drive": ("no-ticket placeholders", "child handoff envelope"),
            "tk-grill-me": ("The ledger is not a per-turn dump template", "append phase/status provenance"),
            "tk-grooming": ("Lead with one `## Disposition`", "Add `## Exceptions` only"),
            "tk-handoff": ("handoff artifact owns disposition", "Omit empty sections"),
            "tk-implement": (
                "Lead with `## Changed`",
                "2–5 short",
                "never paste logs or narrate review mechanics",
            ),
            "tk-learn": ("Lead with the promotion or no-op decision", "`Target path`"),
            "tk-merge-conflict": ("Use only non-empty sections in this order", "`Blocked: no active conflict`"),
            "tk-prototype": ("Record decision-relevant status once", "Keep command mechanics after the decision"),
            "tk-reflect": ("In chat, emit only", "no raw logs, transcripts, diff excerpts"),
            "tk-skill-diagnose": ("In chat, emit `## Diagnosis`", "Never copy raw logs, transcripts"),
            "tk-to-spec": ("Lead with the `Ready | Draft | Blocked | Unverifiable` decision", "Vertical slicing candidate areas"),
            "tk-to-tickets": ("User-facing output uses the ticket table", "artifact owns ticket bodies"),
        }
        result_tables = {
            "tk-ask-repo": "fields, consumers, or candidates",
            "tk-browser-verify": "`Criterion | Result | Evidence`",
            "tk-drive": "`Ticket | Outcome | Commit`",
            "tk-learn": "`Candidate | Disposition | Target`",
            "tk-merge-conflict": "`Path | Intent | Result`",
            "tk-prototype": "`Criterion | A | B [| C] | Conclusion | Evidence`",
            "tk-skill-diagnose": "`ID | Incident | Root cause`",
            "tk-to-tickets": "`Ticket | User-visible slice`",
        }
        forbidden = {
            "tk-grooming": ("The final section is always this fixed `## Summary` table",),
            "tk-implement": ("a non-empty `## Remaining risks`",),
            "tk-learn": ("Created path reports exact planned path",),
            "tk-reflect": ("The response's final section is always:",),
            "tk-skill-diagnose": ("Emit these canonical sections:",),
        }

        self.assertEqual(set(required), EXPECTED_SKILLS)
        self.assertEqual(set(RESULT_BUDGET_TOKENS), EXPECTED_SKILLS)
        for skill, tokens in required.items():
            with self.subTest(skill=skill):
                text = (root / "skills" / skill / "SKILL.md").read_text(
                    encoding="utf-8"
                )
                self.assertTrue(all(token in text for token in tokens))
                self.assertTrue(
                    all(token not in text for token in forbidden.get(skill, ()))
                )
                if skill in result_tables:
                    normalized = " ".join(text.split())
                    self.assertIn(result_tables[skill], normalized)
                    self.assertIn(
                        "Use a sentence when only one user-relevant row exists",
                        normalized,
                    )
                self.assertNotIn("`Outcome: <one user-facing sentence>`", text)
                normalized = " ".join(text.split())
                self.assertTrue(
                    all(token in normalized for token in RESULT_BUDGET_TOKENS[skill])
                )

    def test_catalog_result_budget_gate_rejects_one_weakened_skill(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill_dir = Path(directory) / "tk-ask-repo"
            skill_dir.mkdir()
            source = (
                Path(__file__).resolve().parents[1]
                / "skills/tk-ask-repo/SKILL.md"
            ).read_text(encoding="utf-8")
            weakened = source.replace("top five to seven", "several", 1)
            path = skill_dir / "SKILL.md"
            path.write_text(weakened, encoding="utf-8")

            errors, _ = validate_skill(path)

            self.assertTrue(
                any("bounded result contract missing" in error for error in errors)
            )

    def test_user_decision_contract_gate_rejects_one_weakened_skill(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_root = Path(__file__).resolve().parents[1]
            for skill in EXPECTED_SKILLS:
                target = root / "skills" / skill / "SKILL.md"
                target.parent.mkdir(parents=True)
                text = (
                    source_root / "skills" / skill / "SKILL.md"
                ).read_text(encoding="utf-8")
                if skill == "tk-prototype":
                    text = text.replace(
                        "`request_user_input`, or Hermes",
                        "ask in prose, or Hermes",
                    )
                target.write_text(text, encoding="utf-8")

            errors = validate_user_decision_contract(root)

            self.assertEqual(len(errors), 1)
            self.assertIn("tk-prototype", errors[0])
            self.assertIn("`request_user_input`", errors[0])

    def test_skill_language_validator_rejects_mixed_operational_prose(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for skill in EXPECTED_SKILLS:
                skill_dir = root / "skills" / skill
                references = skill_dir / "references"
                references.mkdir(parents=True)
                (skill_dir / "SKILL.md").write_text(
                    "Operational contract. User-facing prose follows the user's language.\n",
                    encoding="utf-8",
                )
            mixed = root / "skills" / "tk-browser-verify" / "references" / "phase.md"
            mixed.write_text("Do not mix 운영 문장.\n", encoding="utf-8")

            errors = validate_skill_language(root)

            self.assertEqual(len(errors), 1)
            self.assertIn("canonical skill operational prose must be English", errors[0])


class RuntimeScratchTest(unittest.TestCase):
    def init_repo(self, root: Path) -> None:
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)

    def test_allows_ignored_runtime_scratch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.init_repo(root)
            (root / ".gitignore").write_text(".tigerkit/\n", encoding="utf-8")
            (root / ".tigerkit").mkdir()
            (root / ".tigerkit" / "evidence.txt").write_text("local\n", encoding="utf-8")

            self.assertEqual(validate_runtime_scratch(root), [])

    def test_rejects_tracked_runtime_scratch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.init_repo(root)
            (root / ".gitignore").write_text(".tigerkit/\n", encoding="utf-8")
            (root / ".tigerkit").mkdir()
            (root / ".tigerkit" / "evidence.txt").write_text("tracked\n", encoding="utf-8")
            subprocess.run(
                ["git", "add", "-f", ".tigerkit/evidence.txt"],
                cwd=root,
                check=True,
            )

            self.assertEqual(
                validate_runtime_scratch(root),
                [".tigerkit: remove tracked TigerKit runtime scratch"],
            )

    def test_rejects_runtime_scratch_in_package(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".tigerkit").mkdir()

            self.assertEqual(
                validate_runtime_scratch(root),
                [".tigerkit: remove TigerKit runtime scratch from packaged repository"],
            )


class ReleaseContractTest(unittest.TestCase):
    def test_parses_latest_changelog_version(self) -> None:
        text = "# Changelog\n\n## 19.2.3 — Current\n\n## 19.2.2 — Previous\n"

        self.assertEqual(parse_latest_changelog_version(text), "19.2.3")

    def test_requires_readme_snapshot_to_match_latest_changelog(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "CHANGELOG.md").write_text(
                "# Changelog\n\n## 19.2.3 — Current\n", encoding="utf-8"
            )
            (root / "README.md").write_text(
                'Immutable `v19.2.2` snapshot\n', encoding="utf-8"
            )

            self.assertEqual(
                validate_release_version_contract(root),
                ["README.md: immutable snapshot must reference latest changelog release v19.2.3"],
            )

    def test_release_alignment_requires_main_tag_and_release_sha(self) -> None:
        self.assertEqual(
            validate_release_alignment("aaa", "aaa", "aaa"), []
        )
        self.assertEqual(
            validate_release_alignment("aaa", "bbb", "aaa"),
            ["release provenance: origin/main, peeled tag, and GitHub Release must match"],
        )

    def test_rejects_ci_validation_workflows(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workflow = root / ".github/workflows/validate.yml"
            workflow.parent.mkdir(parents=True)
            workflow.write_text("name: validate\n", encoding="utf-8")

            self.assertEqual(
                validate_local_only_workflows(root),
                [
                    ".github/workflows/validate.yml: remove CI validation; "
                    "run verification locally"
                ],
            )

    def test_accepts_matching_readme_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "CHANGELOG.md").write_text(
                "# Changelog\n\n## 19.2.3 — Current\n", encoding="utf-8"
            )
            (root / "README.md").write_text(
                'Immutable `v19.2.3` snapshot\n', encoding="utf-8"
            )

            self.assertEqual(validate_release_version_contract(root), [])


class CatalogRoutingContractTest(unittest.TestCase):
    def test_repository_catalog_matrix_covers_hosts_and_boundaries(self) -> None:
        root = Path(__file__).resolve().parents[1]

        self.assertEqual(validate_catalog_routing(root), [])

    def test_rejects_incomplete_catalog_matrix(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "evals" / "catalog-routing.json"
            path.parent.mkdir(parents=True)
            path.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "critical_hosts": ["codex"],
                        "cases": [
                            {
                                "id": "only",
                                "boundary": "tk-implement vs tk-drive",
                                "prompt": "run",
                                "focus_skill": "tk-drive",
                                "expected_selected_skill": "tk-drive",
                                "critical": True,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            errors = validate_catalog_routing(root)

            self.assertTrue(any("critical_hosts" in error for error in errors))
            self.assertTrue(
                any("all required routing boundaries" in error for error in errors)
            )


class SkillCompatibilityTest(unittest.TestCase):
    def write_skill(self, root: Path, frontmatter: str) -> Path:
        skill = root / "tk-sample"
        skill.mkdir()
        path = skill / "SKILL.md"
        path.write_text(f"---\n{frontmatter}\n---\n\n# Sample\n", encoding="utf-8")
        return path

    def test_rejects_unknown_top_level_frontmatter_field(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_skill(
                Path(directory),
                "\n".join(
                    (
                        "name: tk-sample",
                        'description: "[user/auto] sample"',
                        "unknown-extension: true",
                        "metadata:",
                        "  tigerkit:",
                        "    kind: hybrid",
                        "    origin: tigerkit",
                        "    relationship: native",
                    )
                ),
            )

            errors, _ = validate_skill(path)

            self.assertTrue(any("unknown top-level fields" in error for error in errors))

    def test_allows_documented_user_invocation_extensions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_skill(
                Path(directory),
                "\n".join(
                    (
                        "name: tk-sample",
                        'description: "[user] sample"',
                        "argument-hint: <input>",
                        "disable-model-invocation: true",
                        "metadata:",
                        "  tigerkit:",
                        "    kind: user-invoked",
                        "    origin: tigerkit",
                        "    relationship: native",
                    )
                ),
            )
            agents = path.parent / "agents"
            agents.mkdir()
            (agents / "openai.yaml").write_text(
                'interface:\n  display_name: "Sample"\n  short_description: "[user] Sample"\n'
                "policy:\n  allow_implicit_invocation: false\n",
                encoding="utf-8",
            )

            errors, _ = validate_skill(path)

            self.assertFalse(any("unknown top-level fields" in error for error in errors))


class SkillEvalFixtureTest(unittest.TestCase):
    def write_json(self, path: Path, content: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def write_valid_trigger_contract(self, skill: Path) -> None:
        self.write_json(
            skill / "evals" / "triggers.json",
            '{"skill":"tk-sample","kind":"user-invoked","queries":['
            '{"id":"explicit","split":"train","query":"/tk-sample run","should_trigger":true},'
            '{"id":"implicit","split":"validation","query":"plain request","should_trigger":false}]}',
        )

    def valid_behavior_case(self, case_id: str, path: str = "success") -> dict[str, object]:
        allowed = ["Pass"] if path == "success" else ["Blocked"]
        return {
            "id": case_id,
            "path": path,
            "prompt": "run",
            "expected_output": "receipt",
            "assertions": [
                {"type": "judge", "criterion": "Reports a receipt"},
                {"type": "terminal_status", "allowed": allowed},
            ],
        }

    def write_behavior_contract(self, skill: Path, cases: list[dict[str, object]]) -> None:
        self.write_json(
            skill / "evals" / "evals.json",
            json.dumps({"skill_name": "tk-sample", "evals": cases}),
        )

    def test_rejects_train_validation_trigger_overlap(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "tk-sample"
            self.write_json(
                skill / "evals" / "triggers.json",
                '{"skill":"tk-sample","kind":"user-invoked","queries":['
                '{"id":"train-same","split":"train","query":"same request","should_trigger":true},'
                '{"id":"validation-same","split":"validation","query":"same request","should_trigger":false}]}'
            )
            self.write_json(
                skill / "evals" / "evals.json",
                '{"skill_name":"tk-sample","evals":['
                '{"id":"ok","path":"success","prompt":"/tk-sample run",'
                '"expected_output":"receipt","assertions":['
                '{"type":"judge","criterion":"Reports a receipt"},'
                '{"type":"terminal_status","allowed":["Pass"]}]},'
                '{"id":"stop","path":"boundary","prompt":"/tk-sample impossible",'
                '"expected_output":"blocked","assertions":['
                '{"type":"judge","criterion":"Stops as Blocked"},'
                '{"type":"terminal_status","allowed":["Blocked"]}]}]}'
            )

            errors = validate_skill_eval_files(skill, "user-invoked")

            self.assertTrue(any("train/validation query overlap" in error for error in errors))

    def test_rejects_small_hybrid_validation_set(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "tk-sample"
            self.write_json(
                skill / "evals" / "triggers.json",
                '{"skill":"tk-sample","kind":"hybrid","queries":['
                '{"id":"train-positive","split":"train","query":"run it","should_trigger":true},'
                '{"id":"validation-negative","split":"validation","query":"skip it","should_trigger":false}]}'
            )
            self.write_json(
                skill / "evals" / "evals.json",
                '{"skill_name":"tk-sample","evals":['
                '{"id":"ok","path":"success","prompt":"run",'
                '"expected_output":"receipt","assertions":['
                '{"type":"judge","criterion":"Reports a receipt"},'
                '{"type":"terminal_status","allowed":["Pass"]}]},'
                '{"id":"stop","path":"boundary","prompt":"stop",'
                '"expected_output":"blocked","assertions":['
                '{"type":"judge","criterion":"Stops as Blocked"},'
                '{"type":"terminal_status","allowed":["Blocked"]}]}]}'
            )

            errors = validate_skill_eval_files(skill, "hybrid")

            self.assertTrue(any("at least 8 positive and 8 negative" in error for error in errors))
            self.assertTrue(any("missing query facets" in error for error in errors))

    def test_accepts_minimal_user_invoked_eval_contract(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "tk-sample"
            self.write_json(
                skill / "evals" / "triggers.json",
                '{"skill":"tk-sample","kind":"user-invoked","queries":['
                '{"id":"explicit","split":"train","query":"/tk-sample run","should_trigger":true},'
                '{"id":"implicit","split":"validation","query":"plain request","should_trigger":false}]}'
            )
            self.write_json(
                skill / "evals" / "evals.json",
                '{"skill_name":"tk-sample","evals":['
                '{"id":"ok","path":"success","prompt":"/tk-sample run",'
                '"expected_output":"receipt","assertions":['
                '{"type":"judge","criterion":"Reports a receipt"},'
                '{"type":"terminal_status","allowed":["Pass"]}]},'
                '{"id":"stop","path":"boundary","prompt":"/tk-sample impossible",'
                '"expected_output":"blocked","assertions":['
                '{"type":"judge","criterion":"Stops as Blocked"},'
                '{"type":"terminal_status","allowed":["Blocked"]}]}]}'
            )

            self.assertEqual(validate_skill_eval_files(skill, "user-invoked"), [])

    def test_validates_host_scoped_event_order_assertions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "tk-sample"
            self.write_valid_trigger_contract(skill)
            success = self.valid_behavior_case("ok")
            success["hosts"] = ["claude-code"]
            success["assertions"].append(
                {
                    "type": "event_order",
                    "hosts": ["claude-code"],
                    "before": {
                        "type": "phase_receipt",
                        "phase": "tk-to-spec",
                        "state": "Ready",
                        "transition": "ticket decision",
                    },
                    "after": {
                        "type": "phase_invocation",
                        "phase": "tk-implement",
                    },
                    "forbidden_between": [{"type": "final_output"}],
                }
            )
            success["assertions"].append(
                {
                    "type": "event_absent",
                    "hosts": ["claude-code"],
                    "event": {
                        "type": "phase_invocation",
                        "phase": "tk-implement",
                    },
                }
            )
            self.write_behavior_contract(
                skill,
                [success, self.valid_behavior_case("stop", "boundary")],
            )

            self.assertEqual(validate_skill_eval_files(skill, "user-invoked"), [])

            success["hosts"] = ["unknown-host"]
            success["assertions"][-2] = {
                "type": "event_order",
                "hosts": ["unknown-host"],
                "before": {"type": "phase_receipt"},
                "after": {"type": "unknown"},
                "forbidden_between": "final_output",
            }
            success["assertions"][-1] = {
                "type": "event_absent",
                "hosts": ["unknown-host"],
                "event": {"type": "unknown"},
            }
            self.write_behavior_contract(
                skill,
                [success, self.valid_behavior_case("stop", "boundary")],
            )

            errors = validate_skill_eval_files(skill, "user-invoked")

            self.assertTrue(any("case 1 hosts" in error for error in errors))
            self.assertTrue(any("event_order hosts" in error for error in errors))
            self.assertTrue(any("event_order before" in error for error in errors))
            self.assertTrue(any("event_order after" in error for error in errors))
            self.assertTrue(
                any("event_order forbidden_between" in error for error in errors)
            )
            self.assertTrue(any("event_absent hosts" in error for error in errors))
            self.assertTrue(any("event_absent event" in error for error in errors))

    def test_rejects_duplicate_behavior_id(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "tk-sample"
            self.write_valid_trigger_contract(skill)
            self.write_behavior_contract(
                skill,
                [
                    self.valid_behavior_case("same"),
                    self.valid_behavior_case("same", "boundary"),
                ],
            )

            errors = validate_skill_eval_files(skill, "user-invoked")

            self.assertTrue(any("duplicate case ids" in error for error in errors))

    def test_rejects_unknown_skill_name(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "tk-sample"
            self.write_valid_trigger_contract(skill)
            self.write_json(
                skill / "evals" / "evals.json",
                json.dumps(
                    {
                        "skill_name": "tk-other",
                        "evals": [
                            self.valid_behavior_case("ok"),
                            self.valid_behavior_case("stop", "boundary"),
                        ],
                    }
                ),
            )

            errors = validate_skill_eval_files(skill, "user-invoked")

            self.assertTrue(any("skill_name must match" in error for error in errors))

    def test_rejects_missing_or_prose_only_assertions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "tk-sample"
            self.write_valid_trigger_contract(skill)
            success = self.valid_behavior_case("ok")
            success["assertions"] = [{"type": "judge", "criterion": "Looks correct"}]
            self.write_behavior_contract(
                skill,
                [success, self.valid_behavior_case("stop", "boundary")],
            )

            errors = validate_skill_eval_files(skill, "user-invoked")

            self.assertTrue(any("mechanical assertion" in error for error in errors))

    def test_rejects_missing_input_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "tk-sample"
            self.write_valid_trigger_contract(skill)
            success = self.valid_behavior_case("ok")
            success["files"] = ["fixtures/missing.json"]
            self.write_behavior_contract(
                skill,
                [success, self.valid_behavior_case("stop", "boundary")],
            )

            errors = validate_skill_eval_files(skill, "user-invoked")

            self.assertTrue(any("missing input file" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
