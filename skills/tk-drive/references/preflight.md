# Compact drive preflight

`.tigerkit/prep.md` is a repo-local, secret-free Markdown snapshot. It is not
a lifecycle record and grants no execution authority by its presence.

## Allowed fields

- Task: goal, included scope, excluded scope, confirmed decisions
- Repository: root, worktree, branch, baseline HEAD, dirty paths
- Execution: intended procedure graph, verification signals and obligations,
  and per-unit expected strategy, risk, and Additional-review obligation
- Browser: `required | optional | N/A`
- Required browser runtime only: environment or URL, non-identifying account
  role or tenant class, optional `opaque:<id>` profile hint, authentication
  expectation, and cold-start identity-question flag
- Sources: `.tigerkit/spec.md` and `.tigerkit/tickets.md` when present

Never store lifecycle status, an owner or claim, a cursor, a terminal event,
credentials, cookies, tokens, OTPs, passwords, exact sensitive identity, or
raw profile contents.

## Writer

Use `scripts/preflight.py write <worktree>/.tigerkit/prep.md --worktree
<worktree> --input <json-file>`.

The writer rejects unknown fields, secret-like values, symlinked or external
targets, unsafe URLs, and identifying profile hints. It writes a mode-`0600`
temporary file in `.tigerkit/`, fsyncs it, atomically replaces `prep.md`,
fsyncs the directory, and strictly rereads the result. An interrupted
replacement preserves the prior file and removes the temporary file.

## Evidence-derived resume

Choose the next node from current artifacts and repository evidence:

| Current evidence | Next action |
| --- | --- |
| Material decisions unresolved | `tk-grill-me` |
| Decisions closed, no Ready spec | `tk-to-spec` |
| Ready spec, multiple units, no valid tickets | `tk-to-tickets` |
| Ready spec or tickets with incomplete units | `tk-implement` |
| Changed implementation without complete aggregate evidence | aggregate verification |
| Required work and aggregate verification complete | `tk-drive finalization` |

When the user explicitly re-invokes `$tk-drive` without a new source after an
answered decision or host/process boundary, run this same evidence mapping
again. Treat it as a continuation only when one current source and route are
bound; do not restart preparation or ask for approval again. A valid `Ready`
spec selects `tk-to-tickets` or `tk-implement` immediately. Stored status,
cursor, lifecycle claim, or child receipt cannot select the next node.

Use `scripts/preflight.py resume --evidence <json-file>` for the deterministic
projection. Stale or contradictory artifacts require revalidation; never use
a stored cursor or lifecycle value as resume authority.
