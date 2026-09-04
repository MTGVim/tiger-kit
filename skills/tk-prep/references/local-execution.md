# Local Execution

Read this reference only when the approved outcome may include local implementation. Handoff-only preparation does not
need workspace setup or completion mechanics.

## Workspace safety

Before final approval, establish the repository root, current branch/HEAD, default branch, linked-worktree state,
submodule status, staged/unstaged/untracked paths, unrelated user work, and required test/browser/server readiness.
Never absorb, stage, commit, clean, stash, review, or overwrite unrelated work.

Reuse a non-default task checkout only when its task identity and HEAD are proven. Treat `GIT_DIR != GIT_COMMON` as a
linked-worktree signal only after excluding submodules with `git rev-parse --show-superproject-working-tree` or equivalent
evidence. If execution would start from the default branch, final approval must cover creating or using a fresh isolated
task checkout.

When isolation is required, detect existing isolation first. Prefer an available agent-callable native mechanism such as
`EnterWorktree`, `WorktreeCreate`, `/worktree`, or `--worktree`, then fresh-read its path, branch or detached state, and
HEAD. Approval for the exact plan and isolated checkout also authorizes that native mechanism; do not ask again solely
because the tool has its own name.

Use manual `git worktree` only when no safe native mechanism exists. Start from the approved source HEAD, avoid unrelated
work and path/branch collisions, and verify the result. When creating a task branch from any ref other than current HEAD,
prevent inherited upstream tracking (for example, `git worktree add ... -b <branch> --no-track <base-ref>`). Before product
mutation, verify the task branch does not track a shared integration branch such as `origin/main`, `origin/dev`, or
`origin/production`; unset that upstream or return `Blocked` if safe isolation cannot be proven. Do not edit `.gitignore`
or create a setup commit for isolation. If isolation cannot be proven, return `Blocked` before product mutation. Preserve
the lifecycle of host-managed workspaces; do not remove, prune, relocate, or clean them on completion.

## Direct execution and completion

Direct changes follow RED → verified failure → minimal GREEN → refactor while green → self-simplify → exact-change
read-only review → scoped remediation/re-review → binding verification → commit. Remove unnecessary indirection,
speculative flexibility, dead branches, custom replacements for repository-native helpers, and production APIs added
only for tests.

When the approved browser plan says the candidate can affect rendered output, invoke `tk-browser-verify` to capture the
planned pre-change baseline before the first product edit. Preserve its exact source and replay metadata for the after
call. If the baseline call is `Blocked | Unverifiable`, continue only within the approved limitation and never convert
candidate-only acceptance evidence into an absence-of-regression claim.

When direct execution needs multiple commits, prefer a stronger repository convention; otherwise split by independently
understandable, verifiable, and revertible work units rather than file type or layer. Keep each behavior with the tests
that prove it and factual documentation that must change with it when practical. Keep one coherent judgment surface in
one commit, and do not perform fragile retrospective hunk surgery merely to increase the commit count.

After candidate implementation and before final review, construct an implementation retro that records actual behavior
changed, deviations from approved decisions and reasons, newly discovered risks, verification observations, and unresolved
limitations. It is an untrusted claim bundle, not review proof.

Every exact-change review applies [independent review protocol](review-protocol.md) and
[finding quality](finding-quality.md). A direct final review uses two eligible context-isolated discovery seats; both
record independent `Spec/AC` and `Quality/Standards` verdicts and complete both required walks. Withhold the implementation
retro until each seat records its blind pass, aggregate the union, and separately verify every reportable candidate.
If the required fresh contexts are unavailable, disclose the missing independent coverage as `Unverifiable`; repeated
serial passes in one context do not satisfy it. Read [TypeScript](typescript.md),
[React](react.md), and [security](security.md) only when the review scope meets those references' conditions. These lenses
change review judgment, not the target, commit, remediation, or authority protocol.

Handle verified `Critical | Important` findings for at most five remediation rounds. Recheck the original open findings
and exact fix diff rather than rerunning broad discovery after every edit, and admit only new qualifying breakage caused
by that fix. Stop with the exact unresolved result after round five; do not continue until a stochastic review happens to
return no findings.

For direct and SDD execution, preserve scope and UI literals, use the exact review range, run acceptance review, retain
automated regression protection, and create only approved local commits. Invoke `tk-browser-verify` for every
browser-visible AC; its runtime evidence does not replace automated protection. SDD's whole-change final review already
satisfies the broad review gate.

During final exact-scope review, when the actual diff changes a public command, path, configuration key, environment
variable, API contract, or installation/build/deployment/onboarding procedure, compare it with an exact repository-owned
document only if preparation already identified that document as the owner of the changed fact. Correct only stale factual
content in the same approved local change, using the repository's generator instead of editing generated output directly.
Do not search the documentation tree, invent a new document, or edit voice, structure, strategy, or nearby prose. Skip this
check when the public fact did not change or no exact owner was already known. A correction that requires a new product
decision or material scope expansion returns to preparation for revision and reapproval.

Material Goal/Scope/approved Decision/AC/security/required Verification drift returns to preparation for revision and
reapproval. A reversible engineering ambiguity may receive a visible `Ruling:` with its reason and cost if wrong.
Repeated blockers end as `Fail | Unverifiable | Blocked`, not an infinite loop.
