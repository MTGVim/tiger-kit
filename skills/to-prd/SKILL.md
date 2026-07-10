---
name: to-prd
description: PRD 정리 트리거입니다.
---

# To PRD

`/tk:to-prd` wrapper skill입니다. 상세 계약, output contract, helper/path semantics의 source of truth는 `commands/to-prd.md`입니다.

## Use when

- 현재 대화나 요구사항을 draft-only PRD로 정리해야 할 때
- acceptance criteria를 구현 전에 먼저 고정해야 할 때

## Wrapper rules

- 이 skill은 `commands/to-prd.md`를 대체하지 않고, command intent를 빠르게 잡는 얇은 wrapper입니다.
- artifact path / apply boundary / helper invocation / receipt shape는 `commands/to-prd.md`를 그대로 따릅니다.
- command contract에 이미 있는 절차와 경계를 다시 장문으로 복제하지 않습니다.
