---
description: 요구사항 source를 .tigerkit task ledger로 정리하고 light-gap까지 반영합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 작업 산출물도 한글로 작성합니다. 단, 인용한 원문, 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

목표: 사용자 요구사항 source를 `.tigerkit/{work_id}/requirements.md`와 실행 가능한 task queue로 정리합니다. `/tk:prep`은 project planning command가 아니라 source-to-task-ledger command이며, 마지막에 경량 light-gap sanity pass를 수행합니다.

## 기본 산출물

- `.tigerkit/{work_id}/requirements.md`
- `.tigerkit/{work_id}/implementation-context.md`
- `.tigerkit/{work_id}/tasks.md`
- `.tigerkit/{work_id}/tasks.index.json`
- `.tigerkit/{work_id}/decisions.md`
- 필요 시 `.tigerkit/{work_id}/inputs/sources/<kind>/<name>/`

기존 workdir에 `leverage.md`가 있어도 신규 기본 산출물로 유지하지 않습니다. legacy `leverage.md` 호환성은 `/tk:do`에서만 처리합니다.

## work_id 결정

1. 사용자가 work_id 또는 `.tigerkit/{work_id}/` 경로를 지정했으면 그것을 사용합니다.
2. 앞선 대화나 source에서 자연스러운 작업명이 명확하면 후보 work_id를 제안합니다.
3. 후보가 없거나 여러 개면 추측하지 말고 work_id를 물어봅니다.
4. `main`, `master`, `develop` 같은 기반 브랜치에서 변경 가능한 작업을 시작한다면 작업 브랜치 사용을 권유하지만, 브랜치 생성/전환은 사용자 승인 없이 하지 않습니다.

## 절차

1. source material을 요구사항, scope, non-goal, acceptance signal로 정리합니다.
2. source가 부족하면 사용자가 중간에 자료를 추가한 뒤 reply로 이어갈 수 있게 필요한 추가 source만 요청하고 멈춥니다.
3. implementation context 초안을 먼저 정리합니다.
4. 요구사항을 작은 task로 소분합니다.
5. `tasks.md`를 active task ledger로 작성/갱신합니다.
6. `tasks.index.json`을 compact state index로 작성/갱신합니다.
7. `decisions.md`를 초기화하거나 기존 구조를 유지합니다.
8. API 문제는 planning 단계에서 taxonomy로 만들지 않습니다. source에 명시된 외부 blocker만 기록하고, 실제 API follow-up은 `/tk:do`에서 lazy하게 만듭니다.
9. 마지막에 light-gap sanity pass를 수행합니다.

## light-gap

`/tk:prep`의 light-gap는 `/tk:gap`을 대체하지 않습니다. 아래만 경량 점검합니다.

- requirement 누락/중복
- task granularity 과대/과소
- immediate clarification 필요 여부
- obvious shared blocker
- 바로 실행 가능한 task 존재 여부

하지 않는 일:
- merge-ready 판단
- API follow-up 병합 후보 정밀 검토
- detailed readiness audit
- report-only 장문 gap 출력

## source 접근 기록

Figma처럼 큰 MCP source는 raw 전체를 저장하지 않습니다. raw는 context overflow를 만들고, 요약은 정보 손실을 만듭니다. 대신 `.tigerkit/{work_id}/inputs/sources/<kind>/<name>/access.md`에 다시 접근할 수 있는 index만 기록합니다.

기록 항목:

- provider와 MCP tool 이름
- source URL
- file/project key
- page/frame id
- node id 또는 selection id 목록
- 사용한 query/focus
- 다시 불러오는 방법
- 확인한 시점과 목적

작은 텍스트 source만 raw snapshot을 둘 수 있습니다. 대형 MCP source에는 `*.raw.*`와 긴 `summary.md`를 만들지 않습니다.

Figma처럼 frame 단위 구조가 있는 source는 관련 frame을 각각 MCP로 새로 읽고, raw 대신 추출한 metadata/style 값만 chunk로 저장할 수 있습니다.

권장 구조:

```text
inputs/sources/figma/<name>/
  access.md
  frames.index.json
  chunks/
    chunk-001.md
    chunk-002.md
```

chunk에는 frame id, node id, selection id, component name, text label, CSS/layout/spacing/color/typography 값, 관찰 목적만 둡니다. 전체 node tree raw dump는 넣지 않습니다.

CSS, layout, spacing, color, typography 같은 UI 요소를 확인할 때는 이전 `access.md`나 오래된 screenshot 요약에 의존하지 않습니다. 반드시 현재 MCP source를 새로 읽고, 사용한 node id/selection id와 refetch steps를 다시 기록합니다.

## Implementation Context 초안

사용자를 blank interview로 시작시키지 않습니다. agent가 먼저 source와 repo 맥락을 바탕으로 implementation context 초안을 만들고, 사용자는 그 초안을 첨삭합니다.

`implementation-context.md`에는 아래 범주를 담습니다.

- 참고할 기존 화면, flow, 구현
- 재사용 후보 컴포넌트, hook, util, pattern
- 피해야 할 구현, dependency, UX, protected contract
- inferred non-goal, scope boundary, do-not-touch 범위
- material unknowns와 safe assumption
- 사용자가 수정한 context
- 최종 implementation context

한 번에 하나의 material question만 묻습니다. 답을 못 해도 `pending`으로 기록하고 안전한 범위에서 계속합니다.

질문은 blank form이 아니라 correction prompt여야 합니다.

```text
제가 먼저 확인한 기준은 이렇습니다.

- 참고할 기존 구현: ...
- 재사용 후보: ...
- 피해야 할 접근: ...
- 범위 밖: ...
- 아직 애매한 점: ...

이 기준으로 진행하겠습니다.
추가/수정할 참고 대상이나 제약이 있으면 첨삭해주세요.
```

## tasks.index.json 최소 schema

```json
{
  "tasks": [
    {
      "id": "T-001",
      "status": "todo",
      "summary": "...",
      "sourceRequirements": ["R-001"],
      "apiFollowups": [],
      "decisionLogRef": "decisions.md#t-001",
      "changedFiles": []
    }
  ],
  "apiFollowups": [],
  "sharedBlockers": [],
  "steer": {
    "active": false
  },
  "reflect": {
    "pendingCandidateCount": 0
  }
}
```

`tasks.index.json`에는 긴 plan, evidence log, 복잡한 API taxonomy, 상세 dependency graph를 넣지 않습니다. 목적은 다음 상태를 적은 token으로 읽는 것입니다.

## 금지

- 현재 구현 전체 분석
- gap report 대량 생성
- 과도한 plan 문서 생성
- API capability taxonomy 생성
- 강한 API key 생성
- task와 무관한 reflect 승격 흐름 시작
- 구현, commit, push, PR 생성, merge, deploy

## 출력

receipt-first로 짧게 보고합니다.

```text
task ledger 만들었습니다.
- work_id: search-ui
- requirements: `.tigerkit/search-ui/requirements.md`
- implementation context: `.tigerkit/search-ui/implementation-context.md`
- tasks: T-001..T-004
- light-gap: task-ready

다음 추천: /tk:task
```