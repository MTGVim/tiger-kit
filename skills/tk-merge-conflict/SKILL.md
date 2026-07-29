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
are absent, report `Blocked: no active conflict` once and stop without source,
marker, or test investigation.

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
| operation state | resolve `MERGE_HEAD`, `rebase-merge`, `rebase-apply`, `CHERRY_PICK_HEAD`, and `REVERT_HEAD` with `git rev-parse --git-path`, then inspect only the resolved paths | one active operation kind and its step agree with status/worktree metadata | conflicting or unreadable markers are `Unverifiable`; do not infer from `.git/` paths |
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

Use only non-empty sections in this order: `Operation`, `Resolution`,
`Verification`, `Follow-up`, `Receipt`. `Operation` owns kind, state, stage, and
continue outcome; `Resolution` owns conflict, intent, and chosen result;
`Verification` owns tests, markers, and index checks. Follow-up names only
remaining work. Receipt records status, unverified items, and references
without duplication. Push requires a separate request.

When more than one conflict path is resolved, render `Resolution` as a compact
`Path | Intent | Result` table. Use a sentence when only one user-relevant row
exists. Receipt starts with `Outcome: <one user-facing sentence>`, remains a
status/provenance index, and does not repeat resolution rows.
Summarize compound intent, resolved path groups, and verification in two to
five short rows or bullets. For eight or more paths, group them into the top
five to seven intent/result rows and cite the exact remaining paths. These are
budgets, not quotas.

### 🔴 HARD GATE · response language

Before any user-facing progress, question, summary, or receipt, resolve the response language from the latest explicit user language instruction; otherwise use the current user message's language. Write every free-form user-facing sentence and every prose receipt value in that resolved language, and do not switch to English because sources, skill bodies, tools, or code are English. Keep canonical headings, receipt keys, status tokens, IDs, commands, paths, code, and exact quoted or source literals byte-stable; explain them in the resolved language around the preserved token. Before returning, scan all free-form user-facing prose and rewrite any sentence that drifts from the resolved language.

## User decision questions

When a user-owned decision blocks progress, ask one self-contained `Question`
before any `Recommendation`. Show only decision-relevant evidence, two or three
mutually exclusive options with material tradeoffs, and exactly one label
ending `(Recommended)` or `(추천)`.

Use native structured input when exposed: Claude Code `AskUserQuestion`, Codex
`request_user_input`, or Hermes Agent `clarify`. Plain text is allowed only
when none is exposed. A failed or rejected call is not absence; preserve
`Pending | Blocked`. This changes presentation, not authority or stop gates.

## DO NOT / ANTI-PATTERNS

- Do not choose one side or invent behavior without evidence.
- Do not auto-run abort, `reset --hard`, `clean`, force push, or push.
- Do not claim completion after editing files without proving unmerged state,
  verification, and operation termination.
