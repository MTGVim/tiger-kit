---
description: .tigerkit/{work_id}/tasks.md를 만들거나 업데이트해 작업 상태를 관리합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 작업 산출물도 한글로 작성합니다. 단, 인용한 원문, 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

목표: `.tigerkit/{work_id}/tasks.md`를 기준으로 작업 목록, 현재 상태, blocked 항목, 다음 후보를 짧게 정리하거나 업데이트합니다.

`tasks.md`가 없고 분해할 기준 문서도 없다면 임의로 만들지 말고 `/tk:breakdown` 또는 `/tk:prep`/`/tk:gap`을 먼저 실행하라고 안내합니다.

기본 산출물:
- `.tigerkit/{work_id}/tasks.md`

상태값은 `todo`, `in_progress`, `blocked`, `done`, `dropped`만 사용합니다.

채팅 응답은 현재 task, 완료 수, blocked 수, 다음 후보 1개만 짧게 표시합니다.

명시적으로 요청받지 않는 한 코드를 구현하지 않습니다.
