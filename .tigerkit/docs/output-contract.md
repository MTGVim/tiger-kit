# TigerKit 운영 Output Contract

이 문서는 TigerKit v7.2.10 command의 출력 계약을 정의합니다. 사용 흐름은 `.tigerkit/docs/usage.md`, 산출물 위치는 `.tigerkit/docs/artifact-layout.md`를 기준으로 봅니다.

```text
stdout is a receipt. Full spec/gap bodies are saved as branch-local artifacts unless explicit print option is used.
```

## 공통 원칙

기본 응답은 아래 네 가지에 집중합니다.

1. outcome
2. branch scope
3. artifact paths when files are written
4. counts, risks, next action

상세 본문은 파일에 저장하고, 각 command가 지원하는 explicit print option을 지정한 경우에만 stdout에 함께 출력합니다. `/tk:spec`은 `--print-body`, `/tk:gap`은 `--print-report`를 사용합니다.

사용자 대화에 보이는 안내, 추천, 요약, next action은 계약용어, path, identifier, field name을 제외하고 한글로 씁니다.

## `/tk:spec` Output Contract

- 목적: raw instruction을 현재 branch-local Spec Patch로 저장합니다.
- 기본 저장 위치: `.claude/tigerkit/branches/<branch-key>/specs/`
- 기본 stdout은 summary만 출력합니다.
- Spec Patch 전체 본문은 `--print-body`가 있을 때만 출력합니다.
- `spec`은 finding을 만들지 않고 구현 분석을 하지 않습니다.

기본 stdout:

```text
Spec Patch 생성: <SP-ID>
Branch Scope: <branch-key>
경로: .claude/tigerkit/branches/<branch-key>/specs/<SP-ID>-<slug>.md
Items:
- <ITEM-ID>
```

## `/tk:gap` Output Contract

- 목적: Product/Design Spec contract와 implementation plan/current implementation을 비교합니다.
- 기본 저장 위치: `.claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/`
- `/tk:gap`은 단일 `/tk:gap` 실행로 실행합니다.
- `--lite`와 `--strict`는 compatibility flag로만 기록하며 user-facing quality mode가 아닙니다.
- 분석 범위는 `analysisDepth: direct|bounded|expanded|exhaustive-capped`와 `depthReasons`로 기록합니다. hard trigger가 risk score보다 우선하며, 명시된 `--analysis-depth`가 위험 표면의 heuristic minimum보다 낮으면 낮추지 않고 escalation을 기록합니다.
- subagent는 final finding을 확정하지 못합니다.
- candidate의 file:line 또는 module-path evidence는 JudgeMergerAgent queue 진입 전에 현재 target surface에서 read-back으로 재확인합니다.
- producer-absence claim은 producer-side evidence gate를 통과해야 합니다.
- user-provided source, referenced source, repo에서 접근 가능한 API contract/schema/endpoint/serializer/data model이 있으면 사용자에게 묻기 전에 먼저 확인합니다.
- consumer-only fallback/default/mapper evidence는 producer absence accepted finding이나 `SourceConflict`로 승격하지 않습니다.
- `missing_producer_evidence`는 숨기지 않습니다. stdout/report에서 확인한 producer surface, access status, 아직 필요한 producer evidence를 알리고 `Clarification Needed`로 사용자 또는 owner 확인을 요청합니다.
- ambiguity와 source conflict는 Judge accept path 전에 `Clarification Needed` 또는 `SourceConflict`로 기록합니다.
- JudgeMergerAgent만 final accepted finding을 확정합니다.
- 유저향 stdout/report table은 run-local short Ref(`G1`, `R1`, `C1`, `Q1`)를 우선 표시하고 긴 canonical ID는 JSON artifact와 report 상세/참조 영역에 보관합니다.
- final finding에는 P0/P1/P2만 포함합니다.
- P3/nit/duplicate/unverifiable/source_conflict는 final finding으로 출력하지 않습니다.
- missed P0/P1 방지를 위해 target surface coverage와 dispatch completeness를 기록하고 `heuristicProof.falseNegative`로 수치화합니다.
- finding이 안 나올 때까지 반복하지 않습니다.

기본 stdout:

