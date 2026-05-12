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

## 기본 형식

```md
완료했습니다.

- 처리: 실행 가능한 task 3개 완료
- 검증: 통과
- 상세 기록: `.tigerkit/{work_id}/tasks.md`, `.tigerkit/{work_id}/gap.md`

다음 추천: /tk:close
```

blocker가 있을 때:

```md
멈췄습니다. 구현 문제가 아니라 확인이 필요한 상태입니다.

- 완료: task 2개
- 막힌 지점: API contract 확인 필요
- 상세 기록: `.tigerkit/{work_id}/tasks.md`

다음 추천: /tk:plan
```

## 기본 응답에서 피할 것

- 전체 `requirements.md`, `gap.md`, `plan.md`, `tasks.md` dump
- JSON-like key-value block
- 내부 metadata hash 나열
- 모든 task table
- commit hash 장황한 나열
- TDD/sub-agent routing 상세 설명
- 사용자가 요청하지 않은 verbose report

## 세부 정보 원칙

- 상세 상태는 artifact path로 안내합니다.
- 사용자가 명시적으로 원할 때만 verbose report를 보여줍니다.
- command별 출력은 보통 3~6줄 안팎을 목표로 합니다.
- 내부 상태 enum을 단독으로 던지지 않습니다.
- 다음 행동은 항상 1개 이상 명확히 제시합니다.
