# Drive-optimistic reflection

This mode is available only from one active `tk-drive` tail after aggregate
product verification passes. Standalone reflection uses the same local apply
safety boundary, while only the active drive owns finalization.

## Entry and fixed point

Require a valid active-drive reflection handoff after aggregate product
verification. The handoff includes task identity, product verification HEAD,
branch, initial HEAD, pre-existing dirty ownership, ordered product commits,
aggregate verification, and evidence refs for `.tigerkit/implementation.md`,
spec, and tickets. Missing or mismatched authority is `Blocked`; inaccessible
required evidence is `Unverifiable`.

Freeze the product verification HEAD before reflection. Reflection may not touch
product/source paths. A local rule apply leaves final HEAD equal to product
verification HEAD. Capture the exact target identity, ownership evidence,
current bytes, SHA-256, and target state at reflection start; the target need not
have been predicted in the drive-start ledger.

## Prevention owner

Classify every candidate at the earliest verified prevention point:

- `implement-preflight`;
- `simplify`;
- `test`;
- `lint/typecheck`;
- `CI`;
- `repo rule`;
- `user rule`;
- `skill`;
- `discard`.

Only an eligible local `repo rule` or `user rule` can be applied in this mode.
Other actionable owners remain follow-up candidates; `skill` receives a
promotion packet and never mutates a skill.

## Optimistic eligibility

Apply at most one local rule only when every condition holds:

- prevention owner is `repo rule` or `user rule`;
- confidence is `high`, backed by at least two independently verified Evidence
  IDs and no counterexample;
- trigger, action, and boundary are exact;
- one existing exact user-managed target is proven at reflection start;
- the target is a regular non-symlink file and byte-identical to its frozen
  reflection-start SHA-256 immediately before mutation;
- a repo target is inside the exact current worktree and Git proves it is
  untracked; ignored and visible untracked states are both eligible;
- a user target is an exact current-host-native path inside the user's home and
  outside the current repository;
- the target is not vendor, generated, persistent memory, or unknown ownership;
- no test, lint/typecheck, or CI owner prevents the issue earlier;
- the change is not skill creation or semantic skill mutation;
- the user did not prohibit reflection.

Use [local rule apply](local-rule-apply.md) before eligibility. A candidate that
fails any condition stays `pending` without a drive-stopping question. No
verified reusable evidence is a successful `no-op`.

## Ineligible targets

Tracked repository files, new or missing targets, symlinked targets, paths
outside their allowed scope, changed-since-baseline targets, globs, ambiguous
paths, generated/vendor targets, and ownership-unknown targets never
local-apply. Keep the candidate `pending` and do not create a replacement target.

A repository target is not ineligible merely because `git check-ignore` exits
`1`; that is the verified `untracked-visible` state. Exit codes other than the
documented tracked/untracked and ignored/visible values, or disagreement with
`git status`, are `Unverifiable` and prohibit mutation.

## Exact existing local target

Never create a new local rule target. Before mutation, save the exact before
image and metadata in `.tigerkit/reflect-backup/`.

Use `scripts/safe_rule_apply.py` with the exact repository root, target scope,
exact target, reflection-start SHA-256, verified `--user-managed` assertion, a
regular candidate file inside `.tigerkit/`, and at least one shell-free
JSON-array validation command. The script rechecks containment, path components,
regular-file and symlink state, repo Git state or user-scope separation,
baseline hash, backup, atomic replacement, post-write state, validators, and
exact rollback.

This path creates no commit and does not change final HEAD. Record `applied
locally`, scope, target state, ignore source when present, and the rollback
snapshot or exact restore command. Target or snapshot drift prohibits automatic
rollback and is `Blocked | Unverifiable`.

## Skill promotion packet

Every skill candidate remains `pending` regardless of confidence. Record:

- candidate ID and verified Evidence refs;
- difference from a rule, default capability, and existing skills;
- proposed `repo skill | user skill`;
- suggested name and kind;
- positive and negative trigger summary;
- independent workflow and I/O;
- remaining uncertainty;
- gates that a future `tk-learn` run must revalidate.

Do not create, edit, merge, invoke, or commit a skill. Skill candidates do not
change drive terminal status and do not create a user question.

## Ledger

Atomically write or replace `.tigerkit/reflect.md` for every tail, including
no-op and pending outcomes. Record task identity, product verification HEAD,
evidence refs, each candidate's interpretation, confidence, preferred
prevention owner, host dependency, target state, action, eligibility result,
application and validation, local rollback snapshot, promotion packet, and
pending/discard reason. Do not store raw logs, transcripts, full diffs,
credentials, screenshots, or copied receipt prose.

## Failure and completion

A pre-write failure leaves targets untouched. On a local write or validation
failure, restore the exact before image and verify its hash. Verified restoration
preserves product `Pass` while reflection reports `Fail`. Failed restoration,
target drift, out-of-scope changes, or indeterminate workspace state is
`Blocked | Unverifiable`.

On successful mutation or no-op, pass product verification HEAD, final HEAD,
local rollback when applicable, candidate IDs, ledger path, and validation
evidence directly to `tk-drive finalization`.

The terminal user sees only the bounded standalone Disposition summary:

| ID | Candidate | Action | Target | Why |
| --- | --- | --- | --- | --- |
| RF-01 | `<plain-language name>` | `<action/status and next step>` | `<target>` | `<evidence refs>` |

Show at most five decision-relevant rows. The ledger owns complete evidence,
status, provenance, rollback, and promotion details.
