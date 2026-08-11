# Fresh worker 전달

이 문서는 `tk-drive` 와 위임된 `tk-pr-respond`/`tk-pr-sweep` worker의
catalog tier-to-capability 계약이다. 소비 skill은 이 파일을 참조하며 tier vocabulary를
재정의하지 않는다.

## 두 축 tier 계약

요청된 모든 tier는 두 독립 축으로 해석된다. 축은 provider, model name 또는
user-configurable setting이 아니라 capability를 설명한다.

| Tier | Model 축 | Effort 축 | 사용 시점 |
| --- | --- | --- | --- |
| `cheapest` | lowest sufficient | low | 알려진 pattern과 complete evidence가 있는 mechanical 작업 또는 bounded 구현 |
| `standard` | standard sufficient | medium | 상호작용하는 interface를 가진 multi-file 구현 또는 cheapest tier로 fix를 입증할 수 없을 때의 focused debugging |
| `strongest` | highest available | high | design-heavy, unknown-cause, broad-reasoning, security/data-sensitive 또는 high-complexity 작업 |
| `host-default` | host default | inherit | host가 spawn별 tier를 선택할 수 없음 |

요청 tier는 unit evidence에서 선택된다. 이는 user decision으로 노출하지 않으며
provider/model name은 receipt나 ledger에 절대 저장하지 않는다.

## 실제 dispatch 계약

ticket의 resolved `model`/`effort`와 Drive가 승인한 tier는 설명용 문장이 아니라
native worker 호출의 입력이다. 호출 전마다 다음 dispatch envelope를 만들고 brief와
host tool 호출 양쪽에 전달한다.

```text
worker_role=implementer|corrective|reviewer|verifier
requested_tier=cheapest|standard|strongest|host-default
requested_model=lowest-sufficient|standard-sufficient|highest-available|host-default
requested_effort=low|medium|high|inherit
realized_model=<actual capability axis>
realized_effort=<actual capability axis>
collapse=none|model-unavailable|effort-unavailable|spawn-tier-unavailable
```

- `requested_model`과 `requested_effort`를 prompt에만 적지 말고 native worker
  호출의 실제 model/effort control에도 전달한다. 호출 API가 축을 받지 않으면
  해당 축을 `unavailable`로 판정하고 `host-default`/`inherit` collapse를 기록한다.
- `general-purpose` 같은 host agent label은 worker role 표시일 뿐 tier realization의
  증거가 아니다. 그 label만 반환되고 `realized_model`/`realized_effort`가 없으면
  requested tier가 적용됐다고 주장하지 않는다.
- host가 requested 축을 조용히 무시했는데 collapse를 확인할 수 없으면 mutation 전에
  `Blocked`로 멈춘다. `host-default`를 실제로 사용한 경우에만 그 사실을 ledger receipt에
  남기고 다음 unit에서 다시 cheapest/standard를 제안하지 않는다.
- provider/model name은 저장하지 않되 symbolic requested/realized axis와 collapse는
  저장한다. 따라서 plan의 tier 제안과 실제 dispatch 결과를 사후에 대조할 수 있어야 한다.

구현 작업은 `cheapest` 에서 시작한다. 파일 수, 긴급성 또는 더 강한 model
선호는 promotion 근거가 아니다. unit의 interface 또는 debugging evidence가 요구할 때만
`standard` 를 쓰고, design, unknown-cause, security/data-sensitive 또는 입증된 reasoning
failure일 때만 `strongest` 를 쓴다. corrective escalation은 한 tier만 최대 한 번
promotion하며 bounded 상태를 유지한다.

## 실행 전략

각 unit은 `direct` 또는 `delegated` 중 하나의 explicit execution strategy를 기록한다.

| 전략 | 실행자 | 허용 조건 |
| --- | --- | --- |
| `direct` | 현재 host context가 일시적으로 unit executor 역할을 하며 subagent를 spawn하지 않는다. | 사용자가 `--direct` 를 전달하거나 표시된 plan recommendation `strategy=direct` 를 승인하고, unit이 하나의 bounded standalone `tk-drive` 또는 standalone `tk-pr-respond` 구현일 때이다. |
| `delegated` | 하나의 fresh worker가 bounded unit brief를 받는다. | fresh context, isolation, independent worker, reviewer handoff, design-heavy reasoning 또는 parent `tk-pr-sweep` route가 필요할 때이다. |

isolation obligation이 없는 bounded known-pattern implementation에서는 Prepare가 단일
`👍 Recommendation:` approval surface에서 `strategy=direct` 와 `tier=cheapest` 를
권고한다. `tk-drive` 에서는 이것이 기본 recommendation이며 standalone `tk-pr-respond` 도
unit에 isolation 또는 다른 delegated-only boundary가 필요하지 않은 한 같은 권고를 쓴다.
표시한 plan의 approval은 explicit strategy approval이므로 두 번째 direct confirmation을
요청하지 않는다. `--direct` 는 같은 strategy를 미리 선택한다. 사용자가 delegated를
선택하면 그 선택을 따른다. 이것은 controller fallback이 아닌 role handoff다. 편집 중에는
current context가 unit executor이며 frozen unit paths만 건드릴 수 있다. scope 확장,
다른 unit 생성, approval/ledger owner 변경 또는 remote publish는 할 수 없다. candidate가
준비되면 owning controller가 verification과 mechanical bookkeeping을 재개한다.

