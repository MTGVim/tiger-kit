#!/usr/bin/env python3
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock


SCRIPT = Path(__file__).with_name("preflight.py")


def load_module():
    spec = importlib.util.spec_from_file_location("preflight", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load preflight.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class PreflightTest(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_module()
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name).resolve()
        self.path = self.root / ".tigerkit" / "prep.md"
        self.value = {
            "task": {
                "goal": "Implement the verified change.",
                "included_scope": ["skills/tk-drive"],
                "excluded_scope": ["skills/tk-grooming"],
                "confirmed_decisions": ["Use the direct procedure graph."],
            },
            "repository": {
                "root": str(self.root),
                "worktree": str(self.root),
                "branch": "main",
                "baseline_head": "a" * 40,
                "dirty_paths": ["README.md"],
            },
            "execution": {
                "procedure_graph": ["tk-to-spec", "tk-implement"],
                "verification_profile": {
                    "signals": ["state-compatibility"],
                    "obligations": ["regression-seam"],
                },
            },
            "browser": {
                "decision": "N/A",
                "environment_url": None,
                "account_role_or_tenant_class": None,
                "opaque_profile_hint": None,
                "authentication_expectation": None,
                "ask_identity_on_cold_start": None,
            },
            "sources": {
                "spec": ".tigerkit/spec.md",
                "tickets": ".tigerkit/tickets.md",
            },
        }

    def test_writes_complete_compact_preflight_and_strictly_rereads(self) -> None:
        result = self.module.write_preflight(self.path, self.root, self.value)

        self.assertEqual(set(result), self.module.TOP_KEYS)
        self.assertEqual(self.path.stat().st_mode & 0o777, 0o600)
        self.assertEqual(
            self.module.parse_preflight(self.path.read_bytes()),
            self.value,
        )
        text = self.path.read_text(encoding="utf-8")
        for prohibited in ("claim_id", "phase_cursor", '"status"', '"token"'):
            self.assertNotIn(prohibited, text)

    def test_rejects_lifecycle_and_secret_fields(self) -> None:
        for key, value in (
            ("status", "ready"),
            ("token", "secret"),
            ("phase_cursor", "tk-implement"),
        ):
            with self.subTest(key=key):
                candidate = json.loads(json.dumps(self.value))
                candidate[key] = value
                with self.assertRaises(self.module.PreflightError):
                    self.module.validate_preflight(candidate)

        candidate = json.loads(json.dumps(self.value))
        candidate["task"]["goal"] = "Use password=secret"
        with self.assertRaises(self.module.PreflightError):
            self.module.validate_preflight(candidate)

    def test_required_browser_identity_is_opaque_and_asked_once(self) -> None:
        browser = self.value["browser"]
        browser.update(
            {
                "decision": "required",
                "environment_url": "https://staging.example.test/app",
                "account_role_or_tenant_class": "reviewer tenant",
                "opaque_profile_hint": None,
                "authentication_expectation": "interactive-login-required",
                "ask_identity_on_cold_start": True,
            }
        )
        self.assertEqual(
            self.module.browser_identity_action(self.value, cold_start=True),
            "ask-once",
        )
        browser["opaque_profile_hint"] = "opaque:profile-17"
        self.assertEqual(
            self.module.browser_identity_action(self.value, cold_start=True),
            "ready",
        )
        browser["opaque_profile_hint"] = "person@example.test"
        with self.assertRaises(self.module.PreflightError):
            self.module.validate_preflight(self.value)

    def test_rejects_external_and_symlink_outputs(self) -> None:
        external = self.root.parent / "prep.md"
        with self.assertRaises(self.module.PreflightError):
            self.module.write_preflight(external, self.root, self.value)

        target = self.root / "real"
        target.mkdir()
        link = self.root / ".tigerkit"
        link.symlink_to(target, target_is_directory=True)
        with self.assertRaises(self.module.PreflightError):
            self.module.write_preflight(link / "prep.md", self.root, self.value)

    def test_interrupted_replace_preserves_prior_file_without_partial(self) -> None:
        self.module.write_preflight(self.path, self.root, self.value)
        before = self.path.read_bytes()
        changed = json.loads(json.dumps(self.value))
        changed["task"]["goal"] = "Changed goal."

        with mock.patch.object(self.module.os, "replace", side_effect=OSError("stop")):
            with self.assertRaises(OSError):
                self.module.write_preflight(self.path, self.root, changed)

        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(list(self.path.parent.glob(".prep.*")), [])

    def test_resume_table_is_derived_only_from_current_evidence(self) -> None:
        base = {key: False for key in self.module.RESUME_KEYS}
        cases = (
            ({"material_decisions_unresolved": True}, "tk-grill-me"),
            ({"ready_spec": False}, "tk-to-spec"),
            (
                {"ready_spec": True, "multiple_units": True, "valid_tickets": False},
                "tk-to-tickets",
            ),
            (
                {"ready_spec": True, "valid_tickets": True, "incomplete_units": True},
                "tk-implement",
            ),
            (
                {
                    "ready_spec": True,
                    "implementation_changed": True,
                    "aggregate_complete": False,
                },
                "aggregate verification",
            ),
            (
                {
                    "ready_spec": True,
                    "aggregate_complete": True,
                    "valid_reflection_handoff": True,
                },
                "tk-reflect",
            ),
            (
                {
                    "ready_spec": True,
                    "aggregate_complete": True,
                    "required_work_complete": True,
                },
                "tk-drive finalization",
            ),
        )
        for overrides, expected in cases:
            with self.subTest(expected=expected):
                evidence = {**base, **overrides}
                self.assertEqual(
                    self.module.choose_resume_action(evidence), expected
                )

        with self.assertRaises(self.module.PreflightError):
            self.module.choose_resume_action({**base, "status": True})
