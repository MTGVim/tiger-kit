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

`/tk-pr-respond`, `$tk-pr-respond`, host skill picker 또는 active `tk-pr-sweep`의
fresh한 정확한 PR handoff로만 시작한다. `generic` review, 구현, `triage`,
continuation 또는 둘 이상의 PR에는 절대 활성화하지 않는다.

Respond는 한 PR의 feedback/지원 CI 계획, `direct` 또는 `delegated` unit 실행,
acceptance verification, 제한된 push/reply/resolve/re-review/summary를 소유한다.
Respond는 controller다. `delegated` 전략에서는 **product, test, configuration 변경을
직접 작성하지 않는다.** 모든 primary 또는 corrective edit는 하나의 제한된 resolution
unit으로 fresh worker에게 보낸다. Standalone `--direct` 또는 동등하게 승인된
direct 계획에서는 current context가 승인된 한 unit의 executor가 되어 frozen owned
paths만 수정한다. 이는 controller fallback이 아니며 nested Sweep handoff에는 사용할
수 없다. required verification과 gap closure가 통과한 뒤에만 controller가 각 unit의
mechanical staging과 verified commit 하나를 소유할 수 있다. usable worker가 없으면
delegated 계획을 direct로 바꾸지 않고 `Blocked`로 끝낸다.

## 권한과 장부

Standalone Respond는 `.tigerkit/pr-respond.md`를 원자적으로 대체하고 다시 읽는다.
PR/repository/head/refspec, current finding ID, R/AC, scope와 exclusions, controller가
근거와 함께 해결한 assumption, units/waves, verification, approved publication
action, worker/correction/commit evidence, thread action, 최종 관찰 PR state와
fresh `general-purpose` implementer/reviewer의 brief/report/diff/verdict를 기록한다.
`delegated` unit이면 optional `.tigerkit/session.md` routing source와 `model_class`,
`requested_selector`, `realized_model`, `reasoning_effort`, `worker_id`,
`receipt_source`도 기록한다. 미노출 값은 `unavailable`로 둔다. secret, transcript,
full log는 저장하지 않는다.

Sweep 아래에서 호출되면 `pr-respond.md`, child ledger, 기타 Markdown lifecycle file을
**절대 작성하지 않는다.** owning `.tigerkit/pr-sweep.md`에 compact evidence를 반환한다.
Artifact가 있다고 authority가 생기지는 않는다.

## 생명주기

```text
Prepare -> Execute -> Close gaps -> Finalize
```

### 준비(Prepare)

1. 정확히 하나의 open PR을 fresh-read한다: repository, authenticated user, author,
   branch/base, head ref/SHA, draft state, checks, reviews, comments, threads,
   requested reviewers, 정확한 push refspec. pagination을 완료한다. missing,
   mixed-PR, author/login-mismatched, ambiguous identity는 mutation 전에 `Blocked`다.
2. superseded iteration을 억제하고 각 current finding 또는 지원되는
   GitHub Actions failure를 `apply | reply | defer`로 분류한다. 정확한 ID, 제한된
   quote/summary, requested outcome, R/AC, scope, exclusions, reply draft,
   verification을 보존한다. external/unknown-provider CI는 report-only다. queued,
   cancelled, flaky, infrastructure, inaccessible failure는 code change를 정당화하지
   않는다.
3. evidence로 되돌릴 수 있는 일반 ambiguity를 해결한다. 모든 material assumption과
   근거, behavior-changing alternative를 기록한다. user-owned decision이 안전한
   executable plan을 막을 때만 `tk-grill-me`를 사용한다.
4. independently verifiable resolution unit과 dependency wave를 도출한다. coupled
   또는 uncertain work는 serialize한다. concurrent unit에는 host-provided isolated
   checkout/worktree와 proven independence가 필요하다. scheduler를 만들지 않는다.
   `browser-visible` R/AC 검증은 `tk-browser-verify`에 `handoff`하며, 개발 서버가
   필요하면 정확한 `command`/`cwd`/대상 URL/`auth mode`/`readiness` 조건을 함께
   전달한다. `Respond`/`controller`/`worker`는 브라우저 도구나 개발 서버를 직접
   시작·대기·종료하지 않고 `verifier` 결과 전에는 `commit`하지 않는다.
