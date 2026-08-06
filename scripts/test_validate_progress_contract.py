#!/usr/bin/env python3
from __future__ import annotations

import unittest

import validate_progress_contract


class ProgressContractTest(unittest.TestCase):
    def test_current_repository_uses_one_spaced_contract(self) -> None:
        self.assertEqual(validate_progress_contract.validate_all(), [])

    def test_missing_space_and_legacy_marker_are_rejected(self) -> None:
        text = (
            "When progress or a nonterminal status is shown, use these compact markers: "
            "🚗 active, 🙋 response, ❓ question, ⏳ wait, 🛑 stop, ✅ done, ❌ failure\n"
            "🚗  active 👀 no-op"
        )
        errors = validate_progress_contract.validate_skill_text("fixture", text)
        self.assertTrue(any("must be followed" in error for error in errors))
        self.assertTrue(any("legacy progress marker '👀'" in error for error in errors))

    def test_references_are_checked_without_requiring_the_skill_heading(self) -> None:
        errors = validate_progress_contract._validate_markers(
            "reference", "Lead with `🤖 drive > finalization`.", require_all=False
        )
        self.assertEqual(len(errors), 1)
        self.assertIn("legacy progress route", errors[0])


if __name__ == "__main__":
    unittest.main()
