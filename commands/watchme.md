---
description: teach-by-demonstration WatchMe mode를 시작합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

목표: 사용자가 step by step으로 판단 흐름을 보여주면 agent가 closely follow 하면서 무엇을 먼저 확인하는지, 무엇을 재사용하는지, 어디서 scope를 자르는지, 언제 ask가 필요한지 관찰하는 WatchMe mode를 시작합니다.

## 의미

WatchMe mode는 autonomy mode가 아닙니다. teach-by-demonstration mode입니다.

사용자가 주도합니다. agent는 아래를 관찰합니다.

- 사용자가 먼저 확인하는 정보
- 참고하는 기존 구현
- 재사용을 기대하는 component, hook, util, pattern
- 바꾸지 말아야 할 것
- scope를 자르는 지점
- agent의 원래 판단과 달랐을 지점
- 더 이른 context scan이 있었으면 막을 수 있었던 miss

## 시작 동작

1. WatchMe mode를 active로 표시합니다.
2. local runtime state를 `.tigerkit/watchme-state.json` 또는 work_id가 분명하면 `.tigerkit/{work_id}/watchme-state.json`에 기록합니다.
3. compact indicator를 보여줍니다.

권장 indicator:

```text
watching… 👀
```

mode가 active인 동안 후속 응답 상단 근처에 아래 indicator를 한 번 짧게 보여줄 수 있습니다.

```text
still watching… 👀
```

indicator는 상태 표시일 뿐이며 substantive update를 대체하지 않습니다.

## local state

state는 `.git` 안에 저장하지 않습니다. local runtime state이며 ledger나 durable lesson store가 아닙니다.

권장 shape:

```json
{
  "mode": "watchme",
  "active": true,
  "work_id": "...",
  "started_at": "...",
  "indicator": "still watching… 👀"
}
```

## 동작 원칙

- step by step instruction을 창의적으로 재해석하지 않습니다.
- scope를 넓히지 않습니다.
- unclear requirement를 추측하지 않습니다.
- reuse candidate 확인 없이 새 UI, 새 component, 새 flow를 만들지 않습니다.
- copy, product, design, API intent를 silent change하지 않습니다.
- destructive action, shared contract 변경, ambiguous adapter/extraction decision은 멈추고 묻습니다.

## ask/stop rules

아래 경우에는 WatchMe mode여도 멈추거나 묻습니다.

- requirement 충돌
- user intent의 material ambiguity
- product, design, API, copy meaning 불명확
- destructive change 가능성
- shared component behavior 또는 public contract 변경
- existing reusable implementation은 있는데 adapter/extraction 전략이 불명확
- user instruction 범위를 넘는 구현 필요

## 출력

receipt-first로 짧게 보고합니다.

```text
watching… 👀
- mode: active
- state: `.tigerkit/watchme-state.json`
- learning target: user decision style

다음: step을 보여주세요.
```

## 금지

- durable knowledge 자동 반영
- branch-local note를 user-level learning처럼 과장
- retrospective 없이 mode 종료
- `.git` 내부 state 저장
- 이 mode를 자율 구현 모드처럼 취급