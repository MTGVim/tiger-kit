---
description: requirements.md와 현재 상태 사이의 요구사항 coverage와 남은 gap을 분석합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 작업 산출물도 한글로 작성합니다. 단, 인용한 원문, 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

목표: `.tigerkit/{work_id}/requirements.md`에 정리된 요구사항 기준을 읽고, 필요한 범위에서 현재 구현, 문서, 테스트, 관찰 가능한 동작을 확인한 뒤 요구사항 coverage와 남은 gap을 정리한 분석 결과를 작성합니다.

작업 기준 파일이 없거나 어떤 작업을 분석해야 하는지 불명확하면 분석을 시작하지 말고 `/tk:prep`로 요구사항 기준과 작업 대상을 먼저 정리하라고 안내합니다.

보고서는 Verdict, Requirement Coverage, Remaining Gaps, API Contract Drift, Unable to Verify, Notes를 포함합니다. 확인 불가 요구사항이 하나라도 있으면 `NO_GAPS_FOUND`로 판정하지 않습니다.

`API Contract Drift`는 항상 Markdown 표로 포함합니다. 확인된 drift가 없더라도 헤더를 유지하고 `없음` 행을 남깁니다. mock 또는 assumed contract 흔적이 있고 실제 API나 공식 contract를 관찰할 수 있으면 contract mismatch와 implementation gap을 구분합니다.

요구사항에 API 의존성이 있는데 현재 repo에서 실제 API나 공식 contract를 확인할 수 없으면 `Unable to Verify`에 외부 API/문서 확인 필요를 남깁니다. 기존 `mock_api_contract` 또는 `TK-API-* blocked`가 있거나 API 부재가 계속 관찰되면, 사용자가 이번 범위 밖이라고 명시하지 않은 한 채팅 응답 끝에서 실제 API나 공식 contract가 준비됐는지 cross-check 질문을 합니다.

기본 산출물:
- `.tigerkit/{work_id}/gap.md`
- `.tigerkit/{work_id}/gap.meta.json`

명시적으로 요청받지 않는 한 이 명령에서는 코드를 구현하거나 새로운 구현 계획을 만들지 않습니다.

채팅 응답 마지막에는 `다음 추천: /tk:plan`을 표시합니다.
