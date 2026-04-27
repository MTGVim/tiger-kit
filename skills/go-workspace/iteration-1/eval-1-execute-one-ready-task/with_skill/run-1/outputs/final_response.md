가정 상태에서는 `.gap/feature-toast/tasks.md`에 Ready 작업이 여러 개 있더라도 첫 번째 Ready 작업 하나만 선택해 진행합니다.

다만 이번 평가는 실제 `.gap` 파일을 읽거나 수정하지 않는 조건이므로, 구현과 산출물 갱신은 수행하지 않았습니다. 실제 실행이라면 다음 순서로 처리합니다.

1. `.gap/feature-toast/plan/implementation-plan.md`와 `.gap/feature-toast/tasks.md`를 확인합니다.
2. Ready 섹션의 첫 번째 미완료 작업 하나만 `In Progress`로 표시합니다.
3. 해당 작업에 필요한 파일과 인접 구현, 테스트, 기존 패턴을 확인합니다.
4. 선택한 작업 범위 안에서만 코드를 수정합니다.
5. 가능한 검증 명령을 실행하고 결과를 기록합니다.
6. 완료된 작업을 `Done`으로 이동하고 `.gap/feature-toast/execution-log.md`에 작업명, 변경 파일, 검증 결과, 진행률, 다음 작업을 기록합니다.

진행률은 실제 `tasks.md`를 수정하지 않았기 때문에 계산하지 않았습니다.

다음 작업: 실제 실행 환경에서는 `.gap/feature-toast/tasks.md`의 첫 번째 Ready 작업을 이어서 처리하면 됩니다.