#!/usr/bin/env python3
from __future__ import annotations

import unittest
from unittest.mock import patch

import audit_catalog


class CatalogAuditTest(unittest.TestCase):
    def test_current_catalog_has_objective_contracts(self) -> None:
        result = audit_catalog.audit()
        self.assertGreater(result["skill_count"], 0)
        for row in result["skills"]:
            self.assertIn("success", row["behavior_paths"])
            self.assertIn("boundary", row["behavior_paths"])
            self.assertIn(row["disposition"], {"ContractComplete", "Review"})
        self.assertEqual(result["contract_complete_count"], result["skill_count"])
        self.assertNotIn("keep_count", result)

    def test_drive_removal_requires_experiment_evidence(self) -> None:
        baseline = audit_catalog.audit()
        drive = next(row for row in baseline["skills"] if row["skill"] == "tk-drive")
        self.assertNotEqual(drive["disposition"], "ReviewRemoval")

        with_experiment = audit_catalog.audit({"decision": "RemoveCandidate"})
        drive = next(row for row in with_experiment["skills"] if row["skill"] == "tk-drive")
        self.assertEqual(drive["disposition"], "ReviewRemoval")

    def test_non_removal_experiment_keeps_drive_contract_complete(self) -> None:
        result = audit_catalog.audit({"decision": "Keep"})
        drive = next(row for row in result["skills"] if row["skill"] == "tk-drive")
        self.assertEqual(drive["disposition"], "ContractComplete")
        self.assertIn("drive experiment: Keep", drive["basis"])

    def test_user_invocation_does_not_replace_consumer_evidence(self) -> None:
        skills = audit_catalog.validate_skills.discover_skills()
        names = set(skills)
        explicit = next(
            name
            for name, (_, data, _) in skills.items()
            if audit_catalog.validate_skills.nested(
                data, "metadata", "tigerkit", "kind"
            )
            == "user-invoked"
        )
        with (
            patch.object(
                audit_catalog,
                "catalog_consumers",
                return_value={name: set() for name in names},
            ),
            patch.object(
                audit_catalog,
                "drive_consumers",
                return_value={name: False for name in names},
            ),
        ):
            result = audit_catalog.audit()

        row = next(row for row in result["skills"] if row["skill"] == explicit)
        self.assertEqual(row["disposition"], "Review")


if __name__ == "__main__":
    unittest.main()
