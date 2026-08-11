---
name: tk-pr-respond
description: "[user/auto] 하나의 pull request에서 선택한 feedback 또는 지원되는 GitHub Actions failure를 하나의 승인된 plan, direct 또는 fresh-worker unit, acceptance verification, 제한된 publication으로 해결합니다."
disable-model-invocation: false
argument-hint: "<pull request or repository> [--ci] [--direct]"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# 하나의 pull request에 응답

`/tk-pr-respond`, `$tk-pr-respond`, host skill picker, 또는 active `tk-pr-sweep` 의
fresh exact-PR handoff를 통해서만 시작한다. generic review, implementation, triage,
continuation, 또는 둘 이상의 PR에는 절대 활성화하지 않는다.

Respond는 한 PR의 feedback/supported-CI plan, `direct` 또는 `delegated` unit 실행,
acceptance verification, bounded push/reply/resolve/re-review/summary를 소유한다. Respond는
controller다. Delegated strategy에서는 **product, test, configuration 변경을 직접
작성하지 않는다.** 모든 primary 또는 corrective edit는 하나의 bounded resolution
unit으로 fresh worker에게 보낸다. Standalone `--direct` 또는 그와 동등한 approved
direct plan에서는 current context가
승인된 한 unit의 executor 역할을 맡고 frozen owned paths만 수정한다. 이는
controller fallback이 아니며 nested Sweep handoff에는 사용할 수 없다. required
verification과 gap closure가 통과한 뒤에만 controller가 각 unit의 mechanical
staging과 verified commit 하나를 소유할 수 있다. usable worker가 없으면 delegated
plan을 direct로 뒤집지 않고 `Blocked` 로 끝낸다.

## 권한과 ledger(Authority and ledger)

Standalone Respond는 `.tigerkit/pr-respond.md` 를 원자적으로 대체하고 다시 읽는다.
PR/repository/head/refspec, current finding IDs, R/AC, scope와 exclusions, controller가
근거와 함께 해결한 assumptions, units/waves, verification, approved publication
actions, worker/correction/commit evidence, thread actions, 최종 관찰 PR state와
fresh `general-purpose` implementer/reviewer의 brief/report/diff/verdict를 기록한다.
Delegated unit이면 optional `.tigerkit/session.md` routing source와 `model_class`,
`requested_selector`, `realized_model`, `reasoning_effort`, `worker_id`,
`receipt_source`도 기록한다. 미노출 값은 `unavailable`로 둔다.
secret, transcript, full log는 저장하지 않는다.

Sweep 아래에서 호출되면 `pr-respond.md`, child ledger, 기타 Markdown lifecycle file을
**절대 작성하지 않는다.** owning `.tigerkit/pr-sweep.md` 에 compact evidence를 반환한다.
Artifact가 있다고 authority가 생기지는 않는다.

## 생명주기(Lifecycle)

```text
Prepare -> Execute -> Close gaps -> Finalize
```

### 준비(Prepare)

1. 정확히 하나의 open PR을 fresh-read한다: repository, authenticated user, author,
   branch/base, head ref/SHA, draft state, checks, reviews, comments, threads,
   requested reviewers, exact push refspec. pagination을 완료한다. missing,
   mixed-PR, author/login-mismatched, ambiguous identity는 mutation 전에 `Blocked`다.
2. superseded iteration을 억제하고 각 current finding 또는 supported
   GitHub Actions failure를 `apply | reply | defer` 로 분류한다. exact IDs, bounded
   quote/summary, requested outcome, R/AC, scope, exclusions, reply draft,
   verification을 보존한다. External/unknown-provider CI는 report-only다. queued,
   cancelled, flaky, infrastructure, inaccessible failure는 code change를 정당화하지
   않는다.
3. evidence로 ordinary reversible ambiguity를 해결한다. 모든 material assumption과
   그 basis, behavior-changing alternative를 기록한다. user-owned decision이 safe
   executable plan을 막을 때만 `tk-grill-me` 를 사용한다.
4. independently verifiable resolution unit과 dependency wave를 도출한다. coupled
   또는 uncertain work는 serialize한다. concurrent unit에는 host-provided isolated
   checkout/worktree와 proven independence가 필요하다. scheduler를 만들지 않는다.
