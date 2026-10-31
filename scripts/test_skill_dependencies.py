"""Dependency CLI contract tests; package inspection requires PyYAML."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name('skill_dependencies.py')


class DependencyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()

    def package(self, name, requires=()):
        path = self.root / 'skills' / name
        path.mkdir(parents=True, exist_ok=True)
        (path / 'SKILL.md').write_text(f'---\nname: {name}\ndescription: test\n---\n\nTest.\n')
        (path / 'dependencies.json').write_text(json.dumps({'version': 1, 'requires': list(requires)}))
        return path

    def cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True)

    def test_validate_source_without_generated_catalog(self):
        self.package('tk-a', ['tk-b'])
        self.package('tk-b')
        result = self.cli('validate', '--root', self.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['errors'], [])

    def test_plan_closure_cycles_repeatable_literal_argv_and_no_writes(self):
        self.package('tk-a', ['tk-b', 'tk-c'])
        self.package('tk-b', ['tk-c'])
        self.package('tk-c', ['tk-a'])
        before = sorted(str(p.relative_to(self.root)) for p in self.root.rglob('*'))
        source = 'owner/repo; $(touch PWNED) with spaces'
        args = ('plan', '--root', self.root, '--skill', 'tk-a', '--target', self.root,
                '--agent', 'codex', '--scope', 'project', '--source', source)
        result = self.cli(*args)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        plan = json.loads(result.stdout)
        self.assertEqual(plan['closure'], ['tk-a', 'tk-b', 'tk-c'])
        self.assertEqual(plan['argv'][3:5], ['add', source])
        self.assertEqual(plan['cwd'], str(self.root))
        self.assertNotIn('--global', plan['argv'])
        self.assertNotIn('--yes', plan['argv'][3:])
        self.assertEqual(result.stdout, self.cli(*args).stdout)
        self.assertEqual(before, sorted(str(p.relative_to(self.root)) for p in self.root.rglob('*')))

    def test_catalog_roundtrip_standalone_and_staleness(self):
        self.package('tk-a', ['tk-b'])
        self.package('tk-b')
        catalog = self.root / 'catalog.json'
        built = self.cli('build-catalog', '--root', self.root, '--output', catalog)
        self.assertEqual(built.returncode, 0, built.stdout + built.stderr)
        result = self.cli('plan', '--catalog', catalog, '--skill', 'tk-a', '--source', 'owner/repo',
                          '--target', self.root, '--agent', 'hermes-agent', '--scope', 'project')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)['closure'], ['tk-a', 'tk-b'])
        self.package('tk-c')
        stale = self.cli('validate', '--root', self.root, '--catalog', catalog)
        self.assertNotEqual(stale.returncode, 0)
        self.assertIn('stale', stale.stdout + stale.stderr)

    def test_installed_check_missing_transitive_stops_and_bootstrap_guidance(self):
        self.package('tk-a', ['tk-b'])
        self.package('tk-b', ['tk-c'])
        result = self.cli('check', '--installed-root', self.root / 'skills', '--skill', 'tk-a')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('tk-c', result.stdout + result.stderr)
        self.assertIn('tk-setup-skills', result.stdout + result.stderr)
        self.package('tk-c', ['tk-a'])
        result = self.cli('check', '--installed-root', self.root / 'skills', '--skill', 'tk-a')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)['closure'], ['tk-a', 'tk-b', 'tk-c'])

    def assert_rejected(self, result, text):
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(text, result.stdout + result.stderr)
        self.assertNotIn('Traceback', result.stdout + result.stderr)

    def test_invalid_source_declarations_and_identity_fail_closed(self):
        package = self.package('tk-a')
        cases = [('{', 'Expecting'),
                 ('{"version":1,"requires":[],"requires":[]}', 'duplicate JSON key'),
                 ('{"version":true,"requires":[]}', 'version 1'),
                 ('{"version":1,"requires":["tk-b","tk-b"]}', 'duplicate dependency'),
                 ('{"version":1,"requires":["../tk-b"]}', 'invalid exact'),
                 ('{"version":1,"requires":["tk-unknown"]}', 'unknown dependency'),
                 ('{"version":1,"requires":null}', 'must be a list')]
        for value, message in cases:
            with self.subTest(value=value):
                (package / 'dependencies.json').write_text(value)
                self.assert_rejected(self.cli('validate', '--root', self.root), message)
        self.package('tk-a')
        (package / 'SKILL.md').write_text('---\nname: tk-b\n---\nbody\n')
        self.assert_rejected(self.cli('validate', '--root', self.root), 'identity mismatch')

    def test_symlinks_and_path_escape_fail_closed(self):
        package = self.package('tk-a')
        refs = package / 'references'
        refs.mkdir()
        (refs / 'escape').symlink_to(self.root)
        self.assert_rejected(self.cli('validate', '--root', self.root), 'symlink')
        (refs / 'escape').unlink()
        declaration = package / 'dependencies.json'
        declaration.unlink()
        declaration.symlink_to(self.root / 'missing')
        self.assert_rejected(self.cli('validate', '--root', self.root), 'symlink')
        declaration.unlink()
        self.package('tk-a')
        alias = self.root / 'alias'
        alias.symlink_to(self.root / 'skills', target_is_directory=True)
        self.assert_rejected(self.cli('check', '--installed-root', alias, '--skill', 'tk-a'), 'symlink')
        self.assert_rejected(self.cli('check', '--installed-root', self.root / 'skills',
                                      '--skill', '../tk-a'), 'invalid exact')

    def test_unknown_roots_and_target_options_are_not_silently_broadened(self):
        self.package('tk-a')
        base = ['plan', '--root', self.root, '--source', 'owner/repo', '--target', self.root,
                '--agent', 'codex', '--scope', 'project', '--skill', 'tk-unknown']
        self.assert_rejected(self.cli(*base), 'unknown skill')
        base[-1] = 'tk-a'
        for option, value, text in [('--scope', 'global', 'global target'),
                                    ('--target', 'relative', 'absolute'),
                                    ('--agent', '*', 'invalid choice')]:
            args = base.copy()
            args[args.index(option) + 1] = value
            self.assert_rejected(self.cli(*args), text)

    def test_installed_matching_packages_are_not_reinstalled_or_overwritten(self):
        import shutil
        self.package('tk-a', ['tk-b'])
        self.package('tk-b')
        target = self.root / 'consumer'
        installed = target / '.agents/skills'
        installed.mkdir(parents=True)
        shutil.copytree(self.root / 'skills/tk-a', installed / 'tk-a')
        args = ['plan', '--root', self.root, '--source', 'owner/repo', '--target', target,
                '--agent', 'codex', '--scope', 'project', '--skill', 'tk-a']
        result = self.cli(*args)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)['missing'], ['tk-b'])
        shutil.copytree(self.root / 'skills/tk-b', installed / 'tk-b')
        self.assertEqual(json.loads(self.cli(*args).stdout)['argv'], [])
        (installed / 'tk-a/dependencies.json').write_text('{"version":1,"requires":[]}')
        self.assert_rejected(self.cli(*args), 'refuse overwrite')

    def test_public_validator_reports_missing_declarations_without_throwing(self):
        spec = importlib.util.spec_from_file_location('dependency_shim', SCRIPT)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        package = self.package('tk-a')
        (package / 'dependencies.json').unlink()
        errors = module.validate_dependencies(self.root)
        self.assertIsInstance(errors, list)
        self.assertIn('dependencies.json', errors[0])

    def test_bootstrap_package_alone_uses_bundled_catalog_without_writes(self):
        import shutil
        setup = SCRIPT.parent.parent / 'skills/tk-setup-skills'
        copy = self.root / 'standalone'
        shutil.copytree(setup, copy, ignore=shutil.ignore_patterns('__pycache__'))
        consumer = self.root / 'consumer'
        consumer.mkdir()
        (consumer / 'config.json').write_text('{"preserve":true}')
        before = {str(p.relative_to(self.root)): (p.read_bytes(), p.stat().st_mtime_ns)
                  for p in self.root.rglob('*') if p.is_file()}
        result = subprocess.run([sys.executable, '-I', '-S', '-B', str(copy / 'scripts/skill_dependencies.py'),
                                 'plan', '--skill', 'tk-setup-skills', '--source', 'trusted/repository',
                                 '--target', str(consumer), '--agent', 'codex', '--scope', 'project'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)['closure'], ['tk-setup-skills'])
        after = {str(p.relative_to(self.root)): (p.read_bytes(), p.stat().st_mtime_ns)
                 for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_catalog_malformed_duplicate_and_unknown_dependency_rejected(self):
        catalog = self.root / 'catalog.json'
        base = ['plan', '--catalog', catalog, '--skill', 'tk-a', '--source', 'trusted/repository',
                '--target', self.root, '--agent', 'codex', '--scope', 'project']
        for value, text in [('{', 'Expecting'),
                            ('{"version":1,"packages":{},"packages":{}}', 'duplicate JSON key'),
                            ('{"version":1,"packages":{"tk-a":{"requires":["tk-unknown"]}}}', 'unknown'),
                            ('{"version":1,"packages":{"../tk-a":{"requires":[]}}}', 'invalid exact')]:
            with self.subTest(value=value):
                catalog.write_text(value)
                self.assert_rejected(self.cli(*base), text)

    def test_malformed_installed_yaml_is_not_present_or_complete(self):
        import shutil
        package = self.package('tk-a')
        target = self.root / 'consumer'
        installed = target / '.agents/skills'
        installed.mkdir(parents=True)
        shutil.copytree(package, installed / 'tk-a')
        (installed / 'tk-a/SKILL.md').write_text(
            '---\nname: tk-a\ndescription: [\n---\nbody\n')
        commands = [
            ('check', '--installed-root', installed, '--skill', 'tk-a'),
            ('plan', '--root', self.root, '--source', 'trusted/repository',
             '--target', target, '--agent', 'codex', '--scope', 'project', '--skill', 'tk-a'),
        ]
        for command in commands:
            with self.subTest(command=command[0]):
                self.assert_rejected(self.cli(*command), 'YAML')

    def test_duplicate_yaml_keys_rejected(self):
        package = self.package('tk-a')
        cases = [
            'name: tk-a\n"name": tk-a\ndescription: test',
            'name: tk-a\ndescription: first\ndescription: second',
            'name: tk-a\ndescription: test\nmetadata:\n  owner: first\n  owner: second',
            'name: tk-a\ndescription: test\nmetadata: {<<: {owner: first, owner: second}}',
            'name: tk-a\ndescription: test\nmetadata:\n  <<: {owner: first}\n  <<: {owner: second}',
            'name: tk-a\ndescription: test\nmetadata: {<<: [{owner: first, owner: second}]}',
        ]
        for frontmatter in cases:
            with self.subTest(frontmatter=frontmatter):
                (package / 'SKILL.md').write_text(f'---\n{frontmatter}\n---\nbody\n')
                self.assert_rejected(self.cli('validate', '--root', self.root), 'YAML')

    def test_yaml_constructor_failures_are_structured(self):
        spec = importlib.util.spec_from_file_location('dependency_error_shim', SCRIPT)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        package = self.package('tk-a')
        for metadata in ['metadata: {updated: 2026-99-99}',
                         'metadata: {[unhashable]: value}',
                         'metadata: {flag: !!bool private-marker}',
                         'metadata: {number: !!int ""}',
                         'metadata: {updated: !!timestamp private-marker}']:
            with self.subTest(metadata=metadata):
                (package / 'SKILL.md').write_text(
                    f'---\nname: tk-a\ndescription: test\n{metadata}\n---\nbody\n')
                for command in [('validate', '--root', self.root),
                                ('check', '--installed-root', self.root / 'skills', '--skill', 'tk-a'),
                                ('plan', '--root', self.root, '--skill', 'tk-a',
                                 '--target', self.root, '--agent', 'codex',
                                 '--scope', 'project', '--source', 'owner/repo')]:
                    result = self.cli(*command)
                    self.assert_rejected(result, 'YAML')
                    self.assertNotIn(metadata, result.stdout + result.stderr)
                    self.assertNotIn('private-marker', result.stdout + result.stderr)
                errors = module.validate_dependencies(self.root)
                self.assertIsInstance(errors, list)
                self.assertTrue(errors)
                self.assertIn('YAML', errors[0])

    def test_missing_yaml_parser_is_a_closed_failure_without_traceback(self):
        self.package('tk-a')
        result = subprocess.run(
            [sys.executable, '-I', '-S', '-B', str(SCRIPT), 'check',
             '--installed-root', str(self.root / 'skills'), '--skill', 'tk-a'],
            capture_output=True, text=True)
        self.assert_rejected(result, 'PyYAML')

    def test_valid_yaml_quoted_keys_and_merge_overrides_remain_supported(self):
        package = self.package('tk-a')
        (package / 'SKILL.md').write_text(
            '---\n"name": tk-a\ndescription: >-\n  A valid description.\n'
            'defaults: &defaults\n  owner: original\n'
            'metadata:\n  <<: *defaults\n  owner: override\n'
            '  flag: !!bool true\n  number: !!int 42\n'
            '  updated: !!timestamp 2026-10-31\n---\nbody\n')
        result = self.cli('validate', '--root', self.root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unsafe_yaml_tags_are_rejected_without_input_echo(self):
        package = self.package('tk-a')
        marker = 'private-frontmatter-marker'
        (package / 'SKILL.md').write_text(
            f'---\nname: tk-a\ndescription: !!python/name:{marker}\n---\nbody\n')
        result = self.cli('validate', '--root', self.root)
        self.assert_rejected(result, 'YAML')
        self.assertNotIn(marker, result.stdout + result.stderr)

    def test_required_description_schema_rejected(self):
        package = self.package('tk-a')
        for description in ['', "description: ''", 'description: []',
                            'description: ' + json.dumps('x' * 1025)]:
            with self.subTest(description=description):
                (package / 'SKILL.md').write_text(f'---\nname: tk-a\n{description}\n---\nbody\n')
                self.assert_rejected(self.cli('validate', '--root', self.root), 'description')

    def test_identity_unbalanced_quotes_rejected(self):
        package = self.package('tk-a')
        (package / 'SKILL.md').write_text('---\nname: "tk-a\ndescription: bad YAML\n---\nbody\n')
        self.assert_rejected(self.cli('validate', '--root', self.root), 'identity mismatch')


if __name__ == '__main__':
    unittest.main()
