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

Apply only during active merge, rebase, cherry-pick, or revert with conflicts. Never apply to ordinary edits or unstarted operation.

## Contract

Before editing, inspect operation state, `git status`, unmerged index entries, all conflict markers, and both primary sources. If operation goal and primary sources cannot resolve intent, never guess: stop `Blocked`. Unreadable required state/evidence is `Unverifiable`.

First check only active-operation markers and unmerged index existence. If both absent, report `Blocked: no active conflict` once; stop without source, marker, or test investigation.

Use `Pass` only after verifying every completion signal in Command evidence. Editing conflict files alone is incomplete.

## 🔴 CHECKPOINT · 🛑 STOP · resolution/continue boundary

Never finalize, stage, continue, or abort before proving operation state, every conflict hunk, both primary sources, and resolution basis. Missing basis is `Blocked`. When evidence selects among incompatible requirements, record trade-off and continue.

## Workflow

1. `operation state`: identify active operation kind/state.
2. `conflict inventory`: list conflict paths/hunks and unmerged index entries.
3. `intent evidence`: map each hunk and both primary sources to intent/basis.
4. `resolution`: edit only conflict files supported by per-hunk evidence.
5. `stage and verify`: prove markers/unmerged entries removed, stage exact paths, run relevant verification.
6. `continue`: run operation-matching continue command; capture result.
7. `receipt`: return `Pass | Fail | Blocked | Unverifiable`, unverified items, and references to operation/verification/follow-up sections without copying them.

Never proceed without required prior output. New conflicts restart at `conflict inventory`.

Before intent analysis, map index stages 1/2/3 to actual base, current commit, and operation target/replayed commit; record commit IDs/paths. Especially for rebase/cherry-pick/revert, never infer user branch or desired behavior from `ours`/`theirs`; use operation metadata and actual commit content.

### Command evidence

| Evidence | Command contract | Completion signal | Failure route |
|---|---|---|---|
| operation state | resolve `MERGE_HEAD`, `rebase-merge`, `rebase-apply`, `CHERRY_PICK_HEAD`, and `REVERT_HEAD` with `git rev-parse --git-path`, then inspect only resolved paths | one active operation kind and step agree with status/worktree metadata | conflicting/unreadable markers are `Unverifiable`; never infer from `.git/` paths |
| operation/index | inspect `git status --short --branch`, `git diff --name-only --diff-filter=U`, and `git ls-files -u` together | kind, step, and HEAD match freshness fixed point; no unreviewed path | rebuild inventory; unexplained state is `Unverifiable` |
| markers | search every tracked conflict path for `^(<<<<<<<|=======|>>>>>>>)` | zero markers | remaining path/hunk is `Fail`; no continue |
| stage | `git add -- <supported-path...>` then recheck staged diff/unmerged index | only evidence-backed paths staged; zero unmerged entries | stage failure/residual entry is `Fail`; no continue |
| verification | execute relevant tests/build/static checks | command/result/scope recorded; no change-related failure | unavailable is `Unverifiable`; failing is `Fail` |
| continue | run exactly one matching `git merge --continue`, `git rebase --continue`, `git cherry-pick --continue`, or `git revert --continue` | operation ends as intended with no new conflict | capture failure/new inventory; restart |

### Operation freshness gate

At first inventory, freeze operation kind, HEAD, Git-provided step/target, unmerged paths, and existing staged paths. Stage only paths in resolution evidence; add new path only after inventory gains reason/intent basis.

Before verification/continue, reread metadata, HEAD, status, and index. Operation disappearance, kind/step/HEAD change, or unreviewed unmerged/staged content stales prior resolution. Rebuild inventory, evidence, and verification. Unknown drift is `Unverifiable`; never claim this run completed vanished operation.

## Failure paths

- Incomplete inventory/intent: never edit/stage; report missing state/hunk/source as `Unverifiable | Blocked`.
- Residual marker/unmerged entry or stage failure: never continue; recheck status/index and report command, paths, checks as `Fail`.
- Unavailable verification: never mark passed; report required command/access/environment as `Unverifiable`.
- Failed continue/new conflict: never claim completion; capture output and restart inventory.

