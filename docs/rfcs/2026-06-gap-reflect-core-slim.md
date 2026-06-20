# RFC: TigerKit를 `gap` + `reflect` 중심의 경량 코어로 단순화

- 상태: Proposed
- 날짜: 2026-06-20
- 작성자: Hermes Agent

## 요약

TigerKit의 active command surface를 `gap`과 `reflect` 두 개로 줄인다.

이번 변경은 TigerKit을 workflow runner, Patron delegation, setup/management command 모음이 아니라, **SoT(Source of Truth) 우선 정합성 확인 + 세션 학습 정리**에 집중한 경량 Claude Code plugin으로 재정의한다.

## 배경

현재 TigerKit Slim은 `gap`, `grill`, `afk`, `reflect`, `setup`을 active surface로 노출한다. 그러나 실제 사용 관점에서 다음 문제가 있다.

1. `afk` / Patron / temporary helper framing은 실제 자동 orchestration 기대를 만들지만, 사용자가 체감하는 동작은 그 기대에 못 미친다.
2. `setup`은 user-level workflow preference를 설명하는 데 비해 command surface가 과하다.
3. `grill`은 유용할 수 있으나 core surface에 둘 필요는 약하다. 필요하면 별도 optional plugin/command로 다시 도입할 수 있다.
4. TigerKit의 가장 강한 가치 제안은 이미 `gap`과 `reflect`에 있다.

## 목표

- TigerKit의 정체성을 한 문장으로 설명 가능하게 만든다.
- 사용자가 언제 `gap`을 고려해야 하는지 명확히 한다.
- `reflect`를 통해 세션에서 재사용 가능한 학습을 정리하는 흐름은 유지한다.
- README, plugin manifest, evals, command docs, cover image가 같은 메시지를 말하도록 정렬한다.
- semver major bump에 걸맞은 surface reduction을 명시적으로 문서화한다.

## 비목표

- launch-era workflow 실험을 복원하지 않는다.
- AFK / Patron을 soft rename으로 유지하지 않는다.
- setup wizard나 recommended tools menu를 재설계하지 않는다.
- repo-local runtime/helper code를 추가하지 않는다.

## 제안

### 1. Active command surface를 `gap` / `reflect`로 축소

남기는 명령:

- `/tk:gap`
- `/tk:reflect`

active surface에서 제거:

- `/tk:grill`
- `/tk:afk`
- `/tk:setup`

기존 launch-era deprecated command는 계속 deprecated 문맥으로만 남긴다.

### 2. TigerKit의 core guidance를 문서 본문과 description에 직접 명시

TigerKit은 더 이상 setup command로 workflow preference를 설치하지 않는다. 대신 README와 command markdown 본문이 아래 규칙을 직접 소유한다.

- SoT가 있으면 구현 전에 `/tk:gap`을 먼저 고려한다.
- SoT가 없으면 먼저 SoT 제공을 제안한다.
- 사용자가 직접 진행을 원하면 `/tk:gap` 없이 진행할 수 있다.
- SoT 없이 진행할 때는 가정과 불확실성을 명시한다.
- 의미 있는 작업이 끝나면 `/tk:reflect`로 재사용 가능한 learning을 정리한다.

### 3. 커버 이미지도 동일한 메시지로 재구성

README 커버는 기존의 AFK/Patron/setup 세계관을 벗어나, 다음 메시지를 직관적으로 보여줘야 한다.

- source of truth
- current implementation
- gap analysis
- reflect / learning capture

### 4. evals를 2-command 모델에 맞게 재작성

새 evals는 적어도 아래 계약을 검증해야 한다.

- active command surface는 `/tk:gap`, `/tk:reflect`만 포함한다.
- `gap`은 SoT와 current implementation의 one-shot comparison이다.
- SoT가 있으면 `gap`을 먼저 고려한다.
- SoT가 없으면 SoT 제공을 제안한다.
- 사용자가 즉시 진행을 원하면 `gap` 없이 진행 가능하다.
- `reflect`는 reusable learning extraction contract를 유지한다.

## 세부 변경 범위

### Manifest / packaging

- `.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`

### User-facing docs

- `README.md`
- `commands/gap.md`
- `commands/reflect.md`
- 새 RFC 문서

### Remove from active surface

- `commands/grill.md`
- `commands/afk.md`
- `commands/setup.md`

### Remove or archive supporting docs

- `docs/patron-catalog.md`
- `docs/patron-decision-ledger.md`
- `docs/patron-lifecycle.md`
- `docs/afk-default.md`
- `docs/config-state.md`
- `docs/vowline-integration.md`
- `docs/recommended-tools.md`

### Evals

- `evals/evals.json`

## 마이그레이션

기존 사용자는 아래처럼 이해하면 된다.

- 예전의 `afk` / Patron decision delegation 흐름은 더 이상 active contract가 아니다.
- setup wizard 없이도 TigerKit의 기본 사용 규칙은 README와 command description에서 바로 확인할 수 있다.
- pressure-test 질문 렌즈가 필요하면 지금은 repo 외부 도구/별도 command로 다루고, TigerKit core에는 포함하지 않는다.

## 버전 정책

이 변경은 active command surface를 실질적으로 축소하는 breaking change다. 따라서 semver **major bump**를 적용한다.

## 검증 계획

1. plugin manifest validation 통과
2. evals JSON / marketplace / plugin JSON 구조 검증 통과
3. version consistency script 통과
4. README와 command docs가 2-command surface를 일관되게 설명함을 확인
5. Claude review에서 findings가 없을 때만 commit / PR / merge / tag 진행

## 대안 검토

### A. `setup`만 유지

장점:
- workflow preference를 명시적으로 설명할 수 있다.

단점:
- core surface를 단순화하려는 목적에 어긋난다.
- 실제 저장/설치할 user-level state보다 설명 역할이 커서 command 가치가 약하다.

### B. `grill`만 optional active로 유지

장점:
- review/question lens 도구를 원하는 사용자를 만족시킬 수 있다.

단점:
- core identity가 다시 흐려진다.
- 추후 별도 optional command로 가져오면 충분하다.

### C. AFK/Patron framing만 유지하고 실체를 약화

장점:
- 기존 세계관을 덜 깨뜨린다.

단점:
- 실제 동작보다 더 큰 기대를 계속 만들 수 있다.
- 이번 simplification의 취지와 충돌한다.

## 결론

TigerKit은 `gap`과 `reflect`에 집중할 때 가장 설명 가능하고, 가장 덜 과장되며, 가장 실용적이다. 이번 RFC는 TigerKit을 **SoT-first gap/reflect workflow kit**으로 재정의하고, 그에 맞춰 문서/manifest/evals/이미지를 모두 정렬하는 변경을 제안한다.
