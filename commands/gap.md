---
description: Product/Design Spec contract와 현재 구현/계획을 비교해 branch-local Contract-based Gap Review를 생성합니다.
argument-hint: "[--strict|--no-strict] [--spec <SP-ID|path>] [--no-specs] [--legacy] [--print-report]"
---

이 명령은 TigerKit v7 Contract-based Gap Review contract를 따릅니다.

사용자에게는 한글로 답합니다. 코드, path, URL, ticket, commit, hash, identifier, error는 원문 그대로 둘 수 있습니다.

목표: `/tk:gap`은 현재 브랜치의 Product/Design Spec, implementation plan, current implementation을 비교해 수정 가치가 있는 actionable finding만 도출하고 branch-local run artifact로 저장합니다.

```text
gap = branch-local contract-based inspection + judge-driven final finding
```

## Command surface

- plugin slash invocation은 `/tk:gap`입니다.
- `tiger-kit gap` CLI 표현은 이 plugin command의 사용자 관점 alias로 취급합니다.
- legacy Figma diff style은 정식 사용자 모드가 아닙니다.

## 핵심 원칙

- Product/Design Spec 기반 inspection입니다.
- basis는 현재 비교 자료이며 절대적 진실이 아닙니다.
- subagent는 candidate만 생성합니다.
- JudgeMergerAgent만 final finding을 확정합니다.
- final accepted finding에는 P0/P1/P2만 포함합니다.
- P3/nit/duplicate/unverifiable/source_conflict는 final finding이 아닙니다.
- current implementation 비교 전에는 integration branch freshness를 확인합니다.
- visible UI copy는 confirmed contract와 exact match가 필요합니다.
- finding이 안 나올 때까지 반복하지 않습니다.
- strict red-team pass는 최대 1회입니다.
- stdout은 summary만 출력하고 상세는 report.md에 저장합니다.

## Terminology

내부 개념은 source tool 이름이 아니라 spec class로 부릅니다.

| Source 예 | 내부 개념 |
| --- | --- |
| PRD, ticket, ad-hoc instruction | Product Spec |
| design file, design guide, screenshot, design feedback | Design Spec |
| design system docs | Design System Spec |
| implementation plan | Implementation Plan |
| current code/rendering | Current Implementation |

권장 표현:

- Product Spec
- Design Spec
- Design System Spec
- Spec Patch
- Contract-based Gap Review
- Actionable Finding

금지 표현:

- Figma gap
- Figma diff
- PRD review skill
- Design review skill

## Branch-local storage

반드시 current worktree root 아래에 저장합니다.

```text
.claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/
```

필수 파일:

```text
input-manifest.json
contracts.json
candidates.json
judge-result.json
report.md
```

`input-manifest.json`과 `judge-result.json`에는 `strictExecuted`와 `autoStrictTriggers`를 반드시 기록합니다.

`.claude/tigerkit/`은 generated branch-local working memory이며 repo-wide durable knowledge가 아닙니다.

## CLI options

- default: auto mode
- `--strict`: default review 후 CriticalRedTeamAgent 1회 실행
- `--no-strict`: risk trigger가 있어도 red-team pass 미실행
- `--spec <SP-ID>`: current branch scope의 `specs/index.json`에서만 resolve
- `--spec <path>`: current worktree root 내부 path만 허용
- `--no-specs`: active Spec Patch 자동 참조 비활성화
- `--legacy`: debug/rollback fallback only
- `--print-report`: 저장된 report.md 본문을 stdout에도 출력

`TIGERKIT_GAP_LEGACY=1`도 debug fallback으로만 허용합니다. legacy 실행 시 v1/v7 공식 경로가 아님을 warning으로 표시합니다.

## Contract schema

Contract는 review 기준으로 쓰는 normalized requirement입니다.

```text
Contract = {
  id,
  source: product | design | design_system | engineering | qa | analytics,
  sourceRef,
  origin,
  type,
  status: confirmed | draft | assumed | unclear | conflict | superseded,
  expected,
  verification,
  severityHint: P0 | P1 | P2 | P3,
  supersedes,
  notes
}
```

Final finding evidence로 사용 가능한 contract는 `confirmed`이고 superseded가 아니어야 합니다.

## Active Spec Patch loading

기본으로 current branch scope에서 아래 조건을 만족하는 Spec Patch item만 contract로 normalize합니다.

- Spec Patch status = `active`
- Spec Item status = `confirmed`
- item ID가 `itemSupersedes`의 old item으로 등록되지 않음

명시 `--spec`으로 draft/conflict patch를 참조하면 warning을 출력하고, confirmed가 아닌 item은 final finding evidence로 쓰지 않습니다.

Spec ID를 찾지 못하면 아래 메시지로 중단합니다.

```text
Spec Patch <SP-ID> was not found in the current branch scope.
Use --spec <path> to reference a file explicitly.
```

## Agents

Default agents:

- ProductContractAgent
- DesignContractAgent
- PlanCoverageAgent
- ImplementationComplianceAgent
- JudgeMergerAgent

Strict 추가 agent:

- CriticalRedTeamAgent

