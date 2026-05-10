---
description: requirements.md 또는 gap.md를 기준으로 구현 묶음, 선행관계, 검증 순서를 짧은 실행계획으로 정리합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 작업 산출물도 한글로 작성합니다. 단, 인용한 원문, 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

목표: `.tigerkit/{work_id}/requirements.md` 또는 `.tigerkit/{work_id}/gap.md`를 기준으로 구현 전에 합의해야 할 실행계획을 작성합니다.

기준 파일이 없거나 어떤 작업을 계획해야 하는지 불명확하면 계획을 만들지 말고 `/tk:prep` 또는 `/tk:gap`로 기준을 먼저 정리하라고 안내합니다.

기본 산출물:
- `.tigerkit/{work_id}/plan.md`

계획에는 Context, Recommended Approach, Task Breakdown, Dependencies, Verification을 포함합니다.

승인 전에는 `.tigerkit/{work_id}/tasks.md`를 만들지 않습니다. 명시적으로 요청받지 않는 한 코드를 구현하지 않습니다.
