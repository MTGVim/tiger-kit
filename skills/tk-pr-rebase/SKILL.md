---
name: tk-pr-rebase
description: "[user/auto] 하나의 open GitHub pull request를 정확한 최신 base로 rebase하고, conflict를 해결하고, 승인된 또는 sweep-owned force-with-lease authority로 검증 후 publish합니다."
argument-hint: "<pull request or repository> [--ci]"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Pull Request rebase

`/tk-pr-rebase`, `$tk-pr-rebase`, 또는 host skill picker를 통해서만 시작한다. generic
rebase, update-branch, conflict, review-response, continuation에는 절대
활성화하지 않는다. 유일한 automatic entry는 active `tk-pr-sweep`의 fresh
exact-PR handoff다.

하나의 PR에 대한 local rebase, bounded force-with-lease publication,
rebase로 충족된 review reply와 thread resolution, rebase summary, conditional human
re-review를 소유한다. Standalone execution은 `.tigerkit/pr-rebase.md`를 소유하고,
Sweep CI는 child Markdown ledger를 작성하지 않으며 compact evidence를
`.tigerkit/pr-sweep.md`에 반환한다. 관련 없는 feedback을 구현하거나 merge, close,
tag, release를 수행하거나 repository rules를 바꾸지 않는다.

## 모드

- **Normal:** explicit invocation은 local rebase만 authorize한다. publication
  question은 아래에 둔다.
- **Sweep CI:** `--ci`에는 exact repository, PR, base/head refs와 SHAs, route attempt,
  fresh isolated worker/specialist dispatch를 freeze한 active `tk-pr-sweep`
  handoff가 필요하다. Sweep Plan approval 이후에는 handoff가 별도 question 없이
  bounded rebase/conflict resolution과 publication을 허용한다. semantic conflict
  ambiguity 또는 dispatch isolation 누락은 `Blocked`로 남는다.

## 작업 흐름

1. 정확히 하나의 open PR, repository, authenticated identity, author, head
   repository/ref/SHA, base repository/ref/SHA, local branch, dirty paths, active
   Git operation, checks, reviews, comments, threads, requested reviewers를 확정한다.
   ambiguity, identity/ownership mismatch, unsafe fork destination, 또는 이 plan이
   만들지 않은 operation이면 중지한다.
2. 정확한 remote head와 latest base를 fetch한다. `old_head`, `base_sha`, current
   review/thread state, existing requested reviewers를 freeze한다. clean worktree,
   unrelated staged paths 없음, local `HEAD == old_head`, remote PR head
   `== old_head`를 요구한다.
3. findings를 분류한다. PR을 frozen base로 업데이트해 requested outcome을
   충족할 때만 thread를 close한다. unrelated, deferred, superseded-uncertain,
   unverified finding은 open으로 유지한다.
4. branch를 정확한 `base_sha` 위로 rebase한다. Normal invocation은 local rebase만
   authorize하며 abort, reset, push, comment publication은 authorize하지 않는다.
   각 conflict iteration에는 `tk-merge-conflict`를 사용하고, operation, intent,
   index, marker, verification gates가 통과한 뒤에만 resume한다. Sweep CI에서는
   exact approved maintenance-rebase handoff가 verified result를 publish할 수
   있지만, 절대 추측하거나 auto-abort하지 않는다.
5. rebase가 끝났는지, worktree와 index가 clean인지, `base_sha`가 새 `HEAD`의
   ancestor인지, intended commits와 diff가 유지되는지, 관련 tests/checks가
   통과하는지 검증한다. branch가 이미 `base_sha`를 포함해 rewrite가 필요 없으면
   force-push하지 않는다.
6. Normal mode에서는 `.tigerkit/pr-rebase.md`에 frozen refs와 SHAs,
   verification, exact `--force-with-lease` expectation/refspec, 모든 outbound
   reply, thread action, 의도적으로 open인 finding, summary, prior human
   reviewers, normal 및 reviewer-mention fallback bodies, exclusions를 기록한다.
   Sweep CI에서는 Markdown ledger를 작성하지 않고 이 compact facts를 parent에
   반환한다. URLs가 있으면 user-facing output의 PR 및 review/thread
   references를 clickable Markdown links로 렌더링한다. 표시 전에 GitHub
   `<br>`/`<br/>` break를 실제 newline으로 normalize한다. 모든 external
   reply/comment는 `_🤖 본 코멘트는 AI가 작성했습니다._`로 끝낸다.
7. base, old/new head, verification, exact replies와
   `resolve | keep open` actions, re-review candidates, operation order, risks,
   one recommendation을 보여준다. publication question은 하나만 하고
   `Pending`으로 멈춘다.
