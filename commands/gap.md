---
description: requirements.md와 현재 상태 사이의 요구사항 coverage와 남은 gap을 분석합니다.
---

TigerKit의 `gap` 스킬을 사용합니다.

사용자에게는 한글로 답합니다. 작업 산출물도 한글로 작성합니다. 단, 인용한 원문, 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

목표: `.tigerkit/{work_id}/requirements.md`에 정리된 요구사항 기준을 읽고, 필요한 범위에서 현재 구현, 문서, 테스트, 관찰 가능한 동작을 확인한 뒤 `.tigerkit/{work_id}/gap.md`를 작성합니다.

작업 기준 파일이 없거나 어떤 작업을 분석해야 하는지 불명확하면 분석을 시작하지 말고 `/tk:req`로 요구사항 기준을 먼저 정리하라고 안내합니다.

보고서는 Verdict, Requirement Coverage, Remaining Gaps, Unable to Verify, Notes를 포함합니다. 확인 불가 요구사항이 하나라도 있으면 `NO_GAPS_FOUND`로 판정하지 않습니다.

명시적으로 요청받지 않는 한 이 명령에서는 코드를 구현하거나 구현 계획을 새로 만들지 않습니다.
