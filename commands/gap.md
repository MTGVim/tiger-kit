---
description: Product/Design Spec contract와 현재 구현/계획을 비교해 branch-local Contract-based Gap Review를 생성합니다.
argument-hint: "[--analysis-depth <direct|bounded|expanded|exhaustive-capped>] [--spec <SP-ID|path>] [--no-specs] [--print-report]"
---

이 명령은 TigerKit v7.2.7 Contract-based Gap Review contract를 따릅니다.

사용자에게는 한글로 답합니다. 코드, path, URL, ticket, commit, hash, identifier, error는 원문 그대로 둘 수 있습니다.

목표: `/tk:gap`은 현재 브랜치의 Product/Design Spec, implementation plan, current implementation을 비교해 수정 가치가 있는 actionable finding만 도출하고, missed critical issue를 줄이는 coverage proof와 함께 branch-local run artifact로 저장합니다.

```text
gap = branch-local contract-based inspection + judge-driven final finding
```

## Command surface

- plugin slash invocation은 `/tk:gap`입니다.
- `tiger-kit gap` CLI 표현은 이 plugin command의 사용자 관점 alias로 취급합니다.
- `--lite`와 `--strict`는 compatibility flag로만 기록하며 active v7.2.7 user-facing quality mode가 아닙니다.
- `--legacy`, `TIGERKIT_GAP_LEGACY`, `--deep`, `--no-strict`는 active v7.2.7 mode가 아닙니다.
- v6-era legacy behavior는 미지원 과거 동작입니다. `lite`의 별칭이나 계승 mode로 표현하지 않습니다.
- legacy Figma diff style은 정식 사용자 모드가 아닙니다.

## 핵심 원칙

- Product/Design Spec 기반 inspection입니다.
- basis는 현재 비교 자료이며 절대적 진실이 아닙니다.
- subagent는 candidate만 생성합니다.
- JudgeMergerAgent만 final finding을 확정합니다.
- final accepted finding에는 P0/P1/P2만 포함합니다.
- P3/nit/duplicate/unverifiable/source_conflict는 final finding이 아닙니다.
- candidate의 file:line 또는 module-path evidence는 JudgeMergerAgent queue 진입 전에 현재 target surface에서 read-back으로 재확인합니다.
- producer가 값을 미제공/미커버한다는 claim은 producer 계약, schema, serializer, endpoint response, data model, persistence logic 같은 producer-side evidence 없이는 final finding이나 source_conflict로 승격하지 않습니다.
- current implementation 비교 전에는 integration branch freshness를 확인합니다.
- `/tk:gap`은 하나의 실행으로 동작합니다.
- 속도는 quality mode가 아니라 `analysisDepth`와 `verificationEscalation`으로 제어합니다.
- 모든 final finding은 analysis depth와 관계없이 evidence precision, producer evidence, ambiguity, JudgeMerger gate를 통과해야 합니다.
- missed P0/P1 방지를 위해 source/target coverage, dispatch completeness, CriticalRedTeamAgent missed-critical search 결과를 false-negative proof로 기록합니다.
- `lite`, `strict`, `preset`, `mode`는 현재 동작에서 user-facing quality concept이 아닙니다.
- 사용자가 files/scope를 명시하지 않는 기본 흐름은 issue ticket, design node link, screenshot, pasted notes 같은 user-provided references에서 target hints를 추출합니다.
- changed files는 primary scope가 아니라 Current Implementation 후보 evidence입니다.
- Product Spec, Design Spec, API contract, source priority, owner decision의 ambiguity는 명확해 보여도 user consent 전에는 confirmed contract로 승격하지 않습니다.
- visible UI copy는 confirmed contract와 exact match가 필요합니다.
- finding이 안 나올 때까지 반복하지 않습니다.
- CriticalRedTeamAgent pass는 targeted verification으로 최대 1회입니다.
- stdout은 summary receipt와 compact finding tables만 출력하고 상세는 report.md에 저장합니다.
- 유저향 stdout/report table은 run-local short Ref(`G1`, `R1`, `C1`, `Q1`)를 우선 표시하고 긴 canonical ID는 JSON artifact와 report 상세/참조 영역에 보관합니다.
- run summary와 report에는 analysis depth, 확장 이유, 성능 증명을 남깁니다.

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

`input-manifest.json` 또는 `judge-result.json`에는 `qualityGates`, `analysisDepth`, `depthReasons`, `riskScore`, `sideEffectConfidence`, `verificationEscalation`, `compatibilityFlags`, `dispatchPlan`, `dispatchSkips`, `candidateIntakeGate`, `evidencePrecisionGate`, `targetSurfaceCoverageGate`, `dispatchCompletenessGate`, `blockedClarifications`, `claimFreshnessGate`, `performance`, `heuristicProof`를 반드시 기록합니다. 둘 다에 중복 기록할 필요는 없지만, `report.md`와 stdout은 같은 canonical metadata를 참조해야 합니다.

