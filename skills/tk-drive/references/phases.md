# Drive phase invariants

Drive owns one continuous `Preparing → Executing` run. The source is supplied
only through an explicit `/tk-drive <source>` or equivalent host invocation.
A pending decision answer may resume the same active conversation; a manifest
or generic continuation cannot start a new run.

The phase-owner allowlist is:

- Preparing: `tk-grill-me | tk-to-spec | tk-to-tickets | tk-prototype`
- Executing: `tk-implement | tk-reflect` (`tk-reflect` only in the successful
  drive-optimistic tail)
- Conditional support tools: `tk-browser-verify | tk-merge-conflict`

Phase owners never invoke sibling phase owners. Drive alone records and
executes transitions. The only late return from Executing is one amendment
through the Preparing owners `tk-grill-me`, `tk-to-spec`, `tk-to-tickets`, and
when comparison is necessary, `tk-prototype`.

## Preparing authority

Before any product mutation, bind:

- complete source and stable task anchors;
- repository root, worktree, branch, and initial HEAD;
- applicable instructions and initial dirty inventory;
- resolved user decisions;
- Ready R/AC, source UI writing inventory, and verification profile;
- material implementation/verification strategy and conditional browser route;
- ticket order or one no-ticket slice;
- bounded prior-art dispositions;
- cold-start reconstruction evidence.

Prior-art discovery is bounded to at most seven task- or symbol-related durable
items from applicable instructions, ADRs, tests, types, lint/CI configuration,
repository skills, and code invariants. Exclude `.tigerkit/reflect.md`, old
implementation ledgers, pending skill drafts, raw sessions, arbitrary global
TigerKit state, unrelated work, and inaccessible host-only rules. No relevant
prior art is a silent no-op.

`tk-to-spec` owns `adopted | already-satisfied | not-applicable | conflict`
disposition and R/AC linkage. Drive owns discovery and supplies the evidence;
it does not duplicate spec semantics.

## Strategy and browser preflight

Before decision closure, inspect the implementation sequence, verification
approach, required tools and permissions, safe side effects, and recovery or
stop conditions. Resolve repository-evidenced and implementation-owned facts
without asking. Route only a material user-owned choice through
`tk-grill-me`, one at a time; ordinary implementation details remain agent
owned.

For user-visible web UI or browser-relevant behavior, classify browser
evidence as `required | optional | N/A`. When required, or optional and
selected, bind target URL/environment, Guard/Verdict mode, account role and
tenant, `isolated` or opaque profile hint, authentication expectation, safe
interaction boundary, and unavailable runtime inputs. Persist only
non-identifying hints. An exact identity that must not be stored is
`intentionally omitted` with `re-request on cold start`; credentials, cookies,
tokens, OTPs, and profile contents never enter preparation artifacts. The
executor may re-request that already confirmed runtime input once before
browser launch, and that rehydration is not a Preparing amendment. `N/A`
causes no browser question or empty strategy section.

## Internal manifest boundary

After every preparation gate passes, call the drive-local
`scripts/prep_manifest.py create` command, then its `validate` command. The
artifact path is exactly `.tigerkit/prep.md`; never create an archive,
pointer, mirror, global state, or `.gitignore` mutation.

The manifest binds task ID and anchors, repository/worktree/branch/base HEAD,
source digest, dirty and instruction inventories, Ready spec, tickets or
no-ticket mode, and verification profile. Use current canonical inputs for
validation; never copy values from the header merely to make equality pass.

Immediately after strict Ready reread, use the drive-local
`scripts/prep_state.py claim` command to atomically activate the same manifest
for this run. This is internal concurrency and freshness enforcement, not a
public invocation surface. Record the returned identity in the implementation
ledger and execute the first prepared unit in the same active turn. Do not
emit a Ready terminal result or ask for implementation confirmation.

No product mutation, implementation handoff, or implementation-ledger unit
transition may precede activation.

## Handoff envelope

Before every child invocation, record the native `Success state` and exactly
one `Outstanding transition`. A child success is consumable only when it
echoes:

```text
Return to: tk-drive
Success state: <expected state>
Outstanding transition: <exact parent transition>
```

A missing or mismatched echo is receipt drift and cannot authorize another
transition.

Preparing transitions are decision closure, spec revalidation, ticket
derivation, prototype reconciliation, seal and activate, or the first
implementation unit. Executing transitions are the next unit, aggregate
verification, one corrective unit, the single amendment, reflection, or
finalization.

When both `TK_DRIVE_EVENT_RECORDER` and `TK_DRIVE_EVENT_LOG` are present in
an evaluation-owned environment, invoke:

