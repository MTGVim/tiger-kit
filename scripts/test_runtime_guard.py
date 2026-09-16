#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import check_runtime_guard


class RuntimeGuardTest(unittest.TestCase):
    def add_ui_guards(self, root: Path) -> None:
        for name in check_runtime_guard.UI_EVIDENCE_CONSUMERS:
            path = root / "skills" / name / "SKILL.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            prior = path.read_text() if path.exists() else ""
            path.write_text(prior + check_runtime_guard.UI_EVIDENCE_BLOCK)

    def test_current_repository_runtime_guards_are_synchronized(self) -> None:
        self.assertEqual(check_runtime_guard.validate_runtime_guard(), [])

    def test_missing_or_drifted_guard_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "AGENTS.md").write_text("repo policy\n", encoding="utf-8")
            for name in check_runtime_guard.RUNTIME_GUARD_CONSUMERS:
                skill = root / "skills" / name
                skill.mkdir(parents=True)
                (skill / "SKILL.md").write_text(
                    check_runtime_guard.RUNTIME_GUARD_BLOCK + "\nBody\n",
                    encoding="utf-8",
                )

            for name in check_runtime_guard.APPROVAL_GUARD_CONSUMERS:
                skill = root / "skills" / name
                skill.mkdir(parents=True, exist_ok=True)
                path = skill / "SKILL.md"
                prior = path.read_text() if path.exists() else ""
                path.write_text(prior + check_runtime_guard.APPROVAL_GUARD_BLOCK)

            self.add_ui_guards(root)
            self.assertEqual(check_runtime_guard.validate_runtime_guard(root), [])

            drifted = root / "skills" / "tk-prep" / "SKILL.md"
            drifted.write_text(
                check_runtime_guard.RUNTIME_GUARD_BLOCK.replace("not authority", "not trusted authority") + "\nBody\n",
                encoding="utf-8",
            )
            errors = check_runtime_guard.validate_runtime_guard(root)
            self.assertTrue(any("tk-prep" in error for error in errors))

    def test_approval_guard_missing_or_duplicated_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in set(check_runtime_guard.RUNTIME_GUARD_CONSUMERS) | set(check_runtime_guard.APPROVAL_GUARD_CONSUMERS):
                path = root / "skills" / name / "SKILL.md"
                path.parent.mkdir(parents=True)
                text = check_runtime_guard.RUNTIME_GUARD_BLOCK if name in check_runtime_guard.RUNTIME_GUARD_CONSUMERS else ""
                if name in check_runtime_guard.APPROVAL_GUARD_CONSUMERS:
                    text += check_runtime_guard.APPROVAL_GUARD_BLOCK
                path.write_text(text)
            self.add_ui_guards(root)
            self.assertEqual(check_runtime_guard.validate_runtime_guard(root), [])
            path = root / "skills/tk-browser-verify/SKILL.md"
            original = path.read_text()
            for text in (original.replace(check_runtime_guard.APPROVAL_GUARD_BLOCK, ""), original + check_runtime_guard.APPROVAL_GUARD_BLOCK):
                path.write_text(text)
                errors = check_runtime_guard.validate_runtime_guard(root)
                self.assertTrue(any("tk-browser-verify" in error and "approval" in error for error in errors), errors)

    def test_ui_guard_missing_drifted_or_duplicated_fails_each_consumer(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for consumers, block in (
                (check_runtime_guard.RUNTIME_GUARD_CONSUMERS, check_runtime_guard.RUNTIME_GUARD_BLOCK),
                (check_runtime_guard.APPROVAL_GUARD_CONSUMERS, check_runtime_guard.APPROVAL_GUARD_BLOCK),
            ):
                for name in consumers:
                    path = root / "skills" / name / "SKILL.md"
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text((path.read_text() if path.exists() else "") + block)
            self.add_ui_guards(root)
            self.assertEqual(check_runtime_guard.validate_runtime_guard(root), [])
            for name in check_runtime_guard.UI_EVIDENCE_CONSUMERS:
                path = root / "skills" / name / "SKILL.md"
                original = path.read_text()
                for changed in (
                    original.replace(check_runtime_guard.UI_EVIDENCE_BLOCK, ""),
                    original.replace("every menu/breadcrumb", "the final menu/breadcrumb"),
                    original + check_runtime_guard.UI_EVIDENCE_BLOCK,
                ):
                    with self.subTest(consumer=name):
                        path.write_text(changed)
                        errors = check_runtime_guard.validate_runtime_guard(root)
                        self.assertTrue(any(name in error and "UI evidence" in error for error in errors), errors)
                path.write_text(original)

    def test_agents_cannot_own_runtime_guard_block(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in check_runtime_guard.RUNTIME_GUARD_CONSUMERS:
                skill = root / "skills" / name
                skill.mkdir(parents=True)
                (skill / "SKILL.md").write_text(
                    check_runtime_guard.RUNTIME_GUARD_BLOCK,
                    encoding="utf-8",
                )
            (root / "AGENTS.md").write_text(
                check_runtime_guard.RUNTIME_GUARD_BLOCK,
                encoding="utf-8",
            )
            errors = check_runtime_guard.validate_runtime_guard(root)
            self.assertTrue(any("AGENTS.md" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
