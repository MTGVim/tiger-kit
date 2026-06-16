---
description: source를 근거로 고정하고 모호함을 공격해 sealed launch workflow 또는 blocked report를 생성합니다.
argument-hint: "[--review] [--analysis-depth <direct|bounded|expanded|exhaustive-capped>] [--spec <SP-ID|path>] [--no-specs] [--print-report] [--maintainer-proof]"
---

이 명령은 TigerKit v8.0 sealed GAP workflow contract를 따릅니다. `/tk:gap --review`는 v7 Contract-based Gap Review compatibility mode입니다.

사용자에게는 한글로 답합니다. 코드, path, URL, ticket, commit, hash, identifier, error는 원문 그대로 둘 수 있습니다.

목표: 기본 `/tk:gap`은 source를 근거로 고정하고, 모호함과 failure mode를 공격한 뒤, launch 가능한 sealed workflow를 만들거나 launch 금지 사유를 branch-local artifact로 저장합니다.

```text
gap = ground sources + attack ambiguity + produce sealed launch workflow
```

## User-facing command interface

### Product principle

기본 `/tk:gap`은 proof generator가 아닙니다. 기본 실행에는 사용자가 고치거나 답할 수 있는 것만 남깁니다.

1. 실제로 고칠 문제를 찾습니다.
2. 틀린 지적을 줄입니다.
3. 모호하면 좋은 질문으로 넘깁니다.
4. 다음 행동을 짧게 줍니다.

TigerKit 자체 성능 개선, baseline, heuristic proof, performance proof, false-positive/false-negative improvement claim은 `--maintainer-proof`에서만 다룹니다.

## Command surface

- plugin slash invocation은 `/tk:gap`입니다.
- `tiger-kit gap` CLI 표현은 이 plugin command의 사용자 관점 alias로 취급합니다.
- `/tk:gap`은 하나의 실행으로 동작합니다.
- 기본 `/tk:gap`은 `GAP_READY` 또는 `GAP_BLOCKED` 중 하나로 끝납니다.
- `GAP_READY`는 정확히 하나의 `tigerkit-launch-workflow` block과 workflow hash를 포함합니다.
- `GAP_BLOCKED`는 unresolved decision/conflict/missing source를 기록하고 `tigerkit-launch-workflow` block을 포함하지 않습니다.
- `/tk:gap --review`는 v7 Contract-based Gap Review compatibility mode입니다.
- `--maintainer-proof`는 maintainer/self-eval 전용입니다. 일반 사용자 품질 모드가 아니며 기본 gap 결과를 더 강하게 만드는 옵션처럼 설명하지 않습니다.
- `--lite`와 `--strict`는 compatibility flag로만 기록하며 active v8.0 user-facing quality mode가 아닙니다.
- `--legacy`, `TIGERKIT_GAP_LEGACY`, `--deep`, `--no-strict`는 active v8.0 mode가 아닙니다.
- v6-era legacy behavior는 미지원 과거 동작입니다. `lite`의 별칭이나 계승 mode로 표현하지 않습니다.
- legacy Figma diff style은 정식 사용자 모드가 아닙니다.

## 기본 GAP workflow 경로

1. 사용자 의도, URL, ticket, notes, screenshots, repo context, prior specs, conversation decisions를 intake합니다.
2. source material과 authority를 분리합니다.
3. confirmed requirement, assumption, rejected assumption, non-goal을 정규화합니다.
4. bounded ambiguity attack으로 contradiction, missing decision, hidden dependency, edge case, failure mode, verification gap을 탐지합니다.
5. YAGNI trim으로 workflow 밖 future extensibility를 제거합니다.
6. task graph, success/failure condition, verification gate, abort policy, commit policy를 작성합니다.
7. launch 가능하면 `GAP_READY`와 sealed `tigerkit-launch-workflow`를 저장합니다.
8. launch 금지 사유가 남으면 `GAP_BLOCKED`와 blocked report를 저장합니다.

