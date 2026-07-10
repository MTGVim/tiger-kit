---
name: route
description: route 판단 트리거입니다.
---

# Route

`/tk:route` wrapper skill입니다. 상세 계약, output contract, helper/path semantics의 source of truth는 `commands/route.md`입니다.

## Use when

- direct / subagent-driven / goal-driven / decision / need-sot 중 어디로 갈지 정해야 할 때
- 구현보다 먼저 역할 분리, SoT, ownership을 얇게 판단해야 할 때
- same repo/scope `gap packet`이 있으면 그것을 재사용해 route 판단을 이어가야 할 때

## Wrapper rules

- 이 skill은 `commands/route.md`를 대체하지 않고, command intent를 빠르게 잡는 얇은 wrapper입니다.
- artifact path / apply boundary / helper invocation / receipt shape는 `commands/route.md`를 그대로 따릅니다.
- command contract에 이미 있는 절차와 경계를 다시 장문으로 복제하지 않습니다.
