---
description: .tigerkit task ledger의 task 하나를 구현하고 lazy API follow-up을 갱신합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 코드, 테스트 이름, 파일 경로, 식별자, 오류 메시지는 원문 그대로 유지할 수 있습니다.

목표: `.tigerkit/{work_id}/tasks.md`의 task 하나를 구현하고 `tasks.md`, `tasks.index.json`, 필요한 API follow-up 상태를 갱신합니다. `/tk:do`가 TigerKit의 중심 command입니다.

## task 선택

1. 사용자가 task ID를 지정했으면 그 task를 선택합니다.
2. 지정이 없으면 `tasks.index.json`에서 `in_progress`, 그다음 첫 번째 `todo`를 선택합니다.
3. `blocked`, `done`, `dropped`는 구현 후보에서 제외합니다.
4. task가 없거나 work_id가 불명확하면 추측하지 말고 멈춰서 물어봅니다.
5. 한 번에 task 하나만 처리합니다.

## 시작 전 판단

구현 전에 아래를 짧게 밝힙니다.

- 선택 task와 source requirement
- API 확인 필요 여부
- TDD 적용 여부: `TDD 추천`, `TDD 비추천`, `TDD 생략`
- 실행 방식: `inline`, `sub-agent`
- 검증 명령 또는 확인 방법

## Implementation Context Scan Gate

구현 전에는 blank context 질문으로 시작하지 않습니다. 먼저 조사하고, 그 결과를 기준으로 사용자에게 correction만 요청합니다.

순서:

1. 선택 task와 연결 requirement를 확인합니다.
2. relevant user-level learning from reflect가 있으면 먼저 읽고 이번 scan의 operational guidance로 적용합니다.
3. `.tigerkit/{work_id}/requirements.md`를 읽습니다.
4. `.tigerkit/{work_id}/implementation-context.md`를 먼저 읽습니다.
5. `implementation-context.md`가 없고 legacy `.tigerkit/{work_id}/leverage.md`가 있으면 fallback으로 읽습니다.
6. 관련 화면, route, page, component, hook, util, form pattern, API usage, test, source reference를 조사합니다.
7. `Proposed Implementation Context`를 짧게 제시합니다.
8. 사용자는 blank form 작성자가 아니라 agent scan의 editor여야 합니다. 추가/수정이 있으면 첨삭받고, 없으면 그 기준으로 진행합니다.
9. 사용자 correction은 `implementation-context.md`에 기록합니다.

`User-Level Prior Applied`는 personal profile dump가 아니라 이번 task에서 적용한 operational guidance로 씁니다.

좋은 예:

```text
- 먼저 조사한 뒤 기준을 제시하고 첨삭받기
- 기존 구현, 컴포넌트 재사용 우선
- product/copy/API intent는 추측하지 않기
```

피할 예:

```text
- 이 사용자는 X를 싫어한다
```

출력 패턴:

```md
구현 전 컨텍스트를 먼저 확인했습니다.

## 적용한 사용자 레벨 기준
- ...

## 참고할 기존 구현
- ...

## 재사용 후보
- ...

## 피해야 할 접근
- ...

## 범위 밖
- ...

## 아직 애매한 점
- ...

이 기준으로 진행하겠습니다.
추가로 참고해야 할 화면/컴포넌트/source,
반드시 재사용해야 할 hook/util/pattern,
피해야 할 접근,
범위 밖 항목이 있으면 첨삭해주세요.
없으면 이 기준으로 진행합니다.
```

`reflect`의 durable knowledge는 사용자 승인 없이 갱신하지 않습니다. 읽어서 priors로 적용할 수는 있지만, 쓰기나 promotion은 명시적 승인 뒤에만 합니다.

## API 정책

API 존재 여부는 planning 단계에서 미리 전부 확인하지 않습니다. task 구현 시점에 필요한 만큼 확인합니다.

```text
API available
→ 실제 API 또는 공식 contract 기준으로 구현

API missing + safe mock
→ task 구현 계속
→ TK-API-* follow-up 생성 또는 재사용
→ affected task 연결
→ mock location과 해소 조건 기록
→ unresolved API follow-up은 close/merge blocker

API missing + unsafe mock
→ task를 blocked로 둠
→ blocked reason과 필요한 contract/결정 기록
```

