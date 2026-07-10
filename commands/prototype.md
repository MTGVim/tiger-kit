---
description: throwaway prototype으로 검증합니다.
argument-hint: '"<idea>" [--ui|--logic] [--target <path|area>] [--print-plan]'
---

이 문서는 TigerKit `/tk:prototype` command contract를 정의합니다.

사용자에게는 한글로 답합니다. 코드, path, URL, identifier, command, YAML/JSON field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:prototype`은 UI 또는 logic/state 가설을 production finish 전에 throwaway prototype으로 빠르게 검증하는 surface입니다.

related wrapper skill:

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

- section label은 항상 `🎯 Goal:`처럼 leading emoji를 붙인 `라벨:` 한 줄 뒤 바로 다음 줄에 내용을 둡니다. 라벨 뒤 빈 줄을 두지 않습니다.
- 같은 역할의 label은 가능하면 같은 emoji를 재사용합니다.
- top-level section label에만 emoji를 붙이고, nested bullet label은 plain을 우선합니다.
- compact는 유지하되 section 사이에는 한 줄 여백을 두어 읽힘을 확보합니다.
- 긴 설명은 가능하면 bullet을 쪼개서 한 줄에 한 뜻만 남깁니다.
- optional section은 비어 있으면 통째로 생략합니다. 의미 보존이 필요한 receipt가 아니면 `NONE`을 출력하지 않습니다.

```text
Prototype 준비 | Prototype 완료 | Prototype 중단
🧭 Mode: ui | logic
🎯 Goal:
- <what is being tested>
[📁 Created files:
- <prototype files>]
✅ Confirmed:
- <what the prototype proved>
⚠️ Still fake:
- <what is mocked or assumed>
▶️ Next production step:
- <what to port, delete, or refine>
```

## Non-goals

- production-ready finish claim
- no-op 문서화만 하고 prototype 미생성
- commit/push/merge
