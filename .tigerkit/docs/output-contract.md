# TigerKit 운영 Output Contract

이 문서는 TigerKit command의 출력 계약을 정의합니다.

## 공통 원칙

- 사용자-facing label은 한글로 씁니다.
- 코드, path, URL, identifier, status code, field name은 원문을 유지할 수 있습니다.
- Evidence, Interpretation, Decision, Suggestion을 구분합니다.
- 검증하지 않은 success를 선언하지 않습니다.
- command가 파일을 쓰면 changed path를 출력합니다.
- Active command surface는 `/tk:gap`, `/tk:loop-spec`, `/tk:execute`, `/tk:reflect`입니다.
- 기본 projection은 compact합니다. empty section, default empty list, `NONE` line, no-op reflect item은 의미 보존에 필요할 때만 출력합니다.

## `/tk:gap` Output Contract

`/tk:gap`은 SoT와 Current Implementation의 one-shot gap analysis입니다.

```md
## Gap Summary

| Area | SoT | Current | Gap | Impact | Priority |
|---|---|---|---|---|---|

## Findings

### 1. <finding title>
- SoT:
- Current:
- Evidence:
- Evidence type:
- Impact:
- Priority:
- Suggested fix:

## Ambiguities / Missing Evidence

| Ref | Question | Evidence checked | Impact | Recommendation |
|---|---|---|---|---|

## Not accepted summary

- <optional low-priority or rejected note>

## Recommended Next Steps

1. <next step>
```

Gap values: `missing`, `mismatch`, `overbuilt`, `ambiguous`.

Route labels for actionable findings:

```text
direct | loop-spec | decision
```

Route 이유는 evidence identifier와 연결합니다. Non-actionable finding에는 route를 강제하지 않습니다.

## `/tk:loop-spec` Output Contract

`/tk:loop-spec`은 명시적 task를 실행 없는 LoopSpec v2 계약으로 컴파일하거나 기존 spec을 검증합니다.

```text
LoopSpec: <spec-id>
Readiness: complete | blocked
Executor: fast | reasoning | NONE
Worktree: <branch or workspace>

Blockers
  - <id>: <reason>

Guards
  - <guard>

Saved
  <~/.tigerkit/.../loop-specs/<spec-id>/spec.yaml or NONE>

Write receipt
  changed: <path or NONE>
  source tree changed: no

Next
  /tk:execute <spec-id-or-path>
```

`Next`는 readiness가 `complete`일 때만 출력합니다. Blocked spec에는 executor recommendation이 없어야 합니다.

Validation output:

```text
LoopSpec: <id or path>
Schema: valid | invalid
Context: current | stale | unknown
```

LoopSpec v2는 `task`, `context`, `blockers[]`, `guards[]`, `steps[]`, `verifiers[]`, `scope`, `execution`의 closed-world field set을 사용합니다. Legacy spec은 `/tk:execute`에서 `unsupported_loop_spec_schema`로 reject합니다.

## `/tk:execute` Output Contract

`/tk:execute`는 user-only dispatcher입니다.

```text
Execute: completed | escalated | failed | rejected
Spec: <spec-id>
Executor: fast | reasoning | NONE
Receipt: <~/.tigerkit/.../executions/<execution-id>.yaml or NONE>
Changed paths: <count>
Verifiers: <passed>/<total> passed
Primary reason: <reason code when non-completed>
Required action: <recommended action when non-completed>
```

Rules:

- Empty/default sections are omitted.
- `completed` has no reason code and no recommended action.
- `rejected` has no observed source change.
- `failed` can include partial changes when technical execution failed.
- `escalated` means safety/judgment mismatch, not success.
- `claimedObservedMismatch: true` forces `escalated` with primary `claimed_observed_mismatch` unless stronger safety reason is primary.
- Partial changes suppress retry recommendation.
- Dispatcher output is a projection of persisted receipt when receipt exists.

### Receipt result vocabulary

```text
completed | escalated | failed | rejected
```

### Boundary enforcement vocabulary

```text
hard | detection_only
```

`detection_only` is developer-preview only and must not be counted as stable public execution.

### Verifier status vocabulary

```text
passed | failed | error | timed_out | not_run
```

Verifier result field set:

```yaml
id: <verifier id>
command: <required only for postflight>
status: passed | failed | error | timed_out | not_run
exitCode: <integer or null>
reasonCode: <required for error/timed_out/not_run, forbidden for passed/failed>
message: <optional non-empty human detail>
```

### Reason code vocabulary

Rejected/preflight:

