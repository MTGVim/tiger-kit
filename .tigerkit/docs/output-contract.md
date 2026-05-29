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

- 목적: basis와 target을 비교해 gap analysis 또는 PR-ready basis-target gap comment를 생성합니다.
- basis는 현재 비교에 쓰는 자료이며 Spec reference를 포함할 수 있고, 절대적 진실로 단정하지 않습니다.
- 허용 mode: `analysis`, `review`, `both`
- `mode=analysis`: compact `## Summary Table`, `## Findings`, `## Bottom Recap`만 출력합니다. 상단 summary는 table이어야 하며, 하단 recap은 긴 Findings 뒤에 핵심 count와 next action을 반복합니다.
- `mode=review`: PR에 바로 붙일 수 있는 basis-target gap comment만 출력합니다. 일반 code review가 아닙니다.
- `mode=both`: analysis 형식 뒤에 basis-target gap comment를 이어서 출력하며 같은 finding에는 같은 stable ID를 사용합니다.
- visible UI copy 차이는 exact match 기준으로 판단합니다. 의미상 유사함은 충분하지 않습니다.
- basis끼리 충돌하면 Status `conflicting_sources`로 기록합니다.
- 근거가 부족하거나 target state를 재현할 수 없으면 Type `unverifiable`, Status `cannot_verify`를 사용합니다.
- 접근할 수 없는 외부 URL, image, Figma/design link, screenshot URL, local path는 Type `unverifiable`, Status `blocked_external`로 기록합니다.
- clean working tree가 아니어도 관측 가능한 baseline이 있으면 분석은 진행할 수 있습니다. 다만 재현 불가 상태는 `cannot_verify`로 둡니다.
- ambiguity가 있으면 먼저 code, docs, similar implementation, repo rules, reuse-map을 더 탐색하고, 그래도 불명확할 때만 질문합니다.
- 질문은 recommendation과 evidence를 포함하고 `implementation-blocking` 또는 `reference-only`로 구분합니다.
- Judgment는 더 이상 출력 축으로 사용하지 않습니다.

### Ambiguity Handling

아래 조건 중 하나라도 있으면 조용히 결정하지 않습니다.

1. requirements document와 code가 충돌합니다.
2. 2개 이상의 유사 구현이 서로 다른 pattern을 사용합니다.
3. Spec reference 또는 source basis에 접근할 수 없습니다.
4. reuse-map에 entry가 없고 repo-wide exploration이 아직 충분하지 않습니다.
5. UI/UX intent를 copy나 screenshot만으로 확인할 수 없습니다.
6. API response, DTO, permission, state transition이 불명확합니다.
7. 변경 범위가 common module에 영향을 줄 수 있습니다.

처리 규칙:

- 먼저 관측 가능한 code/docs/similar implementation/repo rules/reuse-map을 더 확인합니다.
- 불명확성이 남으면 `cannot_verify`, `conflicting_sources`, `blocked_external` 중 맞는 Status로 Findings에 남깁니다.
- `mode=analysis`에서는 별도 Open Questions 섹션을 만들지 않고 단일 Findings table 안에 질문 구분, recommendation, evidence를 포함합니다.
- `mode=review`에서는 confirmed defect가 아니라 확인 요청으로 작성하고 `Ask:`에 질문 구분, recommendation, evidence를 포함합니다.

### Taxonomy

아래 값만 사용합니다.

Type:

- `missing`: basis에 있는 요구, UI, 동작, 검증, 접근성, 산출물이 target에 없음
- `mismatch`: basis와 target이 서로 다름
- `convention`: repo convention, `.claude/rules/*`, reuse/component/API 규칙 위반
- `unverifiable`: 근거 부족, 접근 불가, 재현 불가로 확인할 수 없음
- `out_of_scope`: 현재 요청 scope 밖임

Severity:

- `critical`: 핵심 업무 흐름, 데이터 손실, 보안/권한, 결제/정산, 법무/승인, destructive action에 직접 영향
- `major`: 요구 충족, 사용자 이해, 운영 품질, 회귀 위험에 의미 있는 영향
- `minor`: 국소적 copy, 보조 UI, 낮은 위험의 convention 또는 후속 확인 항목

Status:

- `needs_fix`: basis와 target을 비교한 결과 수정이 필요함
- `cannot_verify`: 증거가 부족하거나 재현할 수 없어 판정할 수 없음
- `conflicting_sources`: basis끼리 충돌함
- `blocked_external`: 외부 근거에 접근할 수 없어 사용자 제공 자료가 필요함
- `out_of_scope`: 현재 요청 범위 밖임

Type은 finding의 성격, Severity는 영향도, Status는 처리 상태입니다.

### Stable Finding ID

finding ID는 안정적인 slug를 사용합니다.

```text
gap-<scope-slug>-<finding-slug>
```

규칙:

- 같은 scope와 같은 finding은 `mode=analysis`, `mode=review`, `mode=both`에서 같은 ID를 사용합니다.
- `GAP-001` 같은 순번 기반 finding ID를 만들지 않습니다.
- scope slug는 사람이 읽는 scope label에서 만들고, finding slug는 관측된 문제의 핵심 명사구에서 만듭니다.
- Scope label은 섹션 번호만 쓰지 않습니다. 사람이 읽을 수 있는 title, menu, page, component, row 이름을 포함합니다.
- 좋은 Scope label 예: `§3.2 Summary Row`, `Settings > Billing Page`, `Login Modal Confirm Button`.
- 나쁜 Scope label 예: `§3.2`, `3.2`, `row 4`.

