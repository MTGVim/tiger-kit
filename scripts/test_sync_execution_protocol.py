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
        for module in ("scripts.validate_skills", "scripts.run_seed_release_gate"):
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
        self.prep = self.root / "skills/tk-prep/references"
        self.respond = self.root / "skills/tk-pr-respond/references"
        self.review = self.root / "skills/tk-review/references"
        self.wizard = self.root / "skills/tk-wizard/references"
        self.clear_source = self.root / "skills/tk-rewrite/references/clear-writing.md"
        self.clear_target = self.root / "skills/tk-explain/references/clear-writing.md"
        self.clear_source.parent.mkdir(parents=True)
        self.clear_source.write_text("Preserve context. 한국어 예시.\n", encoding="utf-8")
        self.domain_targets = tuple(
            self.root / f"skills/{name}/references/domain-context.md"
            for name in ("tk-ask-repo", "tk-audit", "tk-pr-open", "tk-pr-respond", "tk-review")
        )
        for directory in (self.prep, self.respond, self.review, self.wizard):
            directory.mkdir(parents=True, exist_ok=True)
        for name in sync_execution_protocol.FILES:
            (self.prep / name).write_text(f"execution {name}\n", encoding="utf-8")
        (self.prep / "domain-context.md").write_text("domain\n", encoding="utf-8")
        for name in sync_execution_protocol.REVIEW_FILES:
            (self.review / name).write_text(f"review {name}\n", encoding="utf-8")
        (self.prep / "external-contracts.md").write_text("external\n", encoding="utf-8")
        questions = self.root / "skills/tk-grill/references/questions.md"
        questions.parent.mkdir(parents=True)
        questions.write_text("Canonical frontier protocol\n", encoding="utf-8")
        (questions.parent.parent / "SKILL.md").write_text("# Grill\n", encoding="utf-8")
        notice = Path(__file__).resolve().parents[1] / "skills/tk-grill/LICENSE.txt"
        shutil.copyfile(notice, questions.parent.parent / "LICENSE.txt")
        research = self.root / "skills/tk-research/references/evidence.md"
        research.parent.mkdir(parents=True)
        research.write_text("Primary evidence\n", encoding="utf-8")
        self.clear_target.parent.mkdir(parents=True, exist_ok=True)
        (self.clear_target.parent / "html-output.md").write_text("Offline native navigation\n", encoding="utf-8")
        (self.clear_target.parent / "visual-grammar.md").write_text("Question-led representation\n", encoding="utf-8")
        discovery = self.root / "skills/tk-audit/references/repository-context.md"
        discovery.parent.mkdir(parents=True, exist_ok=True)
        discovery.write_text("Optional context, not authority\n", encoding="utf-8")
        canonical = Path(__file__).resolve().parents[1] / "skills/tk-browser-verify"
        fixture = self.root / "skills/tk-browser-verify"
        for directory, names in (("references", verification_policy.REFERENCES),
                                 ("scripts", (verification_policy.SCRIPT,))):
            (fixture / directory).mkdir(parents=True, exist_ok=True)
            for name in names:
                shutil.copyfile(canonical / directory / name, fixture / directory / name)
        # Build installed packages because sync now validates their conditional guards too.
        for consumers, block in (
            (check_runtime_guard.RUNTIME_GUARD_CONSUMERS, check_runtime_guard.RUNTIME_GUARD_BLOCK),
            (check_runtime_guard.APPROVAL_GUARD_CONSUMERS, check_runtime_guard.APPROVAL_GUARD_BLOCK),
            (check_runtime_guard.UI_EVIDENCE_CONSUMERS, check_runtime_guard.UI_EVIDENCE_BLOCK),
        ):
            for name in consumers:
                path = self.root / "skills" / name / "SKILL.md"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text((path.read_text() if path.exists() else "") + block)
        repo = Path(__file__).resolve().parents[1]
        for name in sync_execution_protocol.HTML_CONSUMERS:
            assets = self.root / "skills" / name / "assets"
            assets.mkdir(parents=True, exist_ok=True)
            for asset in sync_execution_protocol.HTML_ASSETS:
                shutil.copyfile(repo / "skills/tk-explain/assets" / asset, assets / asset)
        for relative in sync_execution_protocol.HTML_TEMPLATES:
            shutil.copyfile(repo / relative, self.root / relative)

    def run_main(self, *args: str) -> int:
        with (
            patch.object(sync_execution_protocol, "ROOT", self.root),
            patch.object(sync_execution_protocol, "SOURCE", self.prep),
            patch.object(sync_execution_protocol, "TARGET", self.respond),
            patch.object(sync_execution_protocol, "REVIEW_SOURCE", self.review),
            patch.object(sync_execution_protocol, "REVIEW_TARGETS", (self.prep, self.respond)),
            patch.object(
                sync_execution_protocol,
                "EXTERNAL_CONTRACT_SOURCE",
                self.prep / "external-contracts.md",
            ),
            patch.object(
                sync_execution_protocol,
                "EXTERNAL_CONTRACT_TARGET",
                self.wizard / "external-contracts.md",
            ),
            patch.object(sync_execution_protocol, "DOMAIN_CONTEXT_TARGETS", self.domain_targets),
            patch.object(sync_execution_protocol, "CLEAR_WRITING_SOURCE", self.clear_source),
            patch.object(sync_execution_protocol, "CLEAR_WRITING_TARGET", self.clear_target),
            patch.object(sys, "argv", ["sync_execution_protocol.py", *args]),
            redirect_stdout(io.StringIO()),
        ):
            return sync_execution_protocol.main()

    def test_sync_creates_missing_copies_and_clean_check_passes(self) -> None:
        self.assertEqual(self.run_main(), 0)
        self.assertEqual(self.run_main("--check"), 0)
        for name in sync_execution_protocol.REVIEW_FILES:
            expected = (self.review / name).read_bytes()
            self.assertEqual((self.prep / name).read_bytes(), expected)
            self.assertEqual((self.respond / name).read_bytes(), expected)
        self.assertFalse((self.root / "skills/tk-autoresearch").exists())
        for name in ("clear-writing.md", "html-output.md", "visual-grammar.md"):
            self.assertEqual((self.root / "skills/tk-research/references" / name).read_bytes(),
                             (self.root / "skills/tk-explain/references" / name).read_bytes())
        context = (self.root / "skills/tk-audit/references/repository-context.md").read_bytes()
        for name in ("tk-prep", "tk-research"):
            self.assertEqual((self.root / "skills" / name / "references/repository-context.md").read_bytes(), context)
        expected_domain = (self.prep / "domain-context.md").read_bytes()
        for target in self.domain_targets:
            self.assertEqual(target.read_bytes(), expected_domain)
        self.assertEqual(
            (self.wizard / "external-contracts.md").read_bytes(),
            (self.prep / "external-contracts.md").read_bytes(),
        )

    def test_research_and_repository_context_drift_fail_and_repair(self) -> None:
        self.assertEqual(self.run_main(), 0)
        for name in ("html-output.md", "clear-writing.md", "repository-context.md"):
            stale = self.root / "skills/tk-research/references" / name
            stale.write_text("stale\n", encoding="utf-8")
            self.assertEqual(self.run_main("--check"), 1)
            self.assertEqual(self.run_main(), 0)
            self.assertEqual(self.run_main("--check"), 0)

    def test_check_fails_for_stale_copy_and_sync_repairs_it(self) -> None:
        self.assertEqual(self.run_main(), 0)
        stale = self.respond / "security.md"
        stale.write_text("stale\n", encoding="utf-8")
        self.assertEqual(self.run_main("--check"), 1)
        self.assertEqual(self.run_main(), 0)
        self.assertEqual(stale.read_bytes(), (self.review / "security.md").read_bytes())

    def test_installed_notice_is_required_and_sync_preserves_other_attribution(self) -> None:
        self.assertEqual(self.run_main(), 0)
        notice = self.root / "skills/tk-prep/LICENSE.txt"
        notice.write_text("Existing unrelated attribution\n", encoding="utf-8")
        self.assertEqual(self.run_main("--check"), 1)
        self.assertEqual(self.run_main(), 0)
        restored = notice.read_bytes()
        self.assertTrue(restored.startswith(b"Existing unrelated attribution\n"))
        self.assertIn(b"Copyright (c) 2026 Matt Pocock", restored)
        self.assertEqual(self.run_main(), 0)
        self.assertEqual(notice.read_bytes(), restored)
        self.assertEqual(self.run_main("--check"), 0)

    def test_incomplete_canonical_notice_is_rejected_and_repaired(self) -> None:
        self.assertEqual(self.run_main(), 0)
        notice = self.root / "skills/tk-grill/LICENSE.txt"
        notice.write_text("MIT License\nCopyright (c) 2026 Matt Pocock\n", encoding="utf-8")
        self.assertEqual(self.run_main("--check"), 1)
        self.assertEqual(self.run_main(), 0)
        self.assertEqual(self.run_main("--check"), 0)

    def test_app_provider_contract_drift_blocks_check_and_sync_repairs_it(self) -> None:
        self.assertEqual(self.run_main(), 0)
        stale = self.root / "skills/tk-app-verify/references/providers.json"
        stale.write_text('{"version":1,"providers":[]}')
        self.assertEqual(self.run_main("--check"), 1)
        self.assertEqual(self.run_main(), 0)
        self.assertEqual(self.run_main("--check"), 0)

    def test_clear_writing_check_detects_both_sides_drift_and_missing_consumer(self) -> None:
        self.assertEqual(self.run_main(), 0)
        for mutation in ("consumer", "canonical", "missing"):
            with self.subTest(mutation=mutation):
                if mutation == "missing":
                    self.clear_target.unlink()
                else:
                    changed = self.clear_source if mutation == "canonical" else self.clear_target
                    changed.write_text(f"{mutation} change: 한국어 예시.\n", encoding="utf-8")
                self.assertEqual(self.run_main("--check"), 1)
                self.assertEqual(self.run_main(), 0)
                self.assertEqual(self.clear_target.read_bytes(), self.clear_source.read_bytes())
                self.assertEqual(self.run_main("--check"), 0)


    def test_visual_grammar_drift_missing_copy_and_canonical_change_fail_check(self) -> None:
        self.assertEqual(self.run_main(), 0)
        canonical = self.clear_target.parent / "visual-grammar.md"
        consumer = self.root / "skills/tk-study/references/visual-grammar.md"
        for mutation in ("consumer", "missing", "canonical"):
            with self.subTest(mutation=mutation):
                if mutation == "missing":
                    consumer.unlink()
                else:
                    (consumer if mutation == "consumer" else canonical).write_text("Altered geometry\n")
                self.assertEqual(self.run_main("--check"), 1)
                self.assertEqual(self.run_main(), 0)
                self.assertEqual(consumer.read_bytes(), canonical.read_bytes())
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