Workflow hash는 fenced block body raw UTF-8 bytes를 LF로 정규화하고 final LF를 하나 보장한 뒤 SHA-256으로 계산합니다. opening/closing fence line은 hash에서 제외하고 YAML key sort나 normalize를 하지 않습니다.

## `/tk:gap --review` 핵심 원칙

- Product/Design Spec 기반 inspection입니다.
- basis는 현재 비교 자료이며 절대적 진실이 아닙니다.
- subagent는 candidate만 생성합니다.
- JudgeMergerAgent만 final finding을 확정합니다.
- final accepted finding에는 P0/P1/P2만 포함합니다.
- P3/nit/duplicate/unverifiable/source_conflict는 final finding이 아닙니다.
- candidate의 file:line, module-path, rendered output evidence는 JudgeMergerAgent queue 진입 전에 현재 target surface에서 read-back으로 재확인합니다.
- producer가 값을 미제공/미커버한다는 claim은 producer 계약, schema, serializer, endpoint response, data model, persistence logic 같은 producer-side evidence 없이는 final finding이나 source_conflict로 승격하지 않습니다.
- current implementation 비교 전에는 integration branch freshness를 확인합니다.
- 모든 final finding은 analysis depth와 관계없이 evidence precision, producer evidence, ambiguity, JudgeMerger gate를 통과해야 합니다.
- 사용자가 files/scope를 명시하지 않는 기본 흐름은 issue ticket, design node link, screenshot, pasted notes 같은 user-provided references에서 target hints를 추출합니다.
- source set이 커서 다중 breakpoint/variant/case를 한 번에 받으면 source-by-source locked intake를 권장합니다. 먼저 원하는 전달 포맷을 명시하고, source 단위로 수집·측정·대조·lock한 뒤 다음 source로 진행합니다. source가 적고 독립 검증이 흐려지지 않으면 기존 일괄 intake를 유지할 수 있습니다.
- changed files는 primary scope가 아니라 Current Implementation 후보 evidence입니다.
- Product Spec, Design Spec, API contract, source priority, owner decision의 ambiguity는 명확해 보여도 user consent 전에는 confirmed contract로 승격하지 않습니다.
- visible UI copy는 confirmed contract와 exact match가 필요합니다.
- finding이 안 나올 때까지 반복하지 않습니다.
- CriticalRedTeamAgent pass는 targeted verification으로 최대 1회입니다.
- full execution graph나 runner를 소유하지 않습니다.
- report에는 clarification, finding, re-check 순서를 이해시키는 graph-lite `Next Action Graph`를 포함할 수 있습니다.
- stdout은 run 결과, finding/clarification count, report path, run.json path, next action만 기본 출력합니다.
- 유저향 stdout/report table은 run-local short Ref(`G1`, `R1`, `C1`, `Q1`)를 우선 표시하고 긴 canonical ID는 `run.json` 또는 maintainer proof artifact에 보관합니다.
- Hook guard는 repo 유지보수 sync/lint가 아니라 플러그인 사용자가 보는 receipt, artifact path, finding Ref 안전장치일 때만 사용합니다. 그런 user-facing guard 표면이 없으면 hook을 추가하지 않습니다.

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
- Clarification Needed

금지 표현:

- Figma gap
- Figma diff
- PRD review skill
- Design review skill
- quality mode
- preset 추천

## Source intake and design evidence trust

대량 source intake에서는 독립 검증과 사용자 확정 시점을 보존합니다.

- source set이 다중 breakpoint, variant, 보조 case set처럼 커 보이면 먼저 전달 포맷을 제안합니다.
- source 단위로 raw reference, derived Contract, current implementation 비교 결과, clarification 여부를 분리해 기록합니다.
- 각 source는 측정·대조가 끝난 시점에 lock하고, lock 후 새 자료가 오면 같은 source를 조용히 덮어쓰지 않고 추가 source 또는 superseding source로 다룹니다.
- locked intake는 누락·과적을 줄이기 위한 권장 경로입니다. source가 적거나 서로 의존하는 단일 bundle이면 기존 일괄 intake를 사용할 수 있습니다.

