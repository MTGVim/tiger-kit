---
description: task ledger 상태를 보고, 새 task를 추가하고, 상태를 갱신하는 main entrypoint입니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

목표: `/tk:task`는 TigerKit task ledger의 main entrypoint입니다. bare 호출은 상태 요약과 사용법 가이드, 세부 호출은 task 조회/추가/상태 갱신/상위 status snapshot을 담당합니다.

## bare 호출

인자가 없으면 아래를 짧게 보여줍니다.

- 현재 work_id
- active tasks 요약
- in_progress / blocked / review_required / done count
- pending reflect candidate count
- 가능한 하위 사용법

## 지원 형태

```text
/tk:task
/tk:task list
/tk:task status
/tk:task T-003
/tk:task add
/tk:task T-003 in_progress
/tk:task T-003 blocked auth contract unclear
/tk:task T-003 review_required
/tk:task T-003 done
```

## `list`

- active task 목록을 compact하게 보여줍니다.
- 기본은 active queue만 보여줍니다.
- archive 상세 dump는 하지 않습니다.

## `<task-id>`

- 해당 task의 status, summary, requirement, API follow-up, done criteria를 보여줍니다.
- 필요할 때만 관련 blocker나 decisions 포인터를 보여줍니다.

## `add`

- 새 task를 ledger에 추가합니다.
- 최소 항목:
  - summary
  - source requirement 또는 rationale
  - done criteria
- 자동으로 issue draft를 만들지 않습니다.
- task 추가는 `tasks.md`와 `tasks.index.json`을 함께 갱신합니다.

## 상태 변경

지원 상태:
- `todo`
- `in_progress`
- `blocked`
- `review_required`
- `done`
- `dropped`

원칙:
- `blocked`는 blocked reason을 남깁니다.
- `review_required`는 사람 판단이 남아 있을 때 사용합니다.
- `done`은 unresolved human review가 없을 때만 사용합니다.

## `status`

`/tk:task status`는 old `close/state/handoff` 역할을 흡수합니다.

보여줄 것:
- active task summary
- review_required / blocked
- unresolved API follow-ups
- merge-ready 여부
- next action 1개
- decisions/reflect badge 상태

하지 않는 일:
- 별도 `handoff.md` 필수 생성
- 장문 retrospective 생성
- deep audit 수행

`/tk:task status`는 snapshot이고, 깊은 감사는 `/tk:gap`가 담당합니다.

## decisions / indicator 연계

`tasks.index.json`과 `decisions.md`를 함께 읽어 아래 상태를 요약할 수 있습니다.

- `[🛞]` steer active 또는 steer context 존재
- `[🪞 2]` reflect candidate 2개 pending
- `[🛞 / 🪞 2]` 둘 다

기본은 trailing 표시이며, `/tk:statusline`으로 delivery mode를 바꿀 수 있습니다.

## 출력 예시

### bare

```text
task ledger 확인했습니다.
- work_id: search-ui
- active: 3, blocked: 1, review_required: 1
- reflect pending: 2

다음 추천: /tk:task list
```

### status

```text
상태 정리했습니다.
- active: 3, review_required: 1, blocked: 1
- API: TK-API-001 unresolved, merge blocker
- merge-ready: NO

다음 추천: /tk:next
```

## 금지

- 전체 `tasks.md` dump
- 자동 issue draft 생성
- deep audit 대신하기
- 사용자 승인 없는 commit, push, PR 생성, merge, deploy