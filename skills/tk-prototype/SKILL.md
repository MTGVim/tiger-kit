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

Apply on explicit invocation or a request for an executable disposable
comparison/harness. Do not auto-apply to production implementation or
conversation-only exploration.

Accept a prompt, idea, screenshot, spec, ticket, code, or design reference.
Unless a temporary route/harness is more useful, write under
`.tigerkit/prototypes/<slug>/`. Create parents lazily, replace atomically when
possible, never archive automatically or edit `.gitignore`, and warn when
scratch is tracked.

## Workflow

1. `hypothesis/success criteria`: produce measurable criteria from the idea,
   references, and verification question.
2. `temporary path/boundary`: inspect repository preflight; choose existing
   toolchain/UI stack/components/tokens, temp path, artifact ownership, and
   `fake | real` integration boundary.
3. `variants/harness`: build 2–3 variants or a harness with real example I/O.
4. `run`: execute selected variants/harness and capture actual output or
   screenshots plus command result.
5. `compare`: map evidence to criteria, verified differences, unverified items,
   and next decision.
6. `receipt`: return status plus `## Tested`, `## Variants or harness`,
   `## Confirmed`, `## Still fake`, and `## Production implication`. These
   sections are the receipt; do not add another Receipt.

For unresolved UI comparison, build 2–3 materially different rendered
alternatives with a switch. Vary information architecture, flow, hierarchy,
navigation, or feedback, not color alone. For logic, prefer a small pure
harness with example inputs/outputs and minimal adapter.

For web prototypes, inspect repository run commands, installed UI stack,
components, and design tokens. Reuse a safe isolated route/harness without new
dependencies or manifest/lockfile changes. If none exists, use a small
`.tigerkit/prototypes/<slug>/index.html`, `styles.css`, and `app.js`.

Hold content, data, and interaction state constant while comparing only 2–3
decision-relevant concepts. Default to side-by-side 2–3 columns wide and stacked
narrow. Use an explicit A/B or A/B/C toggle only when simultaneous rendering
harms the concept or minimum legibility. Stop at A/B if a third adds no
independent value; create no prototype when repository evidence resolves the
decision.

Verify web output through `tk-browser-verify` Guard mode, including actual
interaction, run URL/command, and success-criteria screenshots. Check both wide
and narrow only when the hypothesis concerns responsiveness/layout. Clean only
run-owned tracked harnesses and temporary servers; preserve existing routes,
dependencies, and production source.

Do not commit by default. Do not invest in production abstractions/error
handling, call output production-ready, auto-promote it, or invoke another user
skill.

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
boundary, and unverified scope. Any missing item or failed execution prevents
`Complete`; use `Fail | Blocked | Unverifiable`.

## Contract

Record status once. Lead with `## Confirmed`, then
`## Production implication`, `## Tested`, `## Variants or harness`, and
`## Still fake`; omit empty sections. Confirmed owns evidence-backed
conclusions, Production implication the discard/iterate/next decision, Tested
command results, Variants or harness the alternatives/path/run URL and final
`kept | removed` state, and Still fake the fake/real and unverified scope.
Keep command mechanics after the decision.

When more than one criterion or variant is compared, render `## Confirmed` as
a compact `Criterion | A | B [| C] | Conclusion | Evidence` table. Use a
sentence when only one user-relevant row exists. Record whether
content/data/state stayed equal. Use `not observed` for unseen differences and
`unverifiable` for missing evidence. Do not promote unaudited aesthetic
preference into a conclusion.
Summarize comparison results and selection rationale in two to five bullets or
option rows. For eight or more observations, show the top five to seven and
cite the prototype or evidence path that owns the remainder. These are budgets,
not quotas.

### 🔴 HARD GATE · actionable user output

Treat the skill's canonical output contract as the schema and this gate as its presentation layer. Never remove or reorder required headings, tables, receipt keys, IDs, status tokens, result budgets, approval or safety boundaries, host-required progress notices, or response-language rules. Apply the response-language rules to every free-form clause and prose receipt value; retain another language only for canonical tokens, code identifiers, commands, paths, or exact quoted or source literals. Ordinary workflow jargon is prose, not a code identifier: translate it unless changing the token would make it incorrect.

In the first available free-form prose slot, lead with the answer, outcome, or action instead of a preamble. For multi-step user work, use the fewest bounded numbered steps. For continuing work, restate current state and the next transition without duplicating a plan or receipt. Make completed behavior visible. State errors as the observed failure, an evidence-backed cause when known, and a concrete recovery; never manufacture a cause.

Suppress tangents, ceremonial openers, repeated recaps, and closing pleasantries. When a required schema field repeats a result already stated, keep the field but make its value referential or minimal instead of recapping the result. When work remains, end with exactly one concrete next action owned by the user or workflow; when work is complete, stop without inventing one. Use a concrete time estimate only when evidence supports it and it helps the person executing the step.

When this gate conflicts with the canonical output contract or the host harness, preserve the higher-priority contract and apply the same shape inside its first prose value or slot. Do not label the user, mention this gate, expose a persistent mode, or require a runtime reference outside this skill.

### 🔴 HARD GATE · response language

Before any user-facing progress, question, summary, or receipt, resolve the response language from the latest explicit user language instruction; otherwise use the current user message's language. Write every free-form user-facing sentence and every prose receipt value in that resolved language, and do not switch to English because sources, skill bodies, tools, or code are English. Keep canonical headings, receipt keys, status tokens, IDs, commands, paths, code, and exact quoted or source literals byte-stable; explain them in the resolved language around the preserved token. Before returning, scan all free-form user-facing prose and rewrite any sentence that drifts from the resolved language.

## User decision questions

When a user-owned decision blocks progress, ask one self-contained `Question`
before any `Recommendation`. Show only decision-relevant evidence, two or three
mutually exclusive options with material tradeoffs, and exactly one label
ending `(Recommended)` or `(추천)`.

Use native structured input when exposed: Claude Code `AskUserQuestion`, Codex
`request_user_input`, or Hermes Agent `clarify`. Plain text is allowed only
when none is exposed. A failed or rejected call is not absence; preserve
`Pending | Blocked`. This changes presentation, not authority or stop gates.

## DO NOT / ANTI-PATTERNS

- Do not call a prototype production-ready or auto-promote/commit it.
- Do not report fake integration as real or claim success without run evidence.
- Do not add color-only variants, dependencies, manifest/lockfile edits,
  unnecessary production abstraction, or a valueless third option.
