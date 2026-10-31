from __future__ import annotations

import unittest
from pathlib import Path



ROOT = Path(__file__).resolve().parents[1]
EXPECTED_CONSUMERS = (
    "tk-prep",
    "tk-ask-repo",
    "tk-audit",
    "tk-pr-open",
    "tk-pr-respond",
    "tk-review",
)
DOMAIN_POINTER = "[domain context](../tk-repository-guidance/references/domain-context.md)"


class DomainContextContractTest(unittest.TestCase):
    def test_single_owner_is_reachable_by_every_semantic_consumer(self) -> None:
        from shared_references import link_error
        canonical = ROOT / "skills/tk-repository-guidance/references/domain-context.md"
        self.assertTrue(canonical.is_file())
        self.assertFalse(canonical.is_symlink())
        for name in EXPECTED_CONSUMERS:
            skill = ROOT / "skills" / name / "SKILL.md"
            self.assertIsNone(link_error(skill, "../tk-repository-guidance/references/domain-context.md", ROOT / "skills"))
            self.assertFalse((skill.parent / "references/domain-context.md").exists())

    def test_each_semantic_consumer_points_to_domain_context(self) -> None:
        for name in EXPECTED_CONSUMERS:
            skill = ROOT / "skills" / name / "SKILL.md"
            self.assertIn(DOMAIN_POINTER, skill.read_text(encoding="utf-8"), name)


if __name__ == "__main__":
    unittest.main()
