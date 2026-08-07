# TigerKit Issue 277 structural migration

TigerKit now treats `tk-drive` as one product-change controller instead of a
chain of independently invoked workflow phases.

## Invocation

Start a change with one explicit source:

```text
$tk-drive <source>
```

Drive performs `Prepare -> Execute -> Close gaps -> Finalize` in one active run.
Former standalone preparation, unit-slicing, and implementation phase calls have
no replacement invocation. Small ordinary edits still stay in the current
conversation without Drive.

## One approval

Prepare reads source and repository evidence, resolves safe defaults, records
material assumptions and alternatives, derives Ready R/AC plus dependency waves,
and shows one final approval surface. `tk-grill-me` is used only when a user-owned
decision prevents a safe executable plan.

The approval authorizes only the displayed snapshot. Material source, scope,
branch/head, remote-state, or irreversible-decision drift returns to Prepare.
An unchanged plan does not receive another routine approval.

## Fresh-worker mutation

Drive never authors product, test, or configuration changes. Every primary and
corrective candidate comes from a fresh worker with one bounded unit. Missing
worker dispatch is `Blocked`, not a controller-edit fallback.

Worker selection is automatic per dispatch:

- `cheapest` for mechanical local work with complete evidence;
- `standard` for ordinary multi-file implementation or debugging;
- `strongest` for design-heavy, unknown-cause, security/data-sensitive, or broad
  reasoning work;
- `host-default` when per-spawn selection is unavailable.

There is no user/repository model mapping or provider-name configuration surface.

## Verification and commits

The unit order is:

```text
fresh worker candidate
-> required tests/checks/browser verifier
-> R/AC acceptance-gap closure
-> bounded fresh corrective worker when needed
-> one verified unit commit
```

Mandatory TigerKit review is limited to the gap between approved R/AC and current
evidence. Broader style, architecture, optimization, security, and performance
review remains outside this workflow unless it is explicit acceptance or
repository policy.

## State migration

Drive uses one repo/worktree-local Markdown ledger:

```text
.tigerkit/drive.md
```

Do not migrate split phase artifacts into parallel ledgers. Recreate the current
task from source and repository evidence in `drive.md`; artifact presence alone
grants no authority. Nested workers, reviewers, and verifiers return compact
evidence instead of writing lifecycle Markdown.

## PR workflow migration

`tk-pr-respond` now prepares one exact-PR resolution and publication plan, asks
once, then runs fresh-worker units, acceptance verification, commits, and the
already-approved bounded remote actions. There is no later publication approval.
Standalone state is `.tigerkit/pr-respond.md`.

The former PR-triage wrapper has no replacement skill. Use
`$tk-pr-sweep --report` for read-only inventory; interactive `$tk-pr-sweep`
prepares one multi-PR batch approval and invokes the moved deterministic triage
script directly. Top-level state is `.tigerkit/pr-sweep.md`; nested Respond,
Rebase, workers, reviewers, and verifiers write no competing Markdown ledger.

## Authority

Drive may create the approved verified current-branch unit commits. Push, PR,
merge, tag, release, publish, and history rewriting still require their separate
explicit owners and authority.

## Install/update

```bash
npx skills update --global --yes
```

For repository validation, reinstall from the checkout and confirm the catalog
lists only the current skill surface.
