#!/usr/bin/env bash
set -euo pipefail

hook_input="$(cat)"

json_field() {
  local field="$1"
  HOOK_INPUT="$hook_input" FIELD="$field" python3 - <<'PY'
import json, os
try:
    data = json.loads(os.environ.get("HOOK_INPUT", "{}") or "{}")
except json.JSONDecodeError:
    data = {}
field = os.environ["FIELD"]
value = data.get(field, "")
if value is None:
    value = ""
if isinstance(value, bool):
    value = "true" if value else "false"
print(str(value))
PY
}

hash_text() {
  python3 - "$1" <<'PY'
import hashlib, sys
print(hashlib.sha1(sys.argv[1].encode()).hexdigest()[:12])
PY
}

session_id="$(json_field session_id)"
if [ -z "$session_id" ]; then
  session_id="unknown-session"
fi

cwd="$(json_field cwd)"
if [ -z "$cwd" ]; then
  cwd="$(pwd)"
fi

last_assistant_message="$(json_field last_assistant_message)"
stop_hook_active="$(json_field stop_hook_active)"

if [ ! -d "$cwd" ]; then
  exit 0
fi

cd "$cwd"

if ! repo_root="$(git rev-parse --show-toplevel 2>/dev/null)"; then
  exit 0
fi

cd "$repo_root"

branch="$(git branch --show-current 2>/dev/null || true)"
if [ -z "$branch" ]; then
  branch="detached"
fi

repo_hash="$(hash_text "$repo_root")"
branch_hash="$(hash_text "$branch")"
state_dir="${TMPDIR:-/tmp}/tiger-kit/${repo_hash}/${branch_hash}/${session_id}"
manifest="${state_dir}/verification.md"
mkdir -p "$state_dir"

changed_files="$(
  {
    git diff --name-only
    git diff --cached --name-only
    git ls-files --others --exclude-standard
  } | sed '/^$/d' | sort -u
)"

create_manifest_template() {
  CHANGED_FILES="$changed_files" MANIFEST="$manifest" python3 - <<'PY'
import json, os
from pathlib import Path
files = [p for p in os.environ.get("CHANGED_FILES", "").splitlines() if p]
manifest = Path(os.environ["MANIFEST"])
manifest.parent.mkdir(parents=True, exist_ok=True)
payload = {
    "schema": "tigerkit.verification.v1",
    "files": [
        {
            "path": path,
            "status": "TODO",
            "method": "TODO",
            "result": "TODO",
            "note": "TODO",
        }
        for path in files
    ],
}
manifest.write_text(
    "# TigerKit Verification Manifest\n\n"
    "JSON block:\n\n"
    + json.dumps(payload, ensure_ascii=False, indent=2)
    + "\n",
    encoding="utf-8",
)
PY
}

validate_manifest() {
  CHANGED_FILES="$changed_files" MANIFEST="$manifest" python3 - <<'PY'
import json, os, sys
from pathlib import Path
changed = [p for p in os.environ.get("CHANGED_FILES", "").splitlines() if p]
manifest = Path(os.environ["MANIFEST"])
allowed = {"verified", "unverified", "not-applicable"}
problems = []
try:
    text = manifest.read_text(encoding="utf-8")
except FileNotFoundError:
    print("missing manifest")
    sys.exit(1)
start = text.find("{")
end = text.rfind("}")
if start == -1 or end == -1 or end < start:
    print("missing JSON block")
    sys.exit(1)
try:
    data = json.loads(text[start:end + 1])
except json.JSONDecodeError as exc:
    print(f"invalid JSON block: {exc}")
    sys.exit(1)
entries = data.get("files")
if not isinstance(entries, list):
    print("files must be an array")
    sys.exit(1)
by_path = {}
for entry in entries:
    if isinstance(entry, dict) and isinstance(entry.get("path"), str):
        by_path[entry["path"]] = entry
for path in changed:
    entry = by_path.get(path)
    if entry is None:
        problems.append(f"missing entry: {path}")
        continue
    status = entry.get("status")
    if status not in allowed:
        problems.append(f"invalid status for {path}: {status!r}")
    for key in ("method", "result", "note"):
        value = entry.get(key)
        if not isinstance(value, str) or not value.strip() or value.strip() == "TODO":
            problems.append(f"empty {key} for {path}")
if problems:
    print("\n".join(problems))
    sys.exit(1)
print("ok")
PY
}

