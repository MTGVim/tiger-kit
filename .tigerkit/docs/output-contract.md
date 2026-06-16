# TigerKit 운영 Output Contract

이 문서는 TigerKit v8.0 command의 출력 계약을 정의합니다. 사용 흐름은 `.tigerkit/docs/usage.md`, 산출물 위치는 `.tigerkit/docs/artifact-layout.md`를 기준으로 봅니다.

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

Hook guard는 repo 유지보수용 command/docs sync나 eval JSON 점검이 아니라 플러그인 사용자가 실제로 보는 receipt, artifact path, finding Ref, explicit print option 경계를 보호할 때만 둡니다. 그런 user-facing guard 표면이 없으면 hook을 추가하지 않습니다.

## `/tk:spec` Output Contract

- 목적: raw instruction을 현재 branch-local Spec Patch로 저장합니다.
- source material과 authority를 분리합니다. confirmed 또는 명시 scope가 있는 항목만 gap evidence 후보가 됩니다.
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

이 section은 v8.0 기본 `/tk:gap` stdout의 authoritative contract입니다. `/tk:gap --review` compatibility stdout은 아래 `/tk:gap --review` section을 따릅니다.

- 목적: source를 ground하고 ambiguity를 attack한 뒤 launch 가능한 sealed workflow를 만들거나 launch 금지 사유를 기록합니다.
- `/tk:gap`은 반드시 `GAP_READY` 또는 `GAP_BLOCKED` 중 하나로 끝납니다.
- `GAP_READY`는 정확히 하나의 `tigerkit-launch-workflow` block을 포함해야 합니다.
- `GAP_BLOCKED`는 `tigerkit-launch-workflow` block을 포함하면 안 됩니다.
- 기본 workflow archive 위치: `.claude/tigerkit/branches/<branch-key>/gap/<WF-ID>.md`
- 최신 workflow pointer copy: `.claude/tigerkit/branches/<branch-key>/gap/current.md`

### `/tk:gap default stdout`

`GAP_READY` stdout:

```text
GAP_READY: <WF-ID>
Branch Scope: <branch-key>
Workflow: .claude/tigerkit/branches/<branch-key>/gap/<WF-ID>.md
Workflow Hash: <sha256>
Tasks: <count>
Verification Gates: <count>
Autopilot Allowed: false
Commit Policy: preflight_decision_required
다음 행동: /tk:launch
```

`GAP_BLOCKED` stdout:

```text
GAP_BLOCKED: <GAP-ID>
Branch Scope: <branch-key>
Blocked Reasons: <count>
Human Decisions: <count>
Missing Sources: <count>
Report: .claude/tigerkit/branches/<branch-key>/gap/<GAP-ID>.md
다음 행동: <Q1 확인 후 /tk:gap 재실행|source 제공 필요>
```

### `tigerkit-gap-status` block

```yaml
status: GAP_READY | GAP_BLOCKED
workflow_id: WF-YYYYMMDD-HHmmss-RAND | null
workflow_path: .claude/tigerkit/branches/<branch-key>/gap/<WF-ID>.md | null
workflow_sha256: <sha256> | null
blocked_reasons: []
human_decisions: []
missing_sources: []
```

### `tigerkit-launch-workflow` seal

`workflow_sha256`은 단일 `tigerkit-launch-workflow` fenced block body의 SHA-256입니다.

- opening fence와 closing fence line은 제외합니다.
- block body는 LF로 정규화합니다.
- hashing 전 final LF를 정확히 하나 보장합니다.
- YAML-normalize 또는 key sort를 하지 않습니다.
- archive workflow 파일이 authoritative입니다. `current.md`는 최신 copy입니다.

## `/tk:gap --review` Output Contract

이 section은 v7 Contract-based Gap Review compatibility stdout의 authoritative contract입니다. `commands/gap.md`, `.claude/rules/review/gap-analysis.md`, `evals/evals.json`은 이 section을 기준으로 사용자-facing stdout과 artifact 노출을 맞춥니다.

