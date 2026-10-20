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

## Decision tree and frontier

Map the subject as a decision tree. A branch may become answerable only after its
prerequisites are settled. The current **frontier** is every unresolved decision that can
be answered now without guessing at another unresolved answer.

Work in rounds:

1. Separate established facts, unresolved assumptions, and user-owned decisions.
2. Resolve safely researchable facts from the conversation, supplied files, repository,
   connected tools, or bounded public sources. Do not ask the user for a fact that
   available evidence can answer.
3. Ask the whole current frontier in one round. Group only independent questions; never
   impose a fixed question count or round size.
4. Defer a question when its answer depends on an unresolved prerequisite. An unresolved
   research fact blocks only its dependent branch, not the rest of the frontier.
5. After the user answers, update the tree, identify contradictions or newly exposed
   assumptions, recompute the frontier, and continue.

Do not turn fact-finding into unbounded research. Investigate only facts that can
materially change the current decision tree.

## Visual questions

For unresolved spatial alternatives, read [visual questions](references/visual-questions.md) and attach one HTML comparison to the numbered text round. Keep other decisions in chat; the Boundary permits only this question aid and its canonical artifact setup.

## Question contract

Goals, priorities, trade-off preferences, scope, meaning, tone, and accepted risk belong
to the user. Never silently choose one. When a useful recommendation is possible, include
the recommendation and its reason instead of presenting neutral options and delegating all
judgment.

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
   routes. Create no additional artifact; keep only an already-authorized visual question aid.

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

Create artifacts only when this skill's task authorizes them. Before any artifact write, temporary checkout/transport, or ignore setup, read [artifact paths](references/artifact-paths.md) and apply its Git exclusion, safe-path, and ownership checks. Reuse identical content still in this context; hash-check uncertain copies and reread changed/lost content. Always repeat fresh safety checks. Default repository-owned output to `.tigerkit/`; honor explicit final destinations. Conversation-only work skips this reference and performs no file or ignore setup. Artifact handling grants no unrelated mutation or publication authority.

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

Resolve researchable facts and reuse matching authorization before asking.
For an unmet prerequisite or material user-owned decision, read [question rounds and recovery](references/questions.md)
(reuse it if still in context). Ask only answerable decisions in its plain-chat format,
with approval separate. Otherwise continue without confirmation.
<!-- /tigerkit:questions -->
<!-- tigerkit:skill-feedback -->
## Skill Feedback

For a reusable incident, retain minimal non-secret evidence and suggest `tk-retro`.
Invocation, feedback artifacts, installed-skill edits and publication require separate
authorization through the owning workflow; this pointer grants none.
<!-- /tigerkit:skill-feedback -->
