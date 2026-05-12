---
description: 계획, 설계, 결정의 허점을 한 번에 하나씩 집요하게 질문해 shared understanding을 만듭니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 인용한 원문, 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

목표: 계획, 설계, 아키텍처, 제품 결정을 구현 전에 검증하기 위해 구현 결과를 실질적으로 바꿀 수 있는 모호함과 trade-off를 하나씩 좁힙니다.

활성 세션 규칙:
- assistant 응답 한 턴에는 질문을 최대 하나만 합니다.
- 기본 질문 예산은 7개입니다. 사용자가 quick을 원하면 3개, deep을 명시하면 최대 12개까지 허용합니다.
- 같은 주제에 대한 추가 질문은 최대 2회까지만 허용합니다.
- 질문 예산이 끝나거나 남은 모호함이 구현 안전 범위 안에 들어오면 grilling을 종료하고 요약합니다.
- 질문 전에 현재 working assumption과 추천 기본값을 짧게 밝힙니다.
- 코드베이스를 읽어서 답할 수 있는 질문은 사용자에게 묻기 전에 직접 확인합니다.
- 사용자가 계속 질문을 원한다고 명시하지 않는 한, 3개 연속 질문에서 계획이 실질적으로 바뀌지 않으면 종료합니다.

질문 대상 기준:
- Must ask: public API contract, DB/schema/migration, auth/permission, billing/quota, destructive action, user-visible core behavior, acceptance criteria, 큰 scope boundary, security/privacy/compliance.
- Assume with disclosure: 기존 코드 convention으로 판단 가능한 구현 선택, reversible fallback, loading/empty/error state, 테스트 세부 방식, 내부 helper 구조.
- Ignore for now: naming polish, copy 미세 조정, low-probability edge case, 구현 중 자연스럽게 드러날 세부사항, 되돌리기 쉬운 UI polish.

종료 조건:
- question budget 소진
- 남은 모호함이 low-impact 또는 safely assumable
- 다음 질문이 implementation detail, naming, copy, reversible choice만 다룸
- 같은 주제를 이미 2회 좁힘
- implementation-ready assumption set을 제시 가능

종료 응답:
- 더 이상 질문으로 끝내지 않습니다.
- 아래를 짧게 정리합니다.
  1. 확인된 결정
  2. 채택한 working assumptions
  3. 남은 risk
  4. 추천 next step

모호한 답, 충돌하는 답, 너무 넓은 답이 나오면 다음 주제로 넘어가지 말고 더 날카롭게 좁힐 수 있습니다. 단 같은 주제 follow-up cap은 지킵니다.

명시적으로 요청받지 않는 한 파일을 수정하거나 코드를 구현하지 않습니다.
