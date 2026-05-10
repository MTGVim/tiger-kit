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
| `req-needed` | `requirements.md` 없음 | `/tk:prep` |
| `gap-needed` | `requirements.md` 있음, `gap.md` 없음 | `/tk:gap` |
| `plan-needed` | `gap.md` 있음, `plan.md` 없음 | `/tk:plan` |
| `tasks-needed` | `plan.md` 또는 `gap.md` 있음, `tasks.md` 없음 | `/tk:breakdown` |
| `task-ready` | `tasks.md`에 `in_progress` 또는 `todo` 있음 | 다음 task 1개와 `/tk:do` |
| `blocked` | 실행 가능 task 없고 `blocked`만 있음 | blocker 해결에 필요한 사용자 결정 |
| `re-eval-needed` | task가 모두 `done`/`dropped`이고 gap 재확인 전 | `/tk:gap` |
| `close-ready` | gap 재확인까지 끝났고 새 gap 없음 | `/tk:close` |

## task 선택 규칙

`tasks.md`가 있는 경우:
- `in_progress`가 있으면 그것을 우선 표시합니다.
- `in_progress`가 없으면 첫 번째 `todo`를 표시합니다.
- `blocked`, `done`, `dropped`는 실행 후보에서 제외합니다.

## 출력

짧게 아래만 포함합니다.

- 현재 상태
- 다음 command 또는 다음 task 1개
- 사용한 기준 파일
- blocker가 있으면 blocker
- `다음 추천: ...`

이 명령은 파일을 수정하지 않습니다.