Primary sources: commit messages, issue/PR, spec/tickets, adjacent tests, established branch behavior. Preserve both intents when compatible. Otherwise choose from operation goal/evidence, report trade-off, invent no new behavior.

Explicit conflict-resolution request authorizes finishing active operation, but never automatically authorizes abort, `reset --hard`, `clean`, force push, ordinary push, unsupported mass deletion, or unrelated formatting.

## Completion report

Use only non-empty sections in order: `Operation`, `Resolution`, `Verification`, `Follow-up`. `Operation` owns kind, state, stage, status, unverified items, references, continue outcome; `Resolution` owns conflict, intent, chosen result; `Verification` owns tests, markers, index checks. Follow-up names only remaining work. Push needs separate request.

For multiple resolved conflict paths, render `Resolution` as compact `Path | Intent | Result` table; use sentence for one user-relevant row. Begin with resolved result; never repeat resolution rows or append metadata. Summarize compound intent, resolved path groups, and verification in 2–5 short rows/bullets. For 8+ paths, group into top 5–7 intent/result rows and cite exact remaining paths. Budgets, not quotas.

### 🔴 HARD GATE · terminal user summary

Separate progress commentary, internal procedure evidence, and terminal user response. Begin every terminal user-facing response directly with skill's canonical result heading or, if result schema has no heading, canonical result sentence. Never place standalone separator, ceremonial preamble, or progress recap before opening. Never emit terminal user-summary opening between successful consecutive active-drive procedure invocations.

Never render receipt heading, `Outcome:` label, phase-success token, caller-return instruction, or terminal provenance/status block in user summary. When result requires terminal status, emit single exact `Status: <token>` line in owning result section, not bottom metadata block. Expose path, ID, commit, or recovery detail only when it changes user action or canonical result schema requires it.

Persist provenance only in workflow-owned artifact/ledger. Read-only skill remains read-only. Never require shared runtime reference outside this skill.

### 🔴 HARD GATE · response language

When a user-facing result includes an absolute time, convert it to the user's local timezone and label the timezone; keep raw machine timestamps only in owned evidence. When progress or a nonterminal status is shown, use these compact markers: `🚗 active work`, `🙋 response/approval needed`, `❓ genuinely ambiguous question`, `⏳ CI/remote/re-review wait`, `🛑 checkpoint/abort stop`, `✅ completed row`, and `❌ actual failure`. Put one space after every emoji marker, omit generic no-op rows, show one legend before tables, and omit duplicate English status text in rows; preserve any required terminal `Status: <token>`.

Before user-facing progress, question, or summary, resolve language from latest explicit user language instruction; otherwise current user message's language. Write every free-form user-facing sentence and prose result value in that language. Never switch to English due to sources, skill bodies, tools, or code. Keep canonical headings, status tokens, IDs, commands, paths, code, and exact quoted/source literals byte-stable; explain around preserved token in resolved language. Before return, scan free-form user prose and rewrite drift.

## User decision questions

When user-owned decision blocks progress, ask one self-contained `Question` before any `Recommendation`. Show only decision-relevant evidence, two or three mutually exclusive options with material tradeoffs, and exactly one label ending `(Recommended)` or `(추천)`.

Render question, recommendation, and options directly in chat; never call structured question/input tools. Preserve `Pending | Blocked` until answer. This changes presentation, not authority or stop gates.

## DO NOT / ANTI-PATTERNS

- Never choose one side or invent behavior without evidence.
- Never auto-run abort, `reset --hard`, `clean`, force push, or push.
- Never claim completion after editing files without proving unmerged state, verification, and operation termination.
## Progress

At meaningful work boundaries, standalone output uses `🚗 merge-conflict · <short state>`; use `🙋 merge-conflict · 응답 필요` for a question/approval gate, `⏳ merge-conflict · 대기` for CI/remote/re-review wait, and `🛑 merge-conflict · 중단` for a checkpoint/abort stop. Omit `tk-` from display names; a parent owns `🚗 parent > merge-conflict`. Keep terminal `Status: <token>` unchanged.
