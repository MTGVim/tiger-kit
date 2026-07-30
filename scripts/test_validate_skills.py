#!/usr/bin/env python3
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

if __package__:
    from scripts.validate_skills import (
        DRIVE_GRAPH_EDGES,
        DRIVE_GRAPH_NODES,
        DRIVE_TERMINAL_SUMMARY_GATE,
        DRIVE_STAGE_TOKENS,
        EXPECTED_SKILLS,
        REQUIRED_BEHAVIOR_CASES,
        RESULT_BUDGET_TOKENS,
        TERMINAL_SUMMARY_GATE,
        USER_INVOKED_SKILLS,
        parse_latest_changelog_version,
        validate_local_only_workflows,
        validate_catalog_routing,
        validate_browser_preflight_contract,
        validate_compact_preflight_contract,
        validate_continuation_boundary,
        validate_drive_graph_contract,
        validate_learning_loop_contract,
        validate_prepared_drive_contract,
        validate_reflect_ignored_target_contract,
        validate_release_alignment,
        validate_release_version_contract,
        validate_response_language_contract,
        validate_runtime_scratch,
        validate_single_drive_adhd_contract,
        validate_skill_language,
        validate_terminal_summary_contract,
        validate_unified_grill_contract,
        validate_user_decision_contract,
        validate_skill,
        validate_skill_eval_files,
    )
else:
    from validate_skills import (
        DRIVE_GRAPH_EDGES,
        DRIVE_GRAPH_NODES,
        DRIVE_TERMINAL_SUMMARY_GATE,
        DRIVE_STAGE_TOKENS,
        EXPECTED_SKILLS,
        REQUIRED_BEHAVIOR_CASES,
        RESULT_BUDGET_TOKENS,
        TERMINAL_SUMMARY_GATE,
        USER_INVOKED_SKILLS,
        parse_latest_changelog_version,
        validate_local_only_workflows,
        validate_catalog_routing,
        validate_browser_preflight_contract,
        validate_compact_preflight_contract,
        validate_continuation_boundary,
        validate_drive_graph_contract,
        validate_learning_loop_contract,
        validate_prepared_drive_contract,
        validate_reflect_ignored_target_contract,
        validate_release_alignment,
        validate_release_version_contract,
        validate_response_language_contract,
        validate_runtime_scratch,
        validate_single_drive_adhd_contract,
        validate_skill_language,
        validate_terminal_summary_contract,
        validate_unified_grill_contract,
        validate_user_decision_contract,
        validate_skill,
        validate_skill_eval_files,
    )


