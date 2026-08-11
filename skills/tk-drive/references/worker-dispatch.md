# 새 작업자 전달

이 문서는 `tk-drive` 와 위임된 `tk-pr-respond`/`tk-pr-sweep` 작업자의 direct 또는
Superpowers식 SDD dispatch 계약이다. 소비 스킬은 이 파일을 참조하며 작업자/검토자
순서를 재정의하지 않는다.

## 작업 공간 호스트 backend 짝짓기

작업 트리 생성과 작업자 dispatch는 서로 독립적으로 고르지 않는다. 각 단위는
정확히 하나의 `workspace_backend`를 freeze하고, 같은 backend의
`worktree_backend`, `dispatch_backend`, `backend_evidence`, `receipt_source`를
함께 기록한다.

| `workspace_backend` | 작업 트리 | 작업자 dispatch | 선택 조건 |
| --- | --- | --- | --- |
| `git-native` | `git worktree` | 현재 호스트의 새 native 작업자 | 이 저장소에서 확인된 대체 경로 |
| `orca` | 호스트가 제공하는 작업 트리 | 같은 호스트의 worker-start | 작업 트리·dispatch·receipt를 모두 현재 실행에서 증명 |
| `paseo` | 호스트가 제공하는 workspace | 같은 호스트의 작업자 실행 | 작업 트리·dispatch·receipt를 모두 현재 실행에서 증명 |

CLI 설치, 전역 스킬 목록, 과거 실행 기록만으로 `orca`나 `paseo`를 선택하지
않는다. 선택한 backend가 두 기능을 함께 제공하지 않거나 identity·receipt 소스를
노출하지 않으면 mutation 전에 `Blocked`다. `orca` 작업 트리와 별도 native 작업자,
또는 `paseo` workspace와 다른 호스트 dispatch를 조합하는 것은 금지한다.

## 위임된 SDD 작업자 계약

`delegated` 를 선택한 단위만 `subagent-driven-development`의 짧은 루프를 따른다.

- delegated 단위마다 새 `general-purpose` 작업자 하나를 dispatch한다. 이 label은
  실패가 아니라 implementer/검토자의 의도된 호스트 역할이다.
- `model`/`effort`는 계획 metadata이며 아래 session routing으로 spawn 전에 native
  selector를 resolve한다. 작업자를 먼저 띄운 뒤 반환 label로 model을 추정하지 않는다.
- implementer prompt에는 task brief, 정확한 범위/R-AC, 작업 트리 소유권, report
  경로를 넣는다. 작업자는 질문을 먼저 내고, 구현·focused test·self-review·commit을
  마친 뒤 짧은 status와 report 경로만 반환한다.
- commit 전 새 `general-purpose` 검토자를 dispatch한다. 검토자는 diff를 한 번
  읽고 `Spec compliance`와 `Task quality` 두 verdict를 내며 작업 트리를 수정하지 않는다.
- review가 실패하면 rounds 1–3은 같은 implementer를 resume하고, rounds 4–5는 새
  작업자와 한 단계 강한 model을 쓴다. 다섯 번 뒤에도 핵심 발견 사항이 남으면
  `Blocked`다. delegated 단위가 하나라도 있거나 계획이 요구할 때만 마지막에 한 번의
  전체 브랜치 review를 수행한다.

model 선택은 작업에 필요한 최소 capability만 쓴다: mechanical 작업은 `cheapest`,
여러 파일 통합/디버깅은 `standard`, 아키텍처와 최종 검토는
`strongest`. 파일 수나 막연한 품질 선호만으로 승격하지 않는다.

## 세션 모델 라우팅

Delegated dispatch 전에 저장소 루트의 선택적 `.tigerkit/session.md`를 읽는다.
현재 호스트 section에 `cheapest`, `standard`, `strongest` class block이 모두 있고
각 block에 `model`이 있으며 `Status: Ready`이면 선택한 class의 model/effort를
spawn 전에 dispatch한다. 이 section의 schema가 정경이다.

```markdown
# TigerKit session
Status: Ready

## claude-code

### cheapest
- model: haiku
- effort: low

### standard
- model: sonnet
- effort: medium

### strongest
- model: opus
- effort: high
```

