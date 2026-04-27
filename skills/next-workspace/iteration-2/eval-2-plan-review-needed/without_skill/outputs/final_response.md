현재 상태는 `source-packet.md` → `gap-report.md` → `implementation-plan.md`까지는 준비됐지만, 실행용 작업 목록인 `tasks.md`가 아직 없는 단계입니다.

다음 행동은 **구현을 시작하지 말고 `/tigap:gaplan` 단계로 돌아가 `tasks.md`를 생성하는 것**입니다.

권장 진행:

1. `.gap/feature-a/plan/implementation-plan.md`를 검토합니다.
2. 계획이 충분히 맞다면 `/tigap:gaplan`을 실행해 `.gap/feature-a/tasks.md`를 만듭니다.
3. `tasks.md`에 Ready 상태의 첫 작업이 생긴 뒤에만 `/tigap:go`로 구현을 시작합니다.

즉, 지금 바로 코딩하거나 `/tigap:go`를 실행할 단계는 아니며, 먼저 계획을 작업 목록으로 분해해야 합니다.