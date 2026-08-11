---
name: tk-pr-sweep
description: "[user] 승인된 multi-PR 유지보수 배치를 하나 준비·실행하거나, --report로 결정론적 분류만 읽기 전용으로 보고합니다."
argument-hint: "[--report] [--repo owner/name]..."
disable-model-invocation: true
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# Pull request Sweep(일괄 유지보수)

`/tk-pr-sweep`, `$tk-pr-sweep`, 또는 host skill picker로만 시작합니다. 일반 PR
상태 확인, 단일 PR 작업, release, continuation으로는 시작하지 않습니다. Sweep는
multi-PR orchestrator이며, one-PR Respond와 Rebase는 서로를 호출하지 않습니다.

## 결정론적 분류 및 보고 모드

초기·경로별·최종 classification에는 package-local `scripts/triage.mjs`를 직접
실행합니다. identity와 명시적 `--repo` 대상 또는
`$XDG_CONFIG_HOME/tigerkit/pr-triage.json`을 확인하고, 설정이 없으면 현재
origin을 bootstrap합니다. API failure로 classification이 되지 않을 때만 한 번
retry하며, partial snapshot을 합치거나 누락된 checks로 approval을 추론하지
않습니다.

`$tk-pr-sweep --report`는 triage를 한 번 실행하고 `지금 처리`, `검토 요청`,
`대기`로 그룹화해 클릭 가능한 evidence와 next action 하나를 보여준 뒤
반환합니다. approval을 묻지 않고 ledger/worktree/commit/route/GitHub write를
만들지 않으며, 허용된 state write는 config bootstrap뿐입니다.

## 권한 및 불변식

Interactive Sweep는 one plan/approval, `.tigerkit/pr-sweep.md`, isolation, frozen
routes, PR별 summary 하나, aggregate verification, finalization을 소유합니다.
product changes는 직접 작성하지 않으며, nested `tk-pr-respond --ci`가 모든
primary/corrective edit에 delegated fresh workers를 사용합니다. Sweep는 direct
execution flag를 받지 않으며, child authority를
확장하거나 merge, close, PR 생성, tag, release, publish를 수행할 수 없습니다.

```text
Prepare -> Execute -> Close gaps -> Finalize
```

## 준비(Prepare)

1. 새로 결정론적 triage를 실행하고 supplied queue, cached report, stale
   ledger, cursor는 무시합니다. identity, PR/base/head state, categories,
   checks/providers, reviews, comments, threads, requested reviewers를 확인합니다.
2. 모든 row를 actionable, held, report-only로 분류하고 closed router를 사용합니다.

   | 새 evidence | 제한된 route |
   | --- | --- |
   | 동일 repository의 base/head와 명확한 ownership에 정확히 일치하는 maintenance conflict | `tk-pr-rebase --ci` |
   | repository가 유발한 GitHub Actions failure | `tk-pr-respond --ci` |
   | 하나라도 unresolved인 inline review thread | `tk-pr-respond --ci` |
   | 현재 actionable feedback/reply | `tk-pr-respond --ci` |
   | 외부·unknown·unverifiable check, review request, draft 또는 waiting | report-only |

   safe ownership/refspec/scope/route가 없는 row는 hold합니다. Product fix는 exact
   scope와 fresh-worker verification route가 있을 때만 actionable로 취급하며,
   routine second “high-risk approval”은 유지하지 않습니다.
3. 되돌릴 수 있는 각 material assumption, 근거, behavior-changing alternative를
   기록합니다. planning이 user-owned decision으로 막힐 때만 `tk-grill-me`를
   사용합니다.
4. repository/PR/head/category/route/scope/risk/verification/actions와
   exclusions를 freeze합니다. proven independence와 host-provided isolation이
   함께 있을 때만 concurrency를 허용하고, wave를 도출합니다. uncertainty는
   serialize하며 scheduler는 만들지 않습니다. Actionable delegated row가 있으면
   optional `.tigerkit/session.md`의 active-host model routing을 읽습니다. 없거나
   incomplete이면 exact Markdown addition을 recommendation에 포함하고 approval 전에는
   파일을 쓰거나 child를 dispatch하지 않습니다.
