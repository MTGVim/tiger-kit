# TigerKit storage boundary

이 문서는 TigerKit의 현재 저장 경계만 설명합니다.

## Core rule

```text
runtime generated state = ~/.tigerkit/ file-only state outside the project repository
repo-local draft artifacts = .claude/tigerkit/ for handoff / PRD / issue drafts
```

TigerKit는 active runtime generated state를 project repository 밖 `~/.tigerkit/` 아래에 둡니다. repo 안에서는 `/tk:handoff`, `/tk:to-prd`, `/tk:to-issues` 같은 repo-local draft artifacts만 `.claude/tigerkit/` 아래에 둡니다.

## Active runtime state

```text
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/<GAP-ID>.md
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/current.md
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/reflect/REFLECT-YYYYMMDD-HHmmss-RAND.yaml
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/reflect/current.yaml
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/branch-state.json
```

역할:
- `/tk:gap` report archive/current
- `/tk:reflect` ledger archive/current
- branch-local generated pointer

`repo-key`와 `scope-key` 계산은 `scripts/tigerkit_state.py` helper가 수행합니다.

## Repo-local draft artifacts

```text
<git-root>/.claude/tigerkit/handoffs/HANDOFF-YYYYMMDD-HHmmss.md
<git-root>/.claude/tigerkit/prd/PRD-YYYYMMDD-HHmmss.md
<git-root>/.claude/tigerkit/issues/ISSUES-YYYYMMDD-HHmmss.md
```

이 경로들은 tracked product source가 아니라 repo-local draft artifact 경로입니다.

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

Active `~/.tigerkit/` state는 project repository 밖에 있으므로 repo `.gitignore` 대상이 아닙니다.

Repo-local draft artifacts는 local working artifacts이므로 계속 ignore합니다.

```gitignore
.claude/tigerkit/
```

`.claude/` 전체를 ignore하지 않습니다.
