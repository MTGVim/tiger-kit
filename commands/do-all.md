---
description: tasks.md의 실행 가능한 task를 끝날 때까지 하나씩 구현합니다. 각 task마다 TDD와 inline/sub-agent 방식을 스스로 판단합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 코드, 테스트 이름, 파일 경로, 식별자, 오류 메시지는 원문 그대로 유지할 수 있습니다.

목표: `.tigerkit/{work_id}/tasks.md`에서 실행 가능한 task를 순서대로 처리해 가능한 만큼 완료합니다. 코드 수정이 포함된 task는 각 task 검증 통과 후 local commit으로 남깁니다.

## 처리 대상

- `in_progress` task가 있으면 먼저 처리합니다.
- 그다음 `todo` task를 순서대로 처리합니다.
- `blocked`, `done`, `dropped`는 건너뜁니다.
- dependency나 외부 blocker가 명시된 task는 blocker 완료 전 처리하지 않습니다.
- `Clarification Actions`에 `unresolved` 항목이 있으면 구현 loop를 시작하지 않습니다. 모호함을 terminal blocker로 보지 말고 `/tk:grill-me`, brainstorming, targeted question, assumption 선택을 다음 행동으로 보고합니다.
- 단, `API Follow-up Tasks`의 `TK-API-* blocked`만 남은 경우에는 일반 `todo`/`in_progress` task를 계속 처리합니다. `TK-API-* blocked`는 merge blocker로 보고하되 mock 기준 구현을 막는 일반 blocker로 취급하지 않습니다.

## 처리 방식

각 task는 `/tk:do`와 같은 규칙으로 처리합니다.

각 task 시작 전 스스로 판단합니다.

- TDD 적용 여부
- inline 또는 sub-agent 실행 방식
- 검증 명령 또는 수동 확인 방법

여러 task를 한 번에 묶어 구현하지 않습니다. task 하나를 완료/blocked 처리하고, 코드 수정이 포함됐으면 검증 통과 후 해당 task 변경만 commit한 뒤 다음 task로 넘어갑니다.

### Agent routing

Agent 이름은 짧은 표기를 쓰되, plugin runtime이 `tk:tk-*`로 표시하면 그 namespaced 이름을 사용합니다.

각 task마다 `/tk:do`와 같은 routing을 다시 판단합니다. 독립 task를 서로 묶어 처리하지 않지만, 한 task 내부에서 파일 영역이 독립적이고 충돌 위험이 낮으면 여러 `tk-trog` 또는 조사 agent를 병렬로 쓸 수 있습니다. 이 경우에도 main agent가 diff를 합치고 task 단위 검증과 commit을 수행합니다.

- 탐색/영향 범위: Claude Code 내장 `Explore`
- API/contract 확인: `tk-sif-muna`
- bounded implementation: `tk-trog`
- cleanup/docs hygiene: `tk-elyvilon`
- UI/prototype: `tk-nemelex-xobeh`
- visual artifact 분석: `tk-ashenzari`
- review/risk 판단: `tk-ru`

## 중단 조건

아래 상황이면 즉시 중단하고 보고합니다.

- task 요구사항이 모호해 `Clarification Actions`가 필요함. 이 경우 task를 `blocked`로 만들지 않고 clarification next action을 보고합니다.
- work_id가 불명확함
- 검증 실패가 반복됨
- 외부 blocker가 있음. 단 `TK-API-* blocked`만 있고 mock 기준 일반 task가 남아 있으면 중단하지 않습니다.
- 예상보다 범위가 커져 사용자 결정이 필요함
- main/master/develop 같은 기반 브랜치에서 변경 승인이 필요함

## TDD 기준

TDD는 task별로 판단합니다.

추천:
- behavior/API/business logic/bug fix/regression risk
- public interface로 검증 가능한 변경

생략:
- docs/prompt/manifest/config/copy
- test harness 부재
- 작은 mechanical 변경

TDD 적용 시 한 test → minimal implementation → green → 다음 test 순서만 사용합니다. 모든 test를 먼저 쓰는 horizontal slice는 금지합니다.

## 안전 경계

- 코드 수정 task의 local commit은 task별 검증 통과 후 수행합니다.
- push, PR 생성, branch 생성은 사용자 승인 없이 실행하지 않습니다.
- 검증 실패를 우회하지 않습니다.
- task 범위를 넘어선 대규모 refactor를 하지 않습니다.
- sub-agent가 구현한 경우에도 최종 diff와 검증은 main agent가 확인합니다.

## Tail gap check

실행 가능한 일반 task를 모두 처리했고 unresolved `Clarification Actions`, 외부 blocked task, `Shared Blockers`의 `상태=blocked` 항목이 없다면, 종료 전에 gap을 한 번만 다시 확인합니다.

규칙:
- tail gap check는 최대 1회만 수행합니다.
- `requirements.md`를 기준으로 현재 구현, 문서, 테스트, 관찰 가능한 동작을 다시 비교합니다.
- 새 gap이 있으면 `gap.md`를 갱신하고 멈춥니다. 바로 다시 구현 loop를 돌지 않습니다.
- 새 gap이 없고 unresolved `Clarification Actions`, unresolved `TK-API-*`, `Shared Blockers`의 `상태=blocked` 항목이 없으면 `/tk:close`를 추천합니다.
- unresolved `Clarification Actions`가 남아 있으면 clarification next action을 보고하고 `/tk:close`를 추천하지 않습니다.
- unresolved `TK-API-*`가 남아 있으면 merge blocker와 incomplete 상태를 보고하고 API/contract 확인 요청을 다음 action으로 추천합니다.
- 외부 blocked task나 `Shared Blockers`의 `상태=blocked` 항목이 남아 있거나 검증 실패가 있으면 tail gap check를 하지 않고 blocker를 보고합니다.

## 출력

마지막에는 아래만 짧게 보고합니다.

- 완료 task 수
- 외부 blocked task 수, `Shared Blockers`의 `상태=blocked` 항목 수, unresolved `Clarification Actions` 수
- 각 task의 TDD/실행 방식 요약
- 검증 결과
- 생성한 commit 수와 commit hash
- 남은 task
- tail gap check 결과
- `다음 추천: /tk:plan`, `/tk:close`, 또는 `/tk:next`
