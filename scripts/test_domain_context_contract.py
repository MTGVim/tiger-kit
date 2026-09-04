from __future__ import annotations

import unittest
from pathlib import Path

import sync_execution_protocol


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_CONSUMERS = (
    "tk-prep",
    "tk-ask-repo",
    "tk-audit",
    "tk-pr-open",
    "tk-pr-respond",
    "tk-review",
)
EXPECTED_TARGETS = tuple(
    ROOT / f"skills/{name}/references/domain-context.md"
    for name in EXPECTED_CONSUMERS
    if name != "tk-prep"
)
DOMAIN_POINTER = "[domain context](references/domain-context.md)"


class DomainContextContractTest(unittest.TestCase):
    def test_sync_targets_cover_exact_expected_consumers(self) -> None:
        self.assertEqual(sync_execution_protocol.DOMAIN_CONTEXT_TARGETS, EXPECTED_TARGETS)

    def test_shared_domain_context_copies_match_canonical(self) -> None:
        canonical = ROOT / "skills/tk-prep/references/domain-context.md"
        expected = canonical.read_bytes()
        for target in EXPECTED_TARGETS:
            self.assertEqual(target.read_bytes(), expected, str(target.relative_to(ROOT)))

    def test_each_semantic_consumer_points_to_domain_context(self) -> None:
        for name in EXPECTED_CONSUMERS:
            skill = ROOT / "skills" / name / "SKILL.md"
            self.assertIn(DOMAIN_POINTER, skill.read_text(encoding="utf-8"), name)


if __name__ == "__main__":
    unittest.main()
