---
name: quiz
description: 이해도 게이트 트리거입니다.
disable-model-invocation: true
---

# Quiz

`/tk:quiz` wrapper skill입니다. diff/ledger source, quiz artifact path, receipt shape의 source of truth는 `commands/quiz.md`입니다.

## Use when

- merge 전 현재 diff와 판단 근거를 사람이 실제로 이해했는지 확인해야 할 때
- decision ledger 기반 질문으로 comprehension gate를 걸고 싶을 때

## Wrapper rules

- 이 skill은 `commands/quiz.md`를 대체하지 않는 얇은 wrapper입니다.
- current diff + same worktree ledger를 source of truth로 읽는 경계를 유지합니다.
- publish나 merge 실행 없이 comprehension gate만 수행합니다.
