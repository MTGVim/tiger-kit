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
