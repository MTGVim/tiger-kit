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
4. next action

전체 `requirements.md`, `gap.md`, `reflect.md`, `DESIGN.md`, `reuse-map.md`를 채팅에 dump하지 않습니다.

## prep receipt

```text
source index 갱신했습니다.
- 기록: `.tigerkit/requirements.md`
- external sources: reference만 저장
- interview: raw와 interpretation 분리
- ambiguity: 확인 필요 항목 기록

다음 추천: /tk:gap
```

## gap receipt

```text
gap 기록했습니다.
- baseline: `abc1234`
- inspected files: source 비교에 필요한 파일
- recorded: `GAP-001`, `GAP-002`
- 기록: `.tigerkit/gap.md`

다음 추천: /tk:reflect
```

## reflect receipt

```text
reflection 정리했습니다.
- 기록: `.tigerkit/reflect.md`
- primary source: current conversation context
- durable learning: evidence 있는 항목만 분리
- one-off correction: session 한정으로 유지
- design note: 조건부 표시. `DESIGN.md`가 없고 넣을 derived design knowledge가 있을 때만 초기화 필요 알림

다음 추천: 제안된 derived knowledge 검토
```

## detail 원칙

- 상세 내용은 artifact path로 안내합니다.
- 사용자가 명시적으로 원할 때만 verbose report를 보여줍니다.
- command별 출력은 보통 3~6줄 안팎을 목표로 합니다.
- 다음 행동은 하나 이상 명확히 제시합니다.
- evidence, interpretation, decision, suggestion을 섞지 않습니다.
- ambiguity를 resolved처럼 말하지 않습니다.

## 피할 것

- JSON-like metadata dump
- 전체 artifact dump
- 실행 대기열 생성
- 내부 진행 상태 노출
- source summary를 requirement처럼 확정하는 문구
- 사용자가 요청하지 않은 verbose retrospective
