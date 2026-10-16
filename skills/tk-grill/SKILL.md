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
artifacts, scratch files, ledgers, or task graphs. Do not invoke another skill or begin
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
   routes. Do not create an artifact unless a separately selected owner later does so.

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

This skill creates no artifacts. Do not create temporary files, write reports, or edit ignore rules for this invocation; return the result in the conversation.

<!-- tigerkit:result-summary -->
## Reader-facing Result Summary

Use this shared structure only for a final user-facing session-completion message. It does not replace an owning skill's required artifact, publication preview, machine-readable nested return, approval checkpoint, verdict/status field or footer, or final question block. Keep those contracts exact. Nested phase returns remain compact and emoji-free.

When no stricter owner format applies, keep the summary concise and use these headings in this order:

```text
### 🛠️ 변경/산출물        (내용이 있을 때만)
### ✅ 확인한 것          (항상; 실제 확인·실행 내용을 기록)
### 💭 결정              (기록할 결정이 있을 때만)
### 💡 권고              (실행 가능한 권고가 있을 때만)
### ⚠️ 한계              (예외, 실패, 미실행 또는 미해결 내용이 있을 때만)
### 🧹 정리              (항상; 정리한 자원 또는 추가 정리 대상 없음)
### 👤 사람이 할 일       (항상; 없음 또는 ID·이유·다음 행동)
```

Use emoji only at the start of section headings. Keep status and evidence values as exact machine-readable tokens. Omit empty optional sections. Report planned versus executed work and distinguish completed checks from skipped, failed, blocked or unverifiable work. Put every remaining user action, including uncovered manual rows, in `👤`; do not imply the user has no work when any remains. This is the last substantive block. If the owner requires a final question block, put `👤` immediately before it; if an exact status footer is mandatory, preserve it unchanged after the substantive blocks.

Put complete absolute artifact/evidence paths on their own final lines in the relevant block. `🧹` reports only actual cleanup or the absence of owned resources; do not claim cleanup that was not checked.
<!-- /tigerkit:result-summary -->

<!-- tigerkit:output-notation -->
## Output Notation

Use ASCII numbering such as `(1) Item` or `1. Item`, with a space after the marker, in generated headings, lists, choices, tables, diagrams, and summaries. Use `- Item` for unordered items. Do not generate Unicode circled/enclosed numbers, single-character parenthesized numbers, or keycap emoji as item markers; they can overlap adjacent text in terminal renderers. Show file paths as complete absolute paths; never abbreviate a path with `...` or `…`, including in examples, because terminal renderers make paths clickable. Preserve exact code, commands, URLs, quotations, identifiers, and verified UI labels unless explicitly authorized to edit them; apply this rule to the surrounding explanation instead.

In chat responses, use a GFM pipe table for comparisons where several rows share at least two comparable attributes. Use a list for single-attribute enumerations. Keep tables narrow (about four columns or fewer), with a header row and short cells so they remain readable when the host shows raw pipes. Do not draw tables with box-drawing characters, wrap a table in a code fence, or emit an empty or ceremonial table. An owner-specific preview rule, such as summarizing a publication body's table in one line, takes precedence. These chat-table rules do not govern tables inside publication bodies or file artifacts.

In Markdown-rendered chat, documents and PR/issue bodies, write ranges with a hyphen (`146-149`) or spell out both endpoints. Escape a literal tilde as `\~` outside inline code and fenced code; preserve exact quotations and identifiers. Do not use unescaped tildes for prose ranges: GFM may render intervening text as strikethrough.

For authorized user-editable temporary input files, follow the owning skill's Artifact Paths input branch before creation and consumption. A prefilled template does not signal completed input; this rule grants no write authority.
<!-- /tigerkit:output-notation -->

<!-- tigerkit:questions -->
## User Questions

Before sending any user-owned clarification, choice, or approval, read [question rounds](references/questions.md) in this turn, reusing identical content already read this turn and still in this context. Hash-check uncertain copies; another agent's read is insufficient. Ask the whole answerable frontier in one plain-chat round; resolve facts first, preserve existing authorization, and skip question ceremony when no decision remains. Do not use question tools for ordinary TigerKit questions.

Minimum shape, even when already familiar:

```text
---

❓ **Q1 · <short title>**: <question and relevant choices>

➡️ <recommendation and reason, when supported>
```

Start the question block with a standalone horizontal rule (`---`) after the preceding context; do not add a `## Questions` or `## 질문` heading. Separate questions with blank lines and bold `❓ **Q<n> · ...**` title lines, without horizontal rules between questions. Put context before the question block and make it the final substantive block: no plan, promise, or “answer and I will proceed” line afterward, except one short reply-format hint. An approval request is its own numbered `Q`, never buried in the proposal. Defer approval whose scope still depends on an unresolved answer.
<!-- /tigerkit:questions -->
<!-- tigerkit:skill-feedback -->
## Skill Feedback

When a skill run reveals a reusable incident, preserve only minimal non-secret evidence and suggest a `tk-retro` review. Do not silently invoke it, create improvement artifacts, edit installed skills, or publish issues/PRs. Explicit implementation requests belong to the authorized change owner; this pointer grants no mutation authority.
<!-- /tigerkit:skill-feedback -->
