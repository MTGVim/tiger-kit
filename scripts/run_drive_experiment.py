#!/usr/bin/env python3
"""Compare tk-drive with explicit phase composition on matched scenarios."""
from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Mapping

from run_skill_evals import git_head, isolated_checkout, resolve_ref, run_adapter

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "evals/drive-ab.json"
BUILTIN_ADAPTER = ROOT / "scripts/adapters/tigerkit_host_adapter.py"
HOST_ORDER = ("codex", "claude-code", "hermes-agent")
ARMS = ("drive", "composition")


def load_manifest() -> dict[str, object]:
    value = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or value.get("version") != 1:
        raise ValueError("drive A/B manifest must be a version-1 object")
    if value.get("hosts") != list(HOST_ORDER):
        raise ValueError("drive A/B hosts must be ordered codex, claude-code, hermes-agent")
    runs = value.get("runs")
    scenarios = value.get("scenarios")
    if isinstance(runs, bool) or not isinstance(runs, int) or runs < 2:
        raise ValueError("drive A/B runs must be at least two")
    if not isinstance(scenarios, list) or len(scenarios) < 3:
        raise ValueError("drive A/B needs at least three scenarios")
    ids: set[str] = set()
    for index, scenario in enumerate(scenarios, 1):
        if not isinstance(scenario, dict):
            raise ValueError(f"drive A/B scenario {index} must be an object")
        scenario_id = scenario.get("id")
        if not isinstance(scenario_id, str) or not scenario_id or scenario_id in ids:
            raise ValueError(f"drive A/B scenario {index} needs a unique id")
        ids.add(scenario_id)
        for field in ("source", "drive_required_phases", "composition_required_phases", "expected_terminal", "verification"):
            if field not in scenario:
                raise ValueError(f"drive A/B scenario {scenario_id} needs {field}")
        if not isinstance(scenario.get("expect_commit"), bool):
            raise ValueError(f"drive A/B scenario {scenario_id} needs expect_commit")
    return value


def prompt_for(arm: str, source: str) -> str:
    if arm == "drive":
        return f"$tk-drive {source}"
    return (
        "Do not invoke tk-drive. Execute the same source through explicit TigerKit phase owners: "
        "use $tk-grill-me only for a material user decision, then $tk-to-spec, use $tk-to-tickets "
        "only for multiple independent units, invoke $tk-implement once per unit, and perform one final "
        "broad verification. Do not claim the drive orchestration path. Source: " + source
    )


def run_verification(checkout: Path, commands: object) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    if not isinstance(commands, list):
        return rows
    for command in commands:
        if not isinstance(command, str):
            continue
        completed = subprocess.run(
            shlex.split(command),
            cwd=checkout,
            text=True,
            capture_output=True,
            check=False,
        )
        rows.append(
            {
                "command": command,
                "passed": completed.returncode == 0,
                "returncode": completed.returncode,
                "stdout_tail": completed.stdout[-1000:],
                "stderr_tail": completed.stderr[-1000:],
            }
        )
    return rows


def phase_sequence(events: object) -> list[str]:
    if not isinstance(events, list):
        return []
    return [
        str(event["phase"])
        for event in events
        if isinstance(event, dict)
        and event.get("type") == "phase_invocation"
        and isinstance(event.get("phase"), str)
    ]


def final_index(events: object) -> int | None:
    if not isinstance(events, list):
        return None
    for index, event in enumerate(events):
        if isinstance(event, dict) and event.get("type") == "final_output":
            return index
    return None


def ordered_phases(events: object, required: list[str]) -> bool:
    if not isinstance(events, list):
        return False
    cursor = -1
    for required_phase in required:
        found = None
        for index, event in enumerate(events[cursor + 1 :], cursor + 1):
            if isinstance(event, dict) and event.get("type") == "phase_invocation" and event.get("phase") == required_phase:
                found = index
                break
        if found is None:
            return False
        cursor = found
    terminal = final_index(events)
    return terminal is not None and cursor < terminal


