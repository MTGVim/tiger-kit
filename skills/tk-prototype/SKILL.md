---
name: tk-prototype
description: "[user/auto] 비교가 필요한 일회성 UI 또는 로직 prototype을 만들고 실행합니다. production 구현이나 대화형 아이디어 탐색에는 사용하지 않습니다."
disable-model-invocation: false
argument-hint: "<idea, screenshot, spec, ticket, code, or design reference>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Comparison Prototype

Accept a `prompt`, idea, screenshot, `spec`, `ticket`, code, or design reference as input.
Keep standalone artifacts under `.tigerkit/prototypes/<slug>/`. Before writing, prove
that Git effectively ignores `.tigerkit/` and no path under it is tracked. The effective
rule may come from per-directory, local-exclude, or user-level-exclude configuration.
Do not edit `.gitignore` or use an
external scratch fallback. A repository-native route/harness is allowed only when the
selected runtime requires it; record and clean up only run-owned files.

Before execution, use the host's structured question surface when the user must choose a
path, data boundary, verification question, or variant: Claude Code `AskUserQuestion`,
Codex `request_user_input`, or Hermes `clarify`. If unavailable, ask in plain chat.

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
   `## Tested`, and expose the same producer-neutral manifest consumed by publication:
   `evidence_required: true`, `evidence_kind: visual-change`, `verification_status: Pass`,
   the criterion, comparison, limitations, and an inspected artifact with role, absolute
   path, exact origin-free `display_route`, state/region, and viewport. Use the metadata
   returned by `tk-browser-verify`; do not derive it from a filename, raw URL, or producer
   identity. This proves the prototype comparison, not official product runtime acceptance.
6. `terminal summary`: Render the applicable sections under the output contract below;
   do not add a separate provenance/status block.

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

Verify web output through `tk-browser-verify`, including actual interaction,
the `run URL`/`command`, and `success-criteria` screenshots. If a development server is
required, `handoff` the exact `command`/`cwd`/target URL/`auth mode`/`readiness` condition;
`tk-browser-verify` owns server start, wait, and shutdown. Check both wide and narrow only
when the `hypothesis` concerns responsiveness/layout. Clean up only run-owned tracked
`harness` files; preserve any `existing route`, `dependency`, and `production source`.

## Failure Paths

Record pre-existing temporary paths and run-created files before writing.

| Condition | First action | If it still fails |
|---|---|---|
| interrupted/partial write | Clean up only incomplete artifacts proven to be run-owned | `Fail`; report the unsafe cleanup path and restart condition |
| server/harness failure | Preserve the command, exit state, output, and fake/real boundary | `Fail`; do not expand into production/dependency scope |
| Execution succeeds but output/screenshot evidence is unavailable | Retry capture once within the same boundary | `Unverifiable`; do not claim `Pass` |
| ownership/state conflict with existing artifact | Preserve the existing path and record evidence | `Blocked`; choose another path before writing |
| cleanup failure | Re-identify only run-owned resources and report the outcome | `Fail | Unverifiable`; preserve existing routes/processes |
| Scope expands to production/promotion/commit | Stop the prototype and separate it into another implementation request | `Blocked`; do not auto-promote |

## 🔴 CHECKPOINT · 🛑 STOP · Execution Boundary

Before execution, confirm the temporary path, fake/real data, and verification question.
If environment or production-scope expansion occurs, stop at `Blocked | Unverifiable`.

Before reporting, reconcile the command, actual output/screenshot, fake/real boundary, and
unverified scope. If any are missing or execution failed, the result cannot be `Pass`.
Use `Fail | Blocked | Unverifiable`.

## Contract

Record decision-relevant status only once in its owning section. Start with `## Confirmed`,
followed by `## Production implication`, `## Tested`, `## Variants or harness`, and
`## Still fake`, omitting empty sections. `Confirmed` owns evidence-backed conclusions;
`Production implication` owns discard/iterate/next decision; `Tested` owns command results;
`Variants or harness` owns alternatives/paths/run URLs and final `kept | removed` state;
and `Still fake` owns fake/real and unverified scope. Place command mechanics after the
decision.

Use exactly one terminal status: `Pass | Fail | Blocked | Unverifiable`.

When comparing multiple criteria or variants, render `## Confirmed` as a concise
`Criterion | A | B [| C] | Conclusion | Evidence` table. Use a sentence when there is only
one user-relevant row. Record whether content/data/state remained identical. Use
`not observed` for differences that were not observed and `unverifiable` when evidence is
absent. Do not elevate unaudited aesthetic preferences into conclusions. Summarize the
result and selection rationale in 2–5 bullets or option rows. If there are 8 or more
observations, show the top 5–7 and cite the prototype or evidence path that owns the rest.
This is a budget, not a quota.

## Prohibited Patterns

- Do not call a prototype production-ready, auto-promote/commit it, or invoke
  another user skill.
- Do not report fake integration as real or claim success without run evidence.
- Do not add color-only variants, dependencies, manifest/lockfile edits, unnecessary
  production abstractions, or a third option with no value.
