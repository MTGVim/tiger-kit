---
name: tk-prototype
description: "[user/auto] Build and run a disposable UI or logic prototype when comparison can reduce uncertainty. Do not apply to production implementation or conversational idea exploration."
argument-hint: "<idea, screenshot, spec, ticket, code, or design reference>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Prototype

Apply on explicit invocation or request for executable disposable
comparison/harness. Do not auto-apply to production implementation or
conversation-only exploration.

Accept prompt, idea, screenshot, spec, ticket, code, or design reference.
Unless temporary route/harness is more useful, write under
`.tigerkit/prototypes/<slug>/`. Create parents lazily, replace atomically when
possible, never auto-archive or edit `.gitignore`, warn when scratch is tracked.

## Workflow

1. `hypothesis/success criteria`: derive measurable criteria from idea,
   references, and verification question.
2. `temporary path/boundary`: inspect repository preflight; choose existing
   toolchain/UI stack/components/tokens, temp path, artifact ownership, and
   `fake | real` integration boundary.
3. `variants/harness`: build 2–3 variants or harness with real example I/O.
4. `run`: execute selected variants/harness; capture actual output or
   screenshots plus command result.
5. `compare`: map evidence to criteria, verified differences, unverified items,
   and next decision. When parent contract records `PR evidence: required`,
   retain run-owned absolute `Screenshot: <path>` and actual image inspection
   under `## Tested`, then expose bounded handoff with `evidence_required: true`,
   criterion, evidence directory, and producer `tk-prototype`.
6. `terminal summary`: return `## Confirmed`, `## Production implication`,
   `## Tested`, `## Variants or harness`, and `## Still fake` as applicable.
   Do not append provenance/status block.

For unresolved UI comparison, build 2–3 materially different rendered
alternatives with a switch. Vary information architecture, flow, hierarchy,
navigation, or feedback—not color alone. For logic, prefer small pure harness
with example inputs/outputs and minimal adapter.

For web prototypes, inspect repository run commands, installed UI stack,
components, and design tokens. Reuse safe isolated route/harness without new
dependencies or manifest/lockfile changes. If none exists, use small
`.tigerkit/prototypes/<slug>/index.html`, `styles.css`, and `app.js`.

Hold content, data, and interaction state constant while comparing 2–3
decision-relevant concepts. Default side-by-side 2–3 columns wide, stacked
narrow. Use explicit A/B or A/B/C toggle only when simultaneous rendering harms
concept or minimum legibility. Stop at A/B if third adds no independent value;
create no prototype when repository evidence resolves decision.

Verify web output through `tk-browser-verify` Guard mode, including actual
interaction, run URL/command, and success-criteria screenshots. Check wide and
narrow only when hypothesis concerns responsiveness/layout. Clean only run-owned
tracked harnesses and temporary servers; preserve existing routes, dependencies,
and production source.

Do not commit by default. Do not invest in production abstractions/error
handling, call output production-ready, auto-promote it, or invoke another user
skill.

For PR evidence handoff, expose screenshot path, run-owned evidence directory,
criterion, and actual image inspection. This proves prototype comparison, not an
official runtime verdict.

## Failure paths

Record pre-existing temp paths and run-created files before writing.

| Trigger | First action | Still failing |
|---|---|---|
| interrupted/partial write | clean only proven run-owned incomplete artifacts | `Fail`; report unsafe cleanup path and restart condition |
| server/harness failure | preserve command, exit state, output, and fake/real boundary | `Fail`; do not escape into production/dependencies |
| run succeeds but output/screenshot evidence is unavailable | retry capture once inside same boundary | `Unverifiable`; do not claim success/Complete |
| ownership/state conflict with existing artifact | preserve existing path and record evidence | `Blocked`; choose another path before writing |
| cleanup failure | re-identify only run-owned resources and report outcome | `Fail | Unverifiable`; preserve existing route/process |
| scope expands into production/promotion/commit | stop prototype and split a separate implementation request | `Blocked`; do not auto-promote |

## 🔴 CHECKPOINT · 🛑 STOP · execution boundaries

