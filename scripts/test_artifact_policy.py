from __future__ import annotations

import subprocess
import tempfile
import unittest
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

    def test_unignored_and_tracked_artifacts_fail_without_repair(self):
        (self.root / '.gitignore').unlink()
        with self.assertRaises(ValueError):
            policy.checked_artifact_root(self.root)
        self.assertFalse((self.root / '.gitignore').exists())
        (self.root / '.gitignore').write_text('.tigerkit/\n')
        target = self.root / '.tigerkit'
        target.mkdir()
        (target / 'tracked').write_text('keep')
        self.git('add', '-f', '.tigerkit/tracked')
        with self.assertRaises(ValueError):
            policy.checked_artifact_root(self.root)

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
