---
name: tk-prototype
description: "[user/auto] 비교로 불확실성을 줄일 수 있을 때 disposable UI 또는 logic prototype을 만들고 실행한다. production implementation이나 대화형 아이디어 탐색에는 적용하지 않는다."
disable-model-invocation: false
argument-hint: "<idea, screenshot, spec, ticket, code, or design reference>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Comparison Prototype

Apply to explicit `invocation` or executable `disposable` comparison/`harness` requests.
Do not auto-apply to `production implementation` or conversational exploration.

Accept a `prompt`, idea, screenshot, `spec`, `ticket`, code, or design reference as input.
Write under `.tigerkit/prototypes/<slug>/` unless a temporary `route`/`harness` is more
useful. Create parent directories only when needed, replace atomically when possible, and
do not automatically archive or edit `.gitignore`. Warn if the `scratch` path is tracked.

## Workflow

1. `hypothesis/success criteria`: Derive measurable criteria from the idea, reference,
   and verification question.
2. `temporary path/boundary`: Inspect repository preflight and select the existing
   toolchain/UI stack/component/token, temporary path, artifact ownership, and
   `fake | real` integration boundary.
3. `variants/harness`: Create 2–3 `variant`s or a `harness` using realistic example I/O.
4. `run`: Execute the selected `variant`/`harness` and capture actual output or screenshots
   and command results.

Record each run under `## Tested` with the following receipt fields. Do not summarize the
command; record the exact executed values.

```text
Command: <exact command and arguments>
CWD: <absolute worktree or route path>
Exit code: <integer>
Output: <bounded summary or absolute output path>
Artifact: <absolute path | none>; ownership: run-owned | pre-existing
Screenshot: <absolute path | N/A>; actual inspection: yes | no | N/A
```

5. `compare`: Map evidence to criteria and summarize verified differences, unverified
   items, and the next decision. If the parent contract records `PR evidence: required`,
   retain the run-owned absolute `Screenshot: <path>` and actual image inspection under
   `## Tested`, and expose a bounded handoff containing `evidence_required: true`, the
   criterion, evidence directory, and producer `tk-prototype`.
6. `terminal summary`: When applicable, return `## Confirmed`, `## Production implication`,
   `## Tested`, `## Variants or harness`, and `## Still fake`.
   Do not add a provenance/status block.

For unresolved UI comparisons, create 2–3 switchable, genuinely different rendered
alternatives. Do not change only colors; vary information architecture, flow, hierarchy,
navigation, or feedback. For logic, prefer a small pure harness using example input/output
and a minimal adapter.

For a web prototype, inspect the repository's run command, installed UI stack, components,
and design tokens. Reuse a safe isolated route/harness without adding dependencies or
changing manifest/lockfiles. If none exists, use a small
`.tigerkit/prototypes/<slug>/index.html`, `styles.css`, and `app.js`.

Compare 2–3 decision-relevant concepts while keeping content, data, and interaction state
identical. Default to 2–3 side-by-side columns on wide screens and stacked on narrow
screens. Use an explicit A/B or A/B/C toggle only when simultaneous rendering would harm
the concept or minimum legibility. Stop at A/B when a third option adds no independent
value. Do not create a prototype when repository evidence already resolves the decision.

Verify web output through `tk-browser-verify` Guard mode, including actual interaction,
the `run URL`/`command`, and `success-criteria` screenshots. If a development server is
required, `handoff` the exact `command`/`cwd`/target URL/`auth mode`/`readiness` condition;
`tk-browser-verify` owns server start, wait, and shutdown. Check both wide and narrow only
when the `hypothesis` concerns responsiveness/layout. Clean up only run-owned tracked
`harness` files; preserve any `existing route`, `dependency`, and `production source`.

Do not commit by default. Do not invest in production abstractions/error handling, call
the output production-ready, auto-promote it, or invoke another user skill.

For a PR evidence handoff, expose the screenshot path, run-owned evidence directory,
criterion, and actual image inspection. This proves the prototype comparison, not an
official runtime verdict.

## Failure Paths

Record pre-existing temporary paths and run-created files before writing.

| Condition | First action | If it still fails |
|---|---|---|
| interrupted/partial write | Clean up only incomplete artifacts proven to be run-owned | `Fail`; report the unsafe cleanup path and restart condition |
| server/harness failure | Preserve the command, exit state, output, and fake/real boundary | `Fail`; do not expand into production/dependency scope |
| Execution succeeds but output/screenshot evidence is unavailable | Retry capture once within the same boundary | `Unverifiable`; do not claim success/Complete |
| ownership/state conflict with existing artifact | Preserve the existing path and record evidence | `Blocked`; choose another path before writing |
| cleanup failure | Re-identify only run-owned resources and report the outcome | `Fail | Unverifiable`; preserve existing routes/processes |
| Scope expands to production/promotion/commit | Stop the prototype and separate it into another implementation request | `Blocked`; do not auto-promote |

## 🔴 CHECKPOINT · 🛑 STOP · Execution Boundary

Before execution, confirm the temporary path, fake/real data, and verification question.
If environment or production-scope expansion occurs, stop at `Blocked | Unverifiable`.

Before reporting, reconcile the command, actual output/screenshot, fake/real boundary, and
unverified scope. If any are missing or execution failed, the result cannot be `Complete`.
Use `Fail | Blocked | Unverifiable`.

## Contract

Record decision-relevant status only once in its owning section. Start with `## Confirmed`,
followed by `## Production implication`, `## Tested`, `## Variants or harness`, and
`## Still fake`, omitting empty sections. `Confirmed` owns evidence-backed conclusions;
`Production implication` owns discard/iterate/next decision; `Tested` owns command results;
`Variants or harness` owns alternatives/paths/run URLs and final `kept | removed` state;
and `Still fake` owns fake/real and unverified scope. Place command mechanics after the
decision.

When comparing multiple criteria or variants, render `## Confirmed` as a concise
`Criterion | A | B [| C] | Conclusion | Evidence` table. Use a sentence when there is only
one user-relevant row. Record whether content/data/state remained identical. Use
`not observed` for differences that were not observed and `unverifiable` when evidence is
absent. Do not elevate unaudited aesthetic preferences into conclusions. Summarize the
result and selection rationale in 2–5 bullets or option rows. If there are 8 or more
observations, show the top 5–7 and cite the prototype or evidence path that owns the rest.
This is a budget, not a quota.

## Prohibited Patterns

- Do not call a prototype production-ready or auto-promote/commit it.
- Do not report fake integration as real or claim success without run evidence.
- Do not add color-only variants, dependencies, manifest/lockfile edits, unnecessary
  production abstractions, or a third option with no value.
