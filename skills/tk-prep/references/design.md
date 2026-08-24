# 조건부 설계 비교

Repository precedent와 current evidence가 결정을 충분히 정하지 못한 material architecture uncertainty에서만 이
문서를 읽습니다. 다음 네 조건을 모두 만족하지 않으면 저장소 선례 또는 가장 단순한 reversible 선택을 추천하고
추가 ceremony 없이 준비를 계속합니다.

1. interface, seam, schema, architecture, migration처럼 선택을 되돌리기 어렵다.
2. Materially plausible한 설계가 둘 이상 존재한다.
3. 틀렸을 때 rework, compatibility, data 또는 test cost가 의미 있다.
4. 현재 repository evidence가 한 안을 충분히 결정하지 못한다.

## 비교

제어기가 최소 2개의 materially different design을 짧게 만듭니다. 이름만 다른 variation은 세지 않습니다.
각 안을 다음 근거로 비교합니다.

- existing reuse와 repository fit
- simplicity와 숨기는 complexity
- observable test seam
- blast radius와 dependency impact
- migration, rollback, compatibility cost
- cost-if-wrong

메뉴만 나열하지 않고 evidence가 가장 강한 안과 이유를 추천합니다. 서로 다른 안의 장점을 결합한 hybrid가 실제로 더
단순하면 허용합니다. 저장소 선례가 발견되면 comparison을 중단하고 그 선례를 추천합니다.

## Optional exploration과 review guard

2개 이상의 독립 탐색이 실제 confidence를 높이는 복잡한 경우에만 subagent fan-out을 선택합니다. 현재 호스트가
fan-out을 제공하지 않아도 controller가 같은 비교를 수행하며 `Blocked`가 아닙니다. Agent 수, provider, model,
reasoning 값은 이 reference나 `Seed`에 고정하지 않습니다.

이 heuristic은 proposal/discovery 도구입니다. Repository standard, 승인된 `Seed` decision 또는 AC로 실제 승격되지
않은 design vocabulary를 reviewer가 독립 failure criterion으로 사용하지 않습니다. TigerKit-owned design ledger나
새 public workflow를 만들지 않습니다.