5. `.tigerkit/pr-sweep.md`를 atomically replace한 뒤 reread합니다. actionable/held/report-only
   항목, 가정/모호성, 경로 웨이브, 검증, 위험, worktree 소유권,
   bounded remote actions와 `원격 변경: 아직 없음`을 파일에 보존합니다. 다음
   계획 증거 필드도 한 번씩 보존합니다: `저장소 범위`, `분류 기준`,
   `항목 (PR # | head SHA | category | route)`, `경로 / 웨이브`, `검증`,
   `위험 / 제외`, `Worktree 소유권`, `권한`, `승인`,
   `원격 변경: 아직 없음`, active-host routing source와 model class/selector. unknown은 `unavailable`로 두고
   route/authority를 추측하지 않습니다. 채팅에는 plan 전문이나 이 evidence fields를
   반복하지 않습니다.

   산출물의 설명과 heading은 한국어로 작성하고, machine-readable key·status·ID·
   command·path·URL·exact literal만 원문으로 유지합니다. 산출물에는 work `Status`와
   별도로 `Disposition: reported | applied | pending`을 기록합니다. atomic write와
   reread가 일치하면 `Disposition: applied`여도 approval 전 work `Status: Pending`은
   유지합니다. ledger가 missing/stale이거나 reread가 다르면 `Status: Blocked`,
   `Disposition: pending`으로 멈추고 recommendation, approval question, worktree,
   commit, remote mutation을 만들지 않습니다.

`🙋 sweep > plan · 응답 필요`를 하나만 emit하고, artifact의 absolute path와 `Status`,
`Disposition`, row/count 요약, 정확히 하나의 `👍 Recommendation:` 및 approval question만
표시합니다. 사용자는 artifact를 열어 전체 계획을 검토하며, 채팅에 전문을 복사하지
않습니다. approval 전에는 worktree/commit을 만들거나 remote write를 수행하지
않습니다. approval은 nested Respond/Rebase에 정확히 제한된 authority를 제공하며,
nested owner는 다시 묻지 않습니다.

기존 출력 호환성이 필요한 경우 compact report의 path label로 `PR sweep 계획`을,
remote 상태로 `원격 변경: 아직 없음`을 사용할 수 있습니다. 이는 full evidence
field dump가 아닙니다. material identity, PR head/state/category/scope/route,
verifier 또는 irreversible decision이 drift하면 해당 plan은 무효가 되어 Prepare로
돌아갑니다. 변경되지 않은 row에는 routine checkpoint를 다시 주지 않습니다.

## 실행(Execute)

frozen wave를 처리합니다. 각 row 전에 triage를 다시 실행하고 identity, PR state,
head/category/provider, refspec, threads, checks를 증명합니다. 이미 완료된 작업은
child/worktree 없이 `Skipped: already applied`로 처리합니다. external drift는
Prepare로 돌아가게 하며, sweep-owned verified head는 승인된 bound 안에서만
계속합니다.

mutation 전에 exact remote head를 fetch하고 증명합니다. exact clean owned
worktree만 재사용하고, 그렇지 않으면 Orca를 우선하며 unavailable일 때만 Git으로
fallback합니다. frozen/immutable setup은 한 번만 실행하고 package cache만
공유하며 dependency는 공유하지 않습니다.

