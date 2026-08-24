<!-- tigerkit:`shared-execution-protocol`; `canonical`=skills/tk-prep/references/diagnosis.md -->

# 난해한 버그 진단

원인 불명, intermittent/flaky, performance regression, 환경·시간·네트워크·상태 의존 또는 여러 plausible cause가
있는 버그에서만 이 문서를 읽습니다. 저장소 근거로 원인이 명백하고 현재 observable seam에서 exact regression
RED를 바로 만들 수 있으면 이 절차 없이 [행동 우선 테스트](testing.md)로 직행합니다.

목표는 진단 ceremony가 아니라 근거 없는 첫 fix hypothesis에 고정되기 전에 **증상 자체를 판정하는
red-capable feedback loop**를 확보하는 것입니다. 재현 표면을 찾기 위한 코드·테스트·runtime 탐색은 허용합니다.

## Feedback loop

가장 작은 applicable loop를 선택합니다.

- focused test 또는 기존 regression command
- CLI/`curl`, browser harness, captured trace replay
- throwaway harness, fuzz/property input
- `git bisect` 또는 known-good differential comparison
- perf baseline, profiler, query plan

Loop는 exact symptom을 판정하고, deterministic하거나 고정된 높은 재현률을 가지며, 빠르고 agent-runnable해야
합니다. 실제로 실행한 명령과 redacted 결과를 증거로 남깁니다. 느리거나 flaky하면 seed/input/environment를 고정하고
최소 재현으로 줄입니다.

충분한 loop를 만들 수 없으면 시도한 seam과 실패 근거, 남은 위험을 기록합니다. Testability/architecture gap은
finding 후보가 될 수 있지만 임의 abstraction이나 추측 fix로 대체하지 않습니다.

## Hypothesis와 probe

Loop가 red-capable해진 뒤에만 소수의 falsifiable hypothesis를 evidence로 순위화합니다. 각 probe는 한 예측을
판별하고 한 번에 한 변수만 바꿉니다. 결과와 모순되는 hypothesis는 버리고 최소 repro를 계속 줄입니다.

Targeted debugger/inspection을 우선하고 필요한 boundary에만 임시 log를 둡니다. 모든 임시 log에는 검색 가능한 고유
prefix를 붙입니다. Performance 회귀는 무차별 log보다 baseline/profiler/bisect를 우선합니다.

## TDD 합류와 정리

올바른 regression seam을 확보하면 [행동 우선 테스트](testing.md)의 RED → GREEN → REFACTOR로 합류해 최소 fix와
관련 모음을 검증합니다. 완료 전에 고유 prefix, throwaway harness, captured trace와 진단 산출물을 검색해 실행이
소유한 것만 제거합니다.

명령, log, trace, report에는 password, token, OTP, cookie, session, credential 또는 민감한 payload를 넣지 않고
필요한 evidence를 redaction합니다. 새 public skill, durable diagnosis ledger, 전역 state는 만들지 않습니다.

