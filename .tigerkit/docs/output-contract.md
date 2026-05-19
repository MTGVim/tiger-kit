# TigerKit 운영 Output Contract

이 문서는 `.tigerkit/docs/` 아래 TigerKit 운영 문서 중 receipt/output contract를 정의합니다. 사용 흐름은 `.tigerkit/docs/usage.md`, 산출물 위치는 `.tigerkit/docs/artifact-layout.md`를 기준으로 봅니다.

TigerKit command의 기본 채팅 응답은 artifact 자체가 아니라 receipt입니다.

```text
Chat output is a receipt, not the artifact itself.
```

## 원칙

기본 응답은 아래 네 가지에 집중합니다.

1. outcome
2. evidence/risk/ambiguity
3. artifact paths
4. natural-language next action or required confirmation

전체 `requirements.md`, `gap.md`, `reflect.md`, `handoff.md`, `DESIGN.md`, `COMPONENT_REUSE_MAP.md`를 채팅에 dump하지 않습니다. `reuse-map.md`는 legacy alias/migration candidate로 언급할 때만 다룹니다.

## prep receipt

```text
source index 기록 준비했습니다.
- branch: `feature__example`
- 기록: `.tigerkit/branches/feature__example/requirements.md`
- external sources: reference와 access status만 저장
- pending SOT: 접근 불가 source는 fallback 요청
- local asset: binding visual SOT는 `./docs/assets/sot/...` 경로 권장
- interview: raw와 interpretation 분리

해야 할 일: 접근 불가 SOT가 있으면 파일 업로드, 로컬 경로, screenshot/export, pasted content를 제공해 주세요.
```

## gap receipt

```text
gap 기록했습니다.
- branch: `feature__example`
- baseline: `abc1234`
- recorded: `GAP-001`, `GAP-002`
- SOT coverage: partial, `SOT-IMG-001` pending_user_input
- 기록: `.tigerkit/branches/feature__example/gap.md`

해야 할 일: 접근 불가 binding SOT가 있으면 file, local path, screenshot/export, pasted content를 요청해 주세요.
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
- evidence: `COMPONENT_REUSE_MAP.md` miss만 확인하고 새 component 생성을 전제함
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
- pending SOT: `SOT-IMG-001` auth_required, fallback 필요
- pending escalation: `CLAUDE.md` managed section 추가 강한 추천, `COMPONENT_REUSE_MAP.md`

질문: 위 escalation 후보를 실제 반영할까요?
SOT fallback 필요: `SOT-IMG-001` 파일 업로드, 로컬 경로, screenshot/export, pasted content를 제공해 주세요.
```

## handoff-write receipt

```text
handoff 기록했습니다.
- 기록: `.tigerkit/branches/feature__example/handoff.md`
- baseline: `abc1234`
- artifact map: requirements/gap/reflect 상태 포함
- open gaps: 2
- ambiguity: 1
```

## handoff-read receipt

```text
handoff 읽었습니다.
- handoff: `.tigerkit/branches/feature__example/handoff.md`
- baseline match: yes
- artifact map: requirements/gap/reflect 확인
- stale risk: 없음
- 확인 필요: 1개
```

## gap blocked receipt

```text
gap 기록을 시작하지 않았습니다.
- workflow step: `baseline-check`
- blocked: working tree not clean
- staged: yes
- unstaged: no
- untracked: yes
- 해야 할 일: staged 변경은 commit하고, 나머지 변경은 정리하거나 함께 commit한 뒤 clean baseline에서 gap 분석을 다시 요청하세요.
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
- 다음 행동은 command-style recommendation이 아니라 자연어로 짧게 제시합니다.

## 운영 메모

세부 정책과 분류 규칙은 `CLAUDE.md`를 기준으로 봅니다.
