---
description: SoT gap을 분석합니다.
argument-hint: "[SoT refs or pasted source] [--target <path|area>] [--print-report]"
flow: [route, next]
---

이 문서는 TigerKit `/tk:gap` 명령 계약을 정의합니다.

사용자에게는 한글로 답합니다. 코드, path, URL, ticket, commit, hash, identifier, error, contract field name은 증거 보존을 위해 원문 그대로 둘 수 있습니다.

목표: `/tk:gap`은 Source of Truth와 Current Implementation을 한 번 비교해 핵심 차이를 드러내는 명령입니다.

이 명령은 workflow를 생성하거나 고정하지 않습니다.

related wrapper skill:

```text
skills/gap/SKILL.md
```

```text
gap = source of truth ↔ current implementation one-shot comparison
```

## Core guidance

- SoT가 있으면 구현 전에 `/tk:gap`을 먼저 고려합니다.
- SoT가 없다고 바로 중단하지는 않습니다. blindspot pass가 더 맞는 경우에는 unknown unknowns를 질문 목록으로 바꿔 discovery를 돕습니다.
- 사용자가 바로 진행을 원하면 `/tk:gap` 없이 진행할 수 있지만, 그 경우 가정과 불확실성을 명시합니다.

## Modes

- `SoT-present`: 기존 one-shot gap 분석입니다.
- `SoT-absent / blindspot`: 현재 코드베이스와 task wording만으로 unknown unknowns를 스캔하고, 사용자 프롬프트를 개선할 질문 목록을 만듭니다.
- blindspot mode도 workflow executor는 아니고, report + follow-up question surface에 머뭅니다.

## Inputs

가능한 범위에서 아래를 분리합니다.

- `SoT`: 사용자 지시, PRD, design spec, issue, URL, pasted notes, screenshot/export, API docs, source contract.
- `Current`: 현재 repo 파일, diff, rendered output, command output, implementation plan, generated artifact.
- `Unknown`: 접근 불가 reference, 소유자 결정, 모호한 source priority, 확인하지 않은 producer surface.

`Current` evidence는 동일 강도가 아닙니다. 읽은 파일, 실행 결과, rendered output, diff, generated artifact, implementation plan을 구분해서 기록합니다. plan이나 generated artifact만으로 구현 완료를 단정하지 않습니다.

## Analysis policy

1. Source ref 목록과 각 ref의 access status를 먼저 고정합니다.
2. SoT에서 확인 가능한 requirement만 추출합니다.
3. Current Implementation은 읽은 파일, 실행 결과, rendered output, diff처럼 직접 확인한 evidence로만 기록하고 evidence type을 구분합니다.
4. source 간 우선순위가 확인되지 않으면 임의로 병합하지 않고 `ambiguous`로 남깁니다.
5. 아래 네 가지 gap을 분류합니다.
   - `missing`: SoT 요구가 Current에 없음.
   - `mismatch`: SoT와 Current가 다름.
   - `overbuilt`: SoT 밖 구현이 surface 확장, 사용자 혼란, 유지보수 비용, 숨은 자동화 기대를 만듦.
   - `ambiguous`: source conflict, missing owner decision, inaccessible source, producer evidence 부족.
6. 각 finding은 최소한 SoT, Current, Evidence, Impact, Priority, Suggested fix를 포함합니다.
7. actionable finding에는 `direct | brainstorm | decision` route를 제안하고 route 이유를 evidence identifier와 연결합니다. `brainstorm`은 구현 전에 `/tk:route`로 direct, subagent-driven, goal-driven 중 어느 길이 맞는지 먼저 정리해야 한다는 뜻입니다.
8. non-actionable finding에는 route를 강제하지 않습니다.
9. 모호한 source를 조용히 병합하지 않습니다.

## Priority

- `P0`: core task 불가능, 권한/보안/데이터 무결성/파괴적 동작 위험.
- `P1`: 핵심 사용자 흐름, business rule, validation, error/loading/empty state, CTA 이해에 큰 영향.
- `P2`: visible consistency, 정보 위계, design-system consistency 약화.
- `P3`: minor polish. 기본 finding에는 넣지 않고 필요하면 Not accepted summary에만 둡니다.

## Output

기본 stdout projection은 compact합니다.

- 기본 응답은 핵심 표, findings, 다음 행동 중심으로 요약합니다.
- detailed markdown report는 `--print-report`이 있거나 사용자가 저장/출력을 명시했을 때만 전체 형태로 출력하거나 external report로 저장합니다.
- path-heavy artifact detail은 필요할 때만 노출합니다.

```text
📊 Gap summary:
| Area | SoT | Current | Gap | Impact | Priority |
|---|---|---|---|---|---|

📝 Findings:
### 1. <finding title>
- SoT:
- Current:
- Evidence:
- Evidence type:
- Impact:
- Priority:
- Suggested fix:
- Route: direct | brainstorm | decision
- Route evidence:

⚠️ Ambiguities / Missing Evidence:
| Ref | Question | Evidence checked | Impact | Recommendation |
|---|---|---|---|---|

📝 Not accepted summary:
- <optional low-priority or rejected note>

▶️ Recommended next steps:
1. <next step>
```

