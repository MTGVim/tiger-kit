# TigerKit 운영 산출물 구조

이 문서는 현재 TigerKit 산출물 배치와 책임을 설명합니다. active state와 legacy state의 경계는 `.tigerkit/docs/storage-boundary.md`를 기준으로 봅니다.

현재 active generated layout은 project repository 밖 `~/.tigerkit/` 아래의 file-only state입니다. `.claude/tigerkit/`는 legacy/migration context로만 남습니다. 이 저장소의 실제 구현 표면은 SessionStart hook read path와 command-generated state contract입니다.

## Active generated 구조

```text
~/.tigerkit/
  local/
    session-start/
      worktree-context-declines.json
  repos/
    <repo-key>/
      branches/
        <scope-key>/
          gap/
            GAP-YYYYMMDD-HHmmss-RAND.md
            current.md
          branch-state.json
```

Reflect/README/RFC 같은 tracked docs는 generated 구조가 아니라 repo 문서 surface입니다.

## Repo key

`repo-key`는 repo root를 기준으로 만든 stable key입니다. 권장 형식:

```text
<repo-basename-slug>--<sha256(absRepoRoot).slice(0, 8)>
```

Git repo root를 확인할 수 없으면 workspace root를 기준으로 같은 형식을 사용합니다.

## Scope key

Git branch가 있으면 branch 기반 scope key를 사용합니다. Git이 없으면 workspace fallback scope key를 사용합니다.

```text
workspace-<basename-slug>--<sha256(absWorkspaceRoot).slice(0, 8)>
```

## 파일 책임

| 파일 | 역할 | 저장 성격 |
|---|---|---|
| `~/.tigerkit/local/session-start/worktree-context-declines.json` | SessionStart worktree context proposal decline marker | user-local generated marker |
| `~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/<GAP-ID>.md` | `/tk:gap` one-shot report archive | generated working memory |
| `~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/current.md` | 최신 gap report copy | generated pointer |
| `~/.tigerkit/repos/<repo-key>/branches/<scope-key>/branch-state.json` | latest generated artifact pointer | generated index |
| `scripts/tigerkit_state.py` | active generated state helper (`write-gap`, `record-session-start-decline`, path calculation) | shipped helper |
| repo `CLAUDE.local.md` | reflect repo-local auto apply target | local guidance |
| repo `CLAUDE.md` | reflect suggest-only target | shared repo guidance |

`/tk:reflect`는 현재 active generated artifact layout을 문서화하지 않습니다. Reflect command가 파일을 쓰는 경우에는 receipt에 changed path를 출력해야 합니다.

## Optional helper docs

`.tigerkit/docs/reflect-promotion-helpers.md`는 선택형 참고 문서입니다. Runtime behavior, installer, generator, generated artifact layout을 소유하지 않습니다.

## Legacy layout

아래 repo-inside areas는 새 TigerKit active flow가 쓰지 않습니다. 기존 파일이 있으면 migration context 또는 legacy fallback으로 읽을 수 있지만 새 source of truth로 취급하지 않습니다.

- `.claude/tigerkit/local/session-start/worktree-context-declines.json`
- `.claude/tigerkit/branches/<scope-key>/gap/`
- `.claude/tigerkit/branches/<scope-key>/launch/`
- `.claude/tigerkit/branches/<scope-key>/review/`
- `.claude/tigerkit/branches/<scope-key>/next/`
- `.claude/tigerkit/branches/<scope-key>/handoffs/`
- AFK / Patron decision ledger artifacts
- setup/config wizard artifacts

## Git ignore

Active `~/.tigerkit/` state는 project repository 밖에 있으므로 repo `.gitignore` 대상이 아닙니다.

Legacy `.claude/tigerkit/` repo-inside state는 migration context로 남을 수 있으므로 계속 ignore합니다.

```gitignore
.claude/tigerkit/
```

`.claude/` 전체를 ignore하지 않습니다.