Design source는 trust axis를 분리합니다.

| source_type | 역할 | 제한 |
| --- | --- | --- |
| `structural_context` | frame/node 구조, text layer, token/metadata, component hierarchy, variant 관계 확인 | 접근 불가하거나 불완전하면 missing evidence로 표시 |
| `visual_capture` | layout, 구성, hierarchy, state 비교의 보조 근거 | 색, 간격, 치수 같은 수치 값을 단독 확정하지 않음 |

색·간격·치수 같은 numeric design value는 구조/메타 자료, design token, 또는 명시된 confirmed source가 필요합니다. 기존 구현은 대조·추론 보조로만 쓰며 단독 design SOT가 아닙니다. visual capture만 있거나 배율/렌더링 왜곡 가능성이 남으면 수치 단정 대신 `Clarification Needed` 또는 rejected `unverifiable`로 기록합니다.

## Branch-local storage

반드시 current worktree root 아래 `.claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/`에 저장합니다.

기본 `/tk:gap` 필수 파일은 `report.md`와 `run.json`입니다. `report.md`는 사용자가 읽는 표면이고, `run.json`은 후속 대화와 기계 처리를 위한 최소 run record입니다.

상세 artifact layout은 `.tigerkit/docs/artifact-layout.md`를 기준으로 합니다. 상세 stdout/report/run.json 계약은 `.tigerkit/docs/output-contract.md`의 `/tk:gap default stdout` 섹션을 기준으로 합니다.

`.claude/tigerkit/`은 generated branch-local working memory이며 repo-wide durable knowledge가 아닙니다.

## Maintainer proof mode

`--maintainer-proof`가 명시된 경우에만 `maintainer-proof/` 아래 self-eval/performance proof artifact를 생성하거나 요구합니다.

기본 사용자 경로는 false-positive, false-negative, speed, analysis-depth improvement claim을 하지 않습니다. 기본 stdout/report/run.json에 proof/debug artifact 목록이나 self-eval metadata를 섞지 않습니다.

Maintainer-only artifact와 boundary는 `.tigerkit/docs/artifact-layout.md`를 기준으로 합니다. maintainer proof 노출 규칙은 `.tigerkit/docs/output-contract.md`를 기준으로 합니다.

## CLI options

- default: 단일 `/tk:gap` 실행으로 실행하고 사용자-facing `report.md`와 `run.json`을 생성합니다.
- `--analysis-depth <direct|bounded|expanded|exhaustive-capped>`: 품질 gate를 낮추지 않고 source discovery depth만 명시합니다. 기본 stdout에는 proof나 확장 이유 dump를 출력하지 않습니다.
- `--spec <SP-ID>`: current branch scope의 `specs/index.json`에서만 resolve합니다.
- `--spec <path>`: current worktree root 내부 path만 허용합니다.
- `--no-specs`: active Spec Patch 자동 참조를 비활성화합니다.
- `--print-report`: 저장된 `report.md` 본문을 stdout에도 출력합니다.
- `--maintainer-proof`: maintainer/self-eval 전용 proof artifact를 `maintainer-proof/` 아래에 추가 생성합니다.

`--lite`와 `--strict`는 compatibility flag로만 기록하고 quality gate를 바꾸지 않습니다. `--legacy`, `TIGERKIT_GAP_LEGACY`, `--deep`, `--no-strict`는 active v8.0 mode가 아닙니다.

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

## Internal agent, gate, and proof contract