`.claude/tigerkit/`은 generated branch-local working memory이며 repo-wide durable knowledge가 아닙니다.

## CLI options

- default: 단일 `/tk:gap` 실행으로 실행하고 analysis depth를 휴리스틱으로 결정합니다.
- `--analysis-depth <direct|bounded|expanded|exhaustive-capped>`: 품질 gate를 낮추지 않고 source discovery depth만 명시합니다.
- `--spec <SP-ID>`: current branch scope의 `specs/index.json`에서만 resolve
- `--spec <path>`: current worktree root 내부 path만 허용
- `--no-specs`: active Spec Patch 자동 참조 비활성화
- `--print-report`: 저장된 report.md 본문을 stdout에도 출력

`--lite`와 `--strict`는 compatibility flag로만 기록하고 quality gate를 바꾸지 않습니다. `--legacy`, `TIGERKIT_GAP_LEGACY`, `--deep`, `--no-strict`는 active v7.2.7 mode가 아닙니다. v6-era legacy behavior는 미지원 과거 동작이며 `lite`의 별칭이 아닙니다.

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

Targeted verification agent:

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
Do not omit a P0/P1 candidate because a narrower depth was requested when a hard trigger requires escalation.
When citing file:line or module path evidence, cite a current read-back confirmed span.
```

### Agent dispatch gate

source/plan 부재 시 불필요한 agent를 실행하지 않습니다.

- Source/plan/current implementation presence manifest 직후 `dispatchPlan`을 먼저 고정합니다.
- Product source가 없으면 ProductContractAgent를 skip합니다.
- Design 또는 Design System source가 없으면 DesignContractAgent를 skip합니다.
- Implementation Plan이 없으면 PlanCoverageAgent를 skip합니다.
- Current Implementation이 식별되지 않으면 ImplementationComplianceAgent를 skip하고 관련 observation은 `unverifiable` 또는 `missing_evidence`로만 기록합니다.
- CriticalRedTeamAgent는 would-be accepted 또는 high-risk gated candidate가 있을 때 targeted verification으로 최대 1회 실행합니다.
- JudgeMergerAgent는 final judge queue에 대해 1회 실행해 accepted/rejected/source conflict/blocked clarification을 확정합니다.
- 모든 skip은 `input-manifest.json` 또는 `judge-result.json`의 `dispatchSkips`에 `agent`, `reason`, `sourceClass`, `criticalPathEffect`를 기록합니다. Speed proof에 반영하는 credited skip만 `credited: true`, `criticalPathDelta`, `evidenceCoveragePreserved: true`를 추가로 기록합니다.
- skip된 agent는 `performance.currentCriticalPathScore`의 agent critical path group에서 제외하고, 제외 근거를 `dispatchPlan`과 `performance.agentCriticalPathGroups`에 함께 남깁니다.

### ProductContractAgent

Product source에서 검증 가능한 Product Contract만 추출합니다. behavior, validation, permission, business_rule, data_behavior, error_handling, empty_state, loading_state, content, analytics를 담당합니다. implementation gap 판단, final finding 생성, final severity 결정을 하지 않습니다.

### DesignContractAgent

Design source에서 검증 가능한 Design Contract만 추출합니다. screen_structure, visual_hierarchy, required_visible_element, interaction_state, responsive, component_composition, design_system, accessibility를 담당합니다. raw Figma diff, 1-2px nit, subjective preference를 생성하지 않습니다.

### PlanCoverageAgent

Implementation Plan이 contract를 커버하는지 비교하고 `plan_gap` candidate만 생성합니다. plan evidence로 확인되는 누락이나 불완전 coverage만 후보가 됩니다.

### ImplementationComplianceAgent

Current Implementation이 contract를 만족하는지 비교하고 `implementation_gap` candidate만 생성합니다. user-visible하지 않은 DOM 구조 차이나 subjective visual preference는 candidate가 아닙니다.

### CriticalRedTeamAgent

targeted verification에서 두 가지만 수행합니다.

1. would-be accepted 또는 high-risk gated candidate의 false positive 공격
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
  displayRef?: R<N>,
  kind: plan_gap | implementation_gap | red_team_candidate,
  sourceContracts: string[],
  category,
  expected,
  actual,
  evidence: string[],
  evidenceRefs?: EvidenceRef[],
  producerAbsenceClaim?: boolean,
  proposedSeverity: P0 | P1 | P2 | P3 | unverifiable,
  confidence: low | medium | high,
  fixHint,
  intakeGate?: CandidateIntakeGateResult
}

EvidenceRef = {
  ref,
  kind: file_line | module_path | contract | producer_surface | rendered_output | owner_confirmed,
  claimRole: expected | actual | producer_absence | conflict | fix_hint,
  readBackStatus: pending | confirmed | repaired | missing,
  repairedRef?,
  precisionReason
}

CandidateIntakeGateResult = {
  shape: pass | reject | downgrade,
  evidencePrecision: pass | repair | reject | downgrade,
  producerEvidence: pass | reject | downgrade | not_applicable,
  conflictClarification: pass | blocked,
  requirementTraceability: pass | reject | downgrade,
  severityScope: pass | reject | downgrade,
  finalQueue: judge | rejected | source_conflict | clarification_needed,
  reasons: string[]
}

HeuristicProof = {
  requiredImprovementRatio: 1.3,
  falsePositive: {
    metric: accepted_path_blocking_predicate_coverage,
    denominator: required_false_positive_predicates,
    baselinePredicateScore,
    currentPredicateScore,
    improvementRatio,
    claimAllowed
  },
  falseNegative: {
    metric: critical_contract_and_target_surface_coverage,
    denominator: required_false_negative_predicates,
    baselinePredicateScore,
    currentPredicateScore,
    improvementRatio,
    claimAllowed
  },
  speed: {
    metric: contract_critical_path_score,
    denominator: baselineCriticalPathScore,
    baselineCriticalPathScore,
    currentCriticalPathScore,
    improvementRatio,
    claimAllowed
  },
  analysisDepth: {
    metric: hard_trigger_selection_coverage,
    denominator: required_depth_trigger_predicates,
    baselineTriggerCoverage,
    currentTriggerCoverage,
    improvementRatio,
    claimAllowed
  },
  claimAllowed: boolean
}
```

