# Issue #398: tk-autoresearch

기준: `59d97faa4630b338d5f1cfd777bd39bbc0528b45`.

## 변경

- `tk-discover`의 frontier·fog·dependency·provenance 계약을 `tk-autoresearch`로 이관하고 `renamed_from` 평가 계약으로 기존 critical behavior를 보존합니다.
- 승인된 research workspace에 한해 pilot/benchmark/prototype/experiment의 로컬 mutation을 허용하되 제품 worktree, production data, push/PR/merge/release 권한은 확장하지 않습니다.
- finding, direction, research-program 세 수준의 수렴과 `NO-ACTION`/`NO-DELTA`를 추가합니다.
- durable state는 `.tigerkit/autoresearch/state.md` 하나가 정본이며 필요한 실험 근거만 `experiments/<EXP-ID>/`에 둡니다. scheduler, DB, cursor, per-run transcript는 만들지 않습니다.
- `tk-research`는 primary-source resolution과 source-liveness/claim-faithfulness 분리를 강화합니다.

## Upstream

- Orchestra Research `773a52944ba4747a18bd4ae9ade53fff041adcbc`
- uditgoenka/autoresearch `050e30dc4ba0974b03f2873111b9901ec3211390`
- Companion-Inc/feynman `4d62d07a7e8eb1fba1b02d6547e6425e456715eb`
- bryanshake/autoresearch `0fa9a9336fc84a6b069111adb03ca21fabb5394b`
- rohankgeorge/the-researcher `1184d246c290a4ff772ea669ac6b9f9914d3f7da`

각 keep/adapt/omit 및 검증 한계는 skill-local `references/sources.md`에 기록했습니다.

## 평가

- 기존 `tk-discover` behavior와 trigger 계약은 rename으로 보존합니다.
- catalog의 discovery routing은 명시 migration으로 autoresearch case로 이동합니다.
- pilot-first, no-delta stop, research mutation boundary, program convergence와 `tk-research` provenance 검증을 release-critical 대상으로 추가합니다.
