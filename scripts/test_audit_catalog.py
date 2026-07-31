#!/usr/bin/env python3
from __future__ import annotations

import unittest

import audit_catalog


class CatalogAuditTest(unittest.TestCase):
    def test_current_catalog_has_objective_contracts(self) -> None:
        result = audit_catalog.audit()
        self.assertGreater(result["skill_count"], 0)
        for row in result["skills"]:
            self.assertIn("success", row["behavior_paths"])
            self.assertIn("boundary", row["behavior_paths"])
            self.assertIn(row["disposition"], {"Keep", "Review"})

    def test_drive_removal_requires_experiment_evidence(self) -> None:
        baseline = audit_catalog.audit()
        drive = next(row for row in baseline["skills"] if row["skill"] == "tk-drive")
        self.assertNotEqual(drive["disposition"], "ReviewRemoval")

        with_experiment = audit_catalog.audit({"decision": "RemoveCandidate"})
        drive = next(row for row in with_experiment["skills"] if row["skill"] == "tk-drive")
        self.assertEqual(drive["disposition"], "ReviewRemoval")

    def test_non_removal_experiment_keeps_drive(self) -> None:
        result = audit_catalog.audit({"decision": "Keep"})
        drive = next(row for row in result["skills"] if row["skill"] == "tk-drive")
        self.assertEqual(drive["disposition"], "Keep")
        self.assertIn("drive experiment: Keep", drive["basis"])


if __name__ == "__main__":
    unittest.main()
