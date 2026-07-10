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
      worktrees/
        <worktree-key>/
          handoffs/
            current.md
          prd/
            current.md
          issues/
            current.md
          ledger/
            current.md
          quiz/
            current.md
          wayfinder/
            current.md
      browser-verify/
        env.md
        login.md
        login.local.md
        screens/
          README.md
```

## Worktree-scoped draft artifacts under a repo-scoped root

```text
~/.tigerkit/repos/<repo-key>/worktrees/<worktree-key>/handoffs/current.md
~/.tigerkit/repos/<repo-key>/worktrees/<worktree-key>/prd/current.md
~/.tigerkit/repos/<repo-key>/worktrees/<worktree-key>/issues/current.md
~/.tigerkit/repos/<repo-key>/worktrees/<worktree-key>/ledger/current.md
~/.tigerkit/repos/<repo-key>/worktrees/<worktree-key>/quiz/current.md
~/.tigerkit/repos/<repo-key>/worktrees/<worktree-key>/wayfinder/current.md
```

## 파일 책임

| 파일 | 역할 | 저장 성격 |
|---|---|---|
| `~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/<GAP-ID>.md` | `/tk:gap` one-shot report archive | generated working memory |
| `~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/current.md` | 최신 gap report copy | generated pointer |
| `~/.tigerkit/repos/<repo-key>/branches/<scope-key>/reflect/REFLECT-YYYYMMDD-HHmmss-RAND.yaml` | `/tk:reflect` ledger archive | generated working memory |
| `~/.tigerkit/repos/<repo-key>/branches/<scope-key>/reflect/current.yaml` | 최신 reflect ledger copy | generated pointer |
| `~/.tigerkit/repos/<repo-key>/branches/<scope-key>/branch-state.json` | latest generated artifact pointer | generated index |
| `scripts/tigerkit_state.py` | active generated state helper (`write-gap`, `draft-paths`, `usage-summary`, `browser-verify-paths`, key/path calculation) | shipped helper |
| `~/.tigerkit/repos/<repo-key>/worktrees/<worktree-key>/handoffs/current.md` | `/tk:handoff` current-first handoff draft | worktree-scoped draft artifact under repo-scoped root |
| `~/.tigerkit/repos/<repo-key>/worktrees/<worktree-key>/prd/current.md` | `/tk:to-prd` current-first PRD draft | worktree-scoped draft artifact under repo-scoped root |
| `~/.tigerkit/repos/<repo-key>/worktrees/<worktree-key>/issues/current.md` | `/tk:to-issues` current-first issue draft set | worktree-scoped draft artifact under repo-scoped root |
| `~/.tigerkit/repos/<repo-key>/worktrees/<worktree-key>/ledger/current.md` | decision ledger current draft | worktree-scoped draft artifact under repo-scoped root |
| `~/.tigerkit/repos/<repo-key>/worktrees/<worktree-key>/quiz/current.md` | `/tk:quiz` current-first comprehension report | worktree-scoped draft artifact under repo-scoped root |
| `~/.tigerkit/repos/<repo-key>/worktrees/<worktree-key>/wayfinder/current.md` | `/tk:wayfinder` current-first shared map | worktree-scoped draft artifact under repo-scoped root |
| `~/.tigerkit/repos/<repo-key>/browser-verify/env.md` | `/tk:browser-verify` env profile | repo-scoped profile |
| `~/.tigerkit/repos/<repo-key>/browser-verify/login.md` | `/tk:browser-verify` tracked login/context profile | repo-scoped profile |
| `~/.tigerkit/repos/<repo-key>/browser-verify/login.local.md` | `/tk:browser-verify` local override profile | repo-scoped profile |
| `~/.tigerkit/repos/<repo-key>/browser-verify/screens/README.md` | `/tk:browser-verify` screen catalog root | repo-scoped profile |
| repo `CLAUDE.local.md` | reflect eligible repo-local apply target | local guidance |
| repo `CLAUDE.md` | reflect suggest-only target | shared repo guidance |

Reflect direct write가 발생하는 경우에는 changed path를 출력하고, exact apply_plan은 ledger를 source of truth로 삼아야 합니다.
