---
name: tk-grill-me
description: "[user] 아이디어, 계획, 설계, 티켓 또는 RFC를 철저히 검증합니다. 사용자가 명시적으로 호출한 경우에만 사용합니다."
disable-model-invocation: true
argument-hint: "<아이디어, 계획, 설계, 티켓, RFC 또는 경로>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: mattpocock/skills
    upstream-skill: grill-me
    relationship: adapted
---

# 집중 검증

사용자가 이 스킬을 명시적으로 호출한 경우에만 사용하세요. 자동으로 활성화하지 마세요.

1. 요청과 제공된 자료를 읽고, 코드에서 확인 가능한 사실을 조사하세요.
2. 사용자만 결정할 수 있는 미해결 사항을 식별하세요.
3. 가장 영향이 큰 질문을 권고와 짧은 이유와 함께 하세요.
4. 답변을 반영하고 결정이 수렴할 때까지 한 번에 하나씩 질문을 반복하세요.

소스를 수정하거나, 명세/티켓을 생성하거나, 문서를 작성하거나, 이미 답한 질문을 반복하지 마세요.

내용이 있는 섹션만 사용해 마무리하세요: `## Decisions`, `## Assumptions`, `## Remaining risks`.
