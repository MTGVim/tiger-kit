---
name: merge-conflict
description: 충돌 해결 트리거입니다.
disable-model-invocation: true
---

# Merge Conflict

`/tk:merge-conflict` wrapper skill입니다. 상세 계약, output contract, helper/path semantics의 source of truth는 `commands/merge-conflict.md`입니다.

## Use when

- merge/rebase conflict를 ours/theirs intent 기준으로 정리해야 할 때
- 단순 문자열 선택이 아니라 conflict-specific 검증까지 보고해야 할 때

## Wrapper rules

- 이 skill은 `commands/merge-conflict.md`를 대체하지 않고, command intent를 빠르게 잡는 얇은 wrapper입니다.
- artifact path / apply boundary / helper invocation / receipt shape는 `commands/merge-conflict.md`를 그대로 따릅니다.
- command contract에 이미 있는 절차와 경계를 다시 장문으로 복제하지 않습니다.