def run_arm(
    host: str,
    candidate: Path,
    scenario: Mapping[str, object],
    arm: str,
    *,
    adapter_command: str,
    run_number: int,
) -> dict[str, object]:
    with isolated_checkout(candidate) as checkout:
        initial_head = git_head(checkout)
        result = run_adapter(
            adapter_command,
            checkout=checkout,
            skill="tk-drive" if arm == "drive" else "tk-to-spec",
            prompt=prompt_for(arm, str(scenario["source"])),
            mode="drive-ab",
            host=host,
        )
        verification = run_verification(checkout, scenario.get("verification"))
        final_head = git_head(checkout)
    expected_terminal = scenario.get("expected_terminal", [])
    required = scenario.get(f"{arm}_required_phases", [])
    expect_commit = scenario.get("expect_commit") is True
    terminal_ok = isinstance(expected_terminal, list) and result.get("terminal_status") in expected_terminal
    phases_ok = isinstance(required, list) and ordered_phases(result.get("events"), [str(value) for value in required])
    commit_ok = (final_head != initial_head) if expect_commit else (final_head == initial_head)
    verification_ok = all(bool(row["passed"]) for row in verification)
    passed = terminal_ok and phases_ok and commit_ok and verification_ok
    return {
        "host": host,
        "scenario": scenario["id"],
        "arm": arm,
        "run": run_number,
        "passed": passed,
        "terminal_status": result.get("terminal_status"),
        "terminal_ok": terminal_ok,
        "required_phases": required,
        "observed_phases": phase_sequence(result.get("events")),
        "continuation_ok": phases_ok,
        "commit_ok": commit_ok,
        "verification": verification,
        "total_tokens": result.get("total_tokens"),
        "duration_ms": result.get("duration_ms"),
    }


def summarize(records: list[dict[str, object]]) -> dict[str, object]:
    rows: dict[str, dict[str, object]] = {}
    for arm in ARMS:
        arm_records = [row for row in records if row.get("arm") == arm]
        passed = sum(row.get("passed") is True for row in arm_records)
        continuations = sum(row.get("continuation_ok") is True for row in arm_records)
        tokens = [float(row["total_tokens"]) for row in arm_records if isinstance(row.get("total_tokens"), (int, float))]
        durations = [float(row["duration_ms"]) for row in arm_records if isinstance(row.get("duration_ms"), (int, float))]
        rows[arm] = {
            "runs": len(arm_records),
            "pass_rate": passed / len(arm_records) if arm_records else 0.0,
            "continuation_rate": continuations / len(arm_records) if arm_records else 0.0,
            "mean_tokens": sum(tokens) / len(tokens) if tokens else None,
            "mean_duration_ms": sum(durations) / len(durations) if durations else None,
        }
    drive = rows["drive"]
    composition = rows["composition"]
    drive_pass = float(drive["pass_rate"])
    composition_pass = float(composition["pass_rate"])
    drive_continuation = float(drive["continuation_rate"])
    composition_continuation = float(composition["continuation_rate"])
    if drive_pass >= composition_pass and drive_continuation >= composition_continuation:
        decision = "Keep"
    elif drive_pass >= 0.67 and drive_continuation >= 0.67:
        decision = "Experimental"
    elif composition_pass - drive_pass >= 0.34:
        decision = "RemoveCandidate"
    else:
        decision = "Review"
    return {"decision": decision, "arms": rows}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", default="HEAD")
    parser.add_argument("--adapter-command")
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = Path(args.output).resolve()
    if output == ROOT or ROOT in output.parents:
        raise SystemExit("--output must be outside the repository")
    output.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest()
    candidate_sha = resolve_ref(args.candidate)
    adapter_command = args.adapter_command or f"{shlex.quote(sys.executable)} {shlex.quote(str(BUILTIN_ADAPTER))}"

    candidate = ROOT
    records: list[dict[str, object]] = []
    host_attempts: list[dict[str, object]] = []
    selected_host: str | None = None
    for host in HOST_ORDER:
        host_records: list[dict[str, object]] = []
        try:
            for scenario in manifest["scenarios"]:  # type: ignore[index]
                for run_number in range(1, int(manifest["runs"]) + 1):
                    for arm in ARMS:
                        host_records.append(
                            run_arm(
                                host,
                                candidate,
                                scenario,
                                arm,
                                adapter_command=adapter_command,
                                run_number=run_number,
                            )
                        )
        except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
            host_attempts.append({"host": host, "status": "unavailable", "reason": str(exc)})
            continue
        selected_host = host
        records = host_records
        host_attempts.append({"host": host, "status": "completed"})
        break

    if selected_host is None:
        result = {
            "status": "Advisory",
            "candidate": candidate_sha,
            "selected_host": None,
            "hosts": host_attempts,
            "decision": "Unverifiable",
            "records": [],
        }
    else:
        summary = summarize(records)
        result = {
            "status": "Pass",
            "candidate": candidate_sha,
            "selected_host": selected_host,
            "hosts": host_attempts,
            **summary,
            "records": records,
        }
    (output / "drive-ab.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
