---
name: tk-implement
description: "[user] 요청받은 코드 변경을 구현하고 검증합니다. 사용자가 명시적으로 호출했을 때만 사용하세요."
disable-model-invocation: true
argument-hint: "<요청, 티켓 또는 명세>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: mattpocock/skills
    upstream-skill: implement
    relationship: adapted
---

# 구현

사용자가 이 스킬을 명시적으로 호출했을 때만 사용하세요. 자동으로 활성화하지 마세요.

`understand → inspect → implement → verify → report` 순서를 따르세요. 정보 출처의 우선순위는 현재 요청, 대화에서 확인된 결정, 관련 `.tigerkit/tickets.md`, 관련 `.tigerkit/spec.md`, 저장소 지침, 코드/테스트 순입니다. 기존 파일이라고 해서 자동으로 관련 있는 것은 아닙니다.

기본적으로 직접 구현하세요. 명확히 격리할 수 있거나 실제로 독립적인 병렬 작업일 때만 위임하세요. 위임을 중첩하거나 하위 에이전트가 사용자 호출형 TigerKit 스킬을 호출하게 해서는 안 됩니다. 유용한 경우 설치된 규율을 적용하되, 없다고 작업을 막지는 마세요. [위임](references/delegation.md)과 [리뷰 경계](references/review-boundary.md)를 참고하세요.

변경에 맞는 검증을 선택하세요. 실패를 변경 관련, 기존 문제, 환경 문제 또는 검증 불가로 분류하세요. 다른 사용자 호출형 스킬을 자동으로 실행하거나 커밋, 푸시, PR 생성 또는 병합을 하지 마세요.

`## Changed`, `## Verification`, 비어 있지 않은 `## Remaining risks`를 보고하고, 파일 목록만이 아니라 동작을 설명하세요.
