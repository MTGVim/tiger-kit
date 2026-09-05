from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PREP = ROOT / "skills/tk-prep/references"
RESPOND = ROOT / "skills/tk-pr-respond/references"


class SddUpstreamBoundaryTest(unittest.TestCase):
    def test_material_residual_ruling_blocks_destructive_cleanup(self) -> None:
        text = (PREP / "sdd.md").read_text(encoding="utf-8")
        self.assertIn("material deferred or accepted `Ruling:`", text)
        self.assertIn("otherwise retain the existing ledger as the recovery record", text)
        self.assertIn("solely for style/minor findings", text)
        self.assertIn("do not create a\nfollow-up artifact just to make cleanup possible", text)
        self.assertIn("artifacts that satisfy the Recovery\nstate retention rule above", text)

    def test_unknown_failure_routes_to_one_fresh_diagnostic_leaf_only(self) -> None:
        text = (PREP / "sdd.md").read_text(encoding="utf-8")
        self.assertIn("obvious failure with an exact RED seam owned by the\ncurrent `Unit`", text)
        self.assertIn("dispatches one fresh diagnostic leaf", text)
        self.assertIn("without product remediation or redispatch", text)
        self.assertIn("Do not create diagnosis state merely for this\nbranch", text)

    def test_sdd_diagnostic_leaf_returns_before_product_remediation(self) -> None:
        text = (PREP / "diagnosis.md").read_text(encoding="utf-8")
        self.assertIn("When this procedure runs as an SDD diagnostic leaf", text)
        self.assertIn("before any product remediation", text)
        self.assertIn("controller owns routing back to the current `Unit`", text)

    def test_shared_sdd_and_diagnosis_copies_remain_exact(self) -> None:
        for name in ("sdd.md", "diagnosis.md"):
            self.assertEqual((PREP / name).read_bytes(), (RESPOND / name).read_bytes(), name)


if __name__ == "__main__":
    unittest.main()
