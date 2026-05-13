# Output Contract

TigerKit command의 기본 채팅 응답은 artifact 자체가 아니라 receipt여야 합니다.

## 원칙

```text
Chat output is a receipt, not the artifact itself.
```

기본 응답은 아래 네 가지에 집중합니다.

1. outcome
2. user-relevant risk or decision
3. artifact paths
4. next action

## indicator

기본 indicator 규칙:

```text
[🛞]
[🪞 2]
[🛞 / 🪞 2]
```

의미:
- `[🛞]` = steer context active
- `[🪞 2]` = reflect candidate pending count 2
- `[🛞 / 🪞 2]` = 둘 다

기본 delivery는 trailing입니다. `/tk:statusline`으로 statusline 표시를 켤 수 있습니다.

## 기본 형식

```md
처리했습니다.

- task: T-004 검색 결과 empty state 구현
- API: TK-API-001 mock_api_contract, merge blocker
- 검증: 통과
- 기록: `.tigerkit/search/tasks.md`, `.tigerkit/search/tasks.index.json`, `.tigerkit/search/decisions.md`

다음 추천: /tk:task status
```

blocker가 있을 때:

```md
멈췄습니다. 구현 문제가 아니라 확인이 필요한 상태입니다.

- task: T-005
- 막힌 지점: auth permission contract 불명
- 상태: blocked
- 기록: `.tigerkit/search/tasks.md`

다음 추천: permission 기준 확인
```

status snapshot을 보여줄 때:

```md
상태 정리했습니다.

- active: 3
- review_required: 1
- merge-ready: NO
- blocker: TK-API-001 unresolved

다음 추천: /tk:next
```

## 기본 응답에서 피할 것

- 전체 `requirements.md`, `tasks.md`, `decisions.md` dump
- JSON-like key-value block
- 내부 metadata hash 나열
- 모든 task table
- 사용자가 요청하지 않은 verbose report
- 긴 retrospective 본문

## 세부 정보 원칙

- 상세 상태는 artifact path로 안내합니다.
- 사용자가 명시적으로 원할 때만 verbose report를 보여줍니다.
- command별 출력은 보통 3~6줄 안팎을 목표로 합니다.
- 다음 행동은 항상 1개 이상 명확히 제시합니다.
- unresolved `TK-API-*`는 task 실행 blocker인지 merge blocker인지 분리해 씁니다.
- `gap`는 deep audit이고, `task status`는 current snapshot임을 혼동하지 않습니다.
