---
description: 사용자가 운전대를 잡고 step by step으로 지시하는 user-steered execution mode를 시작합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

목표: 사용자가 구현 방향과 교정을 직접 주도하고 agent는 그 지시를 따라 실행합니다. `/tk:steer`는 `do`의 후처리 전용이 아니라 독립 user-steered execution command입니다.

## 의미

- `do` = autopilot
- `steer` = direct drive

사용자가 방향을 정합니다. agent는 아래를 수행합니다.

- 지시된 step 실행
- 재사용 강제 반영
- 왜 새로 만들었는지 설명
- 필요한 경우에만 질문
- correction, reuse rule, ask-rule을 decisions에 기록

## 시작 조건

- `do`가 선행되지 않아도 됩니다.
- task ledger가 이미 있으면 그 task 문맥을 우선 사용합니다.
- task ledger가 없어도 대상 파일/화면/컴포넌트가 명확하면 시작할 수 있습니다.
- work_id나 대상이 너무 모호하면 짧게 물어봅니다.

## 동작 원칙

- 사용자가 지시한 step을 창의적으로 재해석하지 않습니다.
- scope를 넓히지 않습니다.
- 기존 구현, component, hook, util 재사용 여부를 먼저 확인합니다.
- 새 UI, 새 flow, 새 abstraction은 재사용 검토 뒤에만 만듭니다.
- copy, product, design, API intent를 silent change하지 않습니다.
- destructive action, shared contract 변경, ambiguity가 큰 adapter/extraction 판단은 멈추고 묻습니다.

## ask 규칙

왜 묻기 좋은 경우:
- 기존 패턴과 다른 선택
- 다음에도 재사용 가능한 기준
- trade-off가 숨어 있는 선택
- agent 기본 성향과 충돌하는 선택

왜 안 묻기 좋은 경우:
- 단순 file navigation
- 이번 task 한정 사소한 선택
- 흐름만 끊는 질문

## state / decisions

`/tk:steer`는 아래를 local state에 반영할 수 있습니다.

- `.tigerkit/{work_id}/steer-state.json`
- `.tigerkit/{work_id}/decisions.md`

`decisions.md`에는 아래를 compact하게 남깁니다.

- explicit user directions
- observed decision heuristics
- reused implementation references
- corrected agent choices
- reflect candidate가 될 수 있는 규칙

## reflect

`steer`는 reflect 후보를 만들 수 있지만 reflect 승격을 강제하지 않습니다.

- session-only learning
- work-level convention
- durable reflect candidate

이 셋을 분리합니다. durable write는 사용자 승인 없이 하지 않습니다.

## 출력

```text
steer 시작했습니다.
- mode: direct drive
- state: `.tigerkit/search/steer-state.json`
- decisions: `.tigerkit/search/decisions.md`
- rule: user directs, agent executes

다음: step을 지시해주세요.
```

## 금지

- autonomy mode처럼 행동
- blank interview 시작
- 장문 retrospective 바로 생성
- 사용자 승인 없는 durable reflect mutation