Before execution, confirm temp path, fake/real data, and verification question.
No environment or production-scope expansion stops `Blocked | Unverifiable`.

Before reporting, reconcile command, actual output/screenshot, fake/real
boundary, and unverified scope. Missing item or failed execution prevents
`Complete`; use `Fail | Blocked | Unverifiable`.

## Contract

Record decision-relevant status once in owning section. Lead with
`## Confirmed`, then `## Production implication`, `## Tested`,
`## Variants or harness`, and `## Still fake`; omit empty sections. Confirmed
owns evidence-backed conclusions; Production implication, discard/iterate/next
decision; Tested, command results; Variants or harness, alternatives/path/run
URL and final `kept | removed` state; Still fake, fake/real and unverified scope.
Keep command mechanics after decision.

When comparing multiple criteria or variants, render `## Confirmed` as compact
`Criterion | A | B [| C] | Conclusion | Evidence` table. Use sentence for one
user-relevant row. Record whether content/data/state stayed equal. Use
`not observed` for unseen differences and `unverifiable` for missing evidence.
Do not promote unaudited aesthetic preference into conclusion.
Summarize results and selection rationale in two to five bullets or option rows.
For eight or more observations, show top five to seven and cite prototype or
evidence path owning remainder. These are budgets, not quotas.

### 🔴 HARD GATE · terminal user summary

Separate progress/internal evidence from terminal response. Start with skill's
canonical result heading, or canonical result sentence when schema has no heading.
No standalone separator, preamble, or progress recap first; no terminal opening
between successful consecutive active-drive procedure invocations.

User summary: no receipt heading, `Outcome:` label, phase-success token,
caller-return instruction, or provenance/status block. If terminal status is
required, put one exact `Status: <token>` line in owning result section, never
bottom metadata. Expose path, ID, commit, or recovery detail only when user action
changes or canonical schema requires it.

Persist provenance only in workflow-owned artifact/ledger. Read-only stays
read-only. Never require shared runtime reference outside this skill.

### 🔴 HARD GATE · response language

When a user-facing result includes an absolute time, convert it to the user's local timezone and label the timezone; keep raw machine timestamps only in owned evidence. When progress or a nonterminal status is shown, use these compact markers: `🚗 active work`, `🙋 response/approval needed`, `❓ genuinely ambiguous question`, `⏳ CI/remote/re-review wait`, `🛑 checkpoint/abort stop`, `✅ completed row`, and `❌ actual failure`. Put one space after every emoji marker, omit generic no-op rows, show one legend before tables, and omit duplicate English status text in rows; preserve any required terminal `Status: <token>`.

Before any user-facing text, resolve language from latest explicit instruction;
otherwise current user message. Use it for all free-form sentences and prose
values, regardless of English sources, skills, tools, or code. Keep canonical
headings, status tokens, IDs, commands, paths, code, and exact quoted/source
literals byte-stable; explain around them. Rewrite language drift before return.

## User decision questions

When user-owned decision blocks progress, show one self-contained `Question`
before `Recommendation`, only decision-relevant evidence, two or three exclusive
options with material tradeoffs, and exactly one `(Recommended)` or `(추천)` label.

Render variant previews, comparisons, recommendations, options, and questions in
chat, never via structured question/input tool. Preserve `Pending | Blocked`
until answer. Execution tools may still build/run disposable prototype; this
changes presentation, not execution authority or stop gates.

## DO NOT / ANTI-PATTERNS

- Do not call a prototype production-ready or auto-promote/commit it.
- Do not report fake integration as real or claim success without run evidence.
- Do not add color-only variants, dependencies, manifest/lockfile edits,
  unnecessary production abstraction, or valueless third option.
## Progress

At meaningful work boundaries, standalone output uses `🚗 prototype · <short state>`; use `🙋 prototype · 응답 필요` for a question/approval gate, `⏳ prototype · 대기` for CI/remote/re-review wait, and `🛑 prototype · 중단` for a checkpoint/abort stop. Omit `tk-` from display names; a parent owns `🚗 parent > prototype`. Keep terminal `Status: <token>` unchanged.