current category마다 정확히 한 owner만 호출합니다. mutation이 있는
maintenance-rebase row는 `tk-pr-rebase --ci`를 fresh isolated worker/specialist로
dispatch해야 하며 Sweep controller 안에서 inline 실행하지 않습니다. host가
해당 worker를 dispatch할 수 없으면 local 또는 remote mutation 전에 row를
`Blocked`로 표시하며 direct fallback은 없습니다. frozen PR/head/route, finding
IDs, R/AC, 범위/제외, 검증, worktree 사실, 장부 소유자
`tk-pr-sweep`, summary budget을 전달합니다. Nested Respond, Rebase, workers,
reviewers, verifiers는 child Markdown ledger를 쓰지 않고 compact evidence를
`.tigerkit/pr-sweep.md`에 반환합니다. Controller와 nested Respond는 product edit를
작성하지 않으며, correction은 canonical policy
`skills/tk-drive/references/worker-dispatch.md`를 따르는 fresh worker를 사용합니다.
Worker preflight가 실패하면 row를 `Blocked`로 남기고, `general-purpose` worker label은
정상 role로 처리합니다. 각 delegated worker의 requested selector, host가 노출한
realized model, reasoning effort, worker ID와 receipt source를 장부에 기록하며 미노출
값은 `unavailable`로 둡니다.

각 child result 후 exact PR을 fresh-triage하고 `continue`를 묻지 않은 채 frozen
queue를 계속합니다. prompt-local bound를 유지합니다: exact base/head pair마다
rebase 한 번, GitHub Actions corrective cycle 최대 세 번, fresh head마다 feedback
response 한 번, sweep-owned follow-up head 최대 두 개입니다. 반복해서 unchanged
이거나 소진된 작업은 추가 mutation이 아니라 `follow-up-queued`가 됩니다.
push 후 `IN_PROGRESS`는 fresh recheck를 최대 세 번 수행하고, 여전히 완료되지
않으면 `waiting`으로 기록하고 worktree를 유지한 채 independent row를 계속합니다.
반환된 state가 실제로 external check 또는 re-review 대기를 요구하고 모든 inline
review thread가 resolved일 때만
`⏳ sweep · 대기`를 emit합니다.

unresolved identity, corrupt repository evidence, unprovable worktree ownership 같은
shared safety failure일 때만 이후 mutation을 멈춥니다. PR-local `Fail`, `Blocked`,
`Unverifiable`는 proven-independent row를 멈추지 않습니다. complete route가 fresh
Pass한 sweep-created clean worktree만 제거하고, 나머지 worktree는 모두 보존하고
보고합니다.

## 공백 닫기(Close gaps) 및 최종화(Finalize)

각 approved row/R/AC를 `satisfied | missing | partial | unverifiable`로 분류합니다.
general review가 아니라 scope, routes, tests/checks, publication,
ancestry/ownership, freshness만 확인합니다. 불확실한 AC evidence에는 stronger
fresh non-mutating reviewer를 한 번 사용할 수 있지만, 모든 fix는 여전히 fresh
Respond worker를 사용합니다.

모든 initial row를 처리한 뒤 unbounded queue를 늘리지 않고 final deterministic
triage를 한 번 실행합니다. 예상하지 못한 newly actionable supported item은
`Blocked`, `waiting` 또는 `follow-up-queued`는 `Pending`이며, 그 외에는
`Fail > Blocked > Unverifiable > Pending > Pass` 순서로 aggregate합니다.
report-only unsupported row는 supported success 또는 failure가 되지 않습니다.

승인 snapshot, route/worker/verifier/commit 증거, 소비한 bound, 요약 budget,
worktree disposition, final triage, gap verdicts, recovery facts만
`.tigerkit/pr-sweep.md`에 update합니다. credentials, transcript, full logs, resume
cursor는 저장하지 않습니다. Terminal output은 `## PR sweep`로 시작하고,
처리한 모든 PR과 남은 report-only/held item을 보여주며, 정확히 한 줄의
`Status: Pass | Fail | Blocked | Unverifiable | Pending`을 사용합니다. child
receipt는 생략하고, canonical ID/status/command/path/exact literal은 보존한 채
사용자 언어를 따릅니다.