Heuristic proof metrics use fixed denominators from this contract, not ad-hoc run scoring.

- `falsePositive.baselinePredicateScore` and `currentPredicateScore` count covered accepted-path blocking predicates from CandidateShapeGate, EvidencePrecisionGate, ProducerEvidenceGate, ConflictClarificationGate, RequirementTraceabilityGate, SeverityScopeGate, and JudgeMergerAgent. Current v7.2.7 must score all seven; baseline v7.2.5 scores five because requirement traceability and severity scope were embedded in broader gates, not separately blocked before Judge.
- `falseNegative.baselinePredicateScore` and `currentPredicateScore` count covered missed-critical prevention predicates from SourcePresenceManifest, ActiveSpecPatchCoverage, TargetHintExtraction, TargetSurfaceCoverageGate, DispatchCompletenessGate, and CriticalRedTeamAgent missed-P0/P1 search. Current v7.2.7 must score all six; baseline v7.2.5 scores four because it lacks explicit TargetSurfaceCoverageGate and DispatchCompletenessGate.
- `speed` uses the critical path formula in Performance measurement contract.
- `analysisDepth.baselineTriggerCoverage` and `currentTriggerCoverage` count covered depth trigger predicates from direct/bounded/expanded/exhaustive-capped selection rules, requested-depth escalation, post-candidate P0/P1 escalation, target-surface depth backstop, and dispatch-completeness depth backstop. Current v7.2.7 must score eight; baseline v7.2.5 scores six because it lacks the target-surface and dispatch-completeness backstops. Hard triggers must be covered before risk-score tie-breaker coverage can count.
- ClaimFreshnessGate is a separate claim gate, not a score denominator. It can block `heuristicProof.claimAllowed`, but it does not inflate false-positive, false-negative, or analysis-depth ratios.

Contract-level improvement proof target:

```text
falsePositive: baselinePredicateScore = 5, currentPredicateScore = 7, improvementRatio = 7 / 5 = 1.40
falseNegative: baselinePredicateScore = 4, currentPredicateScore = 6, improvementRatio = 6 / 4 = 1.50
speed: baselineCriticalPathScore = 87.1, currentCriticalPathScore <= 51.6, improvementRatio >= 87.1 / 51.6 = 1.69
analysisDepth: baselineTriggerCoverage = 6, currentTriggerCoverage = 8, improvementRatio = 8 / 6 = 1.33
```

Combined claim requires every ratio above to be recomputed from actual run metadata and remain `>= 1.3`.

## Candidate Intake Gate

Before any candidate enters JudgeMergerAgent, run deterministic gates and record the result.

### CandidateShapeGate

