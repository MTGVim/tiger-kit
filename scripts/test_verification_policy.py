from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from verification_policy import verification_errors

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/tk-browser-verify/scripts/verify_preferences.py"
spec = importlib.util.spec_from_file_location("verify_preferences", SCRIPT)
preferences = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preferences)


class VerificationPreferencesTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.config = Path(self.temporary.name) / "config/tigerkit/verify.json"
        self.providers = preferences.registry()

    def run_cli(self, *args, success=True):
        result = subprocess.run([sys.executable, str(SCRIPT), "--config", str(self.config), *args],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_browser_and_app_selection_preserve_other_scope_and_metadata(self):
        self.run_cli("select", "--scope", "browser", "--provider", "chrome-devtools-mcp", "--fallback", "playwright")
        self.run_cli("docs", "--provider", "cua-driver", "--url", "https://cua.ai/docs/cua-driver")
        before = json.loads(self.config.read_text())
        self.run_cli("select", "--scope", "app", "--provider", "cua-driver")
        after = json.loads(self.config.read_text())
        self.assertEqual(after["browser"], before["browser"])
        self.assertEqual(after["docsOverrides"], before["docsOverrides"])
        self.assertEqual(after["app"]["provider"], "cua-driver")

    def test_session_override_does_not_create_or_overwrite_config(self):
        result = self.run_cli("select", "--scope", "app", "--provider", "orca-computer", "--session-only")
        self.assertFalse(result["saved"])
        self.assertFalse(self.config.parent.exists())
        self.run_cli("select", "--scope", "app", "--provider", "cua-driver")
        before = self.config.read_bytes()
        self.run_cli("select", "--scope", "app", "--provider", "orca-computer", "--session-only")
        self.assertEqual(self.config.read_bytes(), before)

    def test_bad_config_and_scope_mismatch_never_reset_existing_data(self):
        self.run_cli("select", "--scope", "browser", "--provider", "playwright")
        before = self.config.read_bytes()
        self.run_cli("select", "--scope", "browser", "--provider", "cua-driver", success=False)
        self.assertEqual(self.config.read_bytes(), before)
        self.config.write_text("{broken")
        self.run_cli("select", "--scope", "app", "--provider", "orca-computer", success=False)
        self.assertEqual(self.config.read_text(), "{broken")
        self.assertEqual(list(self.config.parent.glob("*.lock")), [])

    def test_atomic_save_failure_keeps_prior_config_and_cleans_transport(self):
        self.run_cli("select", "--scope", "app", "--provider", "cua-driver")
        before = self.config.read_bytes()
        with patch.object(preferences.os, "replace", side_effect=OSError("fixture write failure")):
            with self.assertRaises(OSError):
                preferences.update_config(self.config, self.providers, lambda data: data.update({"fixture": "new"}))
        self.assertEqual(self.config.read_bytes(), before)
        self.assertEqual(sorted(p.name for p in self.config.parent.iterdir()), ["verify.json"])

    def test_lock_conflict_blocks_without_overwriting_or_removing_foreign_lock(self):
        self.run_cli("select", "--scope", "app", "--provider", "cua-driver")
        lock = self.config.with_suffix(".json.lock")
        lock.write_text("other-writer")
        before = self.config.read_bytes()
        self.run_cli("select", "--scope", "app", "--provider", "orca-computer", success=False)
        self.assertEqual(self.config.read_bytes(), before)
        self.assertEqual(lock.read_text(), "other-writer")

    def test_symlink_path_cannot_redirect_global_preference_write(self):
        real = Path(self.temporary.name) / "real"
        real.mkdir()
        self.config.parent.parent.mkdir()
        self.config.parent.symlink_to(real, target_is_directory=True)
        self.run_cli("select", "--scope", "app", "--provider", "cua-driver", success=False)
        self.assertEqual(list(real.iterdir()), [])

    def test_verified_notes_replace_same_condition_and_remain_bounded(self):
        for index in range(22):
            self.run_cli("note", "--provider", "cua-driver", "--environment", "fixture-os", "--condition", f"condition-{index}",
                         "--symptom", "missing tree", "--workaround", "safe capture", "--verified")
        result = self.run_cli("note", "--provider", "cua-driver", "--environment", "fixture-os", "--condition", "condition-21",
                              "--symptom", "updated", "--workaround", "verified-safe", "--verified")
        notes = json.loads(self.config.read_text())["providerNotes"]["cua-driver"]
        self.assertEqual(len(notes), 20)
        self.assertEqual(sum(n["condition"] == "condition-21" for n in notes), 1)
        self.assertEqual(notes[-1]["symptom"], "updated")
        self.assertNotIn("providerNotes", result)

    def test_unverified_raw_logs_and_credential_urls_are_rejected(self):
        for data in ({"providerNotes": {"cua-driver": [{"raw_log": "fixture", "verified": True}]}},
                     {"docsOverrides": {"cua-driver": "https://user:password@example.com/docs"}}):
            with self.assertRaises(ValueError):
                preferences.validate_config(data, self.providers)

    def test_registry_requires_canonical_docs_and_unique_identity(self):
        data = json.loads(preferences.REGISTRY.read_text())
        data["providers"][0]["docs"] = ""
        path = Path(self.temporary.name) / "registry.json"
        path.write_text(json.dumps(data))
        with self.assertRaises(ValueError):
            preferences.registry(path)
        data["providers"][0]["docs"] = "https://example.com/docs"
        data["providers"].append(data["providers"][0])
        path.write_text(json.dumps(data))
        with self.assertRaises(ValueError):
            preferences.registry(path)

    def test_installed_packages_share_validated_contract(self):
        self.assertEqual(verification_errors(ROOT), [])


if __name__ == "__main__":
    unittest.main()
