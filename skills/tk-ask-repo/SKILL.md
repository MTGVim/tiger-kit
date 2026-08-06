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

Read-only investigation of external codebase questions. Never edit source, artifacts, tickets, or Git history, or invoke a sibling skill. If an answer needs a decision or implementation, name the owner and stop.

## Invocation

Start only when the user selects `/tk-ask-repo`, `$tk-ask-repo`, or the host
skill picker with a concrete inbound repository question. This is a
user-invoked-only skill: `disable-model-invocation: true` and
`allow_implicit_invocation: false` are the authoritative host flags, so a
natural-language question without explicit selection does not start it.

## Evidence contract

- Every repository-state claim cites `path:line`, or says `unavailable` and why.
- Use the asker's exact symptom, label, or identifier as the first search anchor.
- Declarations prove shape, not origin. Trace values to their producing assignment, stored input, literal, or external boundary.
- "Not found" is not "absent". Search current base and relevant in-flight work first.
- For value, impact, and attribution, classify consumers `must change | must not change | unclear`. `Must not change` is mandatory; say `none found` when empty.

## Workflow

1. **Classify** as `value | structure | existence | impact | attribution`. Split mixed asks; identify the blocker.
2. **Anchor** on the visible string, identifier, route, endpoint, or symbol. If no concrete anchor survives, report attempted queries and stop `Unverifiable`.
3. **Traverse** via the matching path below; record `path:line` each hop.
4. **Sweep** relevant readers/writers for value, impact, and attribution; verify search semantics for scope-determining counts.
5. **Attribute** from evidence:
   - correct value in payload → consuming side;
   - value absent or wrong → producer and exact field;
   - both → split responsibility; name which blocks the other.
6. **Verify** current ref, variants searched, dynamic-dispatch gaps, exclusions, and every cited hop.

## Traversals

- **Value**: visible string → bound key/prop/column → consuming expression → transport field → declaring type → assignment site. Read sibling assignments and comments before judging meaning.
- **Structure**: entry point → ordered boundaries, e.g. view → transport → producer → store/external. Mark dynamic dispatch.
- **Existence**: current base ref → open/unmerged work → environment state.
  Distinguish `absent | unreleased here | present but empty/placeholder |
  present and live`. Trace introducing change for "since when".
- **Impact**: symbol/field/pattern → all readers/writers → classify every consumer; state search exclusions.
- **Attribution**: finish consuming-side trace before blaming producer. Check transforms, permissions, feature gates, conditional rendering, and same-path environment differences.

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

Lead with `Answer`. Use one to three short paragraphs for one result; compact bullets or one family-specific table for two to seven; top five to seven plus owning evidence paths for more.

Include only relevant non-empty sections:
`Evidence | Origin | Sibling fields | Path | State | Attribution |
Must change | Must not change | Remaining concerns`.

Do not echo the question, repeat evidence, propose a diff, invent an artifact, or append a receipt/provenance block. State `Blocked | Unverifiable`, next owner, or one recovery action only when actionable.

### 🔴 HARD GATE · terminal user summary

Separate progress, internal handoffs, and terminal response. Start every terminal response directly with the canonical result heading, or canonical result sentence when no heading exists. No separator, preamble, or progress recap first. Between successful active-drive phases, emit no terminal-summary opening.

Never render a receipt heading, `Outcome:` label, or terminal provenance/status block. If terminal status is required, put one exact `Status: <token>` line in its owning result section. Show paths, IDs, commits, or recovery details only when they change user action or the canonical schema requires them. Phase receipts are internal handoff envelopes: return required phase, status, IDs, `Return to`, `Success state`, or `Outstanding transition` only to the parent, never the terminal summary.

Persist provenance only in an artifact or ledger this skill already owns. Never create one only for a receipt; read-only stays read-only. Never require a shared runtime reference outside this skill.

### 🔴 HARD GATE · response language

When a user-facing result includes an absolute time, convert it to the user's local timezone and label the timezone; keep raw machine timestamps only in owned evidence. When progress or a nonterminal status is shown, use these compact markers: `🚗 active work`, `🙋 response/approval needed`, `❓ genuinely ambiguous question`, `⏳ CI/remote/re-review wait`, `🛑 checkpoint/abort stop`, `✅ completed row`, and `❌ actual failure`. Put one space after every emoji marker, omit generic no-op rows, show one legend before tables, and omit duplicate English status text in rows; preserve any required terminal `Status: <token>`.

Before user-facing progress, questions, or summaries, use the latest explicit language instruction; otherwise current message language. All free-form sentences and prose result values use it. Do not switch to English because sources, skills, tools, or code are English. Preserve canonical headings, status tokens, IDs, commands, paths, code, and exact source literals byte-stable; explain around them in the resolved language. Before return, rewrite any drifting free-form prose.

## User decision questions

Normal investigation owns no decisions: name the decision and stop `Blocked`. Only an explicitly authorized handoff may ask one self-contained `Question` before `Recommendation`, with two or three mutually exclusive trade-off options and one `(Recommended)` or `(추천)`. Render directly in chat; do not call structured question/input tools. Remain `Pending | Blocked` until answered.
## Progress

At meaningful work boundaries, standalone output uses `🚗 ask-repo · <short state>`; use `🙋 ask-repo · 응답 필요` for a question/approval gate, `⏳ ask-repo · 대기` for CI/remote/re-review wait, and `🛑 ask-repo · 중단` for a checkpoint/abort stop. Omit `tk-` from display names; a parent owns `🚗 parent > ask-repo`. Keep terminal `Status: <token>` unchanged.
