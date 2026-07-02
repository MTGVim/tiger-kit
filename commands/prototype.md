---
description: UI 또는 logic/state 질문에 대해 throwaway prototype을 빠르게 만들어 검증합니다.
argument-hint: '"<idea>" [--ui|--logic] [--target <path|area>] [--print-plan]'
---

이 문서는 TigerKit `/tk:prototype` command contract를 정의합니다.

사용자에게는 한글로 답합니다. 코드, path, URL, identifier, command, YAML/JSON field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:prototype`은 UI 또는 logic/state 가설을 production finish 전에 throwaway prototype으로 빠르게 검증하는 surface입니다.

canonical skill:

```text
skills/prototype/SKILL.md
```

## Core boundary

- 기본 mode는 no-commit
- prototype은 throwaway 전제를 명시
- production 추상화/에러처리/범용화 과투자 금지
- prototype 성공을 merge-ready로 보고하지 않음
- fake와 real 연결을 구분해 보고

## Mode contract

- `--ui`: layout, interaction, visual flow 검증
- `--logic`: state, reducer, parser, branching, adapter shape 검증
- mode를 명시하지 않으면 질문 의도상 더 가까운 쪽을 고르고 이유를 짧게 밝힘

## Output contract

```text
Prototype 준비 | Prototype 완료 | Prototype 중단
Mode: ui | logic
Goal:
- <what is being tested>
Created:
- <prototype files or NONE>
Confirmed:
- <what the prototype proved>
Still fake:
- <what is mocked or assumed>
Next production step:
- <what to port, delete, or refine>
```

## Non-goals

- production-ready finish claim
- no-op 문서화만 하고 prototype 미생성
- commit/push/merge
