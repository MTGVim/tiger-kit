---
name: help
description: entrypoint navigation 트리거입니다.
disable-model-invocation: true
---

# Help

`/tk:help` wrapper skill입니다. command map과 output contract의 source of truth는 `commands/help.md`입니다.

## Use when

- 어떤 TigerKit command부터 열어야 할지 빠르게 정리해야 할 때
- 정적 map이나 상황형 entrypoint 안내가 필요할 때

## Wrapper rules

- 이 skill은 `commands/help.md`를 대체하지 않는 얇은 wrapper입니다.
- mapping source는 `docs/help-map.json`, workflow 연결 설명은 `docs/workflow-matrix.md`를 그대로 따릅니다.
- navigation만 담당하고 route 결정이나 multi-step orchestration 실행을 대신하지 않습니다.
