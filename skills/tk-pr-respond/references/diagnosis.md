<!-- tigerkit:`shared-execution-protocol`; `canonical`=skills/tk-prep/references/diagnosis.md -->

# 난해한 버그 진단

원인 불명, `intermittent/flaky`, `performance regression`, 환경·시간·네트워크·상태 의존 또는 여러
`plausible cause`가 있는 버그에서만 이 문서를 읽습니다. 저장소 근거로 원인이 명백하고 현재 `observable seam`에서 `exact regression`
RED를 바로 만들 수 있으면 이 절차 없이 [행동 우선 테스트](testing.md)로 직행합니다.

목표는 진단 절차가 아니라 근거 없는 첫 `fix hypothesis`에 고정되기 전에 **증상 자체를 판정하는
`red-capable feedback loop`**를 확보하는 것입니다. 재현 표면을 찾기 위한 코드·테스트·`runtime` 탐색은 허용합니다.

## 판정 반복

가장 작은 적용 가능한 반복을 선택합니다.

- 집중 테스트 또는 기존 회귀 명령
- CLI/`curl`, 브라우저 장치, 저장된 추적 재생
- 일회성 장치, `fuzz/property input`
- `git bisect` 또는 `known-good differential comparison`
- 성능 기준선, 프로파일러, 쿼리 계획

판정 반복은 `exact symptom`을 판정하고, `deterministic`하거나 고정된 높은 재현률을 가지며, 빠르고
`agent-runnable`해야 합니다. 실제로 실행한 명령과 비식별 처리 결과를 증거로 남깁니다. 느리거나 `flaky`하면 `seed/input/environment`를 고정하고
최소 재현으로 줄입니다.

충분한 반복을 만들 수 없으면 시도한 `seam`과 실패 근거, 남은 위험을 기록합니다.
`Testability/architecture gap`은 발견 후보가 될 수 있지만 임의 추상화나 추측 수정으로 대체하지 않습니다.

## 가설과 탐침

판정 반복이 `red-capable`해진 뒤에만 소수의 `falsifiable hypothesis`를 근거로 순위화합니다. 각 탐침은 한 예측을
판별하고 한 번에 한 변수만 바꿉니다. 결과와 모순되는 가설은 버리고 최소 재현을 계속 줄입니다.

`Targeted debugger/inspection`을 우선하고 필요한 경계에만 임시 로그를 둡니다. 모든 임시 로그에는 검색 가능한 고유
`prefix`를 붙입니다. 성능 회귀는 무차별 로그보다 `baseline/profiler/bisect`를 우선합니다.

## TDD 합류와 정리

올바른 `regression seam`을 확보하면 [행동 우선 테스트](testing.md)의 RED → GREEN → REFACTOR로 합류해 최소 수정과
관련 모음을 검증합니다. 완료 전에 고유 `prefix`, 일회성 장치, 저장된 추적과 진단 산출물을 검색해 실행이
소유한 것만 제거합니다.

명령, 로그, 추적, 보고에는 비밀번호, 토큰, OTP, 쿠키, 세션, 자격 증명 또는 민감한 입력을 넣지 않고
필요한 근거를 비식별 처리합니다. 새 공개 스킬, 영속 진단 장부, 전역 상태는 만들지 않습니다.
