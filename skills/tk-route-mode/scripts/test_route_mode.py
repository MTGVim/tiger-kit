#!/usr/bin/env python3
"""단일 위임 대응표의 로컬 회귀 검사. 네트워크 및 실제 위임을 사용하지 않는다."""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name("route_mode.py")
DEFAULTS = SCRIPT.parent.parent / "references" / "route-defaults.json"


class RouteModeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.path = self.root / "routes.json"
        self.env = {**os.environ, "ROUTE_MODE_CONFIG": str(self.path)}

    def run_cli(self, *args, ok=True):
        result = subprocess.run([sys.executable, str(SCRIPT), *args],
                                capture_output=True, text=True, env=self.env)
        if ok:
            self.assertEqual(result.returncode, 0, result.stderr)
        return result

    def test_default_status_is_read_only_and_has_one_mapping(self):
        result = self.run_cli()
        self.assertIn("bundled defaults", result.stdout)
        self.assertIn("provider: openai", result.stdout)
        self.assertIn("| 티어 |", result.stdout)
        self.assertNotIn("active:", result.stdout)
        self.assertFalse(self.path.exists())

    def test_removed_derive_and_mode_commands(self):
        for command in ("derive", "use", "add", "list", "update"):
            result = self.run_cli(command, ok=False)
            self.assertNotEqual(result.returncode, 0, command)
        self.assertFalse(self.path.exists())

    def legacy(self):
        defaults = json.loads(DEFAULTS.read_text(encoding="utf-8"))
        standard = copy.deepcopy(defaults["providers"])
        economy = copy.deepcopy(standard)
        economy["openai"]["standard"] = {"model": "gpt-6-luna", "effort": "max"}
        legacy = {
            "version": 1, "active": "economy",
            "tiers": defaults["tiers"], "efforts": defaults["efforts"],
            "modes": {
                "standard": {"providers": standard},
                "economy": {
                    "providers": economy,
                    "overrides": {"openai.standard": economy["openai"]["standard"]},
                },
                "custom": {"extends": "economy", "providers": {
                    "anthropic": {"top": {"model": "sonnet", "effort": "high"}}
                }},
            },
        }
        source = self.root / "modes.json"
        source.write_text(json.dumps(legacy), encoding="utf-8")
        return source, legacy

    def test_legacy_preview_does_not_touch_any_file(self):
        source, original = self.legacy()
        before = source.read_bytes()
        status = self.run_cli("status")
        self.assertIn("migration required", status.stdout)
        self.assertIn("economy", status.stdout)
        self.assertIn("gpt-6-luna / max", status.stdout)
        self.assertEqual(source.read_bytes(), before)
        self.assertFalse(self.path.exists())
        blocked = self.run_cli("apply", "--set", "openai.top=gpt-6.2-sol:medium", ok=False)
        self.assertNotEqual(blocked.returncode, 0)
        self.assertFalse(self.path.exists())

    def test_migrate_requires_inactive_mode_ack_and_preserves_override(self):
        source, original = self.legacy()
        preview = self.run_cli("migrate")
        self.assertIn("selected legacy mode: economy", preview.stdout)
        denied = self.run_cli("migrate", "--save", ok=False)
        self.assertNotEqual(denied.returncode, 0)
        self.assertFalse(self.path.exists())
        self.run_cli("migrate", "--save", "--accept-inactive-modes")
        data = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertEqual(data["version"], 2)
        self.assertNotIn("modes", data)
        self.assertNotIn("active", data)
        self.assertEqual(data["providers"]["openai"]["standard"]["model"], "gpt-6-luna")
        self.assertEqual(data["overrides"]["openai.standard"]["effort"], "max")
        self.assertEqual(json.loads(source.read_text(encoding="utf-8")), original)
        self.assertTrue(list((self.root / "backups").glob("legacy-modes-*.json")))
        self.assertIn("OK", self.run_cli("validate").stdout)

    def test_apply_updates_single_cell_and_unset_restores_bundle(self):
        self.run_cli("apply", "--set", "openai.standard=gpt-6.2-sol:low")
        self.run_cli("apply", "--set", "anthropic.top=sonnet:high")
        data = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertEqual(len(data["overrides"]), 2)
        self.assertEqual(data["providers"]["openai"]["standard"]["effort"], "low")
        self.run_cli("apply", "--unset", "openai.standard")
        data = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertNotIn("openai.standard", data["overrides"])
        self.assertEqual(data["providers"]["openai"]["standard"]["model"], "gpt-6.1-terra")
        self.assertIn("anthropic.top", data["overrides"])

    def test_unknown_alias_is_not_silently_replaced(self):
        denied = self.run_cli("apply", "--set", "openai.standard=sol:high", ok=False)
        self.assertNotEqual(denied.returncode, 0)
        self.assertFalse(self.path.exists())
        self.run_cli("apply", "--set", "openai.standard=gpt-6.2-sol:medium")
        data = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertEqual(data["providers"]["openai"]["standard"]["model"], "gpt-6.2-sol")

    def test_migrate_cannot_overwrite_existing_v2(self):
        self.run_cli("apply", "--set", "anthropic.top=sonnet:high")
        self.legacy()
        before = self.path.read_bytes()
        denied = self.run_cli("migrate", "--save", "--accept-inactive-modes", ok=False)
        self.assertNotEqual(denied.returncode, 0)
        self.assertEqual(before, self.path.read_bytes())


if __name__ == "__main__":
    unittest.main()
