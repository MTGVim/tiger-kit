from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from check_token_budget import static_errors

SCRIPT = Path(__file__).with_name("check_token_budget.py")


class RequiredReadBudgetTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skill = self.root / "skills/tk-example/SKILL.md"
        self.skill.parent.mkdir(parents=True)
        self.skill.write_text('---\nname: tk-example\ndescription: example\n---\n\nRead [required](references/required.md).\n', encoding="utf-8")
        ref = self.skill.parent / "references/required.md"
        ref.parent.mkdir()
        ref.write_text("Required evidence.\n", encoding="utf-8")
        self.manifest_path = self.root / "evals/token-budget.json"
        self.manifest_path.parent.mkdir()
        self.manifest = {
            "version": 1,
            "limits": {
                "max_skill_md_bytes": 10000,
                "max_total_skill_md_bytes": 10000,
                "max_skill_md_chars": 10000,
                "max_total_description_chars": 1000,
                "max_single_description_chars": 1000,
                "max_shared_block_bytes": 10000,
                "max_shared_block_ratio_ppm": 1000000,
                "always_read": {"example": {
                    "entrypoint": "skills/tk-example/SKILL.md",
                    "paths": ["skills/tk-example/SKILL.md"],
                    "max_bytes": 10000,
                }},
            },
        }

    def save(self):
        self.manifest_path.write_text(json.dumps(self.manifest), encoding="utf-8")

    def test_missing_direct_required_read_fails_real_check_command(self):
        self.save()
        result = subprocess.run([sys.executable, "-B", str(SCRIPT), "--check", "--candidate", str(self.root)], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("references/required.md", result.stdout + result.stderr)
        self.assertIn("required read", (result.stdout + result.stderr).lower())


    def include_required(self):
        self.manifest["limits"]["always_read"]["example"]["paths"].append("skills/tk-example/references/required.md")

    def test_complete_profile_counts_real_bytes_and_passes(self):
        self.include_required()
        self.save()
        errors, metrics, _ = static_errors(self.root)
        self.assertEqual([], errors)
        self.assertEqual(self.skill.stat().st_size + len(b"Required evidence.\n"), metrics["always_read:example"])

    def test_conditional_and_fenced_read_examples_are_not_universal_load(self):
        self.include_required()
        with self.skill.open("a", encoding="utf-8") as stream:
            stream.write("\nFor requested video, read [optional](references/video.md).\n\n```text\nRead [example](references/example.md).\n```\n")
        self.save()
        self.assertEqual([], static_errors(self.root)[0])

    def test_valid_fenced_examples_do_not_fail_the_real_command(self):
        self.include_required()
        original = self.skill.read_text(encoding="utf-8")
        for opening, closing in [("   ```text", "   ```"), ("```text", "````"), ("   ~~~text", "   ~~~~")]:
            with self.subTest(opening=opening, closing=closing):
                self.skill.write_text(original + f"\n{opening}\nRead [example](references/example.md).\n{closing}\n", encoding="utf-8")
                self.save()
                result = subprocess.run([sys.executable, "-B", str(SCRIPT), "--check", "--candidate", str(self.root)], capture_output=True, text=True)
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_wrapped_second_link_fails_the_real_command(self):
        self.include_required()
        (self.skill.parent / "references/new.md").write_text("New requirement.\n", encoding="utf-8")
        with self.skill.open("a", encoding="utf-8") as stream:
            stream.write("\nRead [required](references/required.md) and\n[new](references/new.md).\n")
        self.save()
        result = subprocess.run([sys.executable, "-B", str(SCRIPT), "--check", "--candidate", str(self.root)], capture_output=True, text=True)
        self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("references/new.md", result.stdout + result.stderr)

    def test_wrapped_read_directive_cannot_hide_its_reference(self):
        self.skill.write_text("# Example\n\nRead\n[required](references/required.md).\n", encoding="utf-8")
        self.save()
        self.assertTrue(any("references/required.md" in error for error in static_errors(self.root)[0]))

    def test_new_explicit_read_is_detected_without_a_second_required_path_list(self):
        self.include_required()
        (self.skill.parent / "references/new.md").write_text("New requirement.\n", encoding="utf-8")
        with self.skill.open("a", encoding="utf-8") as stream:
            stream.write("\n- Read [new](references/new.md#check).\n")
        self.save()
        self.assertTrue(any("required read" in error and "references/new.md" in error for error in static_errors(self.root)[0]))

    def test_non_skill_entrypoint_is_rejected(self):
        (self.root / "notes.md").write_text("Not a skill entrypoint.\n", encoding="utf-8")
        profile = self.manifest["limits"]["always_read"]["example"]
        profile["entrypoint"] = "notes.md"
        profile["paths"] = ["notes.md"]
        self.save()
        self.assertTrue(any("entrypoint" in error for error in static_errors(self.root)[0]))

    def test_missing_entrypoint_cannot_disable_coverage(self):
        self.include_required()
        del self.manifest["limits"]["always_read"]["example"]["entrypoint"]
        self.save()
        self.assertTrue(any("entrypoint" in error for error in static_errors(self.root)[0]))

    def test_entrypoint_must_be_counted(self):
        self.include_required()
        self.manifest["limits"]["always_read"]["example"]["paths"].remove("skills/tk-example/SKILL.md")
        self.save()
        self.assertTrue(any("required read entrypoint missing" in error for error in static_errors(self.root)[0]))

    def test_existing_byte_ceiling_still_rejects_complete_overbudget_profile(self):
        self.include_required()
        self.manifest["limits"]["always_read"]["example"]["max_bytes"] = 1
        self.save()
        self.assertTrue(any("token budget exceeded: always_read:example" in error for error in static_errors(self.root)[0]))

    def test_symlinked_required_read_cannot_escape_repository(self):
        self.include_required()
        with tempfile.TemporaryDirectory() as outside:
            other = Path(outside) / "private.md"
            other.write_text("Outside content must not be read.\n", encoding="utf-8")
            (self.skill.parent / "references/escape.md").symlink_to(other)
            with self.skill.open("a", encoding="utf-8") as stream:
                stream.write("\nRead [escape](references/escape.md).\n")
            self.save()
            errors, _, _ = static_errors(self.root)
        self.assertTrue(any("unsafe required read" in error for error in errors))

    def test_page_scoped_renderer_read_is_required_for_page_profile(self):
        self.include_required()
        with self.skill.open("a", encoding="utf-8") as stream:
            stream.write("\nFor explanation pages, read [renderer](references/renderer.md).\n")
        self.save()
        self.assertTrue(any("references/renderer.md" in error for error in static_errors(self.root)[0]))

    def test_invalid_profile_collection_returns_error_instead_of_crashing(self):
        self.manifest["limits"]["always_read"] = []
        self.save()
        errors, _, _ = static_errors(self.root)
        self.assertTrue(any("always_read must be an object" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
