# Handoff plan 적용

source snapshot `03369ee6d7cafbfcecc4346539b05b3dc0a603bb` 의
`shadcn/improve` 에서 adapted했다. upstream template의 quality bar는 두 번째
plan lifecycle로 복사하지 않고 각 `AUD-*` finding에 적용한다.

저비용 executor는 self-contained context, exact paths와 symbols, current-state
excerpts 또는 evidence, repository conventions, expected results가 있는
commands, hard in/out boundaries, assumptions, explicit STOP/report-back
conditions를 받아야 한다. audited HEAD를 finding에 표시하고 drift 처리 방법을
명시한다. dependencies와 maintenance notes는 근거를 벗어나지 않게 한다.

`tk-audit` 는 절대 `plans/`, implementation code, units, remote issues를 작성하지
않는다. downstream R/AC, execution units, decisions는 `tk-drive` 가 소유한다.