block_for_manifest() {
  local details="$1"
  local count_file="${state_dir}/verification-block-count"
  local count=0
  if [ -f "$count_file" ]; then
    count="$(cat "$count_file" 2>/dev/null || echo 0)"
  fi
  count=$((count + 1))
  printf '%s' "$count" > "$count_file"

  {
    echo "TigerKit verification manifest guard:"
    echo
    echo "변경사항이 있지만 변경 파일별 검증 상태 manifest가 없거나 누락되어 있습니다."
    echo
    echo "임시 manifest 파일을 작성하거나 보완하세요:"
    echo "$manifest"
    echo
    echo "각 변경 파일에는 status, method, result, note가 필요합니다."
    echo "status 허용값: verified | unverified | not-applicable"
    echo
    echo "문제:"
    echo "$details"
    echo
    if [ "$stop_hook_active" = "true" ] || [ "$count" -gt 1 ]; then
      echo "반복 block 중입니다. 위 manifest만 보완하면 통과합니다. 검증 상태 없이 완료 선언은 통과하지 않습니다."
    else
      echo "특정 package manager나 테스트 명령은 강제하지 않습니다. 프로젝트에 맞는 검증 방식을 기록하세요."
    fi
  } >&2
  exit 2
}

if [ -n "$changed_files" ]; then
  if [ ! -f "$manifest" ]; then
    create_manifest_template
    block_for_manifest "manifest가 없어 template을 생성했습니다."
  fi
  if ! validation_output="$(validate_manifest 2>&1)"; then
    block_for_manifest "$validation_output"
  fi
fi

advisor_signal="$(LAST_ASSISTANT_MESSAGE="$last_assistant_message" python3 - <<'PY'
import os, re
msg = os.environ.get("LAST_ASSISTANT_MESSAGE", "") or ""
low = msg.lower()
blocked = [
    "blocked", "stalled", "cannot proceed", "can't proceed", "needs human",
    "human follow-up", "막힘", "막혔", "중단", "확인 필요", "사람 확인",
]
section = [
    "completed", "done", "finished", "pass", "완료", "처리 완료", "검증", "pass", "작업 완료",
]
if any(token in low or token in msg for token in blocked):
    print("blocked")
elif any(token in low or token in msg for token in section):
    print("section-complete")
else:
    print("")
PY
)"

if [ -n "$advisor_signal" ]; then
  signature="$(LAST_ASSISTANT_MESSAGE="$last_assistant_message" SIGNAL="$advisor_signal" python3 - <<'PY'
import hashlib, os, re
signal = os.environ.get("SIGNAL", "")
msg = os.environ.get("LAST_ASSISTANT_MESSAGE", "") or ""
normalized = re.sub(r"\s+", " ", msg).strip()[:800]
print(hashlib.sha1((signal + "\n" + normalized).encode()).hexdigest()[:16])
PY
)"
  seen_file="${state_dir}/advisor-${signature}"
  if [ ! -f "$seen_file" ]; then
    printf '%s
' "$advisor_signal" > "$seen_file"
    {
      echo "TigerKit handoff/reflect advisor:"
      echo
      if [ "$advisor_signal" = "blocked" ]; then
        echo "현재 응답이 blocked/stalled 경계에 도달한 것으로 보입니다."
      else
        echo "현재 응답이 작업 단위 완료 경계에 도달한 것으로 보입니다."
      fi
      echo
      echo "다음 세션에서 이어갈 필요가 있다면 /tk:handoff를 고려하세요."
      echo "이번 세션에서 얻은 durable rule, 제약, 반복 실수가 있다면 /tk:reflect도 고려하세요."
      echo
      echo "이것은 선택형 제안입니다. handoff/reflect 없이 계속 진행해도 됩니다."
    } >&2
    exit 2
  fi
fi

exit 0
