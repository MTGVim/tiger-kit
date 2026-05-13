---
description: .tigerkit/{work_id}/tasks.index.json을 읽고 다음 task 하나만 추천합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 인용한 원문, 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

목표: `.tigerkit/{work_id}/tasks.index.json`과 필요 최소한의 `tasks.md`만 읽고, 지금 할 다음 task 또는 사용자 action 하나만 제안합니다.

## work_id 결정

1. 사용자가 work_id 또는 `.tigerkit/{work_id}/` 경로를 지정했으면 그것을 사용합니다.
2. 현재 대화에서 직전에 사용한 work_id가 명확하면 그것을 사용합니다.
3. `.tigerkit/` 아래 후보가 하나뿐이면 그것을 사용합니다.
4. 후보가 없거나 여러 개면 추측하지 말고 work_id를 물어봅니다.

## read policy

1. `tasks.index.json`을 먼저 읽습니다.
2. 상세 판단이 필요할 때만 `tasks.md`의 active queue, API Follow-ups, Shared Blockers를 읽습니다.
3. `archive/tasks.done.md`는 사용자가 특정 완료 task를 묻는 경우가 아니면 읽지 않습니다.
4. 전체 계획을 다시 만들지 않습니다.

## 선택 규칙

- unresolved Clarification Actions가 있으면 task 실행보다 clarification action을 추천합니다.
- 일반 `in_progress`가 있으면 그것을 우선 표시합니다.
- 일반 `in_progress`가 없으면 첫 번째 일반 `todo`를 표시합니다.
- `blocked`, `done`, `dropped`는 실행 후보에서 제외합니다.
- 실행 가능한 일반 task가 있고 `TK-API-*` unresolved가 남아 있으면 task 구현은 가능하다고 표시하고 close/merge 전 API 확인 필요를 함께 표시합니다.
- 실행 가능한 일반 task가 없고 `TK-API-* todo`가 있으면 API replacement task를 추천합니다.
- 실행 가능한 일반 task가 없고 `TK-API-* blocked`만 남으면 해당 API/contract 확인을 다음 action으로 추천합니다.
- 실행 가능한 task도 blocker도 없으면 `/tk:gap` 또는 `/tk:close`를 추천합니다.

## API follow-up 표시

API 없음은 항상 development blocker가 아닙니다.

```text
mock 가능 = task 진행 가능, close/merge 전 확인 필요
mock 불가 = task blocked
```

## 출력

```text
Next task: T-004 검색 결과 empty state 구현

Status: todo
Requirement: R-002
API Follow-up: TK-API-001 사용자 검색 API contract 불명
Mode: mock_api_contract

판단:
- mock으로 진행 가능
- task 구현은 가능
- close/merge 전 실제 API contract 확인 필요

다음 추천: /tk:do T-004
```

이 명령은 파일을 수정하지 않습니다.