이 아래 section은 runtime 내부 판정 절차와 maintainer/debug 계약입니다. 사용자-facing receipt와 artifact interface는 위 Command surface, Branch-local storage, 그리고 `.tigerkit/docs/output-contract.md`를 따릅니다.

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
Use only the output type assigned to your role: contract agents produce contracts only, candidate agents produce candidates only, and JudgeMergerAgent produces final judge decisions only.
A valid result may contain zero items.
Do not invent issues.
Do not report subjective preferences.
Do not report P3/nit issues unless explicitly requested.
Do not repeat issues already covered by broader candidates.
Every candidate must include concrete evidence and a fix hint.
Do not omit a P0/P1 candidate because a narrower depth was requested when a hard trigger requires escalation.
When citing file:line or module path evidence, cite a current read-back confirmed span.
```

### Agent dispatch

source/plan 부재 시 불필요한 agent를 실행하지 않습니다.

- Product source가 없으면 ProductContractAgent를 skip합니다.
- Design 또는 Design System source가 없으면 DesignContractAgent를 skip합니다.
- Implementation Plan이 없으면 PlanCoverageAgent를 skip합니다.
- Current Implementation이 식별되지 않으면 ImplementationComplianceAgent를 skip하고 관련 observation은 `unverifiable` 또는 `missing_evidence`로만 기록합니다.
- CriticalRedTeamAgent는 would-be accepted 또는 high-risk gated candidate가 있을 때 targeted verification으로 최대 1회 실행합니다.
- JudgeMergerAgent는 final judge queue에 대해 1회 실행해 accepted/rejected/source conflict/blocked clarification을 확정합니다.
- 기본 경로에서는 skip 상세 dump를 출력하지 않습니다. skip 때문에 사용자가 알아야 할 결론 제한이 있으면 `Clarification Needed`, `rejectedSummary`, 또는 `report.md`의 짧은 확인 범위 문장으로만 표현합니다.
- `--maintainer-proof`에서는 dispatch proof와 credited skip metadata를 `maintainer-proof/` artifact에 기록할 수 있습니다.

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

## Candidate Intake Gate

JudgeMergerAgent queue에 넣기 전에 모든 candidate는 아래 gate를 통과해야 합니다. 이 gate는 기본 사용자 경로에서도 품질 기준으로 유지합니다. 단, 기본 artifact에는 gate proof dump를 요구하지 않습니다.

1. CandidateShapeGate: kind, severity, evidence, fixHint, sourceContracts shape 확인
2. EvidencePrecisionGate: file:line, module path, rendered output 좌표 read-back 확인 또는 repair
3. ProducerEvidenceGate: producer-absence claim에 producer-side evidence 존재 여부 확인
4. ConflictClarificationGate: source conflict나 owner decision ambiguity를 accept path에서 분리
5. RequirementTraceabilityGate: confirmed, non-superseded contract trace 확인
6. SeverityScopeGate: P0/P1/P2 user-visible 또는 requirement-relevant impact 확인

Gate 결과가 `judge`가 아니면 JudgeMergerAgent queue에 넣지 않고 rejected observation, SourceConflict, 또는 ClarificationNeeded로 기록합니다.

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
  fixHint
}

EvidenceRef = {
  ref,
  kind: file_line | module_path | contract | producer_surface | rendered_output | owner_confirmed,
  claimRole: expected | actual | producer_absence | conflict | fix_hint,
  readBackStatus: pending | confirmed | repaired | missing,
  repairedRef?,
  precisionReason
}
```

`--maintainer-proof`에서는 `candidateIntakeGate` 세부 결과를 candidate에 추가로 기록할 수 있습니다.

## Candidate gates

### CandidateShapeGate

Reject 또는 downgrade 조건:

- confirmed, non-superseded `sourceContracts` 없음
- concrete `evidence` 없음
- `expected`가 confirmed contract로 trace되지 않음
- `actual`이 관측된 plan 또는 implementation state가 아니라 추측임
- `fixHint`가 추측을 요구하거나 실행 가능하지 않음

Allowed rejected reasons: `missing_evidence`, `not_actionable`, `unverifiable`, `low_confidence`.

### EvidencePrecisionGate

모든 file:line 또는 module-path evidence coordinate에 대해:

