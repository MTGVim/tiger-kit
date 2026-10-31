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

## Shared References

Read branch-triggered criteria from the current installed owners. A missing/mismatched
owner or resource blocks that action: use `tk-setup-skills`, not memory, another installation
or unapproved installs. Reading grants no workflow or mutation authority.

- For a user-owned decision, missing approval or unmet prerequisite, read [question rounds](../tk-questioning/references/questions.md).
- Before a user-facing completion report, artifact-path handoff or multi-attribute chat comparison, read [chat delivery](../tk-writing/references/delivery.md). The task's specific output contract wins.

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
   turn, read [question rounds](../tk-questioning/references/questions.md) and apply its format to every
   round. If any frontier question compares layout, hierarchy, density or navigation
   alternatives, attach the [visual question aid](../tk-questioning/references/visual-questions.md) in this same round.
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

For unresolved spatial alternatives, read [visual questions](../tk-questioning/references/visual-questions.md) and attach one HTML comparison to the numbered text round. Keep every decision complete in chat; the aid also collects nonvisual choices from that same round. The Boundary permits only this question aid and its canonical artifact setup.

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

## Artifact Paths

Before authorized artifact writes, checkout/transport/ignore setup or temporary-input consumption,
read [artifact paths](../tk-artifacts/references/artifact-paths.md). Use safe owned nonsymlink paths
and proven Git exclusion for repository scratch; failed checks stop that file branch. Preserve
explicit final destinations and owner-specific defaults. Prefilled input is not completed input.
Cleanup targets only recorded literal resolved absolute run-owned paths, never cwd-relative paths or globs.
