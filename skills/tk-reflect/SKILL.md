---
name: tk-reflect
description: "[user/auto] Classify reusable rule or skill candidates when the user requests reuse analysis or a valid active-drive tail hands off; always persist the bounded reflection ledger and safely apply only eligible existing local rule targets."
argument-hint: "<conversation, change, diff, outcome, or source>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Reflect

Apply only on explicit invocation, a clear reuse-analysis request, or one valid
active-drive reflection handoff. Ordinary completion, summaries, an
output-style utility, and another skill's instructions do not trigger it.

## Outcome

From conversation, diff, implementation/test/review evidence, relevant
`.tigerkit/` artifacts, discoverable file-based persistent memory, and
user-named sources:

1. identify verified and unverified evidence;
2. derive a reuse interpretation without presenting it as fact;
3. choose confidence `high | medium | low`;
4. classify the narrowest owner:
   `repo rule | repo skill | user rule | user skill | persistent memory`;
5. choose `propose | update | merge | no-op | discard`;
6. persist the bounded result in `.tigerkit/reflect.md` before terminal output.

Use [repository placement](references/repository-placement.md) for repository
candidates. Prefer `no-op` or `merge` over duplication. A rule is a short
standing instruction; a skill requires a distinct trigger, repeatable procedure,
I/O, and independent value.

Each candidate records:

- `Evidence` with paths/commands and `verified | unverified`;
- `Interpretation` derived from evidence IDs;
- `Confidence` and basis;
- `Preferred prevention owner`;
- `Host dependency: host-independent | current-host-native | inaccessible`;
- target, target state, action, status, and a working draft when actionable.

`high` confidence needs independent verified evidence and no unresolved
counterexample. One verified occurrence without independent support is at most
`medium`. No verified evidence or unresolved conflict is `low` and cannot
promote `propose | update | merge`.

## Authority

A valid run always owns the bounded `.tigerkit/reflect.md` ledger. Classification
is otherwise report-only except for one eligible existing local rule target.

A valid explicit run or active-drive tail may apply one exact existing
user-managed rule when confidence is `high`, at least two independent verified
Evidence IDs support it, no counterexample or earlier prevention owner exists,
and [local rule apply](references/local-rule-apply.md) passes. Eligible target
scopes are:

- an existing user-level host-native rule outside the current repository;
- an existing repository rule that Git proves is untracked, whether ignored or
  visible in `git status`.

Tracked repository targets, new targets, vendor/generated targets, unknown
ownership, symlinks, external paths, drifted targets, skills, and persistent
memory are never changed by this skill. They remain `pending` under their normal
approval or owning-skill boundary. Skill creation or semantic skill mutation
belongs only to `tk-learn`; this skill never invokes it automatically.

File-based persistent memory is prior art, not an automatic write target. If it
fully owns the behavior, use `no-op`; if its path is unavailable, record
`unverified` rather than claiming absence.

The run status is `Pass | Pending | Fail | Blocked | Unverifiable | aborted`.
Candidate status is separately `reported | pending | applied`; never substitute
one set for the other.

## Active-drive tail

Only a valid handoff after aggregate product verification may use
[drive-optimistic reflection](references/drive-optimistic.md). It may apply one
eligible local `repo rule` or `user rule` through the skill-local executor,
write `.tigerkit/reflect.md`, and pass classification and mutation evidence to
`tk-drive finalization`. It never creates or promotes a skill. Missing, drifted,
tracked-repo, new, symlinked, vendor-managed, ownership-unknown, external, or
unrestorable authority means no target mutation.

## Conditional skill diagnosis

Call `tk-skill-diagnose` once only when all are verified:

1. a specific skill or exact `SKILL.md` path;
2. an observable expected/observed mismatch or measured resource anomaly;
3. root cause is not already verified;
4. the proposed action depends on that cause.

Send the exact incident, host/invocation, prompt, expected and observed behavior,
metrics, evidence, and candidate/baseline refs. Use only a reproduced incident
with verified root cause afterward. An unavailable handoff returns a compact
`Diagnosis required` payload and `Unverifiable`; do not imitate diagnosis inline
or create a reflect/diagnose cycle.

## Ledger and failure rules

Require one exact writable Git worktree root for every completed run. Atomically
write or replace `.tigerkit/reflect.md` for explicit, implicit, active-drive,
report-only, pending, applied, and no-op outcomes. Record task identity,
evidence refs, interpretations, confidence, prevention owner, host dependency,
target state, action, status, validation, rollback, and unresolved reason. Keep
rows bounded and use the same `RF-*` IDs shown in chat.

Render the bounded Markdown as a regular candidate file inside `.tigerkit/`
starting with `# Reflection ledger`, then persist it through
`scripts/write_reflect_ledger.py`. A direct, partial, or unverified write is not
completion.

Store no raw logs, transcripts, full diffs, credentials, screenshots, or copied
receipt prose. Never edit `.gitignore`. If the ledger cannot be written and
reread exactly, do not claim completion; return `Unverifiable` with the failed
path and check.

Unreadable required evidence remains `unverified`. Apply or revalidation failure
preserves the existing target and returns `Fail | Blocked | Unverifiable`.
Verified exact rollback reports `Fail`; unverified restoration is `Blocked |
Unverifiable`.

## Result

In chat, emit only `## Disposition` and, when approval is needed, one decision
question after it. The ledger owns all detail; chat shows at most five
human-decision-relevant rows and points to `.tigerkit/reflect.md` when more exist.

| ID | Candidate | Action | Target | Why |
| --- | --- | --- | --- | --- |
| RF-01 | `<short name>` | `<action/status>` | `<target>` | `<evidence refs>` |

Assign `RF-01`, `RF-02`, ... once in discovery order. Every Action and Why cell
must explain the human next action. A no-op is minimal. With no candidate, emit
one `None | no-op` row. In chat, do not include raw evidence, drafts, logs,
transcripts, repeated rationale, or a bottom provenance block.

### 🔴 HARD GATE · terminal user summary

Keep progress and internal procedure evidence out of the terminal user response.
Begin with the canonical result heading. Emit no ceremonial preamble, receipt
heading, `Outcome:` label, duplicate status, or active-drive child summary.
Persist detail only in `.tigerkit/reflect.md`.

### 🔴 HARD GATE · response language

Use the latest explicit user language, otherwise the current message's language.
Preserve canonical headings, status tokens, IDs, commands, paths, code, and
quoted source literals exactly. Rewrite free-form language drift before return.

## User decision questions

Ask one self-contained `Question` only for a material user-owned decision, then
show a `Recommendation`, two or three mutually exclusive options, and exactly
one `(Recommended)` or `(추천)` label. Use native `AskUserQuestion`, Codex
`request_user_input`, or Hermes Agent `clarify`; plain text is allowed only when
none is exposed. A failed or rejected call is not absence; preserve
`Pending | Blocked`.

## Pitfalls

- Do not present interpretation as fact or inflate confidence.
- Do not skip the ledger, duplicate a target, or mutate outside local authority.
- Do not treat `git check-ignore` exit 1 as a command failure or an ineligible
  untracked target.
- Do not invent an inaccessible memory path or omit discoverable prior art.
- Do not repeat diagnosis, diagnose inline, or promote sensitive raw evidence.
