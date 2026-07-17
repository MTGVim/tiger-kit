---
name: tk-grill-me
description: "[user] 아이디어, 계획, 설계, 티켓 또는 RFC를 사실 조사 후 한 번에 한 질문씩 검증합니다. 사용자가 명시적으로 호출한 경우에만 사용합니다."
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

## 계약

사용자의 명시적 답변 또는 확인 가능한 근거 없이 사용자 결정을 확정하거나 적용하지 마세요. 침묵, 다음 질문으로의 진행, 과거의 유사한 답변은 동의가 아닙니다. 사실 근거는 사용자를 대신해 선택을 승인하지 않습니다.

사용자가 멈추면 완료로 보고하지 말고 `pending`(답변 대기), `aborted`(사용자 중단), `Blocked`(충돌 또는 필수 근거 부족) 중 하나로 보고하세요. 소스를 수정하거나 문서·티켓·ADR을 만들지 마세요.

## 🔴 CHECKPOINT · 🛑 STOP 사용자 결정 경계

권고 질문 하나를 제시한 뒤 사용자 답변을 받기 전에는 다음 질문, 결정 반영, 문서 수정을 진행하지 마세요. 답변이 없으면 `pending`, 답변과 근거가 충돌하면 `Blocked`로 멈추세요.

1. 요청과 제공된 자료를 읽으세요.
2. 코드와 환경에서 확인 가능한 사실을 먼저 조사하세요.
3. 사용자만 결정할 수 있는 미해결 사항을 식별하세요.
4. 가장 영향이 큰 질문 하나를 `권고 / 근거 / 질문` 세 필드로 제시하세요.
5. 답변을 반영하고 결정이 수렴할 때까지 한 번에 하나씩 반복하세요.
6. 이미 답한 질문을 반복하지 마세요.
7. 합의 전에 구현하거나 문서를 수정하지 마세요.

같은 domain 용어가 서로 다른 의미로 쓰이거나 인접 개념을 구분해야 결정할 수 있다면 그 의미를 질문하세요. 확정된 용어는 이후 `tk-to-spec` 결과에 포함할 수 있지만, 이 스킬은 `CONTEXT.md`, glossary, domain 문서 또는 ADR을 자동으로 만들거나 수정하지 않습니다.

내용이 있는 섹션만 사용해 마무리하세요: `## Decisions`, `## Assumptions`, `## Remaining risks`, `## Receipt`. Receipt에는 결정, `confirmed | pending | aborted | Blocked`, 사용자 답변 또는 근거 위치, 적용 여부를 기록하세요.

## DO NOT / ANTI-PATTERNS

- 사용자의 결정을 대신 확정하거나 한 번에 여러 결정을 질문하지 마세요.
- 사실 조사만으로 승인이나 침묵을 동의로 해석하지 마세요.
- 합의 전에 spec, ticket, ADR 또는 소스를 수정하지 마세요.
