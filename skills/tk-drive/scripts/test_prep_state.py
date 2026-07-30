#!/usr/bin/env python3
import hashlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).with_name("prep_state.py")
PREP_SCRIPT = SCRIPT.parents[2] / "tk-prep" / "scripts" / "prep_manifest.py"
SCHEMA = "tigerkit.prep/v1"


def canonical_json(value) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_module():
    spec = importlib.util.spec_from_file_location("prep_state", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load prep_state.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class PrepStateTest(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name).resolve()
        self.tigerkit = self.root / ".tigerkit"
        self.tigerkit.mkdir()
        self.spec = self.tigerkit / "spec.md"
        self.tickets = self.tigerkit / "tickets.md"
        self.path = self.tigerkit / "prep.md"
        self.spec.write_text(
            "# Spec\n\nStatus: Ready\n\n- R1\n", encoding="utf-8"
        )
        self.tickets.write_text(
            "# Tickets\n\nStatus: Pass\n\n- T1\n", encoding="utf-8"
        )
        self.source = "issue:206"
        self.dirty = ["skills-lock.json"]
        self.instructions = ["AGENTS.md:abc123"]
        self.profile = {
            "obligations": ["regression-seam"],
            "signals": ["state-compatibility"],
        }
        self.base_head = "a" * 40
        self.write_manifest()

    def build_header(self, **overrides):
        identity = {
            "schema_version": SCHEMA,
            "task": {"anchors": ["issue:206"], "id": "issue:206"},
            "repository": {
                "base_head": self.base_head,
                "branch": "main",
                "root": str(self.root),
                "worktree": str(self.root),
            },
            "digests": {
                "source": digest(self.source.encode("utf-8")),
                "dirty_inventory": digest(canonical_json(sorted(self.dirty))),
                "instructions": digest(canonical_json(sorted(self.instructions))),
                "spec": digest(self.spec.read_bytes()),
                "tickets": digest(self.tickets.read_bytes()),
                "verification_profile": digest(
                    canonical_json(
                        {
                            "obligations": sorted(self.profile["obligations"]),
                            "signals": sorted(self.profile["signals"]),
                        }
                    )
                ),
            },
            "ticket_mode": "tickets",
        }
        header = {
            **identity,
            "prep_id": f"prep-{digest(canonical_json(identity))[:16]}",
            "status": "ready",
            "claim": {"actor": None, "id": None},
            "timestamps": {
                "claimed_at": None,
                "created_at": "2026-07-30T01:00:00Z",
                "finished_at": None,
            },
        }
        header.update(overrides)
        return header

    def body(self) -> str:
        return "\n".join(
            (
                "# TigerKit preparation",
                "",
                "## References",
                "",
                "- Task: `issue:206`",
                f"- Source: `{self.source}`",
                "- Spec: `.tigerkit/spec.md`",
                "- Tickets: `.tigerkit/tickets.md`",
                "- Verification profile: `digests.verification_profile`",
                "- Prior-art disposition: none",
            )
        )

    def write_manifest(self, header=None) -> None:
        if header is None:
            header = self.build_header()
        payload = json.dumps(
            header, ensure_ascii=False, indent=2, sort_keys=True
        )
        self.path.write_text(
            f"```json\n{payload}\n```\n\n{self.body()}\n",
            encoding="utf-8",
        )
        self.path.chmod(0o600)

    def claim_command(self, *extra: str) -> list[str]:
        return [
            sys.executable,
            str(SCRIPT),
            "claim",
            str(self.path),
            "--actor",
            "codex",
            "--claim-id",
            "run-1",
            "--claimed-at",
            "2026-07-30T01:01:00Z",
            "--repository-root",
            str(self.root),
            "--worktree",
            str(self.root),
            "--branch",
            "main",
            "--head",
            self.base_head,
            "--dirty-inventory-json",
            json.dumps(self.dirty),
            "--instruction-inventory-json",
            json.dumps(self.instructions),
            "--verification-profile-json",
            json.dumps(self.profile),
            *extra,
        ]

    def run_claim(self, *extra: str):
        return subprocess.run(
            self.claim_command(*extra),
            text=True,
            capture_output=True,
            check=False,
        )

    def read(self):
        module = load_module()
        return module, *module.parse_document(
            self.path.read_text(encoding="utf-8")
        )

    def test_claim_and_finalize_preserve_identity(self) -> None:
        module, ready, body = self.read()
        claimed = self.run_claim()

        self.assertEqual(claimed.returncode, 0, claimed.stderr)
        _, active, active_body = self.read()
        self.assertEqual(active["status"], "active")
        self.assertEqual(
            active["claim"], {"actor": "codex", "id": "run-1"}
        )
        self.assertEqual(
            active["timestamps"]["claimed_at"], "2026-07-30T01:01:00Z"
        )
        self.assertEqual(active["prep_id"], ready["prep_id"])
        self.assertEqual(active["digests"], ready["digests"])
        self.assertEqual(active_body, body)

        finalized = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "finalize",
                str(self.path),
                "--claim-id",
                "run-1",
                "--status",
                "completed",
                "--finished-at",
                "2026-07-30T01:02:00Z",
            ],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(finalized.returncode, 0, finalized.stderr)
        _, terminal, terminal_body = self.read()
        self.assertEqual(terminal["status"], "completed")
        self.assertEqual(
            terminal["timestamps"]["finished_at"],
            "2026-07-30T01:02:00Z",
        )
        self.assertEqual(terminal["prep_id"], ready["prep_id"])
        self.assertEqual(terminal_body, body)

    def test_two_claims_have_exactly_one_winner(self) -> None:
        first = subprocess.Popen(
            self.claim_command("--claim-id", "run-a"),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        second = subprocess.Popen(
            self.claim_command("--claim-id", "run-b"),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        first.communicate(timeout=10)
        second.communicate(timeout=10)

        self.assertEqual(
            sorted((first.returncode, second.returncode)),
            [0, 1],
        )
        _, header, _ = self.read()
        self.assertEqual(header["status"], "active")
        self.assertIn(header["claim"]["id"], {"run-a", "run-b"})

    def test_freshness_drift_invalidates_ready_manifest(self) -> None:
        completed = self.run_claim("--head", "b" * 40)

        self.assertNotEqual(completed.returncode, 0)
        _, header, _ = self.read()
        self.assertEqual(header["status"], "invalid")
        self.assertIsNone(header["claim"]["id"])
        self.assertEqual(
            header["timestamps"]["finished_at"],
            "2026-07-30T01:01:00Z",
        )
        self.assertIn("base HEAD drift", completed.stderr)

    def test_malformed_claim_evidence_preserves_ready_manifest(self) -> None:
        before = self.path.read_text(encoding="utf-8")

        completed = self.run_claim(
            "--dirty-inventory-json",
            "not-json",
        )

        self.assertNotEqual(completed.returncode, 0)
        self.assertEqual(self.path.read_text(encoding="utf-8"), before)

    def test_content_drift_matrix_invalidates_ready_manifest(self) -> None:
        mutations = (
            (
                "source",
                lambda: self.path.write_text(
                    self.path.read_text(encoding="utf-8").replace(
                        "- Source: `issue:206`",
                        "- Source: `issue:changed`",
                        1,
                    ),
                    encoding="utf-8",
                ),
            ),
            (
                "dirty inventory",
                lambda: self.dirty.append("new-user-file.txt"),
            ),
            (
                "instructions",
                lambda: self.instructions.append("RULES.md:def456"),
            ),
            (
                "spec",
                lambda: self.spec.write_text(
                    self.spec.read_text(encoding="utf-8") + "\nchanged\n",
                    encoding="utf-8",
                ),
            ),
            (
                "tickets",
                lambda: self.tickets.write_text(
                    self.tickets.read_text(encoding="utf-8") + "\nchanged\n",
                    encoding="utf-8",
                ),
            ),
            (
                "verification profile",
                lambda: self.profile["signals"].append("public-blast-radius"),
            ),
        )
        for label, mutate in mutations:
            with self.subTest(label=label):
                self.setUp()
                mutate()
                completed = self.run_claim()
                self.assertNotEqual(completed.returncode, 0)
                _, header, _ = self.read()
                self.assertEqual(header["status"], "invalid")

    def test_missing_malformed_active_and_terminal_cannot_claim(self) -> None:
        module = load_module()
        self.path.unlink()
        missing = self.run_claim()
        self.assertNotEqual(missing.returncode, 0)

        self.path.write_text("not a manifest\n", encoding="utf-8")
        malformed = self.run_claim()
        self.assertNotEqual(malformed.returncode, 0)

        for status in ("active", "completed", "invalid", "failed"):
            with self.subTest(status=status):
                header = self.build_header()
                if status == "active":
                    header["status"] = status
                    header["claim"] = {"actor": "codex", "id": "existing"}
                    header["timestamps"]["claimed_at"] = (
                        "2026-07-30T01:01:00Z"
                    )
                elif status == "invalid":
                    header["status"] = status
                    header["timestamps"]["finished_at"] = (
                        "2026-07-30T01:01:00Z"
                    )
                else:
                    header["status"] = status
                    header["claim"] = {"actor": "codex", "id": "existing"}
                    header["timestamps"]["claimed_at"] = (
                        "2026-07-30T01:01:00Z"
                    )
                    header["timestamps"]["finished_at"] = (
                        "2026-07-30T01:02:00Z"
                    )
                self.write_manifest(header)
                completed = self.run_claim()
                self.assertNotEqual(completed.returncode, 0)
                reread, _ = module.parse_document(
                    self.path.read_text(encoding="utf-8")
                )
                self.assertEqual(reread["status"], status)

    def test_strict_parser_rejects_unknown_duplicate_and_mistyped_fields(
        self,
    ) -> None:
        module, header, body = self.read()
        extra = dict(header)
        extra["unknown"] = True
        mistyped = dict(header)
        mistyped["status"] = []
        documents = (
            module.render_document(extra, body),
            module.render_document(mistyped, body),
            module.render_document(header, body).replace(
                '"status": "ready",',
                '"status": "ready",\n  "status": "ready",',
                1,
            ),
        )
        for document in documents:
            with self.assertRaises(module.StateError):
                module.parse_document(document)

    def test_replace_failure_preserves_readable_ready_manifest(self) -> None:
        module, before, body = self.read()
        arguments = module.parse_args(self.claim_command()[2:])

        with mock.patch.object(
            module.os, "replace", side_effect=OSError("simulated failure")
        ):
            with self.assertRaises(OSError):
                module.claim(arguments)

        after, after_body = module.parse_document(
            self.path.read_text(encoding="utf-8")
        )
        self.assertEqual(after, before)
        self.assertEqual(after_body, body)

    def test_post_replace_failure_reports_committed_recovery_state(self) -> None:
        module, _, _ = self.read()
        arguments = self.claim_command()[2:]
        stderr = io.StringIO()

        with mock.patch.object(
            module.os,
            "fsync",
            side_effect=(None, OSError("simulated directory fsync failure")),
        ):
            with mock.patch.object(module.sys, "argv", [str(SCRIPT), *arguments]):
                with redirect_stderr(stderr):
                    exit_code = module.main()

        _, header, _ = self.read()
        self.assertEqual(exit_code, 1)
        self.assertEqual(header["status"], "active")
        self.assertEqual(header["claim"]["id"], "run-1")
        self.assertEqual(
            stderr.getvalue().strip(),
            "prep state error: manifest: transition committed but durability "
            f"verification failed; inspect {self.path} before recovery",
        )

    def test_prep_writer_to_drive_terminal_roundtrip(self) -> None:
        self.path.unlink()
        create = subprocess.run(
            [
                sys.executable,
                str(PREP_SCRIPT),
                "create",
                "--output",
                str(self.path),
                "--task-id",
                self.source,
                "--task-anchor",
                self.source,
                "--repository-root",
                str(self.root),
                "--worktree",
                str(self.root),
                "--branch",
                "main",
                "--base-head",
                self.base_head,
                "--source",
                self.source,
                "--dirty-inventory-json",
                json.dumps(self.dirty),
                "--instruction-inventory-json",
                json.dumps(self.instructions),
                "--spec",
                str(self.spec),
                "--ticket-mode",
                "tickets",
                "--tickets",
                str(self.tickets),
                "--verification-profile-json",
                json.dumps(self.profile),
                "--prior-art-ref",
                "none",
                "--created-at",
                "2026-07-30T01:00:00Z",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        validated = subprocess.run(
            [sys.executable, str(SCRIPT), "validate", str(self.path)],
            text=True,
            capture_output=True,
            check=False,
        )
        claimed = self.run_claim()
        finalized = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "finalize",
                str(self.path),
                "--claim-id",
                "run-1",
                "--status",
                "completed",
                "--finished-at",
                "2026-07-30T01:02:00Z",
            ],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(create.returncode, 0, create.stderr)
        self.assertEqual(validated.returncode, 0, validated.stderr)
        self.assertEqual(claimed.returncode, 0, claimed.stderr)
        self.assertEqual(finalized.returncode, 0, finalized.stderr)
        _, header, _ = self.read()
        self.assertEqual(header["status"], "completed")
        self.assertEqual(header["claim"]["id"], "run-1")

    def test_finalize_rejects_wrong_claim_without_mutation(self) -> None:
        self.assertEqual(self.run_claim().returncode, 0)
        before = self.path.read_text(encoding="utf-8")

        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "finalize",
                str(self.path),
                "--claim-id",
                "wrong-run",
                "--status",
                "failed",
                "--finished-at",
                "2026-07-30T01:02:00Z",
            ],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertNotEqual(completed.returncode, 0)
        self.assertEqual(self.path.read_text(encoding="utf-8"), before)


if __name__ == "__main__":
    unittest.main()
