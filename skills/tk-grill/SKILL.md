---
name: tk-grill
description: "[user] 아이디어·계획·결정을 빠짐없이 stress-test하고 shared understanding까지 선명하게 만들고 싶을 때 명시적으로 사용합니다. 구현할 request/ticket 준비, 일반적인 짧은 brainstorming, 자동 질문 확장에는 사용하지 않습니다."
disable-model-invocation: true
argument-hint: "<idea, decision, or plan>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: mattpocock/skills
    relationship: adapted
    upstream-skill: grilling
---

# Decision Grilling

Start only through an explicit `/tk-grill`, `$tk-grill`, or host skill selection. Do not
invoke automatically when the user asks for a quick opinion, ordinary brainstorming,
repository explanation, or implementation planning.

## Boundary

Own the interview from a rough idea, decision, or plan through confirmed shared
understanding. Keep all state in the current conversation.

Do not create or modify source, tests, config, Git state, tickets, `Seed`, SDD, domain
artifacts, general scratch files, ledgers, or task graphs. The Visual questions branch alone permits one HTML comparison under `.tigerkit/tmp/tk-grill/<run-id>/` and its required ignore setup. Do not invoke another skill or begin
implementation automatically. After synthesis, offer only relevant optional routes:

- `tk-prep` when the result has become an implementation request or ticket;
- `tk-domain` when the user wants repository-native vocabulary or a durable decision;
- stop when no further action is needed.

For a user-only next skill, give one line with `/<skill>` and say that the current
conversation carries over. Supply a full handoff prompt only for a different session;
respect `disable-model-invocation` without attempting the call or simulating its procedure.

## Decision tree and frontier

Map the subject as a decision tree. A branch may become answerable only after its
prerequisites are settled. The current **frontier** is every unresolved decision that can
be answered now without guessing at another unresolved answer.

Work in rounds:

1. Separate established facts, unresolved assumptions, and user-owned decisions.
2. Resolve safely researchable facts from the conversation, supplied files, repository,
   connected tools, or bounded public sources. Do not ask the user for a fact that
   available evidence can answer. Bind shell lookups to the verified repository root;
   quote search globs (for example `rg --glob '*.ts'` or `grep --include='*.ts'`)
   and omit separator-only commands, especially unquoted words starting with `=` in zsh.
3. Ask the whole current frontier in one round. Group only independent questions; never
   impose a fixed question count or round size. Before the first question round in this
   turn, read [question rounds](references/questions.md) and apply its format to every
   round. If any frontier question compares layout, hierarchy, density or navigation
   alternatives, attach the [visual question aid](references/visual-questions.md) in this same round.
4. Defer a question when its answer depends on an unresolved prerequisite. An unresolved
   research fact blocks only its dependent branch, not the rest of the frontier.
5. After the user answers, update the tree, identify contradictions or newly exposed
   assumptions, recompute the frontier, and continue.

Do not turn fact-finding into unbounded research. Investigate only facts that can
materially change the current decision tree.

For a consequential choice between alternatives, test the recommendation against
its decisive assumptions and priorities: identify an evidence-supported change in
conditions that would favor another option, when one is known. Research checkable
constraints rather than asking the user; ask only for user-owned priorities. If the
turning condition is unknown, retain that uncertainty rather than inventing a threshold.
Skip this analysis for minor, easily reversible choices.

## Visual questions

For unresolved spatial alternatives, read [visual questions](references/visual-questions.md) and attach one HTML comparison to the numbered text round. Keep every decision complete in chat; the aid also collects nonvisual choices from that same round. The Boundary permits only this question aid and its canonical artifact setup.

## Question contract

Goals, priorities, trade-off preferences, scope, meaning, tone, and accepted risk belong
to the user. Never silently choose one. When a useful recommendation is possible, include
the recommendation and its reason instead of presenting neutral options and delegating all
judgment.

When a recommendation depends on an existing mechanism or on when data is present,
cite the `path:line` that establishes it; otherwise investigate before recommending.

Do not ask downstream questions merely to appear thorough. Relentless means leaving no
silent decision branch, not maximizing question volume.