Reject or downgrade before Judge when any required candidate field is missing:

- no confirmed, non-superseded `sourceContracts`
- no concrete `evidence`
- `expected` cannot be traced to a confirmed contract
- `actual` is a guess rather than observed plan or implementation state
- `fixHint` requires guessing or is not actionable

Allowed rejected reasons: `missing_evidence`, `not_actionable`, `unverifiable`, `low_confidence`.

### EvidencePrecisionGate

For every file:line or module-path evidence coordinate:

- read back the current target surface
- confirm the cited span supports the candidate claim
- repair stale coordinates only inside the same target surface
- downgrade unsupported coordinates to low confidence
- route unsupported coordinates to `rejected` with `low_confidence`, `missing_evidence`, or `unverifiable` before Judge accept path

Record candidate-level gate output as `candidateIntakeGate.evidencePrecision[]`. A candidate with missing or unsupported evidence may not enter `finalQueue: judge` as an accepted-path candidate.

### ProducerEvidenceGate

Classify producer-absence claims before Judge. A producer-absence claim says a backend, API, serializer, DTO, data layer, or other producer does not provide, persist, transform, expose, or cover a required value or behavior.

Producer-absence claims require direct producer-side evidence: API contract, schema, serializer, endpoint response, data model, persistence logic, backend test fixture, or owner-confirmed behavior.

If producer-side evidence is provided by the user, referenced by source material, or discoverable in the current repo scope, inspect that producer surface before asking the user. Record the checked producer surface and access status in `candidateIntakeGate.producerEvidence`.

Consumer-side UI shape, fallback/default branch, empty state, mock, fixture, mapper, or missing consumer usage is never enough. Without producer-side evidence after checking available producer surfaces, reject or downgrade with `missing_producer_evidence`, `missing_evidence`, or `unverifiable`. Do not create `SourceConflict` from consumer-only evidence; source conflict requires conflicting source contracts or producer-side evidence that supports the conflict.

When the rejected reason is `missing_producer_evidence`, the stdout receipt and `report.md` must still tell the user what producer evidence was checked, what remains missing, and ask for confirmation or owner-mediated evidence. Add a `ClarificationNeeded` entry with `category: implementation-blocking` when the missing producer evidence blocks the gap decision, or `category: reference-only` when it only documents why the observation was rejected.

### RequirementTraceabilityGate

Reject or downgrade before Judge when expected, actual, evidence, or requiredChange cannot be traced to a confirmed contract field and a current target observation. This gate prevents plausible but ungrounded findings from reaching Judge as accepted-path candidates.

### SeverityScopeGate

Reject or downgrade before Judge when the candidate is P3/nit, not user-visible, not requirement-relevant, not interaction-affecting, duplicate, or below the P0/P1/P2 threshold. JudgeMergerAgent remains final authority for candidates that pass, but this gate prevents low-value candidates from inflating the accepted-path queue.

### ConflictClarificationGate

Block Judge accept path before accepted finding consideration. Route by source state:

- Create `SourceConflict` when two or more confirmed, non-superseded source contracts make incompatible requirements for the same target behavior, validation, permission, content, layout, interaction state, design-system rule, or analytics contract.
- Create `SourceConflict` when producer-side evidence directly contradicts a confirmed contract for a producer-absence claim.
- Create `ClarificationNeeded` when source priority, owner decision, inaccessible reference, Product/API/Design interpretation, or divergent similar implementation pattern must be chosen by the user or owner.
- Create `ClarificationNeeded` when producer evidence is missing and the missing producer answer blocks whether the observation is actionable.

These blocked items are not final findings. They must record evidence, impact, recommendation, and status, then stay out of `finalQueue: judge` until the blocking decision is supplied.

Candidate Intake Gate replaces ad-hoc candidate validation. It preserves JudgeMergerAgent as the only final authority over candidates that reach the judge queue.

## False-negative coverage gates

Missed critical issue를 줄이기 위해 candidate accept/reject 판단과 별도로 coverage gate를 기록합니다.

### TargetSurfaceCoverageGate

- Contract마다 target hint, current implementation surface, plan surface, producer surface 필요 여부를 기록합니다.
- `analysisDepth`가 `bounded` 이상이면 대표 usage 1-3개 또는 1-depth caller/consumer 확인 결과를 기록합니다.
- `analysisDepth`가 `expanded` 이상이면 shared component, design-system, API/DTO/state transition, similar implementation divergence surface 확인 결과를 기록합니다.
- `analysisDepth`가 `exhaustive-capped`이면 P0/P1, auth/permission/payment/data mutation/destructive action, release gate, cross-module surface cap과 checked surface 목록을 기록합니다.
- 확인하지 못한 required surface는 accepted finding을 만들지 않는 근거가 아니라 `ClarificationNeeded` 또는 rejected `missing_evidence`/`unverifiable` 근거로 남깁니다.

