# 사용법

## 언어

명령은 사용자에게 한글로 답하고 작업 산출물도 한글로 작성합니다. URL, 코드, 명령어, 경로, 식별자, commit hash는 원문 그대로 유지할 수 있습니다.

## 핵심 모델

```text
TigerKit = source-of-truth index + reproducible gap record + session reflection + operational handoff
```

TigerKit은 LLM의 장기 절차 기억에 실행 순서나 진행 상태를 맡기지 않습니다.

권장 순서:

```text
/tk:prep
/tk:gap
/tk:reflect
/tk:handoff-write
```

이전 세션의 `handoff.md`가 있고 현재 feature branch가 확인되면 이어받는 세션은 `/tk:handoff-read`로 시작합니다. detached HEAD나 `main`, `master`, `develop`이면 먼저 feature branch 전환을 안내합니다.

## Branch-local artifacts

TigerKit working material은 branch별로 격리합니다.

```text
.tigerkit/
  branches/
    feature__example/
      requirements.md
      gap.md
      reflect.md
      handoff.md
```

`{escaped-branch}`는 현재 git branch name을 collision-safe하게 path-safe 변환한 값입니다. ASCII letter, digit, `.`, `_`, `-`는 그대로 두고 다른 byte는 `~HH` uppercase hex로 encode합니다. 예: `feature/foo` → `feature~2Ffoo`, `feature__foo` → `feature__foo`.

Root-level `.tigerkit/requirements.md`, `.tigerkit/gap.md`, `.tigerkit/reflect.md` are deprecated artifacts. TigerKit commands should treat them as migration candidates, not active write targets.

TigerKit branch-local artifacts are not written on detached HEAD or protected branches (`main`, `master`, `develop`). Switch to a feature branch before running write commands.

## Command Surface

| Command | 역할 |
| --- | --- |
| `/tk:prep` | source-of-truth reference와 직접 사용자 인터뷰를 branch-local requirements index에 기록 |
| `/tk:gap` | branch-local indexed SOT reference와 clean HEAD baseline을 비교해 evidence-based gap 기록 |
| `/tk:reflect` | session을 재구성해 branch-local reflection을 기록하고 durable artifact 격상 후보 제안 |
| `/tk:handoff-write` | 다음 모델/세션을 위한 branch-local continuation contract 작성 |
| `/tk:handoff-read` | handoff와 artifact map을 읽고 현재 repo 상태와 stale risk 확인 |

## 일반 대화에서 TigerKit 유도

사용자가 slash command를 직접 입력하지 않아도, 일반 대화에 external source나 gap 비교 요청이 들어오면 TigerKit command contract를 명시적으로 강하게 권장합니다.

권장 기준:

- Jira, Figma, Confluence, ClickUp, GitHub issue/PR, API docs, MCP resource, backend repo, source path가 언급되면 `/tk:prep`로 reference를 먼저 기록하도록 강하게 권장
- "backend API와 맞는지 봐줘"처럼 구현과 외부 기준을 대조하려는 요청이면 backend repo, branch basis, lookup commit, open PR review scope를 SOT candidate로 잡아 `/tk:prep`에 기록하도록 강하게 권장
- "gap 봐줘", "요구사항 대비 빠진 것 찾아줘"처럼 비교 기반 누락 확인 요청이면 `/tk:gap`을 권장
- 세션 종료 시점까지 SOT candidate가 정리되지 않았으면 `/tk:reflect`에서 next safe action을 `/tk:prep`로 남기도록 권장

## 1. Source index

```text
/tk:prep <요구사항 source, 티켓, Figma, PRD, issue, 직접 인터뷰>
```

하는 일:

1. 현재 branch가 safe feature branch인지 확인
2. 외부 source와 직접 사용자 인터뷰를 분리
3. 외부 source는 reference만 저장
4. 현재 session 사용자 인터뷰는 raw text에 가깝게 저장
5. derived interpretation은 별도 표시
6. ambiguity를 숨기지 않고 기록
7. root artifact가 있으면 migration 후보로 표시
8. `CLAUDE.md` TigerKit managed section이 없으면 이후 `/tk:reflect`에서 실제 반영을 강하게 추천해야 할 고우선 후보로 표시

