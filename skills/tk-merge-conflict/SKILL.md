---
name: tk-merge-conflict
description: "[user/auto] Resolve an active merge, rebase, cherry-pick, or revert conflict from intent evidence and finish the operation. Do not apply to ordinary file edits without an active conflict."
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Merge-conflict resolution

Apply only while a merge, rebase, cherry-pick, or revert is actually in
progress with active conflicts. Do not apply to ordinary edits or an operation
that has not started.

## Contract

Before editing, inspect operation state, `git status`, unmerged index entries,
all conflict markers, and both primary sources. If operation goal and primary
sources cannot resolve intent, do not guess: stop `Blocked`. Unreadable required
state/evidence is `Unverifiable`.

First check only active-operation markers and unmerged index existence. If both
are absent, report `Not applicable` once and stop without source, marker, or
test investigation.

Use `Pass` only after every completion signal in Command evidence is verified.
Editing conflict files alone is not completion.

## 🔴 CHECKPOINT · 🛑 STOP · resolution/continue boundary

Do not finalize, stage, continue, or abort before proving operation state, every
conflict hunk, both primary sources, and resolution basis. Missing basis is
`Blocked`. When incompatible requirements can be chosen from evidence, record
the trade-off and continue.

## Workflow

1. `operation state`: identify active operation kind and state.
2. `conflict inventory`: list conflict paths/hunks and unmerged index entries.
3. `intent evidence`: map each hunk and both primary sources to intent/basis.
4. `resolution`: edit only conflict files supported by per-hunk evidence.
5. `stage and verify`: prove markers/unmerged entries removed, stage exact
   paths, and run relevant verification.
6. `continue`: run the operation-matching continue command and capture result.
7. `receipt`: return `Pass | Fail | Blocked | Unverifiable`, unverified items,
   and references to operation/verification/follow-up sections without copying
   them.

Never proceed without the required prior output. New conflicts restart at
`conflict inventory`.

Before intent analysis, map index stages 1/2/3 to actual base, current commit,
and operation target/replayed commit, recording commit IDs and paths. Especially
for rebase/cherry-pick/revert, never infer user branch or desired behavior from
`ours`/`theirs`; use operation metadata and actual commit content.

### Command evidence

| Evidence | Command contract | Completion signal | Failure route |
|---|---|---|---|
| operation/index | inspect `git status --short --branch`, `git diff --name-only --diff-filter=U`, and `git ls-files -u` together | kind, step, and HEAD match freshness fixed point; no unreviewed path | rebuild inventory; unexplained state is `Unverifiable` |
| markers | search every tracked conflict path for `^(<<<<<<<|=======|>>>>>>>)` | zero markers | remaining path/hunk is `Fail`; no continue |
| stage | `git add -- <supported-path...>` then recheck staged diff/unmerged index | only evidence-backed paths staged; zero unmerged entries | stage failure or residual entry is `Fail`; no continue |
| verification | execute relevant tests/build/static checks | command/result/scope recorded; no change-related failure | unavailable is `Unverifiable`; failing is `Fail` |
| continue | run exactly one matching `git merge --continue`, `git rebase --continue`, `git cherry-pick --continue`, or `git revert --continue` | operation ends as intended with no new conflict | capture failure/new inventory and restart |

### Operation freshness gate

At first inventory, freeze operation kind, HEAD, Git-provided step/target,
unmerged paths, and existing staged paths. Stage only paths in resolution
evidence; add a new path only after inventory gains its reason and intent basis.

Before verification and continue, reread metadata, HEAD, status, and index.
Operation disappearance, kind/step/HEAD change, or unreviewed
unmerged/staged content makes prior resolution stale. Rebuild inventory,
evidence, and verification. Unknown drift is `Unverifiable`; never claim this
run completed a vanished operation.

## Failure paths

- Incomplete inventory/intent: do not edit or stage; report missing
  state/hunk/source as `Unverifiable | Blocked`.
- Residual marker/unmerged entry or stage failure: do not continue; recheck
  status/index and report command, paths, and checks as `Fail`.
- Unavailable verification: never mark passed; report required
  command/access/environment as `Unverifiable`.
- Failed continue/new conflict: never claim completion; capture output and
  restart inventory.

Primary sources include commit messages, issue/PR, spec/tickets, adjacent
tests, and established branch behavior. Preserve both intents when compatible.
Otherwise choose from operation goal and evidence, report the trade-off, and
invent no new behavior.

An explicit conflict-resolution request authorizes finishing the active
operation, but never automatically authorizes abort, `reset --hard`, `clean`,
force push, ordinary push, unsupported mass deletion, or unrelated formatting.

## Completion report

Single owners are: `Operation` for kind/state/completion; conflict/intent/
resolution/follow-up sections for their facts; `Stage/continue` for commands and
direct outputs; `Verification` for tests/markers/index checks. Do not duplicate
stage success in Verification or decide operation completion in Stage/continue.
Follow-up names only remaining work. Receipt records status, unverified items,
and references. Push requires a separate request.

User-facing progress and receipt prose follows the user's language while
canonical headings and status tokens remain unchanged.

## DO NOT / ANTI-PATTERNS

- Do not choose one side or invent behavior without evidence.
- Do not auto-run abort, `reset --hard`, `clean`, force push, or push.
- Do not claim completion after editing files without proving unmerged state,
  verification, and operation termination.
