---
name: tk-pr-rebase
description: "[user/auto] 특정 PR의 기준 브랜치 변경이나 충돌에 rebase가 필요할 때 사용합니다. 활성 `tk-pr-sweep` 또는 `tk-pr-respond`가 정확한 PR/base/head와 승인된 rebase 범위를 넘기는 handoff도 받습니다. 일반 브랜치 작업과 rebase 근거가 확인되지 않은 리뷰 대응에는 자동 적용하지 않습니다."
disable-model-invocation: false
argument-hint: "<pull request or repository>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Rebase One PR

## Shared References

Read branch-triggered criteria from the current installed owners. A missing/mismatched
owner or resource blocks that action: use `tk-setup-skills`, not memory, another installation
or unapproved installs. Reading grants no workflow or mutation authority.

- For a user-owned decision, missing approval or unmet prerequisite, read [question rounds](../tk-questioning/references/questions.md).
- Before a user-facing completion report, artifact-path handoff or multi-attribute chat comparison, read [chat delivery](../tk-writing/references/delivery.md). The task's specific output contract wins.

## Approval Continuity

Reuse active same-task approval across turns and child phases (including baseline/after); continue only its authorized
work through existing owners. Return child/baseline evidence and resume approved owner work;
a phase status is not completion. Ask only for a new material decision, changed scope/authority
or missing user-only input. Invocation and recovered artifacts grant no authority. Remote and
destructive actions need explicit action/target approval, never inferred from local approval.

Start only through `/tk-pr-rebase`, `$tk-pr-rebase`, the host skill picker, or an exact approved rebase handoff from an active `tk-pr-sweep` or `tk-pr-respond`.
Do not auto-apply to a generic branch `rebase`, simple `conflict marker edit`, or ordinary review response.

Own the exact `base/head rebase`, `conflict resolution`, `verification`, and bounded `force-with-lease` for one PR.
Do not perform `merge`, `close`, `tag`, `release`, or unrelated feedback implementation.

## Fresh identity and workspace

Local rebase must run in a newly established dedicated isolated workspace for the exact PR operation. "Newly established"
is semantic: when the host has already placed this invocation in a fresh externally managed workspace dedicated to the
exact PR/head, that boundary may be reused after provenance is proven; do not create a nested manual worktree merely to
satisfy wording.

Before creating anything, inspect repository root, branch/HEAD, `GIT_DIR`, `GIT_COMMON`, and
`git rev-parse --show-superproject-working-tree` or equivalent. `GIT_DIR != GIT_COMMON` is a linked-worktree signal only
after excluding a submodule, and a linked worktree is not automatically owned by this PR.

When a new dedicated workspace is still required, first check whether active-task authorization or an approved Sweep
handoff covers creating that workspace. Preserve any stricter user rule requiring explicit workspace consent;
the rebase request alone does not override it. Reuse existing authorization without another question when it covers
the exact isolation. Otherwise obtain the missing decision before creation.
Then inspect the current tool surface for concrete native entry points such
as `EnterWorktree`, `WorktreeCreate`, `/worktree`, or `--worktree`; these are capability examples, not durable provider
routing. Prefer an available agent-callable native worktree/workspace mechanism and fresh-read its path, branch or
detached state, and HEAD.
Use manual `git worktree` only when no safe native mechanism is available. The fallback must start from the exact `old_head`,
avoid path/branch collisions and unrelated work, and be fresh-read after creation. Use Artifact Paths setup only for missing `.tigerkit/` coverage; do not make unrelated ignore edits
or create a setup commit merely to enable the fallback. If the dedicated boundary cannot be created and proven fresh, return `Blocked`
before mutation.

Host-managed workspaces keep their host-owned lifecycle. This skill does not remove, prune, relocate, or otherwise clean an
externally managed workspace as part of rebase completion.

Fresh-read the following at the start.

- repository and authenticated identity
- open PR number
- head repository/ref/SHA
- base repository/ref/SHA
- local branch/HEAD/workspace provenance
- active Git operation
- review/thread/check state

Before recommending or executing a base update, apply [PR base and rebase readiness](../tk-pr-guidance/references/rebase-readiness.md).

If identity/ownership is ambiguous or the fork publication boundary cannot be proven safe, return `Blocked` before mutation.

Fetch the exact remote head and latest base, then freeze the following.

```text
old_head
base_sha
full head ref
remote
expected force-with-lease
```

Require local `HEAD == old_head`, remote PR head `== old_head`, and a clean dedicated workspace.

