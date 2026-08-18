#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import validate_skills


class EvalSotValidatorTest(unittest.TestCase):
    def test_current_repository_is_structurally_valid(self) -> None:
        errors, _ = validate_skills.validate_all()
        self.assertEqual(errors, [])

    def test_native_question_tool_contract_is_present(self) -> None:
        targets = (
            "tk-prep", "tk-audit", "tk-github-image-upload-to-pr", "tk-grooming",
            "tk-learn", "tk-pr-open", "tk-pr-rebase", "tk-pr-respond", "tk-pr-sweep",
            "tk-prototype", "tk-wizard",
        )
        required = ("AskUserQuestion", "request_user_input", "clarify", "unavailable", "plain chat")
        for name in targets:
            text = (validate_skills.ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertTrue(all(token in text for token in required), name)

    def test_korean_canonical_prose_is_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill_dir = root / "tk-example"
            skill_dir.mkdir()
            data = {
                "name": "tk-example",
                "description": "[user/auto] 예시 스킬",
                "disable-model-invocation": False,
                "metadata": {
                    "tigerkit": {
                        "kind": "hybrid",
                        "origin": "tigerkit",
                        "relationship": "native",
                    }
                },
            }
            with patch.object(validate_skills, "ROOT", root):
                errors, _ = validate_skills.validate_frontmatter_and_body(
                    "tk-example", skill_dir, data, "한국어 운영 지침\n"
                )
            self.assertEqual(errors, [])

    def test_hybrid_requires_explicit_model_invocation_flag(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill_dir = root / "tk-example"
            skill_dir.mkdir()
            data = {
                "name": "tk-example",
                "description": "[user/auto] 예시 스킬",
                "metadata": {
                    "tigerkit": {
                        "kind": "hybrid",
                        "origin": "tigerkit",
                        "relationship": "native",
                    }
                },
            }
            with patch.object(validate_skills, "ROOT", root):
                errors, _ = validate_skills.validate_frontmatter_and_body(
                    "tk-example", skill_dir, data, "한국어 운영 지침\n"
                )
            self.assertTrue(any("requires disable-model-invocation: false" in error for error in errors))

    def test_argument_hint_long_options_must_be_defined_in_body(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill_dir = root / "tk-example"
            skill_dir.mkdir()
            data = {
                "name": "tk-example",
                "description": "[user/auto] 예시 스킬",
                "disable-model-invocation": False,
                "argument-hint": "[--ci]",
                "metadata": {
                    "tigerkit": {
                        "kind": "hybrid",
                        "origin": "tigerkit",
                        "relationship": "native",
                    }
                },
            }
            with patch.object(validate_skills, "ROOT", root):
                missing, _ = validate_skills.validate_frontmatter_and_body(
                    "tk-example",
                    skill_dir,
                    data,
                    "---\nargument-hint: [--ci]\n---\n설명 없음\n",
                )
                defined, _ = validate_skills.validate_frontmatter_and_body(
                    "tk-example",
                    skill_dir,
                    data,
                    "---\nargument-hint: [--ci]\n---\n`--ci`를 사용한다.\n",
                )
            self.assertTrue(any("argument-hint option '--ci'" in error for error in missing))
            self.assertFalse(any("argument-hint option '--ci'" in error for error in defined))

    def test_catalog_is_discovered_from_skill_directories(self) -> None:
        skills = validate_skills.discover_skills()
        self.assertGreater(len(skills), 0)
        self.assertEqual(set(skills), {path.parent.name for path in validate_skills.SKILLS.glob("tk-*/SKILL.md")})

    def test_duplicate_eval_surfaces_are_absent(self) -> None:
        self.assertFalse((validate_skills.ROOT / "scripts/sync_eval_compat.py").exists())
        self.assertFalse((validate_skills.ROOT / "evals/trigger-cases.yaml").exists())
        self.assertFalse((validate_skills.ROOT / "evals/behavior-cases.yaml").exists())
        self.assertEqual(list(validate_skills.SKILLS.glob("tk-*/test-prompts.json")), [])

    def test_behavior_contract_requires_mechanical_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "evals.json"
            path.write_text(
                json.dumps(
                    {
                        "skill_name": "tk-example",
                        "evals": [
                            {
                                "id": "success",
                                "path": "success",
                                "prompt": "do it",
                                "expected_output": "done",
                                "assertions": [{"type": "judge", "criterion": "looks right"}],
                            },
                            {
                                "id": "boundary",
                                "path": "boundary",
                                "prompt": "stop",
                                "expected_output": "stopped",
                                "assertions": [{"type": "terminal_status", "expected": "Blocked"}],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            errors, _ = validate_skills.validate_behavior_contract("tk-example", path)
            self.assertTrue(any("mechanical evidence" in error for error in errors))

    def test_trigger_contract_rejects_split_overlap(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "triggers.json"
            path.write_text(
                json.dumps(
                    {
                        "skill": "tk-example",
                        "kind": "user-invoked",
                        "queries": [
                            {
                                "id": "train-positive",
                                "split": "train",
                                "query": "same",
                                "should_trigger": True,
                                "facets": [],
                            },
                            {
                                "id": "validation-negative",
                                "split": "validation",
                                "query": "same",
                                "should_trigger": False,
                                "facets": [],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            errors, _ = validate_skills.validate_trigger_contract("tk-example", "user-invoked", path)
            self.assertTrue(any("overlap" in error for error in errors))

    def test_references_require_readable_non_executable_text(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skills = Path(directory)
            references = skills / "tk-example" / "references"
            references.mkdir(parents=True)
            note = references / "note.md"
            note.write_text("readable knowledge\n", encoding="utf-8")
            self.assertEqual(validate_skills.validate_reference_resources(skills), [])

            executable = references / "helper.sh"
            executable.write_text("#!/bin/sh\n", encoding="utf-8")
            executable.chmod(0o755)
            (references / "invalid.md").write_bytes(b"\x7fELF\x00\xff")
            (references / "nul").write_bytes(b"text\x00")
            errors = validate_skills.validate_reference_resources(skills)
            self.assertTrue(any("must not be executable" in error for error in errors))
            self.assertTrue(any("readable UTF-8 text" in error for error in errors))
            self.assertTrue(any("must not contain NUL bytes" in error for error in errors))
            self.assertEqual(validate_skills.validate_routing_invariants(skills), [])
            with patch.object(validate_skills, "ROOT", skills):
                self.assertEqual(validate_skills.validate_repo_links(), [])

    def test_direct_strategy_rejects_model_tier_pairing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skills = Path(directory)
            skill = skills / "tk-example"
            references = skill / "references"
            references.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                "Recommend `strategy=direct`, `model=cheapest`.\n",
                encoding="utf-8",
            )
            errors = validate_skills.validate_routing_invariants(skills)
            self.assertTrue(any("delegated-only" in error for error in errors))

    def test_direct_strategy_accepts_session_model_inheritance(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skills = Path(directory)
            skill = skills / "tk-example"
            skill.mkdir()
            (skill / "SKILL.md").write_text(
                "Use strategy=direct with model_class=n/a and requested_selector=n/a.\n",
                encoding="utf-8",
            )
            self.assertEqual(validate_skills.validate_routing_invariants(skills), [])

    def test_release_critical_references_canonical_case_ids(self) -> None:
        skills = validate_skills.discover_skills()
        behavior_ids: dict[str, set[str]] = {}
        for name, (skill_dir, _, _) in skills.items():
            errors, ids = validate_skills.validate_behavior_contract(name, skill_dir / "evals/evals.json")
            self.assertEqual(errors, [])
            behavior_ids[name] = ids
        catalog_errors, catalog_ids = validate_skills.validate_catalog(set(skills), behavior_ids)
        self.assertEqual(catalog_errors, [])
        self.assertEqual(validate_skills.validate_release_critical(behavior_ids, catalog_ids), [])

    def test_user_invoked_skill_cannot_be_a_child_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            parent = root / "tk-parent"
            child = root / "tk-child"
            (parent / "evals").mkdir(parents=True)
            child.mkdir()
            (parent / "evals/evals.json").write_text(
                json.dumps({
                    "evals": [{
                        "id": "handoff",
                        "assertions": [{
                            "type": "event_order",
                            "after": {"type": "phase_invocation", "phase": "tk-child"},
                        }],
                    }],
                }),
                encoding="utf-8",
            )
            skills = {
                "tk-parent": (parent, {"metadata": {"tigerkit": {"kind": "hybrid"}}}, ""),
                "tk-child": (child, {"metadata": {"tigerkit": {"kind": "user-invoked"}}}, ""),
            }
            errors = validate_skills.validate_invocation_graph(skills)
            self.assertTrue(any("cannot invoke user-invoked skill tk-child" in error for error in errors))

    def test_readme_does_not_require_a_release_version(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "skills").mkdir()
            (root / "README.md").write_text("timeless product docs\n", encoding="utf-8")
            (root / "CHANGELOG.md").write_text("## 99.4.2 — Example\n", encoding="utf-8")
            (root / ".gitignore").write_text(".tigerkit/\n", encoding="utf-8")
            with patch.object(validate_skills, "ROOT", root), patch.object(validate_skills, "SKILLS", root / "skills"):
                errors = validate_skills.validate_repository_contract(set())
            self.assertFalse(any("README.md" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
