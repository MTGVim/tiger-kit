---
name: tk-tdd
description: "[auto] 레드-그린-리팩터링이 신뢰도를 높이는 유용한 동작 경계에서 테스트 주도 개발을 사용합니다."
user-invocable: false
metadata:
  tigerkit:
    kind: model-invoked
    origin: mattpocock/skills
    upstream-skill: tdd
    relationship: adapted
---

# TDD 규율

의미 있는 테스트 경계가 있을 때만 사용하세요.

1. 가장 유용한 공개 동작 경계를 선택하세요.
2. 수직 슬라이스 테스트 하나를 작성하고 실행해 레드 상태를 확인하세요.
3. 최소한의 동작을 구현하고 실행해 그린 상태를 확인하세요.
4. 동작을 바꾸지 않고 리팩터링하세요.

내부 구현이 아니라 동작을 테스트하고, 테스트만을 위한 프로덕션 코드 왜곡은 피하세요. 유용한 경계가 없으면 TDD를 강제하지 마세요. 레드 명령/결과, 그린 명령/결과, 구현한 동작을 보고하세요.
