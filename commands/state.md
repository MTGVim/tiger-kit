---
description: .tigerkit/{work_id} 전체 상태를 요약해 현재 단계, 산출물, task 현황, blocker를 보여줍니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 인용한 원문, 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

목표: `.tigerkit/{work_id}/`의 현재 상태를 요약해 지금 어디까지 왔는지, 어떤 산출물이 있는지, task와 blocker가 어떤지, 다음에 무엇을 하면 좋은지 한 번에 보여줍니다.

## work_id 결정

1. 사용자가 work_id 또는 `.tigerkit/{work_id}/` 경로를 지정했으면 그것을 사용합니다.
2. 현재 대화에서 직전에 사용한 work_id가 명확하면 그것을 사용합니다.
3. `.tigerkit/` 아래 후보가 하나뿐이면 그것을 사용합니다.
4. 후보가 없거나 여러 개라 불명확하면 추측하지 말고 work_id를 물어봅니다.

## read policy

`tasks.index.json`이 있으면 task 상태 요약은 index를 우선 사용합니다. `tasks.md`는 active queue와 blocker 세부 확인에만 읽고, `archive/tasks.done.md`는 완료 task 상세를 사용자가 요청했거나 review/close 근거가 필요할 때만 읽습니다.

## 반드시 확인할 것

- `requirements.md` 존재 여부
- `gap.md` 존재 여부
- `plan.md` 존재 여부
- `tasks.md` 존재 여부
- task 상태 요약 (`todo`, `in_progress`, 외부 `blocked`, `done`, `dropped`)
- `Clarification Actions`가 있으면 unresolved `TK-CLARIFY-*` 요약과 추천 clarification 경로
- `Shared Blockers`가 있으면 `상태=blocked` 항목 기준으로 외부 blocker 유형, 영향 task, 해소 조건 요약
- `API 준비도` 또는 기존 `API Readiness`와 `API Follow-up Tasks`가 있으면 unresolved `TK-API-*` 요약
- blocker 존재 여부. 모호함은 blocker가 아니라 clarification-needed로 표시합니다.
- 마지막으로 추천할 다음 명령 1개

## 출력

기본 출력은 `TigerKit State`입니다.

짧게 아래만 포함합니다.

- work_id
- 현재 단계
- 산출물 존재 여부
- task 요약
- task를 표나 목록으로 보여줄 때는 task ID만 적지 말고, 각 task에 묶인 gap 또는 포함 작업을 한 줄로 함께 적습니다.
- 가능하면 `포함 작업` 또는 유사한 칼럼명을 사용합니다.
- clarification action과 외부 blocker 요약
- `다음 추천: ...`

이 명령은 파일을 수정하지 않습니다.
