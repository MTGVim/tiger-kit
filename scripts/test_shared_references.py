"""Single-owner shared references preserve installed reachability and boundaries."""
import json
import re
import tempfile
import unittest
from pathlib import Path

from installed_skill_fixture import add_package
from shared_references import SHARED_REFERENCES, link_error, reference_only, validate_shared_references

ROOT = Path(__file__).resolve().parents[1]


def reachable_references(entrypoint: Path, skills: Path) -> set[Path]:
    visited = set()
    pending = [entrypoint.resolve()]
    while pending:
        source = pending.pop()
        if source in visited:
            continue
        visited.add(source)
        for target in re.findall(r"\[[^]]*\]\(([^)]+)\)", source.read_text()):
            path = target.split('#', 1)[0]
            if not path or re.match(r'^[a-z]+:|^//', path):
                continue
            if link_error(source, target, skills) is None:
                resolved = (source.parent / path).resolve()
                if resolved.suffix == '.md':
                    pending.append(resolved)
    return visited


class SharedReferenceTests(unittest.TestCase):
    def test_all_migrated_references_have_one_regular_owner(self):
        self.assertEqual(validate_shared_references(ROOT / 'skills'), [])
        self.assertEqual(len(SHARED_REFERENCES), 46)

    def test_all_222_previously_linked_consumer_references_remain_reachable(self):
        # f6e516d7's entrypoint graph had 235 copies, but these 13 were never linked.
        # Do not invent new unconditional loads to make formerly unused copies reachable.
        previously_unlinked = {
            'skills/tk-research/references/chart-design.md',
            'skills/tk-blind-comparison/references/clear-writing.md',
            'skills/tk-prototype/references/clear-writing.md',
            'skills/tk-qa-sheet/references/clear-writing.md',
            *('skills/tk-research/references/' + name for name in (
                'explanation-techniques.md', 'html-assembly.md', 'html-components.md',
                'html-figures.md', 'html-output.md', 'html-reader.md', 'html-render.md',
                'reader-formatting.md', 'visual-grammar.md')),
        }
        cache = {}
        checked = 0
        for target, originals in SHARED_REFERENCES.items():
            for original in originals:
                if original in previously_unlinked:
                    continue
                consumer = original.split('/')[1]
                if consumer not in cache:
                    cache[consumer] = reachable_references(ROOT / 'skills' / consumer / 'SKILL.md', ROOT / 'skills')
                self.assertIn((ROOT / target).resolve(), cache[consumer], (consumer, target))
                checked += 1
        self.assertEqual(checked, 222)

    def test_missing_single_owner_and_reintroduced_copy_are_errors(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for target in SHARED_REFERENCES:
                path = root / target
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('# Reference\n')
            self.assertEqual(validate_shared_references(root / 'skills'), [])
            for target, originals in SHARED_REFERENCES.items():
                owner = root / target
                owner.unlink()
                self.assertTrue(any(target in e for e in validate_shared_references(root / 'skills')))
                owner.write_text('# Reference\n')
                old = root / originals[0]
                old.parent.mkdir(parents=True, exist_ok=True)
                old.write_text('# Duplicate\n')
                self.assertTrue(any(originals[0] in e for e in validate_shared_references(root / 'skills')))
                old.unlink()

    def test_declared_sibling_link_and_missing_declaration_owner_or_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = add_package(root, 'tk-caller', requires=('tk-shared',))
            owner = add_package(root, 'tk-shared', role='reference')
            reference = owner.parent / 'references/topic.md'
            reference.parent.mkdir()
            reference.write_text('# Topic\n')
            target = '../tk-shared/references/topic.md'
            self.assertIsNone(link_error(source, target, root / 'skills'))
            declaration = source.parent / 'dependencies.json'
            for value in (None, '{broken', '{"version":1,"requires":[]}', '{"version":2,"requires":["tk-shared"]}',
                          '{"version":true,"requires":["tk-shared"]}', '{"version":1,"requires":["tk-shared","tk-shared"]}',
                          '{"version":1,"requires":["../tk-shared"]}'):
                if value is None:
                    declaration.unlink(missing_ok=True)
                else:
                    declaration.write_text(value)
                self.assertIsNotNone(link_error(source, target, root / 'skills'))
            declaration.write_text('{"version":1,"requires":["tk-shared"]}')
            reference.unlink()
            self.assertIsNotNone(link_error(source, target, root / 'skills'))
            reference.write_text('# Topic\n')
            owner.unlink()
            self.assertIsNotNone(link_error(source, target, root / 'skills'))
            owner.write_text('---\nname: tk-imposter\n---\n')
            self.assertIsNotNone(link_error(source, target, root / 'skills'))

    def test_outside_root_and_symlink_references_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = add_package(root, 'tk-caller', requires=('tk-shared',))
            owner = add_package(root, 'tk-shared', role='reference')
            outside = root / 'outside.md'
            outside.write_text('# Outside\n')
            link = owner.parent / 'linked.md'
            link.symlink_to(outside)
            targets = ['../../outside.md', '../../skills/tk-caller/SKILL.md',
                       '../tk-shared/linked.md', str(outside), '..\\tk-shared\\SKILL.md',
                       '%2e%2e/%2e%2e/outside.md']
            for target in targets:
                with self.subTest(target=target):
                    self.assertIsNotNone(link_error(source, target, root / 'skills'))
            link.unlink()
            link.symlink_to(owner)
            self.assertIsNotNone(link_error(source, '../tk-shared/linked.md', root / 'skills'))

    def test_nested_source_uses_its_own_relative_link_base(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = add_package(root, 'tk-caller', requires=('tk-shared',))
            owner = add_package(root, 'tk-shared', role='reference')
            nested = source.parent / 'references' / 'nested.md'
            nested.parent.mkdir()
            nested.write_text('# Nested\n')
            self.assertIsNone(link_error(nested, '../../tk-shared/SKILL.md', root / 'skills'))
            self.assertIsNotNone(link_error(nested, '../tk-shared/SKILL.md', root / 'skills'))

    def test_only_explicit_reference_or_bootstrap_roles_skip_workflow_boilerplate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ordinary = add_package(root, 'tk-ordinary')
            reference = add_package(root, 'tk-shared', role='reference')
            bootstrap = add_package(root, 'tk-setup-skills', role='setup')
            self.assertFalse(reference_only(ordinary))
            self.assertTrue(reference_only(reference))
            self.assertTrue(reference_only(bootstrap))

    def test_sync_preserves_reference_and_bootstrap_packages_without_adding_dependencies(self):
        from artifact_policy import sync_artifact_guards
        from question_policy import sync_questions
        from sync_execution_protocol import sync_feedback, sync_output_notation, sync_result_summary
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, role in (("tk-shared", "reference"), ("tk-setup-skills", "setup")):
                path = add_package(root, name, role=role, body="# Read-only or bootstrap contract\n")
            before = {p: p.read_bytes() for p in (root / 'skills').rglob('*') if p.is_file()}
            sync_artifact_guards(root)
            sync_questions(root)
            sync_feedback(root)
            sync_output_notation(root / 'skills')
            sync_result_summary(root / 'skills')
            self.assertEqual(before, {p: p.read_bytes() for p in (root / 'skills').rglob('*') if p.is_file()})


if __name__ == '__main__':
    unittest.main()
