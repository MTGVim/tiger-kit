# Fresh worker 전달

이 문서는 `tk-drive` 와 위임된 `tk-pr-respond`/`tk-pr-sweep` worker의
Superpowers식 SDD dispatch 계약이다. 소비 skill은 이 파일을 참조하며 worker/reviewer
순서를 재정의하지 않는다.

## Superpowers식 SDD worker 계약

복잡한 tier 매핑 대신 `subagent-driven-development`의 짧은 루프를 따른다.

- delegated unit마다 새 `general-purpose` worker 하나를 dispatch한다. 이 label은
  실패가 아니라 implementer/reviewer의 의도된 host role이다.
- `model`/`effort`는 plan metadata다. `cheapest`/`standard`/`strongest`를
  provider 이름으로 번역하거나 post-spawn receipt를 발명하지 않는다.
- model override를 지원하는 native host면 spawn 전에 선택한 `model`을 명시한다.
  지원하지 않으면 spawn 전에 `model=host-default`로 결정한다. worker를 먼저 띄운
  뒤 반환 label을 보고 tier를 판정하지 않는다.
- implementer prompt에는 task brief, exact scope/R-AC, worktree ownership, report
  path를 넣는다. worker는 질문을 먼저 내고, 구현·focused test·self-review·commit을
  마친 뒤 짧은 status와 report path만 반환한다.
- commit 전 fresh `general-purpose` reviewer를 dispatch한다. reviewer는 diff를 한 번
  읽고 `Spec compliance`와 `Task quality` 두 verdict를 내며 worktree를 수정하지 않는다.
- review가 실패하면 rounds 1–3은 같은 implementer를 resume하고, rounds 4–5는 새
  worker와 한 단계 강한 model을 쓴다. 다섯 번 뒤에도 load-bearing finding이 남으면
  `Blocked`다. 모든 unit 뒤에는 한 번의 whole-branch review를 수행한다.

model 선택은 작업에 필요한 최소 capability만 쓴다: mechanical 작업은 `cheapest`,
multi-file integration/debugging은 `standard`, architecture와 final review는
`strongest`. 파일 수나 막연한 품질 선호만으로 promotion하지 않는다.

## 실행 전략

각 unit은 `direct` 또는 `delegated` 중 하나의 explicit execution strategy를 기록한다.

| 전략 | 실행자 | 허용 조건 |
| --- | --- | --- |
| `direct` | 현재 host context가 일시적으로 unit executor 역할을 하며 subagent를 spawn하지 않는다. | 사용자가 `--direct` 를 전달하거나 표시된 plan recommendation `strategy=direct` 를 승인하고, unit이 하나의 bounded standalone `tk-drive` 또는 standalone `tk-pr-respond` 구현일 때이다. |
| `delegated` | 하나의 fresh worker가 bounded unit brief를 받는다. | fresh context, isolation, independent worker, reviewer handoff, design-heavy reasoning 또는 parent `tk-pr-sweep` route가 필요할 때이다. |

isolation obligation이 없는 bounded known-pattern implementation에서는 Prepare가 단일
`👍 Recommendation:` approval surface에서 `strategy=direct` 와 `model=cheapest` 를
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
model을 주장하지 않는다. model 선택은 delegated worker의 사전 계획에만 적용한다.

## Dispatch authorization 및 실패

`tk-drive` 는 `user-invoked` 이며 `disable-model-invocation: true` 를 가진다. explicit
`/tk-drive` 또는 `$tk-drive` invocation은 skill의 approved execution strategy에 대한
user request다. 또한 user request 뒤에만 AgentTool을 허용하는 host restriction도
충족한다. approved delegated run을 direct execution으로 되돌리지 않는다. host가 usable
`general-purpose` worker를 spawn할 수 없으면 **spawn 전에** `Blocked`로 중단한다.
반환된 `general-purpose` label은 정상 결과이므로 사후에 tier 차단을 시도하지 않는다.

missing context가 제공된 뒤에도 입증된 reasoning 또는 complexity failure가 남을 때만
escalate한다. Escalation은 한 단계 강한 fresh worker를 쓰며 bounded이고 unlimited retry
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

brief는 document body를 복사하지 않고 source/ticket scope를 식별한다. implementer와
reviewer는 각각 report/diff package path를 받는다. unrelated source, verbose history,
child receipt, secret 또는 다른 workflow의 authority를 중첩하지 않는다.
