---
description: .tigerkit/{work_id} 상태를 보고 지금 해야 할 다음 command 또는 다음 task를 하나 추천합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 인용한 원문, 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

목표: `.tigerkit/{work_id}/`의 현재 상태를 확인하고, 지금 진행해야 할 다음 command 또는 다음 task 하나만 추천합니다.

## work_id 결정

1. 사용자가 work_id 또는 `.tigerkit/{work_id}/` 경로를 지정했으면 그것을 사용합니다.
2. 현재 대화에서 직전에 사용한 work_id가 명확하면 그것을 사용합니다.
3. `.tigerkit/` 아래 후보가 하나뿐이면 그것을 사용합니다.
4. 후보가 없거나 여러 개라 불명확하면 추측하지 말고 work_id를 물어봅니다.

## 상태별 추천 규칙

| 상태 | 근거 | 추천 |
|---|---|---|
| `req-needed` | `requirements.md` 없음 | source 문서나 메모가 있으면 `/tk:prep`, 아이디어가 흐릿하면 `/tk:interview`; 불명확하면 어느 쪽인지 질문 |
| `gap-needed` | `requirements.md` 있음, `gap.md` 없음 | `/tk:gap` |
| `plan-needed` | `gap.md` 있음, `plan.md` 없음 | `/tk:plan` |
| `tasks-needed` | `plan.md` 또는 `gap.md` 있음, `tasks.md` 없음 | `/tk:breakdown` |
| `clarification-needed` | `Clarification Actions`에 unresolved 항목 있음 | `/tk:grill-me`, brainstorming, targeted question, assumption 선택 중 하나 |
| `task-ready` | `tasks.md`에 `in_progress` 또는 `todo` 있음 | 다음 task 1개와 `/tk:do` |
| `blocked` | 실행 가능 task 없고 외부 `blocked` 또는 `Shared Blockers`의 `상태=blocked` 항목만 있음 | blocker 해결에 필요한 사용자 결정 또는 접근 확보 |
| `re-eval-needed` | task가 모두 `done`/`dropped`이고 gap 재확인 전 | `/tk:gap` |
| `close-ready` | gap 재확인까지 끝났고 새 gap, unresolved `Clarification Actions`, unresolved `TK-API-*`, `Shared Blockers`의 `상태=blocked` 항목 없음 | `/tk:close` |

## task 선택 규칙

`tasks.index.json`이 있으면 먼저 compact 상태와 다음 후보를 확인합니다. 상세 판단이 필요할 때만 `tasks.md`의 active queue를 읽습니다. `archive/tasks.done.md`는 사용자가 특정 완료 task를 묻는 경우가 아니면 읽지 않습니다.

`tasks.md`가 있는 경우:
- unresolved `Clarification Actions`가 있으면 모호함을 `blocked`로 보고하지 말고 clarification action과 추천 경로(`/tk:grill-me`, targeted question, brainstorming, assumption 선택)를 먼저 표시합니다.
- 일반 `in_progress`가 있으면 그것을 우선 표시합니다.
- 일반 `in_progress`가 없으면 첫 번째 일반 `todo`를 표시합니다.
- `blocked`, `done`, `dropped`는 실행 후보에서 제외합니다.
- 실행 가능한 일반 task가 있고 `API Follow-up Tasks`에 `TK-API-* blocked`가 남아 있으면 일반 task를 추천하되 merge 전 API/contract 확인 필요를 주의로 함께 표시합니다.
- 실행 가능한 일반 task가 없고 `API Follow-up Tasks`에 `TK-API-* todo`가 있으면 그 replacement task와 `/tk:do`를 추천합니다.
- 실행 가능한 일반 task가 없고 `TK-API-* blocked`만 남아 있으면 기다림이 아니라 해당 API/contract 확인 요청을 다음 action으로 추천합니다.

## 출력

짧게 아래만 포함합니다.

- 현재 상태
- 다음 command 또는 다음 task 1개
- task를 보여줄 때는 task ID만 적지 말고, 그 task에 묶인 gap 또는 포함 작업을 한 줄로 함께 적습니다.
- 가능하면 `포함 작업` 또는 유사한 칼럼명을 사용합니다.
- 사용한 기준 파일
- blocker가 있으면 blocker
- `다음 추천: ...`

이 명령은 파일을 수정하지 않습니다.
