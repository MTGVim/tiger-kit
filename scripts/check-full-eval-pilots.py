#!/usr/bin/env python3
"""Validate tracked FULL-style TigerKit eval pilot scaffolding."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, NoReturn, cast

ROOT = Path(__file__).resolve().parents[1]
PILOTS_DIR = ROOT / "evals" / "full-pilots"

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
    "ui-diff-synthetic-vs-trusted-divergence.json": {
        "surface": "/tk:ui-diff",
        "focus": "synthetic-vs-trusted-click-divergence",
        "source_contracts": {
            "commands/ui-diff.md",
            "skills/ui-diff/SKILL.md",
            "skills/ui-diff/references/drivers/cdp-direct.md",
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


def main() -> int:
    for filename, spec in PILOT_SPECS.items():
        path = PILOTS_DIR / filename
        pilot = load_json(path)
        surface = spec["surface"]
        if surface == "/tk:reflect":
            validate_reflect_pilot(path, pilot, spec)
        elif surface == "/tk:gap":
            validate_gap_pilot(path, pilot, spec)
        elif surface == "/tk:ui-diff":
            validate_ui_diff_pilot(path, pilot, spec)
        else:
            fail(f"unsupported pilot surface in validator config: {surface!r}")

    validated = ", ".join(sorted(str((PILOTS_DIR / name).relative_to(ROOT)) for name in PILOT_SPECS))
    print(f"full eval pilots ok: {validated}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