Findings에는 P0/P1/P2만 넣습니다. P3, duplicate, unverifiable, source conflict, missing evidence는 의사결정 가치가 낮거나 근거가 약하므로 Findings가 아니라 Ambiguities 또는 Not accepted summary에 둡니다.

## Artifact policy

사용자가 저장을 명시하거나 command contract가 저장을 요구할 때만 external generated report를 씁니다. 새 write path는 project repository 밖 `~/.tigerkit/`입니다.

```text
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/GAP-YYYYMMDD-HHmmss-RAND.md
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/current.md
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/GAP-YYYYMMDD-HHmmss-RAND.packet.json
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/current.packet.json
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/branch-state.json
```

gap이 남기는 markdown report와 별도로 route handoff용 machine-readable `gap packet`을 둘 수 있습니다.

```text
schemaVersion: tigerkit.gap-packet/v1
```

packet은 최소한 아래를 담아야 합니다.

- `schemaVersion`
- `invocation_id`
- `gap_id`
- `repo_root`
- `repo_key`
- `scope_key`
- `source_refs`
- `precedence`
- `findings`
- `unresolved_questions`
- `report_path`
- `created_at`

`precedence.status`는 `resolved | unresolved`를 구분해야 하며, unresolved source conflict는 packet에서도 조용히 병합하지 않습니다. `Current`가 plan이나 generated artifact뿐이면 packet의 evidence type도 그대로 남겨, route나 후속 surface가 그것을 implementation proof로 착각하지 않게 합니다.

실제 저장이 필요할 때는 최종 markdown report를 만든 뒤 설치된 TigerKit helper `scripts/tigerkit_state.py`를 호출합니다. `CLAUDE_PLUGIN_ROOT`가 있으면 그것을 우선 쓰고, 없으면 설치된 plugin root를 조회합니다. command 문서는 현재 작업 repo에 TigerKit `scripts/`가 있다고 가정하지 않습니다.

enabled `tk@tiger-kit` install이 이 source checkout보다 오래되어 `draft-paths`, `gap-packet-paths`, `read-gap-packet`, `write-gap-packet` 같은 helper subcommand에서 `invalid choice`가 나오면 먼저 marketplace/plugin을 업데이트하거나, matching checkout/install root를 `CLAUDE_PLUGIN_ROOT`로 지정해야 합니다.

```bash
claude plugin marketplace update tiger-kit
claude plugin install tk@tiger-kit --scope user
```

```bash
TIGERKIT_PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$({ claude plugin list --json | python3 -c 'import json,sys; print(next(item["installPath"] for item in json.load(sys.stdin) if item.get("id") == "tk@tiger-kit" and item.get("enabled")))'; })}"
python3 "$TIGERKIT_PLUGIN_ROOT/scripts/tigerkit_state.py" write-gap --repo-root "$PWD" --report-file /absolute/path/to/final-gap-report.md
```

packet path만 확인하려면:

```bash
TIGERKIT_PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$({ claude plugin list --json | python3 -c 'import json,sys; print(next(item["installPath"] for item in json.load(sys.stdin) if item.get("id") == "tk@tiger-kit" and item.get("enabled")))'; })}"
python3 "$TIGERKIT_PLUGIN_ROOT/scripts/tigerkit_state.py" gap-packet-paths --repo-root "$PWD"
```

현재 same repo/scope packet을 읽으려면:

```bash
TIGERKIT_PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$({ claude plugin list --json | python3 -c 'import json,sys; print(next(item["installPath"] for item in json.load(sys.stdin) if item.get("id") == "tk@tiger-kit" and item.get("enabled")))'; })}"
python3 "$TIGERKIT_PLUGIN_ROOT/scripts/tigerkit_state.py" read-gap-packet --repo-root "$PWD"
```

packet json을 저장하려면:

```bash
TIGERKIT_PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$({ claude plugin list --json | python3 -c 'import json,sys; print(next(item["installPath"] for item in json.load(sys.stdin) if item.get("id") == "tk@tiger-kit" and item.get("enabled")))'; })}"
python3 "$TIGERKIT_PLUGIN_ROOT/scripts/tigerkit_state.py" write-gap-packet --repo-root "$PWD" --packet-file /absolute/path/to/final-gap-packet.json
```

stdin으로 직접 넘길 수도 있습니다.

```bash
TIGERKIT_PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$({ claude plugin list --json | python3 -c 'import json,sys; print(next(item["installPath"] for item in json.load(sys.stdin) if item.get("id") == "tk@tiger-kit" and item.get("enabled")))'; })}"
python3 "$TIGERKIT_PLUGIN_ROOT/scripts/tigerkit_state.py" write-gap --repo-root "$PWD" <<'EOF'
<final gap markdown>
EOF
```

helper는 report archive, `current.md`, `current.packet.json`, `branch-state.json`을 함께 갱신할 수 있습니다.

## 금지

- workflow 생성
- workflow freezing
- advisor/runner/autopilot 구조
- finding이 0개가 될 때까지 반복
- 검증 없는 success 선언
- commit, push, PR, deploy, external write side effect
