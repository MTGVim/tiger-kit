---
description: 현재 TigerKit 상태를 읽고 다음 안전 행동을 추천합니다.
argument-hint: "[goal/context?] [--scope current|branch|workspace] [--include-optional] [--no-write]"
---

이 명령은 TigerKit v8.0 next-action utility contract를 따릅니다. GAP → Launch → Reflect 실행 파이프라인의 일부가 아니며, 작업을 실행하지 않습니다.

사용자에게는 한글로 답합니다. 코드, path, URL, ticket, commit, hash, identifier, error는 원문 그대로 둘 수 있습니다.

목표: `/tk:next`는 현재 workspace/repo 상태와 TigerKit branch-local artifact를 읽어 다음 안전 행동 하나를 추천합니다.

```text
next = inspect state + classify blockers + recommend one safe next action
```

## Command surface

- plugin slash invocation은 `/tk:next`입니다.
- `/tk:next`는 utility command입니다. `/tk:gap → /tk:launch → /tk:reflect` primary pipeline을 대체하거나 자동 실행하지 않습니다.
- 자연어로 “다음 뭐 하지?”, “next action 정리해줘”처럼 요청해도 이 contract를 따릅니다.

## Inputs to inspect

가능한 범위에서 아래를 읽습니다.

- current worktree/workspace root
- current branch key 또는 workspace scope key
- `.claude/tigerkit/branches/<branch-key>/branch-state.json`
- latest GAP workflow/status: `.claude/tigerkit/branches/<branch-key>/gap/current.md`
- latest launch receipt: `.claude/tigerkit/branches/<branch-key>/launch/current.md`
- latest reflect report: `.claude/tigerkit/branches/<branch-key>/reflect/current.md`
- latest handoff: `.claude/tigerkit/branches/<branch-key>/handoffs/current.md`
- `.claude/tigerkit/global-index.json` handoff pointer
- current git status when git is available, using side-effect-minimized inspection such as `git --no-optional-locks status --porcelain=v1 -b`
- explicit user-provided goal/context in the command arguments

Missing artifacts are not errors. Treat them as evidence that a corresponding next action may be needed.

## Safety rules

`/tk:next` must not:

- execute `/tk:launch`
- run workflow tasks
- create commits or PRs
- mutate source files
- mutate durable repo rules
- convert speculative follow-ups into confirmed requirements
- ask mid-flight execution questions, because it has no flight/execution phase

`/tk:next` may:

- read files under the current workspace root
- inspect git status when available with side-effect-minimized commands such as `git --no-optional-locks status --porcelain=v1 -b`
- summarize latest TigerKit artifact states
- recommend a command or manual action
- identify blockers
- optionally write a generated next receipt only if a future contract explicitly enables it

MVP behavior is stdout-only. Do not write `.claude/tigerkit/.../next/` artifacts in v8.0.

## Decision policy

Prefer one primary next action. Classify it as exactly one of:

```text
recommended
blocked
optional
manual
none
```

Recommended priority order:

1. If no GAP workflow exists and the user has a goal/source, recommend `/tk:gap`.
2. If latest GAP is `GAP_BLOCKED`, recommend resolving the first blocking decision/source.
3. If latest GAP is `GAP_READY` and no launch receipt exists for the workflow, recommend `/tk:launch` only if preflight risks are acceptable; otherwise recommend preflight/manual check.
4. If latest launch is `ABORTED`, recommend the abort-specific repair path or `/tk:gap` regeneration.
5. If latest launch is successful and reflect is missing, recommend `/tk:reflect`.
6. If reflect produced proposal-only or needs-more-evidence items, recommend reviewing those items.
7. If handoff has pending backlog relevant to the current user goal, recommend the safest backlog item.
8. If nothing actionable is found, report `Next Action: 없음` and explain why.

Git dirty state should not automatically block `/tk:next`, but it may change the recommendation from execution to manual review/preflight. Use observational, side-effect-minimized status checks; do not run mutating shell commands.

## Output contract

Default stdout shape:

```text
Next Action: <한글 한 문장 또는 없음>
Status: recommended | blocked | optional | manual | none
Recommended Command: </tk:gap ... | /tk:launch | /tk:reflect | /tk:handoff | manual | none>
Why: <근거 기반 한 줄>
Blocked By: <none | missing source | human decision | dirty workspace | verification failure | artifact missing | other>
References:
- <artifact path or source ref>
```

If multiple useful follow-ups exist, include at most three under `Alternatives`.

```text
Alternatives:
- <optional action 1>
- <optional action 2>
```

Do not output long artifact bodies. Point to paths instead.

## Examples

No workflow exists:

```text
Next Action: 현재 목표를 `/tk:gap`으로 봉인 가능한 workflow로 정리하세요.
Status: recommended
Recommended Command: /tk:gap "<goal/source>"
Why: branch-local GAP workflow가 아직 없습니다.
Blocked By: none
References:
- .claude/tigerkit/branches/<branch-key>/branch-state.json: missing lastWorkflowPath
```

Blocked GAP:

```text
Next Action: Q1의 API owner 결정을 먼저 확인하세요.
Status: blocked
Recommended Command: manual
Why: 최신 GAP이 GAP_BLOCKED이고 launch workflow가 없습니다.
Blocked By: human decision
References:
- .claude/tigerkit/branches/<branch-key>/gap/current.md
```

Ready to launch:

```text
Next Action: sealed workflow preflight 후 `/tk:launch`를 실행하세요.
Status: recommended
Recommended Command: /tk:launch
Why: 최신 GAP은 GAP_READY이고 해당 workflow의 launch receipt가 없습니다.
Blocked By: none
References:
- .claude/tigerkit/branches/<branch-key>/gap/current.md
```
