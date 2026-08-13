# 인계 계획 적용

소스 snapshot `03369ee6d7cafbfcecc4346539b05b3dc0a603bb`의
`shadcn/improve`에서 변형했습니다. upstream template의 품질 기준은 두 번째
계획 lifecycle로 복사하지 않고 각 `AUD-*` finding에 적용합니다.

저비용 실행자나 `tk-prep`은 self-contained context, 정확한 경로와 symbol,
현재 상태 근거, 저장소 규칙, 예상 결과가 있는 명령, 엄격한 in/out 경계,
가정, 명시적인 STOP/report-back 조건을 받아야 합니다. audited HEAD를 finding에
표시하고 drift 처리 방법을 명시합니다.

`tk-audit`는 `plans/`, 구현 코드, 실행 단위, 원격 이슈를 작성하지 않습니다.
실행 가능한 작업 계약과 AC, 검증 계획은 필요할 때 `tk-prep`이 현재 근거를 다시 읽어
`.tigerkit/seed.md`에 준비합니다.
