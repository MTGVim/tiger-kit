---
name: handon
description: handoff 재열기 트리거입니다.
---

# Handon

`/tk:handoff`가 남긴 current-first handoff artifact를 다시 열어 다음 작업을 바로 이어가기 위한 read-only skill입니다.

## Goal

- 현재 repo/worktree의 최신 handoff를 source of truth로 읽습니다.
- handoff가 있으면 남은 작업과 리스크를 빠르게 복구합니다.
- handoff가 없으면 expected path를 정확히 알려주고 추측하지 않습니다.

## Default source path

```text
~/.tigerkit/repos/<repo-key>/worktrees/<worktree-key>/handoffs/current.md
```

`repo-key`와 `worktree-key`는 `scripts/tigerkit_state.py draft-paths --kind handoffs` helper가 계산합니다.

## Process

1. 현재 repo/worktree 기준 handoff 경로를 계산합니다.
2. `current.md`가 있으면 그 파일을 source of truth로 읽습니다.
3. 사용자가 focus를 줬으면 그 범위만 더 짧게 정리합니다.
4. handoff가 없으면 missing path를 숨기지 않고 그대로 말합니다.
5. 필요한 첫 행동을 한 줄로 남깁니다.

## Boundaries

- read-only 입니다.
- handoff를 regenerate, overwrite, append 하지 않습니다.
- chat memory나 추측으로 빠진 section을 보완하지 않습니다.
- 기본은 current repo/worktree handoff 하나만 읽습니다.

## Good use cases

- `/clear` 뒤 직전 handoff 다시 열기
- 다른 agent가 남긴 current handoff 빠르게 복구하기
- 남은 작업 / 리스크 / next step만 짧게 다시 보기
- handoff 파일 path만 확인하기
