# 사용법

## 언어

명령은 사용자에게 한글로 답하고 작업 산출물도 한글로 작성합니다. 인용한 원문, 코드, 명령어, 경로, 식별자는 원문 그대로 유지할 수 있습니다.

## 핵심 모델

```text
TigerKit = repo-local requirements/task/status/API-followup/decision ledger
```

TigerKit은 Backlog.md에 의존하지 않습니다. `.tigerkit/{work_id}/` 아래 artifact가 source of truth입니다.

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

## Command Surface

| Command | 역할 |
| --- | --- |
| `/tk:prep` | 요구사항 source를 task ledger로 정리하고 light-gap까지 반영 |
| `/tk:task` | task ledger 상태 조회, 새 task 추가, 상태 갱신, status snapshot |
| `/tk:next` | 다음 task 또는 사용자 action 하나 추천 |
| `/tk:do` | autopilot으로 task 하나 구현, decisions/API follow-up 갱신 |
| `/tk:steer` | user-steered execution 시작 |
| `/tk:steer-end` | steer 세션 종료, correction/reflect candidate 정리 |
| `/tk:gap` | requirements/task/API/blocker/readiness deep audit |
| `/tk:statusline` | steer/reflect indicator 표시 위치 설정 |

## 1. 준비

```text
/tk:prep <요구사항, 티켓, 메모, source>
```

하는 일:

1. 사용자 요구사항 정리
2. implementation context 초안 정리
3. `requirements.md` 생성/갱신
4. `implementation-context.md` 생성/갱신
5. requirements를 작은 task로 소분
6. `tasks.md` 생성/갱신
7. `tasks.index.json` 생성/갱신
8. `decisions.md` 초기화 또는 유지
9. 끝에서 light-gap sanity pass 수행

light-gap가 보는 것:
- requirement 누락/중복
- task granularity 과대/과소
- immediate clarification 필요 여부
- obvious shared blocker
- 바로 실행 가능한 task 존재 여부

하지 않는 일:
- Figma 같은 대형 MCP source raw dump 저장
- 대형 source 긴 요약 생성
- 현재 구현 전체 분석
- API capability taxonomy 생성
- deep gap report 생성
- 구현, commit, push, PR 생성

## source 접근 기록

Figma처럼 큰 MCP source는 raw 전체를 받거나 저장하지 않습니다. `inputs/sources/<kind>/<name>/access.md`에 URL, file key, frame id, node id, selection id, MCP tool, 다시 접근하는 방법만 index처럼 기록합니다. 작은 텍스트 source만 raw snapshot을 둘 수 있습니다.

Figma처럼 frame 단위 구조가 있는 source는 관련 frame을 각각 MCP로 새로 읽고, raw 대신 추출한 metadata/style 값만 `chunks/chunk-001.md`처럼 나눠 저장할 수 있습니다. chunk에는 frame id, node id, selection id, component name, text label, CSS/layout/spacing/color/typography 값, 관찰 목적만 둡니다.

CSS, layout, spacing, color, typography 같은 UI 요소를 확인할 때는 반드시 현재 MCP source를 새로 읽습니다. 오래된 access 기록이나 screenshot 요약만으로 style 값을 확정하지 않습니다.

## 2. 상태판 진입

```text
/tk:task
```

bare 호출은 현재 상태 요약과 사용법 가이드입니다.

예:

```text
task ledger 확인했습니다.
- work_id: search-ui
- active: 3, blocked: 1, review_required: 1
- reflect pending: 2

다음 추천: /tk:task list
```

지원 형태:

```text
/tk:task list
/tk:task status
/tk:task T-003
/tk:task add
/tk:task T-003 in_progress
/tk:task T-003 blocked auth contract unclear
/tk:task T-003 review_required
/tk:task T-003 done
```

### `task status`

`/tk:task status`는 old close/state/handoff 역할을 흡수합니다.

보여줄 것:
- active task summary
- review_required / blocked
- unresolved API follow-ups
- merge-ready 여부
- next action 1개
- decisions/reflect badge 상태

`/tk:task status`는 snapshot입니다. deeper audit은 `/tk:gap`가 담당합니다.

## 3. 다음 action 추천

```text
/tk:next
```

역할:
1. `tasks.index.json` 읽기
2. 실행 가능한 task 또는 사용자 action 하나 고르기
3. 연결된 blocker/API follow-up 표시
4. 다음 한 걸음만 제안

원칙:

```text
/tk:next는 전체 계획을 다시 만들지 않고 다음 한 걸음만 보여준다.
```

## 4. autopilot 실행

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
8. `decisions.md` 기록

핵심:
- `/tk:do`는 autopilot이다.
- 먼저 조사하고 correction-only prompt를 제시한다.
- `decisions.md`에 실제 판단 흔적을 남긴다.
- reflect는 optional 후보만 남긴다.

## API 정책

```text
TigerKit은 API 부재를 항상 개발 blocker로 취급하지 않는다.

API missing + safe mock
→ 개발 진행 가능
→ TK-API-* follow-up 생성/재사용
→ unresolved는 merge blocker

API missing + unsafe mock
→ blocked
```

강한 API Capability Key는 만들지 않습니다.

## 5. direct drive

```text
/tk:steer
```

역할:
1. 사용자가 운전대를 잡고 step-by-step으로 지시
2. agent는 그 지시를 따라 실행
3. correction/reuse/ask-rule을 `decisions.md`에 기록
4. reflect는 후보만 남김

중요:
- `steer`는 `do` 후처리 전용이 아니다.
- `do` 없이도 시작 가능하다.
- blank interview로 시작하지 않는다.
- autonomy mode처럼 행동하지 않는다.

종료:

```text
/tk:steer-end
```

종료 시:
- steer state clear
- correction/decision flush
- reflect candidate pending count 유지 가능
- 장문 retrospective 강제 없음

## 6. 점검

```text
/tk:gap
```

`/tk:gap`는 `prep`의 light-gap보다 깊은 audit입니다.

역할:
1. requirements 대비 누락 확인
2. task 상태 정리
3. `tasks.index.json`과 `tasks.md` 불일치 확인
4. API follow-up 중복 병합 후보 확인
5. shared blocker 확인
6. unresolved blocker 확인
7. merge/review readiness 판단

`/tk:gap`는 report-only입니다. 파일 수정, task 생성, follow-up 자동 병합, PR/merge/push/deploy를 하지 않습니다.

## 7. indicator 설정

```text
/tk:statusline
```

지원:

```text
/tk:statusline install
/tk:statusline remove
/tk:statusline trailing
/tk:statusline trailing on
/tk:statusline trailing off
```

badge 규칙:
- steer only -> `[🛞]`
- reflect pending only -> `[🪞 2]`
- both -> `[🛞 / 🪞 2]`
- none -> 숨김

기본은 trailing입니다. statusline은 token-saving 옵션입니다.

## 검증

TigerKit 저장소에는 package manager 기반 build/test/lint 설정이 없습니다. 명령, manifest, eval fixture를 수정한 뒤에는 다음 검증을 기본으로 실행합니다.

```bash
claude plugin validate .claude-plugin/plugin.json
claude plugin validate .
python3 -m json.tool evals/evals.json >/dev/null
git diff --check
```

`evals/evals.json`은 자동 실행 테스트가 아니라 fixture입니다. JSON 문법 검증과 수동 기대 동작 검토만 의미합니다.
