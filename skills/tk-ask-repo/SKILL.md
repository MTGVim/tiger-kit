---
name: tk-ask-repo
description: "[user] Answer an inbound question about this repository with source-located evidence: origin, flow, existence, impact, or ownership. Use when an outside question requires code investigation. Do not implement, close decisions, reproduce runtime behavior, or estimate effort."
disable-model-invocation: true
argument-hint: "<the inbound question, pasted verbatim>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# Ask Repo

Read-only investigation for questions arriving from outside the codebase. Never
edit source, artifacts, tickets, or Git history, and never invoke a sibling
skill. When the answer requires a decision or implementation, name the owner
and stop.

## Evidence contract

- Every repository-state claim cites `path:line`, or says `unavailable` with a
  reason.
- Preserve the asker's exact symptom, label, or identifier as the first search
  anchor.
- A declaration proves shape, not origin. Trace a value to the assignment,
  stored input, literal, or external boundary that produces it.
- "Not found" is not "absent". Search current base and relevant in-flight work
  before concluding absence.
- For value, impact, and attribution questions, classify consumers as
  `must change | must not change | unclear`. `Must not change` is required and
  says `none found` when empty.

## Workflow

1. **Classify** the question:
   `value | structure | existence | impact | attribution`. Split mixed asks and
   identify the blocking part.
2. **Anchor** on the asker's visible string, identifier, route, endpoint, or
   symbol. If no concrete anchor survives search, report the attempted queries
   and stop `Unverifiable`.
3. **Traverse** with the matching path below, recording `path:line` at each hop.
4. **Sweep** all relevant readers/writers for value, impact, and attribution;
   verify the search semantics used for any count that determines scope.
5. **Attribute** from evidence:
   - correct value already exists in the payload → consuming side;
   - correct value is absent or assigned incorrectly → producer and exact field;
   - both → split responsibility and say which blocks the other.
6. **Verify** current ref, searched variants, dynamic-dispatch gaps, exclusions,
   and every cited hop before reporting.

## Traversals

- **Value**: visible string → bound key/prop/column → consuming expression →
  transport field → declaring type → assignment site. Read sibling assignments
  and comments before deciding meaning.
- **Structure**: entry point → ordered boundaries such as
  view → transport → producer → store/external. Mark dynamic dispatch.
- **Existence**: current base ref → open/unmerged work → environment state.
  Distinguish `absent | unreleased here | present but empty/placeholder |
  present and live`. Trace the introducing change for "since when".
- **Impact**: symbol/field/pattern → all readers and writers → classify each
  consumer and state what the search excluded.
- **Attribution**: finish the consuming-side trace before blaming the producer.
  Check transforms, permissions, feature gates, conditional rendering, and
  same-path environment differences.

## Failure boundaries

| Condition | Result |
| --- | --- |
| anchor missing after exact and component searches | `Unverifiable` with queries run |
| required source unreadable | cite the gap; do not infer across it |
| two supported answers remain | `Blocked` with both and the decision owner |
| unclear consumer remains | list it; never silently include or exclude |
| premise contradicts current code | report the contradiction, not the premise |
| request is implementation, decision, runtime reproduction, estimate, or general knowledge | name the correct owner and stop |

## Result

Lead with `Answer`. Use one to three short paragraphs for one result, compact
bullets or one family-specific table for two to seven, and the top five to seven
plus owning evidence paths for larger results.

Include only relevant non-empty sections:
`Evidence | Origin | Sibling fields | Path | State | Attribution |
Must change | Must not change | Remaining concerns`.

Do not echo the inbound question, repeat evidence, propose a diff, invent an
artifact, or append a receipt/provenance block. State `Blocked | Unverifiable`,
the next owner, or one recovery action only when it changes what the user can do.

### 🔴 HARD GATE · terminal user summary

Keep progress and the terminal user response separate. Begin directly with `Answer`.
Do not emit a ceremonial preamble, separator, `Outcome:`, receipt heading,
duplicated status, or internal handoff fields. This skill is read-only and
creates no ledger.

### 🔴 HARD GATE · response language

Use the latest explicit user language, otherwise the current message's language.
Preserve canonical headings, statuses, paths, commands, code, and exact source
literals.

## User decision questions

Normal investigation does not own decisions: name the decision and stop
`Blocked`. Only an explicitly authorized decision handoff may ask one
self-contained `Question` before `Recommendation`, offer two or three mutually
exclusive options with tradeoffs, and mark one `(Recommended)` or `(추천)`.
Use Claude Code `AskUserQuestion`, Codex `request_user_input`, or Hermes Agent
`clarify` when exposed; plain text is allowed only when none exists. A failed or
rejected tool call preserves `Pending | Blocked`.
