# TigerKit 운영 Output Contract

이 문서는 TigerKit v8.0 command의 출력 계약을 정의합니다. 사용 흐름은 `.tigerkit/docs/usage.md`, 산출물 위치는 `.tigerkit/docs/artifact-layout.md`를 기준으로 봅니다.

```text
stdout is a receipt. Full gap bodies are saved as branch-local artifacts unless explicit print option is used.
```

## 공통 원칙

기본 응답은 아래 네 가지에 집중합니다.

1. outcome
2. branch scope
3. artifact paths when files are written
4. counts, risks, capability/skip reason, next action

상세 본문은 파일에 저장하고, 각 command가 지원하는 explicit print option을 지정한 경우에만 stdout에 함께 출력합니다. v8 MVP 공개 command surface에서는 `/tk:gap`의 `--print-report`가 이에 해당합니다.

사용자 대화에 보이는 안내, 추천, 요약, next action은 계약용어, path, identifier, field name을 제외하고 한글로 씁니다.

Hook guard는 repo 유지보수용 command/docs sync나 eval JSON 점검이 아니라 플러그인 사용자가 실제로 보는 receipt, artifact path, finding Ref, explicit print option 경계를 보호할 때만 둡니다. 그런 user-facing guard 표면이 없으면 hook을 추가하지 않습니다.

## Legacy Spec Patch note

v8 MVP는 `/tk:spec` command를 공개하지 않습니다. 기존 `.claude/tigerkit/branches/<branch-key>/specs/` 자료가 있으면 `/tk:gap`이 source material 후보로 읽을 수 있지만, 출력 계약의 대상은 아닙니다.

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

```tigerkit-gap-status
status: GAP_READY | GAP_BLOCKED
workflow_id: WF-YYYYMMDD-HHmmss-RAND | null
workflow_path: .claude/tigerkit/branches/<branch-key>/gap/<WF-ID>.md | null
workflow_sha256: <sha256> | null
blocked_reasons: []
human_decisions: []
missing_sources: []
```

### `tigerkit-launch-workflow` block

`GAP_READY` artifact는 정확히 하나의 named fenced block을 포함합니다. 이 block은 `/tk:launch`가 소비하는 sealed workflow contract입니다. `workflow_sha256`은 이 block 안에 넣지 않습니다.

```tigerkit-launch-workflow
version: 1
workspace_context:
  root: <absolute path>
  scope_kind: git_branch | git_detached | git_no_remote | workspace
  scope_key: <stable key>
  git:
    available: true | false
    commit_available: true | false
  github:
    remote_available: true | false
    issue_pr_available: true | false
workflow_id: WF-YYYYMMDD-HHmmss-RAND
created_at: <ISO-8601>
source_refs: []
mission: <one sentence>
scope: []
non_goals: []
human_decisions: []
assumptions: []
rejected_assumptions: []
tasks:
  - id: T1
    title: <short title>
    goal: <task goal>
    files: []
    depends_on: []
    allowed_changes: []
    forbidden_changes: []
    assumed_preconditions:
      - id: PC1
        predicate: <checkable read-only predicate>
        evidence: <path/ref/command id>
        required: true
        failure_abort_code: HUMAN_DECISION_REQUIRED | VERIFICATION_UNAVAILABLE | WORKTREE_CONTEXT_APPROVAL_REQUIRED
    success_conditions: []
    verification: []
    abort_conditions: []
readonly_preflight:
  status: passed | blocked
  checked_preconditions: []
  checked_verification_gates: []
  blocked_reasons: []
autopilot_policy:
  allowed: false
  max_recovery_attempts: 0
  max_task_retries: 0
  forbidden: []
commit_policy:
  mode: preflight_decision_required | skip | commit_on_success
  allowed: false
  commit_available: true | false
  skip_reason: null | not_git_repo | no_commit_requested | github_unavailable | readonly_workspace
reflect_policy:
  mode: generated_report_only
  durable_apply_requires_preflight_approval: true
```