## Completion

When the frontier appears empty:

1. Check the whole tree for an unvisited branch, hidden assumption, contradiction, or
   intentionally open risk.
2. Summarize the current understanding briefly and ask the user to confirm that it is
   shared and complete.
3. Do not act on the result before confirmation. If the user corrects it, update the tree
   and continue from the new frontier.
4. After confirmation, return a compact synthesis of the purpose or conclusion, key
   decisions and reasons, intentionally open assumptions or risks, and optional next
   routes. Include a material turning condition when identified. Create no additional
   artifact; keep only an already-authorized visual question aid.

## Source

Adapted the decision-tree, prerequisite-aware frontier, whole-frontier rounds,
fact-versus-decision ownership, recommendations, and shared-understanding gate from
`mattpocock/skills` `skills/productivity/grilling` at commit
`6654f6b60cd9d5be8b54c6fafe44346dabeb3b76`.

TigerKit removes mandatory subagent runtime assumptions, wrappers such as `grill-me` and
`grill-with-docs`, automatic implementation transition, and persistent state. The original
copyright and MIT notice are in [LICENSE.txt](LICENSE.txt).

<!-- tigerkit:artifact-paths -->
## Artifact Paths

Artifacts require task authority. Before writes/checkout/transport/ignore setup, read [artifact paths](references/artifact-paths.md) for Git exclusion/path/ownership checks. Reuse identical in-context content; hash-check uncertainty and reread changes/loss; always recheck safety. Use `.tigerkit/` unless a destination is explicit or the eligible durable-root branch applies. Chat-only: skip file/ignore setup and this reference. This grants no unrelated mutation/publication authority. Prefer fresh directories and supported trash for authorized non-secret cleanup; target only recorded literal resolved absolute run-owned paths, never `cd` plus glob/relative deletion.

<!-- tigerkit:result-summary -->
## Reader-facing Result Summary

Return a brief result with the outcome, actual verification, material limitations
and direct deliverable links. Distinguish plans/skipped checks from executed work;
retain outstanding manual checks and real cleanup, blocker or human-action details.
Never claim unverified completion or cleanup. Preserve the owner's required artifact,
publication preview, approval boundary, machine return, exact status/footer and final
question block; keep nested returns compact and omit empty sections.
<!-- /tigerkit:result-summary -->

<!-- tigerkit:output-notation -->
## Output Notation

Use ASCII numbering (`1. Item`, `(1) Item`) and `- Item`, not enclosed/keycap numerals.
Show complete absolute clickable file paths, including examples, without ellipses.
Preserve exact code, commands, identifiers, URLs, quotations and verified UI labels
unless their edit is authorized.

For chat comparisons with multiple shared attributes, use narrow GFM pipe tables
(about four columns, header, short cells); otherwise use lists. No box-drawing,
fenced or empty tables. Owner-specific previews take precedence; publication bodies
and file artifacts retain their own table formats.

In rendered Markdown prose, use hyphens for ranges and escape literal tildes as `\~`;
preserve exact code, quotations and identifiers.

For authorized temporary input files, follow Artifact Paths before creation and
consumption; a prefilled template is not completed input. This grants no write authority.
<!-- /tigerkit:output-notation -->

<!-- tigerkit:questions -->
## User Questions

Investigate facts; reuse authorization. For user-owned decisions read
[question rounds](references/questions.md); otherwise proceed.
Plain chat, even one approval: standalone `---`, then
`❓ **Q<n> · <title>**: <question>` and `➡️ <recommendation>` per item.
Ask only settled-prerequisite questions; separate approval.
Questions come last; put status, risks and plans before them.
<!-- /tigerkit:questions -->
<!-- tigerkit:skill-feedback -->
## Skill Feedback

For a reusable incident, retain minimal non-secret evidence in the current conversation
and suggest `tk-retro`; do not write it to persistent memory unless the user asks.
Invocation, feedback artifacts, installed-skill edits and publication require separate
authorization through the owning workflow; this pointer grants none.
<!-- /tigerkit:skill-feedback -->
