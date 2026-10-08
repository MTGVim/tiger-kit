import unittest

from check_docs import catalog_kind_errors, table_errors, readme_freshness_errors


class DocumentationTests(unittest.TestCase):
    def test_readme_pipe_regression_is_rejected(self):
        text = '| Skill | Kind | Scope |\n| --- | --- | --- |\n| pr | hybrid | `single | stacked` publishing |\n'
        self.assertTrue(table_errors(text))
        self.assertFalse(table_errors(text.replace('single | stacked', 'single \\| stacked')))

    def test_short_row_is_rejected_and_code_examples_are_not_tables(self):
        self.assertTrue(table_errors('| a | b |\n| --- | --- |\n| one |\n'))
        self.assertFalse(table_errors('```md\n| a | b |\n| --- | --- |\n| one |\n```\n'))
        self.assertFalse(table_errors('<!--\n| a | b |\n| --- | --- |\n| one |\n-->\n'))

    def test_invocation_drift_is_rejected(self):
        text = '## 스킬 구성\n\n| 스킬 | 호출 | 소유 범위 |\n| --- | --- | --- |\n| [tk-test](skills/tk-test/SKILL.md) | `user` | scope |\n'
        self.assertTrue(catalog_kind_errors(text, {'tk-test':'hybrid'}))
        self.assertFalse(catalog_kind_errors(text, {'tk-test':'user-invoked'}))

    def test_linked_catalog_checks_kind_and_exact_owner(self):
        text = ('## 스킬 구성\n\n### 개발\n\n'
                '| 스킬 | 호출 | 소유 범위 |\n| --- | --- | --- |\n'
                '| [tk-test](skills/tk-other/SKILL.md) | `user` | scope |\n')
        self.assertEqual(len(catalog_kind_errors(text, {'tk-test': 'hybrid'})), 2)
        fixed = text.replace('tk-other/SKILL.md', 'tk-test/SKILL.md').replace('`user`', '`hybrid`')
        self.assertFalse(catalog_kind_errors(fixed, {'tk-test': 'hybrid'}))

    def test_catalog_cannot_silently_drop_its_direct_link(self):
        text = ('## 스킬 구성\n\n| 스킬 | 호출 | 소유 범위 |\n| --- | --- | --- |\n'
                '| `tk-test` | `user` | scope |\n')
        self.assertTrue(catalog_kind_errors(text, {'tk-test': 'user-invoked'}))

    def test_unrecognized_catalog_cells_are_rejected(self):
        text = ('## 스킬 구성\n\n| 스킬 | 호출 | 소유 범위 |\n| --- | --- | --- |\n'
                '| [tk-test](skills/tk-test/SKILL.md) | `user` | scope |\n')
        for cell in ('tk-old', '**tk-old**', 'tk-test'):
            with self.subTest(cell=cell):
                self.assertTrue(catalog_kind_errors(text + f'| {cell} | user | stale |\n',
                                                   {'tk-test': 'user-invoked'}))

    def test_catalog_checks_gfm_rows_without_a_leading_pipe(self):
        text = ('## 스킬 구성\n\n스킬 | 호출 | 소유 범위\n--- | --- | ---\n'
                '[tk-test](skills/tk-test/SKILL.md) | `user` | scope\n')
        self.assertFalse(catalog_kind_errors(text, {'tk-test': 'user-invoked'}))
        for row in ('tk-old | user | stale', '**tk-old** | user | stale',
                    '[tk-test](skills/tk-test/SKILL.md) | hybrid | wrong kind'):
            with self.subTest(row=row):
                self.assertTrue(catalog_kind_errors(text + row + '\n', {'tk-test': 'user-invoked'}))

class ReadmeFreshnessTests(unittest.TestCase):
    def test_changed_skill_needs_readme_or_explicit_noop(self):
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp) / 'before'
            current = Path(tmp) / 'after'
            for root in (base, current):
                (root / 'skills/tk-example').mkdir(parents=True)
                (root / 'evals/changes').mkdir(parents=True)
                (root / 'README.md').write_text('# Skills\n')
                (root / 'skills/tk-example/SKILL.md').write_text('---\nname: tk-example\n---\nOld behavior\n')
            (current / 'skills/tk-example/SKILL.md').write_text('---\nname: tk-example\n---\nNew behavior\n')
            self.assertTrue(readme_freshness_errors(base, current))
            (current / 'evals/changes/decision.md').write_text(
                'README: no public change\nAffected: skills/tk-example/SKILL.md\nReason: internal guidance only.\n'
            )
            self.assertEqual(readme_freshness_errors(base, current), [])
            (current / 'README.md').write_text('# Skills\nPublic change reviewed\n')
            self.assertEqual(readme_freshness_errors(base, current), [])


class NestedCheckoutTests(unittest.TestCase):
    def test_ignore_filters_are_relative_to_checkout_not_ancestors(self):
        import tempfile
        from pathlib import Path
        from unittest.mock import patch
        import validate_skills
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / '.tigerkit/tmp/candidate/repo'
            root.mkdir(parents=True)
            (root / 'README.md').write_text('[broken](missing.md)\n' + '/' + 'home/example/private/file\n')
            with patch.object(validate_skills, 'ROOT', root):
                self.assertTrue(validate_skills.validate_repo_links())
            self.assertTrue(validate_skills.validate_portable_artifacts(root))
            ignored = root / '.tigerkit'
            ignored.mkdir()
            (ignored / 'ignored.md').write_text('[broken](missing.md)')
            (root / 'README.md').write_text('# Clean\n')
            with patch.object(validate_skills, 'ROOT', root):
                self.assertFalse(validate_skills.validate_repo_links())
