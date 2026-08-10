---
name: tk-drive
description: "[user] 하나의 승인으로 product-change source를 준비하고, fresh-worker로 실행해 acceptance gap을 닫고, 검증된 unit commit과 finalization까지 수행한다."
disable-model-invocation: true
argument-hint: "<source, request, issue, or approved active run>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# Drive 실행

사용자가 `/tk-drive`, `$tk-drive`, 또는 source가 포함된 host skill picker를
명시적으로 선택했을 때만 시작한다. source 없이 다시 호출하면, 같은 대화에서
현재 source, ledger, Git, repository 근거가 하나의 approved 또는 pending run을
명확히 가리킬 때만 재개한다. 일반 요청, artifact, 새 session은 Drive를
시작하거나 재개하지 않는다.

## 권한과 불변식

승인된 plan 하나로 preparation, fresh-worker mutation, required verification,
승인된 unit마다 하나의 verified current-branch commit, 최대 세 번의 corrective
round, aggregate verification, finalization을 수행할 수 있다. push, PR, merge,
tag, release, publish, history rewriting은 포함하지 않는다.

Drive는 controller다. **product, test, configuration change를 직접 작성하지
않는다.** 모든 primary 및 corrective mutation은 하나의 bounded unit을 맡은
fresh worker에게 보낸다. 이 skill은 user-invoked이므로 명시적 `/tk-drive` 또는
`$tk-drive` 호출 자체가 host의 user-requested AgentTool 조건을 충족한다.
Mechanical Git bookkeeping은 final candidate가
통과한 뒤에만 controller가 맡을 수 있다. Host가 사용할 수 있는 worker를
dispatch하지 못하면 `Blocked`로 중단한다. 절대 controller edit으로 fallback하지
않는다. Worker는 다른 user-owned TigerKit workflow를 orchestrate하거나
호출하지 않는다.

## 생명주기(Lifecycle)

```text
Prepare -> Execute -> Close gaps -> Finalize
```

Drive가 이 lifecycle을 소유한다. Child receipt는 내부 자료이며 `continue`,
`/clear`, model switching, second invocation을 요구하지 않는다. Host/process
boundary를 지난 뒤에는 cursor나 lifecycle claim이 아니라 새 근거에서 다음
행동을 도출한다.

## 준비(Prepare)

1. Complete source와 적용되는 repository instruction을 읽는다. Branch,
   baseline `HEAD`, worktree, pre-existing dirty paths, 그리고 관련 durable
   prior-art를 최대 일곱 개까지 기록한다.
2. Evidence와 safe default로 되돌릴 수 있는 ambiguity를 해결한다. 모든
   material controller choice, 근거, behavior-changing alternative를 기록한다.
   User-owned decision이 안전한 executable plan을 막을 때만 `tk-grill-me`를
   호출한다. 질문이 pending인 동안에는 `🙋 drive > grill-me · 응답 필요`를
   출력하고 worker를 dispatch하지 않는다. Bounded comparison으로 해당
   결정을 닫을 수 있을 때만 `tk-prototype`을 사용한다.
3. Source anchor, scope, exclusion, frozen user-visible literal, verification
   obligation을 포함해 Ready requirement와 acceptance criteria를 작성한다.
4. 독립적으로 검증 가능한 `1..N` unit, dependency graph, wave를 도출한다.
   Coupled하거나 불확실한 unit은 serialize한다. Host가 이미 isolated
   checkout/worktree를 제공하는 경우에만 proven-independent unit을 parallelize한다.
   Scheduler를 만들거나 worker가 mutable worktree를 동시에 공유하게 하지 않는다.
5. Test/check와 browser verification을 분류한다. Browser-visible AC라면 exact
   scenario, target, non-sensitive auth mode, prerequisite, limitation을
   계획한다. 그 외에는 `not-required`로 기록한다. Required headless auth를
   사용할 수 없으면 mutation 전에 `Unverifiable`이다.
6. [worker-dispatch.md](references/worker-dispatch.md)에 따라 dispatch에 필요한
   최소 tier를 선택한다.
