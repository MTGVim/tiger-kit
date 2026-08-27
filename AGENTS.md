# TigerKit 저장소 지침

## 제품 경계

TigerKit은 `workflow` `runner`, `plugin`, `scheduler`, `shared-state` `framework`가 아닌 `Agent Skills` 저장소입니다.

- 각 `skills/tk-*` `package`는 `self-contained`합니다.
- `SKILL.md`가 현재 실행 `behavior`를 소유합니다.
- `package-local` `references/`는 조건부 `readable knowledge`만 소유합니다.
- `package-local` `scripts/`는 `executable helper`를, `agents/`와 `evals/`는 실행·검증 `evidence`를 소유합니다.
- 전역 TigerKit `task` `state`, `host`별 `skill` `body` 복사본, GitHub `Actions` `validation`을 만들지 않습니다.
- 중복 `protocol`보다 삭제와 `progressive` `disclosure`를 우선합니다.
- 사용자-`facing`/운영 `prose`는 한국어를 기본으로 하고 `exact` ID/`path`/`status`/`command`/`technical` `literal`은 원문을 유지합니다.
- `SKILL.md`와 `package-local` `references/`의 `model-facing` 제목과 지시문은 영어로 고정합니다. 한국어는 `SKILL.md`의 `frontmatter` `description`과 정확한 사용자 발화·출력 `literal`에만 두고 `inline code` 또는 `fenced block`으로 표시합니다.

## `Upstream-first` `distillation`

`SDD`, `skill`, `review`처럼 구현 품질에 영향을 주는 변경은 설계 전에 검증된 최신 `upstream`을 먼저 조사합니다.

- `SDD`와 `subagent-development` 변경은 최신 `obra/superpowers`를 `primary upstream`으로 삼고, 다른 자료보다 먼저 현재 구현과 관련 설계 근거·`eval`을 확인합니다.
- 고정된 `revision`에서 현재 구현, 설계 근거, 관련 `eval`을 함께 확인하고, 읽지 못한 근거는 `unverified`로 남깁니다.
- 기존 TigerKit `owner`와 경계를 비교하여 출처와 `keep | adapt | omit` 판단을 기록합니다.
- `behavior contract`와 `failure mode`만 증류하고, `runtime`, 제공자 선택, 작업 공간, `framework`는 복사하지 않습니다.
- 충분한 근거는 성숙한 `upstream`과 구체적인 TigerKit `gap`, 강하게 검증된 재사용 가능 단일 사례, 충분한 자료가 있는 명시적 재사용 `workflow`, 또는 실제로 반복 검증된 사례 중 하나면 됩니다.
- 출처 없는 일화, 원시 `log`, 재사용 가능한 교정 근거가 없는 일회성 실수는 승격하지 않습니다. 구체적인 차이가 입증되지 않으면 기존의 더 단순한 TigerKit 계약을 유지합니다.

## `Agent-facing` instruction economy

Agent가 읽는 문서는 길이가 아니라 **행동 대비 load**로 판단합니다.

- `description`과 `reference` pointer는 본문을 요약하지 않고, 어떤 distinct branch/condition에서 그 내용을 읽어야 하는지 encode합니다.
- 모든 실행 경로가 필요한 step/guard는 inline으로 두고, 일부 branch만 필요한 reference는 정확한 pointer 뒤로 `progressive disclosure`합니다. Reference로 내리는 것 자체가 목표는 아닙니다.
- `package.json`, config, directory layout, 현재 host/tool capability처럼 한 번의 cheap fresh lookup으로 알 수 있는 사실은 environment를 source of truth로 둡니다. 문서가 canonical contract이거나 lookup이 expensive/unreliable한 경우에만 의도적인 cache를 유지합니다.
- 문장·블록 삭제는 미학적 축약이 아니라 no-skill/prior behavior 비교로 판단합니다. Pressure에서 실제 행동을 지키는 rationale/guard는 짧아진다는 이유로 제거하지 않습니다.
- 일반 steering은 해야 할 행동을 직접 쓰는 positive form을 선호하되, publication authority, destructive mutation, secret, freshness, cross-scope safety boundary의 hard stop은 약화하지 않습니다.