5. `skills/tk-drive/references/worker-dispatch.md` 의 canonical worker-dispatch
   contract에 따라 unit별 `direct | delegated` strategy와 최소 model을 선택한다.
   ticket 또는 approved plan의 `model`/`effort`는 plan metadata로 보존한다. 격리 의무가
   없는 bounded known-pattern unit이면 `strategy=direct`, `model=cheapest`를 우선
   추천하고, fresh context·isolation·reviewer handoff·design-heavy reasoning이
   필요하면 `delegated`와 그 근거를 추천한다. Delegated는 fresh `general-purpose`
   implementer와 task reviewer를 함께 사용한다. active-host `.tigerkit/session.md` routing이
   있으면 spawn 전에 사용하고, 없으면 exact Markdown addition을 같은 approval surface에
   제안하며 approval 전에는 파일을 쓰거나 dispatch하지 않는다.
   `general-purpose` 반환은 정상 결과다. Parent Sweep의 `--ci` handoff는 항상
   delegated이며 direct strategy로 바꾸지 않는다. `👍 Recommendation:` 에 strategy와
   model을 포함하고, 사용자가 표시된 plan을 승인하면 그것이 direct strategy에 대한
   명시적 승인이다. 별도 direct 확인은 묻지 않는다.
6. goal/PR/head, included/excluded findings, apply/reply/defer decisions, R/AC,
   units/waves, verification, exact bounded `push`/reply/resolve/re-review/summary actions,
   risks, assumptions/ambiguities를 포함한 compact approval surface 하나를 준비한다. 이것이
   유일한 normal approval이다.

`🙋 respond · 응답 필요` 하나를 emit하고, 정확히 하나의 `👍 Recommendation:` 을 보여주고,
approval question을 묻는다. approval 전에는 worker dispatch, commit, remote write를
하지 않는다. Approval은 표시된 snapshot과 Respond의 existing bounded authority만
승인한다. listed publication도 승인하므로 **두 번째 publication question을 절대 묻지 않는다.**

`--ci` 는 explicit invocation 또는 parent Sweep handoff가 equivalent exact
PR/head/finding/route, verification, publication bound를 이미 제공할 때만 interactive
checkpoint를 건너뛴다. Sweep `test-only` route는 repository의 existing test layout만
허용하며 production, configuration, dependency/lockfile, security/data/performance,
weakened-assertion 변경을 금지한다. Out-of-bound work는 worker dispatch 전에
`Blocked`다.

Material PR head/thread/check/identity/refspec, source, scope, verifier,
irreversible-decision drift는 approval을 무효화하고 Prepare로 돌아가게 한다. 변경되지
않은 plan은 routine checkpoint를 다시 받지 않는다.

### 실행(Execute)

각 dependency wave마다 frozen strategy를 적용한다. delegated unit은 fresh
`general-purpose` implementer가 맡고, standalone direct unit은 current context가
단 하나의 bounded executor로 맡는다.
Executor에는 ID/goal, exact PR finding과 R/AC IDs, scope/exclusions, relevant paths,
verification, Git ownership facts와 task brief/report path를 준다. Implementer는 질문을
먼저 내고 자기 unit만 구현하며, focused checks·self-review·commit 후 report를 반환한다.
Direct unit은 여기서 subagent 없이 controller에 candidate를 반환한다. Delegated unit만
fresh `general-purpose` reviewer가 diff package를 읽고 `Spec compliance`와 `Task
quality`를 판정하기 전에는 완료하지 않는다. requested selector와 host가 노출한 realized
model receipt를 기록하고, 미노출 값은 `unavailable`로 둔다. `general-purpose` label
자체는 실패가 아니다.

다음 불변식을 사용한다:

```text
candidate -> required tests/checks/browser verifier -> Close gaps
          -> bounded fresh correction when needed -> one verified unit commit
```

Required verifiers는 final uncommitted candidate에서 실행한다. direct unit의 gap fix는
같은 frozen unit과 owned paths 안에서만 수행하고, delegated unit의 gap fix는 새 worker를
사용한다. escalation 전에 missing context를 제공하고, demonstrated reasoning failure에는 한 단계 강한 fresh worker를 배정한다. corrective round는 최대 세 번을
선호하며 unchanged failure를 무기한 retry하지 않는다. proven owned paths만 stage하고
pre-existing user changes를 보존한다.

integration conflict는 independence를 반증한다. concurrent integration을 중지하고
serialize하거나 Prepare로 돌아간다. worker는 semantic merge를 지어내지 않는다.

