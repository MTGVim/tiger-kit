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
GAP_RESULT_PATH = RESULTS_DIR / "full-gap-stale-sot-precedence.json"
GAP_RAW_DIR = RESULTS_DIR / "raw" / "full-gap-stale-sot-precedence"
FULL_RESULT_SCHEMA = "tigerkit.full-reflect-repo-local-safety-results/v1"
FULL_SOURCE_SCHEMA = "tigerkit.full-reflect-repo-local-safety-source/v1"
GAP_RESULT_SCHEMA = "tigerkit.full-gap-stale-sot-precedence-results/v1"
GAP_SOURCE_SCHEMA = "tigerkit.full-gap-stale-sot-precedence-source/v1"
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
FULL_FIXTURE_ROOTS_BY_SCENARIO = {
    "eligible-repo-local-apply": {"git-root"},
    "tracked-claude-local-reject": {"git-root"},
    "not-ignored-claude-local-reject": {"git-root"},
    "non-git-repo-local-reject": {"fixture-root"},
    "symlink-claude-local-reject": {"git-root", "external-target"},
}
FULL_TURNS = {
    "eligible-repo-local-apply": 4,
    "tracked-claude-local-reject": 4,
    "not-ignored-claude-local-reject": 4,
    "non-git-repo-local-reject": 8,
    "symlink-claude-local-reject": 5,
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
GIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
FULL_GIT_FIXTURE_ROOTS = {"git-root"}
FULL_EXTERNAL_TARGET_ROOTS = {"external-target"}
FULL_LSTAT_FIELDS = {"path", "exists", "kind", "mode", "size", "sha256", "link_text"}
FULL_GIT_SNAPSHOT_FIELDS = {"is_worktree", "rev_parse_status", "status_porcelain", "head", "branch"}
GAP_SCENARIO_IDS = (
    "stale-plan-vs-live-surface-conflict",
    "unresolved-source-precedence-stays-ambiguous",
    "plan-only-current-is-not-implementation-proof",
)
GAP_PLUGIN_COMMIT = "731c8ea9d8b47011d808020df6ccae6f54d1ca99"
GAP_WRAPPER = "ccs codex"
GAP_WRAPPER_VERSION = "CCS (Claude Code Switch) v8.6.1"
GAP_PROVIDER = "openai-codex"
GAP_CONSUMER = "Claude Code"
GAP_CONSUMER_VERSION = "2.1.150 (Claude Code)"
GAP_MODEL = "gpt-5.5(high)"
GAP_MODEL_SOURCE = "actual modelUsage high-tier routing key; consumer envelope model field was null"
GAP_ALLOWED_TOOLS = ["Read", "Grep", "Glob", "Bash"]
GAP_MODEL_USAGE_KEYS = ["gpt-5.4-mini(low)", "gpt-5.5(high)"]
GAP_CONTRACT_BLOBS = {
    "commands/gap.md": "2d985b65acb65b10a811b136d6c705e0dd6c99fba449cb897a4f414dabcedd1d",
    "skills/gap/SKILL.md": "1f40267d304b90f96c7cfcc2bf3e6902d48f17815ae76312b17eaa7ac44f3828",
    ".tigerkit/docs/output-contract.md": "eab16292a7f5aa3be02e125710bda0bedce1feaa77e364f4afdb1c6e98a59914",
}
GAP_CONTRACT_BLOB_LIST = [
    {"path": relative, "sha256": digest}
    for relative, digest in GAP_CONTRACT_BLOBS.items()
]
GAP_SOURCE_HASHES = {
    "stale-plan-vs-live-surface-conflict": "f4936e9105a8f71fc6e7a975b650154208aaceed8a9e246f4381dc8018021c9b",
    "unresolved-source-precedence-stays-ambiguous": "88d106139317e811f70120536dfb87e3a07e744e8f94893f40af88c0e36183f6",
    "plan-only-current-is-not-implementation-proof": "5aa23f83747e7ce3652b9d3b4bc65de50bf5619b55bbf84790e034732473d567",
}
GAP_RESULT_HASHES = {
    "stale-plan-vs-live-surface-conflict": ("3bce331b67445f45ca553e8b8865d044e12a49cf5eeb9a4359c873ca117d6539", 2939),
    "unresolved-source-precedence-stays-ambiguous": ("7d7a5f66593b86cc5dc386998616c452e948bc519a4f97473ce8bada3b990831", 2291),
    "plan-only-current-is-not-implementation-proof": ("61cee17bfdaf26ff56c5826a0cfc867c5dad971e10d40df985fbe4d92e28b82e", 2323),
}
GAP_PROMPT_HASHES = {
    "stale-plan-vs-live-surface-conflict": "a40be46dded56ec3463d62facd35c05b8aaa6f8a7e8b0bba23110198e16480fb",
    "unresolved-source-precedence-stays-ambiguous": "27ea7f8803b539af6e124011a8af992bca16704a6cff2c3d4cded7ad10501474",
    "plan-only-current-is-not-implementation-proof": "37054f44ca45921450dd1a14c098e315ce8489b9f16c61200ff63865b42ac852",
}
GAP_PROMPT_LENGTHS = {
    "stale-plan-vs-live-surface-conflict": 1189,
    "unresolved-source-precedence-stays-ambiguous": 1259,
    "plan-only-current-is-not-implementation-proof": 1549,
}
GAP_ARGV_HASHES = {
    "stale-plan-vs-live-surface-conflict": "ce00bf5c01904ad3c01b92b5ea33d0409494420daec7c677ab32e54c3b0fe874",
    "unresolved-source-precedence-stays-ambiguous": "352bb8c440a0e437e9824b47e8910df248b2ef26f3659cfa9328333ec410705f",
    "plan-only-current-is-not-implementation-proof": "b3cfee4d86136a641f110867f4dd48b4b2df95e0418ffd2a6ef671c436cb10fa",
}
GAP_MODEL_USAGE_HASHES = {
    "stale-plan-vs-live-surface-conflict": "a2b6fcce09744af17a186fdc49ce5c0ada070924714b511aafd90d1fcdda0667",
    "unresolved-source-precedence-stays-ambiguous": "91c7c92827bf1034774fbf9651bd7a2180dc60c3c6b0620ec4e3396d6d0ec856",
    "plan-only-current-is-not-implementation-proof": "325b6affc8ef1f39f80adac49f515e3f8dc0a2b7b3adce3f06e31727ad764e53",
}
GAP_SOURCE_MANIFEST_HASHES = {
    "stale-plan-vs-live-surface-conflict": "d2ddac14afe0af52d3fb77f85dabe10d966ce1b48c768922041b2a2cf76af0fd",
    "unresolved-source-precedence-stays-ambiguous": "d21c95f5106f7ba63883fd25e2ce0e39eb00760e8b79497e44402091bc03d2e7",
    "plan-only-current-is-not-implementation-proof": "547311efc19e33cb460a0e7cb943a1dc35185a071951414a2fffd5069097a94e",
}
GAP_SESSION_IDS = {
    "stale-plan-vs-live-surface-conflict": "4c5e0b90-ff30-4acf-9268-c4b0784896dd",
    "unresolved-source-precedence-stays-ambiguous": "fdaf2062-aa68-4ce1-9985-47a89aed4d46",
    "plan-only-current-is-not-implementation-proof": "6897964a-b2ed-4407-ade2-16b054d470d0",
}
GAP_TURNS = {
    "stale-plan-vs-live-surface-conflict": 9,
    "unresolved-source-precedence-stays-ambiguous": 10,
    "plan-only-current-is-not-implementation-proof": 6,
}
GAP_FIXTURE_HEADS = {
    "stale-plan-vs-live-surface-conflict": "33bc8c2cb1724342e66e8c192b8c25a36224f516",
    "unresolved-source-precedence-stays-ambiguous": "9a0ca8925aa3dfe9d8c09fc024ed096d632d3d0c",
    "plan-only-current-is-not-implementation-proof": "c3683f26e871efadefc5dbe960aa3f5e54705726",
}
GAP_FIXTURE_INVENTORY_HASHES = {
    "stale-plan-vs-live-surface-conflict": "8067e5fb77c51d97d49633d19ae96cb033507714a931cd3da4e11b5e37d9d841",
    "unresolved-source-precedence-stays-ambiguous": "e3ded81009a50a8f07658d5757b452a8f62a1e3eec5104d20a4514fcfacabff2",
    "plan-only-current-is-not-implementation-proof": "09aa9750e6e121724d08e8082295d05af0bc97a8f0c7f0dec04c68e825ad029f",
}
GAP_FINAL_CLASSIFICATIONS = {
    "stale-plan-vs-live-surface-conflict": "ambiguous",
    "unresolved-source-precedence-stays-ambiguous": "ambiguous",
    "plan-only-current-is-not-implementation-proof": "missing",
}
GAP_RECOMMENDATIONS = {
    "stale-plan-vs-live-surface-conflict": "1. Decide source precedence: either demote `S1` as stale historical planning evidence, or explicitly re-authorize it as active SoT before changing `/bundle --format json`.",
    "unresolved-source-precedence-stays-ambiguous": "1. S1/S2의 source precedence를 결정해 “S2가 S1의 launch-window scoped exception인지”를 명시한 뒤, 그 결정에 맞춰 Current implementation evidence를 다시 확인합니다.",
    "plan-only-current-is-not-implementation-proof": "1. Inspect or produce direct implementation/runtime evidence for `/alert-bundle --severity <level>` returning JSON with the requested severity.",
}
GAP_SOURCE_REFS = {
    "stale-plan-vs-live-surface-conflict": [
        {"ref_id": "S1", "role": "SoT", "type": "historical-plan", "path": "plans/bundle-rollout.md", "access_status": "readable", "sha256": "0fe98e176826832dc8b89e64c157b8ced3f56c3e21c97cc3c9f56efde505648f", "byte_length": 237},
        {"ref_id": "C1", "role": "Current", "type": "file-read", "path": "README.md", "access_status": "readable", "sha256": "86aa158768cee919c45a74959a41cce1eb9ee0cdfdfb9946011885bb694d873f", "byte_length": 159},
        {"ref_id": "C2", "role": "Current", "type": "file-read", "path": "commands/bundle.md", "access_status": "readable", "sha256": "6c6e73200aa0b94e7405c604cfa6604bd047d45d38182742b30127d680da3a2a", "byte_length": 144},
    ],
    "unresolved-source-precedence-stays-ambiguous": [
        {"ref_id": "S1", "role": "SoT", "type": "specification", "path": "specs/bundle-auth.md", "access_status": "readable", "sha256": "c8d9caf8809c190b89b950c05378a71b028a5db480b92c54cc07ca947ae461ec", "byte_length": 103},
        {"ref_id": "S2", "role": "SoT", "type": "specification", "path": "specs/bundle-launch.md", "access_status": "readable", "sha256": "a35e4a9e11bc7f9b9b1d3a60ee98036b0395945bc64436eedc0f053fc89d0143", "byte_length": 132},
        {"ref_id": "C1", "role": "Current", "type": "file-read", "path": "README.md", "access_status": "readable", "sha256": "8cef467ed3cd0cb602d1151e72775abd6705950bdb0f49eab1f894b2d1bbabc4", "byte_length": 93},
        {"ref_id": "C2", "role": "Current", "type": "file-read", "path": "commands/bundle.md", "access_status": "readable", "sha256": "aefc93c12daa3cf93f4522aaeddf032410693a7d9816eeec88dd489ac9cf218b", "byte_length": 83},
    ],
    "plan-only-current-is-not-implementation-proof": [
        {"ref_id": "S1", "role": "SoT", "type": "specification", "path": "specs/alert-bundle.md", "access_status": "readable", "sha256": "2e31cb4bc45aa0ff7606481d7cb8e3124d2b92770d831132eb3f6fb517a21660", "byte_length": 149},
        {"ref_id": "C1", "role": "Current", "type": "implementation-plan", "path": "plans/alert-bundle-implementation.md", "access_status": "readable", "sha256": "c989c0d5dc37c1ea0922b78f6a8d10205bf425452106d128e80035897363efc3", "byte_length": 248},
        {"ref_id": "C2", "role": "Current", "type": "generated-artifact", "path": "generated/alert-bundle-index.json", "access_status": "readable", "sha256": "15ed79d766057a4ba4c9c51d76874f428c23eb1223c7f42ddae11bdad2f2588d", "byte_length": 313},
    ],
}
GAP_CURRENT_EVIDENCE = {
    "stale-plan-vs-live-surface-conflict": [
        {"evidence_id": "C1", "type": "file-read", "strength": "direct"},
        {"evidence_id": "C2", "type": "file-read", "strength": "direct"},
    ],
    "unresolved-source-precedence-stays-ambiguous": [
        {"evidence_id": "C1", "type": "file-read", "strength": "direct"},
        {"evidence_id": "C2", "type": "file-read", "strength": "direct"},
    ],
    "plan-only-current-is-not-implementation-proof": [
        {"evidence_id": "C1", "type": "implementation-plan", "strength": "weak"},
        {"evidence_id": "C2", "type": "generated-artifact", "strength": "derived"},
    ],
}
GAP_PRECEDENCE = {
    "stale-plan-vs-live-surface-conflict": {
        "status": "unresolved",
        "resolved_order": [],
        "conflicts": ["S1", "C1", "C2"],
        "note": "Historical planning prose and live surface evidence have no owner-confirmed priority.",
    },
    "unresolved-source-precedence-stays-ambiguous": {
        "status": "unresolved",
        "resolved_order": [],
        "conflicts": ["S1", "S2"],
        "note": "Both accessible SoT refs conflict and neither has priority, supersession, or approval metadata.",
    },
    "plan-only-current-is-not-implementation-proof": {
        "status": "resolved",
        "resolved_order": ["S1"],
        "conflicts": [],
        "note": "S1 is the only SoT ref; Current plan/generated refs do not establish source priority.",
    },
}
GAP_OUTPUT_LABELS = (
    "📊 Gap summary:",
    "📝 Findings:",
    "⚠️ Ambiguities / Missing Evidence:",
    "▶️ Recommended next steps:",
)

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


def full_allowed_relative(
    value: object,
    field: str,
    allowed_roots: set[str],
    *,
    required_prefix: str | None = None,
) -> str:
    relative = full_safe_relative(value, field)
    if required_prefix is not None and not relative.startswith(f"{required_prefix}/"):
        fail(f"{field} must be under observed_root {required_prefix!r}")
    first_part = PurePosixPath(relative).parts[0]
    if first_part not in allowed_roots:
        fail(f"{field} must be under an allowed logical root")
    return relative


def full_require_inventory_map(
    value: object,
    field: str,
    *,
    allowed_roots: set[str],
    required_prefix: str | None = None,
    require_exists: bool = True,
) -> dict[str, dict[str, Any]]:
    if not isinstance(value, list):
        fail(f"{field} must be a list")
    result: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(cast(list[Any], value)):
        item_field = f"{field}[{index}]"
        if not isinstance(item, dict):
            fail(f"{item_field} must be an object")
        raw_item = cast(dict[str, Any], item)
        path = full_allowed_relative(
            raw_item.get("path"),
            f"{item_field}.path",
            allowed_roots,
            required_prefix=required_prefix,
        )
        if path in result:
            fail(f"{field} contains duplicate path {path!r}")
        snapshot = full_validate_lstat_snapshot(
            raw_item,
            item_field,
            path,
            allowed_roots=allowed_roots,
            required_prefix=required_prefix,
            require_exists=require_exists,
        )
        result[path] = snapshot
    return result


def full_validate_lstat_snapshot(
    value: object,
    field: str,
    expected_path: str,
    *,
    allowed_roots: set[str],
    required_prefix: str | None = None,
    require_exists: bool = False,
) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{field} must be an object")
    snapshot = cast(dict[str, Any], value)
    unknown_fields = set(snapshot) - FULL_LSTAT_FIELDS
    if unknown_fields:
        fail(f"{field} contains unknown fields {sorted(unknown_fields)!r}")
    path = full_allowed_relative(
        snapshot.get("path"),
        f"{field}.path",
        allowed_roots,
        required_prefix=required_prefix,
    )
    if path != expected_path:
        fail(f"{field}.path must be {expected_path!r}")
    exists = snapshot.get("exists")
    kind = snapshot.get("kind")
    if not isinstance(exists, bool):
        fail(f"{field}.exists must be a boolean")
    if exists is False:
        if require_exists:
            fail(f"{field} inventory records must describe existing entries")
        if kind != "absent":
            fail(f"{field} absent state must use kind 'absent'")
        if set(snapshot) != {"path", "exists", "kind"}:
            fail(f"{field} absent state must not include mode, size, sha256, or link_text")
        return snapshot
    if kind not in {"regular", "symlink"}:
        fail(f"{field}.kind must be 'regular' or 'symlink' for an existing entry")
    mode = snapshot.get("mode")
    if not isinstance(mode, str) or re.fullmatch(r"0o[0-7]{3,4}", mode) is None:
        fail(f"{field}.mode must be an octal lstat mode string")
    if kind == "regular":
        size = snapshot.get("size")
        if isinstance(size, bool) or not isinstance(size, int) or size < 0:
            fail(f"{field}.size must be a non-negative integer")
        full_hash(snapshot.get("sha256"), f"{field}.sha256")
        if "link_text" in snapshot:
            fail(f"{field}.regular records must not contain link_text")
        required_fields = {"path", "exists", "kind", "mode", "size", "sha256"}
    else:
        link_text = snapshot.get("link_text")
        if not isinstance(link_text, str) or not link_text or "\x00" in link_text:
            fail(f"{field}.link_text must be a non-empty symlink target")
        if "size" in snapshot or "sha256" in snapshot:
            fail(f"{field}.symlink records must not contain size or sha256")
        required_fields = {"path", "exists", "kind", "mode", "link_text"}
    if set(snapshot) != required_fields:
        missing = sorted(required_fields - set(snapshot))
        forbidden = sorted(set(snapshot) - required_fields)
        fail(f"{field} has malformed fields: missing={missing!r}, forbidden={forbidden!r}")
    return snapshot


def full_validate_git_snapshot(
    value: object,
    field: str,
    *,
    expected_worktree: bool,
) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{field} must be an object")
    snapshot = cast(dict[str, Any], value)
    if set(snapshot) != FULL_GIT_SNAPSHOT_FIELDS:
        missing = sorted(FULL_GIT_SNAPSHOT_FIELDS - set(snapshot))
        unknown = sorted(set(snapshot) - FULL_GIT_SNAPSHOT_FIELDS)
        fail(f"{field} has malformed fields: missing={missing!r}, unknown={unknown!r}")

    is_worktree = snapshot.get("is_worktree")
    if not isinstance(is_worktree, bool):
        fail(f"{field}.is_worktree must be a boolean")
    if is_worktree is not expected_worktree:
        fail(f"{field}.is_worktree must be {expected_worktree!r} for this scenario")

    rev_parse_status = snapshot.get("rev_parse_status")
    if isinstance(rev_parse_status, bool) or not isinstance(rev_parse_status, int):
        fail(f"{field}.rev_parse_status must be an integer, not a boolean")
    status_porcelain = snapshot.get("status_porcelain")
    if not isinstance(status_porcelain, list) or not all(isinstance(item, str) for item in status_porcelain):
        fail(f"{field}.status_porcelain must be a list of strings")

    head = snapshot.get("head")
    branch = snapshot.get("branch")
    if expected_worktree:
        if rev_parse_status != 0:
            fail(f"{field}.rev_parse_status must be 0 for a Git worktree")
        if not isinstance(head, str) or GIT_SHA_RE.fullmatch(head) is None:
            fail(f"{field}.head must be a lowercase 40-character Git SHA")
        require_nonempty_string(branch, f"{field}.branch")
    else:
        if rev_parse_status != 128:
            fail(f"{field}.rev_parse_status must be 128 for a non-Git fixture")
        if status_porcelain != []:
            fail(f"{field}.status_porcelain must be empty for a non-Git fixture")
        if head is not None:
            fail(f"{field}.head must be null for a non-Git fixture")
        if branch is not None:
            fail(f"{field}.branch must be null for a non-Git fixture")
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
        path = full_allowed_relative(
            item.get("path"),
            f"{label}.fixture.ignore_files[{index}].path",
            FULL_GIT_FIXTURE_ROOTS,
        )
        actual_paths.append(path)
        before = full_validate_lstat_snapshot(
            item.get("before"),
            f"{label}.fixture.ignore_files[{index}].before",
            path,
            allowed_roots=FULL_GIT_FIXTURE_ROOTS,
        )
        after = full_validate_lstat_snapshot(
            item.get("after"),
            f"{label}.fixture.ignore_files[{index}].after",
            path,
            allowed_roots=FULL_GIT_FIXTURE_ROOTS,
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


def full_validate_flat_ignore_files(
    value: object,
    label: str,
    before_inventory: dict[str, dict[str, Any]],
    after_inventory: dict[str, dict[str, Any]],
    *,
    expected_paths: list[str],
) -> None:
    if not isinstance(value, list):
        fail(f"{label}.fixture.ignore_files must be a list")
    actual_paths: list[str] = []
    for index, item in enumerate(cast(list[Any], value)):
        item_field = f"{label}.fixture.ignore_files[{index}]"
        if not isinstance(item, dict):
            fail(f"{item_field} must be an object")
        path = full_allowed_relative(item.get("path"), f"{item_field}.path", FULL_GIT_FIXTURE_ROOTS)
        actual_paths.append(path)
        snapshot = full_validate_lstat_snapshot(
            item,
            item_field,
            path,
            allowed_roots=FULL_GIT_FIXTURE_ROOTS,
        )
        if path in before_inventory and before_inventory[path] != snapshot:
            fail(f"{label}: ignore file {path!r} snapshot disagrees with fixture inventory before state")
        if path in after_inventory and after_inventory[path] != snapshot:
            fail(f"{label}: ignore file {path!r} snapshot disagrees with fixture inventory after state")
    if len(actual_paths) != len(set(actual_paths)) or actual_paths != expected_paths:
        fail(
            f"{label}.fixture.ignore_files must contain exactly the ordered snapshots for "
            f"{expected_paths!r}"
        )


def full_bind_target_to_inventory(
    snapshot: dict[str, Any],
    inventory: dict[str, dict[str, Any]],
    field: str,
) -> bool:
    path = cast(str, snapshot["path"])
    inventory_snapshot = inventory.get(path)
    if snapshot["exists"] is True and inventory_snapshot is None:
        fail(f"{field} existing target must have a matching fixture inventory record")
    if inventory_snapshot is not None and inventory_snapshot != snapshot:
        fail(f"{field} disagrees with the matching fixture inventory record")
    return inventory_snapshot is not None


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

    observed_root_first_part = PurePosixPath(observed_root).parts[0]
    state_allowed_roots = {observed_root_first_part}
    inventory_before = full_require_inventory_map(
        state_root.get("inventory_before"),
        f"{label}.state_root.inventory_before",
        allowed_roots=state_allowed_roots,
        required_prefix=observed_root,
    )
    if inventory_before:
        fail(f"{label}.state_root.inventory_before must be empty")
    inventory_after = full_require_inventory_map(
        state_root.get("inventory_after"),
        f"{label}.state_root.inventory_after",
        allowed_roots=state_allowed_roots,
        required_prefix=observed_root,
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
    target_allowed_roots = {"fixture-root"} if scenario_id == "non-git-repo-local-reject" else FULL_GIT_FIXTURE_ROOTS
    before = full_validate_lstat_snapshot(
        before,
        f"{label}.fixture.target.before",
        expected_target_path,
        allowed_roots=target_allowed_roots,
    )
    after = full_validate_lstat_snapshot(
        after,
        f"{label}.fixture.target.after",
        expected_target_path,
        allowed_roots=target_allowed_roots,
    )

    expected_worktree = scenario_id != "non-git-repo-local-reject"
    expected_invocation_cwd = "fixture-root/workdir" if not expected_worktree else "git-root"
    if fixture.get("invocation_cwd") != expected_invocation_cwd:
        fail(f"{label}.fixture.invocation_cwd must be {expected_invocation_cwd!r}")
    expected_git_root = "git-root" if expected_worktree else None
    if fixture.get("git_root") != expected_git_root:
        fail(f"{label}.fixture.git_root must be {expected_git_root!r}")

    git_before = full_validate_git_snapshot(
        fixture.get("git_before"),
        f"{label}.fixture.git_before",
        expected_worktree=expected_worktree,
    )
    git_after = full_validate_git_snapshot(
        fixture.get("git_after"),
        f"{label}.fixture.git_after",
        expected_worktree=expected_worktree,
    )
    if git_before != git_after:
        fail(f"{label}.fixture Git state changed during the scenario")

    fallback_writes = fixture.get("fallback_writes")
    if fallback_writes != []:
        fail(f"{label}.fixture.fallback_writes must be empty")

    fixture_allowed_roots = FULL_FIXTURE_ROOTS_BY_SCENARIO[scenario_id]
    before_inventory = full_require_inventory_map(
        fixture.get("fixture_inventory_before"),
        f"{label}.fixture.fixture_inventory_before",
        allowed_roots=fixture_allowed_roots,
        require_exists=False,
    )
    after_inventory = full_require_inventory_map(
        fixture.get("fixture_inventory_after"),
        f"{label}.fixture.fixture_inventory_after",
        allowed_roots=fixture_allowed_roots,
        require_exists=False,
    )
    if scenario_id == "symlink-claude-local-reject" and before["link_text"] != after["link_text"]:
        fail(f"{label}: symlink link text changed")
    if scenario_id == "eligible-repo-local-apply":
        before_inventory_has_target = full_bind_target_to_inventory(
            before,
            before_inventory,
            f"{label}.fixture.target.before",
        )
        after_inventory_has_target = full_bind_target_to_inventory(
            after,
            after_inventory,
            f"{label}.fixture.target.after",
        )
        if before.get("exists") is not False or before.get("kind") != "absent":
            fail(f"{label}: eligible target must be absent before the run")
        if after.get("exists") is not True or after.get("kind") != "regular":
            fail(f"{label}: eligible target must be a regular file after the run")
        if (
            expected_target_path in before_inventory
            and before_inventory[expected_target_path]["exists"] is True
        ):
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
        before_inventory_has_target = full_bind_target_to_inventory(
            before,
            before_inventory,
            f"{label}.fixture.target.before",
        )
        after_inventory_has_target = full_bind_target_to_inventory(
            after,
            after_inventory,
            f"{label}.fixture.target.after",
        )
        if not before["exists"] and not after["exists"] and before_inventory_has_target != after_inventory_has_target:
            fail(f"{label}: absent target inventory representation must be consistent before and after")

    ignore_files = fixture.get("ignore_files")
    if scenario_id == "not-ignored-claude-local-reject":
        full_validate_ignore_files(ignore_files, label, before_inventory, after_inventory)
    else:
        full_validate_flat_ignore_files(
            ignore_files,
            label,
            before_inventory,
            after_inventory,
            expected_paths=[] if not expected_worktree else [
                "git-root/.gitignore",
                "git-root/.git/info/exclude",
            ],
        )

    external = fixture.get("external_target")
    if scenario_id == "symlink-claude-local-reject":
        if not isinstance(external, dict):
            fail(f"{label}: symlink scenario must record an external target")
        external = full_validate_lstat_snapshot(
            external,
            f"{label}.fixture.external_target",
            "external-target/sentinel.txt",
            allowed_roots=FULL_EXTERNAL_TARGET_ROOTS,
            require_exists=True,
        )
        if external["kind"] != "regular":
            fail(f"{label}.fixture.external_target must describe a regular file")
        if before.get("kind") != "symlink" or after.get("kind") != "symlink":
            fail(f"{label}: symlink scenario target must remain a symlink")
        if before.get("link_text") != after.get("link_text"):
            fail(f"{label}: symlink link text changed")
        if before.get("link_text") != "../external-target/sentinel.txt":
            fail(f"{label}: symlink link text must resolve to the recorded external target")
        external_path = cast(str, external["path"])
        if before_inventory.get(external_path) != external:
            fail(f"{label}: symlink external target disagrees with fixture inventory before state")
        if after_inventory.get(external_path) != external:
            fail(f"{label}: symlink external target disagrees with fixture inventory after state")
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


def gap_exact_object(value: object, fields: set[str], field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{field} must be an object")
    actual = cast(dict[str, Any], value)
    if set(actual) != fields:
        missing = sorted(fields - set(actual))
        unknown = sorted(set(actual) - fields)
        fail(f"{field} has malformed fields: missing={missing!r}, unknown={unknown!r}")
    return actual


def gap_reject_host_paths(value: object, label: str) -> None:
    if isinstance(value, str):
        if any(marker in value for marker in ("/home/", "/Users/", "/tmp/", "/root/")):
            fail(f"{label} must not disclose host-specific absolute paths")
        if re.search(r"(?i)(?:^|[^A-Za-z0-9])[A-Z]:[\\\\/](?:Users|home|root|tmp)(?:[\\\\/]|$)", value):
            fail(f"{label} must not disclose host-specific absolute paths")
    elif isinstance(value, dict):
        for key, item in value.items():
            gap_reject_host_paths(item, f"{label}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            gap_reject_host_paths(item, f"{label}[{index}]")


def gap_validate_contract_blobs(value: object, field: str) -> None:
    if value != GAP_CONTRACT_BLOB_LIST:
        fail(f"{field} must match the approved ordered contract blob set")
    for relative, expected_sha in GAP_CONTRACT_BLOBS.items():
        immutable = full_git_blob(GAP_PLUGIN_COMMIT, relative, f"{field}.{relative}")
        if hashlib.sha256(immutable).hexdigest() != expected_sha:
            fail(f"{field}: immutable Git contract blob changed at {relative}")
        _, live = full_repo_file(relative, f"{field}.live.{relative}")
        if hashlib.sha256(live.read_bytes()).hexdigest() != expected_sha:
            fail(f"{field}: live contract blob differs from the immutable Git blob at {relative}")


def gap_validate_source_refs(
    value: object,
    scenario_id: str,
    label: str,
) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not value or not all(isinstance(item, dict) for item in value):
        fail(f"{label} must be a non-empty list of source-ref objects")
    refs = cast(list[dict[str, Any]], value)
    expected_fields = {"ref_id", "role", "type", "path", "access_status", "sha256", "byte_length"}
    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    for index, item in enumerate(refs):
        item_label = f"{label}[{index}]"
        gap_exact_object(item, expected_fields, item_label)
        ref_id = require_nonempty_string(item.get("ref_id"), f"{item_label}.ref_id")
        if ref_id in seen_ids:
            fail(f"{label} contains duplicate ref_id {ref_id!r}")
        seen_ids.add(ref_id)
        role = item.get("role")
        if role not in {"SoT", "Current"}:
            fail(f"{item_label}.role must be 'SoT' or 'Current'")
        require_nonempty_string(item.get("type"), f"{item_label}.type")
        path = full_safe_relative(item.get("path"), f"{item_label}.path")
        if path in seen_paths:
            fail(f"{label} contains duplicate path {path!r}")
        seen_paths.add(path)
        if item.get("access_status") != "readable":
            fail(f"{item_label}.access_status must be 'readable'")
        full_hash(item.get("sha256"), f"{item_label}.sha256")
        byte_length = item.get("byte_length")
        if isinstance(byte_length, bool) or not isinstance(byte_length, int) or byte_length < 1:
            fail(f"{item_label}.byte_length must be a positive integer")

    expected = GAP_SOURCE_REFS[scenario_id]
    if refs != expected:
        fail(f"{label} role/type/path/hash/access records do not match the approved source inventory")
    return refs


def gap_validate_current_evidence(
    value: object,
    scenario_id: str,
    source_refs: list[dict[str, Any]],
    label: str,
) -> None:
    if not isinstance(value, list) or not value or not all(isinstance(item, dict) for item in value):
        fail(f"{label} must be a non-empty list of evidence records")
    records = cast(list[dict[str, Any]], value)
    expected_fields = {"evidence_id", "type", "strength"}
    source_by_id = {item["ref_id"]: item for item in source_refs}
    seen_ids: set[str] = set()
    for index, item in enumerate(records):
        item_label = f"{label}[{index}]"
        gap_exact_object(item, expected_fields, item_label)
        evidence_id = require_nonempty_string(item.get("evidence_id"), f"{item_label}.evidence_id")
        if evidence_id in seen_ids:
            fail(f"{label} contains duplicate evidence_id {evidence_id!r}")
        seen_ids.add(evidence_id)
        source_ref = source_by_id.get(evidence_id)
        if source_ref is None or source_ref.get("role") != "Current":
            fail(f"{item_label}.evidence_id must identify a Current source ref")
        evidence_type = require_nonempty_string(item.get("type"), f"{item_label}.type")
        if evidence_type != source_ref.get("type"):
            fail(f"{item_label}.type must match its source-ref type")
        if item.get("strength") not in {"direct", "weak", "derived"}:
            fail(f"{item_label}.strength must be direct, weak, or derived")
    if records != GAP_CURRENT_EVIDENCE[scenario_id]:
        fail(f"{label} does not match the approved Current evidence records")


def gap_validate_precedence(value: object, scenario_id: str, source_refs: list[dict[str, Any]], label: str) -> None:
    precedence = gap_exact_object(value, {"status", "resolved_order", "conflicts", "note"}, label)
    status = precedence.get("status")
    if status not in {"resolved", "unresolved"}:
        fail(f"{label}.status must be 'resolved' or 'unresolved'")
    for field in ("resolved_order", "conflicts"):
        values = precedence.get(field)
        if not isinstance(values, list) or not all(isinstance(item, str) and item for item in values):
            fail(f"{label}.{field} must be a list of non-empty strings")
        if len(values) != len(set(values)):
            fail(f"{label}.{field} must not contain duplicate ref IDs")
    ref_ids = {item["ref_id"] for item in source_refs}
    for field in ("resolved_order", "conflicts"):
        if not set(cast(list[str], precedence[field])).issubset(ref_ids):
            fail(f"{label}.{field} must identify listed source refs only")
    require_nonempty_string(precedence.get("note"), f"{label}.note")
    if precedence != GAP_PRECEDENCE[scenario_id]:
        fail(f"{label} does not preserve the approved source-precedence decision")


def gap_validate_inventory_records(value: object, scenario_id: str, label: str) -> None:
    if not isinstance(value, list) or not value or not all(isinstance(item, dict) for item in value):
        fail(f"{label} must be a non-empty list of inventory records")
    records = cast(list[dict[str, Any]], value)
    seen_paths: set[str] = set()
    for index, item in enumerate(records):
        item_label = f"{label}[{index}]"
        path = full_allowed_relative(item.get("path"), f"{item_label}.path", {"fixture-root"})
        if path in seen_paths:
            fail(f"{label} contains duplicate path {path!r}")
        seen_paths.add(path)
        kind = item.get("kind")
        mode = item.get("mode")
        if not isinstance(mode, str) or re.fullmatch(r"0o[0-7]{3,4}", mode) is None:
            fail(f"{item_label}.mode must be an octal lstat mode string")
        if kind == "directory":
            if set(item) != {"path", "kind", "mode"}:
                fail(f"{item_label} directory record has malformed fields")
        elif kind == "regular":
            if set(item) != {"path", "kind", "mode", "size", "sha256"}:
                fail(f"{item_label} regular record has malformed fields")
            size = item.get("size")
            if isinstance(size, bool) or not isinstance(size, int) or size < 0:
                fail(f"{item_label}.size must be a non-negative integer")
            full_hash(item.get("sha256"), f"{item_label}.sha256")
        else:
            fail(f"{item_label}.kind must be 'directory' or 'regular'")
    if full_json_digest(records) != GAP_FIXTURE_INVENTORY_HASHES[scenario_id]:
        fail(f"{label} does not match the approved complete fixture inventory")


def gap_validate_git_snapshot(value: object, scenario_id: str, label: str) -> None:
    snapshot = gap_exact_object(
        value,
        {
            "rev_parse_status",
            "branch_status",
            "status_command_status",
            "staged_command_status",
            "unstaged_command_status",
            "head",
            "branch",
            "status_porcelain",
            "staged_paths",
            "unstaged_paths",
        },
        label,
    )
    for field in (
        "rev_parse_status",
        "branch_status",
        "status_command_status",
        "staged_command_status",
        "unstaged_command_status",
    ):
        value_for_field = snapshot.get(field)
        if isinstance(value_for_field, bool) or not isinstance(value_for_field, int) or value_for_field != 0:
            fail(f"{label}.{field} must be integer 0")
    if snapshot.get("head") != GAP_FIXTURE_HEADS[scenario_id]:
        fail(f"{label}.head must preserve the recorded fixture Git HEAD")
    if snapshot.get("branch") != "main":
        fail(f"{label}.branch must be 'main'")
    for field in ("status_porcelain", "staged_paths", "unstaged_paths"):
        values = snapshot.get(field)
        if values != [] or not isinstance(values, list):
            fail(f"{label}.{field} must be an empty list for the read-only run")


def gap_validate_fixture(source: dict[str, Any], scenario_id: str, label: str) -> None:
    fixture = gap_exact_object(
        source.get("fixture"),
        {
            "invocation_cwd",
            "git_root",
            "git_before",
            "git_after",
            "fixture_inventory_before",
            "fixture_inventory_after",
            "changed_paths",
            "fallback_writes",
        },
        f"{label}.fixture",
    )
    if fixture.get("invocation_cwd") != "fixture-root" or fixture.get("git_root") != "fixture-root":
        fail(f"{label}.fixture must preserve the logical fixture root")
    gap_validate_git_snapshot(fixture.get("git_before"), scenario_id, f"{label}.fixture.git_before")
    gap_validate_git_snapshot(fixture.get("git_after"), scenario_id, f"{label}.fixture.git_after")
    if fixture.get("git_before") != fixture.get("git_after"):
        fail(f"{label}.fixture Git before/after snapshots must be exactly equal")
    gap_validate_inventory_records(
        fixture.get("fixture_inventory_before"),
        scenario_id,
        f"{label}.fixture.fixture_inventory_before",
    )
    gap_validate_inventory_records(
        fixture.get("fixture_inventory_after"),
        scenario_id,
        f"{label}.fixture.fixture_inventory_after",
    )
    if fixture.get("fixture_inventory_before") != fixture.get("fixture_inventory_after"):
        fail(f"{label}.fixture inventories must be exactly equal for a read-only run")
    if fixture.get("changed_paths") != []:
        fail(f"{label}.fixture.changed_paths must be empty")
    if fixture.get("fallback_writes") != []:
        fail(f"{label}.fixture.fallback_writes must be empty")


def gap_validate_empty_inventory(value: object, label: str) -> None:
    if not isinstance(value, list):
        fail(f"{label} must be a list")
    if value != []:
        fail(f"{label} must be empty for the no-write run")


def gap_validate_state(source: dict[str, Any], label: str) -> None:
    state_root = gap_exact_object(
        source.get("state_root"),
        {"requested", "observed_root", "honored", "inventory_before", "inventory_after"},
        f"{label}.state_root",
    )
    if state_root.get("requested") != "state-root" or state_root.get("observed_root") != "state-root":
        fail(f"{label}.state_root requested/observed roots must be 'state-root'")
    if state_root.get("honored") is not True:
        fail(f"{label}.state_root.honored must be true for the captured run")
    gap_validate_empty_inventory(state_root.get("inventory_before"), f"{label}.state_root.inventory_before")
    gap_validate_empty_inventory(state_root.get("inventory_after"), f"{label}.state_root.inventory_after")

    temporary = gap_exact_object(
        source.get("temporary_home_tigerkit"),
        {"root", "inventory_before", "inventory_after"},
        f"{label}.temporary_home_tigerkit",
    )
    if temporary.get("root") != "temporary-home/.tigerkit":
        fail(f"{label}.temporary_home_tigerkit.root must be the normalized temporary-home root")
    gap_validate_empty_inventory(
        temporary.get("inventory_before"),
        f"{label}.temporary_home_tigerkit.inventory_before",
    )
    gap_validate_empty_inventory(
        temporary.get("inventory_after"),
        f"{label}.temporary_home_tigerkit.inventory_after",
    )
    if temporary.get("inventory_before") != temporary.get("inventory_after"):
        fail(f"{label}.temporary_home_tigerkit inventories must be exactly equal")

    privacy = gap_exact_object(source.get("privacy"), {"normalized_paths"}, f"{label}.privacy")
    if privacy.get("normalized_paths") != ["fixture-root", "plugin-root", "state-root", "temporary-home"]:
        fail(f"{label}.privacy.normalized_paths must preserve the approved logical path tokens")


def full_validate_gap_source(path: Path, record: dict[str, Any], scenario_id: str) -> dict[str, Any]:
    label = str(path.relative_to(ROOT))
    source = load_json(path)
    gap_exact_object(
        source,
        {
            "schemaVersion",
            "scenario_id",
            "session",
            "plugin",
            "command",
            "tool_evidence",
            "runtime",
            "consumer_output",
            "gap_observation",
            "fixture",
            "state_root",
            "temporary_home_tigerkit",
            "privacy",
        },
        label,
    )
    if source.get("schemaVersion") != GAP_SOURCE_SCHEMA:
        fail(f"{label}.schemaVersion must be {GAP_SOURCE_SCHEMA!r}")
    if source.get("scenario_id") != scenario_id:
        fail(f"{label}.scenario_id must match the result scenario")
    gap_reject_host_paths(source, label)

    session = gap_exact_object(
        source.get("session"),
        {
            "session_id",
            "fresh",
            "isolated",
            "write_free",
            "consumer",
            "consumer_version",
            "wrapper",
            "wrapper_version",
            "provider",
            "model",
            "model_source",
        },
        f"{label}.session",
    )
    expected_session = {
        "session_id": GAP_SESSION_IDS[scenario_id],
        "fresh": True,
        "isolated": True,
        "write_free": True,
        "consumer": GAP_CONSUMER,
        "consumer_version": GAP_CONSUMER_VERSION,
        "wrapper": GAP_WRAPPER,
        "wrapper_version": GAP_WRAPPER_VERSION,
        "provider": GAP_PROVIDER,
        "model": GAP_MODEL,
        "model_source": GAP_MODEL_SOURCE,
    }
    if session != expected_session or session.get("session_id") != record.get("session_id"):
        fail(f"{label}.session must preserve the actual isolated runtime and derived model truth")

    plugin = gap_exact_object(
        source.get("plugin"),
        {"path", "repo_id", "commit", "contract_blobs"},
        f"{label}.plugin",
    )
    if plugin.get("path") != "plugin-root" or plugin.get("repo_id") != "tiger-kit" or plugin.get("commit") != GAP_PLUGIN_COMMIT:
        fail(f"{label}.plugin must identify the recorded plugin checkout and commit")
    gap_validate_contract_blobs(plugin.get("contract_blobs"), f"{label}.plugin.contract_blobs")

    command = gap_exact_object(
        source.get("command"),
        {
            "argv",
            "argv_sha256",
            "invocation_cwd",
            "plugin_dir",
            "permission_mode",
            "allowed_tools",
            "max_turns",
            "session_persistence",
            "prompt_sha256",
            "prompt_byte_length",
        },
        f"{label}.command",
    )
    argv = command.get("argv")
    if not isinstance(argv, list) or len(argv) != 15:
        fail(f"{label}.command.argv must preserve the 15-argument wrapper invocation")
    prompt = argv[3] if isinstance(argv, list) and len(argv) > 3 else None
    prompt = require_nonempty_string(prompt, f"{label}.command.argv[3]")
    if hashlib.sha256(prompt.encode("utf-8")).hexdigest() != GAP_PROMPT_HASHES[scenario_id]:
        fail(f"{label}.command prompt does not match the approved exact request")
    if len(prompt.encode("utf-8")) != GAP_PROMPT_LENGTHS[scenario_id]:
        fail(f"{label}.command prompt byte length does not match the approved request")
    expected_argv = [
        "ccs",
        "codex",
        "-p",
        prompt,
        "--plugin-dir",
        "plugin-root",
        "--permission-mode",
        "dontAsk",
        "--allowedTools",
        ",".join(GAP_ALLOWED_TOOLS),
        "--max-turns",
        "16",
        "--no-session-persistence",
        "--output-format",
        "json",
    ]
    if argv != expected_argv:
        fail(f"{label}.command.argv must preserve the exact isolated plugin invocation")
    if command.get("argv_sha256") != GAP_ARGV_HASHES[scenario_id] or full_json_digest(argv) != command.get("argv_sha256"):
        fail(f"{label}.command.argv_sha256 does not match the exact invocation")
    if command.get("invocation_cwd") != "fixture-root" or command.get("plugin_dir") != "plugin-root":
        fail(f"{label}.command logical cwd/plugin dir must preserve the captured tokens")
    if command.get("permission_mode") != "dontAsk" or command.get("allowed_tools") != GAP_ALLOWED_TOOLS:
        fail(f"{label}.command permission/tools do not match the captured wrapper")
    if command.get("max_turns") != 16 or command.get("session_persistence") is not False:
        fail(f"{label}.command turn/session settings do not match the captured wrapper")
    if command.get("prompt_sha256") != GAP_PROMPT_HASHES[scenario_id]:
        fail(f"{label}.command.prompt_sha256 does not match the approved exact request")
    if command.get("prompt_byte_length") != GAP_PROMPT_LENGTHS[scenario_id]:
        fail(f"{label}.command.prompt_byte_length does not match the approved request")

    tool_evidence = gap_exact_object(
        source.get("tool_evidence"),
        {"plugin_command", "consumer_envelope"},
        f"{label}.tool_evidence",
    )
    plugin_command = tool_evidence.get("plugin_command")
    if plugin_command != {
        "executable": "ccs",
        "subcommand": "codex",
        "public_surface": "/tk:gap",
        "argv": argv,
        "invocation_cwd": "fixture-root",
        "plugin_dir": "plugin-root",
    }:
        fail(f"{label}.tool_evidence.plugin_command must identify the exact /tk:gap invocation")

    runtime = gap_exact_object(
        source.get("runtime"),
        {"model_usage", "model_usage_keys", "observed_result"},
        f"{label}.runtime",
    )
    model_usage = runtime.get("model_usage")
    if not isinstance(model_usage, dict) or not model_usage:
        fail(f"{label}.runtime.model_usage must be a non-empty object")
    if runtime.get("model_usage_keys") != GAP_MODEL_USAGE_KEYS:
        fail(f"{label}.runtime.model_usage_keys must preserve actual routing keys")
    if full_json_digest(model_usage) != GAP_MODEL_USAGE_HASHES[scenario_id]:
        fail(f"{label}.runtime.model_usage does not match the actual recorded modelUsage")
    expected_observed = {
        "type": "result",
        "subtype": "success",
        "is_error": False,
        "stop_reason": "end_turn",
        "terminal_reason": "completed",
        "num_turns": GAP_TURNS[scenario_id],
        "permission_denials": [],
    }
    if runtime.get("observed_result") != expected_observed:
        fail(f"{label}.runtime.observed_result must preserve the actual successful result metadata")

    envelope = tool_evidence.get("consumer_envelope")
    if envelope != {"session_id": GAP_SESSION_IDS[scenario_id], **expected_observed}:
        fail(f"{label}.tool_evidence.consumer_envelope must preserve the exact envelope; model is intentionally null/absent")

    consumer_output = gap_exact_object(
        source.get("consumer_output"),
        {"result", "result_sha256", "result_byte_length", "raw_result_sha256"},
        f"{label}.consumer_output",
    )
    assistant_result = require_nonempty_string(consumer_output.get("result"), f"{label}.consumer_output.result")
    result_sha, result_length = GAP_RESULT_HASHES[scenario_id]
    if consumer_output.get("result_sha256") != result_sha or consumer_output.get("raw_result_sha256") != result_sha:
        fail(f"{label}.consumer_output result hashes do not match the approved assistant result")
    if hashlib.sha256(assistant_result.encode("utf-8")).hexdigest() != result_sha or consumer_output.get("result_byte_length") != result_length or len(assistant_result.encode("utf-8")) != result_length:
        fail(f"{label}.consumer_output result hash/length does not match the exact result bytes")
    for output_label in GAP_OUTPUT_LABELS:
        if output_label not in assistant_result:
            fail(f"{label}.consumer_output.result is missing canonical label {output_label!r}")
    for ref in GAP_SOURCE_REFS[scenario_id]:
        if ref["ref_id"] not in assistant_result:
            fail(f"{label}.consumer_output.result must visibly preserve source ref {ref['ref_id']!r}")

    observation = gap_exact_object(
        source.get("gap_observation"),
        {
            "source_refs",
            "source_manifest_sha256",
            "current_evidence",
            "precedence",
            "final_classification",
            "recommendation",
            "direct_implementation_evidence",
            "direct_runtime_evidence",
            "direct_command_output_evidence",
            "direct_rendered_output_evidence",
            "direct_diff_evidence",
        },
        f"{label}.gap_observation",
    )
    source_refs = gap_validate_source_refs(observation.get("source_refs"), scenario_id, f"{label}.gap_observation.source_refs")
    source_manifest_sha = full_hash(observation.get("source_manifest_sha256"), f"{label}.gap_observation.source_manifest_sha256")
    if source_manifest_sha != GAP_SOURCE_MANIFEST_HASHES[scenario_id] or full_json_digest(source_refs) != source_manifest_sha:
        fail(f"{label}.gap_observation.source_manifest_sha256 does not bind the deterministic source inventory")
    gap_validate_current_evidence(
        observation.get("current_evidence"),
        scenario_id,
        source_refs,
        f"{label}.gap_observation.current_evidence",
    )
    gap_validate_precedence(
        observation.get("precedence"),
        scenario_id,
        source_refs,
        f"{label}.gap_observation.precedence",
    )
    if observation.get("final_classification") != GAP_FINAL_CLASSIFICATIONS[scenario_id]:
        fail(f"{label}.gap_observation.final_classification must preserve the approved pilot classification")
    recommendation = require_nonempty_string(observation.get("recommendation"), f"{label}.gap_observation.recommendation")
    if recommendation != GAP_RECOMMENDATIONS[scenario_id]:
        fail(f"{label}.gap_observation.recommendation must preserve the approved next step")
    for field in (
        "direct_implementation_evidence",
        "direct_runtime_evidence",
        "direct_command_output_evidence",
        "direct_rendered_output_evidence",
        "direct_diff_evidence",
    ):
        if observation.get(field) != []:
            fail(f"{label}.gap_observation.{field} must be empty; no direct implementation/runtime proof was captured")
    if scenario_id == "plan-only-current-is-not-implementation-proof" and (
        source_refs[1].get("type") != "implementation-plan"
        or source_refs[2].get("type") != "generated-artifact"
        or observation.get("direct_implementation_evidence") != []
        or observation.get("direct_runtime_evidence") != []
    ):
        fail(f"{label}: scenario3 Current evidence must remain plan/generated only with no direct implementation/runtime evidence")

    gap_validate_fixture(source, scenario_id, label)
    gap_validate_state(source, label)
    return source


def full_validate_gap_result() -> None:
    full_validate_inventory()
    result = load_json(GAP_RESULT_PATH)
    label = str(GAP_RESULT_PATH.relative_to(ROOT))
    gap_exact_object(
        result,
        {"schemaVersion", "pilot_id", "kind", "status", "evidence_tier", "evidence_scope", "runtime", "contract_blobs", "scenarios"},
        label,
    )
    if result.get("schemaVersion") != GAP_RESULT_SCHEMA:
        fail(f"{label}.schemaVersion must be {GAP_RESULT_SCHEMA!r}")
    if result.get("pilot_id") != "gap-stale-sot-precedence":
        fail(f"{label}.pilot_id must match the approved GAP pilot")
    if result.get("kind") != "full-real-agent-results":
        fail(f"{label}.kind must be 'full-real-agent-results'")
    if result.get("status") != "full-validated" or result.get("status") == "shipped":
        fail(f"{label}.status must be 'full-validated' and never 'shipped'")
    if result.get("evidence_tier") != "full-real-agent":
        fail(f"{label}.evidence_tier must be 'full-real-agent'")
    if result.get("evidence_scope") != "internal consistency record; not independent authenticity":
        fail(f"{label}.evidence_scope must state the internal-consistency limitation")
    gap_reject_host_paths(result, label)

    runtime = gap_exact_object(
        result.get("runtime"),
        {"wrapper", "wrapper_version", "provider", "consumer", "consumer_version", "model", "plugin_commit", "invocation"},
        f"{label}.runtime",
    )
    for field, expected in {
        "wrapper": GAP_WRAPPER,
        "wrapper_version": GAP_WRAPPER_VERSION,
        "provider": GAP_PROVIDER,
        "consumer": GAP_CONSUMER,
        "consumer_version": GAP_CONSUMER_VERSION,
        "model": GAP_MODEL,
        "plugin_commit": GAP_PLUGIN_COMMIT,
    }.items():
        if runtime.get(field) != expected:
            fail(f"{label}.runtime.{field} must be {expected!r}")
    expected_invocation = {
        "executable": "ccs",
        "subcommand": "codex",
        "permission_mode": "dontAsk",
        "allowed_tools": GAP_ALLOWED_TOOLS,
        "max_turns": 16,
        "session_persistence": False,
        "output_format": "json",
        "paths": "per-scenario logical fixture/plugin/state/home tokens are recorded in each raw source",
    }
    if runtime.get("invocation") != expected_invocation:
        fail(f"{label}.runtime.invocation must preserve the actual wrapper command shape")
    gap_validate_contract_blobs(result.get("contract_blobs"), f"{label}.contract_blobs")

    records = result.get("scenarios")
    if not isinstance(records, list) or len(records) != len(GAP_SCENARIO_IDS) or not all(isinstance(item, dict) for item in records):
        fail(f"{label}.scenarios must contain exactly the three approved scenario records")
    records = cast(list[dict[str, Any]], records)
    actual_ids = [require_nonempty_string(item.get("id"), f"{label}.scenarios[{index}].id") for index, item in enumerate(records)]
    if actual_ids != list(GAP_SCENARIO_IDS):
        fail(f"{label}.scenarios must contain exactly the approved scenario IDs in order")

    seen_sessions: set[str] = set()
    referenced_sources: set[str] = set()
    expected_record_fields = {
        "id",
        "source_path",
        "source_sha256",
        "session_id",
        "prompt_sha256",
        "prompt_byte_length",
        "assistant_result_sha256",
        "assistant_result_byte_length",
        "succeeded",
        "observed_result",
        "model",
        "model_usage_keys",
        "modelUsage",
        "source_manifest_sha256",
        "final_classification",
        "recommendation",
        "result_contains_prompt_refs",
    }
    for index, record in enumerate(records):
        scenario_id = actual_ids[index]
        prefix = f"{label}.scenarios[{index}]"
        gap_exact_object(record, expected_record_fields, prefix)
        expected_source = f"evals/results/raw/full-gap-stale-sot-precedence/{scenario_id}.json"
        source_relative, source_path = full_repo_file(record.get("source_path"), f"{prefix}.source_path")
        if source_relative != expected_source:
            fail(f"{prefix}.source_path must be the canonical durable GAP source for {scenario_id}")
        if source_relative in referenced_sources:
            fail(f"{prefix}.source_path must be unique")
        referenced_sources.add(source_relative)
        source_sha = full_hash(record.get("source_sha256"), f"{prefix}.source_sha256")
        if source_sha != GAP_SOURCE_HASHES[scenario_id] or source_sha != hashlib.sha256(source_path.read_bytes()).hexdigest():
            fail(f"{prefix}.source_sha256 does not match the canonical durable source")

        session_id = require_nonempty_string(record.get("session_id"), f"{prefix}.session_id")
        if session_id in seen_sessions:
            fail(f"{prefix}.session_id must be unique across all GAP scenarios")
        seen_sessions.add(session_id)
        if session_id != GAP_SESSION_IDS[scenario_id]:
            fail(f"{prefix}.session_id must identify the exact isolated run")
        prompt_sha = full_hash(record.get("prompt_sha256"), f"{prefix}.prompt_sha256")
        if prompt_sha != GAP_PROMPT_HASHES[scenario_id] or record.get("prompt_byte_length") != GAP_PROMPT_LENGTHS[scenario_id]:
            fail(f"{prefix}.prompt hash/length does not match the exact recorded request")
        result_sha, result_length = GAP_RESULT_HASHES[scenario_id]
        if record.get("assistant_result_sha256") != result_sha or record.get("assistant_result_byte_length") != result_length:
            fail(f"{prefix} assistant result hash/length does not match the canonical result")
        if record.get("succeeded") is not True:
            fail(f"{prefix}.succeeded must be true for the actual successful result")
        expected_observed = {
            "type": "result",
            "subtype": "success",
            "is_error": False,
            "stop_reason": "end_turn",
            "terminal_reason": "completed",
            "num_turns": GAP_TURNS[scenario_id],
            "permission_denials": [],
        }
        if record.get("observed_result") != expected_observed:
            fail(f"{prefix}.observed_result must preserve actual success metadata")
        if record.get("model") != GAP_MODEL or record.get("model_usage_keys") != GAP_MODEL_USAGE_KEYS:
            fail(f"{prefix}.model/model_usage_keys must preserve the derived actual routing")
        model_usage = record.get("modelUsage")
        if not isinstance(model_usage, dict) or full_json_digest(model_usage) != GAP_MODEL_USAGE_HASHES[scenario_id]:
            fail(f"{prefix}.modelUsage does not match the actual recorded routing usage")
        if record.get("source_manifest_sha256") != GAP_SOURCE_MANIFEST_HASHES[scenario_id]:
            fail(f"{prefix}.source_manifest_sha256 does not match the approved source inventory")
        if record.get("final_classification") != GAP_FINAL_CLASSIFICATIONS[scenario_id]:
            fail(f"{prefix}.final_classification must match the pilot invariant")
        if record.get("recommendation") != GAP_RECOMMENDATIONS[scenario_id]:
            fail(f"{prefix}.recommendation must preserve the approved next step")
        if record.get("result_contains_prompt_refs") is not True:
            fail(f"{prefix}.result_contains_prompt_refs must be true")

        source = full_validate_gap_source(source_path, record, scenario_id)
        if record.get("modelUsage") != source["runtime"]["model_usage"] or record.get("model_usage_keys") != source["runtime"]["model_usage_keys"]:
            fail(f"{prefix}.modelUsage/model_usage_keys must match the durable raw source")
        if record.get("observed_result") != source["runtime"]["observed_result"]:
            fail(f"{prefix}.observed_result must match the durable raw source")
        if record.get("prompt_sha256") != source["command"]["prompt_sha256"] or record.get("prompt_byte_length") != source["command"]["prompt_byte_length"]:
            fail(f"{prefix}.prompt hash/length must match the durable raw command")
        if record.get("assistant_result_sha256") != source["consumer_output"]["result_sha256"] or record.get("assistant_result_byte_length") != source["consumer_output"]["result_byte_length"]:
            fail(f"{prefix}.assistant result hash/length must match the durable raw output")
        if record.get("source_manifest_sha256") != source["gap_observation"]["source_manifest_sha256"]:
            fail(f"{prefix}.source_manifest_sha256 must match the durable source manifest")
        if record.get("final_classification") != source["gap_observation"]["final_classification"]:
            fail(f"{prefix}.final_classification must match the durable source observation")
        if record.get("recommendation") != source["gap_observation"]["recommendation"]:
            fail(f"{prefix}.recommendation must match the durable source observation")

    expected_sources = {
        f"evals/results/raw/full-gap-stale-sot-precedence/{scenario_id}.json"
        for scenario_id in GAP_SCENARIO_IDS
    }
    if referenced_sources != expected_sources:
        fail(f"{label}.scenarios must reference exactly the approved durable GAP raw files")



def full_validate_inventory() -> None:
    if not FULL_RESULT_PATH.exists():
        fail(f"missing required result file: {FULL_RESULT_PATH.relative_to(ROOT)}")
    if not GAP_RESULT_PATH.exists():
        fail(f"missing required result file: {GAP_RESULT_PATH.relative_to(ROOT)}")
    if not GAP_RAW_DIR.exists():
        fail(f"missing required evidence directory: {GAP_RAW_DIR.relative_to(ROOT)}")
    full_require_real_directory(RESULTS_DIR, str(RESULTS_DIR.relative_to(ROOT)))
    result_entries = full_inventory(RESULTS_DIR, str(RESULTS_DIR.relative_to(ROOT)))
    result_files = {entry.name for entry in result_entries if entry.is_file()}
    if result_files != {
        "micro-initial-command-wording.json",
        FULL_RESULT_PATH.name,
        GAP_RESULT_PATH.name,
    }:
        fail(f"{RESULTS_DIR.relative_to(ROOT)} contains unexpected result files: {sorted(result_files)!r}")
    result_dirs = {entry.name for entry in result_entries if entry.is_dir()}
    if result_dirs != {"raw"}:
        fail(f"{RESULTS_DIR.relative_to(ROOT)} contains unexpected directories: {sorted(result_dirs)!r}")
    raw_parent = RESULTS_DIR / "raw"
    raw_parent_entries = full_inventory(raw_parent, str(raw_parent.relative_to(ROOT)))
    raw_dirs = {entry.name for entry in raw_parent_entries if entry.is_dir()}
    if raw_dirs != {
        "micro-initial-command-wording",
        FULL_RAW_DIR.name,
        GAP_RAW_DIR.name,
    }:
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
    gap_entries = full_inventory(GAP_RAW_DIR, str(GAP_RAW_DIR.relative_to(ROOT)))
    actual_gap_files = {entry.name for entry in gap_entries if entry.is_file()}
    expected_gap_files = {f"{scenario_id}.json" for scenario_id in GAP_SCENARIO_IDS}
    if actual_gap_files != expected_gap_files:
        fail(
            f"{GAP_RAW_DIR.relative_to(ROOT)} inventory mismatch: "
            f"unexpected={sorted(actual_gap_files - expected_gap_files)!r}, missing={sorted(expected_gap_files - actual_gap_files)!r}"
        )
    if any(entry.is_dir() for entry in gap_entries):
        fail(f"{GAP_RAW_DIR.relative_to(ROOT)} must contain only logical source files")


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
        full_validate_gap_result()
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
