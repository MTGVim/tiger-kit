#!/usr/bin/env python3
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

if __package__:
    from scripts.validate_skills import (
        EXPECTED_SKILLS,
        REQUIRED_BEHAVIOR_CASES,
        USER_INVOKED_SKILLS,
        parse_latest_changelog_version,
        validate_local_only_workflows,
        validate_catalog_routing,
        validate_release_alignment,
        validate_release_version_contract,
        validate_runtime_scratch,
        validate_skill_language,
        validate_user_decision_contract,
        validate_skill,
        validate_skill_eval_files,
    )
else:
    from validate_skills import (
        EXPECTED_SKILLS,
        REQUIRED_BEHAVIOR_CASES,
        USER_INVOKED_SKILLS,
        parse_latest_changelog_version,
        validate_local_only_workflows,
        validate_catalog_routing,
        validate_release_alignment,
        validate_release_version_contract,
        validate_runtime_scratch,
        validate_skill_language,
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
                "drive-requires-explicit-start",
                "drive-resumes-pending-answer",
                "drive-does-not-auto-reflect",
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
                "grooming-vendor-artifact-remains-report-only",
                "grooming-unknown-ownership-asks-before-proposal",
                "grooming-honors-declared-exclusions",
                "reflect-checks-persistent-memory-prior-art",
                "reflect-separates-adjacent-memory-scope",
                "reflect-bounds-summary-cell-length",
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
                "skill-diagnose-redacts-private-upstream-evidence",
                "reflect-hands-off-qualified-skill-incident-once",
                "reflect-skips-diagnosis-without-four-gate",
                "reflect-blocks-repeated-diagnosis-handoff",
                "browser-bounds-instrumented-evidence",
                "browser-instrumentation-residue-failure-is-unverifiable",
                "browser-proves-current-serving-source",
                "browser-classifies-failure-origin",
                "browser-causal-fix-requires-negative-control",
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
                    prompt = cases[case_id]["prompt"]
                    self.assertIn("Success state:", prompt)
                    self.assertIn("Outstanding transition:", prompt)

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

    def test_canonical_skills_embed_native_user_decision_contract(self) -> None:
        root = Path(__file__).resolve().parents[1]
        required = (
            "## User decision questions",
            "Render `Question` before `Recommendation` and the proposals.",
            "evidence-derived context, decision impact, and unresolved axis",
            "must not require the user to decode raw `Evidence`",
            "two or three mutually exclusive proposals",
            "exactly one best recommendation",
            "`(Recommended)` or `(추천)`",
            "option previews, prototype cards, or equivalent",
            "use it proactively",
            "must call that tool",
            "Plain-text questions are allowed only",
            "failed or rejected tool call",
            "Claude Code: `AskUserQuestion`",
            "Codex: `request_user_input`",
            "Hermes Agent: `clarify`",
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
        self.assertEqual(validate_user_decision_contract(root), [])

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
                        "Codex: `request_user_input`",
                        "Codex: ask in prose",
                    )
                target.write_text(text, encoding="utf-8")

            errors = validate_user_decision_contract(root)

            self.assertEqual(len(errors), 1)
            self.assertIn("tk-prototype", errors[0])
            self.assertIn("Codex: `request_user_input`", errors[0])

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
