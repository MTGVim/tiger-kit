# Respond mode

Respond mode owns review interpretation, resolution-unit planning, aggregate
review state, and remote publication. It delegates every product-code mutation
to `tk-implement`.

## Collect and select

1. Resolve the exact pull request, author, authenticated user, branch, head
   SHA, base, open/draft state, checks, reviews, inline comments, issue
   comments, and review threads with complete pagination.
2. When author and authenticated user differ, stop before comment analysis that
   could lead to mutation and obtain one explicit identity decision.
3. Group replies into threads, suppress superseded bot iterations, preserve a
   bounded exact quote for each current finding, and distinguish unresolved,
   apparently handled, and formally resolved state.
4. Render numbered cards and a final compact summary. Wait `Pending` for the
   user to select `apply`, `reply`, `skip`, or `defer` per item. Do not mutate
   code from the model's recommendation alone.

## Resolution units

Combine comments only when they require the same coherent edit and verification
boundary. Split comments that need independently verifiable behavior. One
resolution unit may satisfy multiple comment IDs; never create empty or
artificial per-comment commits.

For each selected apply unit, invoke `tk-implement` with:

- active `tk-pr respond` identity and PR/head SHA;
- resolution-unit ID and exact comment/thread IDs;
- R/AC or source anchors, scope, exclusions, and required verification;
- initial `HEAD` and pre-existing dirty paths.

Accept only the child's native `Pass | Fail | Blocked | Unverifiable` state and
verified commit. Do not emit a child terminal summary between units. A failed
or unverified unit remains unpublished and keeps its threads open.

## Aggregate verification and publish plan

After selected units finish, verify commit ancestry, comment-to-unit mapping,
required focused checks, aggregate repository checks, current PR head, and
remaining unresolved items. Draft replies that state only measured changes and
verification. Mark a thread resolvable only when its requested outcome is
verified and no deferred dependency remains.

Write exact push refspec, reply bodies, resolvable thread IDs, intentionally
open threads, optional summary comment, and human re-review requests to
`.tigerkit/pr.md`. An apply instruction does not cross this boundary. Show the
outbound plan and stop `Pending` for publish approval.

## Publish

After approval and freshness recheck, execute in this order:

1. push explicit branch ref without force;
2. post exact inline or top-level replies;
3. resolve only verified resolvable threads;
4. post one aggregate comment only for multiple units or explicit request;
5. request re-review only from supported human reviewers selected in the plan.

Reread the PR after publication and report remote SHA, replies, resolved and
open thread counts, checks, and remaining risks. A partial write is `Fail`; do
not duplicate replies or close extra threads during recovery.
