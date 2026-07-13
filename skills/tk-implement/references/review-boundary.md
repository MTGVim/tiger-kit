# 리뷰 경계

Review는 direct/delegated 선택과 별도인 선택적 품질 단계입니다. Implementor와 reviewer는 다른 역할이며 implementor를 독립 reviewer로 계산하지 마세요.

인증, 결제, 개인정보, 권한, 마이그레이션, 데이터 손실 가능성, 동시성, 공개 API, 대규모 구조 변경 또는 테스트하지 않은 고위험 코드에만 reviewer 한 명을 고려하세요.

최대 흐름:

```text
implementation
→ review once
→ fix once
→ regression verification
→ stop
```

Reviewer fan-out, reviewer의 재위임, 자동 재리뷰, 발견 사항이 없을 때 추가 reviewer 실행, review 결과를 이유로 한 전체 구현 재위임을 금지합니다. 수정이 필요하면 한 번 반영하고 기존 발견 사항과 관련 회귀를 검증한 뒤 종료하세요.
