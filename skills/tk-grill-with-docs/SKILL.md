---
name: tk-grill-with-docs
description: "[user] 결정을 철저히 검증하고 확정된 도메인 용어나 중대한 ADR을 기록합니다. 사용자가 명시적으로 호출한 경우에만 사용합니다."
disable-model-invocation: true
argument-hint: "<아이디어, 계획, 설계, 티켓, RFC 또는 경로>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: mattpocock/skills
    upstream-skill: grill-with-docs
    relationship: adapted
---

# 문서와 함께 집중 검증

사용자가 이 스킬을 명시적으로 호출한 경우에만 사용하세요. 자동으로 활성화하지 마세요.

도메인 문서를 유지하면서 한 번에 하나씩 질문하는 집중 검증을 수행하세요. `CONTEXT-MAP.md`, 영역의 `CONTEXT.md`, 루트의 `CONTEXT.md`, `docs/adr/`, 저장소의 기존 ADR 규칙 순서로 검색하세요. 용어나 조건을 충족하는 ADR을 반드시 기록해야 할 때만 파일을 생성하세요.

- 확정된 도메인 의미는 [컨텍스트 형식](references/context-format.md)을 사용해 작성하세요.
- [ADR 형식](references/adr-format.md)의 모든 기준을 충족할 때만 ADR을 작성하세요.
- 명세/티켓을 생성하거나, 코드를 구현하거나, 사소한 선택을 ADR로 만들지 마세요.

중요한 결정이 수렴하고 조건을 충족하는 용어/결정만 기록되면 완료합니다.
