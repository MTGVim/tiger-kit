from __future__ import annotations

import subprocess
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

import artifact_policy as policy


class ArtifactPolicyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'repo'
        self.root.mkdir()
        self.git('init', '-q')
        (self.root / '.gitignore').write_text('.tigerkit/\n')

    def git(self, *args):
        return subprocess.run(['git', *args], cwd=self.root, check=True, capture_output=True)

    def test_scratch_is_ignored_local_and_cleaned(self):
        with policy.scratch_directory('eval', self.root) as value:
            path = Path(value)
            self.assertTrue(path.is_relative_to(self.root / '.tigerkit/tmp/eval'))
            (path / 'result').write_text('evidence')
            self.assertEqual(self.git('ls-files', '--others', '--exclude-standard', '.tigerkit').stdout, b'')
        self.assertFalse(path.exists())

    def test_default_evidence_and_explicit_final_destination(self):
        default = policy.output_directory(None, 'release-gate', self.root)
        self.assertTrue(default.is_relative_to(self.root / '.tigerkit/evidence/release-gate'))
        external = Path(self.temp.name) / 'chosen-final'
        self.assertEqual(policy.output_directory(str(external), 'release-gate', self.root), external)
        local = self.root / '.tigerkit/evidence/chosen'
        self.assertEqual(policy.output_directory(str(local), 'release-gate', self.root), local)

    def test_missing_ignore_is_created_before_artifact_write(self):
        (self.root / '.gitignore').unlink()
        path = policy.artifact_directory('tmp/new', self.root)
        self.assertTrue(path.is_dir())
        self.assertEqual((self.root / '.gitignore').read_bytes(), b'/.tigerkit/\n')
        self.assertEqual(self.git('ls-files').stdout, b'')
        self.assertEqual(self.git('check-ignore', '.tigerkit/tmp/new').stdout.strip(), b'.tigerkit/tmp/new')

    def test_existing_bytes_preserved_and_rule_not_duplicated(self):
        p = self.root / '.gitignore'
        original = b'# keep\r\nnode_modules/\r\n!/.tigerkit/'
        p.write_bytes(original)
        policy.artifact_directory('tmp/one', self.root)
        first = p.read_bytes()
        self.assertEqual(first, original + b'\r\n/.tigerkit/\r\n')
        policy.artifact_directory('tmp/two', self.root)
        self.assertEqual(p.read_bytes(), first)

    def test_existing_local_exclude_needs_no_gitignore(self):
        (self.root / '.gitignore').unlink()
        (self.root / '.git/info/exclude').write_text('/.tigerkit/\n')
        policy.artifact_directory('tmp/one', self.root)
        self.assertFalse((self.root / '.gitignore').exists())

    def test_global_exclude_preserves_repository_ignore(self):
        global_ignore = Path(self.temp.name) / 'global-ignore'
        global_ignore.write_text('/.tigerkit/\n')
        self.git('config', 'core.excludesFile', str(global_ignore))
        for original in (None, b'# unrelated\r\nnode_modules/\r\n'):
            with self.subTest(original=original):
                p = self.root / '.gitignore'
                if original is None:
                    p.unlink(missing_ok=True)
                else:
                    p.write_bytes(original)
                policy.artifact_directory('tmp/global', self.root)
                self.assertEqual(p.read_bytes() if p.exists() else None, original)
                self.assertEqual(global_ignore.read_text(), '/.tigerkit/\n')

    def test_local_negation_overrides_global_exclude(self):
        global_ignore = Path(self.temp.name) / 'global-ignore'
        global_ignore.write_text('/.tigerkit/\n')
        self.git('config', 'core.excludesFile', str(global_ignore))
        p = self.root / '.gitignore'
        p.write_text('!/.tigerkit/\n')
        policy.artifact_directory('tmp/negated', self.root)
        self.assertEqual(p.read_text(), '!/.tigerkit/\n/.tigerkit/\n')
        self.git('check-ignore', '-q', '--', '.tigerkit/')

    def test_ignore_command_error_does_not_edit_ignore(self):
        p = self.root / '.gitignore'
        p.unlink()
        run = subprocess.run

        def fail_ignore(command, **kwargs):
            if command[:2] == ['git', 'check-ignore']:
                return subprocess.CompletedProcess(command, 128, b'', b'fatal error')
            return run(command, **kwargs)

        with patch.object(policy.subprocess, 'run', side_effect=fail_ignore):
            with self.assertRaises(ValueError):
                policy.artifact_directory('tmp/error', self.root)
        self.assertFalse(p.exists())
        self.assertFalse((self.root / '.tigerkit').exists())

    def test_symlinked_ignore_is_not_modified(self):
        p = self.root / '.gitignore'
        p.unlink()
        outside = Path(self.temp.name) / 'external-ignore'
        outside.write_text('keep\n')
        p.symlink_to(outside)
        with self.assertRaises(ValueError):
            policy.artifact_directory('tmp/one', self.root)
        self.assertEqual(outside.read_text(), 'keep\n')
        self.assertFalse((self.root / '.tigerkit').exists())

    def test_tracked_artifacts_fail_without_ignore_repair(self):
        (self.root / '.gitignore').unlink()
        target = self.root / '.tigerkit'
        target.mkdir()
        (target / 'tracked').write_text('keep')
        self.git('add', '-f', '.tigerkit/tracked')
        with self.assertRaises(ValueError):
            policy.checked_artifact_root(self.root)
        self.assertFalse((self.root / '.gitignore').exists())

    def test_failed_ignore_write_creates_no_artifacts(self):
        (self.root / '.gitignore').unlink()
        with patch.object(policy.os, 'open', side_effect=PermissionError('read only')):
            with self.assertRaises(ValueError):
                policy.artifact_directory('tmp/one', self.root)
        self.assertFalse((self.root / '.tigerkit').exists())

    def test_invalid_destination_does_not_bootstrap_ignore(self):
        (self.root / '.gitignore').unlink()
        with self.assertRaises(ValueError):
            policy.artifact_directory('../escape', self.root)
        self.assertFalse((self.root / '.gitignore').exists())
        with self.assertRaises(ValueError):
            policy.output_directory(str(self.root / 'docs'), 'eval', self.root)
        self.assertFalse((self.root / '.gitignore').exists())
        base = self.root / '.tigerkit'
        base.mkdir()
        (base / 'outside').symlink_to(Path(self.temp.name), target_is_directory=True)
        with self.assertRaises(ValueError):
            policy.output_directory(str(base / 'outside/result'), 'eval', self.root)
        self.assertFalse((self.root / '.gitignore').exists())

    def test_escape_and_symlink_are_rejected(self):
        with self.assertRaises(ValueError):
            policy.artifact_directory('../escape', self.root)
        base = self.root / '.tigerkit'
        base.mkdir()
        (base / 'tmp').symlink_to(Path(self.temp.name), target_is_directory=True)
        with self.assertRaises(ValueError):
            policy.scratch_directory('eval', self.root)
        with self.assertRaises(ValueError):
            policy.output_directory(str(base / 'tmp/out'), 'eval', self.root)

    def test_existing_results_and_product_directory_are_preserved(self):
        old = policy.output_directory(None, 'release-gate', self.root)
        (old / 'result').write_text('keep')
        with self.assertRaises(ValueError):
            policy.output_directory(str(old), 'release-gate', self.root)
        self.assertEqual((old / 'result').read_text(), 'keep')
        with self.assertRaises(ValueError):
            policy.output_directory(str(self.root / 'docs'), 'release-gate', self.root)
