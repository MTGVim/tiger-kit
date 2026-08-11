# 인계 계획 적용

소스 snapshot `03369ee6d7cafbfcecc4346539b05b3dc0a603bb` 의
`shadcn/improve` 에서 변형했다. upstream template의 품질 기준은 두 번째
계획 생명주기로 복사하지 않고 각 `AUD-*` finding에 적용한다.

저비용 실행자는 self-contained 컨텍스트, 정확한 경로와 symbol, 현재 상태
발췌 또는 근거, 저장소 규칙, 예상 결과가 있는
명령, 엄격한 in/out 경계, 가정, 명시적인 STOP/report-back
조건을 받아야 한다. audited HEAD를 finding에 표시하고 drift 처리 방법을
명시한다. 의존성과 유지보수 메모는 근거를 벗어나지 않게 한다.

`tk-audit` 는 절대 `plans/`, 구현 코드, 단위, 원격 이슈를 작성하지
않는다. downstream R/AC, 실행 단위, 결정은 `tk-drive` 가 소유한다.
