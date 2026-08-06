---
name: tk-drive
description: "[user] Drive an explicit source through decision closure, a Ready spec, conditional tickets, verified unit commits, aggregate verification, and finalization in one continuous run. Use only when selected explicitly with a source, or when resuming an unfinished drive in the same conversation."
disable-model-invocation: true
argument-hint: "<source, request, issue, or existing Ready spec>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# Drive

Start only when user selects `/tk-drive`, `$tk-drive`, or the host skill picker with a source, or explicitly re-invokes it in the same conversation after a pending decision or unfinished drive. A no-source re-invocation is a continuation request only after current artifacts and repository evidence validate one resumable source; it does not create a second run or grant a new approval. Ordinary implementation requests, generic continuation, artifacts, or new sessions neither start nor resume it.

## Authority

One start authorizes Preparing, Executing, aggregate verification, unit review, one verified current-branch commit per selected unit, and up to three corrective unit commits. It excludes push, PR, merge, tag, release, publish, history rewriting, and out-of-scope mutation.

Drive owns workflow and the only active-drive terminal response. Child procedures own specialist work and pass native result state directly to the next applicable node. A successful run never stops to ask the user to invoke drive again.

## Direct procedure graph

```text
tk-drive preflight
  -> tk-grill-me, only for material user-owned decisions
       -> tk-prototype, only when a bounded comparison helps
       -> tk-grill-me
  -> tk-to-spec
  -> tk-to-tickets, only for multiple independently verifiable units
  -> tk-implement, once per selected unit
       -> tk-merge-conflict, only for an active conflict
       -> tk-implement
  -> aggregate verification
       -> tk-browser-verify, only when required
       -> corrective tk-implement, at most three cycles
  -> tk-drive finalization

terminal non-success
  -> freeze product mutation
  -> tk-drive non-success finalization
```

Use complete edge/state-normalization contract in [phases.md](references/phases.md). Apply each edge's entry, success, failure, and next-node contract. Successful nodes invoke the next applicable node in the same active turn; allowed recovery runs before terminal finalization.

Continuation is prompt-directed, not a durable scheduler or guaranteed cross-turn execution. After host/process boundaries, resume by rereading current artifacts and repository evidence.

## Re-invocation

A no-source `$tk-drive` after an answered decision or host/process boundary
resumes the same source only after rereading current artifacts and repository
evidence. Do not restart, re-ask, or stop at valid `Ready`; continue to the next
node, verification, and finalization. Stale/contradictory evidence emits one
`❓` checkpoint before mutation; cursor, lifecycle claim, and child receipt are
never authority.

## Progress

At plan, meaningful node transitions, aggregate verification, finalization, and
non-advancing boundaries, emit one line such as `▶️ drive > implement 2/4`,
`❓ drive > grill-me · 답변 필요`, `🟢 spec · Ready · 다음 단계 수동`, or
`⏳ drive > browser-verify · server`. Omit `tk-`; `▶️` auto-continues, `❓`
needs user input, `🟢` is standalone manual `Ready`, and `⏳` is machine/remote
wait. Keep only the one decisive token (unit/count, route, or wait reason); the
marker and route encode result/next action. A Ready child consumed by drive
stays `▶️`. Direct skills show only their name. Suppress receipts, reasoning,
logs, timers, approval requests, and nonterminal `Status:` lines; actual skill
names/contracts keep `tk-`.

Use `✅ Pass`, `⏳ Waiting`, `⚠️ Advisory`, `❌ Fail`, `⛔ Blocked`, and `❓ Unverifiable` for matching outcomes; preserve terminal `Status: <token>` exactly.

For an intentional decision checkpoint, emit `❓ drive > grill-me · 답변 필요`
before the question:

```text
Question: <one user-owned decision>
```

This is nonterminal commentary. Preserve native `Pending`, emit no terminal
`Status:` line, and invoke no downstream procedure until the explicit answer.
Use the same form when only the final agreed-goal approval remains, identifying
that approval in `Decision` and keeping `tk-grill-me` as the current node.

## Preparing

Before product mutation:

1. Resolve repository instructions, branch, baseline `HEAD`, worktree, and pre-existing dirty paths.
2. Read complete source. Find at most seven relevant durable prior-art items from applicable rules, ADRs, tests, types, lint, CI, repository skills, and code invariants. Exclude raw sessions, implementation scratch, pending drafts, arbitrary global state, unrelated work, and inaccessible host-only rules.
3. Close only material user-owned decisions through `tk-grill-me`; use `tk-prototype` only when evidence reduces the decision.
4. Produce or validate one Ready R/AC spec with `tk-to-spec`.
5. Use `tk-to-tickets` only for multiple independently verifiable vertical units; otherwise one no-ticket unit.
6. Seal each unit's expected `direct | delegated`, risk `low | high | unknown-until-diff`, and Additional review `required | not-required | unknown-until-diff`; evidence may raise but never silently lower obligations.
7. Write compact `.tigerkit/prep.md` via [preflight.md](references/preflight.md); immediately start Executing.

### 🔴 HARD GATE · source UI writing

Freeze every user-visible source literal and its `authorized change` in R/AC before mutation. Executing compares source, current value, candidate/staged diff, and rendered result. Missing evidence, unresolved mismatch, or wording outside authorization stops before commit.

