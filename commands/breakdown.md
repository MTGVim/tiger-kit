---
description: gap.md나 plan.md를 작은 실행 task 목록으로 분해합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 작업 산출물도 한글로 작성합니다. 단, 인용한 원문, 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

목표: `.tigerkit/{work_id}/gap.md` 또는 `.tigerkit/{work_id}/plan.md`를 읽고, 실행 가능한 작은 task 목록으로 분해해 `.tigerkit/{work_id}/tasks.md`에 정리합니다.

기준 파일이 없거나 어떤 작업을 task로 내려야 하는지 불명확하면 task를 만들지 말고 `/tk:gap` 또는 `/tk:plan`을 먼저 실행하라고 안내합니다.

기본 산출물:
- `.tigerkit/{work_id}/tasks.md`

각 task는 ID, 상태, 목적, 포함 작업 또는 묶인 gap 요약, 체크리스트, 완료 기준, blocker를 짧게 포함합니다.
포함 작업 요약은 task ID만 보고도 무엇을 해야 하는지 알 수 있게 한 줄로 적습니다.

상태값은 `todo`, `in_progress`, `blocked`, `done`, `dropped`만 사용합니다.

## Shared Blockers와 Clarification Actions

`spec_unclear`나 모호한 요구사항은 terminal `blocked`로 만들지 않습니다. 대신 `Clarification Actions` 섹션에 `TK-CLARIFY-<n>` 항목으로 올리고, `/tk:grill-me`, brainstorming, targeted question, assumption 선택 중 다음 행동을 명시합니다. 이 항목은 실행을 포기하는 blocker가 아니라 모호함을 걷어내는 active next action입니다. 표에는 `ID`, `상태`, `모호점`, `추천 경로`, `영향 task`, `완료 조건`을 포함합니다. 상태는 `unresolved` 또는 `resolved`로 표시하고, `unresolved`가 하나라도 있으면 `clarification-needed`입니다.

`blocked`와 `Shared Blockers`는 외부에서 풀어야 하는 상태에만 사용합니다. 기본 유형은 `api_contract_missing`, `permission_required`, `external_dependency_unavailable`, `human_decision_required`입니다. 같은 외부 blocker를 공유하는 task는 개별 blocked task로 복제하지 말고 `Shared Blockers` 항목 하나에 영향 task를 모읍니다. 표에는 `ID`, `유형`, `상태`, `영향 task`, `해소 조건`, `현재 근거`를 포함합니다. 상태는 `blocked` 또는 `resolved`로 표시합니다.

재실행 시 기존 `tasks.md`가 있으면 진행 상태를 최대한 보존합니다. `done`은 보존하고, `in_progress`는 충돌 여부를 표시하고, `blocked`는 blocker 원인을 재평가하고, 새 계획에서 사라진 task는 `dropped` 또는 `Superseded Tasks`로 기록합니다.

`plan.md`에 `API Readiness`가 있으면 task 분해는 그 표를 기준으로 합니다. `mock_api_contract` feature slice는 일반 구현 task를 `blocked`로 복제하지 않습니다. 대신 `API Follow-up Tasks` 섹션을 별도로 만들고, 같은 API capability는 `TK-API-<n>` 하나로 합쳐 여러 slice가 참조하게 합니다.

`API Follow-up Tasks`는 기존 상태값을 그대로 씁니다. 실제 API나 공식 contract가 없으면 `TK-API-*`는 `blocked`, 준비되면 `todo`, 교체 완료 시 `done`입니다. 표에는 `ID`, `상태`, `API Capability`, `Affected Slices`, `완료 기준`을 포함합니다.

`mock_api_contract` task의 완료 기준에는 아래를 포함합니다.
- assumed contract와 mock API 경계가 명시됨
- feature 전용 mock은 feature task에 포함하고, 여러 slice가 공유하는 mock은 shared mock setup task로 분리함
- mock boundary 파일에는 기본 `FIXME(TK-API-<n>)` marker를 남김. 저장소 규칙상 `FIXME`가 금지되면 `TODO(TK-API-<n>)`로 낮춤
- mock API 기준으로 golden path, loading, error를 검증함. empty state는 list/search/nullable data slice일 때 검증함
- unresolved `TK-API-*`는 merge blocker로 남김

구현, commit, push, PR 생성은 사용자 승인 없이 실행하지 않습니다.

채팅 응답 마지막에는 `다음 추천: /tk:next`를 표시합니다.
