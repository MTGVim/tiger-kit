구현 계획을 세우려면 먼저 다음 TIGAP 산출물을 읽어야 합니다.

```text
.gap/feature-login/normalized/source-packet.md
.gap/feature-login/analysis/gap-report.md
```

현재 요청에서는 `.gap/feature-login/analysis/gap-report.md`가 있다고 가정했지만, 원천 자료 정규화 파일인 `source-packet.md` 내용이 제공되지 않았고 이번 실행에서는 실제 `.gap` 파일을 만들거나 읽지 않는 조건입니다. 따라서 요구사항, 범위, 가정, 위험, 구현 갭, 검증 필요 사항을 확인하지 않은 상태에서 구현 계획을 추측해 작성하지 않겠습니다.

다음 중 하나로 진행해 주세요.

1. `/tigap:gap`을 먼저 실행해 `source-packet.md`와 `gap-report.md`를 준비합니다.
2. 이미 있는 `.gap/feature-login/normalized/source-packet.md`와 `.gap/feature-login/analysis/gap-report.md`의 내용을 제공해 주세요.
3. 최소한의 자료 수집을 위해 로그인 기능의 목표, 현재 동작, 원하는 동작, 알려진 갭, 제약 조건을 알려주세요.

승인 전이므로 `tasks.md` 작업 목록은 확정하지 않습니다.
