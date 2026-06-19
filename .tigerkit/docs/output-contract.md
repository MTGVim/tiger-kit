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
- `/tk:gap`은 반드시 `GAP_READY`, `GAP_AUTO_LAUNCHED`, 또는 `GAP_BLOCKED` 중 하나로 끝납니다.
- `GAP_READY`는 정확히 하나의 `tigerkit-launch-workflow` block을 포함하고 실행은 `/tk:launch`로 분리해야 합니다.
- `GAP_AUTO_LAUNCHED`는 같은 `/tk:gap` 호출 안에서 sealed workflow 생성 뒤 정식 `/tk:launch` 루틴까지 완료 또는 중단한 경우에만 사용합니다.
- `GAP_BLOCKED`는 `tigerkit-launch-workflow` block을 포함하면 안 됩니다.
- 기본 workflow archive 위치: `.claude/tigerkit/branches/<branch-key>/gap/<WF-ID>.md`
- 최신 workflow pointer copy: `.claude/tigerkit/branches/<branch-key>/gap/current.md`

### `/tk:gap default stdout`

`GAP_READY` stdout:

```text
GAP_READY: <WF-ID>
브랜치 범위: <branch-key>
워크플로: .claude/tigerkit/branches/<branch-key>/gap/<WF-ID>.md
워크플로 해시: <sha256>
작업: <count>
검증 게이트: <count>
자동 실행 허용: false
커밋 정책: preflight_decision_required
다음 행동: /tk:launch
```

`GAP_AUTO_LAUNCHED` stdout:

```text
GAP_AUTO_LAUNCHED: <WF-ID>
브랜치 범위: <branch-key>
워크플로: .claude/tigerkit/branches/<branch-key>/gap/<WF-ID>.md
워크플로 해시: <sha256>
Launch 결과: SUCCESS | PARTIAL | ABORTED
Launch 보고서: .claude/tigerkit/branches/<branch-key>/launch/<LCH-ID>.md
검증: <passed>/<total> 통과, <failed> 실패, <blocked> 차단
커밋: <created|skipped_preflight_required|skipped_not_requested|skipped_not_git_repo|skipped_no_github_remote|skipped_readonly_workspace|skipped_commit_policy_skip>
다음 행동: <없음|사용자 결정 필요|검증 실패 수정|review finding 반영|commit 승인 필요>
```

`GAP_BLOCKED` stdout:

```text
GAP_BLOCKED: <GAP-ID>
브랜치 범위: <branch-key>
차단 사유: <count>
사용자 결정 필요: <count>
누락 근거: <count>
보고서: .claude/tigerkit/branches/<branch-key>/gap/<GAP-ID>.md
다음 행동: <Q1 확인 후 /tk:gap 재실행|source 제공 필요>
```

### `tigerkit-gap-status` block

```tigerkit-gap-status
status: GAP_READY | GAP_AUTO_LAUNCHED | GAP_BLOCKED
workflow_id: WF-YYYYMMDD-HHmmss-RAND | null
workflow_path: .claude/tigerkit/branches/<branch-key>/gap/<WF-ID>.md | null
workflow_sha256: <sha256> | null
launch_receipt_path: .claude/tigerkit/branches/<branch-key>/launch/<LCH-ID>.md | null
launch_status: SUCCESS | PARTIAL | ABORTED | null
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
    parallel_group: <group id|null>
    join_after: []
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
review_policy:
  mode: required | optional | skip
  reason: <one sentence>
  reviewer: tk-reviewer
  duplicate_review: forbid_unless_new_diff
reflect_policy:
  mode: generated_report_only
  durable_apply_requires_preflight_approval: true
```

### Planning-time parallelism

`depends_on`은 task ordering list가 아니라 dependency edge surface입니다. `/tk:gap`은 독립 작업에 불필요한 edge를 추가하지 않고, 안전하면 별도 task와 `parallel_group`으로 분리해 DAG-shaped workflow를 봉인합니다. later verification, artifact merge, receipt synthesis처럼 fan-in이 필요한 지점은 `join_after`나 명시 verification task로 표현합니다.

Phase 1 `/tk:launch` runtime은 task를 순차 실행할 수 있습니다. 순차 실행은 runtime 제약이며 sealed workflow의 planning-time parallel intent를 제거하지 않습니다.

### Model routing policy

Core contract는 concrete provider model name 대신 model tier를 기록합니다. Host adapter artifact는 Claude Code agent frontmatter나 receipt처럼 관측 가능한 surface에서 `sonnet` 같은 concrete alias를 기록할 수 있습니다.