```text
Gap Review 시작: <GAP-ID>
Branch Scope: <branch-key>
품질 gate: evidence precision + producer evidence + ambiguity + JudgeMerger
분석 깊이: <direct|bounded|expanded|exhaustive-capped>
확장 이유: <none|summary>
검증 강화: <none|targeted-red-team>
상태: 완료
Report: .claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/report.md
성능 증명: cumulative <ratio>x / iteration <ratio>x by <measurementMethod>
누적 개선 증명: FP <ratio>x / FN <ratio>x / speed <ratio>x / depth <ratio>x
반복 개선 증명: FP <ratio>x / FN <ratio>x / speed <ratio>x / depth <ratio>x
Baseline: cumulative <sourceRef> / iteration <sourceRef>
Baseline refresh: <pass|blocked> from <registryPath>
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

Run artifact files:

```text
input-manifest.json
contracts.json
candidates.json
judge-result.json
baseline-snapshot.json
report.md
```

Gap run metadata must include:

- `displayRefs` or item-level `displayRef` mapping between run-local Ref and canonical IDs
- `qualityGates: evidencePrecision|producerEvidence|ambiguity|JudgeMerger`
- `analysisDepth: direct|bounded|expanded|exhaustive-capped`
- `depthReasons: string[]`
- `riskScore: number`
- `sideEffectConfidence: number`
- `verificationEscalation: none|targeted-red-team`
- `compatibilityFlags: string[]`
- `dispatchPlan`
- `dispatchSkips` with `agent`, `reason`, `sourceClass`, `criticalPathEffect`, `evidenceCoveragePreserved`, and `falseNegativeRisk` for every skip; credited speed-proof skips also include `credited: true`, `criticalPathDelta`, and `evidenceCoveragePreserved: true`
- `candidateIntakeGate`
- `evidencePrecisionGate`
- `targetSurfaceCoverageGate`
- `dispatchCompletenessGate`
- `blockedClarifications`
- `baselineAutoRefreshGate`
- `baseline-snapshot.json` with `seriesId`, `metricDirections`, `cumulativeBaseline`, `iterationBaseline`, `currentScore`, `cumulativeImprovementRatio`, `iterationImprovementRatio`, `promotionCandidate`, `sourceRefs`, `capturedAt`, and `status`
- `claimFreshnessGate`
- `heuristicProof`

Performance proof fields:

- `performance.cumulativeBaselineCriticalPathScore`
- `performance.iterationBaselineCriticalPathScore`
- `performance.currentCriticalPathScore`
- `performance.cumulativeImprovementRatio`
- `performance.iterationImprovementRatio`
- `performance.agentCriticalPathGroups`
- `performance.deterministicStageGroups`
- `performance.runProcedureSteps`
- `performance.measurementMethod`

Speed improvement may be claimed only when numeric performance fields are recorded and speed's cumulative and iteration ratios are calculated with `baselineScore / currentScore` because speed is `lower_is_better`. Credited `dispatchSkips` may contribute to the proof only when `credited: true`, `criticalPathDelta`, and `evidenceCoveragePreserved: true` are recorded. Vague wording such as `expected`, `estimated`, or `likely` is not proof.

Current optimized `/tk:gap` contract target keeps cumulative baseline `87.1`, loads iteration baseline from previous main `50.3`, and keeps `currentCriticalPathScore <= 50.3`. Cumulative speed proof remains `87.1 / 50.3 = 1.731...` with display ratio `1.73`; iteration speed ratio is `50.3 / 50.3 = 1.00`, so v7.2.10 makes no new iteration speed improvement claim. Concrete runs must recompute actual run proof from `dispatchPlan`, credited `dispatchSkips`, deterministic stage count, and run procedure step count.

Heuristic proof fields:

- `heuristicProof.cumulativeRequiredImprovementRatio` (fixed at `1.3` for the cumulative target)
- `heuristicProof.iterationRequiredImprovementRatio` (`>1.0` for per-iteration numeric improvement)
- `heuristicProof.falsePositive.metric: accepted_path_blocking_predicate_coverage`
- `heuristicProof.falsePositive.denominator: required_false_positive_predicates`
- `heuristicProof.falsePositive.scoreDirection: higher_is_better`
- `heuristicProof.falsePositive.cumulativeBaseline`
- `heuristicProof.falsePositive.iterationBaseline`
- `heuristicProof.falsePositive.currentScore`
- `heuristicProof.falsePositive.cumulativeImprovementRatio`
- `heuristicProof.falsePositive.iterationImprovementRatio`
- `heuristicProof.falsePositive.improvementFormula`
- `heuristicProof.falsePositive.claimAllowed`
- `heuristicProof.falseNegative.metric: critical_contract_and_target_surface_coverage`
- `heuristicProof.falseNegative.denominator: required_false_negative_predicates`
- `heuristicProof.falseNegative.scoreDirection: higher_is_better`
- `heuristicProof.falseNegative.cumulativeBaseline`
- `heuristicProof.falseNegative.iterationBaseline`
- `heuristicProof.falseNegative.currentScore`
- `heuristicProof.falseNegative.cumulativeImprovementRatio`
- `heuristicProof.falseNegative.iterationImprovementRatio`
- `heuristicProof.falseNegative.improvementFormula`
- `heuristicProof.falseNegative.claimAllowed`
- `heuristicProof.speed.metric: contract_critical_path_score`
- `heuristicProof.speed.scoreDirection: lower_is_better`
- `heuristicProof.speed.cumulativeBaseline`
- `heuristicProof.speed.iterationBaseline`
- `heuristicProof.speed.currentScore`
- `heuristicProof.speed.cumulativeImprovementRatio`
- `heuristicProof.speed.iterationImprovementRatio`
- `heuristicProof.speed.improvementFormula`
- `heuristicProof.speed.claimAllowed`
- `heuristicProof.analysisDepth.metric: hard_trigger_selection_coverage`
- `heuristicProof.analysisDepth.denominator: required_depth_trigger_predicates`
- `heuristicProof.analysisDepth.scoreDirection: higher_is_better`
- `heuristicProof.analysisDepth.cumulativeBaseline`
- `heuristicProof.analysisDepth.iterationBaseline`
- `heuristicProof.analysisDepth.currentScore`
- `heuristicProof.analysisDepth.cumulativeImprovementRatio`
- `heuristicProof.analysisDepth.iterationImprovementRatio`
- `heuristicProof.analysisDepth.improvementFormula`
- `heuristicProof.analysisDepth.claimAllowed`
- `claimFreshnessGate.status`
- `claimFreshnessGate.checkedAfter`
- `claimFreshnessGate.staleInputs`
- `claimFreshnessGate.repairedInputs`
- `heuristicProof.baselineProvenance.registrySourceRef`
- `heuristicProof.baselineProvenance.cumulativeSourceRef`
- `heuristicProof.baselineProvenance.iterationSourceRef`
- `heuristicProof.baselineProvenance.currentSourceRef`
- `heuristicProof.baselineProvenance.capturedFrom`
- `heuristicProof.baselineProvenance.scoreDirectionVerified`
- `heuristicProof.baselineProvenance.autoRefreshVerified`
- `heuristicProof.baselineAutoRefreshGate.status`
- `heuristicProof.baselineAutoRefreshGate.registryPath`
- `heuristicProof.baselineAutoRefreshGate.bootstrapIterationSeed`
- `heuristicProof.baselineAutoRefreshGate.promotionCandidate`
- `heuristicProof.baselineAutoRefreshGate.staleFixedBaselineReuse`
- `heuristicProof.claimAllowed`

Heuristic proof metrics use fixed denominators from the command contract and must record both `cumulativeBaseline` and `iterationBaseline`. False-positive counts accepted-path plus baseline-provenance and baseline-auto-refresh blocking predicates, false-negative counts critical contract/target surface plus baseline-provenance and baseline-auto-refresh predicates, speed uses the critical path score, and analysis depth counts required depth trigger plus baseline provenance and baseline auto-refresh predicates. Higher-is-better metrics use `currentScore / baselineScore`; speed uses `baselineScore / currentScore`. ClaimFreshnessGate is a separate claim gate, not a score denominator. A gap run may claim combined improvement only when all four subproofs record cumulative and iteration ratios, cumulative ratios meet the cumulative target, iteration ratios are `> 1.0`, BaselineAutoRefreshGate proves iteration baseline came from previous refreshed `origin/main`, all four have `claimAllowed: true`, and ClaimFreshnessGate passes.

Contract-level improvement proof target:

```text
falsePositive: cumulativeBaseline = 5, iterationBaseline = 9, currentScore = 9, cumulativeImprovementRatio = 9 / 5 = 1.80, iterationImprovementRatio = 9 / 9 = 1.00 (no new iteration claim)
falseNegative: cumulativeBaseline = 4, iterationBaseline = 8, currentScore = 8, cumulativeImprovementRatio = 8 / 4 = 2.00, iterationImprovementRatio = 8 / 8 = 1.00 (no new iteration claim)
speed: cumulativeBaseline = 87.1, iterationBaseline = 50.3, currentScore <= 50.3, cumulativeImprovementRatio = 87.1 / 50.3 = 1.731... (display 1.73), iterationImprovementRatio = 50.3 / 50.3 = 1.00 (no new iteration claim)
analysisDepth: cumulativeBaseline = 6, iterationBaseline = 10, currentScore = 10, cumulativeImprovementRatio = 10 / 6 = 1.666... (display 1.67), iterationImprovementRatio = 10 / 10 = 1.00 (no new iteration claim)
```

Concrete runs must recompute actual run proof from metadata before claiming improvement. Do not claim new iteration improvement from the fixed cumulative baseline alone; update `iterationBaseline` from the previous main version for each run. BaselineAutoRefreshGate must load `.tigerkit/docs/gap-baselines.json` from refreshed `origin/main`, or use a `bootstrapIterationSeed` from fresh `origin/main` contract score only when the registry does not exist yet. It must write `baseline-snapshot.json` and block iteration claims when `staleFixedBaselineReuse: true` or no registry/seed source exists.

False-negative coverage metadata must include:

- `targetSurfaceCoverageGate.contractsChecked`
- `targetSurfaceCoverageGate.surfacesChecked`
- `targetSurfaceCoverageGate.uncheckedRequiredSurfaces`
- `dispatchCompletenessGate.requiredAgents`
- `dispatchCompletenessGate.skippedAgents`
- `dispatchCompletenessGate.falseNegativeRiskSummary`
- `dispatchCompletenessGate.missedP0P1SearchStatus`

Candidate intake metadata must include:

- `candidateIntakeGate.shape`
- `candidateIntakeGate.evidencePrecision`
- `candidateIntakeGate.producerEvidence`
- `candidateIntakeGate.conflictClarification`
- `candidateIntakeGate.requirementTraceability`
- `candidateIntakeGate.severityScope`
- `candidateIntakeGate.finalQueue`
- `candidateIntakeGate.reasons`

Claim freshness metadata must include:

- `claimFreshnessGate.status`
- `claimFreshnessGate.checkedAfter`
- `claimFreshnessGate.staleInputs`
- `claimFreshnessGate.repairedInputs`

Clarification table shape:

```md
| Ref | Category | Question | Options | Evidence | Impact | Recommendation | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Q1 | implementation-blocking | <질문> | A / B | <근거> | <영향> | <추천> | blocked_pending_user |
```

긴 `CLAR-...` canonical ID는 JSON artifact와 report 상세/참조 영역에 보관합니다.

UI clarification prototype은 오른쪽 border 정렬을 맞춥니다.

```text
Option A
┌────────────────────┐
│ 저장               │
└────────────────────┘

