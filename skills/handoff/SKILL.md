---
name: handoff
description: handoff 생성 트리거입니다.
---

# Handoff

`/tk:handoff` wrapper skill입니다. 상세 계약, output contract, helper/path semantics의 source of truth는 `commands/handoff.md`입니다.

## Use when

- 다음 세션이나 다른 에이전트가 바로 이어서 움직일 handoff를 남겨야 할 때
- current-first handoff artifact에 goal / state / risks를 정리해야 할 때

## Wrapper rules

- 이 skill은 `commands/handoff.md`를 대체하지 않고, command intent를 빠르게 잡는 얇은 wrapper입니다.
- artifact path / apply boundary / helper invocation / receipt shape는 `commands/handoff.md`를 그대로 따릅니다.
- command contract에 이미 있는 절차와 경계를 다시 장문으로 복제하지 않습니다.
