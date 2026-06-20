# TigerKit 운영 산출물 구조

이 문서는 현재 TigerKit 산출물 배치와 책임을 설명합니다. `.claude/tigerkit/`에 무엇을 두고 무엇을 두지 않는지는 `.tigerkit/docs/storage-boundary.md`를 기준으로 봅니다.

## 현재 generated 구조

```text
.claude/
  tigerkit/
    branches/
      <scope-key>/
        gap/
          GAP-YYYYMMDD-HHmmss-RAND.md
          current.md
        branch-state.json
```

Reflect/README/RFC 같은 tracked docs는 generated 구조가 아니라 repo 문서 surface다.

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
| `.claude/tigerkit/branches/<scope-key>/branch-state.json` | latest generated artifact pointer | generated index |
| repo `CLAUDE.local.md` | reflect repo-local auto apply target | local guidance |
| repo `CLAUDE.md` | reflect suggest-only target | shared repo guidance |

`/tk:reflect`는 현재 active generated artifact layout을 문서화하지 않습니다. Reflect command가 파일을 쓰는 경우에는 receipt에 changed path를 출력해야 합니다.

## Optional helper docs

`.tigerkit/docs/reflect-promotion-helpers.md`는 선택형 참고 문서입니다. Runtime behavior, installer, generator, generated artifact layout을 소유하지 않습니다.

## Deprecated layout

아래 launch-era generated areas는 새 TigerKit active flow가 만들지 않습니다.

- `.claude/tigerkit/branches/<scope-key>/launch/`
- `.claude/tigerkit/branches/<scope-key>/review/`
- `.claude/tigerkit/branches/<scope-key>/next/`
- `.claude/tigerkit/branches/<scope-key>/handoffs/`
- AFK / Patron decision ledger artifacts
- setup/config wizard artifacts

기존 파일이 있으면 migration context로 읽을 수 있지만 새 source of truth로 취급하지 않습니다.

## Git ignore

권장 `.gitignore`:

```gitignore
.claude/tigerkit/
```

`.claude/` 전체를 ignore하지 않습니다.