하지 않는 일:

- external source 내용을 local requirement로 재작성
- source summary를 official requirement처럼 저장
- 실행 대기열 생성
- `CLAUDE.md`, `DESIGN.md`, `reuse-map.md` 업데이트
- root-level `.tigerkit/requirements.md` 새로 쓰기
- 구현, commit, push, PR 생성

권장 구조:

```md
# TigerKit 요구사항 인덱스

## 외부 소스 참조

- PRD 참조: https://...
- Figma 참조: https://...
- GitHub Issue 참조: https://...

## 사용자 인터뷰 요구사항

### 원문

> 사용자 원문에 가까운 내용

### 파생 해석

- 명시적으로 파생 해석임을 표시

## 모호성

- 확인되지 않은 점
```

## 2. Gap record

```text
/tk:gap
```

하는 일:

1. 현재 branch가 safe feature branch인지 확인
2. `.tigerkit/branches/{escaped-branch}/requirements.md`에서 compared SOT reference 확인
3. code baseline 확인
4. working tree가 clean하지 않으면 commit 또는 정리 요청
5. 관련 code path inspection
6. evidence와 interpretation 분리
7. `.tigerkit/branches/{escaped-branch}/gap.md`에 gap 기록

baseline 원칙:

```text
feature branch + clean working tree + HEAD commit hash = required baseline
```

`/tk:gap`은 clean HEAD commit만 baseline으로 사용합니다. staged, unstaged, untracked 변경이 하나라도 있으면 gap record를 시작하지 않습니다. 특히 staged 변경은 commit hash가 없으므로 먼저 commit하거나 working tree를 정리한 뒤 다시 실행해야 합니다.

`/tk:gap`은 기능 구현 누락만이 아니라 design consistency, hierarchy, density, component reuse risk, design-system drift, nearby screen pattern mismatch도 gap으로 기록할 수 있습니다. Figma 등 design SOT와 비교할 때는 의미가 비슷해 보여도 fixture 표현 차이, label/copy 차이, date/time/number/currency/line break format 차이를 중대한 gap 사유로 봅니다. 현재 구현 증거가 부족하면 문제 화면의 DOM, accessibility tree, screenshot, rendered text, style token evidence를 확보하거나 사용자에게 요청할 수 있습니다. `reuse-map.md`는 cache-0 discovery aid일 뿐 SOT가 아니며, 거기에 항목이 없다는 사실만으로 새 구현을 정당화할 수 없습니다. 새 component/hook/util/mapper/API client/layout primitive/UI pattern 생성 전에는 repo-wide exploration이 필요하고, 공통 모듈 수정 전에는 callsite impact analysis와 명시적 사용자 승인이 필요합니다.

gap은 evidence record입니다.

```md
## GAP-001 — Tooltip copy 불일치

유형: mismatch
상태: open

### 비교한 SOT
- Source: PRD
- 참조: https://...
- 섹션: Tooltip copy

### 비교한 코드
- Baseline: abc1234
- 확인한 파일:
  - src/...

### 증거
SOT:
> short exact excerpt 또는 pointer

Code:
> short exact excerpt 또는 pointer

### 발견 사항
PRD copy와 구현 tooltip copy가 다릅니다.

### 해석
implementation drift로 보입니다.

### 필요한 해결 기준
사용자 확인 또는 code update 필요.
```

하지 않는 일:

- gap을 실행 대기열로 변환
- ambiguity를 조용히 해소
- `CLAUDE.md`, `DESIGN.md`, `reuse-map.md` 업데이트
- root-level `.tigerkit/gap.md` 새로 쓰기
- 구현, commit, push, PR 생성

## 3. Reflection

```text
/tk:reflect
```

하는 일:

1. 현재 branch가 safe feature branch인지 확인
2. 현재 대화 context review
3. explicit user confirmation 확인
4. branch-local `requirements.md`, `gap.md`, `handoff.md` review
5. 최근 diff/commit review
6. durable learning과 one-off correction 분리
7. `.tigerkit/branches/{escaped-branch}/reflect.md` 갱신
8. `CLAUDE.md`, `MEMORY.md`, `DESIGN.md`, `reuse-map.md` escalation 후보 제안
9. `CLAUDE.md` managed section이 없으면 약한 후보가 아니라 강한 반영 추천 상태로 명시
10. 실제 반영할지 사용자에게 질문

