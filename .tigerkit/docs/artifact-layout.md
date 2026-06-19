# TigerKit 운영 산출물 구조

이 문서는 TigerKit Slim 산출물 배치와 책임을 설명합니다.

## 기본 구조

```text
.claude/
  tigerkit/
    branches/
      <scope-key>/
        gap/
          GAP-YYYYMMDD-HHmmss-RAND.md
          current.md
        grill/
          GRILL-YYYYMMDD-HHmmss-RAND.md
          current.md
        afk/
          decisions/
            DEC-YYYYMMDD-HHmmss-RAND.md
            current.md
        reflect/
          RFL-YYYYMMDD-HHmmss-RAND.md
          current.md
        branch-state.json

docs/
  migration-from-launch.md
  patron-catalog.md
  patron-lifecycle.md
  reflect-file-policy.md
  afk-default.md
  vowline-integration.md
  recommended-tools.md
```

## Scope key

Git branch가 있으면 branch 기반 scope key를 사용합니다. Git이 없으면 workspace fallback scope key를 사용합니다.

```text
workspace-<basename-slug>--<sha256(absWorkspaceRoot).slice(0, 8)>
```

## 파일 책임

| 파일 | 역할 | 저장 성격 |
|---|---|---|
| `.claude/tigerkit/branches/<scope-key>/gap/<GAP-ID>.md` | `/tk:gap` one-shot report archive | generated working memory |
| `.claude/tigerkit/branches/<scope-key>/gap/current.md` | 최신 gap report copy | generated pointer |
| `.claude/tigerkit/branches/<scope-key>/grill/<GRILL-ID>.md` | `/tk:grill` question/risk report archive | generated working memory |
| `.claude/tigerkit/branches/<scope-key>/grill/current.md` | 최신 grill report copy | generated pointer |
| `.claude/tigerkit/branches/<scope-key>/afk/decisions/<DEC-ID>.md` | Patron decision ledger archive | generated working memory |
| `.claude/tigerkit/branches/<scope-key>/afk/decisions/current.md` | 최신 decision ledger copy | generated pointer |
| `.claude/tigerkit/branches/<scope-key>/reflect/<RFL-ID>.md` | reflect generated report archive | generated working memory |
| `.claude/tigerkit/branches/<scope-key>/reflect/current.md` | 최신 reflect report copy | generated pointer |
| `.claude/tigerkit/branches/<scope-key>/branch-state.json` | latest generated artifact pointers | generated index |
| `~/.claude/tigerkit/config.json` | AFK default, Patron, Vowline, reflect policy source of truth | user config |
| repo `CLAUDE.local.md` | reflect repo-local auto apply target | local guidance |
| repo `CLAUDE.md` | reflect suggest-only target | shared repo guidance |

## Deprecated layout

아래 launch-era generated areas는 Slim active flow가 새로 만들지 않습니다.

- `.claude/tigerkit/branches/<scope-key>/launch/`
- `.claude/tigerkit/branches/<scope-key>/review/`
- `.claude/tigerkit/branches/<scope-key>/next/`
- `.claude/tigerkit/branches/<scope-key>/handoffs/`
- sealed `tigerkit-launch-workflow` artifacts

기존 파일이 있으면 migration context로 읽을 수 있지만 새 source of truth로 취급하지 않습니다.

## Git ignore

권장 `.gitignore`:

```gitignore
.claude/tigerkit/
```

`.claude/` 전체를 ignore하지 않습니다.
