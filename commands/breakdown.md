---
description: gap.md나 plan.md를 작은 실행 task 목록으로 분해합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 작업 산출물도 한글로 작성합니다. 단, 인용한 원문, 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

목표: `.tigerkit/{work_id}/gap.md` 또는 `.tigerkit/{work_id}/plan.md`를 읽고, 실행 가능한 작은 task 목록으로 분해해 `.tigerkit/{work_id}/tasks.md`에 정리합니다.

기준 파일이 없거나 어떤 작업을 task로 내려야 하는지 불명확하면 task를 만들지 말고 `/tk:gap` 또는 `/tk:plan`을 먼저 실행하라고 안내합니다.

기본 산출물:
- `.tigerkit/{work_id}/tasks.md`

각 task는 ID, 상태, 목적, 체크리스트, 완료 기준, blocker를 짧게 포함합니다.

상태값은 `todo`, `in_progress`, `blocked`, `done`, `dropped`만 사용합니다.

구현, commit, push, PR 생성은 사용자 승인 없이 실행하지 않습니다.

채팅 응답 마지막에는 `다음 추천: /tk:next`를 표시합니다.
