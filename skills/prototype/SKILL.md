---
name: prototype
description: throwaway 검증 트리거입니다.
disable-model-invocation: true
---

# Prototype

`/tk:prototype` wrapper skill입니다. 상세 계약, output contract, helper/path semantics의 source of truth는 `commands/prototype.md`입니다.

## Use when

- UI 또는 logic/state 가설을 throwaway prototype으로 빠르게 검증해야 할 때
- 무엇이 fake이고 무엇이 실제 연결인지 분리해서 보고해야 할 때

## Wrapper rules

- 이 skill은 `commands/prototype.md`를 대체하지 않고, command intent를 빠르게 잡는 얇은 wrapper입니다.
- artifact path / apply boundary / helper invocation / receipt shape는 `commands/prototype.md`를 그대로 따릅니다.
- command contract에 이미 있는 절차와 경계를 다시 장문으로 복제하지 않습니다.
