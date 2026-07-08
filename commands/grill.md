---
description: 계획, 설계, RFC, 개선안을 수렴형 질문으로 압박 검증합니다.
argument-hint: '"<plan|RFC|idea>" [--target <path|area>] [--print-checklist]'
---

이 문서는 TigerKit `/tk:grill` command contract를 정의합니다.

사용자에게는 한글로 답합니다. 코드, path, URL, identifier, command, YAML/JSON field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:grill`은 계획, 설계, RFC, 개선안을 바로 구현으로 밀지 않고 수렴형 질문으로 압박 검증하는 surface입니다.

canonical skill:

```text
skills/grill/SKILL.md
```

## Core boundary

- preview-only
- source 수정 금지
- 자동 문서 수정 금지
- hard cap 5문항 금지
- 코드베이스에서 확인 가능한 것은 직접 확인
- 이미 답한 내용 재질문 금지
- 사용자가 `멈춰`, `그만`, `가정하고 가`, `그냥 진행`이라고 하면 즉시 중단

## Process contract

1. 관련 repo evidence를 먼저 읽습니다.
2. 직접 확인으로 풀 수 없는 전제만 질문합니다.
3. 질문은 한 번에 하나씩 던집니다.
4. 5회 이상 길어지면 hint를 노출하고 진행 방식을 제안합니다.
5. 종료 시 아래 세 묶음을 요약합니다.
   - 결정사항
   - 가정
   - 남은 리스크

## Output contract

- section label은 항상 `라벨:` 한 줄 뒤 바로 다음 줄에 내용을 둡니다. 라벨 뒤 빈 줄을 두지 않습니다.
- optional section은 비어 있으면 통째로 생략합니다. 의미 보존이 필요한 receipt가 아니면 `NONE`을 출력하지 않습니다.

```text
Grill 진행중 | Grill 중단 | Grill 요약
Question:
- <one sharp question>
Why:
- <why this matters>
Confirmed facts:
- <confirmed facts>
Decision summary:
- <decisions>
Assumptions:
- <assumptions>
Risks:
- <remaining risks>
Next step:
- <continue questioning | proceed with assumptions | stop>
```

## Non-goals

- interview for its own sake
- source write
- approval을 가장한 강압적 endless questioning
- 이미 코드베이스에서 확인 가능한 사실 재질문
