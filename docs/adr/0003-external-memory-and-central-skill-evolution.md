# ADR 0003: External memory and central skill evolution

- Status: Accepted
- Date: 2026-07-31
- Source: MTGVim/tiger-kit issue #224
- Supersedes: ADR 0002의 reflection·rule lifecycle 결정

## Context

TigerKit은 Agent Skills 저장소이며 persistent memory product나 repository/user rule lifecycle
manager가 아닙니다. 과거에는 successful workflow 뒤 reflection을 수행하고 reusable finding을
rule 또는 skill 후보로 승격하는 경로가 있었지만, 이 구조는 다음 책임을 TigerKit 안으로 끌어왔습니다.

- 장기 memory 저장·검색·dedupe·decay
- repository/user rule의 생성·수정·배치·정리
- skill diagnosis와 semantic skill mutation의 중복 owner
- workflow 완료 이후 별도의 learning tail

이 책임은 TigerKit의 독립형 skill distribution 경계보다 큽니다.

## Decision

### 1. Persistent memory와 rule lifecycle을 소유하지 않는다

TigerKit은 persistent memory backend를 감지·설정·호출하지 않습니다. 또한 normal lifecycle에서
repository/user rule을 생성·수정·승격·정리하지 않습니다.

기존 repository instruction, ADR, tests, types, lint/CI policy 등은 계속 **외부에서 소유되는
read-only authority**로 읽고 따릅니다. 읽는 것과 lifecycle을 소유하는 것은 구분합니다.

### 2. Post-session reflection owner를 두지 않는다

Retired `tk-reflect`를 복원하지 않습니다. Product workflow는 검증된 자신의 terminal boundary에서
끝나며, 별도의 TigerKit persistent-memory/reflection tail을 성공 조건으로 요구하지 않습니다.

외부 memory tool이 설치되어 있다면 해당 도구가 TigerKit과 독립적으로 session/output을 관찰할 수
있지만 TigerKit은 이를 runtime dependency나 optional adapter로 취급하지 않습니다.

### 3. `tk-learn`이 semantic skill mutation의 단일 owner다

Reusable skill의 semantic 변경은 `tk-learn`이 다음 세 종류로 단독 소유합니다.

```text
create | improve | merge
```

`tk-learn`은 evidence, dedupe, trigger/eval, provenance/license, compatibility, exact target,
apply approval을 검증한 뒤에만 canonical skill source를 씁니다.

### 4. Diagnosis와 grooming은 writer가 아니다

- `tk-skill-diagnose`는 observed Agent Skill incident를 재현·격리하고 verified objective를
  `learn-ready` 형태로 넘길 수 있지만 canonical semantic patch를 소유하지 않습니다.
- `tk-grooming`은 repository/user skill catalog의 중복·trigger·scope·ownership을 감사하고 semantic
  변경이 필요하면 proposal을 만들 수 있지만 `tk-learn`을 자동 호출하거나 writer 역할을 가져가지 않습니다.

### 5. 자주 바뀌는 실행 계약은 ADR에 고정하지 않는다

현재 공개 skill 수, standalone 여부, direct/delegated strategy, model routing, browser/PR 세부 절차,
ledger schema 같은 실행 surface는 이 ADR의 장기 결정이 아닙니다.

그 정본은 다음에 둡니다.

1. `README.md` — 현재 공개 skill surface
2. `skills/tk-*/SKILL.md` — 현재 skill 계약
3. skill-local eval과 `evals/catalog-routing.json` — executable behavior/routing
4. `AGENTS.md` — TigerKit 저장소 제품 경계

따라서 이후 catalog가 추가·삭제·재구성되어도 위 네 architecture decision이 유지되는 한 이 ADR은
갱신할 필요가 없습니다.

## Consequences

- TigerKit은 session history를 장기 memory로 저장하거나 항상 로드되는 rule corpus를 성장시키지 않습니다.
- existing instruction은 존중하지만 TigerKit 소유 artifact로 승격하지 않습니다.
- skill semantic writer가 하나이므로 diagnosis/audit와 apply gate가 분리됩니다.
- 외부 memory 제품은 TigerKit과 coupling 없이 독립적으로 선택·교체할 수 있습니다.
- 과거 CHANGELOG, closed issue, superseded ADR은 당시 behavior를 설명할 수 있지만 current routing이나
  skill surface의 authority는 아닙니다.

## Verification obligations

이 ADR의 경계를 바꾸는 변경은 최소 다음을 증명해야 합니다.

- retired `tk-reflect` 또는 동등한 post-session memory owner가 active catalog에 다시 들어오지 않음
- normal TigerKit lifecycle이 repository/user rule 또는 persistent-memory store를 semantic하게 쓰지 않음
- `tk-learn` 외 skill이 reusable skill의 `create | improve | merge` canonical write owner를 주장하지 않음
- `tk-skill-diagnose`와 `tk-grooming`의 handoff/proposal이 자동 semantic mutation으로 이어지지 않음
- existing repository instruction의 read-only consumption은 계속 허용됨

현재 catalog 개수나 개별 workflow의 세부 assertion은 이 ADR이 아니라 현재 skill/eval 정본으로
검증합니다.