현재 호스트 section이 없거나 불완전하면 일반 `👍 Recommendation:` 안에
`.tigerkit/session.md`에 추가할 정확한 block과 근거를 제안한다. 기존 block을 조용히
덮어쓰거나 승인 전에 파일을 쓰거나 작업자를 dispatch하지 않는다.
`routing_state=decision-required`로 기록하고 사용자가 승인하면 그 block만 merge한 뒤
`Status: Ready`, 세 class, 각 `model`을 reread해 검증한다. 실패하면 `Blocked`다.
호스트 catalog/설정에서 selector를 확인할 수 없으면 값을 발명하지 않고 사용자 소유
selector 결정으로 남긴다. 세 class의 confirmed `model`이 모이기 전에는
`unavailable`, `USER_DECISION_REQUIRED` 같은 sentinel을 넣은 Markdown block을 보여
주지 않는다. 문법상 유효해 보이는 잘못된 파일 대신 누락된 제어를 질문하고
`Pending`으로 남긴다.

전환 기간에는 기존 flat `- cheapest: haiku` 3종도 읽되
`reasoning_effort=inherited`로 처리한다. 새로 제안하거나 쓰는 block은 항상 중첩된
정경 스키마다. `effort`가 생략됐거나 호스트가 지원하지 않으면 inherited로 기록하고,
지원되면 native effort control에 spawn 전에 전달한다.

라우팅 소스는 저장소 로컬 `.tigerkit/session.md` 하나다. 호스트 전역
`CLAUDE.md`, `AGENTS.md`, `SOUL.md` 또는 다른 사용자 파일을 라우팅 상태로 읽거나
쓰지 않는다. TigerKit의 런타임 상태를 저장소/작업 트리 밖에 만들지 않는 제품
경계를 유지한다.

Class block에서 허용되는 key는 `model`, `effort`뿐이다. 다른 key, 중복 key 또는
알 수 없는 heading이 있으면 모델이 의미를 추정해 소비하지 않는다. 알 수 없는 필드를 장부에 기록하고 dispatch 전에 `Blocked`다.

실행 가능한 delegated 단위가 하나라도 있으면 chat 승인 표면에 단위별
`model_class`, resolved `model`, `effort`, routing 소스를 필수로 표시한다.
누락된 승인 표면으로는 dispatch하지 않고 `Blocked`다.

Host adapter는 다음 native control을 우선한다.

| 호스트 | dispatch control | realized receipt |
| --- | --- | --- |
| `claude-code` | `Agent`의 explicit `model`과 지원되는 `effort` | task/agent transcript가 노출한 model |
| `codex` | spawned agent의 explicit model/reasoning effort override | spawned-agent event/usage가 노출한 model |
| `hermes-agent` | configured `delegation.model`; class별 control이 필요하면 새 `hermes -z -m <selector> --reasoning <effort> --usage-file <path>` 작업자 | usage 파일의 model |

Ledger에는 `model_class`, `requested_selector`, `realized_model`, `reasoning_effort`,
`worker_id`, `receipt_source`를 기록한다. Host가 realized model을 노출하지 않으면
`realized_model=unavailable`로 기록하고 requested selector에서 추론하지 않는다.

Delegated child report는 다음 정확한 receipt를 항상 반환한다. Worker identity의
canonical 소스는 child self-report가 아니라 parent가 받은 호스트 dispatch 표면다.
Child의 작업자 ID self-report는 선택적이며 `unavailable`이어도 된다. Parent는 dispatch
직후 호스트 작업자 ID/handle과 receipt 소스를 장부에 기록한다. 빈 `Plan deviations`는
미보고이며 `none` 리터럴만 no-deviation이다.

```text
Frozen receipt: strategy=<delegated> model_class=<class> requested_selector=<selector> owned_paths=<exact list>
Host dispatch receipt: worker_id=<host id or handle> receipt_source=<host dispatch surface>
Actual receipt: strategy=<actual> model_class=<actual> requested_selector=<actual> changed_paths=<exact list>
Plan deviations: none | transient-self-corrected:<field; frozen; transient; restored; reason> | scope-violating:<field; frozen; published; reason>
```

Parent가 delegated를 freeze했으면 호스트 dispatch receipt가 없거나 실제 strategy가
direct인 결과는 정상이어도 contract violation이다. model class, selector, changed 경로도
frozen receipt와 정확한 compare한다. `transient-self-corrected`는 parent가 ancestry,
published diff/tree, frozen 범위, intended changes와 필수 checks를 독립적으로 다시
읽어 net effect 0을 입증한 경우에만 recorded deviation으로 허용한다. 그 외 mismatch,
빈 deviation 또는 `scope-violating`은 `Pass`가 아니다.

## 실행 전략

각 단위는 `direct` 또는 `delegated` 중 하나의 명시적 실행 strategy를 기록한다.

