---
name: reflect
description: reflect 분류 트리거입니다.
disable-model-invocation: true
---

# Reflect

`/tk:reflect` wrapper skill입니다. 상세 계약, output contract, helper/path semantics의 source of truth는 `commands/reflect.md`입니다.

## Use when

- 세션 결과와 사용자 피드백에서 reusable learning을 durable target으로 분류해야 할 때
- repo-local / user-global / skill / hook / command / agent / discard 경계를 먼저 정해야 할 때
- `/tk:learn`으로 넘길 same session/ledger candidate를 정리해야 할 때

## Wrapper rules

- 이 skill은 `commands/reflect.md`를 대체하지 않고, command intent를 빠르게 잡는 얇은 wrapper입니다.
- artifact path / apply boundary / helper invocation / receipt shape는 `commands/reflect.md`를 그대로 따릅니다.
- command contract에 이미 있는 절차와 경계를 다시 장문으로 복제하지 않습니다.
