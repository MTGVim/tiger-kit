# Output Contract

TigerKit command의 기본 채팅 응답은 artifact 자체가 아니라 receipt입니다.

```text
Chat output is a receipt, not the artifact itself.
```

## 원칙

기본 응답은 아래 네 가지에 집중합니다.

1. outcome
2. evidence/risk/ambiguity
3. artifact paths
4. next action or required confirmation

전체 `requirements.md`, `gap.md`, `reflect.md`, `handoff.md`, `DESIGN.md`, `reuse-map.md`를 채팅에 dump하지 않습니다.

## prep receipt

```text
source index 기록 준비했습니다.
- branch: `feature__example`
- 기록: `.tigerkit/branches/feature__example/requirements.md`
- external sources: reference만 저장
- interview: raw와 interpretation 분리
- migration: root artifact 후보 표시
- CLAUDE.md: managed section이 없으면 이후 반영을 강하게 추천할 고우선 후보 표시

다음 추천: /tk:gap
```

## gap receipt

```text
gap 기록했습니다.
- branch: `feature__example`
- workflow step: `checkpoint-ready`
- baseline: `abc1234`
- recorded: `GAP-001`, `GAP-002`
- 기록: `.tigerkit/branches/feature__example/gap.md`

해야 할 일: high-impact ambiguity가 있으면 /tk:checkpoint로 계속 진행 가능 여부를 판단하고, 없으면 gap별 필요한 해결 기준에 따라 진행합니다.
```

## checkpoint receipt

```md
# Checkpoint

## 1. Current Status

현재 확인한 source와 task state를 짧게 기록합니다.

## 2. Blocking Questions

| ID | Question | Source | Why it matters | Consequence if wrong | Pause? |
|---|---|---|---|---|---|

## 3. User Decisions Needed

| ID | Decision | Options | Current assumption | Recommended handling | Pause? |
|---|---|---|---|---|---|

## 4. Assumptions Being Made

| ID | Assumption | Source | Risk | Consequence if wrong |
|---|---|---|---|---|

## 5. Not Verifiable Items

| ID | Item | Reason | Needed input | Current handling |
|---|---|---|---|---|

## 6. SOT / Policy Conflicts

| ID | Conflict | Sources | Current priority rule | Needs user decision? |
|---|---|---|---|---|

## 7. Self-resolvable Items

| ID | Item | Why self-resolvable | Safe action |
|---|---|---|---|

## 8. Items Not Safe to Auto-resolve

| ID | Item | Reason | Required next input |
|---|---|---|---|

## 9. Continue / Pause Judgment

Final status: `CLEAR | PROCEED_WITH_ASSUMPTIONS | PAUSE_FOR_USER_DECISION | BLOCKED_BY_ACCESS | NEED_VERIFICATION`

한 줄 설명.
```

## review receipt

finding이 있을 때:

```md
FINDINGS

1. [High] repo-wide reuse exploration 누락
- 위치: `commands/gap.md:...`
- 규칙: 새 module 생성 전 candidate/callsite inspection 필요
- evidence: `reuse-map.md` miss만 확인하고 새 component 생성을 전제함
- 영향: unnecessary new implementation, design-system drift 가능
- 필요한 수정: repo-wide exploration과 배제 근거 기록
```

finding이 없을 때:

```text
NO_FINDINGS
```

## reflect receipt

```text
reflection 기록했습니다.
- 기록: `.tigerkit/branches/feature__example/reflect.md`
- recorded only: `reflect.md`
- pending escalation: `CLAUDE.md` managed section 추가 강한 추천, `reuse-map.md`

질문: 위 후보를 실제 반영할까요?
```

## handoff-write receipt

```text
handoff 기록했습니다.
- 기록: `.tigerkit/branches/feature__example/handoff.md`
- baseline: `abc1234`
- artifact map: requirements/gap/reflect 상태 포함
- open gaps: 2
- ambiguity: 1

다음 추천: 다음 세션에서 /tk:handoff-read
```

## handoff-read receipt

```text
handoff 읽었습니다.
- handoff: `.tigerkit/branches/feature__example/handoff.md`
- baseline match: yes
- artifact map: requirements/gap/reflect 확인
- stale risk: 없음
- 확인 필요: 1개

next safe action: 사용자 확인 후 GAP-001 관련 파일 inspect
```

## gap blocked receipt

```text
gap 기록을 시작하지 않았습니다.
- workflow step: `baseline-check`
- blocked: working tree not clean
- staged: yes
- unstaged: no
- untracked: yes
- 해야 할 일: staged 변경은 commit하고, 나머지 변경은 정리하거나 함께 commit한 뒤 rerun `/tk:gap`
```

## protected branch receipt

```text
기록하지 않았습니다.
- workflow step: `branch-check`
- reason: protected branch `main`
- 해야 할 일: feature branch로 switch/create
- artifact: 변경 없음
```

## detail 원칙

- 상세 내용은 artifact path로 안내합니다.
- 사용자가 명시적으로 원할 때만 verbose report를 보여줍니다.
- command별 출력은 보통 3~6줄 안팎을 목표로 합니다.
- 다음 행동은 하나 이상 명확히 제시합니다.
- `/tk:gap` receipt는 `workflow step`과 `해야 할 일`을 포함합니다.
- `/tk:checkpoint`는 required sections와 final status를 포함합니다.
- `/tk:review`는 finding별 severity, 위치, 규칙, evidence, 영향, 필요한 수정을 포함하거나 `NO_FINDINGS`만 출력합니다.
- evidence, interpretation, decision, suggestion을 섞지 않습니다.
- ambiguity를 resolved처럼 말하지 않습니다.
- `recorded only`, `applied`, `pending escalation`, `skipped`를 구분합니다.

## 피할 것

- JSON-like metadata dump
- 전체 artifact dump
- 실행 대기열 생성
- 내부 진행 상태 노출
- `/tk:reflect`를 default next command로 추천
- `/tk:review`에서 preference 수준 wording을 blocking finding으로 격상
- inaccessible SOT-dependent item을 evidence 없이 `Match`로 표시
- source summary를 requirement처럼 확정하는 문구
- 사용자가 요청하지 않은 verbose retrospective
- `reflect.md` 기록과 durable artifact 반영을 같은 outcome처럼 말하기
