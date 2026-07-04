# TigerKit promotion statuses

이 문서는 wording / contract / eval 결과를 어떤 상태로 승격해 볼지 정리하는 operator note입니다.

## Why this exists

TigerKit에는 두 종류의 검증이 섞여 들어오기 쉽습니다.

- contract eval: 문서 계약과 공개 surface가 맞는가
- full behavior eval: 실제 agent run에서도 그 계약이 지켜지는가

이 둘은 같은 증거가 아닙니다.

contract eval만 통과했다고 곧바로 shipped wording으로 보면 안 됩니다.
반대로 FULL pilot이 있다고 해서 자동으로 public contract가 shipped가 되는 것도 아닙니다.

즉, prose correctness와 behavior correctness를 분리해 상태를 올려야 합니다.

## Status vocabulary

정식 vocabulary는 아래 4개입니다.

- `draft`
- `micro-validated`
- `full-validated`
- `shipped`

## Status meaning

### `draft`

- 문구/계약/registry 초안이 생긴 상태
- 아직 cheap wording check나 real behavior proof가 부족한 상태
- repo 안에 존재해도 public contract의 안정판이라고 부르지 않습니다

### `micro-validated`

- cheap wording 비교나 small-sample contract check에서 유의미한 확인을 거친 상태
- 주로 "이 phrasing이 덜 흔들린다" 수준의 근거
- behavior correctness를 아직 대신하지 않습니다

### `full-validated`

- FULL eval pilot 또는 동등한 실전 검증으로 behavior correctness가 확인된 상태
- write/no-write, fallback, ambiguity honesty 같은 runtime behavior에 대한 근거가 있는 상태
- 다만 이것만으로 public contract 승격이 자동 완료되진 않습니다

### `shipped`

- public command contract / README / operator docs에 반영된 현재 표준 상태
- shipped는 문서 노출만 뜻하지 않습니다
- 최소한 공개 surface 반영 + 적절한 validation trail이 함께 있어야 합니다

## Promotion rule

- `draft -> micro-validated`
  - cheap wording check 또는 대응 contract/eval로 1차 확인
- `draft -> full-validated`
  - FULL behavior eval로 실전 동작 확인
- `micro-validated -> shipped`
  - public surface 반영 전에 behavior risk가 낮다는 근거 필요
- `full-validated -> shipped`
  - public contract 반영과 operator note 정리까지 끝났을 때 승격

## Hard rule

Do not promote from `draft` to `shipped` with no intermediate evidence.

그리고 아래도 금지입니다.

- contract eval 하나만 보고 behavior correctness를 주장하기
- FULL pilot 결과만 보고 public wording migration이 끝났다고 말하기
- sample registry를 실제 shipped registry라고 포장하기

## Contract eval vs FULL behavior eval

- contract eval
  - 문서/manifest/output contract/readme 정합성 확인
  - 빠르고 싸지만 실제 runtime behavior를 직접 증명하지는 않음
- FULL behavior eval
  - real-agent session 기반 검증
  - 느리고 비싸지만 behavior correctness를 증명함

둘 다 필요할 수 있지만, 역할이 다릅니다.

## Operator guidance

1. 새로운 wording이나 route rule을 넣으면 우선 `draft`로 둡니다.
2. cheap 비교/fixture로 wording 안정성이 보이면 `micro-validated`를 검토합니다.
3. runtime behavior가 중요하면 FULL eval pilot을 붙여 `full-validated`까지 올립니다.
4. public command contract, README, operator docs까지 정리되면 `shipped`를 검토합니다.
5. shipped 이후에도 regressions가 보이면 다시 하향 조정할 수 있습니다.

## Example registry

sample registry는 아래 example file을 봅니다.

- `evals/contracts/promotion-status-registry.example.json`

이 sample은 vocabulary와 기록 shape를 설명하기 위한 것이지, 자동으로 현재 repo의 authoritative release ledger를 대신하지 않습니다.
