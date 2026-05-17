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
- baseline: `abc1234`
- recorded: `GAP-001`, `GAP-002`
- 기록: `.tigerkit/branches/feature__example/gap.md`

다음 추천: /tk:reflect
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

## protected branch receipt

```text
기록하지 않았습니다.
- reason: protected branch `main`
- required action: feature branch로 switch/create
- artifact: 변경 없음
```

## detail 원칙

- 상세 내용은 artifact path로 안내합니다.
- 사용자가 명시적으로 원할 때만 verbose report를 보여줍니다.
- command별 출력은 보통 3~6줄 안팎을 목표로 합니다.
- 다음 행동은 하나 이상 명확히 제시합니다.
- evidence, interpretation, decision, suggestion을 섞지 않습니다.
- ambiguity를 resolved처럼 말하지 않습니다.
- `recorded only`, `applied`, `pending escalation`, `skipped`를 구분합니다.

## 피할 것

- JSON-like metadata dump
- 전체 artifact dump
- 실행 대기열 생성
- 내부 진행 상태 노출
- source summary를 requirement처럼 확정하는 문구
- 사용자가 요청하지 않은 verbose retrospective
- `reflect.md` 기록과 durable artifact 반영을 같은 outcome처럼 말하기
