---
name: next
description: 다음 command 추천 트리거입니다.
disable-model-invocation: true
---

# Next

`/tk:next` wrapper skill입니다. 정확한 heuristic, stop gate, helper semantics의 source of truth는 `commands/next.md`입니다.

## Use when

- 지금 다음으로 어떤 TigerKit command를 1개만 열지 정해야 할 때
- current artifact 상태를 보고 resume entrypoint를 골라야 할 때

## Wrapper rules

- 이 skill은 `commands/next.md`를 대체하지 않는 얇은 wrapper입니다.
- `docs/help-map.json`과 `usage-summary` helper를 읽는 conductor semantics를 그대로 따릅니다.
- command 2개 이상을 연쇄 호출하지 않는 stop gate를 유지합니다.
