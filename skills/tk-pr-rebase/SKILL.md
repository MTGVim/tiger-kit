---
name: tk-pr-rebase
description: "[user/auto] 하나의 `open` GitHub `pull request`를 정확한 최신 `base`로 `rebase`하고 `conflict`를 해결한 뒤, `standalone` 승인 또는 `active` `Sweep`의 `bounded authority`로 검증된 `force-with-lease publication`을 수행합니다."
disable-model-invocation: false
argument-hint: "<pull request or repository> [--ci]"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Rebase One PR

Start only through `/tk-pr-rebase`, `$tk-pr-rebase`, the host skill picker, or an exact `PR handoff` from an active `tk-pr-sweep`.
Do not auto-apply to a generic branch `rebase`, simple `conflict marker edit`, or review response.

Own the exact `base/head rebase`, `conflict resolution`, `verification`, and bounded `force-with-lease` for one PR.
Do not perform `merge`, `close`, `tag`, `release`, or unrelated feedback implementation.

## Fresh identity

Fresh-read the following at the start.

- repository and authenticated identity
- open PR number
- head repository/ref/SHA
- base repository/ref/SHA
- local branch/HEAD/worktree
- active Git operation
- review/thread/check state

If identity/ownership is ambiguous or the fork publication boundary cannot be proven safe, return `Blocked` before mutation.

Fetch the exact remote head and latest base, then freeze the following.

```text
old_head
base_sha
full head ref
remote
expected force-with-lease
```

Require local `HEAD == old_head`, remote PR head `== old_head`, and a clean worktree.

## Rebase and conflict

Rebase onto the exact `base_sha`.
If a conflict occurs, apply the intent/index/marker/verification contract from `tk-merge-conflict`.
Do not choose arbitrarily when semantic ambiguity exists.

After the rebase, verify the following.

- Git operation completed
- worktree/index clean
- `base_sha` is an ancestor of the new HEAD
- intended commit/diff preserved
- relevant tests/checks pass

Do not force-push if no rewrite is needed.

## Standalone publication

An explicit standalone invocation automatically authorizes only the local rebase.
Before remote publication, record the exact PR/base/head, old/new SHA,
verification, exact lease/refspec, reply/thread action, and exclusions in `.tigerkit/pr-rebase.md`, then reread it.

## 🔴 CHECKPOINT · 🛑 STOP · Standalone publication boundary

Do not tell the user merely to read the entire ledger. Naturally summarize what changed, what was verified,
and which exact publication will be performed, then obtain one current-turn approval.
STOP immediately before the remote write if repository/identity/open state/base/head/refspec/lease cannot be rechecked
or if any material drift invalidates the approval.

Only exact `--force-with-lease=<full-head-ref>:<old_head>` is allowed for publication.
Plain `--force` is prohibited.

## Execution under Sweep

If an active `tk-pr-sweep` has already approved the exact repository/PR/base/head and rebase route, do not repeat the publication question.

A Sweep child must not create `.tigerkit/pr-sweep.md` or `.tigerkit/pr-rebase.md`.
Return only the following compact evidence to the parent.

- repository/PR
- consumed `base_sha` / `old_head`
- verified `new_head`
- tests/checks
- exact lease/refspec
- remaining conflict/finding
- status

Recheck the exact PR/base/head immediately before child execution.
If the head/base changed materially after parent approval, return only that PR to the parent as `Blocked`.

## After publication

Verify that the remote PR head is `new_head`.
Reply to or resolve only review threads actually satisfied by the rebase.
Fresh-read every thread/review/check and do not hide unresolved findings as complete.

If needed, re-request review from an existing human reviewer, excluding the author, authenticated user, bots, and still-valid approvers.
End generated GitHub comments with `_🤖 본 코멘트는 AI가 작성했습니다._`.

## Status

| 상태 | 의미 |
| --- | --- |
| `Pass` | exact rebase와 필요한 publication이 fresh evidence로 확인됨 |
| `Pending` | standalone publication 승인을 기다림 |
| `Blocked` | identity, authority, semantic conflict, freshness가 안전하게 닫히지 않음 |
| `Unverifiable` | 필요한 Git/GitHub evidence를 읽을 수 없음 |
| `Fail` | 일부 local/remote operation이 실패했고 적용 상태를 정확히 보고해야 함 |

Do not claim success for any reply/resolve/review/check state that was not observed.