repository-caused GitHub Actions에서는 fresh failure read와 fix 한 번이 한 cycle이다.
exact push 뒤에는 freshly observed just-pushed head만 promote하고 relevant checks를 모두
rerun한다. corrective cycle 세 번 뒤에 중지한다. interactive CI workflow를 automatic
children으로 절대 invoke하지 않는다.

### 공백 닫기(Close gaps)

모든 approved finding/R/AC를 `satisfied`, `missing`, `partial`, 또는 `unverifiable` 로
분류한다. approved scope/exclusions, skipped units, externally visible behavior, required
verifier evidence, commit ancestry/ownership, freshness만 확인한다. 이것은 general code
review가 아니다. verdict를 확정할 수 없으면 같은 narrow brief를 가진 stronger fresh
non-mutating reviewer를 최대 한 명 사용한다. required-but-unavailable independent review는
`Unverifiable`다. correction은 여전히 fresh worker에게 보낸다.

### 최종화 및 발행(Finalize and publish)

Delegated unit이 하나라도 있거나 approved plan이 independent final review를 요구할 때만
fresh `general-purpose` whole-PR reviewer를 한 번 dispatch해 전체 diff의 Spec/AC와
품질을 확인한다. all-direct run은 aggregate checks와 self-review만 사용한다. delegated
review finding이 있으면 하나의 fresh corrective worker와 한 번의 scoped re-review만
수행하고, load-bearing residual은 `Blocked`로 남긴다.
모든 selected unit이 gap을 close한 뒤 repository identity, local `HEAD`, PR head/ref/open
state, checks, threads를 fresh-read한다. 변경되지 않은, 이미 approved된 action만 다음
순서로 publish한다.

1. 검증된 commit이 있을 때 정확한 branch를 push한다.
2. 현재 finding별로 정확히 reply한다.
3. reply가 성공한 뒤 fresh verification을 거친 thread만 resolve한다.
4. GraphQL `reviewThreads`를 끝까지 paginate해 review/thread/check/mergeability를
   fresh-read한다. 하나라도 unresolved이면 완료나 waiting-for-review로 판정하지 않고
   exact thread evidence와 함께 open unit으로 유지한다.
5. author, authenticated user, bot 및 여전히 유효한 approver를 제외하고 조건부 human re-review를 한다.
6. PR summary는 최대 하나만 작성한다.

## Terminal branch contract

아래 terminal branch 중 하나에 도달하면 해당 상태를 기록하고 그 branch의 후속 조치만
수행한다. 다른 branch를 추정하거나 `Pass` 로 승격하지 않는다.

| 조건 | 즉시 조치 | Status |
|---|---|---|
| approval question 또는 user-owned decision 대기 | worker, commit, remote write를 하지 않고 표시된 snapshot을 유지한다 | `Pending` |
| identity, authority, freshness, scope 또는 `--ci` boundary가 unresolved | mutation 전에 멈추고 정확한 blocker를 기록한다 | `Blocked` |
| required evidence 또는 independent review를 사용할 수 없음 | finding/unit을 open으로 유지하고 판정을 확정하지 않는다 | `Unverifiable` |
| partial remote write 또는 approved operation failure | remote를 다시 읽어 적용된 상태만 보고하고 임의 retry하지 않는다 | `Fail` |
| 모든 selected unit이 gap을 close하고 모든 inline thread가 resolved이며 approved action 및 fresh final-read가 완료됨 | exact result와 remaining checks만 보고한다 | `Pass` |

Sweep 아래에서는 one-summary budget을 consume하고, 이미 consume했으면 draft를 반환한다.
모든 generated external comment는 정확히
`_🤖 본 코멘트는 AI가 작성했습니다._` 로 끝난다. failed reply는 thread를 open으로 남긴다.
Deferred, failed, partial, unverifiable finding은 open으로 유지한다. force-push, merge,
unrelated thread close, bot review request, draft ready 표시, tag, release, release
publish는 절대 하지 않는다.

최종 PR을 fresh-read한다. partial remote write는 `Fail`; required evidence가 없으면
`Unverifiable`; authority/identity/freshness conflict는 `Blocked`; approved scope가
complete면 `Pass`다. nested run은 Sweep에 compact evidence만 반환한다. Standalone
output은 `## PR respond` 로 시작하고 정확히 하나의
`Status: Pass | Fail | Blocked | Unverifiable | Pending` line을 포함한다. worker
receipts와 raw logs는 생략하며, canonical IDs, statuses, commands, paths, exact literals를
보존한 채 사용자의 언어를 사용한다.
