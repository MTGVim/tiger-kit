# Drive non-success finalization

`tk-drive non-success finalization` owns terminal accounting only after
`phases.md` normalizes a child-native result to `Fail | Blocked |
Unverifiable` and every allowed alternate edge, retry, and amendment is
exhausted. It is internal, read-only, and has no outgoing edge.

## Freeze boundary

At entry, stop product and source mutation. Do not edit, create, or delete
product files; stage or commit; reset, revert, stash, or clean; start a new
test, build, server, or browser command; or invoke another implementation,
reviewer, browser, learning, or phase-owner child.

Read-only artifact and Git audits remain allowed. Do not infer missing evidence
from self-report or rerun work merely to improve the terminal receipt.

## Scope accounting

Reread applicable source, prep, spec, tickets, implementation ledger, and
existing browser evidence, then audit branch, `HEAD`, current-branch ancestry,
and dirty paths. Classify selected scope as:

- `Completed`: an ancestor commit still binds to matching unit receipt, review,
  and verification evidence;
- `Stopped`: the unit or procedure that produced terminal non-success;
- `Dependency blocked`: an incomplete unit transitively depends on `Stopped`;
- `Not attempted`: an incomplete independent unit was not run after mutation
  froze;
- `Unverified`: a change or completion claim lacks current binding evidence.

Branch, `HEAD`, ancestry, or receipt drift prevents `Completed`. Exclude
pre-existing dirty user paths from drive ownership. Never call partial scope
`Pass`.

## Ledger ownership

Keep existing owners instead of creating another run ledger:

- `.tigerkit/prep.md`, `.tigerkit/spec.md`, existing browser evidence, and
  `.tigerkit/reflect.md` are read-only here.
- `tk-implement` owns the no-commit attempt in
  `.tigerkit/implementation.md` and writes native status, actual branch and
  `HEAD`, changed or uncommitted paths, executed verification, unverified
  scope, `commit: none`, failure or blocker, and one recovery condition before
  returning. Finalization rereads that receipt and does not rewrite it.
- When `.tigerkit/tickets.md` already exists and the exact current ticket is
  known, `tk-drive non-success finalization` is the sole downstream writer
  allowed to add bounded `Last attempt`, `Evidence`, and `Recovery` fields to
  that incomplete ticket. Use same-directory temporary replacement, preserve
  completed receipts and unrelated pending tickets byte-for-byte, and reread
  the result. Do not invoke `tk-to-tickets` again.
- When no exact ticket ledger/current ticket exists, write no terminal ledger.

Never create `.tigerkit/run.md`, `.tigerkit/findings.md`, another status file,
a cursor, a lifecycle claim, raw logs, full diffs, transcripts, or secrets.

## Recovery

Choose exactly one action supported by current evidence:

1. consume a pending decision answer in the same conversation;
2. restore environment or tooling, then explicitly rerun the same source;
3. manually reconcile the failed unit's uncommitted state, then explicitly
   rerun;
4. start fresh from source when prep, spec, ticket, branch, or receipt evidence
   drifted.

Do not promise automatic continuation or start another independent unit.

## Terminal response

Lead with one result sentence and omit empty sections. Use `Completed`,
`Stopped`, `Remaining`, and `Recovery` only when applicable. A multi-unit
`Completed` table may use `Unit | Outcome | Commit | Evidence`; `Outcome` is
only a table header, never a top-level `Outcome:` label. `Remaining`
distinguishes `Dependency blocked`, `Not attempted`, and `Unverified`.

End with exactly one originating `Status: Fail`, `Status: Blocked`, or
`Status: Unverifiable` line. Never emit `Status: Pass` or a new partial status.
