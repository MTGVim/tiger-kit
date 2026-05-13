# 산출물 구조

TigerKit은 Backlog.md에 의존하지 않습니다. `.tigerkit/{work_id}/`가 repo-local source of truth입니다.

## 권장 구조

```text
.tigerkit/{work_id}/
  inputs/
    sources/
      <kind>/
        <name>/
          access.md
          meta.json
  requirements.md
  leverage.md
  tasks.md
  tasks.index.json
  handoff.md
  archive/
    tasks.done.md
```

## 파일 책임

| 파일 | 역할 |
| --- | --- |
| `inputs/` | 요구사항 정리에 참고한 source 접근 index 보관 위치. Figma 같은 대형 MCP source는 raw 대신 접근 방법만 기록 |
| `requirements.md` | 작업 기준점. 사용자 요구사항과 합의된 범위 |
| `leverage.md` | 참고 화면, reuse 후보, 피해야 할 구현, non-goals, API/외부 의존성, pending 질문 |
| `tasks.md` | 사람이 읽는 task ledger |
| `tasks.index.json` | Claude가 적은 token으로 현재 상태를 파악하기 위한 compact state index |
| `handoff.md` | 며칠 뒤 재진입을 위한 요약 |
| `archive/tasks.done.md` | 완료 또는 dropped task의 상세 이력 archive |

## source 접근 기록

Figma, design MCP, large document MCP처럼 큰 source는 원문 전체를 저장하지 않습니다. raw 저장은 context overflow를 만들고, 요약은 중요한 UI/detail 정보를 잃게 만들 수 있습니다. 대신 `access.md`에 다시 MCP로 접근할 수 있는 index만 남깁니다.

`access.md` 권장 항목:

```md
# Source Access

provider: figma
mcp_tool: figma.get_file | figma.get_node | ...
url: ...
file_key: ...
page_id: ...
frame_id: ...
node_ids:
- ...
selection_ids:
- ...
query_or_focus: ...
refetch_steps:
- MCP에서 file_key와 node_ids로 다시 조회
purpose: requirements/leverage 확인
checked_at: YYYY-MM-DD
```

작은 텍스트 source만 `*.raw.<ext>`를 둘 수 있습니다. 대형 MCP source에는 raw dump와 긴 `summary.md`를 만들지 않습니다.

Figma처럼 frame 단위 구조가 있는 source는 관련 frame을 각각 MCP로 새로 읽고, raw 대신 추출한 metadata/style 값만 chunk로 저장할 수 있습니다.

```text
inputs/sources/figma/<name>/
  access.md
  frames.index.json
  chunks/
    chunk-001.md
    chunk-002.md
```

chunk에는 frame id, node id, selection id, component name, text label, CSS/layout/spacing/color/typography 값, 관찰 목적만 둡니다. 전체 node tree raw dump는 넣지 않습니다.

CSS, layout, spacing, color, typography 같은 UI 요소를 확인할 때는 반드시 MCP source를 새로 읽습니다. `access.md`는 다시 접근하기 위한 index일 뿐이며, style 값의 최신 근거로 재사용하지 않습니다.

## 작업 흐름 단계

| 단계 | 근거 | 추천 다음 행동 |
| --- | --- | --- |
| `req-needed` | `requirements.md` 없음 | `/tk:prep` |
| `task-ledger-needed` | `requirements.md`는 있고 `tasks.md` 또는 `tasks.index.json` 없음 | `/tk:prep`로 ledger 생성/갱신 |
| `clarification-needed` | unresolved Clarification Actions 있음 | targeted question 또는 issue draft 정리 |
| `task-ready` | 실행 가능한 `todo` 또는 `in_progress` task 있음 | `/tk:next`, `/tk:do` |
| `blocked` | 실행 가능한 일반 task가 없고 외부 blocker만 있음 | blocker 해결 또는 API/contract 확인 |
| `gap-needed` | task 상태가 꼬였거나 close 전 점검 필요 | `/tk:gap` |
| `close-ready` | 실행 가능한 task가 없고 handoff 필요 | `/tk:close` |

## tasks.md 구조

```md
# Tasks

## Active Tasks

| ID | Status | Summary | Req | API Follow-ups | Done Criteria |
|---|---|---|---|---|---|

## API Follow-ups

| ID | Status | Summary | Affected Tasks | Mock Location | Resolution |
|---|---|---|---|---|---|

## Shared Blockers

| ID | Type | Status | Summary | Affected Tasks | Resolution |
|---|---|---|---|---|---|

## Done Archive

Moved to archive/tasks.done.md
```

## tasks.index.json 최소 구조

```json
{
  "tasks": [
    {
      "id": "T-003",
      "status": "done",
      "summary": "사용자 검색 UI 구현",
      "sourceRequirements": ["R-002"],
      "apiFollowups": ["TK-API-001"]
    },
    {
      "id": "T-004",
      "status": "todo",
      "summary": "검색 결과 empty state 구현",
      "sourceRequirements": ["R-003"],
      "apiFollowups": ["TK-API-001"]
    }
  ],
  "apiFollowups": [
    {
      "id": "TK-API-001",
      "status": "mock_api_contract",
      "summary": "사용자 검색 API contract 불명",
      "affectedTasks": ["T-003", "T-004"],
      "mergeBlocker": true,
      "mockLocation": "src/mocks/users.ts",
      "resolution": "실제 API contract 확인 후 mock 교체"
    }
  ],
  "sharedBlockers": []
}
```

넣지 말 것:

- 복잡한 API taxonomy
- 과도한 evidence log
- 긴 plan 전문
- 상세 dependency graph

## API Follow-ups와 Shared Blockers

| 섹션 | 용도 |
| --- | --- |
| `API Follow-ups` | mock 가능하거나 API contract 확인이 필요한 항목 |
| `Shared Blockers` | 권한, 인간 결정, 외부 의존성 등 실제로 여러 task를 막는 것 |

API follow-up은 `/tk:do` 중 실제 필요할 때 lazy하게 생성합니다. 확신 있으면 기존 follow-up을 재사용하고, 애매하면 새 follow-up을 만든 뒤 `/tk:gap` 또는 `/tk:close`에서 병합 후보로 보고합니다.

## archive 정책

기본 실행 경로에서 command는 `tasks.index.json`과 `tasks.md`의 active queue만 우선 읽습니다. 완료/dropped 상세 본문은 `archive/tasks.done.md`로 분리하고, active queue에는 pointer와 count만 남깁니다.

## cleanup 경계

`/tk:close`는 cleanup 후보를 제안할 수 있지만 branch 생성, commit, push, PR 생성, merge, deploy, 파일 삭제는 사용자 승인 없이 실행하지 않습니다.
