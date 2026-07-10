---
name: grooming
description: guidance 감사 트리거입니다.
disable-model-invocation: true
---

# Grooming

`/tk:grooming` wrapper skill입니다. 상세 계약, output contract, helper/path semantics의 source of truth는 `commands/grooming.md`입니다.

## Use when

- guidance drift를 report-first로 평가하고 싶을 때
- user-global만 direct apply하고 repo 쪽은 suggestion-only로 남겨야 할 때

## Wrapper rules

- 이 skill은 `commands/grooming.md`를 대체하지 않고, command intent를 빠르게 잡는 얇은 wrapper입니다.
- artifact path / apply boundary / helper invocation / receipt shape는 `commands/grooming.md`를 그대로 따릅니다.
- command contract에 이미 있는 절차와 경계를 다시 장문으로 복제하지 않습니다.
