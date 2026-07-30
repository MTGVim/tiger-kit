# Drive-optimistic reflection

This mode is available only from one active `tk-drive` tail after aggregate
product verification passes. Standalone and ordinary implicit reflection keep
their report-only and separate-approval contracts.

## Entry and fixed point

Require the handoff to include:

Require a valid active-drive reflection handoff after aggregate product
verification. The handoff names the eligible target and its containment
evidence; it does not store a caller-return instruction.

Also require task identity, product verification HEAD, branch, initial HEAD,
pre-existing dirty ownership, ordered product commits, aggregate verification,
and evidence refs for `.tigerkit/implementation.md`, spec, and tickets. Missing
or mismatched authority is `Blocked`; inaccessible required evidence is
`Unverifiable`.

The drive-start implementation ledger must already name the one exact
normalized repository-relative target, prove that it existed, record its
before-image SHA-256, and classify it as user-managed, untracked, and ignored.
Freeze the product verification HEAD and reread that baseline evidence before
mutation. Reflection may not touch product/source paths. Local-only reflection
leaves final HEAD equal to product verification HEAD.

## Prevention owner

Classify every candidate at the earliest verified prevention point:

- `implement-preflight`;
- `simplify`;
- `test`;
- `lint/typecheck`;
- `CI`;
- `repo rule`;
- `skill`;
- `discard`.

Only `repo rule` can be applied in this mode. Other actionable owners remain
follow-up candidates; `skill` receives a promotion packet and never mutates a
skill.

## Optimistic eligibility

Apply a repository rule only when every condition holds:

- prevention owner is `repo rule`;
- confidence is `high`, backed by at least two independently verified Evidence
  IDs and no counterexample;
- repository-specific trigger, action, and boundary are exact;
- the drive-start ledger proves one existing exact user-managed repository
  rule target;
- the target is currently a regular non-symlink file contained by the
  repository, untracked, ignored, and byte-identical to its baseline SHA-256;
- the target is not vendor, generated, global, user-level, persistent memory,
  or unknown ownership;
- target content and ownership have not drifted;
- no test, lint/typecheck, or CI owner prevents the issue earlier;
- the change is not skill creation or semantic skill mutation;
- the user did not prohibit reflection.

Use the repository placement rubric before eligibility. A candidate that fails
any condition stays `pending` without a drive-stopping question. No verified
reusable evidence is a successful `no-op`.

## Ineligible targets

Tracked, unignored, new, symlinked, external, changed-since-baseline,
ambiguous, generated, or ownership-unknown targets never auto-apply. Keep the
candidate `pending` under its normal approval boundary and do not create a
replacement local target. A target path containing a glob or resolving
through another path is ambiguous.

## Exact existing ignored target

The exact user-managed local rule file must already exist at drive start.
Never create a new local rule target. Before mutation, save its exact
before-image and hash in the current task's single latest snapshot under
`.tigerkit/reflect-backup/`.

Use `scripts/ignored_rule_apply.py` with the exact repository root,
repository-relative target, drive-start SHA-256, a regular candidate file
inside `.tigerkit/`, and at least one shell-free JSON-array validation command.
The script rechecks containment, every path component, regular-file and
symlink state, Git tracked/ignored state, and baseline hash; writes a mode-0600
backup; atomically replaces the target; reruns the supplied syntax/link
validation; and restores the exact before-image when post-write validation
fails. Do not bypass a script rejection or treat the ownership assertion as a
fact the script can infer.

This path creates no commit and does not change final HEAD. Report
`applied locally`, the target, and the rollback snapshot or exact restore
command. Target or snapshot drift prohibits automatic rollback and is
`Blocked | Unverifiable`.

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

Atomically write or replace `.tigerkit/reflect.md`. Record task identity,
product verification HEAD, evidence refs, each candidate's interpretation,
confidence, preferred prevention owner, host dependency, action, eligibility
result, application and validation, local rollback snapshot, promotion packet,
and pending/discard reason. Do not store raw logs,
transcripts, full diffs, credentials, or copied receipt prose.

## Failure and completion

A pre-write failure leaves targets untouched. On a local write or validation
failure, restore the exact before-image and verify its hash. Verified
restoration preserves product `Pass` while reflection reports `Fail`. Failed
restoration, target drift, out-of-scope changes, or indeterminate workspace
state is `Blocked | Unverifiable`.

On successful mutation or no-op, pass product verification HEAD, final HEAD,
local rollback when applicable, candidate IDs, and validation evidence
directly to `tk-drive finalization`. Omit no-op, empty risks, and
zero-candidate sections from user-facing output.

For every non-no-op result, preserve the standalone bounded Disposition table:

| ID | Candidate | Action | Target | Why |
| --- | --- | --- | --- | --- |
| RF-01 | `<plain-language name>` | `<action/status and next step>` | `<target>` | `<evidence refs>` |

Show at most five decision-relevant rows. Status, provenance, rollback, and
decision IDs remain in the owned ledger; they never replace the table with
code names alone.
