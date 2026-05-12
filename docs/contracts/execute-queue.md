# execute-queue 내부 contract

`execute-queue`는 사용자-facing slash command가 아니라 `/tk:auto`의 task 단계에서 쓰는 내부 실행 contract입니다.

## 목적

`.tigerkit/{work_id}/tasks.md`의 실행 가능한 active task를 하나씩 처리하고, 각 task가 요구사항 기준과 검증을 통과할 때만 완료로 표시합니다.

## 입력 read policy

기본 실행 경로는 아래만 우선 읽습니다.

1. `.tigerkit/{work_id}/tasks.index.json`
2. `.tigerkit/{work_id}/tasks.md`의 active queue
3. task가 참조하는 `requirements.md`, `gap.md`, `plan.md`의 필요한 부분

`archive/tasks.done.md`는 기본 context에 넣지 않습니다. 사용자가 특정 완료 task를 지정했거나 regression, review, close 근거 확인에 필요할 때만 읽습니다.

## 처리 대상

- `in_progress` task를 먼저 처리합니다.
- 그다음 `todo` task를 순서대로 처리합니다.
- `blocked`, `done`, `dropped`는 실행 후보에서 제외합니다.
- unresolved `Clarification Actions`가 있으면 구현 loop를 시작하지 않고 clarification next action을 보고합니다.
- `API Follow-up Tasks`의 `TK-API-* blocked`만 남은 경우에는 일반 `todo`/`in_progress` task를 계속 처리하고 merge blocker로 보고합니다.

## task별 gate

각 task는 아래 순서를 따릅니다.

1. task를 `in_progress`로 표시합니다.
2. 필요한 파일만 읽습니다.
3. `Requirement Pinning`을 보고합니다.
   - Task ID
   - `Source requirements`
   - exact copy, strict constraint, allowed discretion
   - unresolved ambiguity 여부
4. 관련 요구사항을 특정할 수 없거나 exact copy source가 없으면 구현하지 않고 `TK-CLARIFY-*` 후보를 만듭니다.
5. TDD 적용 여부를 task 성격에 따라 판단합니다.
6. 최소 변경으로 구현합니다.
7. 검증을 실행합니다.
8. `Spec Adherence Gate`를 수행합니다.
   - checked requirements
   - unsourced assumptions
   - missing verification
   - verdict: `PASS`, `FAIL_SPEC_VIOLATION`, `NEEDS_CLARIFICATION`
9. `PASS`일 때만 task를 `done`으로 갱신합니다.
10. 코드 수정이 포함됐고 검증이 통과했으면 관련 변경 파일만 stage해 task별 local commit을 만듭니다.

`FAIL_SPEC_VIOLATION` 또는 `NEEDS_CLARIFICATION`이면 다음 task로 넘어가지 않고 멈춥니다.

## TDD 기준

추천:
- behavior/API/business logic/bug fix/regression risk
- public interface로 검증 가능한 변경

생략 가능:
- docs/prompt/manifest/config/copy 변경
- test harness 부재
- 작은 mechanical 변경

TDD 적용 시 한 test → 최소 구현 → green → 다음 test 순서만 사용합니다.

## Agent routing

Agent 이름은 짧은 표기를 쓰되, plugin runtime이 `tk:tk-*`로 표시되면 namespaced 이름을 사용합니다.

- 탐색/영향 범위: Claude Code 내장 `Explore`
- API/contract 확인: `tk-sif-muna`
- bounded implementation: `tk-trog`
- cleanup/docs hygiene: `tk-elyvilon`
- UI/prototype: `tk-nemelex-xobeh`
- visual artifact 분석: `tk-ashenzari`
- spec-adherence review, trade-off, risk 판단: `tk-ru`

한 task 내부에서 sub-agent를 쓰더라도 main agent가 diff 병합, 최종 검증, task 상태 갱신, commit 책임을 집니다.

## 중단 조건

- work_id가 불명확함
- 요구사항 모호함이 있어 `Clarification Actions`가 필요함
- `FAIL_SPEC_VIOLATION`
- `NEEDS_CLARIFICATION`
- 검증 실패 반복
- 외부 blocker 존재. 단 `TK-API-* blocked`만 있고 mock 기준 일반 task가 남아 있으면 중단하지 않습니다.
- 예상보다 범위가 커져 사용자 결정이 필요함
- main/master/develop 같은 기반 브랜치에서 변경 승인이 필요함

## tail gap check

실행 가능한 일반 task를 모두 처리했고 unresolved `Clarification Actions`, 외부 blocked task, `Shared Blockers`의 `상태=blocked` 항목이 없다면 종료 전에 gap을 한 번만 다시 확인합니다.

- tail gap check는 최대 1회만 수행합니다.
- 새 gap이 있으면 `gap.md`를 갱신하고 멈춥니다. 바로 다음 implementation cycle로 들어가지 않습니다.
- 새 gap이 없고 unresolved `Clarification Actions`, unresolved `TK-API-*`, blocked `Shared Blockers`가 없으면 `/tk:close`를 추천합니다.
- unresolved `TK-API-*`가 남아 있으면 merge blocker와 incomplete 상태를 보고하고 API/contract 확인을 다음 action으로 둡니다.

## 출력

`/tk:auto`가 사용자에게 보고합니다. 기본 출력은 receipt-first로 유지하고, 상세 상태 dump 대신 처리 task 수, 검증 결과, 남은 blocker, tail gap check 결과, 다음 추천만 짧게 포함합니다.
