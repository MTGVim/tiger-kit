---
description: 현재 tasks.md에서 다음에 진행할 task 하나만 고릅니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 인용한 원문, 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

목표: `.tigerkit/{work_id}/tasks.md`를 읽고 지금 진행할 task 하나만 선택합니다.

`tasks.md`가 없으면 task를 새로 만들지 말고 `/tk:breakdown` 또는 `/tk:tasks` 실행을 제안하고 멈춥니다.

선택 규칙:
- `in_progress`가 있으면 그것을 우선 표시합니다.
- `in_progress`가 없으면 첫 번째 `todo`를 표시합니다.
- `blocked`, `done`, `dropped`는 실행 후보에서 제외합니다.

출력은 다음 task, 완료 기준, 확인 파일, 주의점만 포함합니다.

명시적으로 요청받지 않는 한 코드를 구현하지 않습니다.
