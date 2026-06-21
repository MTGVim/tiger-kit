# TigerKit storage boundary

이 문서는 TigerKit generated state의 active external layout과 legacy repo-inside layout의 경계를 구분한다.

## Core rule

```text
active generated state = ~/.tigerkit/ file-only state outside the project repository
legacy repo-inside state = .claude/tigerkit/ migration context only
core tk plugin = hook-free / explicit commands only
```

TigerKit generated state는 durable repo guidance, shared team rule, user-global guidance, user skill source, hook settings, command source, agent source의 canonical home이 아니다.

## Active external state

Core `tk` plugin은 hook-free다. Active generated state는 project repository 밖 `~/.tigerkit/` 아래에 둔다. `TIGERKIT_STATE_ROOT`가 있으면 그 값을 state root로 사용할 수 있지만, 기본 contract는 `~/.tigerkit/`이다.

```text
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/<GAP-ID>.md
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/current.md
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/loop-specs/<spec-id>/spec.yaml
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/branch-state.json
```

역할:

- `/tk:gap` one-shot report archive
- latest gap report pointer
- `/tk:loop-spec` worktree-scoped recommendation spec
- branch/workspace-local generated index

`repo-key`는 repo root를 기준으로 만든 stable key다. 권장 형식:

```text
<repo-basename-slug>--<sha256(absRepoRoot).slice(0, 8)>
```

Git repo root를 확인할 수 없으면 workspace root를 기준으로 같은 형식을 사용한다.

`scope-key`는 Git branch가 있으면 branch 기반 key를 사용하고, Git이 없으면 workspace fallback key를 사용한다.

```text
workspace-<basename-slug>--<sha256(absWorkspaceRoot).slice(0, 8)>
```

Reflect는 TigerKit generated artifact layout을 갖지 않는다. `/tk:reflect`가 파일을 쓰는 경우, 해당 command receipt는 실제 쓴 changed path를 출력해야 한다.

## Legacy SessionStart state

Core `tk` plugin은 active `SessionStart` hook을 제공하지 않는다. 기존 decline marker는 inactive legacy state로만 보존하며 core command/runtime이 읽거나 쓰지 않는다.

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

기존 파일이 있으면 migration context로 언급할 수 있지만, active source of truth로 취급하지 않는다. 새 generated state, gap report, pointer write는 `~/.tigerkit/`에 쓴다.

기존 repo-inside layout:

```text
.claude/tigerkit/local/session-start/worktree-context-declines.json
.claude/tigerkit/branches/<scope-key>/gap/<GAP-ID>.md
.claude/tigerkit/branches/<scope-key>/gap/current.md
.claude/tigerkit/branches/<scope-key>/branch-state.json
```

## Not stored here

TigerKit generated state에는 아래를 canonical source로 저장하지 않는다.

- repo `CLAUDE.md`
- repo `CLAUDE.local.md`
- repo shared docs 본문
- user `CLAUDE.md`
- user `PROFILE.md`
- user skill source
- hook settings
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

`.tigerkit/docs/reflect-promotion-helpers.md` 같은 helper docs는 선택형 참고 문서다. Runtime write path, installer, generator, generated state layout을 선언하지 않는다.

## Receipt boundary

Command가 파일을 쓰면 receipt는 changed path를 출력한다. 파일을 쓰지 않으면 `NONE`으로 표시한다.

Receipt가 proposal을 포함해도 아래를 뜻하지 않는다.

- hook installed
- settings updated
- command generated
- agent generated
- user skill generated under TigerKit generated state
- plugin manifest modified
- Claude Code auto memory written/mirrored/backed up

## Git policy

Active `~/.tigerkit/` state는 project repository 밖에 있으므로 repo `.gitignore` 대상이 아니다.

Legacy `.claude/tigerkit/` repo-inside state는 migration context로 남을 수 있으므로 계속 git ignore 대상이다.

```gitignore
.claude/tigerkit/
```

`.claude/` 전체를 ignore 대상으로 확대하지 않는다.

## Review checklist

TigerKit generated state path를 추가하거나 수정할 때 확인한다.

1. active write path가 project repository 밖 `~/.tigerkit/`인가?
2. repo identity와 branch/workspace scope가 충돌 없이 분리되는가?
3. `.claude/tigerkit/`는 legacy/migration context로만 쓰는가?
4. canonical durable source는 다른 표면이 소유하는가?
5. 파일을 쓴 command receipt가 changed path를 출력하는가?
6. user-global guidance, shared repo rule, skill source, Claude Code auto memory를 복제하지 않는가?
7. core plugin active surface에 `SessionStart` hook을 다시 추가하지 않았는가?

## Bottom line

TigerKit active generated state는 `~/.tigerkit/` 아래의 file-only external state다. Core `tk` plugin은 hook-free이며 `.claude/tigerkit/`와 legacy decline marker는 migration context로만 남긴다.
