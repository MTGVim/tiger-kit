---
name: grill
description: 압박 검증 트리거입니다.
disable-model-invocation: true
---

# Grill

`/tk:grill` wrapper skill입니다. 상세 계약, output contract, helper/path semantics의 source of truth는 `commands/grill.md`입니다.

## Use when

- 계획, 설계, RFC를 바로 구현으로 밀기 전에 한 번 압박 검증해야 할 때
- 질문은 유지하되, 사용자가 모른다고 말했을 때만 후보를 좁혀야 할 때

## Wrapper rules

- 이 skill은 `commands/grill.md`를 대체하지 않고, command intent를 빠르게 잡는 얇은 wrapper입니다.
- artifact path / apply boundary / helper invocation / receipt shape는 `commands/grill.md`를 그대로 따릅니다.
- command contract에 이미 있는 절차와 경계를 다시 장문으로 복제하지 않습니다.