Option B
┌────────────────────┐
│ 변경사항 저장      │
└────────────────────┘
```

Accepted finding uses:

- canonical ID: `FND-YYYYMMDD-HHmmss-RAND-NN`
- user-facing displayRef: `G<N>`
- finalSeverity: `P0`, `P1`, or `P2`
- sourceContracts referencing confirmed, non-superseded contracts
- concrete evidence
- requiredChange engineers can execute without guessing
- confidence `medium` or `high`

Rejected finding uses one of:

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

## `/tk:reflect` Output Contract

- 목적: branch-local working memory에서 durable repo insight만 추출합니다.
- 기본 동작은 `apply=true`입니다.
- `--dry-run`과 `--apply=false`는 preview-only입니다.
- 기본 apply target은 `CLAUDE.md` 또는 `.claude/rules/**/*.md`입니다.
- `.claude/tigerkit/` 아래에는 durable insight를 저장하지 않습니다.
- source code는 수정하지 않습니다.
- content write는 `CLAUDE.md` 또는 `.claude/rules/**/*.md`만 수정합니다.
- branch recency bookkeeping으로 `global-index.json`의 `lastUsedAt`은 갱신할 수 있습니다.
- 같은 insight를 중복 반영하지 않습니다.

기본 stdout:

```text
Reflect 완료
Apply: true
적용 대상:
- CLAUDE.md
- .claude/rules/<path>.md