reflect는 현재 대화 context를 primary source로 사용합니다. artifact와 git evidence는 보조 근거입니다. 대화 context에 없는 내용은 추측하지 않고 `확인 불가`로 둡니다.

`DESIGN.md`가 없으면 새로 만들지 않습니다. `DESIGN.md`에 넣을 derived design knowledge가 있으면 사용자에게 초기화 필요를 알립니다.

승인 전에는 `CLAUDE.md`, `MEMORY.md`, `DESIGN.md`, `reuse-map.md`를 수정하지 않습니다.

## 4. Handoff write

```text
/tk:handoff-write
```

하는 일:

1. 현재 branch가 safe feature branch인지 확인
2. 현재 branch, HEAD, working tree 상태 기록
3. requirements/gap/reflect artifact map 작성
4. open gap, resolved gap, ambiguity, not confirmed 항목 분리
5. next safe action과 do-not-do 기록
6. `.tigerkit/branches/{escaped-branch}/handoff.md` 작성

handoff는 다음 모델/세션용 continuation contract입니다. task queue가 아닙니다.

## 5. Handoff read

```text
/tk:handoff-read
```

하는 일:

1. 현재 branch가 safe feature branch인지 확인
2. branch-local handoff 읽기
3. handoff baseline과 현재 branch/HEAD 비교
4. artifact map에 있는 requirements/gap/reflect 확인
5. `CLAUDE.md`, `DESIGN.md`, `reuse-map.md`가 있으면 확인
6. matched, stale, missing, conflict, needs-confirmation 분리
7. 구현하지 않고 next safe action 제시

handoff를 source of truth처럼 맹신하지 않습니다. 현재 repo 상태와 artifact freshness를 먼저 확인합니다.

## Evidence Rule

중요 claim은 아래 중 하나에 근거해야 합니다.

- external SOT reference
- direct user interview text
- code path
- commit hash
- observed diff
- explicit user confirmation
- gap record
- derived artifact clearly marked as derived

항상 분리합니다.

```text
Evidence = directly observed
Interpretation = inferred from evidence
Decision = confirmed by user or SOT
Suggestion = proposed, not confirmed
Not Confirmed = 아직 확인하지 않음
Ambiguity = 확인했지만 source가 결론을 지지하지 않거나 source끼리 충돌
```

## Ambiguity Rule

source가 결론을 지지하지 않으면 추측하지 않습니다.

```text
record gap, not work plan
ask user, do not guess
```

## Durable context intake

명령이 요구하는 범위 안에서 아래 파일을 적극 활용합니다.

1. `CLAUDE.md` / project instructions
2. `.tigerkit/branches/{escaped-branch}/handoff.md`, if present
3. `.tigerkit/branches/{escaped-branch}/requirements.md`
4. `.tigerkit/branches/{escaped-branch}/gap.md`
5. `.tigerkit/branches/{escaped-branch}/reflect.md`
6. `DESIGN.md`, if present
7. `reuse-map.md`, if present
8. code inspection

`DESIGN.md`와 `reuse-map.md`는 derived repo-level knowledge입니다. 외부 SOT를 대체하지 않습니다. 현재 code 또는 SOT와 충돌하면 resolved처럼 다루지 말고 기록하거나 사용자에게 확인합니다.

## 검증

TigerKit 저장소에는 package manager 기반 build/test/lint 설정이 없습니다. 명령, manifest, eval fixture를 수정한 뒤에는 다음 검증을 기본으로 실행합니다.

```bash
claude plugin validate .claude-plugin/plugin.json
claude plugin validate .
python3 -m json.tool evals/evals.json >/dev/null
git diff --check
```

`evals/evals.json`은 자동 실행 테스트가 아니라 fixture입니다. JSON 문법 검증과 수동 기대 동작 검토만 의미합니다.
