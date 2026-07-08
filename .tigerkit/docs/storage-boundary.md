# TigerKit storage boundary

이 문서는 TigerKit의 현재 저장 경계만 설명합니다.

## Core rule

```text
runtime generated state + repo-scoped root with worktree-scoped draft artifacts = ~/.tigerkit/ file-only state outside the project repository
reflect direct-write targets = repo CLAUDE.local.md or host-native user-global guidance surface
```

TigerKit는 active runtime generated state와 `/tk:handoff`, `/tk:to-prd`, `/tk:to-issues` 같은 repo-scoped draft artifacts, 그리고 `/tk:browser-verify` repo profile을 project repository 밖 `~/.tigerkit/` 아래에 둡니다. reflect direct-write target인 repo `CLAUDE.local.md`와 host-native user-global guidance surface는 이 artifact store와 별개의 target입니다.

## Active runtime state

```text
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/<GAP-ID>.md
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/current.md
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/<GAP-ID>.packet.json
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/current.packet.json
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/reflect/REFLECT-YYYYMMDD-HHmmss-RAND.yaml
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/reflect/current.yaml
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/branch-state.json
```

역할:
- `/tk:gap` report archive/current
- `/tk:gap` packet archive/current
- `/tk:reflect` ledger archive/current
- branch-local generated pointer

`repo-key`와 `scope-key` 계산은 `scripts/tigerkit_state.py` helper가 수행합니다.

## Worktree-scoped draft artifacts under a repo-scoped root

```text
~/.tigerkit/repos/<repo-key>/worktrees/<worktree-key>/handoffs/current.md
~/.tigerkit/repos/<repo-key>/worktrees/<worktree-key>/prd/current.md
~/.tigerkit/repos/<repo-key>/worktrees/<worktree-key>/issues/current.md
```

이 경로들은 tracked product source가 아니라 repo-scoped `~/.tigerkit` root 아래의 worktree-scoped generated draft artifact 경로입니다. 선택적으로 archive를 남길 수는 있지만 기본은 current-first 입니다. `repo-key`와 `worktree-key` 계산은 `scripts/tigerkit_state.py` helper가 수행합니다. `worktree-key`는 현재 worktree를 구분하는 canonicalized directory key로 보고, 서로 다른 worktree draft가 섞이지 않게 합니다.

## Repo-scoped browser-verify profile

```text
~/.tigerkit/repos/<repo-key>/browser-verify/env.md
~/.tigerkit/repos/<repo-key>/browser-verify/login.md
~/.tigerkit/repos/<repo-key>/browser-verify/login.local.md
~/.tigerkit/repos/<repo-key>/browser-verify/screens/README.md
```

이 경로들은 `/tk:browser-verify`가 읽는 repo-scoped profile 경로입니다. legacy `ui-diff` profile이 남아 있으면 migration guide를 우선하고, 둘 다 없을 때만 missing-file bootstrap을 수행합니다. 기존 파일은 덮어쓰지 않습니다. `repo-key` 계산은 `scripts/tigerkit_state.py browser-verify-paths` helper가 수행합니다.

## Not stored here

TigerKit runtime generated state는 아래를 canonical source로 저장하지 않습니다.

- source code
- plugin manifest
- command source
- agent source
- user skill source
- Claude Code auto memory

## Promotion boundary

`/tk:reflect`는 learning을 분류하지만, runtime generated state가 durable target 자체를 소유하지는 않습니다.

| Target | Canonical owner or action |
|---|---|
| `repo-local` | repo `<git-root>/CLAUDE.local.md` |
| `repo-shared` | suggest-only proposal |
| `user-global` | supported host guidance surface |
| `skill` | explicit-apply proposal to user skill surface |
| `hook` | suggest-only proposal |
| `command` | suggest-only proposal |
| `agent` | suggest-only proposal |
| `discard` | no storage |

## Git policy

Active `~/.tigerkit/` state와 repo-scoped draft artifacts는 project repository 밖에 있으므로 repo `.gitignore`가 canonical storage boundary를 정의하지 않습니다.

repo `.gitignore`의 `.claude/tigerkit/` ignore는 local leftover housekeeping일 수는 있지만 active write target 정의가 아닙니다. `.claude/` 전체를 ignore하지 않는다는 원칙은 유지합니다.
