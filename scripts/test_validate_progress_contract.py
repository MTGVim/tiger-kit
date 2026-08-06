#!/usr/bin/env python3
from __future__ import annotations

import unittest

import validate_progress_contract


class ProgressContractTest(unittest.TestCase):
    def test_current_repository_uses_optional_core_contract(self) -> None:
        self.assertEqual(validate_progress_contract.validate_all(), [])

    def test_missing_space_and_legacy_marker_are_rejected(self) -> None:
        text = (
            "Progress is optional and nonterminal: 🚗 active, 🙋 response, ⏳ wait\n"
            "🚗  active 👀 no-op ❓ question"
        )
        errors = validate_progress_contract.validate_skill_text("fixture", text)
        self.assertTrue(any("must be followed" in error for error in errors))
        self.assertTrue(any("legacy progress marker '👀'" in error for error in errors))
        self.assertTrue(any("legacy progress marker '❓'" in error for error in errors))

    def test_progress_section_is_optional(self) -> None:
        self.assertEqual(
            validate_progress_contract.validate_skill_text("fixture", "Status: Pass"), []
        )

    def test_references_are_checked_without_requiring_the_skill_heading(self) -> None:
        errors = validate_progress_contract._validate_markers(
            "reference", "Lead with `🤖 drive > finalization`.", require_all=False
        )
        self.assertEqual(len(errors), 1)
        self.assertIn("legacy progress route", errors[0])


if __name__ == "__main__":
    unittest.main()