### DispatchCompletenessGate

- Source/plan/current implementation presence manifest와 `dispatchPlan`을 비교해 required agent가 누락되지 않았는지 확인합니다.
- Skipped agent마다 `criticalPathEffect`, `evidenceCoveragePreserved`, `falseNegativeRisk`를 기록합니다.
- Missing source 때문에 agent를 skip한 경우 speed proof에는 credit하지 않고, false-negative proof에는 coverage blocker 또는 reference-only clarification으로 반영합니다.
- CriticalRedTeamAgent는 would-be accepted 후보 검증뿐 아니라 selected analysis depth에서 missed P0/P1 candidate가 없는지 targeted search를 1회 수행합니다.

`heuristicProof.falseNegative`는 위 두 gate와 SourcePresenceManifest, ActiveSpecPatchCoverage, TargetHintExtraction, CriticalRedTeamAgent missed-P0/P1 search를 합산합니다. Combined improvement claim은 `falseNegative.improvementRatio >= 1.3`, `claimAllowed: true`, ClaimFreshnessGate `pass`일 때만 허용됩니다.

## ClaimFreshnessGate

Final receipt, report, and JSON artifact에 쓸 projected payload가 같은 canonical metadata를 참조하는지 확인합니다. 이 gate는 JudgeMergerAgent 이후, performance 계산 이후, artifact write 직전에 실행합니다.

- `claimFreshnessGate.status`는 `pass` 또는 `blocked`입니다.
- `checkedAfter`에는 `judge-result`, `performance`, `artifact-write` 중 마지막으로 재확인한 단계를 기록합니다.
- `heuristicProof`와 projected stdout/report/JSON payload가 final `candidateIntakeGate`, `targetSurfaceCoverageGate`, `dispatchCompletenessGate`, `performance`, `analysisDepth`, `dispatchPlan`, `dispatchSkips`와 불일치하면 stale input으로 기록하고 combined improvement claim을 차단합니다.
- 같은 run metadata 안에서 deterministic repair가 가능하면 `repairedInputs`에 기록하고 재계산합니다.
- repair할 수 없는 stale input이 남으면 `heuristicProof.claimAllowed: false`로 두고 stdout/report에서 개선 claim 대신 blocked proof를 출력합니다.

## AcceptedFinding schema