- 현재 target surface를 read back합니다.
- cited span이 candidate claim을 지지하는지 확인합니다.
- stale coordinate는 같은 target surface 안에서만 repair합니다.
- unsupported coordinate는 low confidence로 downgrade합니다.
- unsupported coordinate는 Judge accepted path 전에 `low_confidence`, `missing_evidence`, `unverifiable`로 분리합니다.

### ProducerEvidenceGate

Producer-absence claim은 backend, API, serializer, DTO, data layer, persistence, transform, expose, coverage 부재를 주장하는 claim입니다.

Producer-absence claim에는 API contract, schema, serializer, endpoint response, data model, persistence logic, backend test fixture, owner-confirmed behavior 같은 direct producer-side evidence가 필요합니다.

사용자가 producer evidence를 제공했거나 source material이 참조했거나 현재 repo scope에서 발견 가능하면 사용자에게 묻기 전에 그 producer surface를 먼저 확인합니다.

Consumer-side UI shape, fallback/default branch, empty state, mock, fixture, mapper, missing consumer usage는 충분하지 않습니다. available producer surface 확인 후에도 producer-side evidence가 없으면 `missing_producer_evidence`, `missing_evidence`, `unverifiable`로 reject/downgrade합니다. consumer-only evidence로 `SourceConflict`를 만들지 않습니다.

`missing_producer_evidence`가 gap 결정에 영향을 주면 `Clarification Needed`의 `Q<N>`으로 사용자 또는 owner 확인을 요청합니다. stdout에서는 질문만 짧게 보여주고, 어떤 producer evidence가 확인됐고 무엇이 missing인지 상세는 `report.md`에 둡니다.

### RequirementTraceabilityGate

expected, actual, evidence, requiredChange가 confirmed contract field와 current target observation으로 trace되지 않으면 Judge accepted path 전에 reject/downgrade합니다.

### SeverityScopeGate

P3/nit, not user-visible, not requirement-relevant, not interaction-affecting, duplicate, P0/P1/P2 threshold 미달 candidate는 Judge accepted path 전에 reject/downgrade합니다.

### ConflictClarificationGate

아래는 final finding이 아닙니다.

- confirmed, non-superseded source contracts가 같은 target behavior에 대해 충돌하는 경우: `SourceConflict`
- producer-side evidence가 confirmed contract와 직접 충돌하는 경우: `SourceConflict`
- source priority, owner decision, inaccessible reference, Product/API/Design interpretation, divergent similar implementation pattern을 사용자나 owner가 선택해야 하는 경우: `ClarificationNeeded`
- producer evidence가 missing이고 그 답이 actionability를 좌우하는 경우: `ClarificationNeeded`

Blocked item은 evidence, impact, recommendation, status를 기록하고 blocking decision이 공급될 때까지 Judge accepted path에 들어가지 않습니다.

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

Source discovery는 user-facing mode가 아니라 `analysisDepth`로 제어합니다.

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

Depth selection uses hard triggers before risk-score tie-breakers. Explicit `--analysis-depth` may not lower the heuristic-required minimum depth for risky surfaces; lower requested depth is escalated internally without changing user-facing quality mode.

기본 stdout/report/run.json은 depth proof를 요구하지 않습니다. `--maintainer-proof`에서만 analysis depth score, baseline, improvement ratio를 기록할 수 있습니다.

## Maintainer proof contracts

이 section은 `--maintainer-proof`가 명시된 경우에만 적용합니다.

### HeuristicProof

```text
HeuristicProof = {
  cumulativeRequiredImprovementRatio: 1.3,
  iterationRequiredImprovementRatio: >1.0,
  falsePositive: { metric, denominator, scoreDirection, cumulativeBaseline, iterationBaseline, currentScore, cumulativeImprovementRatio, iterationImprovementRatio, improvementFormula, claimAllowed },
  falseNegative: { metric, denominator, scoreDirection, cumulativeBaseline, iterationBaseline, currentScore, cumulativeImprovementRatio, iterationImprovementRatio, improvementFormula, claimAllowed },
  speed: { metric, scoreDirection, cumulativeBaseline, iterationBaseline, currentScore, cumulativeImprovementRatio, iterationImprovementRatio, improvementFormula, claimAllowed },
  analysisDepth: { metric, denominator, scoreDirection, cumulativeBaseline, iterationBaseline, currentScore, cumulativeImprovementRatio, iterationImprovementRatio, improvementFormula, claimAllowed },
  baselineProvenance,
  baselineAutoRefreshGate,
  claimAllowed
}
```

