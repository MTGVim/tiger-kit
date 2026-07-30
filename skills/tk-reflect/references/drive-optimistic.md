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

Freeze the product verification HEAD and every candidate target's path,
content, hash, tracked/ignored state, and ownership before mutation. Reflection
may not touch product/source paths. A tracked reflection commit may advance
final HEAD; ignored/local-only reflection leaves final HEAD equal to product
verification HEAD.

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
- an existing exact user-managed repository rule target is verified;
- the target is not vendor, generated, global, user-level, persistent memory,
  or unknown ownership;
- target content and ownership have not drifted;
- no test, lint/typecheck, or CI owner prevents the issue earlier;
- the change is not skill creation or semantic skill mutation;
- the user did not prohibit reflection.

Use the repository placement rubric before eligibility. A candidate that fails
any condition stays `pending` without a drive-stopping question. No verified
reusable evidence is a successful `no-op`.

## Tracked target

Freeze the product HEAD and target hash, apply only the eligible rule scope,
and revalidate syntax, links, ownership, diff scope, and target hash lineage.
Create one separate commit whose changed paths are only the allowed rule
targets; prefer `chore(tigerkit): reflect <short rule>`. Report product and
reflection commits separately and give `git revert <reflection-sha>` as
rollback.

If write/revalidation fails before commit, restore the exact frozen content
and verify its hash. Never amend, squash, reset, or hide the product commits.

## Existing ignored or untracked local target

The exact user-managed local rule file must already exist at drive start.
Never create a new local rule target. Before mutation, save its exact
before-image and hash in the current task's single latest snapshot under
`.tigerkit/reflect-backup/`. Revalidate the target hash, syntax, links, and
ownership after writing.

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
result, application and validation, tracked commit or local rollback snapshot,
promotion packet, and pending/discard reason. Do not store raw logs,
transcripts, full diffs, credentials, or copied receipt prose.

## Failure and receipt

A pre-write failure leaves targets untouched. On a tracked pre-commit failure
or local write failure, restore the exact before-image and verify its hash.
Verified restoration preserves product `Pass` while reflection reports
`Fail`. Failed restoration, target drift, out-of-scope changes, or indeterminate
workspace state is `Blocked | Unverifiable`.

On successful mutation or no-op, pass product verification HEAD, final HEAD,
reflection commit or local rollback when applicable, candidate IDs, and
validation evidence directly to `tk-drive finalization`. Omit no-op, empty
risks, and zero-candidate sections from user-facing output.

For every non-no-op result, preserve the standalone bounded Disposition table:

| ID | Candidate | Action | Target | Why |
| --- | --- | --- | --- | --- |
| RF-01 | `<plain-language name>` | `<action/status and next step>` | `<target>` | `<evidence refs>` |

Show at most five decision-relevant rows. The receipt owns status, provenance,
commit/rollback, and decision IDs; it never replaces the table with code names
alone.