| Tier | 허용 범위 | 금지 범위 |
| --- | --- | --- |
| cheap scout / session-default / Haiku-class | source inventory, link/doc/file candidate collection, lightweight grounding pre-pass, source grouping, source-by-source intake scaffolding, non-binding draft summary | confirmed requirement normalization, ambiguity attack final decision, producer-evidence-sensitive judgment, `GAP_READY` vs `GAP_BLOCKED` freeze decision, acceptance review verdict |
| Sonnet-class | final gap freeze/judge, launch execution, verification synthesis, review verdict, durable guidance에 영향을 주는 reflect decision | 없음 |
| Opus-class escalation | high-risk 또는 semver-major ambiguity, cross-cutting design/adapter/contract arbitration, repeated `REVIEW_BLOCKED`/`REVIEW_PARTIAL` non-convergence, release-gate/high-risk acceptance review | routine source scouting 대체 용도 |

Cheap scout output은 non-binding intake evidence로만 쓰며, evidence precision, producer evidence, ambiguity, JudgeMerger gate를 낮추지 않습니다.

### `tigerkit-launch-workflow` seal

`manual_review_required`는 verification gate type이며 embedded acceptance review의 대체가 아닙니다. sealed workflow의 acceptance review 실행 여부는 `review_policy`가 결정합니다.


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
브랜치 범위: <branch-key>
결과: P0 <count> / P1 <count> / P2 <count> / 근거 충돌 <count> / 확인 필요 <count>
보고서: .claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/report.md
실행 JSON: .claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/run.json
다음 행동: <G1 먼저 수정|Q1 확인 필요|없음>

조치 필요 항목:
| Ref | Sev | 요약 | 필요한 변경 |
| --- | --- | --- | --- |
| G1 | P1 | <final finding 1줄 요약> | <수정 방향 1줄> |

확인 필요:
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
# Tiger Kit Gap 보고서: <GAP-ID>

## 요약

## 사용한 근거

## 조치 필요 항목

## 확인 필요

## 미채택 요약

## 다음 행동 그래프

## 다음 행동
```

`## 사용한 근거`에는 source별 `source_type`, access status, lock status, raw reference, derived Contract 상태를 구분해 둡니다. 대량 source는 source 단위 lock 시점을 남기고, visual capture가 numeric design value의 단독 근거인지 여부를 표시합니다.

`## 조치 필요 항목`에는 accepted P0/P1/P2 final finding만 둡니다.

`## 확인 필요`는 implementation-blocking과 reference-only를 구분합니다. 질문은 option/evidence/impact/recommendation/status를 표로 제시합니다.

`## 다음 행동 그래프`는 full runner가 아니라 run-local Ref 기반 graph-lite 순서 안내입니다. clarification dependency, finding 선후관계, re-check, re-run 순서만 짧게 표현합니다.

확인 질문 표 형식:

```md
| Ref | 분류 | 질문 | 선택지 | 근거 | 영향 | 추천 | 상태 |
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

채택된 finding은 아래를 사용합니다:

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

- 목적: sealed launch workflow를 `tk-runner` subagent로 실행하고 verification gate 결과, runtime harness, acceptance review verdict, abort reason, reflect trace를 branch-local artifact로 남깁니다.
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
- `review_policy.mode == required`이면 verification 뒤에 read-only `tk-reviewer` acceptance review를 실행합니다. `optional`은 not-run reason을 receipt에 남기고, `skip`은 명시 skip으로 기록합니다.
- execution success는 acceptance review pass를 자동 의미하지 않습니다. reviewer fail/block이면 overall status는 plain success가 아닙니다.

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
execution:
  status: SUCCESS | ABORTED | FAILED_PREFLIGHT
  tasks_completed: <done>/<total>
verification:
  passed: []
  failed: []
  blocked: []
acceptance_review:
  required: true | false
  policy_mode: required | optional | skip
  reviewer: tk-reviewer | none
  status: REVIEW_PASS | REVIEW_PARTIAL | REVIEW_FAIL | REVIEW_BLOCKED | NOT_RUN_OPTIONAL | SKIPPED
  reason: <text|null>
  review_report_path: .claude/tigerkit/branches/<branch-key>/review/<RVW-ID>.md | null
overall_status: SUCCESS | PARTIAL | ABORTED
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
브랜치 범위: <branch-key>
워크플로: .claude/tigerkit/branches/<branch-key>/gap/<WF-ID>.md
워크플로 해시: <sha256>
결과: SUCCESS | PARTIAL

실행 하네스: tk-runner / model=sonnet / status=<active|fallback_inline|unavailable>
워크트리 컨텍스트: <none|proposal:<count>|approval_required>
실행:
- 상태: SUCCESS
- 작업: <done>/<total>

검증:
- 통과: <passed>/<total>
- 실패: <failed>
- 차단: <blocked>

수용 검토:
- 상태: <REVIEW_PASS|REVIEW_PARTIAL|REVIEW_FAIL|REVIEW_BLOCKED|NOT_RUN_OPTIONAL|SKIPPED>
- Reviewer: <tk-reviewer|none>

종합:
- 상태: <SUCCESS|PARTIAL>

커밋: <created|skipped_preflight_required|skipped_not_requested|skipped_not_git_repo|skipped_no_github_remote|skipped_readonly_workspace|skipped_commit_policy_skip>
보고서: .claude/tigerkit/branches/<branch-key>/launch/<LCH-ID>.md
최신본: .claude/tigerkit/branches/<branch-key>/launch/current.md
Reflect 보고서: .claude/tigerkit/branches/<branch-key>/reflect/<RFL-ID>.md
Reflect 최신본: .claude/tigerkit/branches/<branch-key>/reflect/current.md

다음 행동: <없음|reflect 제안 검토|review finding 반영|commit 승인 필요>
```