## `Adaptive prep` `product` `work`

TigerKit의 `product-work` `owner`는 `tk-prep`입니다.

`tk-prep`은 중앙 `runtime`이 아니라 **대화형 준비 + 승인된 로컬 실행 담당자**입니다. 작업 크기에 따라
`direct/no-Seed | Ready Seed direct | SDD | handoff`를 선택합니다.

```text
request
→ conversational prep
→ final local-mutation approval
→ direct/no-Seed | Ready Seed | SDD | handoff
→ local implementation
→ review/verification
→ commit
→ tk-pr-open
```

Ready `Seed`는 지속 가능한 맥락이 실제로 필요할 때만 만듭니다. `direct/no-Seed`는 SDD 상세 문서를 읽지 않습니다.
SDD가 선택되면 `tk-prep`과 `tk-pr-respond`의 패키지 로컬 생성 참조가 하나의 행동 원천을
공유하고, 실제 자식 `model`/`reasoning_effort`는 현재 호스트 기능과 허용 목록에서 실행 중에만 결정합니다.

TigerKit은 다음 `runtime` `mapping`을 소유하지 않습니다.

- `cheapest | standard | strongest`
- `provider`/`model` `selector`
- `reasoning` `effort` `mapping`
- `.tigerkit/session.md`
- `durable` `worker`/`wave` `cursor`

모델 수준과 `fan-out`은 `Seed`에서 사람 친화적인 추천으로만 표현할 수 있습니다.
승인된 `execution shape`, `acceptance`, `verification`은 구속력이 있으며 제공자 값은 지속되는 산출물에 넣지 않습니다.

## `Seed` 계약

`.tigerkit/seed.md`는 **존재할 때만** 현재 작업으로 표시되고 식별자에 묶인 `self-contained` `context`입니다.
인터뷰 중 `Pending Seed`를 만들지 않고 최종 승인 전 기존 Ready `Seed`를 보존합니다.

Ready `Seed`는 `fresh` `lower-capability` `executor`가 원 대화 없이 다음을 이해할 수 있어야 합니다.

- `goal`/`background`
- `current` `evidence`/`entry` `points`
- `scope`/`exclusions`
- `confirmed` `material` `decisions`
- `implementation` `direction`
- `engineering` `readiness`
- AC와 `per-AC` `verification`
- `browser` `plan`
- `known` `traps`/`do-not-change`
- `execution` `recommendation`

`Seed`는 `transcript`, `progress` `ledger`, `provider` `routing`, `secret` `store`가 아닙니다. 활성 SDD 복구는
현재 `Seed` 식별자와 해시가 일치하는 하나의 무시된 `.tigerkit/sdd.md`만 사용할 수 있습니다.

실행 중 `material` `evidence`가 `Seed` `contract`를 깨면 임의 해석 변경 대신 `tk-prep`으로 돌아가
`revision` + `user` `reapproval`을 거칩니다.

## `Conversational` UX

`tk-prep`, `tk-wizard`, `tk-ask-repo`, `tk-pr-respond`, `tk-pr-sweep`의 공통 원칙:

> **대화는 자연스럽게, 상태는 엄격하게.**

`structured` `state`/`safety` `gate`를 사용자에게 `form`/`report`로 그대로 노출하지 않습니다.
이미 확인된 내용을 반복 질문하지 않고, 사용자가 실제로 결정하거나 행동해야 하는 것만 요청합니다.
`engineering` 판단은 숨기지 않고 추천과 이유를 자연어로 설명합니다.

## `Skill` 존재 규율

`Skill` 유지 조건:

- 독립 `invocation` 또는 좁은 `trigger`
- 일반 모델보다 실질적으로 다른 `procedure`
- `objective` `completion`/`boundary`
- `owned` `artifact`, `mutation`, `authority` 또는 `safety` `boundary`

약한 후보는 `inline`/`merge`/`reference`/`delete`를 우선합니다.

## 핵심 `authority`

