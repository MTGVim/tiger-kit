# TigerKit 운영 산출물 구조

이 문서는 TigerKit의 현재 산출물 배치와 책임을 설명합니다. 저장 경계는 `.tigerkit/docs/storage-boundary.md`를 기준으로 봅니다.

## Active runtime generated layout

```text
~/.tigerkit/
  repos/
    <repo-key>/
      branches/
        <scope-key>/
          gap/
            GAP-YYYYMMDD-HHmmss-RAND.md
            current.md
          reflect/
            REFLECT-YYYYMMDD-HHmmss-RAND.yaml
            current.yaml
          branch-state.json
```

## Repo-local draft artifacts

```text
<git-root>/.claude/tigerkit/handoffs/HANDOFF-YYYYMMDD-HHmmss.md
<git-root>/.claude/tigerkit/prd/PRD-YYYYMMDD-HHmmss.md
<git-root>/.claude/tigerkit/issues/ISSUES-YYYYMMDD-HHmmss.md
```

## 파일 책임

| 파일 | 역할 | 저장 성격 |
|---|---|---|
| `~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/<GAP-ID>.md` | `/tk:gap` one-shot report archive | generated working memory |
| `~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/current.md` | 최신 gap report copy | generated pointer |
| `~/.tigerkit/repos/<repo-key>/branches/<scope-key>/reflect/REFLECT-YYYYMMDD-HHmmss-RAND.yaml` | `/tk:reflect` ledger archive | generated working memory |
| `~/.tigerkit/repos/<repo-key>/branches/<scope-key>/reflect/current.yaml` | 최신 reflect ledger copy | generated pointer |
| `~/.tigerkit/repos/<repo-key>/branches/<scope-key>/branch-state.json` | latest generated artifact pointer | generated index |
| `scripts/tigerkit_state.py` | active generated state helper (`write-gap`, path calculation) | shipped helper |
| `<git-root>/.claude/tigerkit/handoffs/HANDOFF-YYYYMMDD-HHmmss.md` | `/tk:handoff` repo-local draft | repo-local draft artifact |
| `<git-root>/.claude/tigerkit/prd/PRD-YYYYMMDD-HHmmss.md` | `/tk:to-prd` repo-local draft | repo-local draft artifact |
| `<git-root>/.claude/tigerkit/issues/ISSUES-YYYYMMDD-HHmmss.md` | `/tk:to-issues` repo-local draft | repo-local draft artifact |
| repo `CLAUDE.local.md` | reflect eligible repo-local apply target | local guidance |
| repo `CLAUDE.md` | reflect suggest-only target | shared repo guidance |

Reflect direct write가 발생하는 경우에는 changed path를 출력하고, exact apply_plan은 ledger를 source of truth로 삼아야 합니다.
