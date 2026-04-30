---
description: 외부 요구사항 소스를 정제해 이후 계획과 갭 확인의 기준이 되는 requirements.md로 정리합니다.
---

TigerKit의 `prep` 스킬을 사용합니다.

사용자에게는 한글로 답합니다. 작업 산출물도 한글로 작성합니다. 단, 인용한 원문, 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

목표: Jira 티켓, Confluence 문서, PRD, 사용자 메모, 회의 요약, 기존 요구사항 문서 같은 source of truth 후보를 중복 제거, 충돌/모호점 표시, acceptance signal, scope boundary 중심으로 정규화해 `.tigerkit/{work_id}/requirements.md`에 저장합니다.

먼저 앞선 대화에서 추론한 스펙명 또는 작업 ID를 제안하고, 그 이름으로 `.tigerkit/{work_id}/`에 정리해도 되는지 확인합니다.

명시적으로 요청받지 않는 한 이 명령에서는 구현 계획을 확정하거나 코드를 수정하지 않습니다.