- `tk-prep`: 준비, 최종 승인, 승인된 격리 로컬 구현/검증/`commit`. `push`/발행 금지.
- `tk-ask-repo`: `read-only` `repository` `investigation`.
- `tk-audit`: `read-only` AUD `finding`.
- `tk-browser-verify`: `browser-visible` `runtime` `evidence`와 `dev-server` `lifecycle`.
- `tk-pr-open`: `exact` single-PR `create`/`update` 또는 승인된 retrospective stacked-PR `publication`.
- `tk-pr-respond`: `exact` `one-PR` `feedback`/지원 CI `resolution`과 `bounded` `publication`.
- `tk-pr-rebase`: `exact` `rebase` + `force-with-lease`.
- `tk-pr-sweep`: `deterministic` `multi-PR` `triage`와 승인된 `child` `maintenance`.
- `tk-learn`: `reusable` `skill`의 `semantic` `create | improve | merge` `writer`.
- `tk-domain`: `repository` 고유 `canonical domain vocabulary`의 `CONTEXT.md`와 `sparse durable decision/ADR context` 작성·정제 담당자.

`Push`/PR/`merge`/`tag`/`release`/`publish`는 각각 해당 `owner`의 명시 `authority` 없이는 확장하지 않습니다.

## PR `fresh-state` 원칙

PR `state`의 `truth`는 GitHub `fresh` `state`입니다.

`tk-pr-respond`와 `tk-pr-sweep`은 `lifecycle` Markdown `snapshot`을 `authority`로 사용하지 않습니다.
각 `remote` `mutation` 전에 `exact` PR/`head`/`thread`/`check`/`identity`를 필요한 수준으로 다시 확인합니다.

`Sweep`의 `deterministic` `triage` `script`와 `user-level` `repository` `config`는 유지합니다.

```text
$XDG_CONFIG_HOME/tigerkit/pr-triage.json
```

`model`/`worker`/`session`/`pitfall` 설정은 `user-level` `config`로 만들지 않습니다.

## `Browser`

`browser-visible` AC는 계획 단계에서 `target`/`headless`/`auth`/`viewport`/`evidence`/`server` `readiness`를 정합니다.
실제 검증과 `dev-server` `lifecycle`은 `tk-browser-verify`가 소유합니다.

`password`/`token`/OTP/`cookie`/`session` `secret`을 `chat`, `Seed`, `logs`, `receipt`에 저장하지 않습니다.

## 반복 발견

TigerKit은 `persistent` `pitfall` `corpus`나 `memory` `backend`를 소유하지 않습니다.

- 현재 `Seed`를 바꾸는 발견 → `Seed` `revision`
- `repository` `reusable` `invariant` → `repo-native` `owner` 개선 후보
- TigerKit `skill` 반복 실패 → `tk-skill-diagnose` / `tk-learn`
- 개인 `cross-repo` `memory` → 외부 `memory`

자동 승격하지 않습니다.

## `Eval` 정본

```text
skills/<skill>/evals/triggers.json
skills/<skill>/evals/evals.json
evals/catalog-routing.json
evals/release-critical.json
```

`breaking` `release`에서 같은 이름의 `skill` `behavior` `contract`를 의도적으로 교체할 경우
`evals/release-critical.json`의 `replaced_skill_eval_contracts`로 명시하고
`run_seed_release_gate.py`로 `baseline` 보존/교체를 함께 검증합니다.

## 필수 검사

```bash
python3 scripts/sync_execution_protocol.py --check
python3 scripts/validate_skills.py
python3 scripts/validate_skills.py --links-only
python3 -B -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/audit_catalog.py --check
node --check skills/tk-pr-sweep/scripts/triage.mjs
node --test skills/tk-pr-sweep/scripts/triage.test.mjs
npx --yes skills@1.5.9 add . --list
npx --yes skills add . --list
git diff --check
```

`Release` `candidate`:

```bash
python3 scripts/run_seed_release_gate.py \
  --baseline "$(git describe --tags --abbrev=0)" \
  --candidate HEAD \
  --output /tmp/tigerkit-release-gate
```

모든 `validation`은 `local-only`입니다.
