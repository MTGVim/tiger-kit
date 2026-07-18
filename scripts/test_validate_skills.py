#!/usr/bin/env python3
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from validate_skills import (
    parse_latest_changelog_version,
    validate_release_alignment,
    validate_release_behavior_fixtures,
    validate_release_version_contract,
    validate_runtime_scratch,
    validate_skill,
    validate_skill_eval_files,
)


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


class ReleaseFixtureTest(unittest.TestCase):
    def test_maintainer_release_behavior_fixtures_validate(self) -> None:
        self.assertEqual(validate_release_behavior_fixtures(), [])


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

    def test_release_alignment_requires_main_tag_release_and_ci_sha(self) -> None:
        self.assertEqual(
            validate_release_alignment("aaa", "aaa", "aaa", "aaa"), []
        )
        self.assertEqual(
            validate_release_alignment("aaa", "bbb", "aaa", "aaa"),
            ["release provenance: origin/main, peeled tag, GitHub Release, and CI SHA must match"],
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
