# 저비용 모델 인계

각 `AUD-*` `finding`은 다음 모델이나 `tk-prep`이 이 대화나 `audit session` 없이도
작업을 이해할 수 있도록 작성합니다.

- **컨텍스트 완결**: 정확한 경로/`symbol`, 현재 근거, 저장소 규칙, 관련 `exemplar`를 포함합니다.
- **경계**: `in/out` 범위, 가정, 의존성, 구체적인 `STOP/report-back` 조건을 포함합니다.
- **검증**: 명령, 예상 결과, `audited HEAD`, `drift` 처리 방법을 포함합니다.
- **안전**: `secret` 위치와 자격 증명 유형만 포함합니다. `values`, `cookies`, `tokens`, `private identity`는 복사하지 않습니다.

이 계약은 `tk-prep`이 실행 가능한 `Seed`를 만들 때 재사용할 증거를 준비할 뿐이며,
구현, 실행 단위, 원격 발행 권한을 부여하지 않습니다.
