import unittest

from check_docs import catalog_kind_errors, table_errors


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
        text = '## 스킬 구성\n\n| 스킬 | 호출 | 소유 범위 |\n| --- | --- | --- |\n| `tk-test` | `user` | scope |\n'
        self.assertTrue(catalog_kind_errors(text, {'tk-test':'hybrid'}))
        self.assertFalse(catalog_kind_errors(text, {'tk-test':'user-invoked'}))

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
