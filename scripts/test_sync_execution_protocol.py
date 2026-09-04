from __future__ import annotations

import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import sync_execution_protocol


class SyncExecutionProtocolTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.prep = self.root / "skills/tk-prep/references"
        self.respond = self.root / "skills/tk-pr-respond/references"
        self.review = self.root / "skills/tk-review/references"
        self.wizard = self.root / "skills/tk-wizard/references"
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
        expected_domain = (self.prep / "domain-context.md").read_bytes()
        for target in self.domain_targets:
            self.assertEqual(target.read_bytes(), expected_domain)
        self.assertEqual(
            (self.wizard / "external-contracts.md").read_bytes(),
            (self.prep / "external-contracts.md").read_bytes(),
        )

    def test_check_fails_for_stale_copy_and_sync_repairs_it(self) -> None:
        self.assertEqual(self.run_main(), 0)
        stale = self.respond / "security.md"
        stale.write_text("stale\n", encoding="utf-8")
        self.assertEqual(self.run_main("--check"), 1)
        self.assertEqual(self.run_main(), 0)
        self.assertEqual(stale.read_bytes(), (self.review / "security.md").read_bytes())


if __name__ == "__main__":
    unittest.main()