적용 결과:
- <added> added
- <updated> updated
- <skipped> skipped as duplicate

요약:
- <한글 insight summary>
```

Dry-run stdout:

```text
Reflect 완료
Apply: false
예상 대상:
- CLAUDE.md
- .claude/rules/<path>.md

미리보기 결과:
- <added> would add
- <updated> would update
- <skipped> skipped as duplicate

요약:
- <한글 preview summary>
```

Reflect excludes:

- branch-specific one-off decision
- temporary Spec Patch itself
- superseded decision
- P3/nit
- rejected finding
- low-confidence observation
- unresolved source conflict
- 별도 `tigerkit-reflections.md` sidecar 생성

## `/tk:handoff` Output Contract

- 목적: 다음 세션이나 다른 작업자가 이어받을 continuation 문서를 작성합니다.
- 기본 기록 위치: `.claude/handoffs/current.md`
- `archive=true` 또는 사용자 명시 archive 요청이 있을 때만 dated archive를 추가로 만듭니다.
- v7.2에서는 최신 branch-local Spec Patch와 Gap Run path를 Relevant Files 또는 Validation에 포함할 수 있습니다.
- handoff는 durable rule 저장소가 아닙니다.

채팅 receipt:

```text
handoff 작성했습니다.
- 기록: .claude/handoffs/current.md
- archive: 없음
- next action: .claude/handoffs/current.md 읽고 Next Actions부터 이어가.
```

필수 section:

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

## `/tk:meta-feedback` Output Contract

- 목적: 현재 세션에서 관측된 TigerKit command/skill 개선점을 프로젝트 자산 유출 없이 일반화합니다.
- 세션 내역 전체에서 friction, 사용자 교정, 반복 실수, output UX 문제, latency 문제, false-positive pattern을 찾습니다.
- 기본값은 proposal-only입니다.
- `--out <path>`가 있을 때만 current worktree root 내부 지정 경로에 파일을 작성할 수 있습니다.
- worktree root 밖 경로, user home, `/tmp`, hidden control file path에는 쓰지 않습니다.
- raw session evidence, 사용자 원문 quote, repo 이름, product 이름, 도메인 고유명, 내부 path, URL, ticket, branch, PR 번호, commit hash를 출력하지 않습니다.
- repo rule patch는 `/tk:reflect`, basis-target 비교는 `/tk:gap` 대상으로 분리합니다.

필수 section:

```md
## Meta Feedback Summary
- Target: <skill-or-command>
- Feedback class: <ux|output-format|taxonomy|safety|dispatch|docs|performance|false-positive>
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

안전하게 일반화할 수 없으면 `Privacy status: cannot_generalize_safely`, `Change: none`, `Why: privacy gate failed`를 사용합니다.

## Evidence Rule

중요 판단은 아래 구분을 유지합니다.

```text
Evidence = directly observed
Interpretation = inferred from evidence
Decision = confirmed by user or source contract
Suggestion = proposed, not confirmed
```

## Storage Rule

`spec`, `gap` generated artifacts는 current worktree root 아래 `.claude/tigerkit/branches/<branch-key>/`에 저장합니다.

금지:

- `/tmp`
- `$GIT_COMMON_DIR`
- `.git/worktrees/*`
- user home global path
- current worktree root 밖 path

## detail 원칙

- command별 stdout은 필요한 만큼만 작성합니다.
- 다음 행동은 자연어로 짧게 제시합니다.
- 근거가 부족한 항목은 추측하지 않고 `unknown`, rejected, 또는 source conflict로 둡니다.