원칙:

```text
API 없음 = 무조건 blocked 아님
mock 가능 = 개발 진행 가능
unresolved API = close/merge blocker
```

강한 API Capability Key는 만들지 않습니다. `TK-API-*` follow-up ID만 사용합니다.

## lazy follow-up reuse

1. 새 API 문제가 발견되면 기존 `API Follow-ups`와 `tasks.index.json.apiFollowups`를 확인합니다.
2. 같은 문제로 확신하면 기존 `TK-API-*`를 재사용합니다.
3. 애매하면 새 `TK-API-*`를 만듭니다.
4. `/tk:gap` 또는 `/tk:close`에서 중복 병합 후보를 보고합니다.

## 구현 루프

1. task를 `in_progress`로 표시합니다.
2. 필요한 파일만 읽습니다.
3. `Requirement Pinning`을 짧게 정리합니다.
4. 현재 코드와 필요한 API를 확인합니다.
5. CSS, layout, spacing, color, typography 같은 UI 요소가 task 판단에 필요하면 Figma/design MCP source를 새로 읽습니다. 오래된 access 기록, raw, summary, screenshot 설명만으로 style 값을 확정하지 않습니다.
6. safe mock 가능 여부를 판단합니다.
7. 최소 변경으로 구현합니다.
8. 검증을 실행합니다.
9. `Spec Adherence Gate`를 수행합니다.
10. 디자인/UX/API/copy/product 판단처럼 사람 검수가 필요하면 `done` 대신 `review_required`로 둡니다.
11. `PASS`이고 사람 검수가 필요 없을 때만 task를 `done` 또는 repo convention에 맞는 완료 상태로 갱신합니다.
12. `tasks.md`와 `tasks.index.json`의 task 상태, API follow-up link, shared blocker 상태를 함께 갱신합니다.
13. 필요하면 `archive/tasks.done.md`로 완료 task 상세를 옮기고 active queue에는 compact pointer만 남깁니다.

## TDD 기준

추천:
- 새 behavior, bug fix, business logic, state transition, public API 변화
- regression risk가 있고 observable behavior로 검증 가능

생략 가능:
- docs, prompt, manifest, config, copy 변경
- 테스트 harness가 없고 수동 검증이 더 직접적인 경우
- 작은 mechanical 변경

TDD 적용 시 한 behavior test → 최소 구현 → green → 다음 behavior 순서만 사용합니다.

## Agent routing

Agent 이름은 짧은 표기를 쓰되, plugin runtime이 `tk:tk-*`로 표시하면 그 namespaced 이름을 사용합니다.

- 위치 탐색, 영향 범위 조사: Claude Code 내장 `Explore`
- 실제 API, 공식 contract, `TK-API-*` 교체 확인: `tk-sif-muna`
- 명확한 code/test/doc 구현 task: `tk-trog`
- cleanup, docs hygiene, 작은 consistency patch: `tk-elyvilon`
- UI, responsive layout, prototype 구현: `tk-nemelex-xobeh`
- screenshot, PDF, diagram 기반 확인: `tk-ashenzari`
- 반복 실패, architecture risk, review 판단: `tk-ru`

agent를 사용해도 task 선택, 상태 갱신, 최종 검증은 main agent가 책임집니다.

## 금지

- 여러 task 동시 구현
- 강한 API taxonomy 생성
- task 범위 밖 refactor
- 사용자 승인 없는 branch 생성, commit, push, PR 생성, merge, deploy
- 검증 실패 숨김
- blank context interview로 구현 시작
- 사용자 승인 없는 durable reflect mutation

## 출력

```text
처리했습니다.
- task: T-004 검색 결과 empty state 구현
- implementation context: `.tigerkit/search/implementation-context.md`
- API: TK-API-001 mock_api_contract, close/merge blocker
- 변경 파일: ...
- 검증: 통과
- 상태: done

다음 추천: /tk:next
```