- 목적: Product/Design Spec contract와 implementation plan/current implementation을 비교해 사용자가 바로 고치거나 확인할 항목만 남깁니다.
- 기본 저장 위치: `.claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/`
- 기본 산출물은 `report.md`와 `run.json`입니다.
- `/tk:gap`은 단일 `/tk:gap` 실행로 실행합니다.
- `--lite`와 `--strict`는 compatibility flag로만 기록하며 user-facing quality mode가 아닙니다.
- `--maintainer-proof`는 maintainer/self-eval 전용입니다. 일반 사용자 품질 모드나 더 강한 gap 분석 옵션처럼 표현하지 않습니다.
- subagent는 final finding을 확정하지 못합니다.
- candidate의 file:line, module-path, rendered output evidence는 JudgeMergerAgent queue 진입 전에 현재 target surface에서 read-back으로 재확인합니다.
- producer-absence claim은 producer-side evidence gate를 통과해야 합니다.
- user-provided source, referenced source, repo에서 접근 가능한 API contract/schema/endpoint/serializer/data model이 있으면 사용자에게 묻기 전에 먼저 확인합니다.
- source set이 크면 source-by-source locked intake를 권장하고, report/run record에는 source별 source_type, access status, lock status, derived Contract 상태를 분리해 남깁니다.
- design evidence는 `structural_context`와 `visual_capture`를 구분합니다. `visual_capture`만으로 색·간격·치수 같은 numeric design value를 confirmed contract로 확정하지 않습니다. 기존 구현은 대조·추론 보조로만 쓰며 design SOT가 아닙니다.
- consumer-only fallback/default/mapper evidence는 producer absence accepted finding이나 `SourceConflict`로 승격하지 않습니다.
- `missing_producer_evidence`는 숨기지 않습니다. 기본 stdout에서는 `Clarification Needed`로 짧게 보여주고, 확인한 producer surface와 missing evidence 상세는 `report.md`에 둡니다.
- ambiguity와 source conflict는 Judge accept path 전에 `Clarification Needed` 또는 `SourceConflict`로 기록합니다.
- JudgeMergerAgent만 final accepted finding을 확정합니다.
- 유저향 stdout/report table은 run-local short Ref(`G1`, `R1`, `C1`, `Q1`)를 우선 표시하고 긴 canonical ID는 `run.json` 또는 maintainer proof artifact에 보관합니다.
- `mode`, `preset`, `lite`, `strict`는 stdout에서 품질 선택지처럼 표시하지 않습니다. compatibility flag로 언급해야 할 때도 quality mode나 추천 preset으로 쓰지 않습니다.
- final finding에는 P0/P1/P2만 포함합니다.
- P3/nit/duplicate/unverifiable/source_conflict는 final finding으로 출력하지 않습니다.
- finding이 안 나올 때까지 반복하지 않습니다.

### `/tk:gap --review default stdout`

기본 stdout은 compact receipt입니다. 아래 필드는 항상 이 순서로 출력합니다.

```text
Gap Review 완료: <GAP-ID>
Branch Scope: <branch-key>
결과: P0 <count> / P1 <count> / P2 <count> / Source Conflicts <count> / Clarification Needed <count>
Report: .claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/report.md
Run JSON: .claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/run.json
다음 행동: <G1 먼저 수정|Q1 확인 필요|없음>

Actionable Findings:
| Ref | Sev | 요약 | Required change |
| --- | --- | --- | --- |
| G1 | P1 | <final finding 1줄 요약> | <수정 방향 1줄> |

Clarification Needed:
| Ref | 질문 | 추천 |
| --- | --- | --- |
| Q1 | <확인 질문 1줄> | <추천 1줄> |
```

`Actionable Findings`는 accepted finding이 있을 때만 출력합니다. `Clarification Needed`는 확인 질문이 있을 때만 출력합니다. 둘 다 없으면 table 대신 `다음 행동: 없음`만 출력합니다.

`--print-report`가 있을 때만 저장된 `report.md` 본문을 stdout에 추가 출력합니다. `--maintainer-proof`가 있어도 기본 stdout은 위 receipt와 compact table 경계를 유지하고, maintainer proof artifact list나 proof metadata를 dump하지 않습니다.

Default stdout에 아래 항목을 직접 출력하지 않습니다. 기본 `report.md`와 `run.json`에도 proof/self-eval metadata를 필수로 요구하지 않습니다.

- quality gate dump
- analysis depth proof와 확장 이유 dump
- risk score, side-effect confidence
- verification escalation
- dispatch plan/skip proof
- target surface coverage proof
- performance proof
- heuristic proof
- baseline refresh
- proof freshness
- rejected/downgraded observation 상세 목록
- artifact file list
- false-positive/false-negative/speed/analysis-depth improvement claim

기본 `run.json` 필드:

```text
runId
command
branchScope
status
reportPath
runJsonPath
maintainerProofEnabled: false
sourceRefs
sourceIntake
counts
findings
clarifications
sourceConflicts
rejectedSummary
displayRefs
checkedEvidenceRefs
nextAction
```

기본 `report.md` H2:

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

`## Sources Used`에는 source별 `source_type`, access status, lock status, raw reference, derived Contract 상태를 구분해 둡니다. 대량 source는 source 단위 lock 시점을 남기고, visual capture가 numeric design value의 단독 근거인지 여부를 표시합니다.

`## Actionable Findings`에는 accepted P0/P1/P2 final finding만 둡니다.

`## Clarification Needed`는 implementation-blocking과 reference-only를 구분합니다. 질문은 option/evidence/impact/recommendation/status를 표로 제시합니다.

