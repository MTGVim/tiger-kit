---
name: tk-browser-verify
description: "[user/auto] Verify real-page UI accuracy or interaction in a browser, or resume this skill's pending runtime-identity request in the same conversation. Use Guard for disposable exploration and Verdict for explicit invocation or persistent user-visible changes. Do not apply to passive web research, document reading, URL extraction, or simple screenshot saving."
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Browser verification

Apply only when real browser evidence is needed. Explicit invocation selects
`Verdict`; a direct answer to this run's pending runtime-identity question may
resume it in the same conversation.

## Modes

Choose before any browser or verification-server call.

- **Guard** — disposable HTML, prototypes, and exploratory UI checks. Run only
  the requested trusted interaction, capture at least one run-owned screenshot,
  inspect the actual image, record minimal evidence, and clean owned resources.
  Do not manufacture a responsive matrix or official verdict.
- **Verdict** — explicit invocation, persistent user-visible source changes, or
  an official runtime verdict. Verify every required criterion and return
  `Pass | Fail | Blocked | Unverifiable`.

Consume an active `tk-drive` browser profile without reopening product
choices. Re-request an `intentionally omitted` runtime identity once, keep it
ephemeral, and return material strategy drift to the parent.

## Workflow

1. **Scope** — choose Guard/Verdict, target, success criteria, and safe
   interaction boundary. For a local-app request, an omitted URL or launch
   command is discovery work, not a user decision: inspect repository scripts,
   documentation, and listening processes, then proceed only with one
   worktree-bound target.
2. **Preflight** — load only applicable references: [UI verification](references/ui-verification.md),
   [design](references/design.md), [accessibility](references/accessibility.md),
   [visual](references/visual.md), [behavior](references/behavior.md), and
   [safety](references/safety.md).
3. **Launch** — prove the browser, effective arguments, profile ownership, and
   current-worktree serving source. An unnamed browser provider is not itself
   `Unverifiable`; use the first available native, Playwright-compatible, MCP,
   or verified CDP route without installing dependencies, and return
   `Unverifiable` only when none can capture and inspect the required evidence.
4. **Run** — navigate from a known state, perform safe interactions, inspect
   required network/final state, capture at least one screenshot, and inspect
   the actual image(s).
5. **Verdict** — bind each criterion to evidence and classify failures as
   `change-related | pre-existing | environment | unverifiable`.
6. **Cleanup** — close only run-owned browser resources and verify required
   capture residue.

Follow [session lifecycle](references/session-lifecycle.md) for browser
ownership and [environment](references/environment.md) for serving-source and
launch evidence.

## Critical pitfalls

### Chrome launch

A newly started Chrome/Chromium must prove the exact effective argument
`--headless=new` before the first browser call. Do not infer it from a tool name,
`headless: true`, or provider defaults. If an auto-launch route cannot prove the
argument, launch directly and attach through CDP; otherwise return
`Unverifiable`.

A headed browser is allowed only for user-completed credential entry, OTP,
2FA, passkey, CAPTCHA, or device approval. After authentication, close the
headed owned browser and resume the same profile with verified headless launch
before collecting product evidence. Never expose profile contents, credentials,
cookies, OTPs, or tokens.

### Evidence and captures

DOM, accessibility, network success, or visual similarity does not replace a
runtime screenshot plus actual image inspection. Every Guard and Verdict run
must leave at least one non-empty run-owned screenshot plus its actual image
inspection; missing capture or inspection makes the result `Unverifiable`.
When the parent contract records `PR evidence: required`, expose a bounded
handoff with `evidence_required: true`, its criterion, the absolute evidence
directory, inspected screenshot paths, and producer `tk-browser-verify`.
Changed behavior needs the
relevant transition and final-state evidence, not only a toast or local DOM
change.

Before the first persisted capture, create and resolve
`.tigerkit/browser-verify/runs/<run-id>/` as the run-owned ledger. Record its
absolute path as `Evidence directory: /absolute/path/...` in the terminal
`## Evidence` section whenever the path is resolvable. Move only
files proven to belong to this run. Sensitive network, console, or auth-adjacent
captures require verified redaction and residue absence; otherwise use
`Unverifiable`. Never edit `.gitignore` or delete user-owned evidence.

The evidence directory must contain the non-empty screenshot before a completed
Guard result or a `Pass` Verdict. If the directory cannot be resolved, emit
`Evidence directory: unavailable` and return `Unverifiable`; never substitute a
relative path when an absolute path is required.

When a parent request marks PR evidence as required, preserve the absolute
`Evidence directory`, `Screenshot`, criterion, and actual image inspection
as the producer handoff. Only a `Pass` Verdict may be handed to
`tk-github-image-upload-to-pr`.

Never paste or store raw console, network/HAR, or transcript bodies when a path
and compact finding are enough. Instrumented evidence is allowed only under the
restoration and residue rules in [visual](references/visual.md).

On crash, connection loss, timeout, or unexpected route/tab change, discard the
partial-flow verdict and retry once from the same verified initial state. Then
stop `Unverifiable` if evidence is still incomplete.

Do not edit production code. Unsafe irreversible interaction without a safe
environment and explicit authority is `Unverifiable`.

## Result

| Status | Meaning |
| --- | --- |
| `Pass` | Every required criterion and runtime image check is verified |
| `Fail` | A runtime requirement violation is observed |
| `Blocked` | A pre-session user decision is required |
| `Unverifiable` | Safe environment, authority, or required evidence is unavailable |

When a design basis exists, use `## Alignment` only for the design decision.
Use `## Verdict` for the runtime result, with non-empty `## Verified`, optional
`## Findings`, `## Evidence`, `## Unverified`, and `## Cleanup`. `## Evidence`
must include `Evidence directory: <absolute path>` and at least one
`Screenshot: <path>` plus the actual image inspection result. When several
criteria exist, use `Criterion | Result | Evidence`; use a sentence when only
one user-relevant row exists. Summarize two to seven verified scenarios; for
more, show the top five to seven and cite the ledger. Do not add a receipt
heading or duplicate provenance.

### 🔴 HARD GATE · terminal user summary

Keep progress and internal procedure evidence out of the terminal user response.
Begin with the canonical result heading or sentence. Emit no ceremonial
preamble, receipt heading, `Outcome:` label, duplicate status, or active-drive
child summary. Put detailed provenance only in this skill's owned ledger; a
read-only path remains read-only.

### 🔴 HARD GATE · response language

Use the latest explicit user language, otherwise the current message's language.
Preserve canonical headings, status tokens, IDs, commands, paths, code, and
quoted source literals exactly. Rewrite any free-form language drift before
returning.

## User decision questions

Ask one self-contained `Question` only for a material user-owned decision, then
show a `Recommendation`, two or three mutually exclusive options, and exactly
one `(Recommended)` or `(추천)` label. Render the question and options directly
in the chat response; do not call structured question or input tools. Preserve
`Pending | Blocked` until the user answers.
