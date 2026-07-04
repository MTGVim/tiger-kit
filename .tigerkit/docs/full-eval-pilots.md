# TigerKit FULL eval pilots

이 문서는 TigerKit의 FULL-style behavior eval pilot를 설명합니다.

## 왜 따로 두나

현재 `evals/evals.json`은 주로 command contract / output wording / surface drift를 검증합니다.
이건 중요하지만, 실제 coding-agent session에서 일어나는 write / reject / fallback 동작 자체를 증명하진 않습니다.

FULL eval pilot는 그 빈틈을 메우기 위한 얇은 실전 검증층입니다.

- contract eval = 문서 계약이 맞는가
- FULL eval pilot = 실제 agent run에서도 그 계약이 지켜지는가

즉, prose correctness와 behavior correctness를 분리해서 봅니다.

promotion status 관점에서는 FULL pilot이 보통 `full-validated` 근거가 되지만, FULL pilot by itself does not mean shipped 입니다. public command contract와 operator docs 반영까지 끝나야 `shipped`를 검토합니다.

## Current pilots

### 1) `evals/full-pilots/reflect-repo-local-safety.json`

범위:
- surface: `/tk:reflect`
- focus: repo-local write safety
- intent: `CLAUDE.local.md`가 eligible일 때만 write되고, tracked / not-ignored / non-git / symlink 상황에서는 mutate 없이 reject되는지 확인

Covered scenarios:
- eligible repo-local apply
- tracked `CLAUDE.local.md` reject
- not ignored `CLAUDE.local.md` reject
- non-git worktree reject
- symlink `CLAUDE.local.md` reject

### 2) `evals/full-pilots/gap-stale-sot-precedence.json`

범위:
- surface: `/tk:gap`
- focus: stale SoT / source precedence honesty
- intent: stale planning prose와 conflicting source를 만났을 때 `ambiguous`를 숨기지 않고, plan-only Current evidence를 implementation proof로 승격하지 않는지 확인

Covered scenarios:
- stale plan vs live surface conflict
- unresolved source precedence stays ambiguous
- plan-only Current evidence is not implementation proof

## Operator discipline

FULL pilot는 아래를 함께 봐야 합니다.

1. stdout receipt 또는 final report
   - `reason_code`
   - `Applied candidates`
   - `Changed paths`
   - `Gap` classification과 `Evidence type`
2. 실제 filesystem / git / source-state 결과
   - `CLAUDE.local.md` bytes changed or unchanged
   - fallback path 생성 여부
   - ignore file mutation 여부
   - live source와 stale prose가 실제로 어떻게 충돌하는지
3. boundary fidelity
   - repo-local write target이 `<git-root>/CLAUDE.local.md` 밖으로 새지 않는지
   - unresolved precedence가 조용히 병합되지 않는지
   - plan/generated artifact가 code/runtime proof로 둔갑하지 않는지

문구만 그럴듯하면 통과가 아닙니다.
실제 no-write / exact-write / honest-ambiguity proof가 같이 있어야 합니다.

## Relationship to command contracts

이 pilot들은 아래 contract를 source of truth로 삼습니다.

- `commands/reflect.md`
- `docs/reflect-file-policy.md`
- `commands/gap.md`
- `skills/gap/SKILL.md`
- `.tigerkit/docs/output-contract.md`

pilot는 이 contract들을 대체하지 않습니다.
반대로 contract도 pilot 없이 "실전에서 동작한다"는 증거를 대신하지 않습니다.
