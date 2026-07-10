---
name: arch-review
description: 구조 리뷰 트리거입니다.
---

# Arch Review

`/tk:arch-review` wrapper skill입니다. 상세 계약, output contract, helper/path semantics의 source of truth는 `commands/arch-review.md`입니다.

## Use when

- boundary, ownership, coupling, 반복 마찰을 evidence-first로 검토해야 할 때
- 자동 리팩터링이 아니라 report-only 구조 판단이 먼저일 때

## Wrapper rules

- 이 skill은 `commands/arch-review.md`를 대체하지 않고, command intent를 빠르게 잡는 얇은 wrapper입니다.
- artifact path / apply boundary / helper invocation / receipt shape는 `commands/arch-review.md`를 그대로 따릅니다.
- command contract에 이미 있는 절차와 경계를 다시 장문으로 복제하지 않습니다.
