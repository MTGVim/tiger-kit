---
description: SoT와 현재 구현의 차이를 구현 전에 한 번 점검하는 분석 명령입니다.
argument-hint: "[SoT refs or pasted source] [--target <path|area>] [--print-report]"
---

이 문서는 TigerKit `/tk:gap` 명령 계약을 정의합니다.

사용자에게는 한글로 답합니다. 코드, path, URL, ticket, commit, hash, identifier, error, contract field name은 증거 보존을 위해 원문 그대로 둘 수 있습니다.

목표: `/tk:gap`은 Source of Truth와 Current Implementation을 한 번 비교해 핵심 차이를 드러내는 명령입니다.

이 명령은 workflow를 생성하거나 고정하지 않습니다.

```text
gap = source of truth ↔ current implementation one-shot comparison
```

## Core guidance

- SoT가 있으면 구현 전에 `/tk:gap`을 먼저 고려합니다.
- SoT가 없으면 추측 대신 먼저 SoT 제공을 제안합니다.
- 사용자가 바로 진행을 원하면 `/tk:gap` 없이 진행할 수 있지만, 그 경우 가정과 불확실성을 명시합니다.

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
7. 모호한 source를 조용히 병합하지 않습니다.

## Priority

- `P0`: core task 불가능, 권한/보안/데이터 무결성/파괴적 동작 위험.
- `P1`: 핵심 사용자 흐름, business rule, validation, error/loading/empty state, CTA 이해에 큰 영향.
- `P2`: visible consistency, 정보 위계, design-system consistency 약화.
- `P3`: minor polish. 기본 finding에는 넣지 않고 필요하면 Not accepted summary에만 둡니다.

## Output

```md
## Gap Summary

| Area | SoT | Current | Gap | Impact | Priority |
|---|---|---|---|---|---|

## Findings

### 1. <finding title>
- SoT:
- Current:
- Evidence:
- Evidence type:
- Impact:
- Priority:
- Suggested fix:

## Ambiguities / Missing Evidence

| Ref | Question | Evidence checked | Impact | Recommendation |
|---|---|---|---|---|

## Not accepted summary

- <optional low-priority or rejected note>

## Recommended Next Steps

1. <next step>
```

Findings에는 P0/P1/P2만 넣습니다. P3, duplicate, unverifiable, source conflict, missing evidence는 의사결정 가치가 낮거나 근거가 약하므로 Findings가 아니라 Ambiguities 또는 Not accepted summary에 둡니다.

## Artifact policy

사용자가 저장을 명시하거나 command contract가 저장을 요구할 때만 external generated report를 씁니다. 새 write path는 project repository 밖 `~/.tigerkit/`입니다.

```text
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/GAP-YYYYMMDD-HHmmss-RAND.md
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/current.md
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/branch-state.json
```

실제 저장이 필요할 때는 최종 markdown report를 만든 뒤 아래 helper를 사용합니다.

```bash
python3 scripts/tigerkit_state.py write-gap --repo-root "$PWD" --report-file /absolute/path/to/final-gap-report.md
```

stdin으로 직접 넘길 수도 있습니다.

```bash
python3 scripts/tigerkit_state.py write-gap --repo-root "$PWD" <<'EOF'
<final gap markdown>
EOF
```

helper는 report archive, `current.md`, `branch-state.json`을 함께 갱신합니다.

기존 `.claude/tigerkit/branches/<scope-key>/gap/` report는 migration context로 읽을 수 있지만 새 report write path로 사용하지 않습니다.

## 금지

- workflow 생성
- workflow freezing
- advisor/runner/autopilot 구조
- finding이 0개가 될 때까지 반복
- 검증 없는 success 선언
- commit, push, PR, deploy, external write side effect
