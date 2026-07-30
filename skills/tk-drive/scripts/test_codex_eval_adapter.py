#!/usr/bin/env python3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from codex_eval_adapter import (
    CodexObservation,
    _build_turn_start_params,
    _hide_project_skills_from_git,
    _read_event_log,
    _remove_project_skills,
    _restore_git_exclude,
    _prepare_live_fixture,
    _stage_project_skills,
)


class CodexObservationTest(unittest.TestCase):
    def test_extracts_marked_phase_order_bulleted_status_and_metrics(self) -> None:
        observation = CodexObservation()
        observation.consume(
            {
                "method": "item/completed",
                "params": {
                    "item": {
                        "type": "agentMessage",
                        "id": "message-1",
                        "text": "Outcome: complete\n\n- Status: Pass",
                        "phase": "final_answer",
                    }
                },
            }
        )
        observation.consume(
            {
                "method": "thread/tokenUsage/updated",
                "params": {
                    "tokenUsage": {
                        "total": {
                            "totalTokens": 21,
                            "inputTokens": 13,
                            "outputTokens": 8,
                        }
                    }
                },
            }
        )
        observation.consume(
            {
                "method": "turn/completed",
                "params": {
                    "turn": {
                        "status": "completed",
                        "error": None,
                        "durationMs": 1200,
                    }
                },
            }
        )
        events = [
            {"type": "phase_invocation", "phase": "tk-implement"},
            {
                "type": "phase_receipt",
                "phase": "tk-implement",
                "state": "Pass",
                "transition": "aggregate verification",
            },
            {"type": "phase_invocation", "phase": "tk-implement"},
        ]

        result = observation.result(
            skill="tk-drive",
            mode="behavior",
            available_skills=["tk-drive", "tk-implement"],
            selected=True,
            events=events,
        )

        self.assertEqual(result["terminal_status"], "Pass")
        self.assertEqual(result["total_tokens"], 21)
        self.assertEqual(result["duration_ms"], 1200)
        self.assertEqual(result["selected_skill"], "tk-drive")
        self.assertEqual(
            result["events"],
            events + [{"type": "final_output", "terminal_status": "Pass"}],
        )

    def test_missing_status_does_not_invent_success(self) -> None:
        observation = CodexObservation()
        observation.consume(
            {
                "method": "item/completed",
                "params": {
                    "item": {
                        "type": "agentMessage",
                        "id": "message-1",
                        "text": "Success state: Ready",
                    }
                },
            }
        )
        observation.consume(
            {
                "method": "turn/completed",
                "params": {
                    "turn": {
                        "status": "completed",
                        "error": None,
                        "durationMs": 900,
                    }
                },
            }
        )

        result = observation.result(
            skill="tk-drive",
            mode="behavior",
            available_skills=["tk-drive"],
            selected=True,
            events=[],
        )

        self.assertEqual(result["terminal_status"], "Unverifiable")
        self.assertEqual(
            result["events"],
            [{"type": "final_output", "terminal_status": "Unverifiable"}],
        )

    def test_turn_start_uses_explicit_skill_and_narrow_git_write_scope(self) -> None:
        checkout = Path("/tmp/tigerkit-eval-checkout")
        skill_path = checkout / ".agents/skills/tk-drive/SKILL.md"

        params = _build_turn_start_params(
            thread_id="thread-1",
            checkout=checkout,
            prompt="$tk-drive do the work",
            skill="tk-drive",
            skill_path=skill_path,
        )

        self.assertEqual(
            params["input"],
            [
                {"type": "text", "text": "$tk-drive do the work"},
                {
                    "type": "skill",
                    "name": "tk-drive",
                    "path": str(skill_path),
                },
            ],
        )
        self.assertEqual(
            params["sandboxPolicy"],
            {
                "type": "workspaceWrite",
                "writableRoots": [str(checkout), str(checkout / ".git")],
                "networkAccess": False,
            },
        )

    def test_project_skill_staging_is_git_invisible_and_fully_restored(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            checkout = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=checkout, check=True)
            subprocess.run(
                ["git", "config", "user.email", "canary@example.invalid"],
                cwd=checkout,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Canary"],
                cwd=checkout,
                check=True,
            )
            source = checkout / "skills" / "tk-drive"
            source.mkdir(parents=True)
            (source / "SKILL.md").write_text("# tk-drive\n", encoding="utf-8")
            subprocess.run(["git", "add", "skills"], cwd=checkout, check=True)
            subprocess.run(["git", "commit", "-qm", "fixture"], cwd=checkout, check=True)
            exclude = checkout / ".git" / "info" / "exclude"
            original = exclude.read_bytes()

            staged, remove_agents_dir = _stage_project_skills(checkout)
            exclude_state = _hide_project_skills_from_git(checkout)
            dirty_while_staged = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=checkout,
                text=True,
                capture_output=True,
                check=True,
            ).stdout
            _remove_project_skills(staged, remove_agents_dir)
            _restore_git_exclude(exclude_state)

            self.assertEqual(dirty_while_staged, "")
            self.assertEqual(exclude.read_bytes(), original)
            self.assertFalse((checkout / ".agents").exists())

    def test_prepared_live_fixture_is_strict_and_source_free(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            checkout = Path(directory)
            subprocess.run(["git", "init", "-qb", "main"], cwd=checkout, check=True)
            subprocess.run(
                ["git", "config", "user.email", "canary@example.invalid"],
                cwd=checkout,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Canary"],
                cwd=checkout,
                check=True,
            )
            (checkout / "README.md").write_text("fixture\n", encoding="utf-8")
            subprocess.run(["git", "add", "README.md"], cwd=checkout, check=True)
            subprocess.run(["git", "commit", "-qm", "fixture"], cwd=checkout, check=True)
            skills_target = checkout / ".agents" / "skills"
            prep_scripts = skills_target / "tk-prep" / "scripts"
            prep_scripts.mkdir(parents=True)
            source_script = (
                Path(__file__).resolve().parents[2]
                / "tk-prep"
                / "scripts"
                / "prep_manifest.py"
            )
            (prep_scripts / "prep_manifest.py").write_bytes(
                source_script.read_bytes()
            )

            prompt = _prepare_live_fixture(
                checkout,
                skills_target,
                "[tigerkit-eval:prepared-two-unit]\n/tk-drive",
            )
            manifest = checkout / ".tigerkit" / "prep.md"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(Path(__file__).with_name("prep_state.py")),
                    "validate",
                    str(manifest),
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(prompt, "/tk-drive")
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn('"status": "ready"', manifest.read_text(encoding="utf-8"))
            tickets = (checkout / ".tigerkit" / "tickets.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("T-EVAL-ALPHA", tickets)
            self.assertIn("T-EVAL-BETA", tickets)

    def test_event_log_rejects_malformed_rows(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.jsonl"
            path.write_text(
                '{"type":"phase_invocation","phase":"tk-implement"}\n'
                '{"type":"phase_receipt","phase":"tk-implement","state":"Draft",'
                '"transition":"aggregate verification"}\n',
                encoding="utf-8",
            )

            with self.assertRaisesRegex(RuntimeError, "line 2"):
                _read_event_log(path)


if __name__ == "__main__":
    unittest.main()
