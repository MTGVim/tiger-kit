---
description: requirements.md 또는 gap.md를 기준으로 구현 묶음, 선행관계, 검증 순서를 짧은 실행계획으로 정리합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 작업 산출물도 한글로 작성합니다. 단, 인용한 원문, 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

목표: `.tigerkit/{work_id}/requirements.md` 또는 `.tigerkit/{work_id}/gap.md`를 기준으로 구현 전에 합의해야 할 실행계획을 작성합니다.

기준 파일이 없거나 어떤 작업을 계획해야 하는지 불명확하면 계획을 만들지 말고 `/tk:prep` 또는 `/tk:gap`로 기준을 먼저 정리하라고 안내합니다.

기본 산출물:
- `.tigerkit/{work_id}/plan.md`

계획에는 Revision Notes, Context, Recommended Approach, API Readiness, Task Breakdown, Dependencies, Verification을 포함합니다.

`plan.md`는 항상 canonical 최신 계획입니다. 재실행 시 `plan.v2.md` 같은 버전 파일을 만들지 말고, 기존 `plan.md`, `gap.md`, `tasks.md`에서 유지/폐기/새로 배운 것/API readiness 변경을 읽어 상단 `Revision Notes`에 짧게 기록한 뒤 새 `plan.md`로 갱신합니다.

`API Readiness`는 work_id 전체가 아니라 feature slice 단위 표로 작성합니다. 열은 `Feature Slice`, `Required API`, `Readiness`, `근거`, `Action`을 기본으로 합니다. `Readiness` 값은 아래만 사용합니다.

- `ready`: 실제 API 또는 공식 contract가 확인되어 정상 진행 가능
- `mock_api_contract`: 실제 API와 공식 contract를 확인할 수 없어 assumed contract와 mock API로 진행
- `blocked`: mock으로도 진행하지 않기로 결정했거나 이번 범위 밖인 API 의존성

`gap.md`에서 API 확인 불가가 남았고 사용자가 이번 범위 밖이라고 명시하지 않았다면, `/tk:plan`은 멈추지 않고 기본값으로 `mock_api_contract`를 선택합니다. 이때 assumed contract, mock/MSW 같은 검증 경계, 실제 API 확인 후 교체할 `TK-API-*` follow-up 필요성을 계획에 명시합니다. `mock_api_contract`는 개발 진행 가능 상태이지만 완료나 merge-ready 상태가 아닙니다.

승인 전에는 `.tigerkit/{work_id}/tasks.md`를 만들지 않습니다. 명시적으로 요청받지 않는 한 코드를 구현하지 않습니다.

채팅 응답 마지막에는 `다음 추천: /tk:breakdown`을 표시합니다.
