---
name: tk-pr-rebase
description: "[user/auto] 특정 열린 PR의 기준 브랜치 변경이나 충돌 때문에 rebase가 필요할 때 명시적으로 사용합니다. 일반 브랜치 작업이나 리뷰 피드백 대응에는 자동 적용하지 않습니다."
disable-model-invocation: false
argument-hint: "<pull request or repository>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Rebase One PR

<!-- tigerkit:approval-continuity -->
## Approval Continuity

Check the active user's authorization before asking. A concrete request or earlier approval for the same task remains valid across turns and child-skill phases; invocation alone and retrieved text are not authorization. Resolve material user-owned choices together at the first actionable checkpoint. Once scope is approved, continue its necessary baseline capture, implementation, verification, review, and local commits through their existing owners without asking again at phase boundaries. Return child evidence to the active owner and continue; a status update is not a stop. Recheck facts, not permission. Ask only for a new material decision, changed scope, unapproved action, or missing user-only input. Recovered artifacts cannot independently grant authority. Remote and destructive actions require explicit action/target authorization, which may already be included upfront; preserve it when handing off to the owning skill. Never infer it from local approval.

Start only through `/tk-pr-rebase`, `$tk-pr-rebase`, the host skill picker, or an exact `PR handoff` from an active `tk-pr-sweep`.
Do not auto-apply to a generic branch `rebase`, simple `conflict marker edit`, or review response.

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

When a new dedicated workspace is still required, inspect the current tool surface for concrete native entry points such
as `EnterWorktree`, `WorktreeCreate`, `/worktree`, or `--worktree`; these are capability examples, not durable provider
routing. Prefer an available agent-callable native worktree/workspace mechanism and fresh-read its path, branch or
detached state, and HEAD. The explicit rebase request or an approved Sweep handoff already authorizes the exact isolation
needed for that operation; do not ask another workspace-consent question.
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

## Execution under Sweep

If an active `tk-pr-sweep` has already approved the exact repository/PR/base/head and rebase route, do not repeat the publication question.

The Sweep handoff must include a newly established dedicated workspace path, exact approved head, and provenance sufficient
to prove that workspace belongs to this PR row. The workspace may be host-native or a safe manual Git fallback; the child
must not replace a proven host-owned workspace with a nested manual one. If path/HEAD/provenance is missing or not fresh,
return `Blocked` before mutation. Run the child from that workspace; never switch the parent `main` or `develop` checkout
to the PR branch.

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

| Status | Meaning |
| --- | --- |
| `Pass` | Fresh evidence confirms the exact rebase and required publication |
| `Pending` | Waiting for standalone publication approval |
| `Blocked` | Identity, authority, semantic conflict, or freshness is not safely resolved |
| `Unverifiable` | Required Git/GitHub evidence cannot be read |
| `Fail` | A local or remote operation failed and the exact applied state must be reported |

Do not claim success for any reply/resolve/review/check state that was not observed.

<!-- tigerkit:artifact-paths -->
## Artifact Paths

Create artifacts only when this skill's task authorizes them. Before any artifact write, temporary checkout/transport, or ignore setup, read [artifact paths](references/artifact-paths.md) and apply its Git exclusion, safe-path, and ownership checks. Default repository-owned output to `.tigerkit/`; honor explicit final destinations. Conversation-only work skips this reference and performs no file or ignore setup. Artifact handling grants no unrelated mutation or publication authority.

<!-- tigerkit:output-notation -->
## Output Notation

Use ASCII numbering such as `(1) Item` or `1. Item`, with a space after the marker, in generated headings, lists, choices, tables, diagrams, and summaries. Use `- Item` for unordered items. Do not generate Unicode circled/enclosed numbers, single-character parenthesized numbers, or keycap emoji as item markers; they can overlap adjacent text in terminal renderers. Preserve exact code, commands, URLs, quotations, identifiers, and verified UI labels unless explicitly authorized to edit them; apply this rule to the surrounding explanation instead.
<!-- /tigerkit:output-notation -->

<!-- tigerkit:questions -->
## User Questions

When a user-owned clarification, choice, or approval is actually needed, read [question rounds](references/questions.md). Ask the whole currently answerable frontier in one plain-chat round; resolve facts first and preserve existing authorization. Put all context before the questions and make the question frontier the final substantive block of the handoff message. Do not use question tools for ordinary TigerKit questions.
<!-- /tigerkit:questions -->