### `tigerkit-launch-workflow` seal

`workflow_sha256`은 단일 `tigerkit-launch-workflow` fenced block body의 SHA-256이며, `tigerkit-gap-status`와 `branch-state.json`에 기록하는 외부 seal입니다. `tigerkit-launch-workflow` block 내부에 자기참조 field로 넣지 않습니다.

- opening fence와 closing fence line은 제외합니다.
- block body는 LF로 정규화합니다.
- hashing 전 final LF를 정확히 하나 보장합니다.
- YAML-normalize 또는 key sort를 하지 않습니다.
- archive workflow 파일이 authoritative입니다. `current.md`는 최신 copy입니다. `/tk:launch`는 archive block hash, `current.md` block hash, branch-state hash가 일치하지 않으면 `WORKFLOW_HASH_MISMATCH`로 중단합니다.

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

- 목적: sealed launch workflow를 `tk-runner` subagent로 실행하고 verification gate 결과, runtime harness, abort reason, reflect trace를 branch-local artifact로 남깁니다.
- 기본 입력은 `.claude/tigerkit/branches/<branch-key>/gap/current.md` 또는 명시 workflow path입니다.
- `tigerkit-launch-workflow` block은 정확히 하나여야 합니다.
- hash mismatch, missing workflow, multiple blocks, blocked workflow는 실행 전 abort합니다.
- 각 task의 required `assumed_preconditions`는 mutation 전에 read-only로 확인합니다.
- mid-flight 질문은 금지합니다. 새 결정이 필요하면 `HUMAN_DECISION_REQUIRED`로 abort합니다.
- Phase 1에서 `--autopilot` recovery는 실행하지 않습니다.
- commit은 preflight approval evidence 없이는 금지합니다.
- `TIGERKIT_SESSION_START` worktree context proposal은 SessionStart additional context에서 소비합니다. Command마다 같은 후보를 다시 스캔하거나 다시 묻지 않습니다.
- 자동 symlink/copy는 하지 않습니다.
- workflow가 worktree context 적용을 required precondition으로 두었는데 승인/evidence가 없으면 `WORKTREE_CONTEXT_APPROVAL_REQUIRED`로 task 실행 전 abort합니다.
- required `tk-runner`/model harness가 unavailable이면 `MODEL_HARNESS_UNAVAILABLE`로 abort합니다.

### `tigerkit-launch-receipt` block

Launch report는 사람용 H2와 별도로 정확히 하나의 machine-readable block을 포함합니다.

```tigerkit-launch-receipt
version: 1
launch_id: LCH-YYYYMMDD-HHmmss-RAND
workflow_id: WF-YYYYMMDD-HHmmss-RAND
workflow_path: .claude/tigerkit/branches/<branch-key>/gap/<WF-ID>.md
workflow_sha256: <sha256>
status: SUCCESS_NO_COMMIT | SUCCESS_COMMITTED | ABORTED | FAILED_PREFLIGHT
abort_code: null | WORKFLOW_NOT_FOUND | MULTIPLE_WORKFLOW_BLOCKS | WORKFLOW_HASH_MISMATCH | GAP_BLOCKED | HUMAN_DECISION_REQUIRED | MODEL_HARNESS_UNAVAILABLE | WORKTREE_CONTEXT_APPROVAL_REQUIRED | AUTOPILOT_DISABLED | AUTOPILOT_NOT_IMPLEMENTED_IN_PHASE1 | OUT_OF_SCOPE_DIFF | VERIFICATION_FAILED | ARTIFACT_ROOT_UNWRITABLE | COMMIT_REQUIRED_UNAVAILABLE | GITHUB_REQUIRED_UNAVAILABLE | VERIFICATION_UNAVAILABLE
runtime_harness:
  role: tk-runner
  expected_host_binding: claude_code_agent
  expected_model: sonnet
  model_tier: balanced
  effort_tier: medium
  status: active | fallback_inline | unavailable
  fallback_reason: null | agent_unavailable | host_does_not_support_subagents | model_binding_unobservable
worktree_context:
  detected: true | false
  linked_worktree: true | false
  source_worktree: <absolute path|null>
  missing_root_markdown: []
  missing_claude_dir: true | false
  proposal_only: true
  approval_required: true | false
  approval_present: true | false
  candidate_signature: <sha256|null>
  decline_marker: .claude/tigerkit/local/session-start/worktree-context-declines.json | null
  suppressed_by_decline: true | false
preconditions:
  checked: []
  failed: []
abort_feedback:
  reusable_gap_input: true | false
  failed_task: <T-ID|null>
  failed_precondition: <ID|null>
  failed_gate: <VG-ID|null>
  observed_evidence: []
  required_decision: <text|null>
commit_created: false
commit_status: created | skipped_preflight_required | skipped_not_requested | skipped_not_git_repo | skipped_no_github_remote | skipped_readonly_workspace | skipped_commit_policy_skip
reflect_report_path: .claude/tigerkit/branches/<branch-key>/reflect/<RFL-ID>.md
reflect_current_path: .claude/tigerkit/branches/<branch-key>/reflect/current.md
```

