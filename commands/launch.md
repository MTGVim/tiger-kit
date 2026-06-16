---
description: sealed GAP workflow를 실행하고 검증·abort·reflect receipt를 생성합니다.
argument-hint: "[workflow path|--latest] [--autopilot] [--worktree|--no-worktree]"
---

이 명령은 TigerKit v8.0 Claude Code command-contract runner의 launch contract를 따릅니다.

사용자에게는 한글로 답합니다. 코드, path, URL, ticket, commit, hash, identifier, error는 원문 그대로 둘 수 있습니다.

목표: `/tk:launch`는 `/tk:gap`이 만든 sealed launch workflow만 실행하고, workflow 밖 scope 확장이나 mid-flight 질문 없이 성공 또는 abort receipt를 남깁니다.

```text
launch = execute sealed workflow + verify gates + abort safely + reflect trace
```

## Command surface

- plugin slash invocation은 `/tk:launch`입니다.
- `/tk:launch --autopilot`은 Phase 1에서 recovery를 수행하지 않고 `AUTOPILOT_DISABLED` 또는 `AUTOPILOT_NOT_IMPLEMENTED_IN_PHASE1`로 abort합니다.
- `/tk:launch --worktree`와 `/tk:launch --no-worktree`는 preflight 선택지를 문서화합니다. Phase 1 command contract는 worktree 결정을 기록하지만 별도 runner binary를 만들지 않습니다.

## Input

기본 입력은 current branch scope의 최신 launch workflow입니다.

```text
.claude/tigerkit/branches/<branch-key>/gap/current.md
```

명시 workflow path가 있으면 current worktree root 내부의 `.claude/tigerkit/branches/<branch-key>/gap/` 아래 파일만 허용합니다.

허용되는 workflow surface는 정확히 하나의 fenced block입니다.

````text
```tigerkit-launch-workflow
...
```
````

## Preflight

1. current worktree root와 branch key를 계산합니다.
2. workflow 파일을 찾습니다.
3. `tigerkit-launch-workflow` fenced block이 정확히 하나인지 확인합니다.
4. block body를 LF로 정규화하고 final LF를 하나 보장한 뒤 SHA-256을 계산합니다.
5. `tigerkit-gap-status`와 `branch-state.json`에 기록된 외부 `workflow_sha256`과 계산값을 비교합니다. `tigerkit-launch-workflow` 내부 자기참조 hash는 사용하지 않습니다.
6. `status`가 `GAP_READY`인지 확인합니다.
7. `source_refs`, `requirements`, `tasks`, `verification_gates`, `abort_policy`, `commit_policy`를 확인합니다.
8. `autopilot_policy.enabled`가 false인데 `--autopilot`이면 abort합니다.
9. worktree 선택이 명시되어 있으면 workflow의 worktree policy와 충돌하지 않는지 확인합니다.
10. commit 가능 여부는 `commit_policy`와 preflight approval evidence로만 판단합니다.

## Abort codes

| Code | 조건 | 처리 |
| --- | --- | --- |
| `WORKFLOW_NOT_FOUND` | workflow 파일 또는 current pointer를 찾지 못함 | 실행하지 않음 |
| `MULTIPLE_WORKFLOW_BLOCKS` | launch workflow block이 2개 이상 | 실행하지 않음 |
| `WORKFLOW_HASH_MISMATCH` | block hash가 seal과 다름 | 실행하지 않음 |
| `GAP_BLOCKED` | workflow status가 launch 불가 | 실행하지 않음 |
| `HUMAN_DECISION_REQUIRED` | 실행 중 새 사용자/owner 결정 필요 | 질문하지 않고 abort |
| `AUTOPILOT_DISABLED` | workflow가 autopilot을 금지 | recovery 없이 abort |
| `AUTOPILOT_NOT_IMPLEMENTED_IN_PHASE1` | Phase 1에서 recovery 요청 | recovery 없이 abort |
| `OUT_OF_SCOPE_DIFF` | workflow 밖 파일·동작 변경 필요 또는 발생 | 변경 중단 후 abort |
| `HYDRATION_CONFLICT` | tracked file symlink 등 hydration 충돌 | hydration 중단 후 abort |
| `VERIFICATION_FAILED` | verification gate 실패 | 실패 evidence와 함께 abort |

## Execution rules

- workflow의 task graph 순서만 따릅니다.
- missing requirement를 임의 해석하지 않습니다.
- public API, DB, product behavior를 workflow 밖에서 재정의하지 않습니다.
- mid-flight 질문을 하지 않습니다. 결정이 필요하면 `HUMAN_DECISION_REQUIRED`로 abort합니다.
- out-of-scope diff를 만들지 않습니다. 발견하면 `OUT_OF_SCOPE_DIFF`로 abort합니다.
- verification 없이 success를 선언하지 않습니다.
- commit은 `commit_policy.mode=commit_on_success`만으로 수행하지 않습니다. preflight receipt에 `user_preapproved_commit=true`와 `approval_source_ref`가 있어야 합니다.

## Verification gates

각 verification gate는 아래 field를 가져야 합니다.

```text
id: VG1
command_id: V1
purpose: <검증 목적>
required: true
success_condition: <성공 조건>
failure_abort_code: VERIFICATION_FAILED
```

`verification command id`와 `verification gate id`는 별도 namespace입니다.

## Reflect postflight

SUCCESS 또는 ABORTED 후 `/tk:launch`는 generated launch report를 남기고 `/tk:reflect`가 읽을 수 있는 trace를 branch-local artifact로 기록합니다.

Reflect postflight는 durable apply나 commit을 자동 수행하지 않습니다. preflight에서 승인되지 않은 durable rule 변경은 proposal 또는 generated report에만 남깁니다.

## Output

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
Report: .claude/tigerkit/branches/<branch-key>/launch/<LCH-ID>.md
Current: .claude/tigerkit/branches/<branch-key>/launch/current.md
Reflect: .claude/tigerkit/branches/<branch-key>/reflect/<RFL-ID>.md
Reflect Current: .claude/tigerkit/branches/<branch-key>/reflect/current.md
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
Report: .claude/tigerkit/branches/<branch-key>/launch/<LCH-ID>.md
Current: .claude/tigerkit/branches/<branch-key>/launch/current.md
Reflect: .claude/tigerkit/branches/<branch-key>/reflect/<RFL-ID>.md
Reflect Current: .claude/tigerkit/branches/<branch-key>/reflect/current.md
다음 행동: <human decision|workflow 재생성|scope 조정|검증 실패 수정>
```

## 금지

- workflow 밖 scope 확장
- missing requirement 임의 해석
- public API / DB / product behavior 재정의
- verification 없이 success 선언
- out-of-scope diff commit
- mid-flight 사용자 질문
- Phase 1 autopilot recovery 수행
- preflight 승인 없는 commit