```text
spec_not_found
ambiguous_spec_reference
unsupported_loop_spec_schema
invalid_loop_spec
blocked_loop_spec
missing_executor_recommendation
missing_executor_mapping
repository_identity_mismatch
worktree_identity_mismatch
scope_key_mismatch
stale_base_revision
stale_fingerprint
scope_resolution_drift
invalid_scope_pattern
unsupported_path_encoding
case_collision
unsupported_scope_entry_type
invalid_create_delete_state
dirty_scoped_path
dirty_excluded_path
unresolved_merge_conflict
required_verifier_unavailable
hard_enforcement_unavailable
```

Escalated/safety:

```text
plan_deviation_required
scope_expansion_required
executor_capability_mismatch
concurrent_drift
scope_violation
excluded_path_modified
unapproved_path_created
unapproved_path_deleted
claimed_observed_mismatch
baseline_dirty_path_modified
dispatcher_boundary_violation
head_changed_concurrently
```

Failed/technical:

```text
executor_error
required_tool_unavailable
verifier_failed
verifier_error
verifier_timed_out
budget_exhausted
success_condition_not_met
receipt_persistence_failed
transient_runtime_failure
```

### Recommended action vocabulary

```text
regenerate_loop_spec
resolve_blockers
revise_loop_spec
review_partial_changes
cleanup_partial_changes
resolve_concurrent_drift
restore_required_tool
retry_execute
inspect_scope_violation
inspect_enforcement_failure
inspect_loop_spec
resolve_worktree_state
resolve_merge_conflict
refresh_capability_proof
report_runtime_failure
```

`retry_execute` is allowed only when `safeToRetry: true`.

### ReasonDetail sub-schema

```yaml
code: <reason code>
message: <optional non-empty human detail>
verifierId: <optional verifier id>
```

No other fields are allowed. `(code, verifierId-or-empty)` must be unique. Details sort by `reasonCodes[]` order, generic detail first, then verifier declaration order.

## `/tk:reflect` Output Contract

`/tk:reflect`는 promotion router로서 세션 learning과 execution receipt를 안전한 promotion surface로 분류합니다. 기본값은 preview-only입니다. 명시적 `--apply=true`가 있어도 write는 eligible `repo-local` candidate의 `<git-root>/CLAUDE.local.md`로 제한합니다.

If every candidate is no-op, default output is exactly:

```text
Reflect: 반영할 변경 없음.
```

Canonical target enum:

```text
repo-local, repo-shared, user-global, skill, hook, command, agent, discard
```

`PROFILE.md`, `automation`, `hookify`, `hook / hookify`는 target 이름이 아닙니다.

Legacy selector output:

```text
Requested target: repo
Effective targets: repo-local, repo-shared
Deprecation: Deprecated target selector: repo expands to repo-local, repo-shared.
```

```text
Requested target: user
Effective targets: user-global
Deprecation: Deprecated target selector: user expands to user-global.
```

Candidate minimum field set:

```yaml
candidate_id: R1
status: candidate | confirmed | deprecated
duplicate_status: confirmed | unknown
action: preview_only | apply | suggest_only | discard
target: repo-local | repo-shared | user-global | skill | hook | command | agent | discard
path: <path or NONE>
evidence: <direct observed evidence>
reason: <routing reason>
```

Reflect consumes persisted receipt before transcript when execution ID or receipt path is provided. It must validate at least `schemaVersion`, `executionId`, `specId`, `result`, `boundaryEnforcement`, `reasonCodes`, `reasonDetails`, `observed.changedPaths`, `postflightVerifiers`, `safeToRetry`, `cleanupRequired`, `recommendedActions`.

Reflect projection is compact by default:

- omit empty target sections, default empty lists, and standalone `NONE` lines unless they carry safety or state meaning
- emit `Deprecation:` only when a legacy selector was actually used
- emit `Changed paths` only for real writes or apply/rollback receipts where explicit no-change proof matters
- emit `Apply plan` only when the current invocation produced one
- omit `충돌 / 적용 조건` and `다음 행동` when empty

## Golden output fixtures

`evals/golden/human-output/` owns exact UTF-8/LF fixtures for command projection. Release evals compare rendered output bytes and semantic omission assertions. Fixture updates are review-only and not auto-generated by runtime.

## Deprecated output surfaces

아래 status/output surfaces는 새 TigerKit active flow에서 생성하지 않습니다.

- AFK receipt
- Patron decision ledger
- setup receipt
- grill question receipt
- launch workflow receipt
- handoff receipt
- active `SessionStart` hook receipt
- workflow hash
- sealed workflow
- `tigerkit-launch-workflow`
