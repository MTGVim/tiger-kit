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

Apply only when real browser evidence is required. Explicit invocation selects `Verdict`; a direct answer to this run's pending runtime-identity question may resume it in the same conversation.

## Modes

Choose before any browser or verification-server call.

- **Guard** — disposable HTML, prototypes, exploratory UI checks. Run only requested trusted interactions, capture and inspect at least one run-owned screenshot, record minimal evidence, clean owned resources. Do not create a responsive matrix or official verdict.
- **Verdict** — explicit invocation, persistent user-visible changes, or official runtime verdict. Verify all criteria; return `Pass | Fail | Blocked | Unverifiable`.

Consume an active `tk-drive` browser profile without reopening product decisions. Re-request an `intentionally omitted` runtime identity once, keep it ephemeral, and return material strategy drift to the parent.

## Progress

Standalone runs emit one compact line at scope/server/browser/verdict
boundaries, e.g. `🚗 browser-verify · server`, `⏳ browser-verify · 대기`,
or `🙋 browser-verify · 응답 필요`; omit `tk-`. A parent owns
`parent > browser-verify`. Use `🙋` for user runtime input or approval and `⏳`
for server/remote/re-review wait. Preserve terminal `Status: <token>` as the
only final outcome marker. Suppress raw logs/receipts; keep paths and bounded
findings in the evidence artifact.

## Workflow

1. **Scope** — choose Guard/Verdict, target, criteria, safe interaction boundary. For local apps, omitted URL/launch command is discovery, not a user decision: inspect repository scripts, docs, and listening processes; proceed only with one worktree-bound target.
2. **Preflight** — load applicable references only: [UI verification](references/ui-verification.md), [design](references/design.md), [accessibility](references/accessibility.md), [visual](references/visual.md), [behavior](references/behavior.md), [safety](references/safety.md).
3. **Launch** — prove browser, effective arguments, profile ownership, and current-worktree serving source. An unnamed provider is not automatically `Unverifiable`; use the first available native, Playwright-compatible, MCP, or verified CDP route without installing dependencies. If starting a long-running verification server, launch it as a run-owned background process, record PID/cwd/port/command/log path, tail only bounded startup output, and poll a concrete readiness signal with a bounded timeout; never wait for the server process to exit. Continue after readiness, and return `Fail | Unverifiable` with the log path and last bounded lines when startup fails. Return `Unverifiable` only if none can capture and inspect required evidence.
4. **Run** — start from known state, perform safe interactions, inspect required network/final state, capture screenshots, inspect actual images.
5. **Verdict** — bind each criterion to evidence; classify failures `change-related | pre-existing | environment | unverifiable`.
6. **Cleanup** — close only run-owned resources; verify required capture residue.

Follow [session lifecycle](references/session-lifecycle.md) for browser ownership and [environment](references/environment.md) for serving-source and launch evidence.

## Critical pitfalls

### Chrome launch

New Chrome/Chromium must prove exact effective argument `--headless=new` before the first browser call. Tool names, `headless: true`, and provider defaults are insufficient. If auto-launch cannot prove it, launch directly and attach through CDP; otherwise return `Unverifiable`.

Headed browser allowed only for user credential entry, OTP, 2FA, passkey, CAPTCHA, or device approval. After auth, close the owned headed browser and resume the same profile with verified headless launch before product evidence. Never expose profile contents, credentials, cookies, OTPs, or tokens.

### Evidence and captures

DOM, accessibility, network success, and visual similarity cannot replace a runtime screenshot plus actual image inspection. Every Guard/Verdict run needs one non-empty run-owned screenshot and inspection; otherwise `Unverifiable`. When parent records `PR evidence: required`, return a bounded handoff containing `evidence_required: true`, criterion, absolute evidence directory, inspected screenshot paths, and producer `tk-browser-verify`. Changed behavior requires transition and final-state evidence, not only a toast or local DOM change.

Before first persisted capture, create and resolve `.tigerkit/browser-verify/runs/<run-id>/` as run-owned ledger. When resolvable, record absolute `Evidence directory: /absolute/path/...` in terminal `## Evidence`. Move only proven run-owned files. Sensitive network, console, or auth-adjacent captures require verified redaction and no residue; otherwise `Unverifiable`. Never edit `.gitignore` or delete user-owned evidence.

The evidence directory must contain the non-empty screenshot before completed Guard or `Pass` Verdict. If unresolved, emit `Evidence directory: unavailable` and return `Unverifiable`; never use a relative path where absolute is required.

For required PR evidence, preserve absolute `Evidence directory`, `Screenshot`, criterion, and actual image inspection in the producer handoff. Only `Pass` Verdict may go to `tk-github-image-upload-to-pr`.

Never paste/store raw console, network/HAR, or transcript bodies when a path and compact finding suffice. Instrumented evidence must follow restoration/residue rules in [visual](references/visual.md).

On crash, connection loss, timeout, or unexpected route/tab change, discard partial verdict and retry once from the same verified initial state. If still incomplete, stop `Unverifiable`.

Never edit production code. Unsafe irreversible interaction without safe environment and explicit authority is `Unverifiable`.

## Result

| Status | Meaning |
| --- | --- |
| `Pass` | Every required criterion and runtime image check is verified |
| `Fail` | A runtime requirement violation is observed |
| `Blocked` | A pre-session user decision is required |
| `Unverifiable` | Safe environment, authority, or required evidence is unavailable |

With a design basis, use `## Alignment` only for the design decision. Use `## Verdict` for runtime result, with non-empty `## Verified`, optional `## Findings`, `## Evidence`, `## Unverified`, and `## Cleanup`. `## Evidence` includes `Evidence directory: <absolute path>`, at least one `Screenshot: <path>`, and actual image inspection. For multiple criteria, use `Criterion | Result | Evidence`; for one user-relevant row, use a sentence. Summarize two to seven scenarios; for more, show top five to seven and cite the ledger. No receipt heading or duplicate provenance.

### 🔴 HARD GATE · terminal user summary

Keep progress and internal procedure evidence out of terminal response. Begin with canonical result heading or sentence. No preamble, receipt heading, `Outcome:` label, duplicate status, or active-drive child summary. Put detailed provenance only in the owned ledger; read-only stays read-only.

### 🔴 HARD GATE · response language

When a user-facing result includes an absolute time, convert it to the user's local timezone and label the timezone; keep raw machine timestamps only in owned evidence. Progress is optional and nonterminal: standalone execution is silent by default; emit `🙋 response/approval needed` only when user action is required, `⏳ wait` only when external waiting is next, or `🚗 meaningful boundary` only for long-running work. Put one space after each marker, omit no-op rows, and keep terminal responses free of progress markers while preserving any required terminal `Status: <token>`.

Use latest explicit user language; otherwise current message language. Preserve canonical headings, status tokens, IDs, commands, paths, code, and quoted source literals exactly. Rewrite drifting free-form language before return.

## User decision questions

Ask one self-contained `Question` only for a material user-owned decision, followed by `Recommendation`, two or three mutually exclusive options, and exactly one `(Recommended)` or `(추천)`. Render directly in chat; do not call structured question/input tools. Remain `Pending | Blocked` until answered.