7. [ledger.md](references/ledger.md)에 따라 `.tigerkit/drive.md`의 current task를 atomically
   replace하고 reread한 뒤 하나의 compact approval surface를 제시한다. Plan record는
   `Repository (branch/HEAD/dirty paths)`, `Source / Goal (anchor)`, `Scope / Exclusions`,
   `Frozen literals`, `R/AC`, `Units / Waves (ownership)`, `Verification (tests/browser/auth)`,
   `Risks / Assumptions`, `Bounded external actions`, `Ledger / Approval`을 각각 한 번 소유하며,
   unknown은 `unavailable`로 둔다. 이는 별도 lifecycle output이 아닌 approval evidence이다.

Approval question이 action surface다. `🙋 drive · 응답 필요`를 한 줄 출력하고
정확히 하나의 `👍 Recommendation:`을 보여 준다.
Approval은 표시된 snapshot에만 적용된다. Material source, scope, branch/head,
remote-state, verifier-prerequisite, irreversible-decision drift가 생기면
승인은 무효가 되어 Prepare로 돌아간다. Plan이 변하지 않았다면 routine
second approval을 받지 않는다.

## 실행(Execute)

각 dependency wave마다 unit 하나를 맡은 fresh worker를 dispatch한다. Worker에게는
ID/goal, exact R/AC, scope/exclusion, 관련 path, verification obligation,
branch/head/diff ownership만 전달한다. Worker는 현재 근거를 확인하고 해당
unit만 구현하며 focused check를 실행한다. 그 뒤 하나의 bounded
behavior-preserving simplify/reuse pass를 수행하고 changed paths, candidate
evidence, unresolved item을 반환한다. 다음 불변식을 지킨다.

```text
candidate -> required tests/checks/browser verifier -> Close gaps
          -> bounded fresh correction when needed -> one verified unit commit
```

Required verifier는 commit 전에 final candidate를 대상으로 실행한다. Proven
owned path만 stage하고 pre-existing user change를 보존한다. Isolated gap이
있으면 fresh corrective worker를 dispatch하고 영향받은 obligation을 다시
실행한다. 최대 세 round를 우선한다. Missing context는 tier upgrade 없이
보충한다. Demonstrated reasoning failure가 있을 때만 다음 tier의 fresh
worker를 한 번 사용한다. 변하지 않거나, 원인을 격리할 수 없거나, 충돌하거나,
scope를 넓히는 failure가 반복되면 mutation을 중단한다.

Integration conflict는 independence가 틀렸다는 뜻이다. 영향받은 unit을
serialize하거나 다시 Prepare한다. Worker는 semantic merge를 임의로 만들지
않는다. Isolation, integration order, stale-base/conflict detection, cleanup은
Drive가 소유한다.

## 공백 닫기(Close gaps)

승인된 각 R/AC에 대해 관찰된 evidence를 `satisfied`, `missing`, `partial`,
`unverifiable` 중 하나로 분류한다. Acceptance와 관련된 scope/exclusion,
unit, verifier, externally visible behavior, commit/ancestry, dirty-path
ownership, evidence freshness만 확인한다. 그 acceptance 사실과 무관한
finding은 생략한다.

Evidence만으로 confident verdict를 낼 수 없을 때는 동일한 좁은 R/AC brief를
사용하는 stronger fresh non-mutating reviewer를 최대 한 번 dispatch한다.
User/repository policy가 independent review를 요구할 때만 사용 가능한
built-in 또는 third-party reviewer를 쓴다. Required review를 사용할 수
없으면 `Unverifiable`이다. 모든 fix는 여전히 fresh corrective worker에게
보낸다.

## 최종화(Finalize)

모든 verified unit commit 뒤에 aggregate R/AC traceability, repository check,
ancestry, exclusion, freshness를 다시 확인한다. Unit commit, verifier/gap
evidence, corrective round, aggregate result, recovery fact를 포함하도록
`.tigerkit/drive.md`를 갱신한다. Non-success면 mutation을 동결하고
[non-success-finalization.md](references/non-success-finalization.md)를 따른다.

Success면 concise behavior result, 유용한 unit commit, aggregate verification
한 개에서 네 개, 정확히 `Status: Pass`를 출력한다. Active run의 terminal
response는 Drive만 출력한다. Child receipt, raw log, dispatch tier,
progress marker는 생략한다.
