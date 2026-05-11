---
description: tasks.md의 task 하나를 구현합니다. 규모와 성격에 따라 TDD 적용 여부와 inline/sub-agent 실행 방식을 스스로 판단합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 코드, 테스트 이름, 파일 경로, 식별자, 오류 메시지는 원문 그대로 유지할 수 있습니다.

목표: `.tigerkit/{work_id}/tasks.md`의 task 하나를 골라 실제 구현, 검증, 상태 갱신까지 진행합니다. 코드 수정이 포함된 task는 검증 통과 후 관련 변경을 local commit으로 남깁니다.

## task 선택

1. 사용자가 task ID를 지정했으면 그 task를 선택합니다.
2. 지정이 없으면 `in_progress` task를 우선합니다.
3. `in_progress`가 없으면 첫 번째 `todo` task를 선택합니다.
4. `blocked`, `done`, `dropped`는 구현 후보에서 제외합니다.
5. task가 없거나 work_id가 불명확하면 추측하지 말고 멈춰서 물어봅니다.

## 시작 전 판단

구현 전에 아래를 짧게 밝힙니다.

- 선택 task
- TDD 적용 여부: `TDD 추천`, `TDD 비추천`, `TDD 생략`
- 실행 방식: `inline`, `sub-agent`
- 검증 명령 또는 확인 방법
- 코드 수정 포함 여부와 commit 필요 여부

### TDD 판단

TDD를 추천하는 경우:
- 새 behavior, bug fix, business logic, state transition, public API 변화
- regression risk가 있고 observable behavior로 검증 가능
- 기존 test harness가 있거나 작은 integration-style test를 추가할 수 있음

TDD를 생략하거나 비추천하는 경우:
- docs, prompt, manifest, config, copy 변경
- 테스트 harness가 없고 수동 검증이 더 직접적인 경우
- 매우 작은 mechanical rename이나 formatting 변경
- prototype/throwaway 작업

TDD 적용 시 규칙:
- horizontal slice 금지. 모든 test를 먼저 쓰지 않습니다.
- 한 번에 한 behavior test만 작성합니다.
- public interface로 observable behavior를 검증합니다.
- 내부 collaborator를 mock하지 않습니다. mock은 외부 API, time, randomness, filesystem 같은 boundary에 제한합니다.
- RED → minimal GREEN → 다음 behavior 순서로 진행합니다.
- RED 상태에서 refactor하지 않습니다.
- 모든 test가 green인 뒤에만 refactor합니다.

### 실행 방식 판단

inline을 선택하는 경우:
- 작은 task
- 1~3개 파일 변경
- command/prompt/docs처럼 문맥 판단이 중요한 변경
- 즉시 검증 가능한 변경

sub-agent를 선택하는 경우:
- task가 독립적이고 범위가 큼
- 파일 탐색/구현/검증을 분리해도 안전함
- 병렬 검토나 별도 구현 세션이 이득인 경우

sub-agent를 쓴 경우에도 최종 diff와 검증 결과는 main agent가 확인합니다.

### Agent routing

사용 가능한 TigerKit agent가 있으면 task 성격에 따라 선택합니다.

- 위치 탐색, 영향 범위 조사: Claude Code 내장 `Explore`
- 실제 API, 공식 contract, `TK-API-*` 교체 확인: `tk-sif-muna`
- 명확한 code/test/doc 구현 task: `tk-trog`
- UI, responsive layout, prototype 구현: `tk-nemelex-xobeh`
- screenshot, PDF, diagram 기반 확인: `tk-ashenzari`
- 반복 실패, architecture risk, review 판단: `tk-ru`

agent 사용 여부와 관계없이 task 선택, 상태 갱신, 최종 검증, local commit은 이 명령을 실행하는 main agent가 책임집니다.

## `mock_api_contract` task 처리

선택한 task가 `mock_api_contract` slice를 구현한다면 mock API는 외부 API boundary로만 둡니다. mock boundary 파일에는 `FIXME(TK-API-<n>)` marker를 남기고, 저장소 규칙상 `FIXME`가 금지되면 `TODO(TK-API-<n>)`로 낮춥니다. 검증은 mock API 기준 golden path, loading, error를 포함하고, empty state는 list/search/nullable data slice일 때 포함합니다.

## `TK-API-*` follow-up task 처리

선택한 task가 `API Follow-up Tasks`의 `TK-API-*`이면 실제 API나 공식 contract를 기준으로 assumed contract와 mock 경계를 교체합니다. 관련 `FIXME(TK-API-<n>)` 또는 `TODO(TK-API-<n>)` marker를 해결하거나, 실제 API 차단 사유가 남으면 marker와 task blocker 이유를 갱신합니다. 교체 완료 전에는 `done`으로 표시하지 않습니다.

## 구현 루프

1. task를 `in_progress`로 표시합니다.
2. 필요한 파일을 읽습니다.
3. TDD 적용 시 한 behavior test부터 작성하고 실패를 확인합니다.
4. 최소 구현으로 green을 만듭니다.
5. 필요한 behavior만 반복합니다.
6. refactor가 필요하면 green 상태에서만 작게 수행합니다.
7. 검증을 실행합니다.
8. `tasks.md`의 체크리스트뿐 아니라 현재 `gap.md`, 요구사항 문서, 실제 repo 상태와도 task 완료 판단이 맞는지 교차 확인합니다.
9. 완료 기준을 충족하면 task를 `done`으로 갱신합니다.
10. 코드 수정이 포함됐고 검증이 통과했으면 관련 변경 파일만 stage해 새 commit을 만듭니다. commit message는 repo의 최근 commit 스타일에 맞춥니다.
11. commit hook이 실패하면 우회하지 말고 원인을 고친 뒤 새 commit을 다시 시도합니다.
12. 실패하거나 막히면 `blocked`로 갱신하고 이유를 남깁니다.

## 안전 경계

- main/master/develop 같은 기반 브랜치에서 코드 변경을 시작하려면 먼저 작업 브랜치 사용을 권유합니다.
- 코드 수정 task의 local commit은 검증 통과 후 수행합니다.
- push, PR 생성, branch 생성은 사용자 승인 없이 실행하지 않습니다.
- 검증 실패를 숨기거나 hook을 우회하지 않습니다.
- task 범위를 넘어선 refactor를 하지 않습니다.

## 출력

마지막에는 아래만 짧게 보고합니다.

- 처리한 task
- TDD 사용 여부
- 실행 방식
- 변경 파일
- 검증 결과
- task 상태
- commit 생성 여부와 commit hash
- `다음 추천: /tk:next`
