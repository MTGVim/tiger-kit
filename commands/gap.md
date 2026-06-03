---
description: Product/Design Spec contract와 현재 구현/계획을 비교해 branch-local Contract-based Gap Review를 생성합니다.
argument-hint: "[--lite|--strict] [--spec <SP-ID|path>] [--no-specs] [--print-report]"
---

이 명령은 TigerKit v7.2 Contract-based Gap Review contract를 따릅니다.

사용자에게는 한글로 답합니다. 코드, path, URL, ticket, commit, hash, identifier, error는 원문 그대로 둘 수 있습니다.

목표: `/tk:gap`은 현재 브랜치의 Product/Design Spec, implementation plan, current implementation을 비교해 수정 가치가 있는 actionable finding만 도출하고 branch-local run artifact로 저장합니다.

```text
gap = branch-local contract-based inspection + judge-driven final finding
```

## Command surface

- plugin slash invocation은 `/tk:gap`입니다.
- `tiger-kit gap` CLI 표현은 이 plugin command의 사용자 관점 alias로 취급합니다.
- `--legacy`, `TIGERKIT_GAP_LEGACY`, `--deep`, `--no-strict`는 active v7.2 mode가 아닙니다.
- v6-era legacy behavior는 미지원 과거 동작입니다. `lite`의 별칭이나 계승 mode로 표현하지 않습니다.
- legacy Figma diff style은 정식 사용자 모드가 아닙니다.

## 핵심 원칙

- Product/Design Spec 기반 inspection입니다.
- basis는 현재 비교 자료이며 절대적 진실이 아닙니다.
- subagent는 candidate만 생성합니다.
- JudgeMergerAgent만 final finding을 확정합니다.
- final accepted finding에는 P0/P1/P2만 포함합니다.
- P3/nit/duplicate/unverifiable/source_conflict는 final finding이 아닙니다.
- current implementation 비교 전에는 integration branch freshness를 확인합니다.
- `/tk:gap`은 discovery depth와 verification strength를 추천하고, 기본은 추천 preset으로 자동 진행합니다.
- `lite`와 `strict`는 agent 유무가 아니라 discovery depth와 verification strength의 preset 차이입니다.
- 사용자가 files/scope를 명시하지 않는 기본 흐름은 issue ticket, design node link, screenshot, pasted notes 같은 user-provided references에서 target hints를 추출합니다.
- changed files는 primary scope가 아니라 Current Implementation 후보 evidence입니다.
- Product Spec, Design Spec, API contract, source priority, owner decision의 ambiguity는 명확해 보여도 user consent 전에는 confirmed contract로 승격하지 않습니다.
- visible UI copy는 confirmed contract와 exact match가 필요합니다.
- finding이 안 나올 때까지 반복하지 않습니다.
- strict red-team pass는 최대 1회입니다.
- stdout은 summary만 출력하고 상세는 report.md에 저장합니다.
- run summary와 report에는 다른 preset으로 재실행 가능한 rerun trail을 남깁니다.

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

`input-manifest.json`과 `judge-result.json`에는 `mode`, `strictExecuted`, `recommendedMode`, `recommendationReasons`, `discoveryDepth`, `verificationStrength`, `dispatchSkips`, `blockedClarifications`, `rerunTrail`을 반드시 기록합니다.

`.claude/tigerkit/`은 generated branch-local working memory이며 repo-wide durable knowledge가 아닙니다.

## CLI options

- default: preflight skim 후 preset recommendation을 출력하고 추천 preset으로 자동 실행합니다. 보통 작은/저위험 scope는 `lite`입니다.
- `--lite`: 빠른 contract-based gap preset. reference hint 중심 bounded target resolver와 bounded usage lookup을 사용합니다.
- `--strict`: 확장 contract-based gap preset. 더 넓은 source discovery와 verification을 수행하고 `CriticalRedTeamAgent`를 1회 실행합니다.
- `--spec <SP-ID>`: current branch scope의 `specs/index.json`에서만 resolve
- `--spec <path>`: current worktree root 내부 path만 허용
- `--no-specs`: active Spec Patch 자동 참조 비활성화
- `--print-report`: 저장된 report.md 본문을 stdout에도 출력

`--legacy`, `TIGERKIT_GAP_LEGACY`, `--deep`, `--no-strict`는 active v7.2 mode가 아닙니다. v6-era legacy behavior는 미지원 과거 동작이며 `lite`의 별칭이 아닙니다.

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

### Agent dispatch gate

`lite`와 `strict` 모두 source/plan 부재 시 불필요한 agent를 실행하지 않습니다.

