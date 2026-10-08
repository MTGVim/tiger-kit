"""Integration coverage for the worktree-shared browser auth helper."""
from __future__ import annotations

import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "skills/tk-browser-verify/scripts/shared_auth.py"


@unittest.skipUnless(os.name == "posix", "Private POSIX file mode backend only")
class SharedBrowserAuthTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.root = self.base / "repo"
        self.root.mkdir()
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        (self.root / ".gitignore").write_text("/.tigerkit/\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(self.root), "add", ".gitignore"], check=True)
        subprocess.run(["git", "-C", str(self.root), "-c", "user.email=test@example.invalid",
                        "-c", "user.name=Tester", "commit", "--allow-empty", "-qm", "seed"], check=True)
        self.other = self.base / "another"
        subprocess.run(["git", "-C", str(self.root), "worktree", "add", "-q", "-b", "other", str(self.other)], check=True)
        self.args = ("--authority", "https://auth.example.invalid", "--environment", "dev",
                     "--role", "admin", "--profile", "tester")

    def call(self, action, *, repo=None, extras=(), code=0):
        command = [sys.executable, str(SCRIPT), action, "--repo", str(repo or self.root),
                   *self.args, *extras]
        cp = subprocess.run(command, text=True, capture_output=True)
        self.assertEqual(cp.returncode, code, cp.stderr + cp.stdout)
        self.assertNotIn("TOP_SECRET", cp.stdout + cp.stderr)
        return json.loads(cp.stdout)

    def input(self, *, repo=None, content='{"token":"TOP_SECRET"}'):
        repo = repo or self.root
        base = repo / ".tigerkit" / "secret-input"
        base.mkdir(parents=True, exist_ok=True, mode=0o700)
        folder = base / "tk-browser-verify-test"
        folder.mkdir(mode=0o700)
        path = folder / "input.json"
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def test_share_between_worktrees_and_compare_revision(self):
        claim = self.call("claim")
        self.assertEqual(claim["status"], "claimed")
        path = self.input()
        stored = self.call("commit", extras=("--claim-id", claim["claim_id"], "--input", str(path)))
        self.assertEqual(stored["status"], "stored")
        shared = self.call("inspect", repo=self.other)
        self.assertEqual(shared["status"], "needs-verification")
        self.assertEqual(shared["revision"], stored["revision"])
        self.assertTrue(Path(shared["token_path"]).is_file())
        self.assertEqual(stat.S_IMODE(Path(shared["token_path"]).stat().st_mode), 0o600)
        # A rejected stale response must not invalidate a more recent revision.
        self.assertEqual(self.call("invalidate", repo=self.other,
                                  extras=("--revision", "unrelated"))["status"], "superseded")
        self.assertEqual(self.call("invalidate", repo=self.other,
                                  extras=("--revision", stored["revision"]))["status"], "invalidated")
        self.assertEqual(self.call("inspect")["status"], "missing")

    def test_created_input_paths_and_no_overwrite(self):
        claim = self.call("claim")
        receipt = self.call("prepare-input", extras=("--claim-id", claim["claim_id"],
                                                      "--run-id", "baseline-1"))
        self.assertEqual(receipt["status"], "input-pending")
        self.assertEqual(receipt["template"], {"token": ""})
        self.assertEqual(receipt["relative_path"],
                         ".tigerkit/secret-input/tk-browser-verify-baseline-1/input.json")
        file = Path(receipt["absolute_path"])
        self.assertEqual(file.read_text(), '{"token":""}')
        self.assertEqual(stat.S_IMODE(file.stat().st_mode), 0o600)
        self.assertEqual(stat.S_IMODE(file.parent.stat().st_mode), 0o700)
        file.write_text('{"token":"TOP_SECRET"}')
        second = self.call("prepare-input", extras=("--claim-id", claim["claim_id"],
                                                     "--run-id", "baseline-1"))
        self.assertEqual(second["absolute_path"], receipt["absolute_path"])
        self.assertEqual(file.read_text(), '{"token":"TOP_SECRET"}')
        self.assertEqual(second["template"], {"token": ""})

    def test_prepare_input_refuses_unignored_git_paths(self):
        claim = self.call("claim")
        (self.root / ".gitignore").write_text("", encoding="utf-8")
        result = self.call("prepare-input", extras=("--claim-id", claim["claim_id"],
                                                     "--run-id", "baseline-2"), code=3)
        self.assertEqual(result["status"], "blocked")

    def test_one_claim_until_release(self):
        first = self.call("claim")
        second = self.call("claim", repo=self.other)
        self.assertEqual(first["status"], "claimed")
        self.assertEqual(second["status"], "pending")
        self.assertEqual(self.call("renew", extras=("--claim-id", first["claim_id"]))["status"], "renewed")
        self.assertEqual(self.call("release", extras=("--claim-id", first["claim_id"]))["status"], "released")
        third = self.call("claim", repo=self.other)
        self.assertEqual(third["status"], "claimed")

    def test_reject_unsafe_input_and_wrong_claim(self):
        first = self.call("claim")
        path = self.input()
        path.chmod(0o644)
        self.assertEqual(self.call("commit", extras=("--claim-id", first["claim_id"], "--input", str(path)),
                                   code=3)["status"], "blocked")
        path.chmod(0o600)
        self.assertEqual(self.call("commit", extras=("--claim-id", "not-owner", "--input", str(path)),
                                   code=3)["status"], "blocked")
        self.assertEqual(self.call("inspect")["status"], "pending")

    def test_expiry_and_no_secret_console_output(self):
        claim = self.call("claim")
        path = self.input()
        stored = self.call("commit", extras=("--claim-id", claim["claim_id"], "--input", str(path),
                                             "--expires-at", "2020-01-01T00:00:00Z"))
        self.assertEqual(stored["status"], "stored")
        self.assertEqual(self.call("inspect")["status"], "expired")
        self.assertEqual(self.call("claim")["status"], "claimed")

    def test_scope_separation(self):
        claim = self.call("claim")
        stored = self.call("commit", extras=("--claim-id", claim["claim_id"], "--input", str(self.input())))
        self.assertEqual(stored["status"], "stored")
        args = self.args
        self.args = ("--authority", "https://auth.example.invalid", "--environment", "production",
                     "--role", "admin", "--profile", "tester")
        self.assertEqual(self.call("inspect")["status"], "missing")
        self.args = args

    def test_untrusted_origin_is_blocked(self):
        self.args = ("--authority", "http://not-local.invalid", "--environment", "dev",
                     "--role", "admin", "--profile", "tester")
        self.assertEqual(self.call("inspect", code=3)["status"], "blocked")


if __name__ == "__main__":
    unittest.main()
