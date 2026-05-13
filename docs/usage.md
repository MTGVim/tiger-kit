# 사용법

## 언어

명령은 사용자에게 한글로 답하고 작업 산출물도 한글로 작성합니다. 인용한 원문, 코드, 명령어, 경로, 식별자는 원문 그대로 유지할 수 있습니다.

## 핵심 모델

```text
TigerKit = repo-local requirements/task/status/API-followup ledger
```

TigerKit은 Backlog.md에 의존하지 않습니다. `.tigerkit/{work_id}/` 아래 artifact가 source of truth입니다.

기본 흐름:

```text
/tk:prep
/tk:next
/tk:do T-001
/tk:gap
/tk:close
```

## Command Surface

| Command | 역할 |
| --- | --- |
| `/tk:prep` | 요구사항 source를 task ledger로 정리 |
| `/tk:next` | 다음 task 또는 사용자 action 하나 추천 |
| `/tk:do` | task 하나 구현, API follow-up 갱신 |
| `/tk:gap` | requirements/task/API/blocker/readiness 점검 |
| `/tk:close` | handoff와 merge-ready 판단 정리 |

skill은 command surface 밖에서 유지됩니다. `issue`는 자연어 auto-trigger 없이 command가 명시적으로 요청할 때만 씁니다.

| Skill | 역할 |
| --- | --- |
| `issue` | command가 명시적으로 요청할 때 issue/task-ledger 변경 draft 작성. 자연어 auto-trigger 없음 |

## 1. 준비

```text
/tk:prep <요구사항, 티켓, 메모, source>
```

하는 일:

1. 사용자 요구사항 정리
2. leverage 확인
3. `requirements.md` 생성/갱신
4. requirements를 작은 task로 소분
5. `tasks.md` 생성/갱신
6. `tasks.index.json` 생성/갱신

하지 않는 일:

- Figma 같은 대형 MCP source raw dump 저장
- 대형 source 긴 요약 생성
- 현재 구현 전체 분석
- API capability taxonomy 생성
- 과도한 plan 문서 생성
- gap report 대량 생성
- 구현, commit, push, PR 생성

## source 접근 기록

Figma처럼 큰 MCP source는 raw 전체를 받거나 저장하지 않습니다. `inputs/sources/<kind>/<name>/access.md`에 URL, file key, frame id, node id, selection id, MCP tool, 다시 접근하는 방법만 index처럼 기록합니다. 작은 텍스트 source만 raw snapshot을 둘 수 있습니다.

Figma처럼 frame 단위 구조가 있는 source는 관련 frame을 각각 MCP로 새로 읽고, raw 대신 추출한 metadata/style 값만 `chunks/chunk-001.md`처럼 나눠 저장할 수 있습니다. chunk에는 frame id, node id, selection id, component name, text label, CSS/layout/spacing/color/typography 값, 관찰 목적만 둡니다.

CSS, layout, spacing, color, typography 같은 UI 요소를 확인할 때는 반드시 현재 MCP source를 새로 읽습니다. 오래된 access 기록이나 screenshot 요약만으로 style 값을 확정하지 않습니다.

## 2. 다음 task 추천

```text
/tk:next
```

역할:

1. `tasks.index.json` 읽기
2. 실행 가능한 task 하나 고르기
3. 연결된 blocker/API follow-up 표시
4. 다음 행동만 제안

원칙:

```text
/tk:next는 전체 계획을 다시 만들지 않고 다음 task 하나만 보여준다.
```

## 3. task 하나 실행

```text
/tk:do T-004
```

하는 일:

1. task 하나 선택
2. 구현 시점에 현재 코드 확인
3. 필요한 API 확인
4. 구현
5. 테스트/검증
6. task 상태 갱신
7. 필요하면 API Follow-up 생성/연결

API 존재 여부는 `/tk:prep`에서 미리 추측하지 않습니다. `/tk:do`에서 실제 필요할 때 확인합니다.

## API 정책

```text
TigerKit은 API 부재를 항상 개발 blocker로 취급하지 않는다.

task 구현 중 API contract가 없거나 불명확한 경우:
- mock contract로 안전하게 진행 가능하면 task를 계속 진행한다.
- TK-API-* follow-up을 새로 만들거나 기존 항목을 재사용한다.
- 영향받는 task를 해당 follow-up에 연결한다.
- unresolved API follow-up은 task 실행 blocker가 아니라 close/merge blocker로 남긴다.
- mock이 잘못된 확신을 만들거나 유효하지 않은 구현을 강제한다면 task를 blocked로 둔다.
```

| 상황 | task 상태 | API follow-up 상태 | 의미 |
| --- | --- | --- | --- |
| API 없음, mock 가능 | `todo` / `in_progress` / `done` 가능 | `mock_api_contract` | 개발은 진행 가능, close/merge 전 확인 필요 |
| API 없음, mock 불가 | `blocked` | `blocked` | task 실행 불가 |
| API 있음 | 일반 진행 | 없음 | 정상 구현 가능 |

강한 API Capability Key는 만들지 않습니다. 동일 API 문제 grouping은 task 구현 중 기존 `TK-API-*` follow-up을 lazy하게 재사용하는 방식으로 처리합니다.

## 4. 점검

```text
/tk:gap
```

`/tk:gap`는 기존 gap 분석의 축소판입니다. 중심 workflow가 아니라 검증 gate입니다.

역할:

1. requirements 대비 누락 확인
2. task 상태 정리
3. API follow-up 중복 병합 후보 확인
4. shared blocker 확인
5. unresolved blocker 확인
6. close/merge readiness 판단

추천 실행 시점:

- 사용자가 명시적으로 호출할 때
- close 전
- task 상태가 꼬였다고 판단될 때
- API follow-up이 여러 개 쌓였을 때

`/tk:gap`는 report-only입니다. 파일 수정, task 생성, follow-up 자동 병합, PR/merge/push/deploy를 하지 않습니다.

## 5. 종료

```text
/tk:close
```

출력해야 할 것:

1. 완료한 task
2. 남은 task
3. unresolved API follow-ups
4. shared blockers
5. merge-ready 여부
6. 다음 세션 handoff

중요 판정:

```text
unresolved TK-API-* 있음
→ development may be complete
→ merge-ready는 아님
```

## 검증

TigerKit 저장소에는 package manager 기반 build/test/lint 설정이 없습니다. 명령, manifest, eval fixture를 수정한 뒤에는 다음 검증을 기본으로 실행합니다.

```bash
claude plugin validate .claude-plugin/plugin.json
claude plugin validate .
python3 -m json.tool evals/evals.json >/dev/null
git diff --check
```

`evals/evals.json`은 자동 실행 테스트가 아니라 fixture입니다. JSON 문법 검증과 수동 기대 동작 검토만 의미합니다.