- Product source가 없으면 ProductContractAgent를 skip합니다.
- Design 또는 Design System source가 없으면 DesignContractAgent를 skip합니다.
- Implementation Plan이 없으면 PlanCoverageAgent를 skip합니다.
- Current Implementation이 식별되지 않으면 ImplementationComplianceAgent는 관련 candidate를 `unverifiable` 또는 `missing_evidence`로만 처리합니다.
- JudgeMergerAgent는 항상 실행해 accepted/rejected/source conflict/blocked clarification을 확정합니다.
- `--strict`에서만 CriticalRedTeamAgent를 1회 실행합니다.
- 모든 skip은 `input-manifest.json` 또는 `judge-result.json`의 `dispatchSkips`에 agent, reason, sourceClass를 기록합니다.

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

## ClarificationNeeded schema

ClarificationNeeded entries are not final findings. They temporarily block only the ambiguous finding path, not the whole run.

```text
ClarificationNeeded = {
  id: CLAR-YYYYMMDD-HHmmss-RAND-NN,
  category: implementation-blocking | reference-only,
  question,
  options: string[],
  evidence: string[],
  impact,
  recommendation,
  status: blocked_pending_user | blocked_pending_owner | reference_only
}
```

UI clarification should use a compact option table. When a visual decision is needed, add a TUI/ASCII prototype. Right borders must align; account for Korean full-width glyphs and padding.

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

## Target scope and source discovery

사용자는 files/scope를 명시하지 않는 경우가 많습니다. `/tk:gap`은 아래 순서로 target을 좁힙니다.

1. user-provided references: issue ticket, design node link, PRD/doc link, screenshot/export, pasted notes
2. target hints: screen name, route/path, component name, feature name, copy string, API/DTO/event name, design node/frame name
3. repo mapping: route registry, component index, command manifest, repo rules, reuse docs, filename/name search
4. changed files: base branch diff 또는 local dirty files. primary scope가 아니라 Current Implementation 후보 evidence입니다.

`lite` discovery:

- user-provided references와 active confirmed Spec Patch refs를 우선합니다.
- target hints와 직접 매칭되는 Current Implementation을 찾습니다.
- target 주변 1-depth 또는 대표 usage 1-3개만 확인합니다.
- broad repo-wide exhaustive scan, history/PR/과거 구현 탐색, 대규모 design-system 전수조사는 하지 않습니다.

`strict` discovery:

- `lite` seed에서 시작해 관련 docs/rules/similar implementations/shared component 영향 범위까지 확장합니다.
- validation, permission, auth, payment, data mutation, persistence, state transition edge case를 더 확인합니다.
- 그래도 source/plan class가 없으면 관련 agent는 dispatch gate에 따라 skip합니다.

외부 reference가 접근 불가하면 pending reference로 기록하고 file, screenshot/export, pasted content를 요청합니다. 관측 가능한 repo evidence가 있으면 그 범위만 비교하고, 모호한 판단은 clarification으로 둡니다.

## Target freshness preflight

Current Implementation이 current branch, current working tree, local checkout을 뜻하면 비교 전에 integration branch freshness를 확인합니다.

- repository default remote branch를 식별합니다. 이 저장소 convention은 `origin/main`입니다.
- 가능하면 remote metadata를 refresh 또는 verify합니다.
- local `HEAD`가 integration branch tip보다 behind이면 requested scope 또는 target evidence 파일이 `HEAD..integration` 사이에서 바뀌었는지 확인합니다.
- behind changes가 target area에 영향을 주면 stale checkout을 target으로 삼지 않고 integration branch tip shape를 비교 기준으로 보고합니다.
- 사용자가 특정 commit, branch, PR diff, working tree state를 target으로 고정하면 target을 전환하지 않고 stale 여부만 evidence로 기록합니다.

## Lite / strict preset recommendation

`/tk:gap` 기본 호출은 먼저 user-provided references, target hints, current implementation 후보, 위험 신호를 짧게 skim하고 execution preset을 결정합니다.

Preset은 두 축의 조합입니다.

- discovery depth: target/source를 얼마나 넓게 찾는지
- verification strength: finding을 얼마나 강하게 반박/재검증하는지

기본 성향은 보수적으로 `strict`입니다. `lite`는 side-effect confidence가 아주 높을 때만 추천합니다.

Preset score:

```text
riskScore: 0..100
sideEffectConfidence: 0..100

if hardStrictTrigger exists:
  recommendedPreset = strict
else if sideEffectConfidence >= 90 and riskScore <= 15:
  recommendedPreset = lite
else:
  recommendedPreset = strict
```

Hard strict trigger:

- BE/API/DTO/persistence/state transition
- auth/permission/payment/data mutation/destructive action
- shared component 또는 design-system component
- source conflict 또는 implementation-blocking clarification
- inaccessible source reference
- 모호한 Product/API/Design decision
- 2+ similar implementations with different patterns
- cross-module impact
- 신규 화면 또는 신규 flow 개발
- release gate context
- `accepted_or_candidate_P0_exists`

Lite 허용 조건은 전부 만족해야 합니다.

- source reference가 issue/ticket/design note 1개 수준
- FE-only 또는 copy/layout/simple validation 변경
- single screen/component 영향
- API/DTO/state transition 없음
- auth/permission/payment/data mutation/destructive action 없음
- shared component/design-system component 영향 없음
- ambiguity 없음
- sideEffectConfidence >= 90
- riskScore <= 15

