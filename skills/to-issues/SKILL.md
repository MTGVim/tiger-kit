---
name: to-issues
description: issue 분해 트리거입니다.
disable-model-invocation: true
---

# To Issues

`/tk:to-issues` wrapper skill입니다. 상세 계약, output contract, helper/path semantics의 source of truth는 `commands/to-issues.md`입니다.

## Use when

- plan/PRD를 independently grabbable vertical-slice issue draft로 쪼개야 할 때
- publish 전에 dependency와 ordering을 먼저 draft로 고정해야 할 때

## Wrapper rules

- 이 skill은 `commands/to-issues.md`를 대체하지 않고, command intent를 빠르게 잡는 얇은 wrapper입니다.
- artifact path / apply boundary / helper invocation / receipt shape는 `commands/to-issues.md`를 그대로 따릅니다.
- command contract에 이미 있는 절차와 경계를 다시 장문으로 복제하지 않습니다.