공통 agent rule:

```text
You are not the final judge.
You may only produce structured contracts or candidate findings.
A valid result may contain zero items.
Do not invent issues.
Do not report subjective preferences.
Do not report P3/nit issues unless explicitly requested.
Do not repeat issues already covered by broader candidates.
Every candidate must include concrete evidence and a fix hint.
```

### ProductContractAgent

Product source에서 검증 가능한 Product Contract만 추출합니다. behavior, validation, permission, business_rule, data_behavior, error_handling, empty_state, loading_state, content, analytics를 담당합니다. implementation gap 판단, final finding 생성, final severity 결정을 하지 않습니다.

### DesignContractAgent

Design source에서 검증 가능한 Design Contract만 추출합니다. screen_structure, visual_hierarchy, required_visible_element, interaction_state, responsive, component_composition, design_system, accessibility를 담당합니다. raw Figma diff, 1-2px nit, subjective preference를 생성하지 않습니다.

### PlanCoverageAgent

Implementation Plan이 contract를 커버하는지 비교하고 `plan_gap` candidate만 생성합니다. plan evidence로 확인되는 누락이나 불완전 coverage만 후보가 됩니다.

### ImplementationComplianceAgent

Current Implementation이 contract를 만족하는지 비교하고 `implementation_gap` candidate만 생성합니다. user-visible하지 않은 DOM 구조 차이나 subjective visual preference는 candidate가 아닙니다.

### CriticalRedTeamAgent

strict mode에서 두 가지만 수행합니다.

1. accepted finding의 false positive 공격
2. missed P0/P1 issue 탐색

P2/P3/nit는 보고하지 않습니다. 새 candidate가 0개인 결과도 유효합니다.

### JudgeMergerAgent

final finding을 확정하는 유일한 agent입니다.

각 candidate에 대해:

- evidence 검증
- actionability gate 검증
- severity 분류
- duplicate merge
- P3/nit/unverifiable/source_conflict reject
- P0/P1/P2 actionable finding만 accept

## CandidateFinding schema

```text
CandidateFinding = {
  id: CAND-<KIND>-YYYYMMDD-HHmmss-RAND-NN,
  kind: plan_gap | implementation_gap | red_team_candidate,
  sourceContracts: string[],
  category,
  expected,
  actual,
  evidence: string[],
  proposedSeverity: P0 | P1 | P2 | P3 | unverifiable,
  confidence: low | medium | high,
  fixHint
}
```

Candidate validation:

- `sourceContracts` must not be empty.
- `evidence` must not be empty.
- `expected` must derive from source contracts.
- `actual` must describe plan or implementation state.
- `fixHint` must be implementable without guessing.

## AcceptedFinding schema

```text
AcceptedFinding = {
  id: FND-YYYYMMDD-HHmmss-RAND-NN,
  finalSeverity: P0 | P1 | P2,
  title,
  sourceContracts: string[],
  evidence: string[],
  requiredChange: string[],
  category: string[],
  confidence: medium | high,
  decisionReason
}
```

`finalSeverity` cannot be P3. `confidence` cannot be low.

## RejectedFinding reasons

- `P3_nit`
- `duplicate`
- `unverifiable`
- `source_conflict`
- `not_user_visible`
- `not_actionable`
- `low_confidence`
- `missing_evidence`
- `superseded_source`

## SourceConflict schema

Source conflicts are not final findings.

```text
SourceConflict = {
  id: CONFLICT-YYYYMMDD-HHmmss-RAND-NN,
  involvedContracts: string[],
  summary,
  impact: behavior | validation | permission | content | layout | interaction_state | design_system | unknown,
  decision: clarification_needed,
  reason
}
```

## Judge Actionability Gate

Candidate를 final finding으로 accept하려면 모두 true여야 합니다.

1. user-visible, requirement-relevant, 또는 interaction-affecting입니다.
2. expected result가 Product Spec, Design Spec, Design System Spec, Engineering Constraint, QA Contract, Analytics Contract, 또는 Implementation Plan에서 검증 가능합니다.
3. actual behavior 또는 plan gap이 concrete evidence로 뒷받침됩니다.
4. 엔지니어가 추측 없이 수정할 수 있습니다.
5. 기존 accepted finding의 duplicate 또는 하위 사례가 아닙니다.
6. 수정했을 때 품질 개선이 구현 비용/위험보다 큽니다.
7. source contract가 confirmed이며 superseded가 아닙니다.
8. candidate confidence가 low가 아닙니다.

하나라도 false면 reject 또는 downgrade합니다.

## Severity

- P0: core task 불가능, business rule 위반, permission 위반, validation 누락, invalid data flow, destructive/payment/auth/data mutation correctness 위반
- P1: task completion, 사용자 이해, 핵심 CTA 상태/위치/문구, error/loading/empty state, product correctness content에 큰 영향
- P2: visible layout/consistency mismatch, 정보 위계 약화, design-system consistency 훼손
- P3: minor polish. final finding에 포함하지 않음
- Unverifiable: source에서 기대 결과를 확인할 수 없음. final finding에 포함하지 않음

## UI copy exactness