ABORTED stdout:

```text
🛑 Launch 중단: <LCH-ID>
브랜치 범위: <branch-key>
워크플로: .claude/tigerkit/branches/<branch-key>/gap/<WF-ID>.md
워크플로 해시: <sha256|unknown>
결과: ABORTED | PARTIAL
중단 코드: <CODE|없음>
원인: <한글 1줄>

실행 하네스: tk-runner / model=sonnet / status=<active|fallback_inline|unavailable>
워크트리 컨텍스트: <none|proposal:<count>|approval_required>
실행:
- 상태: <ABORTED|FAILED_PREFLIGHT>
- 완료 작업: <done>/<total>

검증:
- 통과: <passed>/<total>
- 실패: <failed>
- 차단: <blocked>

수용 검토:
- 상태: <REVIEW_FAIL|REVIEW_BLOCKED|NOT_RUN_OPTIONAL|SKIPPED|없음>
- Reviewer: <tk-reviewer|none>

종합:
- 상태: <ABORTED|PARTIAL>

보고서: .claude/tigerkit/branches/<branch-key>/launch/<LCH-ID>.md
최신본: .claude/tigerkit/branches/<branch-key>/launch/current.md
Reflect 보고서: .claude/tigerkit/branches/<branch-key>/reflect/<RFL-ID>.md
Reflect 최신본: .claude/tigerkit/branches/<branch-key>/reflect/current.md

다음 행동: <사용자 결정 필요|workflow 재생성|scope 조정|검증 실패 수정|review finding 반영>
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

## `/tk:review` Output Contract

- 목적: frozen goal/spec 또는 sealed workflow 대비 launch 결과와 현재 구현을 검증하고 verdict를 남깁니다.
- `/tk:gap --review`는 v7 Contract-based Gap Review compatibility mode이며, `/tk:review`는 post-launch verification command입니다.
- standalone target 우선순위는 explicit target, current diff, branch diff, latest launch receipt, current PR context, blocked입니다.
- 구현 수정, launch 실행, commit, push, PR, merge, release, deploy, GitHub issue write는 수행하지 않습니다.
- verification 없이 `REVIEW_PASS`를 선언하지 않습니다.
- review는 `Review Target`을 먼저 pin하고 Spec / Standards / Evidence 축을 분리합니다.
- latest embedded review가 같은 target을 이미 커버하고 new diff가 없으면 duplicate review를 반복하지 않습니다.

기본 receipt 위치:

```text
.claude/tigerkit/branches/<branch-key>/review/RVW-YYYYMMDD-HHmmss-RAND.md
.claude/tigerkit/branches/<branch-key>/review/current.md
```

Machine-readable block:

```tigerkit-review-report
version: 1
review_id: RVW-YYYYMMDD-HHmmss-RAND
scope_kind: git_branch | git_detached | git_no_remote | workspace
scope_key: <branch-key-or-workspace-key>
status: REVIEW_PASS | REVIEW_PARTIAL | REVIEW_FAIL | REVIEW_BLOCKED
target:
  mode: current_diff | branch_diff | pr | artifact | claim | latest_launch | blocked
  basis: <why selected>
  ref: <path#section or target ref>
  alternatives_skipped: []