Preset rule:

```text
if --strict: mode = strict; strictExecuted = true
else if --lite: mode = lite; strictExecuted = false
else: mode = recommendedPreset; strictExecuted = (recommendedPreset == strict)
```

`/tk:gap`은 실행 preset으로 자동 진행합니다. stdout은 기본적으로 실행 preset과 이유만 표시합니다. 추천 preset은 실행 preset과 다를 때만 추가 노출합니다. 실행 후에는 더 깊거나 다른 preset으로 재실행할 수 있는 `rerunTrail`을 남깁니다.

일반 출력 예:

```text
실행 preset: strict
이유: side-effect confidence 72 < 90이라 expanded discovery와 red-team 검증이 필요합니다.
Discovery depth: expanded
Verification strength: red-team
상태: strict preset 기준 완료
```

lite 예외 출력 예:

```text
실행 preset: lite
이유: FE-only copy change, single screen, side-effect confidence 94, risk score 8입니다.
Discovery depth: bounded
Verification strength: standard
상태: lite preset 기준 완료
Rerun: 의심되면 /tk:gap --strict 로 더 넓게 재검토하세요.
```

명시 `--lite`로 실행했는데 strict 추천이면 추천 preset을 추가 노출하고 rerun trail을 남깁니다.

```text
실행 preset: lite
이유: 사용자가 --lite를 명시했습니다.
추천 preset: strict
추천 이유: shared component와 permission 의미가 불명확합니다.
Discovery depth: bounded
Verification strength: standard
상태: lite preset 기준 완료
Rerun: 더 넓은 discovery와 red-team 검증이 필요하면 /tk:gap --strict 로 재실행하세요.
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
4. user-provided references, target hints, current implementation 후보, 위험 신호를 짧게 skim
5. integration branch freshness 확인
6. discovery depth와 verification strength recommendation 평가 및 기록
7. 실행 preset 결정. 명시 option이 없으면 recommended preset으로 자동 진행
8. branch lock 획득
9. `--no-specs`가 없으면 active Spec Patch 로드. `--no-specs`가 있으면 Spec Patch 자동 로드를 생략
10. 실행 preset에 맞춰 Product/Design/Design System/Engineering/QA/Analytics source를 bounded 또는 expanded로 로드
11. Implementation Plan과 Current Implementation 후보 식별
12. source/plan presence manifest 작성
13. Product source가 있으면 ProductContractAgent 실행. 없으면 dispatch skip 기록
14. Design 또는 Design System source가 있으면 DesignContractAgent 실행. 없으면 dispatch skip 기록
15. Spec Patch items를 Contract로 normalize
16. draft/unclear/conflict/superseded contract 제거
17. Implementation Plan이 있으면 PlanCoverageAgent 실행. 없으면 dispatch skip 기록
18. Current Implementation이 있으면 ImplementationComplianceAgent 실행. 없으면 관련 candidate를 `unverifiable` 또는 `missing_evidence`로만 기록
19. JudgeMergerAgent 실행
20. 실행 preset이 `strict`이면 CriticalRedTeamAgent 1회 실행
21. 실행 preset이 `strict`이면 JudgeMergerAgent 재실행
22. ambiguity consent gate에 걸린 항목을 `ClarificationNeeded` 또는 `SourceConflict`로 확정
23. rerun trail 작성
24. run artifact 저장
25. `branch-state.json`에 `lastGapRunId` 기록
26. `global-index.json`에 branch `lastUsedAt` 갱신
27. branch lock 해제
28. stdout summary 출력

## Output

기본 stdout은 summary만 출력합니다.

```text
실행 preset: <lite|strict>
이유: <한글 이유>
Discovery depth: <bounded|expanded>
Verification strength: <standard|red-team>
상태: <lite|strict> preset 기준 완료
추천 preset: <lite|strict, 실행 preset과 다를 때만 출력>
추천 이유: <한글 이유, 실행 preset과 다를 때만 출력>

Gap Review 완료: <GAP-ID>
Branch Scope: <branch-key>
Strict 실행: <yes|no>
Report: .claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/report.md

Findings:
- P0: <count>
- P1: <count>
- P2: <count>

Source Conflicts: <count>
Clarification Needed: <count>
Rejected/Downgraded: <count>
Rerun: <none|/tk:gap --lite|/tk:gap --strict + reason>
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

`## Summary`에는 실행 preset, 실행 이유, discovery depth, verification strength, dispatch skip summary, rerun trail을 포함합니다. 추천 preset은 실행 preset과 다를 때만 포함합니다.

`## Source Conflicts / Clarification Needed`는 implementation-blocking과 reference-only를 구분합니다. 질문은 option/evidence/impact/recommendation/status를 표로 제시합니다. UI 판단이 필요한 경우 오른쪽 border가 정렬된 TUI/ASCII prototype을 함께 둡니다.

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
