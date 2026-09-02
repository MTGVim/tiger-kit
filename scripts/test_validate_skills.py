#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import validate_skills


class EvalSotValidatorTest(unittest.TestCase):
    def test_frontmatter_requires_standard_yaml_scalars(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "SKILL.md"
            path.write_text(
                "---\nname: tk-example\ndescription: 'foo: bar'\n---\nBody\n",
                encoding="utf-8",
            )
            data, _ = validate_skills.frontmatter(path)
            self.assertEqual(data["description"], "foo: bar")

            path.write_text(
                "---\nname: tk-example\ndescription: foo: bar\n---\nBody\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "invalid YAML frontmatter"):
                validate_skills.frontmatter(path)

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

    def test_skill_body_requires_english_narrative(self) -> None:
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
            frontmatter = "---\ndescription: [user/auto] 예시 스킬\n---\n"
            with patch.object(validate_skills, "ROOT", root):
                rejected, _ = validate_skills.validate_frontmatter_and_body(
                    "tk-example", skill_dir, data, frontmatter + "한국어 운영 지침\n"
                )
                accepted, _ = validate_skills.validate_frontmatter_and_body(
                    "tk-example",
                    skill_dir,
                    data,
                    frontmatter
                    + "Use the exact literal `한국어 출력`.\n\n"
                    + "```text\n한국어 출력\n```\n",
                )
            self.assertTrue(any("model-facing narrative must be English" in error for error in rejected))
            self.assertFalse(any("model-facing narrative must be English" in error for error in accepted))

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
                    "tk-example", skill_dir, data, "English operating instructions.\n"
                )
            self.assertTrue(any("requires disable-model-invocation: false" in error for error in errors))

    def test_openai_policy_must_be_top_level(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill_dir = root / "tk-example"
            agents = skill_dir / "agents"
            agents.mkdir(parents=True)
            (agents / "openai.yaml").write_text(
                'interface:\n  short_description: "[user/auto] Example"\n'
                "  policy:\n    allow_implicit_invocation: true\n",
                encoding="utf-8",
            )
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
                    "tk-example", skill_dir, data, "English operating instructions.\n"
                )
            self.assertTrue(any("policy must be top-level" in error for error in errors))

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
                    "---\nargument-hint: [--ci]\n---\nNo option is documented.\n",
                )
                defined, _ = validate_skills.validate_frontmatter_and_body(
                    "tk-example",
                    skill_dir,
                    data,
                    "---\nargument-hint: [--ci]\n---\nUse `--ci`.\n",
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

    def test_path_not_read_requires_a_safe_checkout_relative_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "tk-example"
            evals = skill / "evals"
            evals.mkdir(parents=True)
            path = evals / "evals.json"

            def write(watched: str) -> None:
                path.write_text(
                    json.dumps(
                        {
                            "skill_name": "tk-example",
                            "evals": [
                                {
                                    "id": "success",
                                    "path": "success",
                                    "prompt": "explain it",
                                    "expected_output": "done",
                                    "assertions": [
                                        {"type": "path_not_read", "path": watched}
                                    ],
                                },
                                {
                                    "id": "boundary",
                                    "path": "boundary",
                                    "prompt": "stop",
                                    "expected_output": "stopped",
                                    "assertions": [
                                        {"type": "terminal_status", "expected": "Blocked"}
                                    ],
                                },
                            ],
                        }
                    ),
                    encoding="utf-8",
                )

            write("fixtures/unrelated.md")
            errors, _ = validate_skills.validate_behavior_contract("tk-example", path)
            self.assertEqual(errors, [])

            write("../outside.md")
            errors, _ = validate_skills.validate_behavior_contract("tk-example", path)
            self.assertTrue(any("path_not_read needs safe path" in error for error in errors))

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

    def test_reference_body_requires_english_narrative(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skills = Path(directory)
            references = skills / "tk-example" / "references"
            references.mkdir(parents=True)
            note = references / "note.md"
            note.write_text("한국어 운영 지침\n", encoding="utf-8")

            with patch.object(validate_skills, "ROOT", skills.parent):
                rejected = validate_skills.validate_reference_resources(skills)
            self.assertTrue(
                any(
                    "note.md:1" in error
                    and "model-facing narrative must be English" in error
                    for error in rejected
                )
            )

            note.write_text(
                "---\ntitle: 한국어 제목\n---\nEnglish reference.\n",
                encoding="utf-8",
            )
            with patch.object(validate_skills, "ROOT", skills.parent):
                rejected_frontmatter = validate_skills.validate_reference_resources(skills)
            self.assertTrue(any("note.md:2" in error for error in rejected_frontmatter))

            note.write_text(
                "Use the exact literal `한국어 출력`.\n\n"
                "```text\n한국어 출력\n```\n",
                encoding="utf-8",
            )
            with patch.object(validate_skills, "ROOT", skills.parent):
                self.assertEqual(validate_skills.validate_reference_resources(skills), [])

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

    def test_changelog_is_not_a_repository_requirement(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "skills").mkdir()
            (root / "README.md").write_text("timeless product docs\n", encoding="utf-8")
            (root / ".gitignore").write_text(".tigerkit/\n", encoding="utf-8")
            with patch.object(validate_skills, "ROOT", root), patch.object(validate_skills, "SKILLS", root / "skills"):
                errors = validate_skills.validate_repository_contract(set())
            self.assertFalse(any("CHANGELOG.md" in error for error in errors))

    def test_shared_execution_protocol_copies_must_match(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skills = Path(directory)
            canonical = skills / "tk-prep/references"
            consumer = skills / "tk-pr-respond/references"
            canonical.mkdir(parents=True)
            consumer.mkdir(parents=True)
            for name in validate_skills.SHARED_EXECUTION_PROTOCOLS:
                (canonical / name).write_text(f"canonical {name}\n", encoding="utf-8")
                (consumer / name).write_text(f"canonical {name}\n", encoding="utf-8")

            self.assertEqual(validate_skills.validate_shared_execution_protocols(skills), [])
            (consumer / "sdd.md").write_text("drift\n", encoding="utf-8")
            self.assertTrue(
                any(
                    "sdd.md" in error and "sync_execution_protocol.py" in error
                    for error in validate_skills.validate_shared_execution_protocols(skills)
                )
            )

    def test_shared_domain_context_copies_must_match(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skills = Path(directory)
            canonical = skills / "tk-prep/references/domain-context.md"
            canonical.parent.mkdir(parents=True)
            canonical.write_text("canonical domain context\n", encoding="utf-8")
            for skill_name in validate_skills.SHARED_DOMAIN_CONTEXT_CONSUMERS:
                consumer = skills / skill_name / "references/domain-context.md"
                consumer.parent.mkdir(parents=True)
                consumer.write_text("canonical domain context\n", encoding="utf-8")

            self.assertEqual(validate_skills.validate_shared_domain_context(skills), [])
            drifted = skills / "tk-pr-open/references/domain-context.md"
            drifted.write_text("drift\n", encoding="utf-8")
            self.assertTrue(
                any(
                    "tk-pr-open" in error and "sync_execution_protocol.py" in error
                    for error in validate_skills.validate_shared_domain_context(skills)
                )
            )


if __name__ == "__main__":
    unittest.main()