class CanonicalSkillContractTest(unittest.TestCase):
    def test_continuation_is_honest_about_runtime_boundary(self) -> None:
        source_root = Path(__file__).resolve().parents[1]
        self.assertEqual(validate_continuation_boundary(source_root), [])

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            relative = "skills/tk-drive/SKILL.md"
            target = root / relative
            target.parent.mkdir(parents=True)
            target.write_text(
                (
                    source_root / relative
                ).read_text(encoding="utf-8").replace(
                    "not a durable scheduler",
                    "a durable scheduler",
                    1,
                ),
                encoding="utf-8",
            )
            errors = validate_continuation_boundary(root)

        self.assertTrue(
            any("runtime workflow engine" in error for error in errors)
        )

    def test_reflect_auto_apply_is_limited_to_exact_ignored_target(self) -> None:
        source_root = Path(__file__).resolve().parents[1]
        self.assertEqual(validate_reflect_ignored_target_contract(source_root), [])

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            relative = "skills/tk-reflect/references/drive-optimistic.md"
            target = root / relative
            target.parent.mkdir(parents=True)
            target.write_text(
                (
                    source_root / relative
                ).read_text(encoding="utf-8").replace(
                    "Tracked, unignored, new, symlinked, external, changed-since-baseline",
                    "Most unsafe targets",
                    1,
                ),
                encoding="utf-8",
            )
            errors = validate_reflect_ignored_target_contract(root)

        self.assertTrue(
            any("exact ignored-target reflection safety" in error for error in errors)
        )

    def test_compact_preflight_replaces_lifecycle_machinery(self) -> None:
        source_root = Path(__file__).resolve().parents[1]
        self.assertEqual(validate_compact_preflight_contract(source_root), [])

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            obsolete = root / "skills/tk-drive/scripts/prep_state.py"
            obsolete.parent.mkdir(parents=True)
            obsolete.write_text("legacy\n", encoding="utf-8")
            errors = validate_compact_preflight_contract(root)

        self.assertTrue(any("obsolete drive lifecycle machinery" in error for error in errors))

    def test_grill_contract_keeps_one_owner_for_both_callers(self) -> None:
        source_root = Path(__file__).resolve().parents[1]
        self.assertEqual(validate_unified_grill_contract(source_root), [])

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            grill = root / "skills/tk-grill-me/SKILL.md"
            drive = root / "skills/tk-drive/SKILL.md"
            grill.parent.mkdir(parents=True)
            drive.parent.mkdir(parents=True)
            grill.write_text(
                (source_root / "skills/tk-grill-me/SKILL.md").read_text(
                    encoding="utf-8"
                ),
                encoding="utf-8",
            )
            drive.write_text(
                (source_root / "skills/tk-drive/SKILL.md").read_text(
                    encoding="utf-8"
                ),
                encoding="utf-8",
            )
            (root / "skills/tk-grilling").mkdir()

            errors = validate_unified_grill_contract(root)

        self.assertTrue(
            any("boundary-less duplicate procedure" in error for error in errors)
        )

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
                "tk-adhd",
                "tk-prototype",
                "tk-reflect",
                "tk-skill-diagnose",
                "tk-to-spec",
                "tk-to-tickets",
            },
        )
        self.assertEqual(
            USER_INVOKED_SKILLS, {"tk-ask-repo", "tk-drive", "tk-adhd"}
        )
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
                "drive-writes-compact-preflight",
                "drive-bounds-task-anchored-prior-art",
                "drive-excludes-forbidden-prior-art",
                "drive-preserves-preflight-on-write-failure",
                "drive-rejects-preflight-secrets",
                "drive-resumes-from-current-evidence",
                "adhd-explicit-one-shot",
                "adhd-does-not-carry-over",
                "adhd-safety-exception",
                "drive-requires-explicit-start",
                "drive-resumes-preparing-decision-answer",
                "drive-bounds-result-cardinality",
                "drive-response-language-explicit-korean",
                "drive-response-language-explicit-english",
                "drive-reflects-once-then-finalizes",
                "drive-invokes-direct-graph-owners",
                "drive-continues-after-preflight",
                "drive-enforces-exact-procedure-graph",
                "drive-continues-without-receipt-boundary",
                "drive-continues-multi-unit-through-reflection",
                "drive-owns-single-terminal-response",
                "drive-prepares-trivial-task",
                "drive-amends-on-first-new-decision",
                "drive-skips-grill-for-ready-source",
                "drive-blocks-second-amendment",
                "drive-writes-compact-preflight",
                "drive-preserves-preflight-on-write-failure",
                "drive-rejects-preflight-secrets",
                "drive-resumes-from-current-evidence",
                "drive-blocks-repeated-decision-return",
                "drive-commits-per-ticket",
                "drive-invalidates-source-current-ui-mismatch",
                "drive-invalidates-unapproved-secondary-axis",
                "drive-reads-complete-remote-source",
                "grill-me-unifies-caller-modes",
                "grill-me-uses-native-question-tool",
                "grill-me-active-drive-routes-directly",
                "grill-me-blocks-active-drive-autostart",
                "grill-me-does-not-mutate-or-invoke-phases",
                "to-spec-routes-ready-state-directly",
                "to-spec-returns-decision-blocker-to-prep",
                "to-spec-blocks-source-current-ui-mismatch",
                "to-tickets-routes-ledger-state-directly",
                "to-tickets-returns-decision-blocker-to-prep",
                "to-tickets-blocks-source-current-ui-mismatch",
                "implement-reviews-every-standalone-run",
                "implement-audits-postcommit-hook-drift",
                "implement-blocks-semantic-hook-drift",
                "implement-allows-bounded-hook-bypass",
                "implement-diagnoses-unknown-cause-failure",
                "implement-active-drive-unit-state",
                "implement-routes-unit-state-directly",
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
                "reflect-classifies-prevention-owner-and-host-dependency",
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
                "reflect-drive-applies-exact-existing-ignored-rule",
                "reflect-drive-never-creates-local-rule-target",
                "reflect-drive-rejects-ineligible-target-matrix",
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
                "to-spec-disposes-prior-art-semantically",
                "to-spec-omits-empty-prior-art",
                "to-spec-blocks-prior-art-conflict",
                "to-tickets-bounds-result-cardinality",
            }.issubset(REQUIRED_BEHAVIOR_CASES)
        )
        self.assertFalse(
            any(
                case.startswith(("code-review-", "diagnosing-bugs-"))
                for case in REQUIRED_BEHAVIOR_CASES
            )
        )

    def test_drive_declares_direct_continuation_and_one_terminal_owner(self) -> None:
        root = Path(__file__).resolve().parents[1]
        drive = (root / "skills/tk-drive/SKILL.md").read_text(encoding="utf-8")
        phases = (root / "skills/tk-drive/references/phases.md").read_text(
            encoding="utf-8"
        )

        for text in (drive, phases):
            self.assertIn("same active turn", text)
            self.assertIn("tk-drive finalization", text)
            self.assertNotIn("Outstanding transition", text)
            self.assertNotIn("Return to: tk-drive", text)

        self.assertEqual(validate_drive_graph_contract(root), [])

    def test_drive_declares_read_only_non_success_finalization(self) -> None:
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
        tickets = (root / "skills/tk-to-tickets/SKILL.md").read_text(
            encoding="utf-8"
        )

        node = "tk-drive:non-success-finalization"
        self.assertIn(node, DRIVE_GRAPH_NODES)
        sources = {source for source, target, *_ in DRIVE_GRAPH_EDGES if target == node}
        self.assertEqual(
            sources,
            {
                "tk-drive:preflight",
                "tk-grill-me",
                "tk-prototype",
                "tk-to-spec",
                "tk-to-tickets",
                "tk-implement",
                "tk-merge-conflict",
                "aggregate-verification",
                "tk-browser-verify",
                "tk-reflect",
            },
        )
        self.assertFalse(any(source == node for source, *_ in DRIVE_GRAPH_EDGES))

        for text in (drive, phases):
            self.assertIn("tk-drive non-success finalization", text)
            self.assertIn("Dependency blocked", text)
            self.assertIn("Not attempted", text)
            self.assertIn("Unverified", text)
            self.assertIn("no outgoing edge", text)
        self.assertIn("changed or uncommitted paths", implement)
        self.assertIn("recovery condition", implement)
        self.assertIn("commit: none", review)
        self.assertIn("Last attempt", tickets)
        self.assertEqual(validate_drive_graph_contract(root), [])

    def test_drive_graph_rejects_unknown_node_cycle_and_missing_condition(self) -> None:
        root = Path(__file__).resolve().parents[1]
        unknown = list(DRIVE_GRAPH_EDGES)
        unknown[0] = ("tk-drive:preflight", "tk-gril-me", "", "confirmed", "stop", "tk-to-specc")
        cycle = list(DRIVE_GRAPH_EDGES)
        cycle.append(("tk-drive:finalization", "tk-drive:preflight", "restart", "ready", "stop", "tk-grill-me"))
        non_success_cycle = list(DRIVE_GRAPH_EDGES)
        non_success_cycle.append(
            (
                "tk-drive:non-success-finalization",
                "tk-drive:preflight",
                "restart",
                "ready",
                "stop",
                "tk-grill-me",
            )
        )
        duplicate = list(DRIVE_GRAPH_EDGES) + [DRIVE_GRAPH_EDGES[0]]

        unknown_errors = validate_drive_graph_contract(root, tuple(unknown))
        cycle_errors = validate_drive_graph_contract(root, tuple(cycle))
        non_success_cycle_errors = validate_drive_graph_contract(
            root, tuple(non_success_cycle)
        )
        duplicate_errors = validate_drive_graph_contract(root, tuple(duplicate))

        self.assertTrue(any("unknown node 'tk-gril-me'" in error for error in unknown_errors))
        self.assertTrue(any("unknown next node 'tk-to-specc'" in error for error in unknown_errors))
        self.assertTrue(any("missing terminal condition" in error for error in unknown_errors))
        self.assertTrue(any("edge set differs" in error for error in unknown_errors))
        self.assertTrue(any("forbidden cycle" in error for error in cycle_errors))
        self.assertTrue(
            any("forbidden cycle" in error for error in non_success_cycle_errors)
        )
        self.assertTrue(any("duplicate edge is ambiguous" in error for error in duplicate_errors))

    def test_drive_stage_gate_rejects_contract_weakening(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_root = Path(__file__).resolve().parents[1]
            for relative in (
                "skills/tk-drive/SKILL.md",
                "skills/tk-drive/references/phases.md",
            ):
                target = root / relative
                target.parent.mkdir(parents=True)
                text = (source_root / relative).read_text(encoding="utf-8")
                text = text.replace(DRIVE_STAGE_TOKENS[0], "Planning")
                text = text.replace("three", "four")
                target.write_text(text, encoding="utf-8")

            errors = validate_prepared_drive_contract(root)

            self.assertEqual(len(errors), 4)
            self.assertEqual(
                sum("stage ownership" in error for error in errors),
                2,
            )
            self.assertEqual(
                sum("corrective boundary" in error for error in errors),
                2,
            )

    def test_drive_prepares_and_executes_every_task_in_one_run(self) -> None:
        root = Path(__file__).resolve().parents[1]
        drive = (root / "skills/tk-drive/SKILL.md").read_text(encoding="utf-8")
        phases = (root / "skills/tk-drive/references/phases.md").read_text(
            encoding="utf-8"
        )

        for text in (drive, phases):
            self.assertIn(".tigerkit/prep.md", text)
            self.assertIn("Preparing", text)
            self.assertIn("Executing", text)
            self.assertIn("same active", text)
        self.assertNotIn("tk-prep", drive)

    def test_adhd_is_explicit_adapted_and_not_shared(self) -> None:
        root = Path(__file__).resolve().parents[1]
        adhd = (root / "skills/tk-adhd/SKILL.md").read_text(encoding="utf-8")

        self.assertIn("disable-model-invocation: true", adhd)
        self.assertIn("origin: ayghri/i-have-adhd", adhd)
        self.assertIn("relationship: adapted", adhd)
        self.assertIn("only to the current response", adhd)
        self.assertIn("Do not carry them into the next response", adhd)
        self.assertIn("Every later response requires a new explicit", adhd)
        self.assertIn("## Scope", adhd)
        self.assertNotIn("## Persistence", adhd)
        self.assertNotIn("ADHD mode: on", adhd)
        self.assertNotIn("ADHD mode: off", adhd)
        self.assertIn("## When to break the rules", adhd)
        self.assertEqual(validate_single_drive_adhd_contract(root), [])

        reflect = (root / "skills/tk-reflect/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("explicit invocation of another skill", reflect)
        self.assertIn("output-style utility", reflect)
        reflect_triggers = (
            root / "skills/tk-reflect/evals/triggers.json"
        ).read_text(encoding="utf-8")
        self.assertIn("$tk-adhd 지금 진행 상태와 다음 행동이 보이게 해줘", reflect_triggers)

    def test_drive_runtime_contract_does_not_require_event_recorder(self) -> None:
        root = Path(__file__).resolve().parents[1]
        for relative in (
            "skills/tk-drive/SKILL.md",
            "skills/tk-drive/references/phases.md",
        ):
            text = (root / relative).read_text(encoding="utf-8")
            self.assertNotIn("TK_DRIVE_EVENT_RECORDER", text)
            self.assertNotIn("TK_DRIVE_EVENT_LOG", text)
            self.assertIn("same active turn", text)

    def test_learning_loop_is_bounded_owned_and_fail_closed(self) -> None:
        root = Path(__file__).resolve().parents[1]
        reflect = (root / "skills/tk-reflect/SKILL.md").read_text(
            encoding="utf-8"
        )
        prep = (root / "skills/tk-drive/SKILL.md").read_text(encoding="utf-8")
        spec = (root / "skills/tk-to-spec/SKILL.md").read_text(
            encoding="utf-8"
        )
        normalized_prep = " ".join(prep.split())

        for token in (
            "Preferred prevention owner",
            "Host dependency",
        ):
            self.assertIn(token, reflect)
        for token in (
            "at most seven",
            "applicable rules",
            "tests",
            "ADRs",
            "repository skills",
            "code invariants",
            "raw sessions",
            "prior implementation or reflection scratch",
            "arbitrary global state",
            "inaccessible host-only rules",
        ):
            self.assertIn(token, normalized_prep)
        for token in (
            "`adopted | already-satisfied | not-applicable | conflict`",
            "R/AC mapping",
            "## Prior art",
            "A `conflict` disposition prevents `Ready`",
            "no relevant prior art exists, omit `## Prior art`",
        ):
            self.assertIn(token, spec)
        self.assertIn(
            "pass their native result state directly",
            " ".join(prep.split()),
        )
        self.assertEqual(validate_learning_loop_contract(root), [])

    def test_learning_loop_validator_rejects_owner_cap_and_conflict_drift(
        self,
    ) -> None:
        source_root = Path(__file__).resolve().parents[1]
        mutations = {
            "skills/tk-reflect/SKILL.md": (
                "Preferred prevention owner",
                "Suggested owner",
            ),
            "skills/tk-drive/SKILL.md": ("at most", "up to"),
            "skills/tk-to-spec/SKILL.md": (
                "A `conflict`",
                "A `disagreement`",
            ),
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative in (
                "skills/tk-grill-me/SKILL.md",
                "skills/tk-reflect/SKILL.md",
                "skills/tk-drive/SKILL.md",
                "skills/tk-to-spec/SKILL.md",
                "skills/tk-to-tickets/SKILL.md",
            ):
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(
                    (source_root / relative).read_text(encoding="utf-8"),
                    encoding="utf-8",
                )
            for relative, (old, new) in mutations.items():
                target = root / relative
                text = target.read_text(encoding="utf-8")
                target.write_text(text.replace(old, new), encoding="utf-8")

            errors = validate_learning_loop_contract(root)

        self.assertEqual(len(errors), 3)
        self.assertTrue(all("learning-loop ownership" in error for error in errors))

    def test_drive_v21_eval_migrations_cover_prepared_cutover(self) -> None:
        root = Path(__file__).resolve().parents[1]
        payload = json.loads(
            (root / "skills/tk-drive/evals/evals.json").read_text(
                encoding="utf-8"
            )
        )
        migrations = {row["from"]: row["to"] for row in payload["migrations"]}

        self.assertEqual(
            {
                key: migrations.get(key)
                for key in (
                    "drive-resumes-pending-answer",
                    "drive-continues-after-ready-spec",
                    "drive-live-continues-after-ready-spec",
                    "drive-live-initial-ssot-stop-control",
                    "drive-requires-spec-for-trivial-task",
                    "drive-invokes-grill-on-unresolved-decision",
                    "drive-reruns-spec-after-grill",
                )
            },
            {
                "drive-resumes-pending-answer": "drive-resumes-preparing-decision-answer",
                "drive-continues-after-ready-spec": "drive-resumes-from-current-evidence",
                "drive-live-continues-after-ready-spec": "drive-live-direct-prepared-execution",
                "drive-live-initial-ssot-stop-control": "drive-live-direct-prepares-and-executes-source",
                "drive-requires-spec-for-trivial-task": "drive-prepares-trivial-task",
                "drive-invokes-grill-on-unresolved-decision": "drive-amends-on-first-new-decision",
                "drive-reruns-spec-after-grill": "drive-blocks-second-amendment",
            },
        )

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

        obligations = (
            "evidence-closure",
            "regression-seam",
            "compatibility",
            "browser-verdict",
            "side-effect-recovery",
            "independent-review",
        )

        self.assertIn("### 🔴 HARD GATE · risk-based verification profile", drive)
        normalized_phases = " ".join(phases.split())
        self.assertIn("Consume the sealed material profile", drive)
        self.assertIn("cannot", normalized_phases)
        self.assertIn("add unsupported", drive)
        self.assertIn("remove an obligation", drive)
        self.assertIn("material verification profile's four fields", implement)
        self.assertTrue(all(obligation in review for obligation in obligations))
        self.assertIn("unavailable review capability is", implement)
        self.assertIn("`Unverifiable`", review)

    def test_active_drive_success_fixtures_use_direct_graph_state(self) -> None:
        root = Path(__file__).resolve().parents[1]
        payload = json.loads(
            (root / "skills/tk-drive/evals/evals.json").read_text(
                encoding="utf-8"
            )
        )
        cases = {case["id"]: case for case in payload["evals"]}
        case = cases["drive-continues-after-preflight"]
        self.assertNotIn("Success state:", case["prompt"])
        self.assertNotIn("Outstanding transition:", case["prompt"])
        self.assertIn("applicable node", case["prompt"])

    def test_drive_live_canary_matrix_is_codex_scoped(self) -> None:
        root = Path(__file__).resolve().parents[1]
        payload = json.loads(
            (root / "skills/tk-drive/evals/evals.json").read_text(
                encoding="utf-8"
            )
        )
        cases = {case["id"]: case for case in payload["evals"]}

        for case_id in (
            "drive-live-direct-prepared-execution",
            "drive-live-direct-implementation-holdout",
            "drive-live-direct-prepares-and-executes-source",
        ):
            with self.subTest(case=case_id):
                self.assertEqual(cases[case_id]["hosts"], ["codex"])
                self.assertIn("/tk-drive", cases[case_id]["prompt"])

        holdout_types = [
            assertion["type"]
            for assertion in cases["drive-live-direct-implementation-holdout"][
                "assertions"
            ]
        ]
        self.assertEqual(
            holdout_types,
            [
                "event_order",
                "path_text_equals",
                "path_text_equals",
                "git_head_changed",
                "git_commit_count_delta",
                "changed_paths_equal",
                "path_text_contains",
                "terminal_status",
            ],
        )
        self.assertEqual(
            cases["drive-live-direct-implementation-holdout"]["assertions"][0][
                "before"
            ],
            {
                "type": "phase_invocation",
                "phase": "tk-implement",
            },
        )
        self.assertEqual(
            cases["drive-live-direct-prepares-and-executes-source"]["path"], "success"
        )
        self.assertEqual(
            [
                assertion["type"]
                for assertion in cases["drive-live-direct-prepares-and-executes-source"][
                    "assertions"
                ]
            ],
            [
                "event_order",
                "path_text_equals",
                "git_head_changed",
                "git_commit_count_delta",
                "changed_paths_equal",
                "path_text_contains",
                "terminal_status",
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

        self.assertIn("invoke `tk-reflect` exactly once", drive)
        self.assertIn("tk-reflect", phases)
        self.assertIn("tk-drive finalization", phases)
        self.assertNotIn("Outstanding transition", phases)
        self.assertNotIn("Return to: tk-drive", phases)
        self.assertNotIn("## Tracked target", tail)
        self.assertIn("scripts/ignored_rule_apply.py", tail)
        self.assertIn("untracked, and ignored", tail)
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
        self.assertEqual(validate_terminal_summary_contract(root), [])
        self.assertEqual(validate_drive_graph_contract(root), [])
        self.assertEqual(validate_prepared_drive_contract(root), [])
        self.assertEqual(validate_reflect_ignored_target_contract(root), [])
        self.assertEqual(validate_continuation_boundary(root), [])

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
                        "Do not emit a standalone separator",
                        "A standalone separator is optional",
                        1,
                    )
                target.write_text(text, encoding="utf-8")

            errors = validate_terminal_summary_contract(root)

            self.assertEqual(len(errors), 1)
            self.assertIn("tk-ask-repo", errors[0])

    def test_drive_browser_preflight_is_material_private_and_cold_start_safe(
        self,
    ) -> None:
        root = Path(__file__).resolve().parents[1]

        self.assertEqual(validate_browser_preflight_contract(root), [])

    def test_drive_browser_preflight_rejects_one_weakened_surface(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_root = Path(__file__).resolve().parents[1]
            for relative in (
                "skills/tk-drive/SKILL.md",
                "skills/tk-drive/references/phases.md",
            ):
                source = source_root / relative
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                text = source.read_text(encoding="utf-8")
                if relative.endswith("SKILL.md"):
                    text = text.replace("re-request", "reuse")
                target.write_text(text, encoding="utf-8")

            errors = validate_browser_preflight_contract(root)

            self.assertEqual(len(errors), 1)
            self.assertIn("skills/tk-drive/SKILL.md", errors[0])

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

        for skill in EXPECTED_SKILLS - {"tk-adhd"}:
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
            "tk-drive": ("explicit source", "internal procedure evidence"),
            "tk-grill-me": (
                "The ledger is not a per-turn dump template",
                "consumes native status directly",
            ),
            "tk-grooming": ("Lead with one `## Disposition`", "Add `## Exceptions` only"),
            "tk-handoff": ("handoff artifact owns disposition", "Omit empty sections"),
            "tk-implement": (
                "Lead with `## Changed`",
                "2–5 short",
                "never paste logs or narrate review mechanics",
            ),
            "tk-learn": ("Lead with the promotion or no-op decision", "`Target path`"),
            "tk-merge-conflict": ("Use only non-empty sections in this order", "`Blocked: no active conflict`"),
            "tk-adhd": ("## Rules", "## When to break the rules"),
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
                        "type": "phase_invocation",
                        "phase": "tk-to-spec",
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
                "before": {"type": "unknown"},
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
