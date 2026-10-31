import json
from pathlib import Path
import shutil
import tempfile
import unittest

from scripts.check_token_budget import compare_token_budget, static_errors


ROOT = Path(__file__).resolve().parents[1]


class TokenBudgetTest(unittest.TestCase):
    def roots(self):
        temporary = tempfile.TemporaryDirectory(prefix='tk-token-budget-')
        base = Path(temporary.name) / 'base'
        candidate = Path(temporary.name) / 'candidate'
        shutil.copytree(ROOT / 'skills', base / 'skills', ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copytree(ROOT / 'skills', candidate / 'skills', ignore=shutil.ignore_patterns('__pycache__'))
        (base / 'evals').mkdir()
        (candidate / 'evals').mkdir()
        manifest = (ROOT / 'evals/token-budget.json').read_text(encoding='utf-8')
        (base / 'evals/token-budget.json').write_text(manifest, encoding='utf-8')
        (candidate / 'evals/token-budget.json').write_text(manifest, encoding='utf-8')
        return temporary, base, candidate

    def test_current_candidate_fits_static_caps(self):
        errors, _, _ = static_errors(ROOT)
        self.assertEqual(errors, [])

    # Use a skill outside always-read groups so other caps cannot mask the metric under test.
    def test_unexplained_skill_growth_over_ten_percent_fails(self):
        temporary, base, candidate = self.roots()
        with temporary:
            path = candidate / 'skills/tk-audit/SKILL.md'
            path.write_text(path.read_text() + '\n' + ('x' * 1600), encoding='utf-8')
            manifest_path = candidate / 'evals/token-budget.json'
            manifest = json.loads(manifest_path.read_text())
            manifest['rationales'].pop('skill_md:skills/tk-audit/SKILL.md', None)
            manifest_path.write_text(json.dumps(manifest), encoding='utf-8')
            errors = compare_token_budget(base, candidate)
            self.assertTrue(any('unexplained context growth: skill_md:skills/tk-audit/SKILL.md' in e for e in errors), errors)

    def test_growth_can_pass_with_a_specific_rationale(self):
        temporary, base, candidate = self.roots()
        with temporary:
            path = candidate / 'skills/tk-audit/SKILL.md'
            path.write_text(path.read_text() + '\n' + ('x' * 1600), encoding='utf-8')
            manifest_path = candidate / 'evals/token-budget.json'
            manifest = json.loads(manifest_path.read_text())
            metric = 'skill_md:skills/tk-audit/SKILL.md'
            manifest['rationales'][metric] = 'Adds the section-routing behavior required by this release.'
            manifest_path.write_text(json.dumps(manifest), encoding='utf-8')
            errors = compare_token_budget(base, candidate)
            self.assertEqual(errors, [])

    def test_new_duplicate_sentence_fails_and_budget_ceiling_growth_needs_a_reason(self):
        temporary, base, candidate = self.roots()
        with temporary:
            sentence = 'This unique sentence measures whether duplicated skill prose remains visible to the budget guard.'
            # Keep this duplicate probe outside always-read groups so an unrelated size cap cannot mask it.
            for name in ('tk-audit', 'tk-grooming'):
                path = candidate / f'skills/{name}/SKILL.md'
                path.write_text(path.read_text() + '\n\n' + sentence + '\n', encoding='utf-8')
            errors = compare_token_budget(base, candidate)
            self.assertTrue(any('new duplicate skill sentence' in e for e in errors), errors)

        temporary, base, candidate = self.roots()
        with temporary:
            manifest_path = candidate / 'evals/token-budget.json'
            manifest = json.loads(manifest_path.read_text())
            manifest['limits']['max_skill_md_bytes'] += 1000
            manifest_path.write_text(json.dumps(manifest), encoding='utf-8')
            errors = compare_token_budget(base, candidate)
            self.assertTrue(any('budget ceiling increased without a rationale' in e for e in errors), errors)
            manifest['rationales']['budget_increase:max_skill_md_bytes'] = 'Allows one verified new skill contract.'
            manifest_path.write_text(json.dumps(manifest), encoding='utf-8')
            self.assertEqual(compare_token_budget(base, candidate), [])

    def test_static_skill_size_cap_blocks_oversized_skill(self):
        temporary, _, candidate = self.roots()
        with temporary:
            path = candidate / 'skills/tk-prep/SKILL.md'
            ceiling = json.loads((candidate / 'evals/token-budget.json').read_text())['limits']['max_skill_md_bytes']
            path.write_text(path.read_text() + '\n' + ('x' * ceiling), encoding='utf-8')
            errors, _, _ = static_errors(candidate)
            self.assertTrue(any('token budget exceeded: skill_md_max_bytes' in e for e in errors), errors)

    def test_reinjection_character_boundary_reports_exact_skill(self):
        temporary, _, candidate = self.roots()
        with temporary:
            path = candidate / 'skills/tk-prep/SKILL.md'
            header = '---\nname: tk-prep\ndescription: probe\n---\n'
            path.write_text(header + 'x' * (19999 - len(header)), encoding='utf-8')
            self.assertEqual(static_errors(candidate)[0], [])
            path.write_text(path.read_text() + 'x', encoding='utf-8')
            errors, _, _ = static_errors(candidate)
            self.assertTrue(any('skills/tk-prep/SKILL.md' in e and '20000 > 19999' in e for e in errors), errors)

    def test_unicode_character_budget_is_distinct_from_byte_budget(self):
        temporary, _, candidate = self.roots()
        with temporary:
            path = candidate / 'skills/tk-prep/SKILL.md'
            path.write_text('---\nname: tk-prep\ndescription: probe\n---\n' + '한' * 7000, encoding='utf-8')
            errors, metrics, _ = static_errors(candidate)
            self.assertEqual(errors, [])
            self.assertGreater(metrics['skill_md:skills/tk-prep/SKILL.md'], 20000)
            self.assertLess(metrics['skill_md_chars:skills/tk-prep/SKILL.md'], 20000)

    def test_astral_characters_fit_both_common_reinjection_units(self):
        temporary, _, candidate = self.roots()
        with temporary:
            path = candidate / 'skills/tk-prep/SKILL.md'
            # Under 20k code points and 36KB, but exactly 20k UTF-16 units.
            header = '---\nname: tk-prep\ndescription: probe\n---\n'
            body = header + 'x' * (20000 - len(header) - 2000) + '\U0001f600' * 1000
            path.write_text(body, encoding='utf-8')
            self.assertLess(len(body), 20000)
            self.assertLess(path.stat().st_size, 36000)
            errors, _, _ = static_errors(candidate)
            self.assertTrue(any('skill_md_utf16_units:skills/tk-prep/SKILL.md 20000 > 19999' in e for e in errors), errors)

    def test_character_ceiling_requires_valid_manifest_value(self):
        temporary, _, candidate = self.roots()
        with temporary:
            path = candidate / 'evals/token-budget.json'
            manifest = json.loads(path.read_text())
            for value in (None, True, -1, '19999'):
                manifest['limits']['max_skill_md_chars'] = value
                path.write_text(json.dumps(manifest), encoding='utf-8')
                errors, _, _ = static_errors(candidate)
                self.assertTrue(any('max_skill_md_chars must be a non-negative integer' in e for e in errors), errors)


if __name__ == '__main__':
    unittest.main()
