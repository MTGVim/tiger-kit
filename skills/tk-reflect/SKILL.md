---
name: tk-reflect
description: "[user/auto] Classify reusable rule or skill candidates only when the user requests reuse analysis from conversation, diff, or outcome evidence, or when a valid active-drive tail hands off. Do not apply to summaries, output-style utilities, explicit invocation of another skill, or ordinary task completion. Implicit mode is report-only."
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
Default and implicit behavior is report-only.

## Outcome

From conversation, diff, implementation/test/review evidence, relevant
`.tigerkit/` artifacts, discoverable file-based persistent memory, and
user-named sources:

1. identify verified and unverified evidence;
2. derive a reuse interpretation without presenting it as fact;
3. choose confidence `high | medium | low`;
4. classify the narrowest owner:
   `repo rule | repo skill | user rule | user skill | persistent memory`;
5. choose `propose | update | merge | no-op | discard`.

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
- target, action, status, and a working draft only when actionable.

`high` confidence needs independent verified evidence and no unresolved
counterexample. One verified occurrence without independent support is at most
`medium`. No verified evidence or unresolved conflict is `low` and cannot
promote `propose | update | merge`.

## Authority

Standalone reflection does not apply a target. Rule application requires a
separate explicit approval naming target and scope. Skill creation or semantic
skill mutation belongs only to `tk-learn`; this skill reports a pending skill
candidate and never invokes it automatically.

File-based persistent memory is prior art, not an automatic write target. If it
fully owns the behavior, use `no-op`; if its path is unavailable, record
`unverified` rather than claiming absence.

The run status is `Pass | Pending | Fail | Blocked | Unverifiable | aborted`.
Candidate status is separately `reported | pending | applied`; never substitute
one set for the other.

## Active-drive tail

Only a valid handoff after aggregate product verification may use
[drive-optimistic reflection](references/drive-optimistic.md). It may apply one
eligible exact pre-existing ignored `repo rule` through the skill-local script,
write `.tigerkit/reflect.md`, and pass classification and mutation evidence to
`tk-drive finalization`. It never creates or promotes a skill. Missing,
drifted, tracked, unignored, new, symlinked, external, or unrestorable authority
means no mutation.

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

## Write and failure rules

Create `.tigerkit/reflect.md` only for an explicit report-artifact request or a
valid drive tail. Write bounded rows atomically; store no raw logs, transcripts,
diff excerpts, credentials, or screenshots. Never edit `.gitignore`.

Unreadable required evidence remains `unverified`. Apply or revalidation failure
preserves the existing target and returns `Fail | Blocked | Unverifiable`.
Outside drive-tail authority, stop at `pending | reported` until separately
approved.

## Result

In chat, emit only `## Disposition` and, when approval is needed, one decision
question after it.

| ID | Candidate | Action | Target | Why |
| --- | --- | --- | --- | --- |
| RF-01 | `<short name>` | `<action/status>` | `<target>` | `<evidence refs>` |

Assign `RF-01`, `RF-02`, ... once in discovery order. Show at most five rows and
cite `.tigerkit/reflect.md` for the rest. Every Action and Why cell must explain
the human next action; IDs and status tokens alone are not a result. A no-op is
minimal. With no candidate, emit one `None | no-op` row. In chat, no raw logs,
transcripts, diff excerpts, repeated rationale, or bottom provenance block.

### 🔴 HARD GATE · terminal user summary

Keep progress and internal procedure evidence out of the terminal user response.
Begin with the canonical result heading or sentence. Emit no ceremonial
preamble, receipt heading, `Outcome:` label, duplicate status, or active-drive
child summary. Persist detail only in an artifact already owned by this skill;
a read-only path remains read-only.

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
- Do not duplicate a target, mutate without approval, or promote a one-off
  workaround.
- Do not invent an inaccessible memory path or omit discoverable prior art.
- Do not repeat diagnosis, diagnose inline, or promote sensitive raw evidence.