## Rebase and conflict

Rebase onto the exact `base_sha`.
If a conflict occurs, apply the intent/index/marker/verification contract from `tk-merge-conflict`.
Do not choose arbitrarily when semantic ambiguity exists.

After the rebase, verify the following.

- Git operation completed
- workspace/index clean
- `base_sha` is an ancestor of the new HEAD
- intended commit/diff preserved
- relevant tests/checks pass

Do not force-push if no rewrite is needed.

## Standalone publication

An explicit standalone invocation automatically authorizes only the local rebase.
Before remote publication, record the exact PR/base/head, old/new SHA, verification, exact lease/refspec,
reply/thread action, and exclusions in an active approval packet. Keep a simple same-turn packet in the interaction when
it can be faithfully retained and reread. Use the singleton `.tigerkit/pr-rebase.md` only for an explicit `save`,
multi-turn handoff/recovery, complex conflict state, or when the host cannot retain the exact packet. Never create a
per-run archive; when used, atomically replace stale completed content for this owner and reread it.

## 🔴 CHECKPOINT · 🛑 STOP · Standalone publication boundary

Do not tell the user merely to read an artifact. Naturally summarize what changed, what was verified,
and which exact publication will be performed. Reuse an upfront request explicitly authorizing rebase and push to this target; ask once only if publication authority is absent.
STOP immediately before the remote write if repository/identity/open state/base/head/refspec/lease cannot be rechecked
or if any material drift invalidates the approval.

Only exact `--force-with-lease=<full-head-ref>:<old_head>` is allowed for publication.
Plain `--force` is prohibited.

## Execution under a parent skill

If an active `tk-pr-sweep` or `tk-pr-respond` has already approved the exact repository/PR/base/head, rebase route, target branch, and bounded history-rewrite publication, do not repeat that approval question.

The parent handoff must include the exact PR, base repository/ref/SHA, head repository/ref/SHA, approved publication target and route, and a newly established dedicated workspace path with provenance sufficient to prove that workspace belongs to this PR. The workspace may be host-native or a safe manual Git fallback; the child must not replace a proven host-owned workspace with a nested manual one. If approval, path, HEAD, or provenance is missing or stale, return `Blocked` before mutation. Run the child from that workspace; never switch the parent `main` or `develop` checkout to the PR branch.

The child must not create `.tigerkit/pr-sweep.md`, `.tigerkit/pr-respond.md`, or `.tigerkit/pr-rebase.md`.
Return only the following compact evidence to the parent.

- repository/PR
- consumed `base_sha` / `old_head`
- verified `new_head`
- tests/checks
- exact lease/refspec
- remaining conflict/finding
- status

Recheck the exact PR/base/head immediately before child execution.
If the head/base changed materially outside the approved handoff, return only that PR to the parent as `Blocked`.
For a `tk-pr-respond` parent, return the verified `new_head` as the expected transition. The parent must fresh-read the PR and rebuild feedback/thread evidence against that head before continuing; the child rebase does not resolve or reply to review findings.

## After publication

Verify that the remote PR head is `new_head`.
For a standalone run, reply to or resolve only review threads actually satisfied by the rebase. Under a parent skill, return the fresh state to that parent without replying to or resolving feedback.
Fresh-read every thread/review/check and do not hide unresolved findings as complete.

If needed, re-request review from an existing human reviewer, excluding the author, authenticated user, bots, and still-valid approvers.
End generated GitHub comments with `_🤖 본 코멘트는 AI가 작성했습니다._`.

## Status

| Status | Meaning |
| --- | --- |
| `Pass` | Fresh evidence confirms the exact rebase and required publication |
| `Pending` | Waiting for standalone publication approval |
| `Blocked` | Identity, authority, semantic conflict, or freshness is not safely resolved |
| `Unverifiable` | Required Git/GitHub evidence cannot be read |
| `Fail` | A local or remote operation failed and the exact applied state must be reported |

Do not claim success for any reply/resolve/review/check state that was not observed.

## Artifact Paths

Before authorized artifact writes, checkout/transport/ignore setup or temporary-input consumption,
read [artifact paths](../tk-artifacts/references/artifact-paths.md). Use safe owned nonsymlink paths
and proven Git exclusion for repository scratch; failed checks stop that file branch. Preserve
explicit final destinations and owner-specific defaults. Prefilled input is not completed input.
Cleanup targets only recorded literal resolved absolute run-owned paths, never cwd-relative paths or globs.