axes:
  spec: PASS | PARTIAL | FAIL | BLOCKED | NO_SPEC
  standards: PASS | PARTIAL | FAIL | BLOCKED
  evidence: VERIFIED | PARTIAL | FAILED | BLOCKED | ASSUMED
requirements_checked: []
verification:
  passed: []
  failed: []
  blocked: []
duplicate_review:
  matched_latest_embedded_review: true | false
  no_new_diff: true | false
closed_gaps: []
remaining_gaps: []
drift_risks: []
next_action: <one sentence or 없음>
```

기본 stdout:

```text
✅ Review 완료: <RVW-ID>
브랜치 범위: <branch-key>
결과: REVIEW_PASS | REVIEW_PARTIAL | REVIEW_FAIL | REVIEW_BLOCKED
대상: <current_diff|branch_diff|pr|artifact|claim|latest_launch|blocked>:<ref>

축 판정:
- Spec: <PASS|PARTIAL|FAIL|BLOCKED|NO_SPEC>
- Standards: <PASS|PARTIAL|FAIL|BLOCKED>
- Evidence: <VERIFIED|PARTIAL|FAILED|BLOCKED|ASSUMED>

검증: <passed>/<total> 통과, <failed> 실패, <blocked> 차단
닫힌 gap: <count>
남은 gap: <count>
Drift/Risk: <none|count>

보고서: .claude/tigerkit/branches/<branch-key>/review/<RVW-ID>.md
최신본: .claude/tigerkit/branches/<branch-key>/review/current.md

다음 행동: <없음|/tk:gap 재실행|/tk:launch 재실행|human decision 필요|/tk:handoff>
```

상태 기호:

- `✅` = `REVIEW_PASS`
- `⚠️` = `REVIEW_PARTIAL`
- `🛑` = `REVIEW_FAIL` 또는 `REVIEW_BLOCKED`

`/tk:review` report 필수 H2:

```md
# Review Report: <RVW-ID>

## 요약
## Review Target
## Spec Axis
## Standards Axis
## Evidence Axis
## Closed Gaps
## Remaining Gaps
## Drift / Risk
## Verdict
## Next Recommendation
```

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
브랜치 범위: <branch-key>
결과: NEXT_DONE | NEXT_PARTIAL | NEXT_BLOCKED | NEXT_SKIPPED
선택한 작업: <한글 한 문장>

실행: <count>
변경 파일: <count>
검증: <passed>/<total> | not_run:<reason>
승인: <not_required|present:<source>|missing:<needed_action>>

보고서: .claude/tigerkit/branches/<branch-key>/next/<NXT-ID>.md
최신본: .claude/tigerkit/branches/<branch-key>/next/current.md
차단 사유: <none | 사용자 결정 필요 | 누락 근거 | 승인 필요 | sealed workflow 필요 | dirty workspace | 검증 실패 | worktree context 승인 필요 | capability 사용 불가 | 기타>

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
- meta-feedback는 기본적으로 emit하지 않습니다. current run이 TigerKit-level friction을 드러낼 때만 proposal-only로 첨부하며, 그렇지 않으면 `Meta-feedback: NONE`을 출력합니다.
- `--no-meta-feedback` 또는 `--meta-feedback=false`가 있으면 meta-feedback 판단 자체를 생략합니다.

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
user_routine_skill_review: []
user_memory_candidates: []
meta_feedback: NONE | PRESENT | SKIPPED_BY_USER
```

기본 stdout:

```text
Reflect 완료
적용: true
적용 대상:
- CLAUDE.md
- .claude/rules/<path>.md

적용 결과:
- <added>건 추가
- <updated>건 갱신
- <skipped>건 중복으로 건너뜀

## Repo Insight
- <한글 insight summary 또는 NONE>

## 사용자 루틴 스킬 검토
- Decision: NONE | SNIPPET | USER_SKILL_CANDIDATE | REPO_RULE | HOOK_OR_SCRIPT | COMMAND
- Reason:
  - <한글 reason 또는 없음>

## Meta-feedback
Meta-feedback: NONE | PRESENT

추가 근거 필요:
- <확인 필요 항목 또는 None>
```

Dry-run stdout:

```text
Reflect 완료
적용: false
예상 대상:
- CLAUDE.md
- .claude/rules/<path>.md

미리보기 결과:
- <added>건 추가 예정
- <updated>건 갱신 예정
- <skipped>건 중복으로 건너뜀

## Repo Insight
- <한글 preview summary 또는 NONE>

## 사용자 루틴 스킬 검토
- Decision: NONE | SNIPPET | USER_SKILL_CANDIDATE | REPO_RULE | HOOK_OR_SCRIPT | COMMAND
- Reason:
  - <한글 reason 또는 없음>

## Meta-feedback
Meta-feedback: NONE | PRESENT

추가 근거 필요:
- <확인 필요 항목 또는 None>
```

`--no-meta-feedback` 또는 `--meta-feedback=false`가 있으면 `Meta-feedback: SKIPPED_BY_USER`로 출력합니다.

Reflect no-op success:

```text
Reflect 완료
적용: true
적용 대상:
- 없음

적용 결과:
- 0건 추가
- 0건 갱신
- <skipped>건 중복으로 건너뜀
- <no_action>건 조치 없음

## Repo Insight
- 영구 반영할 insight 없음.

## 사용자 루틴 스킬 검토
- Decision: NONE
- Reason:
  - 없음

## Meta-feedback
Meta-feedback: NONE

추가 근거 필요:
- <확인 필요 항목 또는 None>
```

Reflect excludes:

- branch-specific one-off decision
- temporary Spec Patch itself
- superseded decision
- P3/nit
- rejected finding
- low-confidence observation
- unresolved source conflict

## `/tk:meta-feedback` Output Contract

- 목적: 현재 세션에서 관측된 TigerKit command/skill 개선점을 프로젝트 자산 유출 없이 일반화합니다.
- 세션 내역 전체에서 friction, 사용자 교정, 반복 실수, output UX 문제, latency 문제, false-positive pattern을 찾습니다.
- 기본값은 proposal-only입니다.
- emit 대상은 TigerKit 자체가 야기한 workflow/tooling friction뿐입니다. ordinary task learning, repo/domain insight, user routine pattern, next-step follow-up은 emit하지 않고 각각 `/tk:reflect`, `/tk:handoff`, `/tk:next`로 route합니다.
- `--out <path>`가 있을 때만 current worktree root 내부 지정 경로에 파일을 작성할 수 있습니다.
- worktree root 밖 경로, user home, `/tmp`, hidden control file path에는 쓰지 않습니다.
- raw session evidence, 사용자 원문 quote, repo 이름, product 이름, 도메인 고유명, 내부 path, URL, ticket, branch, PR 번호, commit hash를 출력하지 않습니다.
- emit 전에 Domain-term guard를 실행해 project/framework/product 이름, path fragment, 파일 확장자, CamelCase/code identifier, domain entity, URL/reference 형태가 남은 proposal을 rewrite 또는 reject합니다.
- 각 proposal은 “다른 repo·다른 도메인에서도 그대로 말이 되는가?”라는 Restate test를 통과해야 합니다.
- repo rule patch와 repo/도메인 insight는 `/tk:reflect`, basis-target 비교는 `/tk:gap`, follow-up 보관은 `/tk:handoff` 또는 `/tk:next`, command·skill 계약 friction은 `/tk:meta-feedback` 대상으로 분리합니다.
- 산출물은 대상 command/skill의 자체 계약 어휘와 feedback taxonomy만 사용합니다.
- agent runtime/config, MCP permission, custom agent 추천은 TigerKit 본체 범위 밖으로 둡니다.

필수 section:

```md
## TigerKit Meta-feedback
Affected command or doc:
- <skill-or-command>

Feedback class:
- <ux|output-format|taxonomy|safety|dispatch|docs|performance|false-positive>

Observed issue:
- <generic issue>

Evidence from current run:
- <source_type=...>

Why this is TigerKit-level:
- <generic reason>

Minimal proposed fix:
- <generic command/skill improvement>

## 비식별화 기록
- 제거: <repo names|paths|URLs|domain labels|quoted user text>
- 유지: <abstract pattern only>
- 일반화 게이트: passed
- 재진술 테스트: passed
- 포함된 위험 상세: none
```

유효한 TigerKit-level issue가 없으면 아래 형식으로 끝냅니다.

```md
## TigerKit Meta-feedback
Meta-feedback: NONE

## 비식별화 기록
- 제거: none
- 유지: none
- 일반화 게이트: not_applicable
- 재진술 테스트: not_applicable
- 포함된 위험 상세: none
```

안전하게 일반화할 수 없거나 Restate test를 통과하지 못하면 `Minimal proposed fix: none`, `이유: privacy gate failed` 또는 `이유: generalization gate failed`에 해당하는 상태로 중단합니다.

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