Visible UI copy는 exact match가 기본입니다.

Exact-match 대상:

- button label
- field label
- placeholder
- helper text
- validation text
- tooltip
- toast/snackbar
- modal title/body
- confirm/cancel/ok text
- table column name
- tab name
- status label
- empty/loading/error text
- date/time/number/currency format
- intended visible line break

공백, 줄바꿈, 구두점, 조사, 접두/접미 표현 차이도 보이는 결과가 다르면 mismatch입니다. 의미가 비슷해도 문자열이 다르면 contract 위반입니다. contract가 variation 허용을 명시한 경우에만 예외를 인정합니다.

## Target freshness preflight

Current Implementation이 current branch, current working tree, local checkout을 뜻하면 비교 전에 integration branch freshness를 확인합니다.

- repository default remote branch를 식별합니다. 이 저장소 convention은 `origin/main`입니다.
- 가능하면 remote metadata를 refresh 또는 verify합니다.
- local `HEAD`가 integration branch tip보다 behind이면 requested scope 또는 target evidence 파일이 `HEAD..integration` 사이에서 바뀌었는지 확인합니다.
- behind changes가 target area에 영향을 주면 stale checkout을 target으로 삼지 않고 integration branch tip shape를 비교 기준으로 보고합니다.
- 사용자가 특정 commit, branch, PR diff, working tree state를 target으로 고정하면 target을 전환하지 않고 stale 여부만 evidence로 기록합니다.

## Auto strict triggers

Auto mode에서 아래 중 하나라도 true면 CriticalRedTeamAgent를 1회 실행합니다.

- `accepted_or_candidate_P0_exists`
- `product_contract_includes_validation`
- `product_contract_includes_permission`
- `product_contract_includes_authentication`
- `product_contract_includes_payment`
- `product_contract_includes_data_mutation`
- `product_contract_includes_destructive_action`
- `product_contract_includes_submit_flow`
- `design_contract_includes_primary_cta`
- `design_contract_includes_error_state`
- `design_contract_includes_empty_state`
- `design_contract_includes_loading_state`
- `design_contract_includes_critical_interaction_state`
- `source_conflict_exists`
- `judge_confidence_below_high`
- `implementation_plan_has_missing_P0_or_P1_coverage`
- `changed_files_count_gte_10`
- `touches_shared_component`
- `touches_design_system_component`
- `review_context_is_release_gate`

Mode rule:

```text
if mode == strict: strictExecuted = true
if mode == no-strict: strictExecuted = false
if mode == auto: strictExecuted = any(autoStrictTrigger == true)
```

## Loop policy

금지:

```text
finding이 안 나올 때까지 반복
```

Default: loop 없음.

Strict: red-team 1회만 수행.

향후 loop가 생겨도 P3, nit, duplicate, unverifiable, source_conflict 때문에 continuation하면 안 됩니다.

## Run procedure

1. current worktree root 계산
2. current branch-key 계산
3. branch scope 초기화
4. branch lock 획득
5. `--no-specs`가 없으면 active Spec Patch 로드. `--no-specs`가 있으면 Spec Patch 자동 로드를 생략
6. Product/Design/Design System/Engineering/QA/Analytics source 로드
7. Implementation Plan 로드
8. Current Implementation 분석
9. ProductContractAgent 실행
10. DesignContractAgent 실행
11. Spec Patch items를 Contract로 normalize
12. draft/unclear/conflict/superseded contract 제거
13. PlanCoverageAgent 실행
14. ImplementationComplianceAgent 실행
15. JudgeMergerAgent 실행
16. auto strict trigger 평가
17. 필요 시 CriticalRedTeamAgent 1회 실행
18. JudgeMergerAgent 재실행
19. run artifact 저장
20. `branch-state.json`에 `lastGapRunId` 기록
21. `global-index.json`에 branch `lastUsedAt` 갱신
22. branch lock 해제
23. stdout summary 출력

## Output

기본 stdout은 summary만 출력합니다.

```text
Gap Review Complete: <GAP-ID>
Branch Scope: <branch-key>
Mode: <auto|strict|no-strict>
Strict Executed: <yes|no>
Report: .claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/report.md

Findings:
- P0: <count>
- P1: <count>
- P2: <count>

Source Conflicts: <count>
Rejected/Downgraded: <count>
```

`--print-report`가 있을 때만 report.md 본문을 함께 출력합니다.

## Report shape

`report.md`는 아래 H2를 사용합니다.

```md
# Tiger Kit Gap Report: <GAP-ID>

## Summary

## Sources Used

## Actionable Findings

## Rejected / Downgraded Observations

## Source Conflicts / Clarification Needed
```

## 금지

- basis를 절대적 진실처럼 단정
- conflict source를 임의 병합
- subagent candidate를 final finding처럼 출력
- P3/nit를 final finding으로 출력
- unverifiable/source_conflict를 final finding으로 출력
- strict red-team을 2회 이상 실행
- finding이 0개가 될 때까지 loop
- default stdout에 전체 report 출력
- `/tmp`, `$GIT_COMMON_DIR`, user home에 gap run 저장