`direct` 는 unavailable delegated worker의 implicit fallback이 될 수 없다. approved
strategy가 `delegated` 이면 unusable worker는 `Blocked` 로 남는다. `tk-pr-sweep` 는
multi-PR isolation과 nested-owner boundary를 하나의 direct executor로 대체할 수 없어
delegated-only다.

Direct execution은 current host context를 상속하므로 host가 제공하는 것보다 낮은
model을 주장하면 안 된다. 아래 model/effort 축을 통한 low-tier preference는 delegated
worker에 적용한다.

## Host capability 계약

첫 dispatch 전에 `model` 과 `effort` 축의 capability를 독립적으로 결정한다. 각 축은
정확히 다음 상태 중 하나다:

| 상태 | 의미와 규칙 |
| --- | --- |
| `per_call` | 축을 모든 spawn에 보낼 수 있다. |
| `definition_only` | 축은 existing matching host/agent definition을 통해서만 적용된다. definition이 없으면 축을 `unavailable` 로 처리하며 roster를 발명하거나 provider-specific mapping을 만들지 않는다. |
| `unavailable` | 축을 적용할 수 없다. model에는 `host-default` 를, effort에는 `inherit` 을 사용한다. |

TigerKit은 provider-specific effort-definition roster를 제공하지 않는다. 그러므로
`definition_only` capability는 host가 이미 matching definition을 제공할 때만 쓸 수 있다.

축은 별도로 해석한다. 따라서 host는 existing definition의 effort를 쓰면서 model을
call마다 적용하거나, model은 host default로 두고 effort만 적용할 수 있다. backing
definition 없이 capability가 `definition_only` 인 축이 적용되었다고 주장하지 않는다.

## Deterministic collapse

host가 requested tier보다 적은 controls를 노출하면 requested tier를 internal fact로
보존하고 realized collapse를 기록한다. silent promotion, mapping layer 발명 또는
silent execution strategy 전환은 하지 않는다.

1. `model` 축을 사용할 수 없으면 model을 `host-default` 로 실현하고, 사용할 수 있는
   경우에도 effort 축은 적용한다.
2. `effort` 축을 사용할 수 없으면 effort를 `inherit` 으로 실현하고, 사용할 수 있는
   경우에도 model 축은 적용한다.
3. 두 축을 모두 사용할 수 없으면 dispatch를 `host-default` 로 실현한다.
4. effort만 사용할 수 있으면 `cheapest` 와 `standard` 는 모두 `low` 로 실현하고,
   `strongest` 는 `high` 로, `host-default` 는 `inherit` 으로 실현한다.
5. spawn별 tier 선택이 불가능하면 dispatch에 `host-default` 를 사용하고 원래 tier는
   user에게 보이지 않는 evidence로만 보존한다.

ledger는 다음과 같은 symbolic fact를 기록한다:
`requested=strongest; model=host-default; effort=high; collapse=model-unavailable`.
provider/model name, secret 또는 user-facing tier choice는 절대 기록하지 않는다.

## Dispatch authorization 및 실패

`tk-drive` 는 `user-invoked` 이며 `disable-model-invocation: true` 를 가진다. explicit
`/tk-drive` 또는 `$tk-drive` invocation은 skill의 approved execution strategy에 대한
user request다. 또한 user request 뒤에만 AgentTool을 허용하는 host restriction도
충족한다. approved delegated run을 direct execution으로 되돌리지 않는다. host가 usable
worker를 spawn할 수 없으면 mutation 전에 `direct` 를 선택하지 않은 한 `Blocked` 로
중단한다. Direct mode도 위 one-unit scope와 verification boundary를 따라야 한다.

missing context가 제공된 뒤에도 입증된 reasoning 또는 complexity failure가 남을 때만
escalate한다. Escalation은 한 tier 높은 fresh worker를 쓰며 bounded이고 unlimited retry
loop가 아니다.

각 fresh worker brief에는 one unit, exact R/AC, source/ticket scope, scope/exclusion,
verification obligation 및 current Git ownership facts가 들어간다. 다음
먼저 현재 target checkout에서 `git rev-parse --show-toplevel`로 `<repository-root>`를
resolve한 뒤, repository-root-derived absolute path를 실제 결과로 치환해 verbatim으로
포함해야 한다:

```text
<repository-root>/.tigerkit/drive.md
<repository-root>/.tigerkit/spec.md
<repository-root>/.tigerkit/tickets.md
<repository-root>/.tigerkit/implement.md
```

brief는 document body를 복사하지 않고 source/ticket scope를 식별한다. unrelated source,
verbose history, child receipt, secret 또는 다른 workflow의 authority를 중첩하지 않는다.