5. `skills/tk-pr-respond/references/worker-dispatch.md`의 canonical worker-dispatch
   contract에 따라 unit별 `direct | delegated` strategy와 최소 model을 선택한다.
   ticket 또는 approved plan의 `model`/`effort`는 plan metadata로 보존한다. 격리 의무가
   없는 bounded known-pattern unit이면 session model을 유지하는 `strategy=direct`를
   우선 추천하고, fresh context·isolation·reviewer handoff·design-heavy reasoning이
   필요하면 `delegated`와 그 근거를 추천한다. `delegated`는 fresh `general-purpose`
   implementer와 task reviewer를 함께 사용한다. active-host `.tigerkit/session.md` routing이
   있으면 정본
   `skills/tk-pr-respond/references/worker-dispatch.md#session-model-routing` schema로
   검증해 `spawn` 전에 사용한다. 파일 또는 `current-host section`이 없고 세 `class`의
   제어값이 모두 확인되면 중첩 `class`별 정확한 Markdown `block`을 스스로
   `.tigerkit/session.md`에 초안 생성하고 `Status: Pending`으로 둔다. 기존 불완전·
   충돌 `block`은 덮어쓰지 않고 보정안을 제안한다. `routing_state=review-required`를
   기록하며 승인 전에는 파일 외의 `dispatch`, 제품, Git, `remote`를 변경하지 않는다.
   사용자가 초안을 검토·승인한 뒤에만 `Status: Ready`로 바꾸고 `reread`해 `spawn`한다.
   `actionable delegated unit`의 `model class`, `selector`, `effort`, `routing source`가 승인 화면에
   모두 보여야 한다.
   Model class/selector/effort 선택은 `delegated` 전용이다. Direct approval과 ledger에는
   `cheapest | standard | strongest` tier를 어떤 label로도 붙이지 않고
   `model_class=n/a`, `requested_selector=n/a`, host가 노출한 session `realized_model` 또는
   `unavailable`, `reasoning_effort=inherited`를 기록한다.
   `general-purpose` 반환은 정상 결과다. Parent Sweep의 `--ci` handoff는 항상
   `delegated`이며 direct strategy로 바꾸지 않는다. 첫 호출에서는 mutation 없이 parent가
   준 frozen strategy/model class/selector/owned paths를 정확한 `Frozen receipt`로 되돌리고
   `Preflight only`에서 멈춘다. Parent가 exact match를 확인해 같은 child를 resume한 뒤에만
   worker를 dispatch한다. fresh worker를 만들 수 없으면 direct edit가 아니라 `Blocked`다.
   Parent는 host dispatch surface의 worker ID/handle을 canonical identity로 기록하며
   child self-report ID는 optional이다. 완료 report에는 canonical worker-dispatch의 `Actual receipt`와
   `Plan deviations: none | ...`을 반드시 포함한다. `👍 Recommendation:`에는 strategy와
   `delegated`일 때만 model을 포함하고, 사용자가 표시된 plan을 승인하면 그것이 direct strategy에 대한
   명시적 승인이다. 별도 direct 확인은 묻지 않는다.
6. goal/PR/head, included/excluded finding, apply/reply/defer decision, R/AC,
   units/waves, verification, 정확히 제한된 `push`/reply/resolve/re-review/summary action,
   risk, assumption/ambiguity를 포함한 compact approval surface 하나를 준비한다. 이것이
   유일한 일반 approval이다.

`🙋 respond · 응답 필요` 하나를 emit하고, 정확히 하나의 `👍 Recommendation:`을 보여주고,
approval question을 묻는다. approval 전에는 worker dispatch, commit, remote write를
하지 않는다. Approval은 표시된 snapshot과 Respond의 기존 bounded authority만 승인한다.
listed publication도 승인하므로 **두 번째 publication question을 절대 묻지 않는다.**

`--ci`는 explicit invocation 또는 parent Sweep handoff가 동등한 정확한
PR/head/finding/route, verification, publication bound를 이미 제공할 때만 interactive
checkpoint를 건너뛴다. Sweep `test-only` route는 repository의 existing test layout만
허용하며 production, configuration, dependency/lockfile, security/data/performance,
weakened-assertion 변경을 금지한다. Out-of-bound work는 worker dispatch 전에
`Blocked`다.

Material PR head/thread/check/identity/refspec, source, scope, verifier,
irreversible-decision drift는 approval을 무효화하고 Prepare로 돌아가게 한다. 변경되지
않은 plan은 routine checkpoint를 다시 받지 않는다.

### 실행(Execute)

각 dependency wave마다 frozen strategy를 적용한다. `delegated` unit은 fresh
`general-purpose` implementer가 맡고, standalone direct unit은 current context가
단 하나의 bounded executor로 맡는다.
Executor에는 ID/goal, 정확한 PR finding과 R/AC ID, scope/exclusions, relevant path,
verification, Git ownership fact와 task brief/report path를 준다. Implementer는 먼저
질문하고 자기 unit만 구현하며, focused check·self-review·commit 후 report를 반환한다.
Direct unit은 여기서 subagent 없이 controller에 candidate를 반환한다. `delegated` unit만
fresh `general-purpose` reviewer가 diff package를 읽고 `Spec compliance`와 `Task
quality`를 판정하기 전에는 완료하지 않는다. requested selector와 host가 노출한 realized
model receipt를 기록하고, 미노출 값은 `unavailable`로 둔다. `general-purpose` label
자체는 실패가 아니다.

다음 불변식을 사용한다:

```text
candidate -> required tests/checks/browser verifier -> Close gaps
          -> bounded fresh correction when needed -> one verified unit commit
```