`## Next Action Graph`는 full runner가 아니라 run-local Ref 기반 graph-lite 순서 안내입니다. clarification dependency, finding 선후관계, re-check, re-run 순서만 짧게 표현합니다.

Clarification table shape:

```md
| Ref | Category | Question | Options | Evidence | Impact | Recommendation | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Q1 | implementation-blocking | <질문> | A / B | <근거> | <영향> | <추천> | blocked_pending_user |
```

긴 `CLAR-...` canonical ID는 `run.json` 또는 maintainer proof artifact에 보관합니다.

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

### `/tk:gap --maintainer-proof` Output Contract

`--maintainer-proof`를 명시한 경우에만 self-eval/performance proof와 내부 gate/debug metadata를 생성하거나 claim할 수 있습니다.

Maintainer proof artifact location:

```text
.claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/maintainer-proof/
```

Maintainer proof mode에서만 아래 metadata가 허용됩니다.

- `input-manifest.json`
- `contracts.json`
- `candidates.json`
- `judge-result.json`
- `baseline-snapshot.json`
- `proof.json`
- `qualityGates`
- `analysisDepth`, `depthReasons`, `riskScore`, `sideEffectConfidence`
- `verificationEscalation`, `compatibilityFlags`
- `dispatchPlan`, `dispatchSkips`
- `candidateIntakeGate`, `evidencePrecisionGate`
- `targetSurfaceCoverageGate`, `dispatchCompletenessGate`
- `baselineAutoRefreshGate`, `claimFreshnessGate`
- `performance`
- `heuristicProof`

Speed improvement may be claimed only in maintainer proof mode when numeric performance fields are recorded and speed's cumulative and iteration ratios are calculated with `baselineScore / currentScore` because speed is `lower_is_better`. Credited `dispatchSkips` may contribute to the proof only when `credited: true`, `criticalPathDelta`, and `evidenceCoveragePreserved: true` are recorded. Vague wording such as `expected`, `estimated`, or `likely` is not proof.

Heuristic proof metrics use fixed denominators from the command contract and must record both `cumulativeBaseline` and `iterationBaseline`. Higher-is-better metrics use `currentScore / baselineScore`; speed uses `baselineScore / currentScore`. ClaimFreshnessGate is a separate claim gate, not a score denominator. A gap run may claim combined improvement only when all four subproofs record cumulative and iteration ratios, cumulative ratios meet the cumulative target, iteration ratios are `> 1.0`, BaselineAutoRefreshGate proves iteration baseline came from previous refreshed `origin/main`, all four have `claimAllowed: true`, and ClaimFreshnessGate passes.

Concrete maintainer proof runs must recompute actual run proof from metadata before claiming improvement. Do not claim new iteration improvement from the fixed cumulative baseline alone; update `iterationBaseline` from the previous main version for each run.

## `/tk:launch` Output Contract

- 목적: sealed launch workflow를 실행하고 verification gate 결과, abort reason, reflect trace를 branch-local artifact로 남깁니다.
- 기본 입력은 `.claude/tigerkit/branches/<branch-key>/gap/current.md` 또는 명시 workflow path입니다.
- `tigerkit-launch-workflow` block은 정확히 하나여야 합니다.
- hash mismatch, missing workflow, multiple blocks, blocked workflow는 실행 전 abort합니다.
- mid-flight 질문은 금지합니다. 새 결정이 필요하면 `HUMAN_DECISION_REQUIRED`로 abort합니다.
- Phase 1에서 `--autopilot` recovery는 실행하지 않습니다.
- commit은 preflight approval evidence 없이는 금지합니다.

SUCCESS stdout:

```text
Launch 완료: <LCH-ID>
Branch Scope: <branch-key>
Workflow: .claude/tigerkit/branches/<branch-key>/gap/<WF-ID>.md
Workflow Hash: <sha256>
결과: SUCCESS
Tasks: <done>/<total>
Verification Gates: <passed>/<total>
Commit: <created|skipped_preflight_required|skipped_not_requested>
Report: .claude/tigerkit/branches/<branch-key>/launches/<LCH-ID>/report.md
Reflect: .claude/tigerkit/branches/<branch-key>/launches/<LCH-ID>/reflect-report.md
다음 행동: <없음|reflect 제안 검토|commit 승인 필요>
```

ABORTED stdout:

```text
Launch 중단: <LCH-ID>
Branch Scope: <branch-key>
Workflow: .claude/tigerkit/branches/<branch-key>/gap/<WF-ID>.md
Workflow Hash: <sha256|unknown>
결과: ABORTED
Abort Code: <CODE>
원인: <한글 1줄>
Completed Tasks: <done>/<total>
Failed Gate: <VG-ID|없음>
Report: .claude/tigerkit/branches/<branch-key>/launches/<LCH-ID>/report.md
Reflect: .claude/tigerkit/branches/<branch-key>/launches/<LCH-ID>/reflect-report.md
다음 행동: <human decision|workflow 재생성|scope 조정|검증 실패 수정>
```

