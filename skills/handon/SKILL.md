---
name: handon
description: handoff 재개 트리거입니다.
disable-model-invocation: true
---

# Handon

`/tk:handon` wrapper skill입니다. 상세 계약, output contract, helper/path semantics의 source of truth는 `commands/handon.md`입니다.

## Use when

- 현재 repo/worktree의 saved handoff를 다시 열어 맥락을 빠르게 복구해야 할 때
- current handoff artifact를 source of truth로 읽고 싶은 때

## Wrapper rules

- 이 skill은 `commands/handon.md`를 대체하지 않고, command intent를 빠르게 잡는 얇은 wrapper입니다.
- artifact path / apply boundary / helper invocation / receipt shape는 `commands/handon.md`를 그대로 따릅니다.
- command contract에 이미 있는 절차와 경계를 다시 장문으로 복제하지 않습니다.
