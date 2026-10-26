# Reader Purpose: Diátaxis-Informed Documentation

Use this reference for substantive reader-facing lessons, explanations, change
walkthroughs and research reports. It governs the reader's purpose and content
order, not renderer implementation. Preserve the calling skill's scope, source
evidence, explicit format and existing output contract. One primary purpose
per unit is usually enough; another form may support that purpose.

## Choose by what the reader needs next

| Form | Reader's need | Author's primary job |
| --- | --- | --- |
| Tutorial (learning) | Acquire a skill by doing | Guide a feasible activity, show expected observations, offer a small changed case and reasoned feedback |
| How-to (task) | Complete a specific real task | Give safe prerequisites, conditional actions and verifiable results without a whole beginner curriculum |
| Reference (lookup) | Retrieve accurate facts while working | Organize precise fields, defaults, behavior and constraints by the thing described |
| Explanation (understanding) | Understand why or how something happens | Connect a concrete mechanism to causes, context, alternatives, outcomes and evidence |

A numbered procedure is not necessarily a tutorial, and a table is not
automatically reference. The reader's immediate goal matters more than the
document extension, layout, skill name or presence of examples. The calling
owner keeps its task: `tk-teach` normally leads learning, `tk-explain` and
`tk-explain-diff` explain a concept or pinned change, and `tk-research`
produces a decision-ready evidence report. Do not reroute the request,
discard its constraints or relabel the work without an explicit reason.

## Build the appropriate experience

- **Tutorial:** Give the learner a reachable goal and only the prerequisites
  required now. Demonstrate or prompt one meaningful choice, prediction,
  trace or action with clear input. State what the learner should observe,
  why it matters and how to check progress before the next attempt. Add
  a changed-condition practice with grounded feedback and retry. Longer
  background belongs where it helps; do not omit required mechanisms.
  An offline prediction or annotated reasoning task is still practice
  when execution is unavailable. Never invent runtime results, a submitted
  learner answer, or demonstrated mastery.
- **How-to:** State the concrete desired outcome, environment, permissions
  and starting conditions. Provide dependency-ordered steps, real branches,
  observable postconditions and safe recovery when supported. Distinguish
  commands to perform from actions actually executed. Do not substitute a
  broad lesson for the reader's immediate task.
- **Reference:** Make exact information easy to locate. Use established
  identifiers, units, types, defaults, version boundaries and exceptions
  where supported. Keep facts tied to trustworthy sources. Avoid a long
  narrative that makes lookup hard; missing information is not verified
  completeness.
- **Explanation:** Begin with the reader's question and a coherent example.
  Trace relevant causal relations, design choices, boundaries and
  consequences. Use figures, comparisons and optional understanding checks
  where useful; action-based practice is not the goal by default.

## Keep genre boundaries and navigation intentional

A focused artifact can include a small supporting procedure, reference
table or explanation, or link to a dedicated resource. Do not create four
mandatory sections or redundant modes. A tutorial can be one scrollable
HTML page; a genuine sequence of lessons can link previous/next files.
Split pages only when the cognitive boundary and current collection
contract justify it. Respect explicitly requested single-file formats
and existing lessons. Do not force a stepper, video, course runtime,
progress tracker, hidden tabs, file rewrite or browser verification.
When the mechanism genuinely requires controlled intermediate states,
reuse visual-grammar/interactive-example contracts, preserving the
static explanation, accessibility and meaningful state changes.

## Review within the existing owner workflow

Check whether the document's title, content and reader activity serve
the chosen need. For tutorials, can the reader attempt the first action,
know the expected observation, and apply feedback to the next case?
For how-to, can the stated goal be achieved with supported conditions
and safe steps? For reference, are entries accurate, bounded, findable
and versioned? For explanation, can a reader follow the actual mechanism
without inventing hidden steps? Does supplementary content support rather
than displace the main purpose? Keep authored checks, real execution,
reader responses and mastery evidence distinct.

Use the calling owner's existing content review; this adds no new review
agent, review report, scoring rubric or automatic browser matrix.

## Origin

Independent TigerKit synthesis informed by Daniele Procida's Diátaxis:
https://diataxis.fr/ , https://diataxis.fr/tutorials/ ,
https://diataxis.fr/how-to-guides/ , https://diataxis.fr/reference/ ,
https://diataxis.fr/explanation/ . These are provenance links,
not imported upstream prose, diagrams, assets or executable code.
