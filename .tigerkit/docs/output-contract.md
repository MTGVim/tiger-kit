# TigerKit 운영 Output Contract

이 문서는 TigerKit command의 출력 계약을 정의합니다. 사용 흐름은 `.tigerkit/docs/usage.md`, 산출물 위치는 `.tigerkit/docs/artifact-layout.md`를 기준으로 봅니다.

```text
Chat output is the primary receipt. File writes happen only when the command contract allows them.
```

## 원칙

기본 응답은 아래 네 가지에 집중합니다.

1. outcome
2. evidence, risk, ambiguity
3. artifact paths when files are written
4. natural-language next action or required confirmation

상세 보고서는 사용자가 원하거나 command mode가 요구할 때만 출력합니다.

## `/tk:gap` Output Contract

- 목적: basis와 target을 비교해 gap analysis 또는 PR-ready review comment를 생성합니다.
- 허용 mode: `analysis`, `review`, `both`
- `mode=analysis`: 분석 형식을 출력합니다.
- `mode=review`: PR-ready review comment만 출력합니다.
- `mode=both`: 분석 형식 뒤에 review comment를 이어서 출력합니다.
- visible UI copy 차이는 `copy_exact_mismatch`로 기록합니다.
- basis끼리 충돌하면 `conflicting_sources`로 기록합니다.
- 근거가 부족하거나 target state를 재현할 수 없으면 `cannot_verify` judgment 또는 `insufficient_evidence` finding을 사용합니다.
- clean working tree가 아니어도 관측 가능한 baseline이 있으면 분석은 진행할 수 있습니다. 다만 재현 불가 상태는 `cannot_verify`로 둡니다.

### finding type

아래 목록만 사용합니다.

- `copy_exact_mismatch`
- `repo_convention_violation`
- `wrong_component_choice`
- `unsupported_library_usage`
- `missing_requirement`
- `requirement_mismatch`
- `partial_implementation`
- `ambiguous_basis`
- `conflicting_sources`
- `insufficient_evidence`
- `test_gap`
- `accessibility_gap`
- `unknown`

### judgment

아래 목록만 사용합니다.

- `satisfied`
- `partially_satisfied`
- `not_satisfied`
- `cannot_verify`
- `conflicting_sources`
- `out_of_scope`

### severity

아래 목록만 사용합니다.

- `critical`
- `major`
- `minor`
- `info`
- `unknown`

### `mode=analysis` 형식

```md
## Scope
- basis:
- target:
- mode: analysis
- compared areas:
- excluded areas:

## Summary
- overall judgment:
- key risks:
- mode reason: 필요할 때만 짧게

## Findings

| ID | Type | Judgment | Severity | Basis | Target Evidence | Summary | Rule ID | Suggested Action |
|---|---|---|---|---|---|---|---|---|
| GAP-001 | missing_requirement | not_satisfied | major | spec 3.2 | `src/...` | 요구 동작 누락 | RULE-123 또는 빈칸 | 구현 또는 기준자료 확인 |

## Open Questions
- 확인이 더 필요한 항목
- 증거 부족 항목
- 충돌하는 기준자료 항목

## Recommended Next Actions
- 바로 수정 가능한 항목
- 사용자 확인이 필요한 항목
- 추가 증거 확보가 필요한 항목
```

### `mode=review` 형식

```md
[major] copy_exact_mismatch
Basis: spec 3.2
Evidence: `src/...`의 버튼 텍스트가 `저장`이 아니라 `확인`입니다.
Why: visible copy는 exact match 기준이라 의미가 비슷해도 허용되지 않습니다.
Ask: spec 기준으로 문구를 exact match로 맞춰 주세요.
```

규칙:
- 첫 줄은 severity로 시작합니다.
- `Basis`에는 기준자료 근거를 적습니다.
- `Evidence`에는 현재 target 근거를 적습니다.
- `Why`에는 영향이나 mismatch 이유를 적습니다.
- 수정 방향이 명확할 때만 `Ask` 또는 동등한 suggested change를 적습니다.
- speculative finding을 confirmed defect처럼 쓰지 않습니다.

### `mode=both` 형식

순서:
1. `mode=analysis` 형식
2. `mode=review` comment 묶음

## `/tk:reflect` Output Contract

- 목적: durable repo rule candidate를 추출하고 `CLAUDE.md` 또는 `.claude/rules/*` 변경을 제안합니다.
- 기본값은 proposal-only입니다.
- `apply=true` 또는 사용자 명시 승인 전에는 파일을 수정하지 않습니다.
- conflict가 남아 있으면 적용하지 않고 먼저 보고합니다.

필수 섹션 순서:

```md
### Reflect Result
- durable rule candidate 요약
- global rule인지 scoped rule인지 표시
- apply 여부 표시

### Classification
- 각 candidate의 target 분류

### Reason
- evidence 기반 이유

### Proposed Patch
- proposal-only 기본 동작
- apply=false면 실제 수정 대신 patch 제안

### Conflicts
- 충돌, 중복, 우선순위 불명확성

### Follow-up Audit
- 추가 검토 대상과 audit 범위
```

적용했을 때는 수정한 파일 경로와 적용 범위를 짧게 보고합니다. 적용하지 않았을 때는 proposal-only 상태를 명시합니다.

## `/tk:handoff` Output Contract

- 기본 기록 위치: `.claude/handoffs/current.md`
- `archive=true` 또는 사용자 명시 archive 요청이 있을 때만 dated archive를 추가로 만듭니다.
- 섹션 제목은 `commands/handoff.md` template과 정확히 맞춰야 합니다.

```md
# Handoff: <task title>

## Reader Guide

## Mission

## Current State

## Key Decisions

## Relevant Files

## Basis / References

## Completed Work

## Pending Work

## Known Risks / Unknowns

## Failed Attempts / Do Not Repeat

## Validation

## Next Actions

## Resume Prompt
```

채팅 receipt는 작성된 파일, archive 여부, 핵심 next action만 짧게 보고합니다.

## Evidence Rule

중요 판단은 아래 구분을 유지합니다.

```text
Evidence = directly observed
Interpretation = inferred from evidence
Decision = confirmed by user or basis
Suggestion = proposed, not confirmed
```

## detail 원칙

- command별 출력은 필요한 만큼만 작성합니다.
- 다음 행동은 command-style recommendation이 아니라 자연어로 짧게 제시합니다.
- 근거가 부족한 항목은 추측하지 않고 `cannot_verify`로 둡니다.
