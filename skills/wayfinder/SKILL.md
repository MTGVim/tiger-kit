---
name: wayfinder
description: shared map 트리거입니다.
disable-model-invocation: true
---

# Wayfinder

`/tk:wayfinder` wrapper skill입니다. map path, output contract, file-only boundary의 source of truth는 `commands/wayfinder.md`입니다.

## Use when

- 긴 작업의 현재 slice와 재개 힌트를 정리해야 할 때
- compact나 세션 전환 뒤에도 빠르게 상태를 복구하고 싶을 때

## Wrapper rules

- 이 skill은 `commands/wayfinder.md`를 대체하지 않는 얇은 wrapper입니다.
- worktree-scoped current-first map artifact와 blocked-by / blocking edges 정리 semantics를 그대로 따릅니다.
- tracker 연동 없이 file-only state로 남깁니다.