### 🔴 HARD GATE · risk-based verification profile

During Preparing, classify material signals/obligations from current evidence. Executing consumes the sealed profile. Drive cannot add unsupported obligations, remove obligations, or substitute weaker evidence.

Classify PR evidence separately as `required | optional | N/A`; seal it and a criterion in Ready spec/preflight when applicable. `required` only when a confirmed source demands attached visual proof or a browser-rendered acceptance criterion cannot be meaningfully code-reviewed; `optional` when screenshot aids review but is not acceptance-critical; `N/A` when no browser-visible result exists. Browser verification being `required` does not itself make PR evidence `required`. Return material ambiguity to Preparing.

Browser preflight is `required | optional | N/A`. Private runtime identity is material user-owned input. Store only opaque profile hint plus `intentionally omitted`; re-request missing identity on cold start. Runtime rehydration is not a Preparing amendment.

## Executing

For each unit:

1. pass only the unit ID, exact R/AC, scope, order, verification profile, and
   artifact paths plus current delta to `tk-implement`; let the child read the
   full artifact instead of repeating unrelated source, history, or receipts;
2. accept only a verified one-unit commit or bounded non-success handoff;
3. preserve pre-existing user changes; audit commit ancestry;
4. treat `Pass` as internal loop signal: without terminal response, pause, or confirmation, render Drive's progress checkpoint and invoke `tk-implement` for the next unit. Exit only when all units are committed or bounded non-success remains after recovery.

Use `tk-merge-conflict` only for an active merge, rebase, cherry-pick, or revert conflict; then return to the interrupted unit.

## Aggregate verification

After all commits, verify R/AC traceability, ancestry, unit boundaries, excluded scope, frozen profile, and broad repository checks. Use `tk-browser-verify` when preflight or changed UI requires runtime evidence.

Passing initial implementation uses zero corrective cycles. Isolated defects may use at most three corrective `tk-implement` cycles. Fourth cycle, repeated unchanged failure, unisolated failure, or scope expansion freezes mutation.

One late material user-owned decision may use one amendment through `tk-grill-me`, Ready-spec revalidation, affected-ticket rederivation, and prep refresh. A second amendment or incompatible committed work is terminal `Blocked`; never rewrite verified history automatically.

## Non-success

After recovery edges exhaust, normalize child state through `phases.md`, freeze mutation, and enter internal read-only finalizer. Follow [non-success finalization](references/non-success-finalization.md). It has no outgoing edge. Never clean failed units, invoke another specialist, create partial status/new ledger, or start an independent unit.

## Success finalization

After aggregate verification passes, finish directly. Reread source, spec, tickets if present, prep, implementation evidence, ancestry, and verification before one terminal response. TigerKit owns no post-session reflection or persistent-memory phase.

Lead with one result sentence: `✅ Pass` for full success; non-success uses mapped marker without changing canonical `Status: <token>`. Then `Implemented` with two to seven behavior bullets and `Verification` with one to four aggregate bullets. For multiple units, add compact `Ticket | Outcome | Commit` and `Unit | Strategy | Additional review | Fix rounds | Result` tables; summarize review routes, not raw per-unit text. Use a sentence for one user-relevant row. If results exceed limits, show top five to seven by user impact and verification value. Include `Remaining risks` only when meaningful. End `Verification` with exactly `Status: Pass`; terminal non-success belongs to read-only finalizer.

### 🔴 HARD GATE · terminal user summary

Separate progress, internal procedure evidence, and terminal response. Begin terminal response with canonical result heading or sentence. No separator, preamble, or recap first; no terminal-summary opening between consecutive successful active-drive procedure invocations.

Never render a receipt heading, `Outcome:` label, phase-success token, caller-return instruction, or terminal provenance/status block. Put one required exact `Status: <token>` line in the owning result section. Show paths, IDs, commits, or recovery details only when actionable or schema-required.

Persist provenance only in an existing workflow-owned artifact/ledger. Never require shared runtime references outside this skill.

### 🔴 HARD GATE · response language

When a user-facing result includes an absolute time, convert it to the user's local timezone and label the timezone; keep raw machine timestamps only in owned evidence. When a table uses emoji status markers, show one legend before the table and omit duplicate English status text in its rows; preserve any required terminal `Status: <token>`.

Before user-facing progress, questions, or summaries, use latest explicit language instruction; otherwise current message language. All free-form sentences and prose values use it; never switch to English because sources, skills, tools, or code are English. Preserve canonical headings, status tokens, IDs, commands, paths, code, and exact source literals byte-stable. Rewrite language drift before return.

## User decision questions

When a user-owned decision blocks Preparing or the one amendment, ask one self-contained `Question` before `Recommendation`. Show only relevant evidence, two or three mutually exclusive options with material tradeoffs, and exactly one `(Recommended)` or `(추천)`.

Render directly in chat; do not call structured question/input tools. Emit the
nonterminal `❓ drive > grill-me · 답변 필요` checkpoint before the question. Remain
native `Pending` for an unanswered question. If the originating state is
`Blocked`, preserve that terminal state and follow non-success finalization
instead of presenting it as a user-input checkpoint. An explicit answer resumes
the existing graph; an explicit `$tk-drive` re-invocation in the same
conversation performs the same current-evidence resume when the host did not
continue automatically.
