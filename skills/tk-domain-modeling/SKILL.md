---
name: tk-domain-modeling
description: "[auto] 도메인 언어를 정교하게 다듬고, 개념 경계를 검증하며, 오래 유지할 용어나 중대한 결정만 기록합니다."
user-invocable: false
metadata:
  tigerkit:
    kind: model-invoked
    origin: mattpocock/skills
    upstream-skill: domain-modeling
    relationship: adapted
---

# 도메인 모델링 원칙

용어나 도메인 경계가 모호할 때 사용합니다.

- 기존 용어집/컨텍스트 파일과 코드에서 의미가 충돌하는지 확인하세요.
- 구체적인 경계 사례로 개념을 검증하고 인접한 용어를 구분하세요.
- 도메인 의미만 기록하고, 구현 구조는 용어집에 넣지 마세요.
- 선택을 되돌리기 어렵고, 맥락 없이는 의외이며, 실질적인 대안이 있었던 경우에만 ADR을 제안하세요.
- 설계를 구현하지 마세요.

[용어 및 ADR 기준](references/terms-and-adrs.md)을 참고하세요. 관련 어휘와 결정 경계가 모호하지 않으면 완료합니다.
