---
description: sealed GAP workflow를 tk-runner subagent로 실행하고 검증·abort·reflect receipt를 생성합니다.
argument-hint: "[workflow path|--latest] [--autopilot] [--worktree|--no-worktree]"
---

이 명령은 TigerKit v8.0 Claude Code command-contract runner의 launch contract를 따릅니다.

사용자에게는 한글로 답합니다. 코드, path, URL, ticket, commit, hash, identifier, error, contract field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:launch`는 `/tk:gap`이 만든 sealed launch workflow만 실행하고, workflow 밖 scope 확장이나 mid-flight 질문 없이 성공 또는 abort receipt를 남깁니다. 실행은 가능한 경우 `tk-runner` subagent가 담당하며, model/runtime harness 상태를 preflight와 receipt에 기록합니다.

```text
launch = preflight + tk-runner sealed workflow execution + verify gates + abort safely + reflect trace
```

## Command surface

- plugin slash invocation은 `/tk:launch`입니다.
- `/tk:launch`는 `agents/tk-runner.md` subagent를 기본 실행 harness로 사용합니다.
- `tk-runner` Claude Code agent는 `model: sonnet`으로 배포됩니다. 휴대 가능한 canonical contract에는 concrete model name을 쓰지 않지만, Claude Code adapter 산출물인 agent frontmatter에는 host-specific model alias를 둘 수 있습니다.
- `/tk:launch --autopilot`은 Phase 1에서 recovery를 수행하지 않고 `AUTOPILOT_DISABLED` 또는 `AUTOPILOT_NOT_IMPLEMENTED_IN_PHASE1`로 abort합니다.
- `/tk:launch --worktree`와 `/tk:launch --no-worktree`는 preflight 선택지를 문서화합니다. Worktree hydration은 SessionStart hook이 먼저 안전 점검/처리를 시도하고, launch는 그 receipt를 preflight evidence로 읽습니다.

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

## SessionStart worktree hydration preflight

TigerKit은 Claude Code `SessionStart` hook으로 worktree-local symlink hydration을 먼저 점검합니다.

Hook entry:

```text
hooks/hooks.json → SessionStart → "${CLAUDE_PLUGIN_ROOT}/hooks/run-hook.cmd" session-start
```

Hook receipt:

```text
.claude/tigerkit/local/session-start/current.json
.claude/tigerkit/local/session-start/SSH-YYYYMMDD-HHmmss-RAND.json
```

Hook 원칙:

- best-effort로 실행하고 Claude Code session startup을 막지 않습니다.
- linked git worktree 또는 `.claude/tigerkit/local/worktree-hydration.json`이 있을 때만 receipt를 씁니다.
- `node_modules`는 기본적으로 symlink하지 않습니다.
- tracked file/directory는 기본적으로 symlink하지 않습니다.
- target regular file이나 different symlink를 덮어쓰지 않습니다.
- `source_worktree`를 임의로 수정하지 않습니다. `create-source-and-symlink` policy가 있어도 SessionStart hook은 source stub을 만들지 않고 existing source만 symlink합니다.
- 충돌이 있으면 receipt status를 `HYDRATION_CONFLICT`로 남기고, `/tk:launch` preflight가 실행 전 abort합니다.

Hydration config 후보:

```text
.claude/tigerkit/local/worktree-hydration.json
```

필드:

```json
{
  "version": 1,
  "hydrationSourceWorktree": "/absolute/source/worktree",
  "files": {
    "CLAUDE.local.md": "symlink",
    "AGENTS.md": "symlink",
    "DESIGN.md": "create-per-worktree"
  },
  "tigerkit": {
    "shared": ["config"]
  },
  "neverSymlink": ["node_modules"],
  "onConflict": "abort"
}
```

## Runtime harness preflight

`/tk:launch`는 task 실행 전에 runtime harness를 확인하고 receipt에 기록합니다.

Required harness record:

```yaml
runtime_harness:
  role: tk-runner
  expected_host_binding: claude_code_agent
  expected_model: sonnet
  model_tier: balanced
  effort_tier: medium
  status: active | fallback_inline | unavailable
  fallback_reason: null | agent_unavailable | host_does_not_support_subagents | model_binding_unobservable
