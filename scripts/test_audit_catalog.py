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

    def test_readme_skill_names_reads_only_catalog_section(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text(
                """# TigerKit

## 스킬 구성

| 스킬 | 호출 | 소유 범위 |
| --- | --- | --- |
| `tk-prep` | `user` | prep |
| `tk-review` | `user` | review |

## 다른 표

| `tk-stale` | value |
""",
                encoding="utf-8",
            )
            self.assertEqual(
                audit_catalog.readme_skill_names(root),
                {"tk-prep", "tk-review"},
            )

    def test_readme_catalog_parity_reports_missing_and_stale(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text(
                """## 스킬 구성

| 스킬 | 호출 | 소유 범위 |
| --- | --- | --- |
| `tk-prep` | `user` | prep |
| `tk-old` | `user` | old |
""",
                encoding="utf-8",
            )
            self.assertEqual(
                audit_catalog.readme_catalog_parity(
                    {"tk-prep", "tk-review"}, root
                ),
                {
                    "missing": ["tk-review"],
                    "stale": ["tk-old"],
                    "duplicates": [],
                },
            )

    def test_readme_catalog_ignores_comments_and_rejects_duplicates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text(
                """## 스킬 구성

| 스킬 | 호출 | 소유 범위 |
| --- | --- | --- |
| `tk-prep` | `user` | prep |
| `tk-prep` | `user` | duplicate |
<!-- | `tk-review` | `user` | hidden | -->

## 다음
""",
                encoding="utf-8",
            )
            self.assertEqual(
                audit_catalog.readme_catalog_parity(
                    {"tk-prep", "tk-review"}, root
                ),
                {
                    "missing": ["tk-review"],
                    "stale": [],
                    "duplicates": ["tk-prep"],
                },
            )

    def test_readme_catalog_ignores_a_second_table_in_the_section(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text(
                """## 스킬 구성

| 스킬 | 호출 | 소유 범위 |
| --- | --- | --- |
| `tk-prep` | `user` | prep |

| 관련 이름 | 값 |
| --- | --- |
| `tk-review` | mention only |

## 다음
""",
                encoding="utf-8",
            )
            self.assertEqual(
                audit_catalog.readme_catalog_parity(
                    {"tk-prep", "tk-review"}, root
                ),
                {
                    "missing": ["tk-review"],
                    "stale": [],
                    "duplicates": [],
                },
            )

    def test_readme_catalog_does_not_fill_an_empty_first_table_from_a_second(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text(
                """## 스킬 구성

| 스킬 | 호출 | 소유 범위 |
| --- | --- | --- |

| 관련 이름 | 값 |
| --- | --- |
| `tk-prep` | mention only |
| `tk-review` | mention only |

## 다음
""",
                encoding="utf-8",
            )
            self.assertEqual(
                audit_catalog.readme_catalog_parity(
                    {"tk-prep", "tk-review"}, root
                ),
                {
                    "missing": ["tk-prep", "tk-review"],
                    "stale": [],
                    "duplicates": [],
                },
            )


if __name__ == "__main__":
    unittest.main()
