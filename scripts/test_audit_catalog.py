from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

import audit_catalog


class AuditCatalogTests(unittest.TestCase):
    def test_positive_trigger_count(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory)
            (skill / "evals").mkdir()
            (skill / "evals/triggers.json").write_text(
                '{"queries":[{"should_trigger":true},{"should_trigger":false}]}',
                encoding="utf-8",
            )
            self.assertEqual(audit_catalog.positive_trigger_count(skill), 1)

    def test_behavior_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory)
            (skill / "evals").mkdir()
            (skill / "evals/evals.json").write_text(
                '{"evals":[{"path":"success"},{"path":"boundary"}]}',
                encoding="utf-8",
            )
            self.assertEqual(
                audit_catalog.behavior_paths(skill),
                {"success", "boundary"},
            )


if __name__ == "__main__":
    unittest.main()
