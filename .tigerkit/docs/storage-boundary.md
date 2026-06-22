# TigerKit storage boundary

이 문서는 TigerKit generated state의 active external layout과 legacy repo-inside layout의 경계를 구분한다.

## Core rule

```text
active generated state = ~/.tigerkit/ file-only state outside the project repository
legacy repo-inside state = .claude/tigerkit/ migration context only
execute support owner = support/execute-support-matrix.json
```

TigerKit generated state는 durable repo guidance, shared team rule, user-global guidance, user skill source, command source, agent source의 canonical home이 아니다. Execute boundary runtime packaging은 plugin package 안의 declared component가 소유하고, active execution receipt는 repository 밖에 저장한다.

## Active external state

Active generated state는 project repository 밖 `~/.tigerkit/` 아래에 둔다. `TIGERKIT_STATE_ROOT`가 있으면 그 값을 state root로 사용할 수 있지만, 기본 contract는 `~/.tigerkit/`이다.

```text
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/<GAP-ID>.md
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/current.md
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/loop-specs/<spec-id>/spec.yaml
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/executions/<execution-id>.yaml
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/branch-state.json
~/.tigerkit/capabilities/execute-write-boundary/<plugin-version>/<environment-key>/proof.yaml
```

역할:

- `/tk:gap` one-shot report archive
- latest gap report pointer
- `/tk:loop-spec` worktree-scoped LoopSpec v2
- `/tk:execute` immutable execution receipt
- branch/workspace-local generated index
- packaged execute write-boundary capability proof cache

`repo-key`와 `scope-key` 계산은 `scripts/tigerkit_state.py` helper만 수행한다. Command prompt나 agent가 path-key 알고리즘을 재구현하지 않는다.

## Execution receipt boundary

Active execution receipt canonical path:

```text
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/executions/<execution-id>.yaml
```

Rules:

- repository 내부 `.tigerkit/executions/`는 사용하지 않는다.
- helper가 repo-key, scope-key, canonical path의 유일한 authority다.
- receipt는 temp file 작성 후 atomic rename으로 확정한다.
- finalized receipt는 immutable하다.
- retry 또는 재실행은 새 `executionId`를 생성한다.
- rejected execution도 repository/scope identity를 resolve한 이후라면 receipt를 저장한다.
- identity set을 확정하지 못한 pre-receipt rejection은 structured command output만 반환하며 receipt v1이라고 표시하지 않는다.
- `/tk:reflect <execution-id>`는 동일 helper로 canonical path를 resolve한다.

## Capability proof boundary

Capability proof canonical root:

```text
~/.tigerkit/capabilities/execute-write-boundary/<plugin-version>/<environment-key>/proof.yaml
```

Rules:

- proof schema is `tigerkit.capability-proof/execute-write-boundary-v1`.
- support matrix schema is `tigerkit.execute-support-matrix/v1`.
- `support/execute-support-matrix.json` owns public, preview, unsupported environment set.
- support matrix `boundaryComponents[]` is the canonical ordered package path set.
- proof `componentDigests[]` must exact-match support matrix component path set plus fixed proof owner path set.
- proof `tests[]` must be exactly `CAP-01` through `CAP-10` in order and all `passed`.
- proof `runtimeBinding` must byte-match current helper capture.
- proof `supportMatrixDigest` must match current package support matrix bytes.

## Boundary runtime packaging

Current selected architecture is `hook_gate` preview. Packaged components:

```text
hooks/hooks.json
hooks/execute-write-boundary.py
```

`hooks/execute-write-boundary.py` is inert unless `TIGERKIT_EXECUTE_BOUNDARY_FILE` is present. During execute, boundary file declares `repoRoot`, `modify`, `create`, `delete`, and `exclude`. The hook rejects out-of-scope, excluded, and path-escape writes before tool execution.

Hook files are mandatory only for hook architecture. Other architecture components must be declared by support matrix if selected later.

## Legacy SessionStart state

기존 decline marker는 inactive legacy state로만 보존하며 core command/runtime이 읽거나 쓰지 않는다.

```text
~/.tigerkit/local/session-start/worktree-context-declines.json
.claude/tigerkit/local/session-start/worktree-context-declines.json
```

처리 원칙:

- 자동 삭제하지 않는다.
- 자동 이관하지 않는다.
- 새 core command contract의 active generated layout으로 취급하지 않는다.
- 새 core command/runtime은 해당 marker를 읽거나 쓰지 않는다.

## Legacy repo-inside state

`.claude/tigerkit/`는 legacy/migration context다. 새 write path가 아니다.

기존 파일이 있으면 migration context로 언급할 수 있지만, active source of truth로 취급하지 않는다. 새 generated state, gap report, pointer write, LoopSpec, execution receipt는 `~/.tigerkit/`에 쓴다.

## Not stored here

TigerKit generated state에는 아래를 canonical source로 저장하지 않는다.

- repo `CLAUDE.md`
- repo `CLAUDE.local.md`
- repo shared docs 본문
- user `CLAUDE.md`
- user `PROFILE.md`
- user skill source
- command source
- agent source
- source code
- product artifact
- Claude Code auto memory backup/mirror

## Promotion boundary

`/tk:reflect`는 learning을 분류할 수 있지만, TigerKit generated state가 promotion target 자체를 소유하지 않는다.

| Target | Canonical owner or action |
|---|---|
| `repo-local` | repo `<git-root>/CLAUDE.local.md` |
| `repo-shared` | suggest-only proposal |
| `user-global` | suggest-only proposal |
| `skill` | suggest-only proposal to user skill surface |
| `hook` | suggest-only proposal |
| `command` | suggest-only proposal |
| `agent` | suggest-only proposal |
| `discard` | no storage |

## Git policy

Active `~/.tigerkit/` state는 project repository 밖에 있으므로 repo `.gitignore` 대상이 아니다.

Legacy `.claude/tigerkit/` repo-inside state는 migration context로 남을 수 있으므로 계속 git ignore 대상이다.

```gitignore
.claude/tigerkit/
```

`.claude/` 전체를 ignore 대상으로 확대하지 않는다.

## Review checklist

1. active write path가 project repository 밖 `~/.tigerkit/`인가?
2. repo identity와 branch/workspace scope가 충돌 없이 분리되는가?
3. `.claude/tigerkit/`는 legacy/migration context로만 쓰는가?
4. execution receipt가 `executions/<execution-id>.yaml`에 atomic write되는가?
5. support matrix가 public environment set의 유일한 owner인가?
6. capability proof가 current package digest/runtime binding/component set과 exact-match하는가?
7. user-global guidance, shared repo rule, skill source, Claude Code auto memory를 복제하지 않는가?

## Bottom line

TigerKit active generated state는 `~/.tigerkit/` 아래의 file-only external state다. Execute receipt와 capability proof도 repository 밖에 저장한다. Public execute support claim은 `support/execute-support-matrix.json`과 matching packaged proof가 함께 만족할 때만 성립한다.
