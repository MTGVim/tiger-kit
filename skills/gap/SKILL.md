---
name: gap
description: SoT gap 분석 트리거입니다.
disable-model-invocation: true
---

# Gap

`/tk:gap` wrapper skill입니다. 상세 계약, output contract, helper/path semantics의 source of truth는 `commands/gap.md`입니다.

## Use when

- SoT와 current implementation 차이를 한 번 evidence-first로 비교해야 할 때
- missing / mismatch / overbuilt / ambiguous를 구현 전에 분리하고 싶을 때

## Wrapper rules

- 이 skill은 `commands/gap.md`를 대체하지 않고, command intent를 빠르게 잡는 얇은 wrapper입니다.
- artifact path / apply boundary / helper invocation / receipt shape는 `commands/gap.md`를 그대로 따릅니다.
- command contract에 이미 있는 절차와 경계를 다시 장문으로 복제하지 않습니다.
