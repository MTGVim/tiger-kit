#!/usr/bin/env python3
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).with_name("prep_manifest.py")


def load_module():
    spec = importlib.util.spec_from_file_location("prep_manifest", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load prep_manifest.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class PrepManifestTest(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        tigerkit = self.root / ".tigerkit"
        tigerkit.mkdir()
        (tigerkit / "spec.md").write_text(
            "# Spec\n\nStatus: Ready\n\n## Requirements\n\n- R1\n",
            encoding="utf-8",
        )
        (tigerkit / "tickets.md").write_text(
            "# Tickets\n\nStatus: Pass\n\n## T1\n",
            encoding="utf-8",
        )
        self.output = tigerkit / "prep.md"

    def command(
        self,
        *extra: str,
        ticket_mode: str = "tickets",
    ) -> list[str]:
        command = [
            sys.executable,
            str(SCRIPT),
            "create",
            "--output",
            str(self.output),
            "--task-id",
            "github:owner/repo#206",
            "--task-anchor",
            "issue:206",
            "--repository-root",
            str(self.root),
            "--worktree",
            str(self.root),
            "--branch",
            "main",
            "--base-head",
            "a" * 40,
            "--source",
            "https://github.com/owner/repo/issues/206",
            "--dirty-inventory-json",
            '["skills-lock.json"]',
            "--instruction-inventory-json",
            '["AGENTS.md:abc123"]',
            "--spec",
            str(self.root / ".tigerkit/spec.md"),
            "--ticket-mode",
            ticket_mode,
            "--verification-profile-json",
            '{"obligations":["regression-seam"],"signals":["public-blast-radius"]}',
            "--prior-art-ref",
            "none",
            "--created-at",
            "2026-07-30T01:02:03Z",
        ]
        if ticket_mode == "tickets":
            command.extend(
                ["--tickets", str(self.root / ".tigerkit/tickets.md")]
            )
        command.extend(extra)
        return command

    def run_create(self, *extra: str, ticket_mode: str = "tickets"):
        return subprocess.run(
            self.command(*extra, ticket_mode=ticket_mode),
            text=True,
            capture_output=True,
            check=False,
        )

    def test_writes_reread_valid_ready_manifest_with_deterministic_digests(
        self,
    ) -> None:
        first = self.run_create()

        self.assertEqual(first.returncode, 0, first.stderr)
        module = load_module()
        document = self.output.read_text(encoding="utf-8")
        header, body = module.parse_document(document)
        self.assertEqual(header["schema_version"], "tigerkit.prep/v1")
        self.assertEqual(header["status"], "ready")
        self.assertEqual(header["claim"], {"actor": None, "id": None})
        self.assertEqual(
            header["timestamps"],
            {
                "claimed_at": None,
                "created_at": "2026-07-30T01:02:03Z",
                "finished_at": None,
            },
        )
        self.assertEqual(header["task"]["anchors"], ["issue:206"])
        self.assertEqual(header["repository"]["base_head"], "a" * 40)
        self.assertEqual(header["ticket_mode"], "tickets")
        self.assertIn("- Spec: `.tigerkit/spec.md`", body)
        self.assertIn("- Tickets: `.tigerkit/tickets.md`", body)
        self.assertIn("- Prior-art disposition: none", body)
        expected_source = hashlib.sha256(
            b"https://github.com/owner/repo/issues/206"
        ).hexdigest()
        self.assertEqual(header["digests"]["source"], expected_source)

        second = self.run_create()

        self.assertEqual(second.returncode, 0, second.stderr)
        second_header, _ = module.parse_document(
            self.output.read_text(encoding="utf-8")
        )
        self.assertEqual(second_header, header)
        self.assertEqual(self.output.stat().st_mode & 0o777, 0o600)

    def test_each_identity_and_digest_input_is_deterministic(self) -> None:
        module = load_module()
        self.assertEqual(self.run_create().returncode, 0)
        baseline, _ = module.parse_document(
            self.output.read_text(encoding="utf-8")
        )
        spec_path = self.root / ".tigerkit/spec.md"
        tickets_path = self.root / ".tigerkit/tickets.md"
        original_spec = spec_path.read_text(encoding="utf-8")
        original_tickets = tickets_path.read_text(encoding="utf-8")

        flag_cases = (
            ("source", "--source", "issue:changed", "source"),
            (
                "dirty inventory",
                "--dirty-inventory-json",
                '["different.txt"]',
                "dirty_inventory",
            ),
            (
                "instructions",
                "--instruction-inventory-json",
                '["RULES.md:different"]',
                "instructions",
            ),
            (
                "verification profile",
                "--verification-profile-json",
                '{"obligations":["compatibility"],"signals":["state-compatibility"]}',
                "verification_profile",
            ),
        )
        for label, flag, value, digest_key in flag_cases:
            with self.subTest(label=label):
                completed = self.run_create(flag, value)
                self.assertEqual(completed.returncode, 0, completed.stderr)
                changed, _ = module.parse_document(
                    self.output.read_text(encoding="utf-8")
                )
                self.assertNotEqual(
                    changed["digests"][digest_key],
                    baseline["digests"][digest_key],
                )
                self.assertNotEqual(changed["prep_id"], baseline["prep_id"])

        identity_cases = (
            ("task", "--task-anchor", "issue:changed"),
            ("repository", "--branch", "release/v21"),
        )
        for label, flag, value in identity_cases:
            with self.subTest(label=label):
                completed = self.run_create(flag, value)
                self.assertEqual(completed.returncode, 0, completed.stderr)
                changed, _ = module.parse_document(
                    self.output.read_text(encoding="utf-8")
                )
                self.assertNotEqual(changed["prep_id"], baseline["prep_id"])

        spec_path.write_text(
            original_spec + "\nChanged requirement.\n", encoding="utf-8"
        )
        self.assertEqual(self.run_create().returncode, 0)
        spec_changed, _ = module.parse_document(
            self.output.read_text(encoding="utf-8")
        )
        self.assertNotEqual(
            spec_changed["digests"]["spec"], baseline["digests"]["spec"]
        )
        self.assertNotEqual(spec_changed["prep_id"], baseline["prep_id"])
        spec_path.write_text(original_spec, encoding="utf-8")

        tickets_path.write_text(
            original_tickets + "\nChanged ticket.\n", encoding="utf-8"
        )
        self.assertEqual(self.run_create().returncode, 0)
        tickets_changed, _ = module.parse_document(
            self.output.read_text(encoding="utf-8")
        )
        self.assertNotEqual(
            tickets_changed["digests"]["tickets"],
            baseline["digests"]["tickets"],
        )
        self.assertNotEqual(tickets_changed["prep_id"], baseline["prep_id"])

        self.assertEqual(
            self.run_create(
                "--dirty-inventory-json",
                '["z.txt","a.txt"]',
                "--instruction-inventory-json",
                '["z","a"]',
            ).returncode,
            0,
        )
        ordered, _ = module.parse_document(
            self.output.read_text(encoding="utf-8")
        )
        self.assertEqual(
            self.run_create(
                "--dirty-inventory-json",
                '["a.txt","z.txt"]',
                "--instruction-inventory-json",
                '["a","z"]',
            ).returncode,
            0,
        )
        reversed_order, _ = module.parse_document(
            self.output.read_text(encoding="utf-8")
        )
        self.assertEqual(ordered["digests"], reversed_order["digests"])
        self.assertEqual(ordered["prep_id"], reversed_order["prep_id"])

    def test_no_ticket_digest_is_deterministic(self) -> None:
        completed = self.run_create(ticket_mode="no-ticket")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        module = load_module()
        header, body = module.parse_document(
            self.output.read_text(encoding="utf-8")
        )
        self.assertEqual(header["ticket_mode"], "no-ticket")
        self.assertEqual(
            header["digests"]["tickets"],
            hashlib.sha256(b'{"mode":"no-ticket"}').hexdigest(),
        )
        self.assertIn("- Tickets: no-ticket single slice", body)

    def test_clean_worktree_and_no_instruction_files_are_valid_inventories(
        self,
    ) -> None:
        completed = self.run_create(
            "--dirty-inventory-json",
            "[]",
            "--instruction-inventory-json",
            "[]",
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_failed_gate_preserves_prior_terminal_manifest(self) -> None:
        self.output.write_text("prior terminal manifest\n", encoding="utf-8")
        (self.root / ".tigerkit/spec.md").write_text(
            "# Spec\n\nStatus: Draft\n", encoding="utf-8"
        )

        completed = self.run_create()

        self.assertNotEqual(completed.returncode, 0)
        self.assertEqual(
            self.output.read_text(encoding="utf-8"),
            "prior terminal manifest\n",
        )

    def test_active_manifest_blocks_ready_replacement(self) -> None:
        self.assertEqual(self.run_create().returncode, 0)
        module = load_module()
        ready_header, body = module.parse_document(
            self.output.read_text(encoding="utf-8")
        )
        active_header = dict(ready_header)
        active_header["status"] = "active"
        active_header["claim"] = {"actor": "codex", "id": "run-1"}
        active_header["timestamps"] = {
            **ready_header["timestamps"],
            "claimed_at": "2026-07-30T01:03:00Z",
        }
        active_document = module.render_document(active_header, body)
        self.output.write_text(active_document, encoding="utf-8")

        completed = self.run_create("--created-at", "2026-07-30T02:00:00Z")

        self.assertNotEqual(completed.returncode, 0)
        self.assertEqual(self.output.read_text(encoding="utf-8"), active_document)

    def test_active_manifest_allows_same_run_amendment_reseal(self) -> None:
        self.assertEqual(self.run_create().returncode, 0)
        module = load_module()
        ready_header, body = module.parse_document(
            self.output.read_text(encoding="utf-8")
        )
        active_header = {
            **ready_header,
            "status": "active",
            "claim": {"actor": "codex", "id": "run-1"},
            "timestamps": {
                **ready_header["timestamps"],
                "claimed_at": "2026-07-30T01:03:00Z",
            },
        }
        self.output.write_text(
            module.render_document(active_header, body),
            encoding="utf-8",
        )
        (self.root / ".tigerkit/spec.md").write_text(
            "# Spec\n\nStatus: Ready\n\n## Requirements\n\n- R1 amended\n",
            encoding="utf-8",
        )

        completed = self.run_create(
            "--created-at",
            "2026-07-30T02:00:00Z",
            "--replace-active-claim-id",
            "run-1",
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        amended, _ = module.parse_document(
            self.output.read_text(encoding="utf-8")
        )
        self.assertEqual(amended["status"], "active")
        self.assertEqual(amended["claim"], active_header["claim"])
        self.assertEqual(
            amended["timestamps"],
            active_header["timestamps"],
        )
        self.assertNotEqual(amended["prep_id"], active_header["prep_id"])

    def test_active_manifest_rejects_wrong_amendment_claim(self) -> None:
        self.assertEqual(self.run_create().returncode, 0)
        module = load_module()
        ready_header, body = module.parse_document(
            self.output.read_text(encoding="utf-8")
        )
        active_header = {
            **ready_header,
            "status": "active",
            "claim": {"actor": "codex", "id": "run-1"},
            "timestamps": {
                **ready_header["timestamps"],
                "claimed_at": "2026-07-30T01:03:00Z",
            },
        }
        active_document = module.render_document(active_header, body)
        self.output.write_text(active_document, encoding="utf-8")

        completed = self.run_create(
            "--replace-active-claim-id",
            "other-run",
        )

        self.assertNotEqual(completed.returncode, 0)
        self.assertEqual(self.output.read_text(encoding="utf-8"), active_document)

    def test_strict_parser_rejects_schema_mutations(self) -> None:
        self.assertEqual(self.run_create().returncode, 0)
        module = load_module()
        document = self.output.read_text(encoding="utf-8")
        header, body = module.parse_document(document)
        mutations = []
        missing = dict(header)
        missing.pop("claim")
        mutations.append(module.render_document(missing, body))
        extra = dict(header)
        extra["unexpected"] = True
        mutations.append(module.render_document(extra, body))
        mistyped = dict(header)
        mistyped["task"] = []
        mutations.append(module.render_document(mistyped, body))
        unsupported = dict(header)
        unsupported["schema_version"] = "tigerkit.prep/v2"
        mutations.append(module.render_document(unsupported, body))
        forged = dict(header)
        forged["prep_id"] = "prep-0000000000000000"
        mutations.append(module.render_document(forged, body))
        relative_repository = dict(header)
        relative_repository["repository"] = {
            **header["repository"],
            "root": "relative/repository",
        }
        mutations.append(module.render_document(relative_repository, body))
        impossible_time = dict(header)
        impossible_time["timestamps"] = {
            **header["timestamps"],
            "created_at": "2026-02-31T01:02:03Z",
        }
        mutations.append(module.render_document(impossible_time, body))
        completed_without_claim = dict(header)
        completed_without_claim["status"] = "completed"
        completed_without_claim["timestamps"] = {
            **header["timestamps"],
            "finished_at": "2026-07-30T01:04:00Z",
        }
        mutations.append(module.render_document(completed_without_claim, body))
        mistyped_status = dict(header)
        mistyped_status["status"] = []
        mutations.append(module.render_document(mistyped_status, body))
        mistyped_ticket_mode = dict(header)
        mistyped_ticket_mode["ticket_mode"] = {}
        mutations.append(module.render_document(mistyped_ticket_mode, body))
        unsorted_anchors = dict(header)
        unsorted_anchors["task"] = {
            **header["task"],
            "anchors": ["z-anchor", "a-anchor"],
        }
        unsorted_identity = {
            key: unsorted_anchors[key]
            for key in (
                "schema_version",
                "task",
                "repository",
                "digests",
                "ticket_mode",
            )
        }
        unsorted_anchors["prep_id"] = (
            "prep-"
            + module._digest(module._canonical_json(unsorted_identity))[:16]
        )
        mutations.append(module.render_document(unsorted_anchors, body))
        mutations.append("```json\n{\"schema_version\":\n```\n")
        mutations.append(
            document.replace(
                '"schema_version": "tigerkit.prep/v1",',
                '"schema_version": "tigerkit.prep/v1",\n'
                '  "schema_version": "tigerkit.prep/v1",',
                1,
            )
        )

        for index, mutation in enumerate(mutations):
            with self.subTest(index=index):
                with self.assertRaises(module.ManifestError):
                    module.parse_document(mutation)

    def test_invalid_output_does_not_create_parent(self) -> None:
        invalid_parent = self.root / "outside" / "nested"
        completed = self.run_create(
            "--output", str(invalid_parent / "prep.md")
        )

        self.assertNotEqual(completed.returncode, 0)
        self.assertFalse(invalid_parent.exists())

    def test_replace_failure_preserves_prior_manifest(self) -> None:
        module = load_module()
        self.assertEqual(self.run_create().returncode, 0)
        ready_header, body = module.parse_document(
            self.output.read_text(encoding="utf-8")
        )
        terminal_header = dict(ready_header)
        terminal_header["status"] = "invalid"
        terminal_header["timestamps"] = {
            **ready_header["timestamps"],
            "finished_at": "2026-07-30T01:04:00Z",
        }
        prior_document = module.render_document(terminal_header, body)
        self.output.write_text(prior_document, encoding="utf-8")
        arguments = module.parse_args(self.command()[2:])

        with mock.patch.object(
            module.os, "replace", side_effect=OSError("simulated replace failure")
        ):
            with self.assertRaises(OSError):
                module.create_ready_manifest(arguments)

        self.assertEqual(
            self.output.read_text(encoding="utf-8"),
            prior_document,
        )


if __name__ == "__main__":
    unittest.main()
