#!/usr/bin/env python3
import os
import shlex
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from codex_eval_adapter import (
    CodexObservation,
    LiveGitApprovalGate,
    _build_turn_start_params,
    _hide_project_skills_from_git,
    _read_event_log,
    _remove_project_skills,
    _restore_git_exclude,
    _scrubbed_child_env,
    _prepare_live_fixture,
    _stage_project_skills,
)


class CodexObservationTest(unittest.TestCase):
    def test_preserves_progress_messages_but_derives_status_from_last_message(self) -> None:
        observation = CodexObservation()
        for item_id, text in [
            ("progress", "▶️ Progress\nDecision: publish next"),
            ("final", "## PR respond\n✅ Pass\nStatus: Pass"),
        ]:
            observation.consume(
                {
                    "method": "item/completed",
                    "params": {
                        "item": {
                            "type": "agent_message" if item_id == "progress" else "agentMessage",
                            "id": item_id,
                            "text": text,
                        }
                    },
                }
            )

        result = observation.result(
            skill="tk-pr-respond",
            mode="behavior",
            available_skills=["tk-pr-respond"],
            selected=True,
            events=[],
        )

        self.assertIn("▶️ Progress", result["output"])
        self.assertIn("## PR respond", result["output"])
        self.assertEqual(result["terminal_status"], "Pass")
        self.assertEqual(result["tool_uses"], 0)

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
            approval_policy="on-request",
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
                "writableRoots": [str(checkout)],
                "networkAccess": False,
            },
        )
        self.assertNotIn("dangerFullAccess", str(params))
        self.assertEqual(params["approvalPolicy"], "on-request")

    def test_child_environment_drops_unrelated_secrets(self) -> None:
        original = os.environ.get("AWS_SECRET_ACCESS_KEY")
        os.environ["AWS_SECRET_ACCESS_KEY"] = "do-not-inherit"
        try:
            child = _scrubbed_child_env()
        finally:
            if original is None:
                os.environ.pop("AWS_SECRET_ACCESS_KEY", None)
            else:
                os.environ["AWS_SECRET_ACCESS_KEY"] = original

        self.assertNotIn("AWS_SECRET_ACCESS_KEY", child)
        self.assertIn("PATH", child)

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

    def test_cold_start_fixture_keeps_source_and_creates_no_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            checkout = Path(directory)
            subprocess.run(["git", "init", "-qb", "main"], cwd=checkout, check=True)
            prompt = "/tk-drive Create canary-choice.txt containing alpha."

            result = _prepare_live_fixture(
                checkout,
                checkout / ".agents" / "skills",
                prompt,
            )

            self.assertEqual(result, prompt)
            self.assertFalse((checkout / ".tigerkit/prep.md").exists())
            self.assertTrue((checkout / ".tigerkit/no-hooks").is_dir())

    def test_respond_ci_fixture_requires_commit_push_reply_and_resolution(self) -> None:
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

            prompt = _prepare_live_fixture(
                checkout,
                checkout / ".agents" / "skills",
                "[tigerkit-eval:prepared-respond-ci]\n/tk-pr-respond --ci",
            )
            self.assertIn("remote-publish", prompt)
            self.assertTrue(prompt.endswith("\n/tk-pr-respond --ci"))
            transport = checkout / ".tigerkit/respond-ci-fixture.py"
            read = subprocess.run(
                [sys.executable, str(transport), "read"],
                cwd=checkout,
                text=True,
                capture_output=True,
                check=True,
            ).stdout
            self.assertIn('"thread_id": "T-EVAL-1"', read)

            (checkout / "respond-canary.txt").write_text("resolved\n", encoding="utf-8")
            subprocess.run(["git", "add", "respond-canary.txt"], cwd=checkout, check=True)
            subprocess.run(["git", "commit", "-qm", "canary"], cwd=checkout, check=True)
            subprocess.run([sys.executable, str(transport), "push"], cwd=checkout, check=True)
            subprocess.run(
                [
                    sys.executable,
                    str(transport),
                    "reply",
                    "Fixed.",
                    "_🤖 본 코멘트는 AI가 작성했습니다._",
                ],
                cwd=checkout,
                check=True,
            )
            subprocess.run([sys.executable, str(transport), "resolve"], cwd=checkout, check=True)
            verified = subprocess.run(
                [sys.executable, str(transport), "verify"],
                cwd=checkout,
                text=True,
                capture_output=True,
                check=True,
            ).stdout
            self.assertIn('"complete": true', verified)

    def test_prepared_live_fixture_is_strict_same_run_continuation(self) -> None:
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
            subprocess.run(
                ["git", "checkout", "--detach", "-q"],
                cwd=checkout,
                check=True,
            )
            skills_target = checkout / ".agents" / "skills"
            drive_scripts = skills_target / "tk-drive" / "scripts"
            drive_scripts.mkdir(parents=True)
            source_script = (
                Path(__file__).resolve().parents[2]
                / "tk-drive"
                / "scripts"
                / "preflight.py"
            )
            (drive_scripts / "preflight.py").write_bytes(
                source_script.read_bytes()
            )

            prompt = _prepare_live_fixture(
                checkout,
                skills_target,
                "[tigerkit-eval:prepared-two-unit]\n/tk-drive",
            )
            manifest = checkout / ".tigerkit" / "prep.md"
            self.assertIn("infer the next action", prompt)
            self.assertTrue(prompt.endswith("\n/tk-drive"))
            self.assertTrue(
                manifest.read_text(encoding="utf-8").startswith(
                    "# TigerKit preflight\n\n```json\n"
                )
            )
            self.assertTrue((checkout / ".git").is_dir())
            self.assertTrue((checkout / ".tigerkit/no-hooks").is_dir())
            self.assertEqual(
                subprocess.run(
                    ["git", "config", "--local", "--get", "core.hooksPath"],
                    cwd=checkout,
                    text=True,
                    capture_output=True,
                    check=True,
                ).stdout.strip(),
                str(checkout / ".tigerkit/no-hooks"),
            )
            self.assertEqual(
                subprocess.run(
                    ["git", "branch", "--show-current"],
                    cwd=checkout,
                    text=True,
                    capture_output=True,
                    check=True,
                ).stdout.strip(),
                "tigerkit-eval-two-unit",
            )
            self.assertNotIn('"status"', manifest.read_text(encoding="utf-8"))
            self.assertNotIn('"cursor"', manifest.read_text(encoding="utf-8"))
            self.assertIn('"additional_review": "not-required"', manifest.read_text(encoding="utf-8"))
            tickets = (checkout / ".tigerkit" / "tickets.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("T-EVAL-ALPHA", tickets)
            self.assertIn("T-EVAL-BETA", tickets)

    def test_live_git_approval_is_limited_to_exact_fixture_add_and_commit(
        self,
    ) -> None:
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
            (checkout / "canary-ready.txt").write_text("ready\n", encoding="utf-8")
            gate = LiveGitApprovalGate(checkout, "single")
            base = {
                "cwd": str(checkout),
                "networkApprovalContext": None,
                "additionalPermissions": None,
            }

            self.assertTrue(gate({**base, "command": "git add -- canary-ready.txt"}))
            self.assertTrue(
                gate(
                    {
                        **base,
                        "command": (
                            "/usr/bin/zsh -lc "
                            "'git add -- canary-ready.txt'"
                        ),
                    }
                )
            )
            branch = subprocess.check_output(
                ["git", "branch", "--show-current"],
                cwd=checkout,
                text=True,
            ).strip()
            head = subprocess.check_output(
                ["git", "rev-parse", "HEAD"],
                cwd=checkout,
                text=True,
            ).strip()
            script = "\n".join(
                (
                    "git add -- canary-ready.txt",
                    "git diff --cached --stat",
                    "git diff --cached --numstat",
                    "git diff --cached --name-status",
                    "git diff --cached --check",
                    "git diff --cached -- canary-ready.txt",
                    f'test "$(git branch --show-current)" = {branch}',
                    f'test "$(git rev-parse HEAD)" = {head}',
                    'test "$(git diff --cached --name-only)" = canary-ready.txt',
                    'git commit -m "test: add canary"',
                )
            )
            wrapped_script = f"/usr/bin/zsh -lc {shlex.quote(script)}"
            self.assertTrue(gate({**base, "command": wrapped_script}))
            self.assertFalse(
                gate(
                    {
                        **base,
                        "command": wrapped_script.replace(
                            "git diff --cached --check",
                            "touch escaped",
                        ),
                    }
                )
            )
            for unsafe_commit in (
                'touch escaped -m "test: add canary"',
                'git commit -m "$(touch escaped)"',
                'git commit -m "`touch escaped`"',
            ):
                self.assertFalse(
                    gate(
                        {
                            **base,
                            "command": f"/usr/bin/zsh -lc {shlex.quote(script.replace('git commit -m \"test: add canary\"', unsafe_commit))}",
                        }
                    )
                )
            verified_worktree = " && ".join(
                (
                    "git add -- canary-ready.txt",
                    "git diff --cached --stat",
                    "git diff --cached --numstat",
                    "git diff --cached --name-only",
                    "git diff --cached -- canary-ready.txt",
                    f'test "$(git branch --show-current)" = {branch}',
                    f'test "$(git rev-parse HEAD)" = {head}',
                    'test "$(wc -c < canary-ready.txt | tr -d \' \')" = 6',
                    'test "$(od -An -tx1 canary-ready.txt | tr -d \' \\n\')" = 72656164790a',
                )
            )
            self.assertTrue(
                gate(
                    {
                        **base,
                        "command": f"/usr/bin/zsh -lc {shlex.quote(verified_worktree)}",
                    }
                )
            )
            verified_commit = " && ".join(
                (
                    "git add -- canary-ready.txt",
                    "git diff --cached --stat",
                    "git diff --cached --numstat",
                    "git diff --cached --name-only",
                    "git diff --cached -- canary-ready.txt",
                    f'test "$(git branch --show-current)" = {branch}',
                    f'test "$(git rev-parse HEAD)" = {head}',
                    'test "$(git diff --cached --name-only)" = canary-ready.txt',
                    'test "$(git show :canary-ready.txt | wc -c | tr -d \' \')" = 6',
                    'test "$(git show :canary-ready.txt | od -An -tx1 | tr -d \' \\n\')" = 72656164790a',
                    'git commit -m "test: add canary"',
                )
            )
            self.assertTrue(
                gate(
                    {
                        **base,
                        "command": f"/usr/bin/zsh -lc {shlex.quote(verified_commit)}",
                    }
                )
            )
            self.assertFalse(
                gate(
                    {
                        **base,
                        "command": f"/usr/bin/zsh -lc {shlex.quote(verified_commit.replace(head, '0' * 40))}",
                    }
                )
            )
            escaped = checkout / "escaped"
            injected_commit = verified_commit.replace(
                'git commit -m "test: add canary"',
                'git commit -m "$(touch escaped)"',
            )
            self.assertFalse(
                gate(
                    {
                        **base,
                        "command": f"/usr/bin/zsh -lc {shlex.quote(injected_commit)}",
                    }
                )
            )
            self.assertFalse(escaped.exists())
            for command in (
                "./git add -- canary-ready.txt",
                "/tmp/git add -- canary-ready.txt",
                verified_commit.replace(
                    'git commit -m "test: add canary"',
                    'touch escaped -m "test: add canary"',
                ),
                verified_commit.replace(
                    'git commit -m "test: add canary"',
                    'git commit -m "`touch escaped`"',
                ),
            ):
                self.assertFalse(
                    gate(
                        {
                            **base,
                            "command": f"/usr/bin/zsh -lc {shlex.quote(command)}",
                        }
                    )
                )
            self.assertFalse(escaped.exists())
            self.assertTrue(
                gate(
                    {
                        **base,
                        "command": (
                            "git add -- canary-ready.txt && "
                            "git commit -m 'add canary'"
                        ),
                    }
                )
            )
            self.assertFalse(gate({**base, "command": "git add -A"}))
            self.assertFalse(
                gate(
                    {
                        **base,
                        "command": "git add canary-ready.txt && touch escaped",
                    }
                )
            )
            self.assertFalse(
                gate(
                    {
                        **base,
                        "command": (
                            "/tmp/zsh -lc "
                            "'git add -- canary-ready.txt'"
                        ),
                    }
                )
            )
            self.assertFalse(
                gate(
                    {
                        **base,
                        "command": (
                            "/usr/bin/zsh -lc "
                            "'git add canary-ready.txt; touch escaped'"
                        ),
                    }
                )
            )
            self.assertFalse(
                gate(
                    {
                        **base,
                        "command": "git add canary-ready.txt",
                        "additionalPermissions": {"network": {"enabled": True}},
                    }
                )
            )
            self.assertFalse(
                gate(
                    {
                        **base,
                        "command": (
                            "git add canary-ready.txt && "
                            "git commit -m canary && touch escaped"
                        ),
                    }
                )
            )
            self.assertFalse(
                gate(
                    {
                        **base,
                        "command": (
                            "git add canary-ready.txt && "
                            "git commit -m \"$HOME\""
                        ),
                    }
                )
            )
            staged_content_script = " && ".join(
                (
                    "git add -- canary-ready.txt",
                    'test "$(git show :canary-ready.txt | wc -c | tr -d \' \')" = 6',
                    (
                        'test "$(git show :canary-ready.txt | od -An -tx1 | '
                        'tr -d \' \\\\n\')" = 72656164790a'
                    ),
                    "git diff --cached --stat",
                    "git diff --cached --numstat",
                    "git diff --cached --name-only",
                    "git diff --cached --check",
                    "git diff --cached -- canary-ready.txt",
                    "git rev-parse HEAD",
                    "git branch --show-current",
                )
            )
            wrapped_staged_content = (
                f"/usr/bin/zsh -lc {shlex.quote(staged_content_script)}"
            )
            self.assertTrue(gate({**base, "command": wrapped_staged_content}))
            self.assertFalse(
                gate(
                    {
                        **base,
                        "command": wrapped_staged_content.replace(
                            "72656164790a",
                            "00",
                        ),
                    }
                )
            )
            subprocess.run(
                ["git", "add", "--", "canary-ready.txt"],
                cwd=checkout,
                check=True,
            )
            self.assertTrue(gate({**base, "command": "git commit -m 'add canary'"}))
            self.assertFalse(gate({**base, "command": "git commit -am 'escape'"}))

    def test_event_log_rejects_malformed_rows(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.jsonl"
            path.write_text(
                '{"type":"phase_invocation","phase":"tk-implement"}\n'
                '{"type":"phase_invocation","phase":"tk-implment"}\n',
                encoding="utf-8",
            )

            with self.assertRaisesRegex(RuntimeError, "line 2"):
                _read_event_log(path)


if __name__ == "__main__":
    unittest.main()
