# ADR 0002: Local reflection targets and durable ledger

- Status: Accepted
- Date: 2026-07-31
- Candidate release: v21.0.9
- Supersedes: ADR 0001 sections `Restrict optimistic mutation`, `Preserve bounded implementation evidence` only where they define reflection target eligibility, baseline timing, or conditional ledger creation

## Context

ADR 0001 closed the implementation feedback loop with a deliberately narrow
optimistic reflection path. Later releases restricted that path further to one
pre-existing ignored repository rule proven in the drive-start ledger.

Real use exposed three false-stop classes:

1. A repository-local target was already untracked and ignored, but the model
   classified it as risky before running the guarded Git checks that would have
   proven its state.
2. `git check-ignore` exit `1` was treated as failure or ineligibility even
   though it means the path is simply unignored. An existing untracked visible
   local rule has the same non-committed ownership boundary as an ignored one.
3. Existing user-level host-native rules were always excluded even when their
   ownership, exact path, baseline, and rollback were verifiable.

Reflection output was also inconsistent: some runs wrote
`.tigerkit/reflect.md`, while report-only or no-op runs sometimes emitted only a
chat table. That made later investigation depend on presentation choices rather
than a stable bounded ledger.

## Decision

### Persist every completed reflection

Every valid `tk-reflect` run atomically writes or replaces
`.tigerkit/reflect.md` before terminal output. This includes explicit, implicit,
active-drive, report-only, pending, applied, blocked, and no-op outcomes.

The ledger owns evidence refs, interpretation, confidence, prevention owner,
host dependency, target state, action, validation, rollback, and unresolved
reason. It remains bounded and excludes raw logs, transcripts, full diffs,
credentials, screenshots, and copied receipts. The user-facing response keeps
only the bounded `ID | Candidate | Action | Target | Why` summary table.

A run that cannot write and reread the ledger does not claim reflection
completion and returns `Unverifiable`.

### Classify repository state with Git before eligibility

Repository targets are classified from the exact worktree root using:

```text
git ls-files --error-unmatch -- <target>
git check-ignore -v --no-index -- <target>
git status --porcelain=v1 --ignored --untracked-files=all -- <target>
```

Exit semantics are part of the contract:

- `git ls-files` exit `0` is tracked and ineligible; exit `1` is untracked;
- `git check-ignore` exit `0` is `untracked-ignored`; exit `1` is
  `untracked-visible`;
- any other exit, or disagreement with `git status`, is `Unverifiable`.

Ignored state is recorded as evidence but is no longer required for local
apply.

### Permit one existing local rule target

A valid explicit reflection or active-drive tail may apply at most one exact
existing user-managed rule when all reusable-evidence and prevention-owner
gates pass.

Eligible scopes are:

- an existing repository regular file that Git proves is untracked, whether
  ignored or visible;
- an existing user-level current-host-native regular file inside the user's
  home and outside the current repository.

Tracked repository files, new or missing targets, symlinks, external or
ambiguous paths, vendor/generated targets, unknown ownership, persistent
memory, and skills remain outside direct mutation authority.

The target baseline is frozen at reflection start after product verification.
It no longer needs to have been predicted in the drive-start ledger. The
executor revalidates exact identity, ownership assertion, state, and SHA-256
immediately before mutation.

### Keep local mutation reversible and commit-free

`scripts/safe_rule_apply.py` owns both target scopes. It writes a mode-0600
before-image and metadata under `.tigerkit/reflect-backup/`, atomically replaces
the target, reruns target-state checks and shell-free validators, and restores
the exact before-image after any post-write failure.

Successful local reflection creates no commit and leaves the product and final
HEAD equal. Verified rollback preserves product `Pass` while reflection reports
`Fail`; unverified restoration is `Blocked | Unverifiable`.

The former `ignored_rule_apply.py` remains a compatibility wrapper for
repository scope.

## Consequences

Positive consequences:

- ignored repository rules no longer false-stop before Git evidence is read;
- visible untracked and ignored untracked repository files share one coherent
  local authority boundary;
- user-level personal rules can receive the same hash-bound reversible update;
- every reflection leaves a durable bounded audit surface;
- chat output stays compact while later runs can inspect complete dispositions;
- product Git history remains unchanged by local reflection.

Costs and risks:

- report-only reflection now writes `.tigerkit/reflect.md` by design;
- an unignored repository rule remains visible as `??` after apply and must be
  reported clearly;
- user-level updates can dirty a separately managed dotfiles repository, so
  verified user-managed ownership and rollback evidence are mandatory;
- the executor and ledger writer add skill-local maintenance surface.

## Verification obligations

Changes to this decision require regression coverage for:

- `untracked-ignored` repository apply;
- `untracked-visible` repository apply;
- existing user-level apply;
- tracked repository rejection;
- user/repo scope laundering rejection;
- missing ownership assertion;
- state-command failure and conflicting Git evidence;
- validation failure with exact rollback;
- atomic ledger create and replace;
- noncanonical, raw-diff, and sensitive ledger rejection;
- chat summary cardinality with complete `.tigerkit/reflect.md` ownership.

A later decision supersedes this ADR only by naming the exact target, baseline,
ledger, mutation, rollback, and terminal-output boundaries it replaces.
