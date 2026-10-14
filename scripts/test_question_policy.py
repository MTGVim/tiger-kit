from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from question_policy import BLOCK, question_errors, question_template_errors, sync_questions


ROOT = Path(__file__).resolve().parents[1]
SINGLE = "```text\n## Questions\n\n❓ **Q1 · Scope**: Which scope?\n\n➡️ Keep the current scope.\n```\n"
MULTIPLE = SINGLE.replace("\n```", "\n\n❓ **Q2 · Approval**: Approve?\n```")


class QuestionTemplateTests(unittest.TestCase):
    def test_single_and_multiple_rounds_start_with_the_same_heading(self):
        for text in (SINGLE, MULTIPLE, SINGLE.replace("## Questions", "## 질문"), BLOCK):
            with self.subTest(text=text):
                self.assertEqual(question_template_errors(text, "example"), [])

    def test_missing_heading_in_a_single_round_is_rejected(self):
        self.assertTrue(question_template_errors(SINGLE.replace("## Questions\n\n", ""), "example"))

    def test_separator_cannot_replace_the_round_heading(self):
        self.assertTrue(question_template_errors(SINGLE.replace("## Questions", "---"), "example"))

    def test_horizontal_rules_are_rejected_even_with_blank_lines(self):
        for separator in ("---", "***", "___"):
            with self.subTest(separator=separator):
                errors = question_template_errors(MULTIPLE.replace("❓ **Q2", separator + "\n\n❓ **Q2"), "example")
                self.assertTrue(any("horizontal rules" in error for error in errors), errors)

    def test_synced_invalid_source_cannot_pass_by_matching_all_copies(self):
        for invalid in (SINGLE.replace("## Questions\n\n", ""),
                        MULTIPLE.replace("❓ **Q2", "---\n\n❓ **Q2")):
            with self.subTest(invalid=invalid), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                source = root / "skills/tk-grill/references/questions.md"
                source.parent.mkdir(parents=True)
                source.write_text(invalid, encoding="utf-8")
                shutil.copyfile(ROOT / "skills/tk-grill/LICENSE.txt", source.parent.parent / "LICENSE.txt")
                (source.parent.parent / "SKILL.md").write_text("# Grill\n", encoding="utf-8")
                sync_questions(root)
                self.assertTrue(any("canonical question rounds" in error for error in question_errors(root)))

    def test_sync_updates_every_package_without_losing_surrounding_content(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "skills/tk-grill/references/questions.md"
            source.parent.mkdir(parents=True)
            source.write_text(MULTIPLE, encoding="utf-8")
            shutil.copyfile(ROOT / "skills/tk-grill/LICENSE.txt", source.parent.parent / "LICENSE.txt")
            for name in ("tk-grill", "tk-example"):
                path = root / "skills" / name / "SKILL.md"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("# Existing owner\n\n" + BLOCK + "\n## Next guard\nKeep it.\n", encoding="utf-8")
            sync_questions(root)
            first = {path: path.read_bytes() for path in (root / "skills").rglob("*.md")}
            sync_questions(root)
            self.assertEqual(first, {path: path.read_bytes() for path in first})
            self.assertEqual(question_errors(root), [])
            for name in ("tk-grill", "tk-example"):
                path = root / "skills" / name / "SKILL.md"
                self.assertTrue(path.read_text().startswith("# Existing owner\n\n"))
                self.assertIn("## Next guard\nKeep it.", path.read_text())
                self.assertEqual((path.parent / "references/questions.md").read_bytes(), source.read_bytes())


if __name__ == "__main__":
    unittest.main()