SUCCESS stdout:

```text
✅ Launch 완료: <LCH-ID>
Branch Scope: <branch-key>
Workflow: .claude/tigerkit/branches/<branch-key>/gap/<WF-ID>.md
Workflow Hash: <sha256>
결과: SUCCESS

Runtime Harness: tk-runner / model=sonnet / status=<active|fallback_inline|unavailable>
Worktree Context: <none|proposal:<count>|approval_required>
Tasks: <done>/<total>
Verification Gates: <passed>/<total>
Commit: <created|skipped_preflight_required|skipped_not_requested|skipped_not_git_repo|skipped_no_github_remote|skipped_readonly_workspace|skipped_commit_policy_skip>

Report: .claude/tigerkit/branches/<branch-key>/launch/<LCH-ID>.md
Current: .claude/tigerkit/branches/<branch-key>/launch/current.md
Reflect: .claude/tigerkit/branches/<branch-key>/reflect/<RFL-ID>.md
Reflect Current: .claude/tigerkit/branches/<branch-key>/reflect/current.md

다음 행동: <없음|reflect 제안 검토|commit 승인 필요>
```

ABORTED stdout:

```text
🛑 Launch 중단: <LCH-ID>
Branch Scope: <branch-key>
Workflow: .claude/tigerkit/branches/<branch-key>/gap/<WF-ID>.md
Workflow Hash: <sha256|unknown>
결과: ABORTED
Abort Code: <CODE>
원인: <한글 1줄>

Runtime Harness: tk-runner / model=sonnet / status=<active|fallback_inline|unavailable>
Worktree Context: <none|proposal:<count>|approval_required>
Completed Tasks: <done>/<total>
Failed Gate: <VG-ID|없음>

Report: .claude/tigerkit/branches/<branch-key>/launch/<LCH-ID>.md
Current: .claude/tigerkit/branches/<branch-key>/launch/current.md
Reflect: .claude/tigerkit/branches/<branch-key>/reflect/<RFL-ID>.md
Reflect Current: .claude/tigerkit/branches/<branch-key>/reflect/current.md

다음 행동: <human decision|workflow 재생성|scope 조정|검증 실패 수정>
```

상태 기호는 첫 줄에만 씁니다. Logical group 사이에는 빈 줄을 두어 receipt를 읽기 쉽게 만듭니다.

Abort code 목록:

- `WORKFLOW_NOT_FOUND`
- `MULTIPLE_WORKFLOW_BLOCKS`
- `WORKFLOW_HASH_MISMATCH`
- `GAP_BLOCKED`
- `HUMAN_DECISION_REQUIRED`
- `MODEL_HARNESS_UNAVAILABLE`
- `WORKTREE_CONTEXT_APPROVAL_REQUIRED`
- `AUTOPILOT_DISABLED`
- `AUTOPILOT_NOT_IMPLEMENTED_IN_PHASE1`
- `OUT_OF_SCOPE_DIFF`
- `VERIFICATION_FAILED`
- `ARTIFACT_ROOT_UNWRITABLE`
- `COMMIT_REQUIRED_UNAVAILABLE`
- `GITHUB_REQUIRED_UNAVAILABLE`
- `VERIFICATION_UNAVAILABLE`