```text
"$TK_DRIVE_EVENT_RECORDER" phase_invocation <phase>
"$TK_DRIVE_EVENT_RECORDER" phase_receipt <phase> Pass "<Outstanding transition>"
```

The exact commands are
`"$TK_DRIVE_EVENT_RECORDER" phase_invocation <phase>` and
`"$TK_DRIVE_EVENT_RECORDER" phase_receipt <phase> Pass "<Outstanding transition>"`.

The first command occurs immediately before the phase and the second
immediately after its matching success. Do not pass `TK_DRIVE_EVENT_LOG` as a
command argument. Missing or failed recording makes live evidence
`Unverifiable`.

## Receipt liveness

Consuming a successful phase result creates transition debt; it is not
completion. In the same active turn, execute exactly the recorded transition.
Progress commentary and receipt summaries do not discharge this debt, and no
user-facing text occurs between a matching success and its transition.

Immediately before emitting the terminal user summary, run the transition-debt check.
Terminal output is prohibited while any consumed successful receipt still has
an unexecuted `Outstanding transition`; execute the recorded transition in the
same active turn or return the one evidence-supported non-success state.

The closed stop set is: missing source, explicit user stop, unresolved
decision, source/identity/preparation drift, receipt drift, inaccessible
required evidence, amendment exhaustion, correction exhaustion, state-write
failure, `Pending | Blocked | Fail | Unverifiable`, or the final terminal
summary.

## Frozen execution

Read the spec and tickets only through references validated by the activated
manifest. A no-ticket preparation is one unit. Ticket mode uses the exact
prepared order and dependencies. Keep at most one unit `in_progress` and hand
each initial unit to `tk-implement` once.

`tk-implement` alone owns implementation strategy, TDD/no-TDD, production
tests, focused verification, unit Standards/Spec review, staging, and one
current-branch unit commit. Before the next handoff, verify the receipt's unit
ID, commit SHA, branch, ancestry, R/AC evidence, profile obligations, and dirty
ownership. Drive never batches units or creates a separate implementation
commit.

## Aggregate verification

After all initial units:

- map every prepared R/AC to a matching unit receipt and commit;
- verify ordered ancestry and current HEAD;
- reconcile source UI literals and material profile obligations;
- inspect cross-unit behavior and cumulative side effects;
- run the broadest relevant executable tests, build, integration, package,
  and browser verification once;
- classify failures as `change-related | pre-existing | environment |
  unverifiable`.

Freeze the successful product verification HEAD before reflection. A later
tracked reflection commit changes final HEAD but not product evidence.

## Corrective cycles

The initial unit set consumes zero corrective cycles. Only an isolated
change-related defect inside frozen R/AC may start correction `1`, `2`, or `3`.
Each correction invokes one `tk-implement` unit, then reruns affected and
aggregate verification. Permit at most three corrective cycles.

A fourth cycle, repeated or unisolated failure, new scope, or new user-owned
decision outside the amendment boundary stops mutation. Do not create a
corrective ticket, amend or squash a verified commit, or reset the cycle count.

## One Preparing amendment

Classify late ambiguity as implementation-owned, evidence-resolvable, or
user-owned. Continue the first two inside Executing. For the third, allow one
transition:

```text
Executing
→ tk-grill-me
→ tk-to-spec revalidation
→ affected tk-to-tickets rederivation
→ prep_manifest.py create --replace-active-claim-id <claim-id>
→ Executing
```

The reseal must preserve the active run owner, strictly reread every current
digest, and state whether existing commits remain valid. Never rewrite,
amend, squash, or revert verified commits automatically. If existing work
conflicts with resealed R/AC, or a repeated blocker or second user-owned
decision appears, return `Blocked` with the conflicting evidence.

## Reflection and terminal state

After product `Pass`, invoke `tk-reflect` exactly once:

```text
Mode: drive-optimistic
Success state: Pass
Outstanding transition: final receipt
Return to: tk-drive
```

Reflection classifies the preferred prevention owner and host dependency. A
no-op is successful. A verified-restored reflection failure may preserve
product `Pass`; unrestored or indeterminate state is
`Blocked | Unverifiable`.

Finalization calls:

```text
prep_state.py finalize .tigerkit/prep.md \
  --claim-id <id> \
  --status <completed|invalid|failed> \
  --finished-at <UTC>
```

Use `completed` only after product and reflection completion, `invalid` for
identity/scope/preparation invalidation, and `failed` for verified execution
failure. Strictly reread terminal state before chat output. Preserve the
manifest at the same path for diagnosis.
