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

Record status once. `## Tested` owns commands, results, and evidence;
`## Variants or harness` the alternatives; `## Confirmed` evidence-backed
conclusions; `## Still fake` fake/real and unverified/unresolved scope;
`## Production implication` discard/iterate/next decision.

For every criterion, `## Confirmed` records one
`criterion | A | B [| C] | conclusion | Tested evidence reference` comparison
and whether content/data/state stayed equal. Use `not observed` for unseen
differences and `unverifiable` for missing evidence. Do not promote unaudited
aesthetic preference into a conclusion.

User-facing progress and receipt prose follows the user's language while
canonical headings and status tokens remain unchanged.

## DO NOT / ANTI-PATTERNS

- Do not call a prototype production-ready or auto-promote/commit it.
- Do not report fake integration as real or claim success without run evidence.
- Do not add color-only variants, dependencies, manifest/lockfile edits,
  unnecessary production abstraction, or a valueless third option.
