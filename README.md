# TigerKit

![TigerKit](assets/tigerkit-cover.png)

[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors)

TigerKit(`tiger-kit`, plugin `tk`)은 repo-local requirements/task/status/API-followup/decision ledger를 관리하는 작은 Claude Code 플러그인입니다.

```text
requirements
→ tasks
→ task status
→ blocked reason
→ API follow-up
→ decisions
```

TigerKit은 Backlog.md에 의존하지 않습니다. `.tigerkit/{work_id}/` 아래 artifact를 source of truth로 둡니다.

## Command Surface

| Command | 역할 |
| --- | --- |
| `/tk:prep` | 요구사항 source를 `.tigerkit` task ledger로 정리하고 light-gap까지 반영 |
| `/tk:task` | task ledger 상태 조회, 추가, 상태 갱신, 상위 status snapshot |
| `/tk:next` | 다음 task 또는 사용자 action 하나 추천 |
| `/tk:do` | autopilot으로 task 하나 구현, decisions/API follow-up 갱신 |
| `/tk:steer` | user-steered execution 시작 |
| `/tk:steer-end` | steer 세션 종료, correction/reflect candidate 정리 |
| `/tk:gap` | requirements/task/API/blocker/readiness deep audit |
| `/tk:statusline` | steer/reflect indicator 표시 위치 설정 |

## Workflow

```mermaid
graph TD
    A[Start] --> B[/tk:prep]
    B --> C[/tk:task]
    C --> D{What now?}

    D -->|Need overview| E[/tk:task list]
    D -->|Need next step| F[/tk:next]
    D -->|Want autopilot| G[/tk:do]
    D -->|Want direct drive| H[/tk:steer]

    G --> I[Update tasks.md / tasks.index.json]
    G --> J[Write decisions.md]
    G --> K[/tk:task status]

    H --> L[Follow user instruction step by step]
    H --> M[Write decisions.md]
    H --> N[Capture correction / reuse / ask-rules]
    H --> O[/tk:steer-end]

    E --> C
    F --> C
    I --> K
    J --> K
    L --> O
    M --> K
    N --> K
    O --> K

    K --> P{Need deeper audit?}
    P -->|Yes| Q[/tk:gap]
    P -->|No| C
    Q --> C

    R[/tk:statusline] --> S["[🛞] [🪞 2] [🛞 / 🪞 2]"]
```

기본 흐름:

```text
/tk:prep
/tk:task
/tk:next
/tk:do T-001
/tk:task status
/tk:gap
```

직접주행 흐름:

```text
/tk:prep
/tk:task
/tk:steer
... 자연어로 지시/교정 ...
/tk:steer-end
/tk:task status
```

## Mental Model

- `/tk:do` = autopilot
- `/tk:steer` = direct drive
- `/tk:task` = 상태판 entrypoint
- `/tk:gap` = deep audit

## Artifact Layout

```text
.tigerkit/{work_id}/
  inputs/
  requirements.md
  implementation-context.md
  tasks.md
  tasks.index.json
  decisions.md
  steer-state.json
  archive/
    tasks.done.md
```

| Artifact | 역할 |
| --- | --- |
| `requirements.md` | 작업 기준점. 사용자 요구사항과 합의된 범위 |
| `implementation-context.md` | 참고 구현, 재사용 후보, 피해야 할 구현, non-goals, unknowns, 사용자 첨삭을 담는 구현 전 컨텍스트 |
| `tasks.md` | 사람이 읽는 task ledger |
| `tasks.index.json` | Claude가 적은 token으로 현재 상태를 파악하는 compact state index |
| `decisions.md` | `do`와 `steer`가 남기는 compact decision trace |
| `steer-state.json` | local steer runtime state |
| `archive/tasks.done.md` | 완료 task archive |

기존 workdir의 `leverage.md`는 legacy alias입니다. 신규 기본 산출물은 `implementation-context.md`이며, `/tk:do`는 새 파일이 없을 때만 `leverage.md`를 fallback으로 읽습니다.

## Core Policy

TigerKit은 초안을 만들고, 최종 touch와 승인은 사람이 합니다.

