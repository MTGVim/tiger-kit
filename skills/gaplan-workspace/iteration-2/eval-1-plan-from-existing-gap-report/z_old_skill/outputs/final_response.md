구현 계획 초안 작성에 들어가려면 먼저 기존 TIGAP 산출물을 확인해야 합니다.

필수 입력으로 다음 두 파일이 필요합니다.

```text
.gap/feature-login/normalized/source-packet.md
.gap/feature-login/analysis/gap-report.md
```

현재 요청에서는 `analysis/gap-report.md`가 있다고 가정했지만, 입력 파일을 제공받지 않았고 이 실행에서는 `.gap` 산출물을 실제로 읽거나 생성하지 않는 조건이므로 구현 계획 내용을 확정해서 작성할 수 없습니다.

다음 중 하나로 진행해 주세요.

1. `.gap/feature-login/normalized/source-packet.md`와 `.gap/feature-login/analysis/gap-report.md` 내용을 제공해 주세요.
2. 아직 갭 산출물이 준비되지 않았다면 먼저 다음 명령으로 갭 분석을 생성해 주세요.

```text
/tigap:gap
```

승인 전 단계이므로 `tasks.md` 작업 목록은 확정하지 않겠습니다. 갭 보고서와 source packet을 확인한 뒤에는 `implementation-plan.md` 초안 형태로 목표, 범위, non-goal, 가정, 의존성, 현재 구현 요약, 작업 분해, 검증 계획, 롤백 계획, 검토 체크리스트를 정리하고 사용자 검토를 기다리겠습니다.
