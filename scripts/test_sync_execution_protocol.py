from __future__ import annotations

import io
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import sync_execution_protocol
import check_runtime_guard
import verification_policy


class SyncExecutionProtocolTest(unittest.TestCase):
    def test_package_entry_points_remain_executable(self) -> None:
        for module in ("scripts.validate_skills", "scripts.run_seed_release_checklist"):
            with self.subTest(module=module):
                result = subprocess.run(
                    [sys.executable, "-B", "-m", module, "--help"],
                    cwd=Path(__file__).resolve().parents[1],
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue(result.stdout.strip())

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(Path(__file__).resolve().parents[1] / "skills", self.root / "skills")

    def run_main(self, *args: str) -> int:
        with (
            patch.object(sync_execution_protocol, "ROOT", self.root),
            patch.object(sys, "argv", ["sync_execution_protocol.py", *args]),
            redirect_stdout(io.StringIO()),
        ):
            return sync_execution_protocol.main()

    def test_question_theme_assets_are_distributed_and_drift_is_repaired(self) -> None:
        self.assertEqual(self.run_main(), 0)
        for name in ("tk-prep", "tk-grill", "tk-roadmap"):
            for asset in ("html-theme.css", "html-theme.js"):
                with self.subTest(skill=name, asset=asset):
                    target = self.root / "skills" / name / "assets" / asset
                    canonical = self.root / "skills/tk-explain/assets" / asset
                    self.assertTrue(target.is_file(), str(target))
                    self.assertEqual(target.read_bytes(), canonical.read_bytes())
                    target.write_text("drift\n", encoding="utf-8")
                    self.assertEqual(self.run_main("--check"), 1)
                    self.assertEqual(self.run_main(), 0)
                    self.assertEqual(target.read_bytes(), canonical.read_bytes())
                    target.unlink()
                    self.assertEqual(self.run_main("--check"), 1)
                    self.assertEqual(self.run_main(), 0)
        self.assertEqual(self.run_main("--check"), 0)

    def test_feedback_memory_boundary_drift_blocks_check_and_repairs(self) -> None:
        self.assertEqual(self.run_main(), 0)
        path = self.root / "skills/tk-prep/SKILL.md"
        text = path.read_text(encoding="utf-8")
        path.write_text(text.replace("in the current conversation", "in persistent memory"), encoding="utf-8")
        self.assertEqual(self.run_main("--check"), 1)
        self.assertEqual(self.run_main(), 0)
        self.assertEqual(self.run_main("--check"), 0)

    def test_summary_body_guard_missing_or_drifted_blocks_release_check(self) -> None:
        self.assertEqual(self.run_main(), 0)
        for name in sync_execution_protocol.SUMMARY_BODY_ANCHORS:
            path = self.root / "skills" / name / "SKILL.md"
            original = path.read_text(encoding="utf-8")
            for replacement in ("", sync_execution_protocol.SUMMARY_BODY_BLOCK.replace("fresh-read", "trust")):
                with self.subTest(skill=name, missing=not replacement):
                    path.write_text(original.replace(sync_execution_protocol.SUMMARY_BODY_BLOCK, replacement), encoding="utf-8")
                    self.assertEqual(self.run_main("--check"), 1)
                    self.assertEqual(self.run_main(), 0)
                    self.assertEqual(self.run_main("--check"), 0)

    def test_result_summary_drift_fails_check_and_sync_repairs_it(self) -> None:
        self.assertEqual(self.run_main(), 0)
        path = self.root / "skills/tk-grill/SKILL.md"
        path.write_text(path.read_text(encoding="utf-8").replace(sync_execution_protocol.RESULT_SUMMARY_BLOCK, sync_execution_protocol.RESULT_SUMMARY_BLOCK.replace("Return", "Skip", 1)), encoding="utf-8")
        self.assertEqual(self.run_main("--check"), 1)
        self.assertEqual(self.run_main(), 0)
        self.assertEqual(self.run_main("--check"), 0)
        self.assertIn(sync_execution_protocol.RESULT_SUMMARY_BLOCK, path.read_text(encoding="utf-8"))




    def test_shared_notice_is_required_and_sync_preserves_attribution(self) -> None:
        self.assertEqual(self.run_main(), 0)
        notice = self.root / "skills/tk-questioning/LICENSE.txt"
        original = notice.read_text()
        notice.write_text("Existing unrelated attribution\n")
        self.assertEqual(self.run_main("--check"), 1)
        self.assertEqual(self.run_main(), 0)
        self.assertEqual(notice.read_text(), "Existing unrelated attribution\n")
        self.assertEqual(self.run_main("--check"), 1)
        notice.write_text("Existing unrelated attribution\n" + original)
        self.assertEqual(self.run_main("--check"), 0)

    def test_incomplete_canonical_notice_is_rejected_without_synthesizing_license(self) -> None:
        self.assertEqual(self.run_main(), 0)
        notice = self.root / "skills/tk-questioning/LICENSE.txt"
        notice.write_text("MIT License\nCopyright (c) 2026 Matt Pocock\n")
        self.assertEqual(self.run_main("--check"), 1)
        self.assertEqual(self.run_main(), 0)
        self.assertEqual(self.run_main("--check"), 1)

    def test_sync_never_recreates_reference_copies_and_missing_owner_stays_blocked(self) -> None:
        from shared_references import SHARED_REFERENCES
        self.assertEqual(self.run_main(), 0)
        self.assertEqual(self.run_main("--check"), 0)
        for originals in SHARED_REFERENCES.values():
            for original in originals:
                self.assertFalse((self.root / original).exists(), original)
        target = self.root / "skills/tk-engineering/references/sdd.md"
        target.unlink()
        self.assertEqual(self.run_main("--check"), 1)
        self.assertEqual(self.run_main(), 0)
        self.assertFalse(target.exists())
        self.assertEqual(self.run_main("--check"), 1)

    def test_missing_dependency_declaration_blocks_check(self) -> None:
        self.assertEqual(self.run_main(), 0)
        (self.root / "skills/tk-prep/dependencies.json").unlink()
        self.assertEqual(self.run_main("--check"), 1)

    def test_app_provider_contract_drift_blocks_check_and_sync_repairs_it(self) -> None:
        self.assertEqual(self.run_main(), 0)
        stale = self.root / "skills/tk-app-verify/references/providers.json"
        stale.write_text('{"version":1,"providers":[]}')
        self.assertEqual(self.run_main("--check"), 1)
        self.assertEqual(self.run_main(), 0)
        self.assertEqual(self.run_main("--check"), 0)


    def test_chart_reference_and_recipe_drift_are_repaired(self) -> None:
        self.assertEqual(self.run_main(), 0)
        for relative in (*sync_execution_protocol.CHART_FILES, *sync_execution_protocol.ASSEMBLY_FILES, *sync_execution_protocol.READER_FILES, *sync_execution_protocol.ARCHIFY_FILES,
                         "scripts/package_html.py", "scripts/highlight_code.py"):
            consumer = self.root / "skills/tk-research" / relative
            canonical = self.root / "skills/tk-explain" / relative
            consumer.write_text("Stale chart recipe\n", encoding="utf-8")
            self.assertEqual(self.run_main("--check"), 1)
            self.assertEqual(self.run_main(), 0)
            self.assertEqual(consumer.read_bytes(), canonical.read_bytes())
            consumer.unlink()
            self.assertEqual(self.run_main("--check"), 1)
            self.assertEqual(self.run_main(), 0)
        self.assertEqual(self.run_main("--check"), 0)



class OutputNotationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = self.root / "skills/tk-example/SKILL.md"
        self.path.parent.mkdir(parents=True)
        self.path.write_text("# Example\n\nKeep this behavior.\n", encoding="utf-8")

    def test_missing_guard_is_rejected_and_sync_is_idempotent(self) -> None:
        self.assertTrue(sync_execution_protocol.output_notation_errors(self.root / "skills"))
        sync_execution_protocol.sync_output_notation(self.root / "skills")
        before = self.path.read_bytes()
        sync_execution_protocol.sync_output_notation(self.root / "skills")
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(sync_execution_protocol.output_notation_errors(self.root / "skills"), [])

    def test_drift_is_rejected_and_repaired_without_losing_adjacent_guard(self) -> None:
        sync_execution_protocol.sync_output_notation(self.root / "skills")
        original = self.path.read_text()
        suffix = "\n## Other behavior\nKeep this instruction.\n\n<!-- tigerkit:other -->\n## Other\nKeep this guard.\n"
        self.path.write_text(original.replace("ASCII numbering", "emoji numbering") + suffix)
        self.assertTrue(sync_execution_protocol.output_notation_errors(self.root / "skills"))
        sync_execution_protocol.sync_output_notation(self.root / "skills")
        self.assertEqual(self.path.read_text(), original + suffix)
        self.assertEqual(sync_execution_protocol.output_notation_errors(self.root / "skills"), [])

    def test_duplicate_guard_is_rejected(self) -> None:
        self.path.write_text(sync_execution_protocol.OUTPUT_NOTATION_BLOCK * 2)
        self.assertTrue(sync_execution_protocol.output_notation_errors(self.root / "skills"))


if __name__ == "__main__":
    unittest.main()