## `/tk:next` Output Contract

- 목적: 현재 TigerKit artifact와 workspace/repo context를 읽고 다음 안전 실행 항목 하나를 실제로 이어서 시도합니다.
- `/tk:next`는 추천 전용 stdout-only utility가 아닙니다. 안전하게 할 수 있는 작업이 있으면 수행하고 receipt를 남깁니다.
- sealed workflow가 필요한 구현은 `/tk:gap → /tk:launch`를 우회하지 않습니다.
- commit, push, PR, merge, release, deploy, GitHub issue write 같은 외부 side effect는 사용자 승인 또는 artifact상의 명시 approval 없이는 수행하지 않습니다.
- missing artifact는 오류가 아니라 다음 행동 판단 근거입니다.

기본 receipt 위치:

```text
.claude/tigerkit/branches/<branch-key>/next/NXT-YYYYMMDD-HHmmss-RAND.md
.claude/tigerkit/branches/<branch-key>/next/current.md
```

Machine-readable block:

```tigerkit-next-receipt
version: 1
next_id: NXT-YYYYMMDD-HHmmss-RAND
scope_kind: git_branch | git_detached | git_no_remote | workspace
scope_key: <branch-key-or-workspace-key>
status: NEXT_DONE | NEXT_PARTIAL | NEXT_BLOCKED | NEXT_SKIPPED
selected_action:
  source: user | handoff | gap | launch | reflect | worktree_context | repo_state | none
  ref: <path#section or none>
  summary: <one sentence>
worktree_context:
  detected: true | false
  proposal_only: true | false
  candidates: []
executed_actions: []
changed_files: []
verification: []
approval:
  required: true | false
  present: true | false
  source_ref: <message|artifact|none>
blocked_by: []
next_action: <one sentence or 없음>
```

기본 stdout:

```text
✅ Next 완료: <NXT-ID>
Branch Scope: <branch-key>
결과: NEXT_DONE | NEXT_PARTIAL | NEXT_BLOCKED | NEXT_SKIPPED
Selected Action: <한글 한 문장>

Executed: <count>
Changed Files: <count>
Verification: <passed>/<total> | not_run:<reason>
Approval: <not_required|present:<source>|missing:<needed_action>>

Report: .claude/tigerkit/branches/<branch-key>/next/<NXT-ID>.md
Current: .claude/tigerkit/branches/<branch-key>/next/current.md
Blocked By: <none | human decision | missing source | approval required | sealed workflow required | dirty workspace | verification failure | worktree context approval required | capability unavailable | other>

다음 행동: <없음|한글 한 문장>
```

상태 기호:

- `✅` = `NEXT_DONE`
- `⚠️` = `NEXT_PARTIAL`
- `🛑` = `NEXT_BLOCKED`
- `⏭️` = `NEXT_SKIPPED`

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


### `tigerkit-reflect-report` block

Reflect report는 정확히 하나의 machine-readable block을 포함합니다.

```tigerkit-reflect-report
version: 1
reflect_id: RFL-YYYYMMDD-HHmmss-RAND
workflow_id: WF-YYYYMMDD-HHmmss-RAND
launch_id: LCH-YYYYMMDD-HHmmss-RAND
mode: generated_report_only | durable_apply
applied: []
skipped: []
proposal_only: []
user_memory_candidates: []
```

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

User-level Memory Candidates:
- <candidate or None>
  Auto-applied: false

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

User-level Memory Candidates:
- <candidate or None>
  Auto-applied: false

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

User-level Memory Candidates:
- <candidate or None>
  Auto-applied: false

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