### `mode=analysis` 형식

출력은 summary-first compact analysis만 생성합니다. H2는 아래 세 개만 사용합니다.

```md
## Summary Table

| Basis | Target | Total Findings | Needs Fix | Cannot Verify | Blocked External | Key Next Action |
|---|---|---:|---:|---:|---:|---|
| spec <reference> | current implementation | 3 | 2 | 1 | 0 | needs_fix 2건을 먼저 반영해 주세요. |

## Findings

| ID | Scope | Type | Severity | Status | Basis | Target Evidence | Finding | Suggested Action |
|---|---|---|---|---|---|---|---|---|
| gap-summary-row-missing-total | §3.2 Summary Row | missing | major | needs_fix | spec §3.2 `Total` row | `src/...`에서 해당 row 미관측 | Summary Row의 `Total` row가 없습니다. | basis에 맞춰 row를 추가해 주세요. |

## Bottom Recap
- Needs fix: 2
- Cannot verify: 1
- Key next action: needs_fix 2건을 먼저 반영해 주세요.
```

규칙:

- Summary Table은 반드시 table입니다. 긴 Findings가 이어지기 전에 전체 count와 핵심 next action을 보여줍니다.
- Findings table은 단일 table입니다. 별도 보조 섹션이나 구형 multi-section template을 만들지 않습니다.
- Bottom Recap은 긴 Findings 뒤에서도 사용자가 결론을 다시 볼 수 있도록 Summary Table의 핵심 count와 next action을 반복합니다.
- open question, 추가 증거 요청, 범위 밖 항목도 필요하면 같은 table에 Status로 표현합니다.
- Scope 칸은 반드시 사람이 읽을 수 있는 title, menu, page, component, row 이름을 포함합니다.
- Evidence, Interpretation, Decision, Suggestion 구분은 table 안의 Basis, Target Evidence, Finding, Suggested Action 표현에서 유지합니다.

### `mode=review` 형식

출력은 PR에 바로 붙일 수 있는 basis-target gap comment만 생성합니다. 일반 code review가 아닙니다. 설명문, 서론, 분석 본문을 덧붙이지 않습니다.

```md
[major] gap-summary-row-copy-save-button | mismatch | needs_fix
Scope: §3.2 Summary Row
Basis: spec §3.2의 button label은 `저장`입니다.
Evidence: `src/...`의 버튼 텍스트가 `저장`이 아니라 `확인`입니다.
Why: visible copy는 exact match 기준이라 의미가 비슷해도 허용되지 않습니다.
Ask: spec 기준으로 문구를 exact match로 맞춰 주세요.
```

규칙:

- 첫 줄은 `[severity] stable-id | type | status` 형식입니다.
- 첫 줄에는 Severity, stable ID, Type, Status가 모두 있어야 합니다.
- 본문은 `Scope:`, `Basis:`, `Evidence:`, `Why:`, `Ask:` 순서를 지킵니다.
- `Scope:`는 반드시 사람이 읽을 수 있는 title, menu, page, component, row 이름을 포함합니다.
- speculative finding은 confirmed defect처럼 쓰지 말고 Status를 `cannot_verify`, `conflicting_sources`, `blocked_external`, `out_of_scope` 중 맞는 값으로 둡니다.

### `mode=both` 형식

순서:

1. `mode=analysis` 형식, 즉 `## Summary Table`, `## Findings`, `## Bottom Recap`
2. `mode=review` basis-target gap comment 묶음

규칙:

- analysis table과 basis-target gap comment는 같은 finding에 같은 stable ID를 사용합니다.
- basis-target gap comment는 analysis에서 Status `needs_fix`인 항목을 우선 작성합니다.
- `cannot_verify`, `conflicting_sources`, `blocked_external`, `out_of_scope` 항목을 basis-target gap comment로 포함해야 한다면 confirmed defect가 아니라 확인 요청으로 작성합니다.

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

## `/tk:meta-feedback` Output Contract

- 목적: TigerKit command 또는 skill 사용 friction을 프로젝트 자산 유출 없이 일반화된 TigerKit 개선안으로 정리합니다.
- 기본값은 proposal-only입니다.
- `--out <path>`가 있을 때만 파일을 작성할 수 있습니다.
- chat output과 file output은 모두 같은 redacted format이어야 합니다.
- raw session evidence, 사용자 원문 quote, repo 이름, product 이름, 도메인 고유명, 내부 path, URL, ticket, branch, PR 번호, commit hash를 출력하지 않습니다.
- 증거는 `source_type=session_correction`, `source_type=repeated_friction`, `source_type=output_shape_feedback` 같은 class로만 표시합니다.
- 안전하게 일반화할 수 없으면 `cannot_generalize_safely`로 중단합니다.

필수 섹션 순서:

```md
## Meta Feedback Summary
- Target: <skill-or-command>
- Feedback class: <ux|output-format|taxonomy|safety|dispatch|docs>
- Privacy status: generalized

## Generalized Friction
- Situation: <generic situation>
- Problem: <generic problem>
- Impact: <generic impact>

## Proposed Improvement
- Change: <generic skill/command improvement>
- Why: <reason without project-specific evidence>

## Redaction Receipt
- Removed: <repo names|paths|URLs|domain labels|quoted user text>
- Kept: <abstract pattern only>
- Unsafe details included: none
```

중단 시에는 `Privacy status: cannot_generalize_safely`, `Change: none`, `Why: privacy gate failed`를 사용합니다.

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