| 상황 | task 상태 | API follow-up 상태 | 의미 |
| --- | --- | --- | --- |
| API 없음, mock 가능 | `todo` / `in_progress` / `done` 가능 | `mock_api_contract` | 개발은 진행 가능, merge 전 확인 필요 |
| API 없음, mock 불가 | `blocked` | `blocked` | task 실행 불가 |
| API 있음 | 일반 진행 | 없음 | 정상 구현 가능 |
| 사람 검수 필요 | `review_required` | 상황별 | 디자인/UX/API/copy/product 판단 전에는 done 아님 |

원칙:

```text
API 없음 = 무조건 blocked 아님
mock 가능 = 개발 진행 가능
unresolved API = merge blocker
```

강한 API Capability Key는 만들지 않습니다. `TK-API-*` follow-up ID만 lazy하게 생성/재사용합니다.

## Prep Light-Gap vs Gap

`/tk:prep`은 끝에서 light-gap sanity pass를 수행합니다.

- requirement 누락/중복
- task granularity 과대/과소
- immediate clarification 필요 여부
- obvious shared blocker
- 바로 실행 가능한 task 존재 여부

`/tk:gap`는 이보다 깊은 audit입니다.

- requirements coverage
- task state consistency
- API follow-up duplicate 후보
- blocker/readiness 판단

## Steering / Reflect Indicators

기본 indicator 규칙:

- steer only -> `[🛞]`
- reflect pending only -> `[🪞 2]`
- both -> `[🛞 / 🪞 2]`
- none -> 숨김

기본 delivery는 trailing이며, `/tk:statusline`으로 statusline 표시를 설정할 수 있습니다.

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
      "apiFollowups": ["TK-API-001"],
      "decisionLogRef": "decisions.md#t-003",
      "changedFiles": ["src/components/Search.tsx"]
    }
  ],
  "apiFollowups": [
    {
      "id": "TK-API-001",
      "status": "mock_api_contract",
      "summary": "사용자 검색 API contract 불명",
      "affectedTasks": ["T-003"],
      "mergeBlocker": true,
      "mockLocation": "src/mocks/users.ts",
      "resolution": "실제 API contract 확인 후 mock 교체"
    }
  ],
  "sharedBlockers": [],
  "steer": {
    "active": false
  },
  "reflect": {
    "pendingCandidateCount": 0
  }
}
```

넣지 말 것:

- 복잡한 API taxonomy
- 과도한 evidence log
- 긴 plan 전문
- 상세 dependency graph

## 설치

### Marketplace로 설치

```text
/plugin marketplace add MTGVim/tiger-kit
/plugin install tk@tiger-kit
/reload-plugins
```

### 로컬 플러그인 디렉터리로 사용

```bash
claude --plugin-dir ./tiger-kit
```

## 검증

이 저장소에는 package manager 기반 build/test/lint 설정이 없습니다. TigerKit을 수정한 뒤에는 다음 검증을 우선 실행합니다.

```bash
claude plugin validate .claude-plugin/plugin.json
claude plugin validate .
python3 -m json.tool evals/evals.json >/dev/null
git diff --check
```

`evals/evals.json`은 자동 실행 테스트가 아니라 명령 기대 동작 fixture입니다. 현재 저장소에는 이 fixture를 LLM에 넣어 pass/fail 판정하는 runner나 harness가 없습니다.

## Inspired by

TigerKit은 아래 workflow와 skill/repo에서 아이디어를 참고해 목적에 맞게 축약했습니다.

- [`claude-reflect`](https://github.com/dontriskit/claude-reflect)
- [OACP `self-improve`](https://github.com/OpenAgentic/agentic-coding-protocol/tree/main/commands/self-improve)
- [Matt Pocock `tdd`](https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd)
- [Q00 `ouroboros`](https://github.com/Q00/ouroboros)
- [superpowers `executing-plans`](https://github.com/pcvelz/superpowers/blob/main/skills/executing-plans/SKILL.md)

## Contributors

Thanks goes to these wonderful people:

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/MTGVim"><img src="https://avatars.githubusercontent.com/u/6271133?v=4?s=100" width="100px;" alt="Taekwon Yoo"/><br /><sub><b>Taekwon Yoo</b></sub></a><br /><a href="https://github.com/MTGVim/tiger-kit/commits?author=MTGVim" title="Code">💻</a> <a href="https://github.com/MTGVim/tiger-kit/commits?author=MTGVim" title="Documentation">📖</a> <a href="#ideas-MTGVim" title="Ideas, Planning, & Feedback">🤔</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://allcontributors.org/) specification. Contributions of any kind are welcome.