```text
AcceptedFinding = {
  id: FND-YYYYMMDD-HHmmss-RAND-NN,
  displayRef: G<N>,
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
- `missing_producer_evidence`
- `superseded_source`

## SourceConflict schema

Source conflicts are not final findings.

```text
SourceConflict = {
  id: CONFLICT-YYYYMMDD-HHmmss-RAND-NN,
  displayRef: C<N>,
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
  displayRef: Q<N>,
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
9. producer-absence claim이면 producer-side evidence gate를 통과했습니다.

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

Source discovery는 mode가 아니라 `analysisDepth`로 제어합니다.

- `direct`: user-provided reference와 active confirmed Spec Patch refs를 우선하고, target hints와 직접 매칭되는 하나의 Current Implementation surface만 확인합니다.
- `bounded`: direct seed에서 시작해 target 주변 1-depth 또는 대표 usage 1-3개를 확인합니다.
- `expanded`: related docs/rules/similar implementations/shared component 영향 범위, validation/permission/state edge를 risk-axis별로 확장합니다.
- `exhaustive-capped`: P0/P1, release gate, cross-module, auth/permission/payment/data mutation/destructive action 범위만 cap을 두고 확장합니다. finding이 0개가 될 때까지 반복하지 않습니다.

외부 reference가 접근 불가하면 pending reference로 기록하고 file, screenshot/export, pasted content를 요청합니다. 관측 가능한 repo evidence가 있으면 그 범위만 비교하고, 모호한 판단은 clarification으로 둡니다.

## Target freshness preflight

Current Implementation이 current branch, current working tree, local checkout을 뜻하면 비교 전에 integration branch freshness를 확인합니다.

- repository default remote branch를 식별합니다. 이 저장소 convention은 `origin/main`입니다.
- 가능하면 remote metadata를 refresh 또는 verify합니다.
- local `HEAD`가 integration branch tip보다 behind이면 requested scope 또는 target evidence 파일이 `HEAD..integration` 사이에서 바뀌었는지 확인합니다.
- behind changes가 target area에 영향을 주면 stale checkout을 target으로 삼지 않고 integration branch tip shape를 비교 기준으로 보고합니다.
- 사용자가 특정 commit, branch, PR diff, working tree state를 target으로 고정하면 target을 전환하지 않고 stale 여부만 evidence로 기록합니다.

## Analysis depth heuristic

`/tk:gap` always uses required quality gates. It chooses only how far to discover source and target evidence.

Analysis depth values:

- `direct`: one explicit source/target maps to one file, screen, command, or component; no ambiguity; no producer/API/state/auth/payment/data mutation surface.
- `bounded`: single screen/component/command with nearby 1-depth usage lookup or representative usage samples up to 3.
- `expanded`: shared component, design-system, API/DTO/state transition, source conflict risk, inaccessible reference, ambiguous Product/API/Design decision, or divergent similar implementations.
- `exhaustive-capped`: P0/P1 candidate, auth/permission/payment/data mutation/destructive action, release gate, or cross-module impact.

Depth scoring:

```text
riskScore starts at 0
+30 BE/API/DTO/persistence/state transition
+30 auth/permission/payment/data mutation/destructive action
+25 shared component/design-system component
+25 cross-module impact
+20 2+ similar implementations with different patterns
+20 inaccessible source reference
+20 source conflict or implementation-blocking clarification
+15 ambiguous Product/API/Design decision
+15 new screen/new flow
+15 release gate context
+40 accepted_or_candidate_P0_exists

sideEffectConfidence starts at 50
+20 explicit source reference maps to one file/component
+15 FE-only copy/layout/simple validation
+10 single screen/component
+10 no API/DTO/state transition
+10 no mutation/auth/permission/payment
+10 no ambiguity
```

Depth selection uses hard triggers first and risk score only as a tie-breaker:

```text
heuristicRequiredDepth = direct|bounded|expanded|exhaustive-capped from the rules below
if implementation target is not identified:
  heuristicRequiredDepth = bounded
  final finding path = missing_evidence/unverifiable only
else if accepted_or_candidate_P0_exists or auth/permission/payment/data mutation/destructive action or release gate or cross-module impact:
  heuristicRequiredDepth = exhaustive-capped
  depthReasons += hard_trigger_exhaustive_capped
else if source is inaccessible or ambiguity blocks contract:
  heuristicRequiredDepth = expanded
  final finding path = clarification/source_conflict only
  depthReasons += hard_trigger_ambiguity_or_inaccessible_source
else if shared component/design-system/API/DTO/persistence/state transition:
  heuristicRequiredDepth = expanded
  depthReasons += hard_trigger_shared_or_producer_surface
else if riskScore >= 45:
  heuristicRequiredDepth = expanded
  depthReasons += score_trigger_expanded
else if riskScore >= 16:
  heuristicRequiredDepth = bounded
  depthReasons += score_trigger_bounded
else if sideEffectConfidence >= 90:
  heuristicRequiredDepth = direct
else:
  heuristicRequiredDepth = bounded

if explicit --analysis-depth is valid:
  analysisDepth = max(requested value, heuristicRequiredDepth)
  if requested value is lower than heuristicRequiredDepth:
    record depthReasons += requested_depth_escalated_for_risk
else:
  analysisDepth = heuristicRequiredDepth
```

`heuristicProof.analysisDepth` records baseline trigger coverage, current trigger coverage, and `improvementRatio`. Analysis depth improvement may be claimed only when hard-trigger coverage is current, ClaimFreshnessGate passes, and `heuristicProof.analysisDepth.improvementRatio >= 1.3`.

`analysisDepth`, `depthReasons`, `riskScore`, `sideEffectConfidence`, `verificationEscalation`, `dispatchSkips`, `claimFreshnessGate`, `heuristicProof`, and `compatibilityFlags` must be recorded in run metadata.

## Performance measurement contract

`/tk:gap` measures speed improvement by a contract-derived critical path proxy when runtime wall-clock instrumentation is unavailable.

Proxy formula:

```text
criticalPathScore = agentCriticalPathGroups * 10 + deterministicStageGroups * 1 + runProcedureSteps * 0.1
improvementRatio = baselineCriticalPathScore / currentCriticalPathScore
```

Baseline for v7.2 strict-shaped flow:

```text
agentCriticalPathGroups = 7
  ProductContractAgent
  DesignContractAgent
  PlanCoverageAgent
  ImplementationComplianceAgent
  JudgeMergerAgent#1
  CriticalRedTeamAgent
  JudgeMergerAgent#2

deterministicStageGroups = 14
runProcedureSteps = 31
baselineCriticalPathScore = 87.1
```

단일 `/tk:gap` 실행 optimized contract target:

```text
agentCriticalPathGroups <= 4
  max(ProductContractAgent, DesignContractAgent)
  max(PlanCoverageAgent, ImplementationComplianceAgent)
  CriticalRedTeamAgent
  JudgeMergerAgent

deterministicStageGroups <= 9
runProcedureSteps <= 26
currentCriticalPathScore <= 51.6
achievedImprovementRatio >= 1.69
requiredImprovementRatio >= 1.3
```

Contract target proof for the v7.2.7 default procedure:

```text
baselineCriticalPathScore = 87.1
currentCriticalPathScore <= 4 * 10 + 9 * 1 + 26 * 0.1 = 51.6
minimumTargetImprovementRatio = 87.1 / 51.6 = 1.69
```

A concrete run must recompute these fields from its actual `dispatchPlan`, credited `dispatchSkips`, deterministic stage count, and run procedure step count. Do not copy the target proof as run proof when actual run metadata differs.

The run receipt or manifest must record the measured proxy fields when a gap run claims performance improvement. `measurementMethod` defaults to `contract-derived-critical-path-proxy` unless actual wall-clock instrumentation exists. Do not claim speed success from vague phrases such as `expected`, `estimated`, or `likely`; success requires recorded numeric fields and `improvementRatio >= 1.3`.

`dispatchSkips` may contribute to speed proof only when each credited skip records `agent`, `reason`, `sourceClass`, `credited: true`, `criticalPathDelta`, and `evidenceCoveragePreserved: true`. A skip caused by missing or ambiguous evidence may reduce agent dispatch, but it cannot be credited to speed improvement unless the run still preserves the required evidence coverage for the selected `analysisDepth`.

`heuristicProof.speed` mirrors the performance fields and sets `claimAllowed: true` only when `performance.improvementRatio >= heuristicProof.requiredImprovementRatio`. `heuristicProof.claimAllowed` is true only when false-positive, false-negative, speed, and analysis-depth subproofs are all allowed and ClaimFreshnessGate passes.

## Loop policy

금지:

```text
finding이 안 나올 때까지 반복
```

Default: loop 없음.

Targeted verification: CriticalRedTeamAgent 1회만 수행.

향후 loop가 생겨도 P3, nit, duplicate, unverifiable, source_conflict 때문에 continuation하면 안 됩니다.

Implementation 개선 작업에서는 `redesign -> analysis -> review -> feedback incorporation` 루프를 사용할 수 있지만, 이것은 command contract를 갱신하고 검증하는 개발 절차입니다. `/tk:gap` runtime은 단일 실행과 capped verification을 유지합니다.

## Run procedure

1. Emit start receipt with GAP-ID, branch-key, and planned report path.
2. In parallel, bind current worktree root, branch-key, run-id, user-provided references, target hints, current implementation candidates, and integration freshness metadata.
3. Build source/plan/current implementation presence manifest.
4. Freeze `dispatchPlan` from the presence manifest and record initial `dispatchSkips` with `criticalPathEffect`, `evidenceCoveragePreserved`, and `falseNegativeRisk`.
5. Compute `riskScore`, `sideEffectConfidence`, `analysisDepth`, `depthReasons`, and `verificationEscalation`.
6. Record deprecated compatibility inputs in `compatibilityFlags` without changing quality gates.
7. Load active Spec Patch unless `--no-specs` is present.
8. Load Product/Design/Design System/Engineering/QA/Analytics sources according to `analysisDepth` and risk-axis expansion rules.
9. Refresh `dispatchPlan` only from newly confirmed source presence; do not unskip from inferred or ambiguous evidence.
10. Freeze eligible confirmed, non-superseded contracts.
11. In parallel, run ProductContractAgent when product source exists and DesignContractAgent when design/design-system source exists; otherwise use recorded dispatch skip.
12. Normalize Spec Patch items deterministically.
13. Freeze merged contract set after removing draft, unclear, conflict, and superseded contracts from final evidence eligibility.
14. Run TargetSurfaceCoverageGate for the selected `analysisDepth` and record unchecked required surfaces.
15. In parallel, run PlanCoverageAgent when implementation plan exists and ImplementationComplianceAgent when current implementation exists; otherwise use recorded dispatch skip or rejected missing evidence observation.
16. Run Candidate Intake Gate for all candidates.
17. Run DispatchCompletenessGate before Judge queue construction.
18. Run CriticalRedTeamAgent once against would-be accepted, high-risk gated candidates, and missed P0/P1 search scope.
19. Run Candidate Intake Gate for any red-team candidate.
20. Run JudgeMergerAgent once on the final judge queue.
21. Run ambiguity/source-conflict receipt materialization for blocked items.
22. Compute and record `performance` fields from the final dispatch plan and deterministic stage count.
23. Run ClaimFreshnessGate against final candidate gates, coverage gates, dispatch metadata, performance proof, and analysis-depth decision.
24. Compute and record `heuristicProof` from false-positive gate coverage, false-negative coverage, performance proof, analysis-depth trigger coverage, and ClaimFreshnessGate.
25. Acquire branch lock, write required artifacts, update branch/global index, release lock.
26. Emit final stdout receipt and compact tables.

## Output

기본 stdout은 summary receipt와 compact finding tables만 출력합니다.

```text
Gap Review 시작: <GAP-ID>
Branch Scope: <branch-key>
품질 gate: evidence precision + producer evidence + ambiguity + JudgeMerger
분석 깊이: <direct|bounded|expanded|exhaustive-capped>
확장 이유: <none|summary>
검증 강화: <none|targeted-red-team>
상태: 완료
Report: .claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/report.md
성능 증명: <improvementRatio>x by <measurementMethod>
개선 증명: FP <ratio>x / FN <ratio>x / speed <ratio>x / depth <ratio>x
Proof freshness: <pass|blocked>

Findings:
- P0: <count>
- P1: <count>
- P2: <count>

Actionable Findings:
| Ref | Sev | 요약 | 의미 | Required change |
| --- | --- | --- | --- | --- |
| G1 | P1 | <final finding 1줄 요약> | <사용자/제품 관점 영향 1줄> | <수정 방향 1줄> |

Rejected/Downgraded:
| Ref | Reason | 요약 | 왜 final gap 아님 |
| --- | --- | --- | --- |
| R1 | missing_evidence | <observation 1줄 요약> | <reject/downgrade 이유 1줄> |

Source Conflicts: <count>
Clarification Needed: <count>
Rejected/Downgraded: <count>
```

`Actionable Findings` table에는 JudgeMergerAgent가 accept한 P0/P1/P2 final finding만 출력합니다. 각 row는 run-local Ref, severity, gap 요약, 사용자/제품 관점 의미, requiredChange 1줄 요약만 포함합니다. final finding이 없으면 `없음` 1줄을 출력합니다.

`Rejected/Downgraded` table에는 final gap이 아닌 observation을 간략히 출력합니다. 각 row는 run-local Ref, reason, observation 요약, final gap이 아닌 이유 1줄만 포함합니다. 항목이 없으면 `없음` 1줄을 출력합니다. `missing_producer_evidence` row는 필요한 producer evidence와 `Q<N>` 확인 요청 Ref를 함께 언급합니다. P3/nit/duplicate/unverifiable/source_conflict 같은 rejected item을 confirmed defect처럼 쓰면 안 됩니다.

유저향 compact table에는 긴 canonical ID를 column으로 직접 노출하지 않습니다. canonical ID는 JSON artifact의 `id`와 `displayRef` mapping, 또는 `report.md` 상세/참조 영역에서 확인할 수 있어야 합니다.

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

`## Summary`에는 `qualityGates`, `analysisDepth`, `depthReasons`, `riskScore`, `sideEffectConfidence`, `verificationEscalation`, dispatch skip summary, Candidate Intake Gate summary, evidence precision gate summary, TargetSurfaceCoverageGate summary, DispatchCompletenessGate summary, ClaimFreshnessGate summary, performance proof, heuristic proof를 포함합니다. compatibility flag는 입력 기록으로만 포함하고 primary label로 출력하지 않습니다. `report.md`의 상세 finding/observation/conflict/clarification 항목은 `G1`, `R1`, `C1`, `Q1` 같은 Ref를 heading 또는 첫 필드로 쓰고 canonical ID를 별도 metadata로 둡니다.

`## Source Conflicts / Clarification Needed`는 implementation-blocking과 reference-only를 구분합니다. 질문은 option/evidence/impact/recommendation/status를 표로 제시합니다. UI 판단이 필요한 경우 오른쪽 border가 정렬된 TUI/ASCII prototype을 함께 둡니다.

## 금지

- basis를 절대적 진실처럼 단정
- conflict source를 임의 병합
- subagent candidate를 final finding처럼 출력
- P3/nit를 final finding으로 출력
- unverifiable/source_conflict를 final finding으로 출력
- targeted red-team을 2회 이상 실행
- finding이 0개가 될 때까지 loop
- default stdout에 전체 report 출력
- 유저향 compact table에서 긴 canonical Candidate/Finding ID를 primary column으로 출력
- `/tmp`, `$GIT_COMMON_DIR`, user home에 gap run 저장