Heuristic proof metrics use fixed denominators from this contract, not ad-hoc run scoring. Each metric records two baselines:

- `cumulativeBaseline`: 최초 tracked baseline contract score.
- `iterationBaseline`: 직전 `origin/main` contract score for the same metric.
- `currentScore`: 이번 contract score from maintainer proof metadata.

Higher-is-better metrics use `currentScore / baselineScore`. Speed uses `baselineScore / currentScore`.

### False-negative coverage proof

Maintainer proof mode에서만 TargetSurfaceCoverageGate, DispatchCompletenessGate, SourcePresenceManifest, ActiveSpecPatchCoverage, TargetHintExtraction, CriticalRedTeamAgent missed-P0/P1 search를 `heuristicProof.falseNegative`로 수치화합니다.

기본 사용자 경로에서는 이 proof를 기록하지 않습니다. 대신 확인 못 한 표면이 사용자의 판단을 막으면 `Clarification Needed` 또는 rejected `missing_evidence`/`unverifiable` 요약으로만 표현합니다.

### Performance measurement contract

Maintainer proof mode에서만 `/tk:gap` speed improvement를 contract-derived critical path proxy로 측정할 수 있습니다.

```text
criticalPathScore = agentCriticalPathGroups * 10 + deterministicStageGroups * 1 + runProcedureSteps * 0.1
cumulativeImprovementRatio = cumulativeBaselineScore / currentScore
iterationImprovementRatio = iterationBaselineScore / currentScore
```

Speed improvement may be claimed only when numeric performance fields are recorded and speed's cumulative and iteration ratios are calculated with `baselineScore / currentScore` because speed is `lower_is_better`. Credited `dispatchSkips` may contribute only when `credited: true`, `criticalPathDelta`, and `evidenceCoveragePreserved: true` are recorded. Vague wording such as `expected`, `estimated`, or `likely` is not proof.

### BaselineAutoRefreshGate

Maintainer proof mode에서만 `.tigerkit/docs/gap-baselines.json`과 refreshed `origin/main`의 baseline registry를 읽어 cumulative baseline과 iteration baseline을 분리합니다.

- `cumulativeBaseline`은 registry의 최초 기준에서만 로드합니다.
- `iterationBaseline`은 refreshed `origin/main:.tigerkit/docs/gap-baselines.json`의 직전 main score snapshot에서 로드합니다.
- `baseline-snapshot.json`에는 `seriesId`, `metricDirections`, `cumulativeBaseline`, `iterationBaseline`, `currentScore`, `cumulativeImprovementRatio`, `iterationImprovementRatio`, `promotionCandidate`, `sourceRefs`, `capturedAt`, `status`를 기록합니다.
- 고정 cumulative score만으로 새 반복 개선을 주장하지 않습니다.

### ClaimFreshnessGate

Maintainer proof mode에서만 final receipt, report, JSON payload, proof artifact가 같은 canonical metadata를 참조하는지 확인합니다. stale input이 남으면 improvement claim을 차단합니다.

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