8. current-turn approval 후 모든 frozen local 및 remote field를 다시 읽는다.
   branch, head, base, identity, dirty-path, review, thread 중 하나라도 drift하면
   approval은 무효이며, refreshed plan과 함께 `Blocked`를 반환한다.
9. 다음 순서로 publish한다: exact
   `--force-with-lease=<full-head-ref>:<old_head>` push, PR이 new
   head를 가리키는지 확인, 승인된 각 reply 게시, verified하고 성공적으로
   답변한 thread만 resolve한다. plain `--force`나 unfrozen lease는 절대 사용하지
   않는다.
10. push 후 reviews, requested reviewers, threads, checks, mergeability를 다시
    읽는다. post-push review state를 관찰하며 stale-review dismissal을 추측하지
    않는다. current actionable, deferred, unverified finding이 하나도 없을 때만,
    feedback이 처리됐거나 새 head에서 approval이 무효가 된 prior human에게
    review를 re-request한다. author, authenticated user, bots, still-valid
    approvers는 제외한다. formal GitHub request를 우선한다. GitHub가 eligible
    reviewer를 거부하면 그 reviewer를 언급한 approved fallback summary를 게시하고
    formal request가 아닌 `mention fallback`으로 보고한다. 그 외에는 re-review
    decision 후 approved normal rebase summary를 게시한다.
11. PR을 다시 읽는다. partial remote writes는 정확히 보고하며, 관찰하지 않은
    reply, resolution, review request, check, mergeable state를 주장하지 않는다.

## Sweep CI 모드

1. 하나의 exact open PR과 unused `(base_sha, old_head)` pair에 대한 fresh
   active-sweep handoff, 그리고 Sweep이 이 route를 fresh isolated
   worker/specialist로 dispatch했다는 proof를 요구한다. handoff가 없거나
   ambiguous, inline/direct-only, repeated authority이면 rebase 또는 remote
   write 전에 `Blocked`로 처리하고, controller execution으로 fallback하지 않는다.
2. normal identity, ownership, clean-worktree, exact-base, conflict,
   preservation, verification gates를 실행한다. pair, verified `new_head`,
   compact verification evidence를 `.tigerkit/pr-sweep.md`에 반환하며,
   `.tigerkit/pr-rebase.md` 또는 다른 child Markdown ledger는 만들지 않는다.
3. publication question만 건너뛴다. push와 이후 모든 remote write 직전에 frozen
   repository, PR, identities, open state, base 및 head refs와 SHAs, remote,
   exact refspec, lease, review 및 thread targets, local clean state를 다시
   읽는다. drift는 `Blocked`이며, unexpected head 위로 lease를 refresh하지 않는다.
4. rewrite가 필요하면 다음 형태로 정확히 한 번 publish한다.
   `git push <remote> <new_head>:<full-head-ref>
   --force-with-lease=<full-head-ref>:<old_head>`. remote PR head가 `new_head`와
   같은지 확인한 뒤 이를 이후 reply/thread writes의 expected head로 사용한다.
   rewrite가 없으면 push하지 않고 observed head를 반환한다.
5. rebase로 충족된 replies, verified thread resolutions, conditional re-review만
   정상 순서로 적용한다. PR-level summary는 `tk-pr-sweep`에 위임하고,
   exact draft/material과 `summary budget: unused`를 반환한다. CI mode에서는
   normal 또는 mention-fallback summary를 절대 publish하지 않는다. 생성하는
   모든 reply는 정확히 `_🤖 본 코멘트는 AI가 작성했습니다._`로 끝낸다.
6. exact repository/PR, consumed `(base_sha, old_head)` pair, `new_head`,
   fresh category evidence, remaining open findings, native
   `Pass | Fail | Blocked | Unverifiable` state를 active sweep에 반환한다.
   user-facing phase summary는 작성하지 않으며 aggregate output은 sweep가
   소유한다.

## Publication gate

Plan은 repository, PR, identities, base 및 head refs와 SHAs, lease, refspec,
verification, replies, thread actions, summary body, re-review candidates,
fallback mentions, order, exclusions를 freeze한다. Approval은 해당 plan만
포괄한다. reply가 실패하면 thread는 open으로 남기며, remaining actionable
finding이 있으면 re-review를 보내지 않는다. branch protection이나 permission
failure를 절대 우회하지 않는다.

요청된 local 및 remote scope가 완료됐음을 관찰한 뒤에만 `Pass`를 사용한다.
publication approval 대기는 `Pending`, unsafe authority 또는 drift는 `Blocked`,
change-related 또는 partial-write failure는 `Fail`, required Git, GitHub, test,
review, thread evidence를 사용할 수 없으면 `Unverifiable`이다.

`## PR rebase`로 시작한다. exact outbound text와 full provenance는 standalone
owned artifact에 보관하고, Sweep CI에서는 compact parent evidence에 보관한다.
