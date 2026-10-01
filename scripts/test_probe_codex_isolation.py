from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
import unittest
from unittest.mock import patch

from probe_codex_isolation import invoke, probe, stop_process


class CodexIsolationProbeTest(unittest.TestCase):
    @unittest.skipUnless(os.name == "posix", "POSIX process-group regression")
    def test_owned_descendant_stops_after_timeout_completion_and_interrupt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            cli = root / "spawn-cli"
            cli.write_text('''#!/usr/bin/env python3
import subprocess, sys, time
from pathlib import Path
child = subprocess.Popen([sys.executable, '-c',
 'import signal,time; signal.signal(signal.SIGTERM, signal.SIG_IGN); time.sleep(30)'],
 stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
Path('child.pid').write_text(str(child.pid))
if sys.argv[1] != 'completed': time.sleep(30)
''', encoding="utf-8")
            cli.chmod(0o700)
            for mode in ("timeout", "completed", "interrupted"):
                with self.subTest(mode=mode):
                    home = root / mode
                    (home / ".codex").mkdir(parents=True)
                    original = subprocess.Popen.communicate
                    def interrupt(process, *args, **kwargs):
                        try:
                            original(process, timeout=0.2)
                        except subprocess.TimeoutExpired:
                            raise KeyboardInterrupt
                    try:
                        if mode == "interrupted":
                            with patch.object(subprocess.Popen, "communicate", interrupt):
                                with self.assertRaises(KeyboardInterrupt):
                                    invoke(str(cli), [mode], home, home, timeout=0.2)
                        else:
                            status, _, clean = invoke(str(cli), [mode], home, home, timeout=0.2)
                            self.assertEqual(status, mode)
                            self.assertTrue(clean)
                        pid = int((home / "child.pid").read_text())
                        deadline = time.monotonic() + 1
                        while time.monotonic() < deadline:
                            state = subprocess.run(['ps', '-p', str(pid), '-o', 'stat='],
                                                   capture_output=True, text=True).stdout.strip()
                            if not state or state.startswith('Z'):
                                break
                            time.sleep(0.01)
                        self.assertTrue(not state or state.startswith('Z'),
                                        "owned child survived invocation cleanup")
                    finally:
                        path = home / "child.pid"
                        if path.exists():
                            try:
                                os.kill(int(path.read_text()), 9)
                            except ProcessLookupError:
                                pass

    def test_unsupported_process_group_cleanup_cannot_pass(self) -> None:
        process = subprocess.Popen([shutil.which("python3"), "-c", "pass"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertFalse(stop_process(process, grouped=False))

    def fake_cli(self, root: Path, *, timeout: bool = False) -> Path:
        cli = root / "cli"
        cli.write_text('''#!/usr/bin/env python3
import json, os, sys, time
from pathlib import Path
home = Path(os.environ['CODEX_HOME'])
if sys.argv[1:] == ['--version']:
 print('codex-cli test')
elif sys.argv[1:] == ['login', 'status']:
 print('Logged in using test auth' if (home / 'auth.json').exists() else 'No auth')
else:
 if 'TIMEOUT_PROBE' in Path(__file__).read_text(): time.sleep(2)
 content = [(home / 'config.toml').read_text()]
 content += [p.read_text() for p in home.glob('skills/*/SKILL.md')]
 content += [p.read_text() for p in Path.cwd().glob('.agents/skills/*/SKILL.md')]
 print(json.dumps([{'role': 'developer', 'content': content}]))
'''.replace("'TIMEOUT_PROBE' in Path(__file__).read_text()", "True" if timeout else "False"),
                       encoding="utf-8")
        cli.chmod(0o700)
        return cli

    def test_observer_reports_catalog_only_and_preserves_auth(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            cli = self.fake_cli(root)
            auth = root / "auth.json"
            auth.write_text('{"synthetic_secret":"DO_NOT_EMIT_871"}')
            original = auth.read_bytes()
            with tempfile.TemporaryDirectory(dir=root) as run:
                result = probe(str(cli), Path(run), timeout=1, auth_file=auth)
                self.assertEqual(result["auth_discovery"], "Pass")
                self.assertEqual(result["auth_unchanged"], "Pass")
                self.assertFalse((Path(run) / "auth-status/.codex/auth.json").exists())
                for signal in ("candidate_catalog_difference", "ambient_skill_catalog_exclusion",
                               "ambient_rule_prompt_exclusion"):
                    self.assertEqual(result[signal], "Pass")
                for signal in ("isolation_status", "skill_activation", "task_execution",
                               "plugins_apps_mcp_exclusion"):
                    self.assertEqual(result[signal], "Unverifiable")
                self.assertNotIn("DO_NOT_EMIT_871", json.dumps(result))
                self.assertNotIn(str(auth), json.dumps(result))
            self.assertFalse(Path(run).exists())
            self.assertEqual(auth.read_bytes(), original)

    def test_timeouts_remain_unverifiable_and_next_run_uses_fresh_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            cli = self.fake_cli(root, timeout=True)
            with tempfile.TemporaryDirectory(dir=root) as first:
                result = probe(str(cli), Path(first), timeout=0.1)
                self.assertEqual(set(result["prompt_input_status"].values()), {"timeout"})
                self.assertEqual(result["candidate_catalog_difference"], "Unverifiable")
                (Path(first) / "state-from-first-run").write_text("obsolete")
            self.assertFalse(Path(first).exists())
            cli = self.fake_cli(root)
            with tempfile.TemporaryDirectory(dir=root) as second:
                self.assertNotEqual(first, second)
                self.assertFalse((Path(second) / "state-from-first-run").exists())
                result = probe(str(cli), Path(second), timeout=1)
                self.assertEqual(result["candidate_catalog_difference"], "Pass")
            self.assertFalse(Path(second).exists())

    @unittest.skipUnless(os.environ.get("TK_EVAL_CODEX_PROBE_LIVE") == "1",
                         "opt-in actual Codex CLI diagnostic")
    def test_actual_cli_auth_discovery_and_conservative_catalog_probe(self) -> None:
        cli = os.environ.get("TK_EVAL_CODEX_PROBE_CLI") or shutil.which("codex")
        self.assertIsNotNone(cli, "live probe requires Codex CLI")
        value = os.environ.get("TK_EVAL_CODEX_PROBE_AUTH_FILE")
        auth = Path(value) if value else None
        with tempfile.TemporaryDirectory() as directory:
            result = probe(cli, Path(directory), timeout=3, auth_file=auth)
            self.assertIsNotNone(result["host_version"])
            if auth is not None:
                self.assertEqual(result["auth_discovery"], "Pass")
                self.assertEqual(result["auth_unchanged"], "Pass")
            self.assertEqual(result["isolation_status"], "Unverifiable")
            self.assertEqual(result["skill_activation"], "Unverifiable")
            self.assertEqual(result["task_execution"], "Unverifiable")
        self.assertFalse(Path(directory).exists())
