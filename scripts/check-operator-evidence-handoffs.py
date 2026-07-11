#!/usr/bin/env python3
"""Validate the retained real-agent helper-backed operator handoff proof."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, NoReturn

ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = ROOT / "evals" / "results" / "operator-evidence-handoffs.json"
SCHEMA = "tigerkit.operator-evidence-handoffs/v1"
PLUGIN_COMMIT = "61c9bc59b4cdec56c05b68f29647e358cfd568a8"
EXPECTED_CHAINS = ("gap-route", "reflect-learn")
EXPECTED_SESSIONS = {
    "gap-route": "bd06a3bd-e427-4b68-89d0-665537cb85c2",
    "reflect-learn": "293843af-4403-484e-973f-518920b8b4f0",
}
EXPECTED_HELPER_ARGV = {
    "gap-route": [
        "python3",
        "plugin-root/scripts/tigerkit_state.py",
        "read-gap-packet",
        "--repo-root",
        "fixture-root",
    ],
    "reflect-learn": [
        "python3",
        "plugin-root/scripts/tigerkit_state.py",
        "read-reflect-candidate",
        "--repo-root",
        "fixture-root",
        "--candidate-id",
        "R1",
    ],
}
EXPECTED_PRODUCER_ARGV = {
    "gap-route": [
        "python3",
        "plugin-root/scripts/tigerkit_state.py",
        "write-gap-packet",
        "--repo-root",
        "fixture-root",
        "--packet-file",
        "gap-packet-input.json",
    ],
    "reflect-learn": ["/tk:reflect", "--target", "skill"],
}
EXPECTED_PUBLIC_SURFACES = {
    "gap-route": "/tk:route",
    "reflect-learn": "/tk:learn",
}
EXPECTED_CONSUMER_COMMAND = ["ccs", "codex", "-p"]
EXPECTED_CONSUMER_OPTIONS = [
    "--plugin-dir",
    "plugin-root",
    "--permission-mode",
    "dontAsk",
    "--allowedTools",
    "Read,Grep,Glob,Bash",
    "--max-turns",
    "16",
    "--no-session-persistence",
    "--output-format",
    "json",
]
EXPECTED_MODELS = "gpt-5.5(high)"
EXPECTED_MODEL_USAGE_KEYS = ["gpt-5.4-mini(low)", "gpt-5.5(high)"]
COMPARABLE_SKILL_PATH = "temporary-home/.claude/skills"
EXCLUDED_SKILL_PATH = "canonical-user-claude-skills"
EXCLUDED_SKILL_REASON = "Path identity is unstable: temporary HOME, TIGERKIT_STATE_ROOT, CLAUDE_CONFIG_DIR, and XDG exports leaked into the controller once and were later restored, so the before/after canonical token snapshots may resolve different physical paths."
CONTRACT_BLOBS = {
    "commands/gap.md": "4f64eafbbcc1d5191d90163e8d57768e90e5fbf20d2082267caf1a2cb701623d",
    "commands/route.md": "043f9d387ac544773df42e3d4d5cc45d72451296afe6d71d96c845ab185df1df",
    "commands/reflect.md": "2a904f242c4657abd92a7ff834e7663fa835cff4b87e653af973a9a430678412",
    "commands/learn.md": "b03b342c04ae78156c8a2f47722127bbebedc685d5857e11169476be16341cea",
    "skills/gap/SKILL.md": "1f40267d304b90f96c7cfcc2bf3e6902d48f17815ae76312b17eaa7ac44f3828",
    "skills/route/SKILL.md": "7c25a0c2608fd676f57c763d08584fb3924d3d576ff2a8676d09110e6d2237d2",
    "skills/reflect/SKILL.md": "5674d26473ea89de383209bb4d06c411d633747b50e00456ab325511ca539634",
    "skills/learn/SKILL.md": "4906704956d6db76fd40820fe3e4e1663584b67e5f769cb8f16fead8bdc4fb62",
    ".tigerkit/docs/output-contract.md": "eab16292a7f5aa3be02e125710bda0bedce1feaa77e364f4afdb1c6e98a59914",
    ".tigerkit/docs/gap-route-evidence-packets.md": "9d93248f25516b11cf7fc57575a0b496e24f4d1e37b8c0e0bd0004ea7bdb55a3",
    ".tigerkit/docs/reflect-learn-evidence-handoff.md": "ba21bef38e4e5ce4f8e55ad5fef2abdffa93f621906b1757937c488dba8c8c09",
}
STALE_INVALID_CHOICE = {
    "commands/gap.md": "enabled `tk@tiger-kit` install이 이 source checkout보다 오래되어 `draft-paths`, `gap-packet-paths`, `read-gap-packet`, `write-gap-packet` 같은 helper subcommand에서 `invalid choice`가 나오면 먼저 marketplace/plugin을 업데이트하거나, matching checkout/install root를 `CLAUDE_PLUGIN_ROOT`로 지정해야 합니다.",
    "commands/learn.md": "enabled `tk@tiger-kit` install이 오래되어 `read-reflect-candidate`가 `invalid choice`로 실패하면 먼저 marketplace/plugin을 업데이트하거나, matching checkout/install root를 `CLAUDE_PLUGIN_ROOT`로 지정합니다.",
}


def fail(message: str) -> NoReturn:
    raise SystemExit(f"operator evidence handoff check failed: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def obj(value: object, field: str) -> dict[str, Any]:
    require(isinstance(value, dict), f"{field} must be an object")
    return value  # type: ignore[return-value]


def text(value: object, field: str) -> str:
    require(isinstance(value, str) and bool(value), f"{field} must be a non-empty string")
    return value


def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def json_digest(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def exact_file_hash(path: str) -> str:
    candidate = ROOT / path
    require(candidate.is_file(), f"missing live contract file: {path}")
    return hashlib.sha256(candidate.read_bytes()).hexdigest()


def immutable_blob(path: str) -> bytes:
    completed = subprocess.run(
        ["git", "show", f"{PLUGIN_COMMIT}:{path}"],
        cwd=ROOT,
        capture_output=True,
        check=False,
    )
    require(completed.returncode == 0, f"cannot read plugin blob at {PLUGIN_COMMIT}:{path}")
    return completed.stdout


def reject_host_paths(value: object, field: str) -> None:
    if isinstance(value, str):
        for marker in ("/home/", "/Users/", "/tmp/", "/root/"):
            require(marker not in value, f"{field} contains host-specific absolute path")
    elif isinstance(value, dict):
        for key, item in value.items():
            reject_host_paths(item, f"{field}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            reject_host_paths(item, f"{field}[{index}]")


def load_result() -> dict[str, Any]:
    require(RESULT_PATH.is_file(), f"missing required result file: {RESULT_PATH.relative_to(ROOT)}")
    try:
        loaded = json.loads(RESULT_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid JSON: {exc}")
    return obj(loaded, str(RESULT_PATH.relative_to(ROOT)))


def validate_plugin(result: dict[str, Any]) -> None:
    plugin = obj(result.get("plugin"), "plugin")
    require(plugin.get("commit") == PLUGIN_COMMIT, "plugin.commit must identify the actual consumer checkout commit")
    require(plugin.get("checkout") == "plugin-root", "plugin.checkout must be plugin-root")
    blobs = plugin.get("contract_blobs")
    require(isinstance(blobs, list), "plugin.contract_blobs must be a list")
    actual: dict[str, str] = {}
    for index, item in enumerate(blobs):
        record = obj(item, f"plugin.contract_blobs[{index}]")
        path = text(record.get("path"), f"plugin.contract_blobs[{index}].path")
        sha = text(record.get("sha256"), f"plugin.contract_blobs[{index}].sha256")
        require(path not in actual, f"duplicate contract blob: {path}")
        actual[path] = sha
    require(actual == CONTRACT_BLOBS, "plugin.contract_blobs must match the recorded contract set")
    for path, expected_sha in CONTRACT_BLOBS.items():
        require(json_digest([path]) != "", "deterministic blob check is enabled")
        require(digest(immutable_blob(path).decode("utf-8")) == expected_sha, f"immutable plugin blob changed: {path}")
        require(exact_file_hash(path) == expected_sha, f"live plugin blob differs from recorded commit: {path}")

    stale = plugin.get("stale_invalid_choice_contract_blobs")
    require(isinstance(stale, list), "stale_invalid_choice_contract_blobs must be a list")
    stale_map = {text(obj(item, "stale contract").get("path"), "stale contract path"): obj(item, "stale contract") for item in stale}
    require(set(stale_map) == set(STALE_INVALID_CHOICE), "stale invalid-choice contract set is incomplete")
    for path, snippet in STALE_INVALID_CHOICE.items():
        record = stale_map[path]
        require(record.get("sha256") == CONTRACT_BLOBS[path], f"stale contract hash mismatch: {path}")
        require(record.get("required_text") == snippet, f"stale invalid-choice text mismatch: {path}")
        require(snippet in immutable_blob(path).decode("utf-8"), f"immutable stale invalid-choice text missing: {path}")


def validate_missing(result: dict[str, Any]) -> None:
    missing = obj(result.get("helper_missing_outputs"), "helper_missing_outputs")
    expected = {
        "gap": {
            "found": False,
            "stdout": "{\n  \"found\": false,\n  \"repoRoot\": \"fixture-root\",\n  \"commonGitDir\": \"fixture-root/.git\",\n  \"repoKey\": \"fixture-root--63e94f81\",\n  \"worktreeKey\": \"fixture-root--d028259f\",\n  \"scopeKey\": \"main\",\n  \"currentPacketPath\": \"state-root/repos/fixture-root--63e94f81/branches/main/gap/current.packet.json\"\n}\n",
            "sha256": "b3461e69220749218bf7df88ba64bf43edfbebfba1132035fd7cedffbe6b067c",
            "byte_length": 298,
        },
        "reflect": {
            "found": False,
            "stdout": "{\n  \"found\": false,\n  \"repoRoot\": \"fixture-root\",\n  \"commonGitDir\": \"fixture-root/.git\",\n  \"repoKey\": \"fixture-root--63e94f81\",\n  \"worktreeKey\": \"fixture-root--d028259f\",\n  \"scopeKey\": \"main\",\n  \"ledgerPath\": \"state-root/repos/fixture-root--63e94f81/branches/main/reflect/current.yaml\",\n  \"candidateId\": \"R1\",\n  \"same_session_required\": true,\n  \"same_ledger_required\": true,\n  \"source_of_truth\": \"reflect-ledger\"\n}\n",
            "sha256": "6ef81453d3fe3f423c66d55ffbb9cf00634a0cc3b378b5398e5112456bdd3f17",
            "byte_length": 415,
        },
    }
    require(set(missing) == set(expected), "helper_missing_outputs must contain exactly gap and reflect")
    for name, values in expected.items():
        actual = obj(missing.get(name), f"helper_missing_outputs.{name}")
        for key, value in values.items():
            require(actual.get(key) == value, f"helper_missing_outputs.{name}.{key} does not match retained missing output")
        require(json.loads(text(actual.get("stdout"), f"helper_missing_outputs.{name}.stdout"))["found"] is False, f"{name} missing output must say found:false")
        require(digest(actual["stdout"]) == actual["sha256"], f"helper_missing_outputs.{name}.sha256 is not over stdout")
        require(len(actual["stdout"].encode("utf-8")) == actual["byte_length"], f"helper_missing_outputs.{name}.byte_length mismatch")


def validate_no_write(chain: dict[str, Any], name: str) -> None:
    proof = obj(chain.get("no_write"), f"{name}.no_write")
    for key in ("fixture_git", "state_root"):
        record = obj(proof.get(key), f"{name}.no_write.{key}")
        require(record.get("before") == record.get("after"), f"{name}.{key} before/after state changed")
        require(record.get("changed_paths") == [], f"{name}.{key}.changed_paths must be empty")
    require(proof.get("fixture_changed_paths") == [], f"{name}.fixture_changed_paths must be empty")
    require(proof.get("plugin_changed_paths") == [], f"{name}.plugin_changed_paths must be empty")
    require(proof.get("state_changed_paths") == [], f"{name}.state_changed_paths must be empty")
    if name == "reflect-learn":
        skill = obj(proof.get("skill_surface"), f"{name}.no_write.skill_surface")
        before = obj(skill.get("before"), f"{name}.skill_surface.before")
        after = obj(skill.get("after"), f"{name}.skill_surface.after")
        before_paths = before.get("paths")
        after_paths = after.get("paths")
        if not isinstance(before_paths, list) or not isinstance(after_paths, list):
            fail(f"{name}.skill_surface paths must be lists")
        before_by_token = {text(obj(item, "skill_surface.before path").get("path_token"), "skill_surface.before path_token"): item for item in before_paths}
        after_by_token = {text(obj(item, "skill_surface.after path").get("path_token"), "skill_surface.after path_token"): item for item in after_paths}
        require(set(before_by_token) == {COMPARABLE_SKILL_PATH, EXCLUDED_SKILL_PATH}, f"{name}.skill_surface.before must retain exactly the comparable and excluded paths")
        require(set(after_by_token) == set(before_by_token), f"{name}.skill_surface.after path set must match before")
        temp_before = before_by_token[COMPARABLE_SKILL_PATH]
        temp_after = after_by_token[COMPARABLE_SKILL_PATH]
        require(temp_before == temp_after and temp_before["exists"] is False, f"{name} temporary skill surface was written")
        require(skill.get("comparable_path_tokens") == [COMPARABLE_SKILL_PATH], f"{name}.comparable_path_tokens must scope no-write proof to the temporary skill surface")
        excluded = skill.get("excluded_incomparable_paths")
        require(excluded == [{"comparison": "excluded", "path_token": EXCLUDED_SKILL_PATH, "reason": EXCLUDED_SKILL_REASON}], f"{name}.excluded_incomparable_paths must bind the unstable canonical snapshot")
        canonical_before = before_by_token[EXCLUDED_SKILL_PATH]
        canonical_after = after_by_token[EXCLUDED_SKILL_PATH]
        require(canonical_before == {"entry_count": 0, "exists": False, "kind": "missing", "manifest_sha256": "ffa63583dfa6706b87d284b86b0d693a161e4840aad2c5cf6b5d27c3b9621f7d", "path_token": EXCLUDED_SKILL_PATH}, f"{name} excluded canonical before snapshot mismatch was not retained")
        require(canonical_after == {"entry_count": 34, "exists": True, "kind": "directory", "manifest_sha256": "7420e259c02961c541d83a18665addf7fdfa05fdaeb680040e101cfe11ba6a32", "path_token": EXCLUDED_SKILL_PATH}, f"{name} excluded canonical after snapshot mismatch was not retained")
        require(canonical_before != canonical_after, f"{name} excluded canonical snapshot mismatch was not retained")
        require(skill.get("no_write_scope") == f"comparable consumer-owned skill surfaces only: {COMPARABLE_SKILL_PATH}", f"{name}.no_write_scope must exclude incomparable paths")
        require(skill.get("candidate_skill_write") is False, f"{name} candidate_skill_write must be false")
        require(skill.get("name_confirmed") is False, f"{name} name_confirmed must be false")
    canonical = obj(proof.get("canonical_tigerkit"), f"{name}.no_write.canonical_tigerkit")
    require(canonical.get("before") == canonical.get("after"), f"{name}.canonical_tigerkit changed")
    require(canonical.get("unchanged") is True, f"{name}.canonical_tigerkit.unchanged must be true")


def validate_chain(chain: dict[str, Any], index: int, seen_sessions: set[str]) -> None:
    name = text(chain.get("id"), f"chains[{index}].id")
    require(name in EXPECTED_CHAINS, f"unexpected chain id: {name}")
    helper = obj(chain.get("helper"), f"{name}.helper")
    producer = obj(chain.get("producer"), f"{name}.producer")
    consumer = obj(chain.get("consumer"), f"{name}.consumer")
    prompt = obj(consumer.get("prompt"), f"{name}.consumer.prompt")
    output = obj(consumer.get("result"), f"{name}.consumer.result")

    helper_stdout = text(helper.get("stdout"), f"{name}.helper.stdout")
    require(digest(helper_stdout) == helper.get("sha256"), f"{name}.helper.sha256 mismatch")
    require(len(helper_stdout.encode("utf-8")) == helper.get("byte_length"), f"{name}.helper.byte_length mismatch")
    helper_data = json.loads(helper_stdout)
    require(helper_data.get("found") is True, f"{name}.helper data must say found:true")
    require(chain.get("expected_helper_argv") == EXPECTED_HELPER_ARGV[name], f"{name}.expected_helper_argv is not the canonical helper argv")
    require(helper.get("argv") == EXPECTED_HELPER_ARGV[name], f"{name}.helper argv mismatch")
    prompt_content = text(prompt.get("content"), f"{name}.consumer.prompt.content")
    require(consumer.get("public_surface") == EXPECTED_PUBLIC_SURFACES[name], f"{name}.consumer.public_surface mismatch")
    consumer_argv = consumer.get("argv")
    require(isinstance(consumer_argv, list), f"{name}.consumer argv must be a list")
    require(
        consumer_argv == EXPECTED_CONSUMER_COMMAND + [prompt_content] + EXPECTED_CONSUMER_OPTIONS,
        f"{name}.consumer argv must preserve ccs codex prompt position and options",
    )
    require(prompt_content in consumer_argv, f"{name} prompt is not bound to consumer argv")
    require(digest(prompt_content) == prompt.get("sha256"), f"{name}.prompt sha256 mismatch")
    require(len(prompt_content.encode("utf-8")) == prompt.get("byte_length"), f"{name}.prompt byte_length mismatch")
    require(helper_stdout in prompt_content, f"{name}.prompt does not contain exact normalized helper stdout")

    producer_output = text(producer.get("output"), f"{name}.producer.output")
    require(digest(producer_output) == producer.get("sha256"), f"{name}.producer output sha256 mismatch")
    require(len(producer_output.encode("utf-8")) == producer.get("byte_length"), f"{name}.producer output byte_length mismatch")
    producer_argv = producer.get("argv")
    require(isinstance(producer_argv, list), f"{name}.producer argv must be a list")
    require(producer_argv == EXPECTED_PRODUCER_ARGV[name], f"{name}.producer argv mismatch")
    producer_data = obj(json.loads(producer_output), f"{name}.producer.output")

    if name == "gap-route":
        producer_packet = producer_data
        helper_packet = obj(helper_data.get("packet"), f"{name}.helper.packet")
        require(
            {key: value for key, value in helper_packet.items() if key != "created_at"} == producer_packet,
            f"{name} producer packet content/identity does not flow into helper packet",
        )
        require(set(helper_packet) == set(producer_packet) | {"created_at"}, f"{name} helper packet fields drifted from producer packet")
        require(producer_packet.get("repo_root") == helper_data.get("repoRoot"), f"{name} repo root identity did not flow into helper")
        require(producer_packet.get("repo_key") == helper_data.get("repoKey"), f"{name} repo key identity did not flow into helper")
        require(producer_packet.get("scope_key") == helper_data.get("scopeKey"), f"{name} scope identity did not flow into helper")
        require(producer.get("output_path") == producer_argv[-1], f"{name} producer packet path does not match producer argv")
    else:
        producer_candidates = producer_data.get("candidates")
        helper_candidate = obj(helper_data.get("candidate"), f"{name}.helper.candidate")
        require(producer_data.get("schemaVersion") == "tigerkit.reflect-ledger/v1", f"{name} producer ledger schema mismatch")
        require(producer_data.get("ledger_path") == helper_data.get("ledgerPath"), f"{name} ledger identity did not flow into helper")
        require(producer_candidates == [helper_candidate], f"{name} producer candidate fields did not flow into helper")
        require(helper_data.get("candidateId") == helper_candidate.get("candidate_id"), f"{name} candidate identity did not flow into helper")
        require(helper_data.get("source_of_truth") == "reflect-ledger", f"{name} helper source_of_truth mismatch")

    session_id = text(consumer.get("session_id"), f"{name}.consumer.session_id")
    require(session_id == EXPECTED_SESSIONS[name], f"{name} session_id is not the retained actual session")
    require(session_id not in seen_sessions, f"session_id reused: {session_id}")
    seen_sessions.add(session_id)
    runtime = obj(consumer.get("runtime"), f"{name}.consumer.runtime")
    require(runtime.get("wrapper") == "ccs codex", f"{name}.runtime.wrapper mismatch")
    require(runtime.get("provider") == "openai-codex", f"{name}.runtime.provider mismatch")
    require(runtime.get("consumer") == "Claude Code", f"{name}.runtime.consumer mismatch")
    require(runtime.get("model") == EXPECTED_MODELS, f"{name}.runtime.model mismatch")
    require(runtime.get("model_usage_keys") == EXPECTED_MODEL_USAGE_KEYS, f"{name}.runtime.model_usage_keys mismatch")
    usage = runtime.get("modelUsage")
    require(isinstance(usage, dict) and list(usage) == EXPECTED_MODEL_USAGE_KEYS, f"{name}.modelUsage keys mismatch")
    require(usage == consumer.get("modelUsage"), f"{name}.runtime.modelUsage must match consumer.modelUsage")
    observed = obj(consumer.get("observed_result"), f"{name}.consumer.observed_result")
    require(observed.get("type") == "result" and observed.get("subtype") == "success", f"{name} must preserve successful result metadata")
    require(observed.get("is_error") is False and observed.get("stop_reason") == "end_turn", f"{name} result metadata mismatch")
    require(observed.get("permission_denials") == [], f"{name} permission_denials must be empty")
    actual_output = text(output.get("content"), f"{name}.consumer.result.content")
    require(digest(actual_output) == output.get("sha256"), f"{name}.result sha256 mismatch")
    require(len(actual_output.encode("utf-8")) == output.get("byte_length"), f"{name}.result byte_length mismatch")
    require(output.get("sha256") == consumer.get("assistant_result_sha256"), f"{name} normalized result hash is not bound to consumer record")
    require(output.get("byte_length") == consumer.get("assistant_result_byte_length"), f"{name} normalized result length is not bound to consumer record")

    if name == "gap-route":
        for citation in ("gap packet", "S1", "S2", "F1", "unresolved", "route: decision"):
            require(citation in actual_output, f"gap-route result missing semantic citation {citation!r}")
        require(helper_data["packet"]["precedence"]["status"] == "unresolved", "gap helper precedence must be unresolved")
        require(helper_data["packet"]["findings"][0]["finding_id"] == "F1", "gap helper finding must be F1")
        require(helper_data["packet"]["findings"][0]["route"] == "decision", "gap helper route must be decision")
        require(helper_data["packet"]["precedence"]["conflicts"] == ["S1", "S2"], "gap helper precedence conflicts mismatch")
    else:
        require("R1" in actual_output, "reflect-learn result missing semantic citation 'R1'")
        require("reflect-candidate" in actual_output, "reflect-learn result missing semantic citation 'reflect-candidate'")
        require(
            "preview-only" in actual_output or "preview only" in actual_output,
            "reflect-learn result missing preview-only semantic citation",
        )
        require("name confirmation needed" in actual_output, "reflect-learn result missing semantic citation 'name confirmation needed'")
        require(helper_data["candidateId"] == "R1", "reflect helper candidate must be R1")
        require(helper_data["source_of_truth"] == "reflect-ledger", "reflect helper source_of_truth mismatch")
        require(helper_data["same_session_required"] is True, "reflect helper same_session_required must be true")
        require(helper_data["same_ledger_required"] is True, "reflect helper same_ledger_required must be true")
        require(helper_data["candidate"]["candidate_id"] == "R1", "reflect helper candidate identity mismatch")
        require(helper_data["candidate"]["action"] == "suggest_only", "reflect helper action mismatch")

    validate_no_write(chain, name)


def main() -> int:
    try:
        result = load_result()
        require(result.get("schemaVersion") == SCHEMA, "schemaVersion mismatch")
        require(result.get("kind") == "full-real-agent-results", "kind mismatch")
        require(result.get("status") == "full-validated", "status must be full-validated")
        require(result.get("evidence_tier") == "full-real-agent", "evidence_tier must be full-real-agent")
        require(result.get("evidence_scope") == "internal consistency record; not independent authenticity", "evidence_scope mismatch")
        reject_host_paths(result, "result")
        validate_plugin(result)
        validate_missing(result)
        chains = result.get("chains")
        require(isinstance(chains, list), "chains must be a list")
        ids = [text(obj(item, f"chains[{i}]").get("id"), f"chains[{i}].id") for i, item in enumerate(chains)]
        require(ids == list(EXPECTED_CHAINS), "chains must contain exactly the two approved chain IDs in order")
        seen_sessions: set[str] = set()
        for index, chain in enumerate(chains):
            validate_chain(obj(chain, f"chains[{index}]"), index, seen_sessions)
        require(len(seen_sessions) == 2, "session IDs must be unique across both chains")
    except SystemExit:
        raise
    except Exception as exc:
        fail(f"malformed evidence rejected without traceback: {type(exc).__name__}: {exc}")
    print("operator evidence handoffs ok: gap-route + reflect-learn; full-validated/full-real-agent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