Abort code 목록:

- `WORKFLOW_NOT_FOUND`
- `MULTIPLE_WORKFLOW_BLOCKS`
- `WORKFLOW_HASH_MISMATCH`
- `GAP_BLOCKED`
- `HUMAN_DECISION_REQUIRED`
- `AUTOPILOT_DISABLED`
- `AUTOPILOT_NOT_IMPLEMENTED_IN_PHASE1`
- `OUT_OF_SCOPE_DIFF`
- `HYDRATION_CONFLICT`
- `VERIFICATION_FAILED`

## `/tk:reflect` Output Contract

- 목적: branch-local working memory와 gap+launch trace에서 durable repo insight만 추출합니다.
- 기본 동작은 `apply=true`입니다.
- 반영할 durable insight가 없으면 파일을 수정하지 않는 정상 성공이 가능합니다.
- `--dry-run`과 `--apply=false`는 preview-only입니다.
- 기본 apply target은 `CLAUDE.md` 또는 `.claude/rules/**/*.md`입니다.
- `.claude/tigerkit/` 아래에는 durable insight를 저장하지 않습니다.
- source code는 수정하지 않습니다.
- content write는 `CLAUDE.md` 또는 `.claude/rules/**/*.md`만 수정합니다.
- branch recency bookkeeping으로 `global-index.json`의 branch entry를 생성하거나 `lastUsedAt`을 갱신할 수 있습니다.
- branch-local specs/gap 산출물이 없다는 사실만으로 세션 관측 패턴을 durable insight 후보로 승격하지 않습니다.
- 같은 insight를 중복 반영하지 않습니다.
- 기존 durable guidance inventory 후 Frequency, Cost, Risk, Stability, Coverage rubric으로 후보를 평가합니다.
- 근거가 부족한 후보는 `Needs more evidence`로 남기고 durable rule로 승격하지 않습니다.
- reflect 처리 직후 `/tk:meta-feedback`을 proposal-only로 함께 제출합니다.
- `--no-meta-feedback` 또는 `--meta-feedback=false`가 있으면 meta-feedback 제출을 생략합니다.

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

Needs more evidence:
- <확인 필요 항목 또는 None>

Meta Feedback:
- submitted
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

Needs more evidence:
- <확인 필요 항목 또는 None>

Meta Feedback:
- submitted
```

`--no-meta-feedback` 또는 `--meta-feedback=false`가 있으면 `Meta Feedback: skipped by opt-out`으로 출력합니다.

Reflect no-op success:

```text
Reflect 완료
Apply: true
적용 대상:
- 없음

적용 결과:
- 0 added
- 0 updated
- <skipped> skipped as duplicate
- <no_action> no action

요약:
- No durable insight promoted.

Needs more evidence:
- <확인 필요 항목 또는 None>

Meta Feedback:
- submitted
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
- canonical 기록 위치: `.claude/tigerkit/branches/<branch-key>/handoffs/current.md`
- 최신 handoff path는 `.claude/tigerkit/global-index.json`의 current branch entry에 `latestHandoffPath`로 함께 기록합니다.
- 경로를 지정하지 않은 resume 지시는 `.claude/tigerkit/global-index.json`의 `latestHandoffPath`를 1순위로 조회합니다.
- 현재 작업을 방해하면 안 되는 follow-up은 `Pending Backlog`에 source/evidence/priority/blocked-by/next action과 함께 저장할 수 있습니다.
- `archive=true` 또는 사용자 명시 archive 요청이 있을 때만 branch-local dated archive를 추가로 만듭니다.
- `.claude/handoffs/current.md`는 optional convenience pointer이며 canonical handoff를 대체하지 않습니다.
- v8.0에서는 최신 branch-local Spec Patch, Gap workflow, Launch Run path를 Relevant Files 또는 Validation에 포함할 수 있습니다.
- handoff는 durable rule 저장소가 아닙니다.

채팅 receipt:

```text
handoff 작성했습니다.
- 기록: .claude/tigerkit/branches/<branch-key>/handoffs/current.md
- index pointer: .claude/tigerkit/global-index.json 갱신
- archive: 없음
- pointer: 없음
- next action: .claude/tigerkit/global-index.json의 latestHandoffPath를 확인하고 Next Actions부터 이어가.
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
## Pending Backlog
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
- repo rule patch는 `/tk:reflect`, basis-target 비교는 `/tk:gap`, follow-up 보관은 `/tk:handoff` 대상으로 분리합니다.
- agent runtime/config, MCP permission, custom agent 추천은 TigerKit 본체 범위 밖으로 둡니다.

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
