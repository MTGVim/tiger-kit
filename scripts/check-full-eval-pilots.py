#!/usr/bin/env python3
"""Validate tracked FULL-style TigerKit eval pilot scaffolding."""
from __future__ import annotations

import hashlib
import json
import re
import stat
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any, NoReturn, cast

ROOT = Path(__file__).resolve().parents[1]
PILOTS_DIR = ROOT / "evals" / "full-pilots"
RESULTS_DIR = ROOT / "evals" / "results"
FULL_RESULT_PATH = RESULTS_DIR / "full-reflect-repo-local-safety.json"
FULL_RAW_DIR = RESULTS_DIR / "raw" / "full-reflect-repo-local-safety"
FULL_RESULT_SCHEMA = "tigerkit.full-reflect-repo-local-safety-results/v1"
FULL_SOURCE_SCHEMA = "tigerkit.full-reflect-repo-local-safety-source/v1"
FULL_SCENARIO_IDS = (
    "eligible-repo-local-apply",
    "tracked-claude-local-reject",
    "not-ignored-claude-local-reject",
    "non-git-repo-local-reject",
    "symlink-claude-local-reject",
)
FULL_PLUGIN_COMMIT = "6e540c5621bfa83acbbc35e72e5511fbe2713d45"
FULL_WRAPPER = "ccs codex"
FULL_PROVIDER = "openai-codex"
FULL_CONSUMER = "Claude Code"
FULL_CONSUMER_VERSION = "2.1.150 (Claude Code)"
FULL_MODEL = "gpt-5.5(high)"
FULL_ALLOWED_TOOLS = ["Read", "Grep", "Glob", "Bash"]
FULL_CONTRACT_BLOBS = {
    "commands/reflect.md": "2a904f242c4657abd92a7ff834e7663fa835cff4b87e653af973a9a430678412",
    "docs/reflect-file-policy.md": "294bcaa9ef7cc3d3362ed2495e0a870f0b3584f16115ad2920a8751f411cff4d",
    ".tigerkit/docs/output-contract.md": "eab16292a7f5aa3be02e125710bda0bedce1feaa77e364f4afdb1c6e98a59914",
}
FULL_SOURCE_HASHES = {
    "eligible-repo-local-apply": "0f93caf8ab940e2ecf64ce25f1812e059aba8f0bcce86a52ebe530ff63e9a55e",
    "tracked-claude-local-reject": "ac9a875f41ff0e62879c89b854e10772833b5d91244d1598cad3bd391bbb05ff",
    "not-ignored-claude-local-reject": "2708cf31c6ebebcd188580192143e1dec382d3e4fb1984918b3a586bac2df2e5",
    "non-git-repo-local-reject": "af8ed2408d7a541ecc017ef679bb0a51ee46d7af780ead391b63d7ade71c8b46",
    "symlink-claude-local-reject": "cf6cf1fcc35feb4e78f9218f4231e2018f2834848e3b74b2e05a7fe51aa4e038",
}
FULL_RESULT_HASHES = {
    "eligible-repo-local-apply": ("ad18e388c6cf666005a3c328b441b1a3db94b06ea5f204926da2aeeac0962376", 337),
    "tracked-claude-local-reject": ("309980a38f435ac92ca7ecd6f1cf2af4ba31534e719a627d67f33b357aa261b6", 629),
    "not-ignored-claude-local-reject": ("0ffa4039ad8b5d148dae668fb6ab54426ed8ea2aae97bf1d1a481e8c818e5c2a", 553),
    "non-git-repo-local-reject": ("12c02cc94329ce8b01cb23e2157e090cd7f22e00350904fb88bdc2198849f2ea", 822),
    "symlink-claude-local-reject": ("39e816da2b899e454672e9b131f01b87d01d977058cdb36e356cbf996a9d9ca8", 666),
}
FULL_PROMPT_HASHES = {
    "eligible-repo-local-apply": "dbc1e3cb6deb58dc5a1686523c09340dc15498501471423f706a34f79c944039",
    "tracked-claude-local-reject": "bd6c021f21847301936a394ff2d110d3008816c935481f272194d40e7273eb40",
    "not-ignored-claude-local-reject": "c09d862f4eca9433484a233e21754dfe26134553f2868bb8b279fa4f977502c5",
    "non-git-repo-local-reject": "0e0021962b1a6b9784be5d23588596268b4893b9a9746d91d5e903dfe5c9a27c",
    "symlink-claude-local-reject": "b17766ca0636e406eb43399c2dc78bab39f28a4bca0da1f163c4c5f09ac46c2f",
}
FULL_ARGV_HASHES = {
    "eligible-repo-local-apply": "5060f69f228c90edd5b72cbdd1670e99595ad4f259e303a193b3031fd4c3feef",
    "tracked-claude-local-reject": "f1d9d22c7c537a0313962133d40b3798d0315df6369eeb456585794b2ccea5b8",
    "not-ignored-claude-local-reject": "d1314d66440127580b4cf4a19350de4954a955f78dabfbb1bf7c1954023eeb5a",
    "non-git-repo-local-reject": "b4a7914a6fc3e0208f2a763775560347397f8133a8e080e2d4eebbbc968aabb2",
    "symlink-claude-local-reject": "a05856c844d94a29ed6ee242606cb7dce95cf301f26d1e43fd9fa2640e9f3080",
}
FULL_MODEL_USAGE_HASHES = {
    "eligible-repo-local-apply": "0c765f88f711a6d526409fd0857497b28c9714de75ff90d0dee0eb80335edf5b",
    "tracked-claude-local-reject": "f3a0817167493f74c69d7e96a20638cd40b795f99fcb000bba83d515b8fbad82",
    "not-ignored-claude-local-reject": "0566bb40b451630f9032b1d885bfd44ec49464f33f9c89e0e3c3385a86a2cea6",
    "non-git-repo-local-reject": "72d65e3bd18a8359386f017474182fc492aa90df5ae733d4b5f9370e59f6aef4",
    "symlink-claude-local-reject": "0539c71053b5925cdfd7c6d98c9a50709012fdfa81a35920c13427f729443ca5",
}
FULL_SESSION_IDS = {
    "eligible-repo-local-apply": "6d547556-74b8-45a8-903a-afbe4dd66fd0",
    "tracked-claude-local-reject": "5a87d29a-5d71-4c3c-8d69-38468447e290",
    "not-ignored-claude-local-reject": "5620494a-5c88-4d10-a222-5dd359079778",
    "non-git-repo-local-reject": "427db30e-6ad7-4a2f-af49-bda06011b0a0",
    "symlink-claude-local-reject": "a45715b2-005e-4740-9e10-ffc9de72eaa2",
}
FULL_REASON_RAW = {
    "eligible-repo-local-apply": None,
    "tracked-claude-local-reject": "`tracked_local_file`",
    "not-ignored-claude-local-reject": "`not_ignored`",
    "non-git-repo-local-reject": "`not_git_worktree`",
    "symlink-claude-local-reject": "`symlink_target`",
}
FULL_REASON = {
    scenario_id: None if raw is None else raw.strip("`")
    for scenario_id, raw in FULL_REASON_RAW.items()
}
FULL_APPLIED = {
    "eligible-repo-local-apply": ["R1"],
    "tracked-claude-local-reject": ["NONE"],
    "not-ignored-claude-local-reject": ["NONE"],
    "non-git-repo-local-reject": ["NONE"],
    "symlink-claude-local-reject": ["NONE"],
}
FULL_CHANGED_PATHS = {
    "eligible-repo-local-apply": ["`git-root/CLAUDE.local.md`"],
    "tracked-claude-local-reject": [],
    "not-ignored-claude-local-reject": [],
    "non-git-repo-local-reject": [
        "`state-home/.tigerkit/repos/non-git-repo-local-reject/branches/local/reflect/REFLECT-20260711-174319-R1.yaml`",
        "repo-local guidance target: NONE",
    ],
    "symlink-claude-local-reject": [],
}
FULL_TARGET_PATHS = {
    "eligible-repo-local-apply": "git-root/CLAUDE.local.md",
    "tracked-claude-local-reject": "git-root/CLAUDE.local.md",
    "not-ignored-claude-local-reject": "git-root/CLAUDE.local.md",
    "non-git-repo-local-reject": "fixture-root/workdir/CLAUDE.local.md",
    "symlink-claude-local-reject": "git-root/CLAUDE.local.md",
}
FULL_TURNS = {
    "eligible-repo-local-apply": 4,
    "tracked-claude-local-reject": 4,
    "not-ignored-claude-local-reject": 4,
    "non-git-repo-local-reject": 8,
    "symlink-claude-local-reject": 5,
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

PILOT_SPECS: dict[str, dict[str, Any]] = {
    "reflect-repo-local-safety.json": {
        "surface": "/tk:reflect",
        "focus": "repo-local-write-safety",
        "source_contracts": {
            "commands/reflect.md",
            "docs/reflect-file-policy.md",
            ".tigerkit/docs/output-contract.md",
        },
        "reason_codes_covered": {
            "tracked_local_file",
            "not_ignored",
            "not_git_worktree",
            "symlink_target",
        },
        "required_scenarios": {
            "eligible-repo-local-apply": {"writes_allowed": True, "reason_code": None},
            "tracked-claude-local-reject": {"writes_allowed": False, "reason_code": "tracked_local_file"},
            "not-ignored-claude-local-reject": {"writes_allowed": False, "reason_code": "not_ignored"},
            "non-git-repo-local-reject": {"writes_allowed": False, "reason_code": "not_git_worktree"},
            "symlink-claude-local-reject": {"writes_allowed": False, "reason_code": "symlink_target"},
        },
    },
    "gap-stale-sot-precedence.json": {
        "surface": "/tk:gap",
        "focus": "stale-sot-and-source-precedence",
        "source_contracts": {
            "commands/gap.md",
            "skills/gap/SKILL.md",
            ".tigerkit/docs/output-contract.md",
        },
        "classifications_covered": {
            "ambiguous",
            "missing",
        },
        "evidence_principles_covered": {
            "unresolved_source_precedence_stays_ambiguous",
            "plan_only_current_is_not_implementation_proof",
        },
        "required_scenarios": {
            "stale-plan-vs-live-surface-conflict": {"primary_gap": "ambiguous"},
            "unresolved-source-precedence-stays-ambiguous": {"primary_gap": "ambiguous"},
            "plan-only-current-is-not-implementation-proof": {"primary_gap": "missing"},
        },
    },
    "browser-verify-synthetic-vs-trusted-divergence.json": {
        "surface": "/tk:browser-verify",
        "focus": "synthetic-vs-trusted-click-divergence",
        "source_contracts": {
            "commands/browser-verify.md",
            "skills/browser-verify/SKILL.md",
            "skills/browser-verify/references/drivers/cdp-direct.md",
            ".tigerkit/docs/output-contract.md",
        },
        "safety_principles_covered": {
            "synthetic_click_can_create_phantom_submit_write",
            "trusted_click_is_control_for_click_activation_submit_verification",
            "dom_only_success_is_not_ground_truth_for_write_flows",
        },
        "required_scenarios": {
            "synthetic-element-click-phantom-write": {"interaction_mode": "synthetic", "write_observed": True},
            "trusted-click-no-write-control": {"interaction_mode": "trusted", "write_observed": False},
            "dom-success-signal-needs-ground-truth": {"interaction_mode": "synthetic", "write_observed": True},
        },
    },
}


def fail(message: str) -> NoReturn:
    raise SystemExit(f"full eval pilot check failed: {message}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        loaded = json.loads(path.read_text())
        if not isinstance(loaded, dict):
            fail(f"top-level json object required in {path.relative_to(ROOT)}")
        return cast(dict[str, Any], loaded)
    except FileNotFoundError:
        fail(f"missing required pilot file: {path.relative_to(ROOT)}")
    except Exception as exc:
        fail(f"invalid json in {path.relative_to(ROOT)}: {exc}")


def require_nonempty_string(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"{field} must be a non-empty string")
    return value


def require_string_list(value: object, field: str) -> list[str]:
    if not isinstance(value, list) or not value or not all(isinstance(item, str) and item.strip() for item in value):
        fail(f"{field} must be a non-empty list of strings")
    return [cast(str, item) for item in value]


def validate_common_fields(pilot: dict[str, Any], *, path_label: str, surface: str, focus: str, source_contracts: set[str]) -> None:
    if pilot.get("schemaVersion") != "tigerkit.full-eval-pilot/v1":
        fail(f"{path_label}: schemaVersion must be 'tigerkit.full-eval-pilot/v1'")
    if pilot.get("kind") != "full-real-agent-pilot":
        fail(f"{path_label}: kind must be 'full-real-agent-pilot'")
    if pilot.get("surface") != surface:
        fail(f"{path_label}: surface must be {surface!r}")
    if pilot.get("focus") != focus:
        fail(f"{path_label}: focus must be {focus!r}")
    if pilot.get("requires_real_agent") is not True:
        fail(f"{path_label}: requires_real_agent must be true")

    require_nonempty_string(pilot.get("pilot_id"), f"{path_label}.pilot_id")
    require_nonempty_string(pilot.get("goal"), f"{path_label}.goal")
    require_nonempty_string(pilot.get("operator_notes"), f"{path_label}.operator_notes")

    actual_source_contracts = set(
        require_string_list(pilot.get("source_contracts"), f"{path_label}.source_contracts")
    )
    if actual_source_contracts != source_contracts:
        fail(
            f"{path_label}: source_contracts must be exactly {sorted(source_contracts)!r}, "
            f"got {sorted(actual_source_contracts)!r}"
        )


def require_scenarios(pilot: dict[str, Any], *, path_label: str) -> dict[str, dict[str, Any]]:
    raw_scenarios = pilot.get("scenarios")
    if not isinstance(raw_scenarios, list) or not raw_scenarios:
        fail(f"{path_label}: scenarios must be a non-empty list")

    seen_ids: set[str] = set()
    scenario_map: dict[str, dict[str, Any]] = {}
    for index, scenario in enumerate(cast(list[Any], raw_scenarios), start=1):
        if not isinstance(scenario, dict):
            fail(f"{path_label}: scenario #{index} must be an object")
        scenario_id = require_nonempty_string(scenario.get("id"), f"{path_label}.scenarios[{index}].id")
        if scenario_id in seen_ids:
            fail(f"{path_label}: duplicate scenario id {scenario_id!r}")
        seen_ids.add(scenario_id)
        require_nonempty_string(scenario.get("title"), f"{path_label}.scenarios[{index}].title")
        require_nonempty_string(scenario.get("why"), f"{path_label}.scenarios[{index}].why")
        require_string_list(scenario.get("setup"), f"{path_label}.scenarios[{index}].setup")
        require_nonempty_string(scenario.get("task_prompt"), f"{path_label}.scenarios[{index}].task_prompt")

        expected = scenario.get("expected")
        if not isinstance(expected, dict):
            fail(f"{path_label}.scenarios[{index}].expected must be an object")
        must_observe = require_string_list(
            expected.get("must_observe"),
            f"{path_label}.scenarios[{index}].expected.must_observe",
        )
        if not must_observe:
            fail(f"{path_label}.scenarios[{index}].expected.must_observe must not be empty")
        scenario_map[scenario_id] = cast(dict[str, Any], scenario)

    return scenario_map


def validate_reflect_pilot(path: Path, pilot: dict[str, Any], spec: dict[str, Any]) -> None:
    path_label = str(path.relative_to(ROOT))
    validate_common_fields(
        pilot,
        path_label=path_label,
        surface=cast(str, spec["surface"]),
        focus=cast(str, spec["focus"]),
        source_contracts=cast(set[str], spec["source_contracts"]),
    )

    actual_reason_codes = set(
        require_string_list(pilot.get("reason_codes_covered"), f"{path_label}.reason_codes_covered")
    )
    required_reason_codes = cast(set[str], spec["reason_codes_covered"])
    if not required_reason_codes.issubset(actual_reason_codes):
        fail(
            f"{path_label}: reason_codes_covered must include {sorted(required_reason_codes)!r}, "
            f"got {sorted(actual_reason_codes)!r}"
        )

    scenario_map = require_scenarios(pilot, path_label=path_label)
    required_scenarios = cast(dict[str, dict[str, Any]], spec["required_scenarios"])
    missing_ids = required_scenarios.keys() - scenario_map.keys()
    if missing_ids:
        fail(f"{path_label}: missing required scenarios {sorted(missing_ids)!r}")

    for scenario_id, invariants in required_scenarios.items():
        expected = cast(dict[str, Any], scenario_map[scenario_id]["expected"])
        writes_allowed = expected.get("writes_allowed")
        if not isinstance(writes_allowed, bool):
            fail(f"{path_label}: scenario {scenario_id} writes_allowed must be a boolean")
        if writes_allowed is not invariants["writes_allowed"]:
            fail(
                f"{path_label}: scenario {scenario_id} writes_allowed must be {invariants['writes_allowed']!r}, got {writes_allowed!r}"
            )
        reason_code = expected.get("reason_code")
        if reason_code is not None and not isinstance(reason_code, str):
            fail(f"{path_label}: scenario {scenario_id} reason_code must be string or null")
        if reason_code != invariants["reason_code"]:
            fail(
                f"{path_label}: scenario {scenario_id} reason_code must be {invariants['reason_code']!r}, got {reason_code!r}"
            )
        must_observe = cast(list[str], expected["must_observe"])
        if not any(
            "reason_code" in item or "Changed paths" in item or "Applied candidates" in item
            for item in must_observe
        ):
            fail(
                f"{path_label}: scenario {scenario_id} must_observe must mention receipt evidence like reason_code/Changed paths/Applied candidates"
            )


def validate_gap_pilot(path: Path, pilot: dict[str, Any], spec: dict[str, Any]) -> None:
    path_label = str(path.relative_to(ROOT))
    validate_common_fields(
        pilot,
        path_label=path_label,
        surface=cast(str, spec["surface"]),
        focus=cast(str, spec["focus"]),
        source_contracts=cast(set[str], spec["source_contracts"]),
    )

    actual_classifications = set(
        require_string_list(pilot.get("classifications_covered"), f"{path_label}.classifications_covered")
    )
    required_classifications = cast(set[str], spec["classifications_covered"])
    if not required_classifications.issubset(actual_classifications):
        fail(
            f"{path_label}: classifications_covered must include {sorted(required_classifications)!r}, "
            f"got {sorted(actual_classifications)!r}"
        )

    actual_principles = set(
        require_string_list(
            pilot.get("evidence_principles_covered"),
            f"{path_label}.evidence_principles_covered",
        )
    )
    required_principles = cast(set[str], spec["evidence_principles_covered"])
    if not required_principles.issubset(actual_principles):
        fail(
            f"{path_label}: evidence_principles_covered must include {sorted(required_principles)!r}, "
            f"got {sorted(actual_principles)!r}"
        )

    scenario_map = require_scenarios(pilot, path_label=path_label)
    required_scenarios = cast(dict[str, dict[str, Any]], spec["required_scenarios"])
    missing_ids = required_scenarios.keys() - scenario_map.keys()
    if missing_ids:
        fail(f"{path_label}: missing required scenarios {sorted(missing_ids)!r}")

    for scenario_id, invariants in required_scenarios.items():
        expected = cast(dict[str, Any], scenario_map[scenario_id]["expected"])
        primary_gap = expected.get("primary_gap")
        if not isinstance(primary_gap, str):
            fail(f"{path_label}: scenario {scenario_id} primary_gap must be a string")
        if primary_gap != invariants["primary_gap"]:
            fail(
                f"{path_label}: scenario {scenario_id} primary_gap must be {invariants['primary_gap']!r}, got {primary_gap!r}"
            )
        must_observe = cast(list[str], expected["must_observe"])
        if not any(
            "Evidence type" in item or "ambiguous" in item or "implementation proof" in item
            for item in must_observe
        ):
            fail(
                f"{path_label}: scenario {scenario_id} must_observe must mention evidence-type/ambiguous/proof behavior"
            )


def validate_ui_diff_pilot(path: Path, pilot: dict[str, Any], spec: dict[str, Any]) -> None:
    path_label = str(path.relative_to(ROOT))
    validate_common_fields(
        pilot,
        path_label=path_label,
        surface=cast(str, spec["surface"]),
        focus=cast(str, spec["focus"]),
        source_contracts=cast(set[str], spec["source_contracts"]),
    )

    actual_principles = set(
        require_string_list(
            pilot.get("safety_principles_covered"),
            f"{path_label}.safety_principles_covered",
        )
    )
    required_principles = cast(set[str], spec["safety_principles_covered"])
    if not required_principles.issubset(actual_principles):
        fail(
            f"{path_label}: safety_principles_covered must include {sorted(required_principles)!r}, "
            f"got {sorted(actual_principles)!r}"
        )

    scenario_map = require_scenarios(pilot, path_label=path_label)
    required_scenarios = cast(dict[str, dict[str, Any]], spec["required_scenarios"])
    missing_ids = required_scenarios.keys() - scenario_map.keys()
    if missing_ids:
        fail(f"{path_label}: missing required scenarios {sorted(missing_ids)!r}")

    required_fragments: dict[str, tuple[str, ...]] = {
        "synthetic-element-click-phantom-write": ("button", "element.click()", "write"),
        "trusted-click-no-write-control": ("Input.dispatchMouseEvent", "UI toggle", "no write request"),
        "dom-success-signal-needs-ground-truth": ("DOM success", "network or backend", "ground-truth"),
    }

    for scenario_id, invariants in required_scenarios.items():
        expected = cast(dict[str, Any], scenario_map[scenario_id]["expected"])
        interaction_mode = expected.get("interaction_mode")
        if not isinstance(interaction_mode, str):
            fail(f"{path_label}: scenario {scenario_id} interaction_mode must be a string")
        if interaction_mode != invariants["interaction_mode"]:
            fail(
                f"{path_label}: scenario {scenario_id} interaction_mode must be {invariants['interaction_mode']!r}, got {interaction_mode!r}"
            )

        write_observed = expected.get("write_observed")
        if not isinstance(write_observed, bool):
            fail(f"{path_label}: scenario {scenario_id} write_observed must be a boolean")
        if write_observed is not invariants["write_observed"]:
            fail(
                f"{path_label}: scenario {scenario_id} write_observed must be {invariants['write_observed']!r}, got {write_observed!r}"
            )

        must_observe = cast(list[str], expected["must_observe"])
        joined = " ".join(must_observe)
        for fragment in required_fragments[scenario_id]:
            if fragment not in joined:
                fail(
                    f"{path_label}: scenario {scenario_id} must_observe must mention fragment {fragment!r}"
                )


def full_json_digest(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def full_hash(value: object, field: str) -> str:
    if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
        fail(f"{field} must be a lowercase SHA-256")
    return value


def full_safe_relative(value: object, field: str) -> str:
    relative = require_nonempty_string(value, field)
    if "\x00" in relative or "\\" in relative:
        fail(f"{field} must be a normalized POSIX path relative to the checkout")
    candidate = PurePosixPath(relative)
    if (
        candidate.is_absolute()
        or not candidate.parts
        or any(part in {"", ".", ".."} for part in candidate.parts)
        or candidate.as_posix() != relative
    ):
        fail(f"{field} must be a normalized POSIX path relative to the checkout")
    return relative


def full_repo_file(value: object, field: str) -> tuple[str, Path]:
    relative = full_safe_relative(value, field)
    candidate = ROOT.joinpath(*PurePosixPath(relative).parts)
    current = ROOT
    try:
        for part in PurePosixPath(relative).parts:
            current /= part
            if current.is_symlink():
                fail(f"{field} must not traverse a symlink")
        mode = candidate.lstat().st_mode
    except FileNotFoundError:
        fail(f"{field} must point to an existing regular file")
    except OSError as exc:
        fail(f"{field} cannot be inspected: {exc}")
    if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
        fail(f"{field} must point to an existing regular file")
    return relative, candidate


def full_require_real_directory(path: Path, label: str) -> None:
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        fail(f"missing required directory: {label}")
    except OSError as exc:
        fail(f"cannot inspect {label}: {exc}")
    if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
        fail(f"{label} must be a real directory")


def full_inventory(path: Path, label: str) -> list[Path]:
    full_require_real_directory(path, label)
    try:
        entries = list(path.iterdir())
    except OSError as exc:
        fail(f"cannot inspect {label}: {exc}")
    for entry in entries:
        try:
            mode = entry.lstat().st_mode
        except OSError as exc:
            fail(f"cannot inspect {label} entry {entry.name!r}: {exc}")
        if stat.S_ISLNK(mode):
            fail(f"{label} must not contain symlinks: {entry.name!r}")
        if not (stat.S_ISREG(mode) or stat.S_ISDIR(mode)):
            fail(f"{label} contains an unsupported special entry: {entry.name!r}")
    return entries


def full_reject_host_paths(value: object, label: str) -> None:
    if isinstance(value, str):
        if any(marker in value for marker in ("/home/", "/Users/", "/tmp/", "/root/")):
            fail(f"{label} must not disclose host-specific absolute paths")
        if any(marker in value for marker in ("system_prompt", "memory", "auth/settings", "MCP logs")):
            fail(f"{label} contains forbidden unrelated session material")
    elif isinstance(value, dict):
        for key, item in value.items():
            full_reject_host_paths(item, f"{label}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            full_reject_host_paths(item, f"{label}[{index}]")


def full_git_blob(commit: str, relative: str, field: str) -> bytes:
    full_safe_relative(relative, field)
    try:
        tree = subprocess.run(
            ["git", "ls-tree", "-z", commit, "--", relative],
            cwd=ROOT,
            capture_output=True,
            check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        fail(f"{field}: cannot inspect immutable Git tree for {commit}: {exc}")
    matches: list[tuple[str, str]] = []
    for entry in (item for item in tree.split(b"\0") if item):
        try:
            metadata, path_bytes = entry.split(b"\t", 1)
            mode, object_type, _object_id = metadata.split()
            path = path_bytes.decode("utf-8")
        except (UnicodeError, ValueError) as exc:
            fail(f"{field}: malformed Git tree entry: {exc}")
        if path == relative:
            matches.append((mode.decode("ascii"), object_type.decode("ascii")))
    if len(matches) != 1:
        fail(f"{field}: {relative!r} must resolve to exactly one Git tree entry")
    mode, object_type = matches[0]
    if object_type != "blob" or mode == "120000":
        fail(f"{field}: {relative!r} must be a non-symlink Git blob")
    try:
        return subprocess.run(
            ["git", "show", f"{commit}:{relative}"],
            cwd=ROOT,
            capture_output=True,
            check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        fail(f"{field}: cannot read immutable Git blob: {exc}")


def full_canonical_prompt(scenario_id: str, invocation_cwd: str) -> str:
    return (
        f"Pilot=reflect-repo-local-safety; Scenario={scenario_id}; Fixture CWD={invocation_cwd}; Plugin checkout=plugin-root. "
        "Invoke the public surface exactly once: /tk:reflect --target repo-local --apply=true --desc "
        f'"Issue 2 pilot {scenario_id}: create exactly one confirmed repo-local candidate from this single guidance: '
        f"Keep the fixture's local test guidance concise and evidence-backed for {scenario_id}. "
        'Forbid repo-shared, user-global, skill, hook, command, agent, and discard candidates.". '
        "Seed exactly one repo-local candidate from the single guidance in --desc. Do not create or propose repo-shared, user-global, skill, hook, command, agent, or discard candidates. "
        "Do not hand-edit CLAUDE.local.md, any ignore file, the plugin checkout, or any fallback path. Do not commit, reset, clean, or use another slash command. "
        "Return the canonical compact receipt with reason_code, Applied candidates, Changed paths, ledger path, and rollback state."
    )


def full_require_inventory_map(value: object, field: str) -> dict[str, dict[str, Any]]:
    if not isinstance(value, list):
        fail(f"{field} must be a list")
    result: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(cast(list[Any], value)):
        if not isinstance(item, dict):
            fail(f"{field}[{index}] must be an object")
        path = require_nonempty_string(item.get("path"), f"{field}[{index}].path")
        if path in result:
            fail(f"{field} contains duplicate path {path!r}")
        result[path] = cast(dict[str, Any], item)
    return result


def full_validate_lstat_snapshot(value: object, field: str, expected_path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{field} must be an object")
    snapshot = cast(dict[str, Any], value)
    if snapshot.get("path") != expected_path:
        fail(f"{field}.path must be {expected_path!r}")
    exists = snapshot.get("exists")
    kind = snapshot.get("kind")
    if exists is False:
        if kind != "absent":
            fail(f"{field} absent state must use kind 'absent'")
        return snapshot
    if exists is not True:
        fail(f"{field}.exists must be a boolean")
    if kind not in {"regular", "symlink", "directory", "special"}:
        fail(f"{field}.kind must describe an lstat entry")
    mode = snapshot.get("mode")
    if not isinstance(mode, str) or not mode.startswith("0o"):
        fail(f"{field}.mode must preserve the lstat mode")
    size = snapshot.get("size")
    if not isinstance(size, int) or size < 0:
        fail(f"{field}.size must be a non-negative integer")
    if kind == "regular":
        full_hash(snapshot.get("sha256"), f"{field}.sha256")
    elif kind == "symlink":
        require_nonempty_string(snapshot.get("link_text"), f"{field}.link_text")
    return snapshot


def full_validate_ignore_files(
    value: object,
    label: str,
    before_inventory: dict[str, dict[str, Any]],
    after_inventory: dict[str, dict[str, Any]],
) -> None:
    if not isinstance(value, list):
        fail(f"{label}.fixture.ignore_files must be a list")
    ignore_files = cast(list[Any], value)
    expected_paths = ["git-root/.gitignore", "git-root/.git/info/exclude"]
    actual_paths: list[str] = []
    for index, item in enumerate(ignore_files):
        if not isinstance(item, dict):
            fail(f"{label}.fixture.ignore_files[{index}] must be an object")
        path = require_nonempty_string(item.get("path"), f"{label}.fixture.ignore_files[{index}].path")
        actual_paths.append(path)
        before = full_validate_lstat_snapshot(
            item.get("before"),
            f"{label}.fixture.ignore_files[{index}].before",
            path,
        )
        after = full_validate_lstat_snapshot(
            item.get("after"),
            f"{label}.fixture.ignore_files[{index}].after",
            path,
        )
        if before != after:
            fail(f"{label}: ignore file {path!r} changed between explicit before/after snapshots")
        if path in before_inventory and before_inventory[path] != before:
            fail(f"{label}: ignore file {path!r} before snapshot disagrees with fixture inventory")
        if path in after_inventory and after_inventory[path] != after:
            fail(f"{label}: ignore file {path!r} after snapshot disagrees with fixture inventory")
    if actual_paths != expected_paths:
        fail(
            f"{label}.fixture.ignore_files must contain exactly the ordered snapshots for "
            f"{expected_paths!r}"
        )


def full_validate_state_root(source: dict[str, Any], label: str) -> None:
    state_root = source.get("state_root")
    if not isinstance(state_root, dict):
        fail(f"{label}.state_root must be an object")

    requested = state_root.get("requested")
    if requested != "state-root":
        fail(f"{label}.state_root.requested must be 'state-root'")
    honored = state_root.get("honored")
    if not isinstance(honored, bool):
        fail(f"{label}.state_root.honored must be a boolean")

    observed_value = state_root.get("observed_root")
    if observed_value is None:
        if honored is not True:
            fail(f"{label}.state_root.observed_root is required when the requested root was not honored")
        # Older honored records use the requested logical root as their observed root.
        observed_root = requested
    else:
        observed_root = full_safe_relative(observed_value, f"{label}.state_root.observed_root")

    if honored and observed_root != requested:
        fail(f"{label}.state_root.honored cannot be true when observed_root differs from requested")
    if not honored and observed_root == requested:
        fail(f"{label}.state_root.honored false must record an observed_root different from requested")

    inventory_before = full_require_inventory_map(
        state_root.get("inventory_before"), f"{label}.state_root.inventory_before"
    )
    if inventory_before:
        fail(f"{label}.state_root.inventory_before must be empty")
    inventory_after = full_require_inventory_map(
        state_root.get("inventory_after"), f"{label}.state_root.inventory_after"
    )
    if not inventory_after:
        fail(f"{label}.state_root.inventory_after must not be empty")

    root_prefix = f"{observed_root}/"
    for inventory_name, inventory in (
        ("inventory_before", inventory_before),
        ("inventory_after", inventory_after),
    ):
        for path in inventory:
            full_safe_relative(path, f"{label}.state_root.{inventory_name}.{path}")
            if not path.startswith(root_prefix):
                fail(
                    f"{label}.state_root.{inventory_name} path {path!r} must be under observed_root {observed_root!r}"
                )


def full_validate_fixture(source: dict[str, Any], scenario_id: str, label: str) -> None:
    fixture = source.get("fixture")
    if not isinstance(fixture, dict):
        fail(f"{label}.fixture must be an object")
    target = fixture.get("target")
    if not isinstance(target, dict):
        fail(f"{label}.fixture.target must be an object")
    before = target.get("before")
    after = target.get("after")
    if not isinstance(before, dict) or not isinstance(after, dict):
        fail(f"{label}.fixture.target before/after must be objects")
    expected_target_path = FULL_TARGET_PATHS[scenario_id]
    if before.get("path") != expected_target_path or after.get("path") != expected_target_path:
        fail(f"{label}.fixture.target path must be {expected_target_path!r}")

    git_before = fixture.get("git_before")
    git_after = fixture.get("git_after")
    if not isinstance(git_before, dict) or not isinstance(git_after, dict):
        fail(f"{label}.fixture.git_before/after must be objects")
    if git_before != git_after:
        fail(f"{label}.fixture Git state changed during the scenario")
    expected_worktree = scenario_id != "non-git-repo-local-reject"
    if git_before.get("is_worktree") is not expected_worktree:
        fail(f"{label}.fixture Git worktree state is inconsistent with the scenario")

    fallback_writes = fixture.get("fallback_writes")
    if fallback_writes != []:
        fail(f"{label}.fixture.fallback_writes must be empty")

    before_inventory = full_require_inventory_map(
        fixture.get("fixture_inventory_before"), f"{label}.fixture.fixture_inventory_before"
    )
    after_inventory = full_require_inventory_map(
        fixture.get("fixture_inventory_after"), f"{label}.fixture.fixture_inventory_after"
    )
    if scenario_id == "eligible-repo-local-apply":
        if before.get("exists") is not False or before.get("kind") != "absent":
            fail(f"{label}: eligible target must be absent before the run")
        if after.get("exists") is not True or after.get("kind") != "regular":
            fail(f"{label}: eligible target must be a regular file after the run")
        if expected_target_path in before_inventory:
            fail(f"{label}: eligible target was already present before the run")
        expected_after = dict(before_inventory)
        expected_after[expected_target_path] = after
        if after_inventory != expected_after:
            fail(f"{label}: eligible changed paths must be exactly the target")
    else:
        if before != after:
            fail(f"{label}: rejected target state changed")
        if before_inventory != after_inventory:
            fail(f"{label}: rejected fixture inventory changed")

    ignore_files = fixture.get("ignore_files")
    if scenario_id == "not-ignored-claude-local-reject":
        full_validate_ignore_files(ignore_files, label, before_inventory, after_inventory)
    else:
        if not isinstance(ignore_files, list):
            fail(f"{label}.fixture.ignore_files must be a list")
        ignore_paths = {
            item.get("path")
            for item in cast(list[Any], ignore_files)
            if isinstance(item, dict)
        }
        for path in ignore_paths:
            if not isinstance(path, str):
                fail(f"{label}.fixture.ignore_files contains an invalid path")
            if path in before_inventory and after_inventory.get(path) != before_inventory[path]:
                fail(f"{label}: ignore file {path!r} changed")

    external = fixture.get("external_target")
    if scenario_id == "symlink-claude-local-reject":
        if not isinstance(external, dict):
            fail(f"{label}: symlink scenario must record an external target")
        external_path = require_nonempty_string(external.get("path"), f"{label}.fixture.external_target.path")
        if before.get("kind") != "symlink" or after.get("kind") != "symlink":
            fail(f"{label}: symlink scenario target must remain a symlink")
        if before.get("link_text") != after.get("link_text"):
            fail(f"{label}: symlink link text changed")
        if before_inventory.get(external_path) != after_inventory.get(external_path):
            fail(f"{label}: symlink external target changed")
    elif external is not None:
        fail(f"{label}: non-symlink scenario must not record an external target")

    full_validate_state_root(source, label)


def full_validate_source(
    path: Path,
    record: dict[str, Any],
    scenario_id: str,
) -> dict[str, Any]:
    label = str(path.relative_to(ROOT))
    source = load_json(path)
    if source.get("schemaVersion") != FULL_SOURCE_SCHEMA:
        fail(f"{label}.schemaVersion must be {FULL_SOURCE_SCHEMA!r}")
    if source.get("scenario_id") != scenario_id:
        fail(f"{label}.scenario_id must match the result scenario")
    full_reject_host_paths(source, label)

    session = source.get("session")
    if not isinstance(session, dict):
        fail(f"{label}.session must be an object")
    if session.get("session_id") != FULL_SESSION_IDS[scenario_id] or session.get("session_id") != record.get("session_id"):
        fail(f"{label}.session.session_id must match the exact isolated session")
    for field, expected in {
        "fresh": True,
        "isolated": True,
        "write_free": False,
        "consumer": FULL_CONSUMER,
        "consumer_version": FULL_CONSUMER_VERSION,
        "wrapper": FULL_WRAPPER,
        "provider": FULL_PROVIDER,
        "model": FULL_MODEL,
    }.items():
        if session.get(field) != expected:
            fail(f"{label}.session.{field} must be {expected!r}")

    plugin = source.get("plugin")
    if not isinstance(plugin, dict):
        fail(f"{label}.plugin must be an object")
    if plugin.get("path") != "plugin-root" or plugin.get("repo_id") != "tiger-kit" or plugin.get("commit") != FULL_PLUGIN_COMMIT:
        fail(f"{label}.plugin must identify the recorded plugin checkout and commit")
    blob_items = plugin.get("contract_blobs")
    if not isinstance(blob_items, list):
        fail(f"{label}.plugin.contract_blobs must be a list")
    blobs: dict[str, str] = {}
    for index, item in enumerate(cast(list[Any], blob_items)):
        if not isinstance(item, dict):
            fail(f"{label}.plugin.contract_blobs[{index}] must be an object")
        relative = full_safe_relative(item.get("path"), f"{label}.plugin.contract_blobs[{index}].path")
        if relative in blobs:
            fail(f"{label}.plugin.contract_blobs contains duplicate path {relative!r}")
        blobs[relative] = full_hash(item.get("sha256"), f"{label}.plugin.contract_blobs[{index}].sha256")
    if blobs != FULL_CONTRACT_BLOBS:
        fail(f"{label}.plugin.contract_blobs must match the approved contract set")
    for relative, expected_sha in FULL_CONTRACT_BLOBS.items():
        immutable = full_git_blob(FULL_PLUGIN_COMMIT, relative, f"{label}.plugin.contract_blobs.{relative}")
        if hashlib.sha256(immutable).hexdigest() != expected_sha:
            fail(f"{label}.plugin contract blob changed at the recorded commit: {relative}")
        _, live = full_repo_file(relative, f"{label}.plugin.live.{relative}")
        if hashlib.sha256(live.read_bytes()).hexdigest() != expected_sha:
            fail(f"{label}.plugin live blob differs from the recorded commit: {relative}")

    command = source.get("command")
    if not isinstance(command, dict):
        fail(f"{label}.command must be an object")
    invocation_cwd = command.get("invocation_cwd")
    if invocation_cwd != ("fixture-root/workdir" if scenario_id == "non-git-repo-local-reject" else "git-root"):
        fail(f"{label}.command.invocation_cwd is not the recorded logical fixture cwd")
    prompt = full_canonical_prompt(scenario_id, cast(str, invocation_cwd))
    argv = command.get("argv")
    expected_argv = [
        "ccs", "codex", "-p", prompt, "--plugin-dir", "plugin-root",
        "--permission-mode", "bypassPermissions", "--allowedTools", ",".join(FULL_ALLOWED_TOOLS),
        "--max-turns", "16", "--no-session-persistence", "--output-format", "json",
    ]
    if argv != expected_argv:
        fail(f"{label}.command.argv must preserve the exact isolated plugin invocation")
    if hashlib.sha256(prompt.encode("utf-8")).hexdigest() != FULL_PROMPT_HASHES[scenario_id]:
        fail(f"{label}.command prompt does not match the approved scenario request")
    if full_json_digest(argv) != command.get("argv_sha256") or command.get("argv_sha256") != FULL_ARGV_HASHES[scenario_id]:
        fail(f"{label}.command.argv_sha256 does not match the exact invocation")
    for field, expected in {
        "plugin_dir": "plugin-root",
        "permission_mode": "bypassPermissions",
        "allowed_tools": FULL_ALLOWED_TOOLS,
        "max_turns": 16,
        "session_persistence": False,
    }.items():
        if command.get(field) != expected:
            fail(f"{label}.command.{field} must be {expected!r}")

    tool_evidence = source.get("tool_evidence")
    if not isinstance(tool_evidence, dict):
        fail(f"{label}.tool_evidence must be an object")
    plugin_command = tool_evidence.get("plugin_command")
    if not isinstance(plugin_command, dict):
        fail(f"{label}.tool_evidence.plugin_command must be an object")
    if plugin_command != {
        "executable": "ccs",
        "subcommand": "codex",
        "public_surface": "/tk:reflect",
        "argv": argv,
        "invocation_cwd": invocation_cwd,
        "plugin_dir": "plugin-root",
    }:
        fail(f"{label}.tool_evidence.plugin_command must identify the exact public invocation")
    transcript = tool_evidence.get("session_transcript")
    if not isinstance(transcript, dict):
        fail(f"{label}.tool_evidence.session_transcript must be an object")
    if transcript.get("session_id") != FULL_SESSION_IDS[scenario_id] or transcript.get("event_type") != "ai-title":
        fail(f"{label}.tool_evidence.session_transcript must identify the minimized source event")
    require_nonempty_string(transcript.get("ai_title"), f"{label}.tool_evidence.session_transcript.ai_title")
    full_hash(transcript.get("sha256"), f"{label}.tool_evidence.session_transcript.sha256")
    if not isinstance(transcript.get("byte_length"), int) or transcript["byte_length"] < 1:
        fail(f"{label}.tool_evidence.session_transcript.byte_length must be positive")

    runtime = source.get("runtime")
    if not isinstance(runtime, dict):
        fail(f"{label}.runtime must be an object")
    model_usage = runtime.get("model_usage")
    if not isinstance(model_usage, dict) or not model_usage:
        fail(f"{label}.runtime.model_usage must be a non-empty object")
    usage_keys = runtime.get("model_usage_keys")
    if usage_keys != list(model_usage.keys()) or usage_keys != ["gpt-5.4-mini(low)", "gpt-5.5(high)"]:
        fail(f"{label}.runtime.model_usage_keys must preserve actual routing keys")
    if full_json_digest(model_usage) != FULL_MODEL_USAGE_HASHES[scenario_id]:
        fail(f"{label}.runtime.model_usage does not match the actual recorded model usage")
    observed = runtime.get("observed_result")
    expected_observed = {
        "type": "result",
        "subtype": "success",
        "is_error": False,
        "stop_reason": "end_turn",
        "terminal_reason": "completed",
        "num_turns": FULL_TURNS[scenario_id],
        "permission_denials": [],
    }
    if observed != expected_observed:
        fail(f"{label}.runtime.observed_result must preserve the actual successful result metadata")

    consumer_output = source.get("consumer_output")
    if not isinstance(consumer_output, dict):
        fail(f"{label}.consumer_output must be an object")
    assistant_result = require_nonempty_string(consumer_output.get("result"), f"{label}.consumer_output.result")
    result_sha, result_length = FULL_RESULT_HASHES[scenario_id]
    if consumer_output.get("result_sha256") != result_sha or hashlib.sha256(assistant_result.encode("utf-8")).hexdigest() != result_sha:
        fail(f"{label}.consumer_output.result_sha256 does not match the canonical assistant result")
    if consumer_output.get("result_byte_length") != result_length or len(assistant_result.encode("utf-8")) != result_length:
        fail(f"{label}.consumer_output.result_byte_length does not match the canonical assistant result")

    receipt = source.get("receipt")
    if not isinstance(receipt, dict):
        fail(f"{label}.receipt must be an object")
    if receipt.get("reason_code") != FULL_REASON_RAW[scenario_id]:
        fail(f"{label}.receipt.reason_code does not match the exact recorded receipt")
    if receipt.get("applied_candidates") != FULL_APPLIED[scenario_id]:
        fail(f"{label}.receipt.applied_candidates does not match the exact recorded receipt")
    if receipt.get("changed_paths") != FULL_CHANGED_PATHS[scenario_id]:
        fail(f"{label}.receipt.changed_paths does not match the exact recorded receipt")
    if receipt.get("stdout_excerpt") != assistant_result:
        fail(f"{label}.receipt.stdout_excerpt must equal the canonical assistant result")
    if receipt.get("consumer_output_sha256") != consumer_output.get("recorded_consumer_output_sha256"):
        fail(f"{label}.receipt consumer output hash must match the recorded source metadata")

    full_validate_fixture(source, scenario_id, label)
    return source


def full_validate_inventory() -> None:
    if not FULL_RESULT_PATH.exists():
        fail(f"missing required result file: {FULL_RESULT_PATH.relative_to(ROOT)}")
    full_require_real_directory(RESULTS_DIR, str(RESULTS_DIR.relative_to(ROOT)))
    result_entries = full_inventory(RESULTS_DIR, str(RESULTS_DIR.relative_to(ROOT)))
    result_files = {entry.name for entry in result_entries if entry.is_file()}
    if result_files != {"micro-initial-command-wording.json", FULL_RESULT_PATH.name}:
        fail(f"{RESULTS_DIR.relative_to(ROOT)} contains unexpected result files: {sorted(result_files)!r}")
    result_dirs = {entry.name for entry in result_entries if entry.is_dir()}
    if result_dirs != {"raw"}:
        fail(f"{RESULTS_DIR.relative_to(ROOT)} contains unexpected directories: {sorted(result_dirs)!r}")
    raw_parent = RESULTS_DIR / "raw"
    raw_parent_entries = full_inventory(raw_parent, str(raw_parent.relative_to(ROOT)))
    raw_dirs = {entry.name for entry in raw_parent_entries if entry.is_dir()}
    if raw_dirs != {"micro-initial-command-wording", FULL_RAW_DIR.name}:
        fail(f"{raw_parent.relative_to(ROOT)} contains unexpected evidence directories: {sorted(raw_dirs)!r}")
    full_entries = full_inventory(FULL_RAW_DIR, str(FULL_RAW_DIR.relative_to(ROOT)))
    actual_files = {entry.name for entry in full_entries if entry.is_file()}
    expected_files = {f"{scenario_id}.json" for scenario_id in FULL_SCENARIO_IDS}
    if actual_files != expected_files:
        fail(
            f"{FULL_RAW_DIR.relative_to(ROOT)} inventory mismatch: "
            f"unexpected={sorted(actual_files - expected_files)!r}, missing={sorted(expected_files - actual_files)!r}"
        )
    if any(entry.is_dir() for entry in full_entries):
        fail(f"{FULL_RAW_DIR.relative_to(ROOT)} must contain only logical source files")


def full_validate_result() -> None:
    full_validate_inventory()
    result = load_json(FULL_RESULT_PATH)
    label = str(FULL_RESULT_PATH.relative_to(ROOT))
    if result.get("schemaVersion") != FULL_RESULT_SCHEMA:
        fail(f"{label}.schemaVersion must be {FULL_RESULT_SCHEMA!r}")
    if result.get("pilot_id") != "reflect-repo-local-safety":
        fail(f"{label}.pilot_id must match the approved FULL pilot")
    if result.get("kind") != "full-real-agent-results":
        fail(f"{label}.kind must be 'full-real-agent-results'")
    if result.get("status") != "full-validated" or result.get("status") == "shipped":
        fail(f"{label}.status must be 'full-validated' and never 'shipped'")
    if result.get("evidence_tier") != "full-real-agent":
        fail(f"{label}.evidence_tier must be 'full-real-agent'")
    if result.get("evidence_scope") != "internal consistency record; not independent authenticity":
        fail(f"{label}.evidence_scope must state the internal-consistency limitation")
    full_reject_host_paths(result, label)

    runtime = result.get("runtime")
    if not isinstance(runtime, dict):
        fail(f"{label}.runtime must be an object")
    for field, expected in {
        "wrapper": FULL_WRAPPER,
        "provider": FULL_PROVIDER,
        "consumer": FULL_CONSUMER,
        "consumer_version": FULL_CONSUMER_VERSION,
        "model": FULL_MODEL,
        "plugin_commit": FULL_PLUGIN_COMMIT,
    }.items():
        if runtime.get(field) != expected:
            fail(f"{label}.runtime.{field} must be {expected!r}")
    invocation = runtime.get("invocation")
    if invocation != {
        "executable": "ccs",
        "subcommand": "codex",
        "permission_mode": "bypassPermissions",
        "allowed_tools": FULL_ALLOWED_TOOLS,
        "max_turns": 16,
        "session_persistence": False,
        "output_format": "json",
        "paths": "per-scenario logical fixture/plugin tokens are recorded in each raw source",
    }:
        fail(f"{label}.runtime.invocation must preserve the actual wrapper command shape")

    records = result.get("scenarios")
    if not isinstance(records, list) or len(records) != len(FULL_SCENARIO_IDS) or not all(isinstance(item, dict) for item in records):
        fail(f"{label}.scenarios must contain exactly the five approved scenario records")
    records = cast(list[dict[str, Any]], records)
    actual_ids = [require_nonempty_string(item.get("id"), f"{label}.scenarios[{index}].id") for index, item in enumerate(records)]
    if actual_ids != list(FULL_SCENARIO_IDS):
        fail(f"{label}.scenarios must contain exactly the approved scenario IDs in order")

    seen_sessions: set[str] = set()
    referenced_sources: set[str] = set()
    for index, record in enumerate(records):
        scenario_id = actual_ids[index]
        prefix = f"{label}.scenarios[{index}]"
        expected_source = f"evals/results/raw/full-reflect-repo-local-safety/{scenario_id}.json"
        source_relative, source_path = full_repo_file(record.get("source_path"), f"{prefix}.source_path")
        if source_relative != expected_source:
            fail(f"{prefix}.source_path must be the canonical durable source for {scenario_id}")
        if source_relative in referenced_sources:
            fail(f"{prefix}.source_path must be unique")
        referenced_sources.add(source_relative)
        source_sha = full_hash(record.get("source_sha256"), f"{prefix}.source_sha256")
        actual_source_sha = hashlib.sha256(source_path.read_bytes()).hexdigest()
        if source_sha != actual_source_sha or source_sha != FULL_SOURCE_HASHES[scenario_id]:
            fail(f"{prefix}.source_sha256 does not match the canonical durable source")

        session_id = require_nonempty_string(record.get("session_id"), f"{prefix}.session_id")
        if session_id in seen_sessions:
            fail(f"{prefix}.session_id must be unique across all scenarios")
        seen_sessions.add(session_id)
        if session_id != FULL_SESSION_IDS[scenario_id]:
            fail(f"{prefix}.session_id must identify the exact isolated run")
        result_sha, result_length = FULL_RESULT_HASHES[scenario_id]
        if record.get("assistant_result_sha256") != result_sha or record.get("assistant_result_byte_length") != result_length:
            fail(f"{prefix} assistant result hash/length does not match the canonical result")
        if record.get("succeeded") is not True:
            fail(f"{prefix}.succeeded must be true for the actual successful result")
        if record.get("observed_result") != {
            "type": "result",
            "subtype": "success",
            "is_error": False,
            "stop_reason": "end_turn",
            "terminal_reason": "completed",
            "num_turns": FULL_TURNS[scenario_id],
            "permission_denials": [],
        }:
            fail(f"{prefix}.observed_result must preserve actual success metadata")
        if record.get("model") != FULL_MODEL:
            fail(f"{prefix}.model must be {FULL_MODEL!r}")
        if record.get("model_usage_keys") != ["gpt-5.4-mini(low)", "gpt-5.5(high)"]:
            fail(f"{prefix}.model_usage_keys must preserve actual routing keys")
        model_usage = record.get("modelUsage")
        if not isinstance(model_usage, dict) or full_json_digest(model_usage) != FULL_MODEL_USAGE_HASHES[scenario_id]:
            fail(f"{prefix}.modelUsage does not match the actual recorded routing usage")
        if record.get("reason_code") != FULL_REASON[scenario_id]:
            fail(f"{prefix}.reason_code must be {FULL_REASON[scenario_id]!r}")
        if record.get("applied_candidates") != FULL_APPLIED[scenario_id]:
            fail(f"{prefix}.applied_candidates does not match the canonical receipt")
        if record.get("changed_paths") != FULL_CHANGED_PATHS[scenario_id]:
            fail(f"{prefix}.changed_paths does not match the canonical receipt")

        source = full_validate_source(source_path, record, scenario_id)
        if record.get("modelUsage") != source["runtime"]["model_usage"]:
            fail(f"{prefix}.modelUsage must match the durable raw source")
        if record.get("model_usage_keys") != source["runtime"]["model_usage_keys"]:
            fail(f"{prefix}.model_usage_keys must match the durable raw source")
        if record.get("observed_result") != source["runtime"]["observed_result"]:
            fail(f"{prefix}.observed_result must match the durable raw source")
        if record.get("reason_code") != FULL_REASON[scenario_id]:
            fail(f"{prefix}.reason_code must match the normalized durable receipt")

    expected_sources = {
        f"evals/results/raw/full-reflect-repo-local-safety/{scenario_id}.json"
        for scenario_id in FULL_SCENARIO_IDS
    }
    if referenced_sources != expected_sources:
        fail(f"{label}.scenarios must reference exactly the approved durable raw files")


def main() -> int:
    try:
        for filename, spec in PILOT_SPECS.items():
            path = PILOTS_DIR / filename
            pilot = load_json(path)
            surface = spec["surface"]
            if surface == "/tk:reflect":
                validate_reflect_pilot(path, pilot, spec)
            elif surface == "/tk:gap":
                validate_gap_pilot(path, pilot, spec)
            elif surface == "/tk:browser-verify":
                validate_ui_diff_pilot(path, pilot, spec)
            else:
                fail(f"unsupported pilot surface in validator config: {surface!r}")
        full_validate_result()
    except SystemExit:
        raise
    except Exception as exc:
        fail(f"malformed evidence rejected without traceback: {type(exc).__name__}: {exc}")

    validated = ", ".join(sorted(str((PILOTS_DIR / name).relative_to(ROOT)) for name in PILOT_SPECS))
    print(
        f"full eval pilots ok: {validated}; "
        "reflect FULL result validated (internal consistency record; not independent authenticity)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