Required verifier는 final uncommitted candidate에서 실행한다. direct unit의 gap fix는
같은 frozen unit과 owned paths 안에서만 수행하고, delegated unit의 gap fix는 새 worker를
사용한다. escalation 전에 missing context를 제공하고, demonstrated reasoning failure에는
한 단계 강한 fresh worker를 배정한다. corrective round는 최대 세 번을 선호하며
unchanged failure를 무기한 retry하지 않는다. proven owned paths만 stage하고
pre-existing user change를 보존한다.

integration conflict는 independence를 반증한다. concurrent integration을 중지하고
serialize하거나 Prepare로 돌아간다. worker는 semantic merge를 지어내지 않는다.

repository-caused GitHub Actions에서는 fresh failure read와 fix 한 번이 한 cycle이다.
exact push 뒤에는 freshly observed just-pushed head만 promote하고 relevant check를 모두
rerun한다. corrective cycle 세 번 뒤에 중지한다. interactive CI workflow를 automatic
child로 절대 invoke하지 않는다.

### 공백 닫기

모든 approved finding/R/AC를 `satisfied`, `missing`, `partial` 또는 `unverifiable`로
분류한다. approved scope/exclusions, skipped unit, externally visible behavior, required
verifier evidence, commit ancestry/ownership, freshness만 확인한다. 이것은 일반 code
review가 아니다. verdict를 확정할 수 없으면 같은 narrow brief를 가진 stronger fresh
non-mutating reviewer를 최대 한 명 사용한다. required-but-unavailable independent review는
`Unverifiable`다. correction은 여전히 fresh worker에게 보낸다.

### 최종화 및 발행

`delegated` unit이 하나라도 있거나 approved plan이 independent final review를 요구할
때만 fresh `general-purpose` whole-PR reviewer를 한 번 dispatch해 전체 diff의 Spec/AC와
품질을 확인한다. all-direct run은 aggregate check와 self-review만 사용한다. `delegated`
review finding이 있으면 하나의 fresh corrective worker와 한 번의 scoped re-review만
수행하고, load-bearing residual은 `Blocked`로 남긴다.
모든 selected unit이 gap을 close한 뒤 repository identity, local `HEAD`, PR head/ref/open
state, check, thread를 fresh-read한다. 변경되지 않은 이미 approved된 action만 다음
순서로 publish한다.

1. 검증된 commit이 있을 때 정확한 branch를 push한다.
2. 현재 finding별로 정확히 reply한다.
3. reply가 성공한 뒤 fresh verification을 거친 thread만 resolve한다.
4. GraphQL `reviewThreads`를 끝까지 paginate해 review/thread/check/mergeability를
   fresh-read한다. 하나라도 unresolved이면 완료나 waiting-for-review로 판정하지 않고
   정확한 thread evidence와 함께 open unit으로 유지한다.
5. author, authenticated user, bot 및 여전히 유효한 approver를 제외하고 조건부 human
   re-review를 한다.
6. PR summary는 최대 하나만 작성한다.

## Terminal branch 계약

아래 terminal branch 중 하나에 도달하면 해당 상태를 기록하고 그 branch의 후속 조치만
수행한다. 다른 branch를 추정하거나 `Pass`로 승격하지 않는다.

| 조건 | 즉시 조치 | Status |
|---|---|---|
| approval question 또는 user-owned decision 대기 | worker, commit, remote write를 하지 않고 표시된 snapshot을 유지한다 | `Pending` |
| identity, authority, freshness, scope 또는 `--ci` boundary가 unresolved | mutation 전에 멈추고 정확한 blocker를 기록한다 | `Blocked` |
| required evidence 또는 independent review를 사용할 수 없음 | finding/unit을 open으로 유지하고 판정을 확정하지 않는다 | `Unverifiable` |
| partial remote write 또는 approved operation failure | remote를 다시 읽어 적용된 상태만 보고하고 임의 retry하지 않는다 | `Fail` |
| 모든 selected unit이 gap을 close하고 모든 inline thread가 resolved이며 approved action 및 fresh final-read가 완료됨 | 정확한 result와 남은 check만 보고한다 | `Pass` |

Sweep 아래에서는 one-summary budget을 consume하고, 이미 consume했으면 draft를 반환한다.
모든 generated external comment는 정확히
`_🤖 본 코멘트는 AI가 작성했습니다._`로 끝난다. failed reply는 thread를 open으로 남긴다.
Deferred, failed, partial, unverifiable finding은 open으로 유지한다. force-push, merge,
unrelated thread close, bot review request, draft ready 표시, tag, release 또는 release
publish는 절대 하지 않는다.

최종 PR을 fresh-read한다. partial remote write는 `Fail`; required evidence가 없으면
`Unverifiable`; authority/identity/freshness conflict는 `Blocked`; approved scope가
complete면 `Pass`다. nested run은 Sweep에 compact evidence만 반환한다. Standalone
output은 `## PR respond`로 시작하고 정확히 하나의
`Status: Pass | Fail | Blocked | Unverifiable | Pending` line을 포함한다. worker
receipt와 raw log는 생략하며, canonical ID, status, command, path, exact literal을
보존한 채 사용자의 언어를 사용한다.