| 전략 | 실행자 | 허용 조건 |
| --- | --- | --- |
| `direct` | 현재 호스트 context가 일시적으로 단위 실행자 역할을 하며 subagent를 spawn하지 않는다. | 사용자가 `--direct` 를 전달하거나 표시된 계획 recommendation `strategy=direct` 를 승인하고, 단위가 하나의 bounded 독립 실행 `tk-drive` 또는 독립 실행 `tk-pr-respond` 구현일 때이다. |
| `delegated` | 새 작업자 하나가 bounded 단위 brief를 받는다. | 새 context, isolation, 독립적인 작업자, 검토자 handoff, design-heavy reasoning 또는 parent `tk-pr-sweep` 경로가 필요할 때이다. |

isolation obligation이 없는 bounded known-pattern 구현에서는 Prepare가 단일
`👍 Recommendation:` 승인 표면에서 `strategy=direct` 를 권고한다. Direct는
이미 실행 중인 session model을 그대로 사용하므로 model class/selector/effort 선택을
붙이지 않으며 `cheapest | standard | strongest`를 model, class, tier 등 다른
label로도 direct에 연결하지 않는다. 승인과 장부에는 `model_class=n/a`,
`requested_selector=n/a`,
`realized_model=<host-exposed session model | unavailable>`,
`reasoning_effort=inherited`를 기록한다. `tk-drive` 에서는 이것이 기본
recommendation이며 독립 실행 `tk-pr-respond` 도
단위에 isolation 또는 다른 delegated-only boundary가 필요하지 않은 한 같은 권고를 쓴다.
표시한 계획의 승인은 explicit strategy 승인이므로 두 번째 direct confirmation을
요청하지 않는다. `--direct` 는 같은 strategy를 미리 선택한다. 사용자가 delegated를
선택하면 그 선택을 따른다. 이것은 controller 대체 경로이 아닌 역할 인계다. 편집 중에는
현재 context가 단위 실행자이며 frozen 단위 경로만 건드릴 수 있다. 범위 확장,
다른 단위 생성, 승인/장부 소유자 변경 또는 원격 발행은 할 수 없다. 후보가
준비되면 소유 controller가 검증과 mechanical bookkeeping을 재개한다.

`direct`는 `unavailable` delegated 작업자의 암묵적 대체 경로가 될 수 없다. 승인된
strategy가 `delegated` 이면 사용할 수 없는 작업자는 `Blocked` 로 남는다. `tk-pr-sweep` 는
multi-PR isolation과 중첩된-소유자 boundary를 하나의 direct 실행자로 대체할 수 없어
delegated-only다.

Direct 실행은 현재 호스트 context를 상속하므로 호스트가 제공하는 것보다 낮은
model을 주장하지 않는다. Subagent, SDD 검토자, session model routing을 사용하지 않고
focused 검증과 self-review만 수행한다. 독립 검토는 사용자/저장소 정책
또는 acceptance uncertainty가 명시적으로 요구할 때만 계획한다.

## Dispatch 권한 및 실패

`tk-drive` 는 `user-invoked` 이며 `disable-model-invocation: true` 를 가진다. 명시적
`/tk-drive` 또는 `$tk-drive` 호출은 스킬의 승인된 실행 strategy에 대한
사용자 요청이다. 또한 user 요청 뒤에만 AgentTool을 허용하는 호스트 제한도
충족한다. approved delegated run을 direct execution으로 되돌리지 않는다. 호스트가 사용 가능한
`general-purpose` 작업자를 spawn할 수 없으면 **spawn 전에** `Blocked`로 중단한다.
반환된 `general-purpose` label은 정상 결과이므로 사후에 tier 차단을 시도하지 않는다.

누락된 컨텍스트가 제공된 뒤에도 입증된 reasoning 또는 complexity 실패가 남을 때만
에스컬레이션한다. Escalation은 한 단계 강한 새 작업자를 쓰며 bounded이고 무제한 재시도
루프가 아니다.

각 새 작업자 brief에는 단위 하나, 정확한 R/AC, 소스/티켓 범위, 범위/exclusion,
검증 obligation 및 현재 Git 소유권 사실이 들어간다. 다음
먼저 현재 대상 checkout에서 `git rev-parse --show-toplevel`로 `<repository-root>`를
resolve한 뒤, 저장소 루트에서 파생한 absolute 경로를 실제 결과로 치환해 그대로
포함해야 한다:

```text
<repository-root>/.tigerkit/drive.md
<repository-root>/.tigerkit/spec.md
<repository-root>/.tigerkit/tickets.md
<repository-root>/.tigerkit/implement.md
```

brief는 문서 본문을 복사하지 않고 소스/티켓 범위를 식별한다. implementer와
검토자는 각각 report/diff package 경로를 받는다. 무관한 소스, 장황한 이력,
child receipt, secret 또는 다른 워크플로의 authority를 중첩하지 않는다.
