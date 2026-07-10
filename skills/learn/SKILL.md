---
name: learn
description: skill 작성 트리거입니다.
disable-model-invocation: true
---

# Learn

`/tk:learn` wrapper skill입니다. 상세 계약, output contract, helper/path semantics의 source of truth는 `commands/learn.md`입니다.

## Use when

- path / URL / 현재 대화 / reflect candidate에서 reusable skill을 만들고 싶을 때
- preview/apply/name confirmation을 분리한 skill-only write가 필요할 때
- reflect candidate와 그 ledger를 source of truth로 읽어야 할 때

## Wrapper rules

- 이 skill은 `commands/learn.md`를 대체하지 않고, command intent를 빠르게 잡는 얇은 wrapper입니다.
- artifact path / apply boundary / helper invocation / receipt shape는 `commands/learn.md`를 그대로 따릅니다.
- command contract에 이미 있는 절차와 경계를 다시 장문으로 복제하지 않습니다.