```

규칙:

- Claude Code agent capability가 있으면 `tk-runner` subagent를 사용합니다.
- `tk-runner`가 보이지 않거나 host가 subagent를 지원하지 않으면, workflow가 `runtime_harness.allow_inline_fallback=true`를 명시한 경우에만 inline fallback을 사용할 수 있습니다.
- inline fallback을 쓰면 receipt에 `status=fallback_inline`과 reason을 기록합니다.
- workflow가 subagent execution을 required로 두었는데 harness가 unavailable이면 task를 실행하지 않고 `MODEL_HARNESS_UNAVAILABLE`로 abort합니다.
- model alias나 실제 provider/model을 런타임에서 관측할 수 없으면 성공처럼 숨기지 말고 `model_binding_unobservable`로 기록합니다.

## Preflight

1. current worktree/workspace root와 scope key를 계산합니다. git이 없으면 `scope_kind=workspace` fallback을 사용합니다.
2. workflow 파일을 찾습니다.
3. `tigerkit-launch-workflow` fenced block이 정확히 하나인지 확인합니다.
4. block body를 LF로 정규화하고 final LF를 하나 보장한 뒤 SHA-256을 계산합니다.
5. `tigerkit-gap-status`와 `branch-state.json`에 기록된 외부 `workflow_sha256`과 계산값을 비교합니다. `tigerkit-launch-workflow` 내부 자기참조 hash는 사용하지 않습니다.
6. `status`가 `GAP_READY`인지 확인합니다.
7. `source_refs`, `requirements`, `tasks`, `verification_gates`, `abort_policy`, `commit_policy`를 확인합니다.
8. SessionStart hydration receipt를 확인합니다. 최신 receipt가 `HYDRATION_CONFLICT`이면 task 실행 전 abort합니다.
9. runtime harness를 확인합니다. `tk-runner` subagent를 사용할 수 있는지, fallback 허용 여부, model binding 관측 가능성을 기록합니다.
10. `autopilot_policy.enabled`가 false인데 `--autopilot`이면 abort합니다.
11. worktree 선택이 명시되어 있으면 workflow의 worktree policy와 충돌하지 않는지 확인합니다.
12. commit 가능 여부는 `commit_policy`, workspace capability, preflight approval evidence로만 판단합니다. git/GitHub가 없어도 workflow가 commit/PR을 요구하지 않으면 launch를 계속할 수 있습니다.

## Commit and VCS fallback

Missing git or GitHub is not an abort by itself. It becomes an abort only when the sealed workflow requires commit/PR behavior.

Allowed commit receipt values:

```text
created
skipped_preflight_required
skipped_not_requested
skipped_not_git_repo
skipped_no_github_remote
skipped_readonly_workspace
skipped_commit_policy_skip
```

If git diff is unavailable, use the workflow diff policy:

```yaml
diff_scope:
  mode: git_diff | file_manifest_snapshot | receipt_only
  before_files: <manifest path|null>
  after_files: <manifest path|null>
  changed_files: <list|unknown>
  diff_lines: <number|unknown>
```

## Abort codes

| Code | 조건 | 처리 |
| --- | --- | --- |
| `WORKFLOW_NOT_FOUND` | workflow 파일 또는 current pointer를 찾지 못함 | 실행하지 않음 |
| `MULTIPLE_WORKFLOW_BLOCKS` | launch workflow block이 2개 이상 | 실행하지 않음 |
| `WORKFLOW_HASH_MISMATCH` | block hash가 seal과 다름 | 실행하지 않음 |
| `GAP_BLOCKED` | workflow status가 launch 불가 | 실행하지 않음 |
| `HUMAN_DECISION_REQUIRED` | 실행 중 새 사용자/owner 결정 필요 | 질문하지 않고 abort |
| `MODEL_HARNESS_UNAVAILABLE` | required `tk-runner` subagent/model harness를 사용할 수 없음 | task 실행 전 abort |
| `AUTOPILOT_DISABLED` | workflow가 autopilot을 금지 | recovery 없이 abort |
| `AUTOPILOT_NOT_IMPLEMENTED_IN_PHASE1` | Phase 1에서 recovery 요청 | recovery 없이 abort |
| `OUT_OF_SCOPE_DIFF` | workflow 밖 파일·동작 변경 필요 또는 발생 | 변경 중단 후 abort |
| `HYDRATION_CONFLICT` | SessionStart worktree hydration receipt가 충돌을 기록함 | task 실행 전 abort |
| `VERIFICATION_FAILED` | verification gate 실패 | 실패 evidence와 함께 abort |
| `ARTIFACT_ROOT_UNWRITABLE` | branch/workspace-local artifact root에 쓸 수 없음 | 실행 전 abort |
| `COMMIT_REQUIRED_UNAVAILABLE` | workflow가 commit을 요구하지만 git/commit capability가 없음 | 실행 전 abort |
| `GITHUB_REQUIRED_UNAVAILABLE` | workflow가 PR/GitHub 작업을 요구하지만 GitHub capability가 없음 | 실행 전 abort |
| `VERIFICATION_UNAVAILABLE` | required verification을 수행할 방법이 없음 | 실행 전 abort |

## Execution rules

- workflow의 task graph 순서만 따릅니다.
- 가능한 경우 `tk-runner` subagent를 dispatch해 task execution을 격리합니다.
- dispatch prompt에는 workflow path/hash, task graph, allowed/forbidden changes, verification gates, abort policy, commit policy, hydration receipt path를 포함합니다.
- missing requirement를 임의 해석하지 않습니다.
- public API, DB, product behavior를 workflow 밖에서 재정의하지 않습니다.
- mid-flight 질문을 하지 않습니다. 결정이 필요하면 `HUMAN_DECISION_REQUIRED`로 abort합니다.
- out-of-scope diff를 만들지 않습니다. 발견하면 `OUT_OF_SCOPE_DIFF`로 abort합니다.
- verification 없이 success를 선언하지 않습니다.
- commit은 `commit_policy.mode=commit_on_success`만으로 수행하지 않습니다. commit unavailable 상태라도 commit이 required가 아니면 skip reason을 기록하고 success가 가능합니다. preflight receipt에 `user_preapproved_commit=true`와 `approval_source_ref`가 있어야 합니다.

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

기본 stdout은 compact receipt입니다. 첫 줄에 상태 기호를 두고, logical group 사이에 빈 줄을 둡니다.

상태 기호:

```text
✅ SUCCESS
🛑 ABORTED
⚠️ PARTIAL / skipped capability
```

SUCCESS stdout:

```text
✅ Launch 완료: <LCH-ID>
Branch Scope: <branch-key>
Workflow: .claude/tigerkit/branches/<branch-key>/gap/<WF-ID>.md
Workflow Hash: <sha256>
결과: SUCCESS

Runtime Harness: tk-runner / model=sonnet / status=<active|fallback_inline|unavailable>
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
- commit/PR이 optional인 workflow를 git/GitHub 부재만으로 abort
- required subagent/model harness unavailable 상태를 숨기고 success로 처리
