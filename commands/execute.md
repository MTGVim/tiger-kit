---
description: LoopSpec v2를 user-only bounded execution dispatcher로 검증하고 execution receipt를 생성합니다.
argument-hint: "<spec-id-or-path>"
---

이 문서는 TigerKit `/tk:execute` command contract를 정의합니다.

사용자에게는 한글로 답합니다. 코드, path, URL, identifier, command, YAML/JSON field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:execute`는 사용자가 명시적으로 지정한 `tigerkit.loop-spec/v2` 하나를 실행 대상으로 받아 preflight, executor routing, postflight verifier, receipt 저장을 수행하는 dispatcher surface입니다.

```text
execute = LoopSpec v2 + current context + support-matrix environment gate -> one executor delegation -> postflight receipt
```

## Core boundary

- 모델이 자동 호출하지 않습니다. 사용자가 `/tk:execute <spec-id-or-path>`를 명시한 경우에만 동작합니다.
- 입력은 spec ID 또는 path 하나뿐입니다.
- legacy LoopSpec, stale spec, blocked spec, invalid spec은 위임 전에 reject합니다.
- dispatcher는 product source를 직접 수정하지 않습니다.
- dispatcher는 정확히 하나의 executor만 선택합니다.
- 자동 fallback, 자동 rollback, executor 간 자동 위임은 없습니다.
- current environment는 `support/execute-support-matrix.json`에 정확히 한 번 등록되어 있어야 합니다.
- matching environment의 `status`가 `preview` 또는 `public`이면 실행을 계속합니다.
- matching environment의 `status`가 `unsupported`이거나 entry가 없으면 `hard_enforcement_unavailable`로 reject합니다.
- environment key는 `claude-code/<platform>/local/<permissionMode>` 형식이며 `isolationMode`는 별도 gate로 보지 않습니다.

## Execution instruction

When this command is invoked, resolve the helper from the **installed TigerKit plugin cache**, not from the current working repository.

```bash
TIGERKIT_STATE_SCRIPT="$({
python3 - <<'PY'
import json, re, subprocess
from pathlib import Path

def version_key_text(text: str):
    try:
        return tuple(int(part) for part in text.split('.'))
    except Exception:
        return (0,)

def version_key_path(path: Path):
    return version_key_text(path.parent.parent.name)

def cache_path_for_version(version: str):
    path = Path.home() / '.claude/plugins/cache/tiger-kit/tk' / version / 'scripts' / 'tigerkit_state.py'
    return path if path.is_file() else None

candidates = []
seen = set()
try:
    details = subprocess.check_output(['claude', 'plugin', 'details', 'tk'], text=True)
    first = details.splitlines()[0].strip()
    match = re.match(r'^tk\s+(\d+(?:\.\d+)*)$', first)
    if match:
        path = cache_path_for_version(match.group(1))
        if path:
            candidates.append(path)
            seen.add(str(path))
except Exception:
    pass
try:
    plugins = json.loads(subprocess.check_output(['claude', 'plugin', 'list', '--json'], text=True))
except Exception:
    plugins = []
for item in plugins:
    if item.get('id') == 'tk@tiger-kit' and item.get('enabled'):
        path = Path(item.get('installPath', '')) / 'scripts' / 'tigerkit_state.py'
        if path.is_file() and str(path) not in seen:
            candidates.append(path)
            seen.add(str(path))
for path in sorted(Path.home().glob('.claude/plugins/cache/tiger-kit/tk/*/scripts/tigerkit_state.py'), key=version_key_path, reverse=True):
    if str(path) not in seen:
        candidates.append(path)
        seen.add(str(path))
if not candidates:
    raise SystemExit('TigerKit helper not found in installed plugin cache. Run `claude plugin marketplace update tiger-kit` and reinstall/update `tk@tiger-kit`.')
print(candidates[0])
PY
})"
python3 "$TIGERKIT_STATE_SCRIPT" execute $ARGUMENTS
```

If the user invokes `/tk:execute` with no spec ID/path or too many arguments, return concise usage text instead of surfacing a raw shell error.

## Dispatcher contract

1. Resolve spec ID/path through `~/.tigerkit/repos/<repo-key>/branches/<scope-key>/loop-specs/<spec-id>/spec.yaml` or explicit path.
2. Validate `schemaVersion: tigerkit.loop-spec/v2`.
3. Validate readiness is `complete`, not `blocked`.
4. Validate executor recommendation is exactly `fast` or `reasoning`.
5. Validate current repository identity, worktree/scope identity, head/fingerprint freshness, scope declarations, guards, and required verifiers.
6. Validate current environment against `support/execute-support-matrix.json`.
7. If environment support is unavailable, reject and persist a receipt only when repository/scope identity is fully resolved.
8. Capture preflight baseline for delegated executions.
9. Delegate to exactly one executor agent matching recommendation.
10. Validate executor response as `tigerkit.executor-claimed-result/v1`.
11. Observe actual create/modify/delete diff independently.
12. Re-run all required verifiers in declaration order.
13. Classify final result as `completed | escalated | failed | rejected`.
14. Persist immutable receipt under `~/.tigerkit/repos/<repo-key>/branches/<scope-key>/executions/<execution-id>.yaml` by atomic rename.

## Human output

Default output is compact projection of persisted receipt or pre-receipt rejection:

```text
Execute: <completed|escalated|failed|rejected>
Spec: <spec-id>
Executor: <fast|reasoning|NONE>
Receipt: <path or NONE>
Changed paths: <count>
Verifiers: <passed>/<total> passed
Primary reason: <reason code when non-completed>
Required action: <recommended action when non-completed>
```

Omit empty/default sections. Do not print `NONE` sections except fields where absence prevents ambiguity.

## 금지

- user request 없이 자동 실행
- legacy spec 자동 변환
- dispatcher source write
- 자동 fallback
- 자동 rollback
- partial changes 숨김
- executor self-report를 completion proof로 단독 신뢰
- support matrix에 없는 environment에서 실행 성공 표시