1. Emit start receipt with GAP-ID, branch-key, planned report path, and planned run.json path.
2. Bind current worktree root, branch-key, run-id, user-provided references, target hints, current implementation candidates, and integration freshness metadata.
3. Load active Spec Patch unless `--no-specs` is present.
4. Load Product/Design/Design System/Engineering/QA/Analytics sources according to selected discovery depth.
5. Build source/plan/current implementation presence summary and skip unnecessary agents.
6. Run ProductContractAgent and DesignContractAgent only when matching source exists.
7. Normalize Spec Patch items deterministically.
8. Freeze confirmed, non-superseded contract set.
9. Run PlanCoverageAgent when implementation plan exists and ImplementationComplianceAgent when current implementation exists.
10. Run Candidate Intake Gate for all candidates.
11. Run CriticalRedTeamAgent once only when would-be accepted or high-risk gated candidate needs targeted verification.
12. Run Candidate Intake Gate for red-team candidates.
13. Run JudgeMergerAgent once on final judge queue.
14. Materialize Actionable Findings, Source Conflicts, Clarification Needed, and rejected summary.
15. If `--maintainer-proof` is present, compute maintainer proof metadata and write `maintainer-proof/` artifacts.
16. Acquire branch lock, write `report.md`, `run.json`, update branch/global index, release lock.
17. Emit final stdout receipt and compact tables.

## Output

기본 stdout은 사용자가 바로 행동할 수 있는 receipt만 출력합니다.

Interface 요약:

- 완료한 단일 `/tk:gap` 실행의 run ID, branch scope, P0/P1/P2 count, Source Conflict count, Clarification Needed count를 출력합니다.
- `report.md`와 `run.json` path, 다음 행동을 출력합니다.
- Actionable Findings와 Clarification Needed table은 row가 있을 때만 compact하게 출력합니다.
- 유저향 table은 run-local Ref(`G<N>`, `Q<N>`)를 우선 사용합니다.
- `--print-report`가 있을 때만 저장된 `report.md` 본문을 stdout에도 출력합니다.
- proof/debug/self-eval metadata와 rejected/downgraded 상세 목록은 기본 stdout에 출력하지 않습니다.

Authoritative stdout contract는 `.tigerkit/docs/output-contract.md`의 `/tk:gap default stdout` 섹션입니다. artifact boundary는 `.tigerkit/docs/artifact-layout.md`를 기준으로 합니다.

## Report shape

기본 `report.md`는 아래 H2를 사용합니다.

```md
# Tiger Kit Gap Report: <GAP-ID>

## Summary

## Sources Used

## Actionable Findings

## Clarification Needed

## Not Accepted Summary

## Next Action Graph

## Next Action
```

`## Summary`에는 run 결과, branch scope, finding count, clarification count, report/run path만 둡니다.

`## Sources Used`에는 비교에 실제로 사용한 source refs와 access status를 짧게 둡니다. target coverage proof나 dispatch proof dump를 두지 않습니다.

`## Actionable Findings`에는 `G<N>` heading 또는 첫 field를 사용합니다. accepted P0/P1/P2 finding만 포함합니다.

`## Clarification Needed`는 implementation-blocking과 reference-only를 구분합니다. 질문은 option/evidence/impact/recommendation/status를 표로 제시합니다. UI 판단이 필요한 경우 오른쪽 border가 정렬된 TUI/ASCII prototype을 함께 둡니다.

`## Not Accepted Summary`는 rejected/downgraded 상세 목록이 아니라 reason별 count와 사용자에게 의미 있는 짧은 요약만 둡니다. 상세 proof나 candidate dump는 `--maintainer-proof`에서만 허용합니다.

`## Next Action Graph`는 구현 runner가 아닙니다. 사용자가 clarification, fixing, re-check, re-run 순서를 이해하도록 run-local Ref로만 가벼운 순서를 적습니다. 예: `Q1 확인 -> G1 수정 -> G2 재확인 -> /tk:gap 재실행`.

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
- 기본 사용자 경로에서 self-eval proof나 성능 개선 claim 출력
- 기본 사용자 경로에서 `input-manifest.json`, `judge-result.json`, `baseline-snapshot.json`, `heuristicProof`, `performance`를 필수 산출물로 요구
- `/tmp`, `$GIT_COMMON_DIR`, `.git/worktrees/*`, user home에 gap run 저장
