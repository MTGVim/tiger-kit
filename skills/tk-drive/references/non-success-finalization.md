# Drive non-success finalization

Enter only after allowed fresh-worker correction, reviewer escalation, re-prepare,
or verifier recovery is exhausted. Preserve the originating `Fail`, `Blocked`, or
`Unverifiable` status and freeze product mutation.

Read current source, `.tigerkit/drive.md`, Git ancestry, dirty paths, and existing
verification evidence without starting new tests, builds, servers, browsers,
workers, reviewers, or cleanup. Classify approved scope as:

- `Completed`: a verified ancestor unit commit still binds to matching evidence;
- `Stopped`: the unit or verifier that produced terminal non-success;
- `Dependency blocked`: incomplete units depending on `Stopped`;
- `Not attempted`: independent units not run after mutation froze;
- `Unverified`: completion lacking current binding evidence.

Atomically update only `.tigerkit/drive.md` with this accounting, actual branch and
`HEAD`, uncommitted owned paths, evidence, status, and one supported recovery
condition. Never reset, revert, stash, clean, rewrite verified history, stage, or
commit a non-passing candidate. Preserve pre-existing user changes.

The terminal response contains only useful `Completed`, `Stopped`, `Remaining`,
and `Recovery` sections plus exactly one originating `Status:` line. Name a
concrete recovery action only when user action is required. Never describe
partial scope as `Pass`.
