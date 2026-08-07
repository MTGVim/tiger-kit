---
name: tk-browser-verify
description: "[user/auto] Verify approved browser-visible acceptance criteria in a headless browser. Use for explicit real-page verification or an exact parent verifier handoff; not for passive web research, generic design critique, implementation, or screenshot-only requests."
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Browser verification

Use only for browser-visible acceptance criteria that require runtime evidence.
Explicit invocation supplies the criteria directly; a nested Drive/Respond route
uses only the already-approved scenarios, target, auth plan, and limitations.

This is a read-only acceptance verifier. It never edits product/test/config
source, opens a visible browser, or creates a Markdown lifecycle ledger. A nested
run returns compact facts and evidence paths to the top-level owner's ledger.

## Headless prerequisite

Before product mutation, establish that every required scenario can run
headlessly. Use the first supported route:

1. no authentication is required;
2. reuse an already available safe, run-owned authenticated session/profile whose
   current headless state can be verified;
3. transiently inject short-lived user-supplied token/session material through a
   repository/application-supported mechanism such as a request header, cookie,
   or storage bootstrap;
4. use username/password only through a repository-supported fully
   non-interactive login with no OTP, MFA, SSO, CAPTCHA, passkey, or device
   approval.

Never guess an injection mechanism. Bind it to repository/application evidence or
an explicit user-provided method, then verify the resulting authenticated state.
If interactive authentication is required, request suitable short-lived material
through an available ephemeral secret-input channel. If safe headless
authentication still cannot be established, return `Unverifiable` before product
mutation; never open a visible-browser fallback.

Auth values are operational inputs only. Never echo or persist usernames,
passwords, tokens, OTPs, cookies, session values, recovery codes, sensitive
identity, secret-bearing commands, or raw auth/network captures in chat,
`.tigerkit/*.md`, prompts, logs, summaries, or child receipts. Record only facts
such as `auth mode: token-headless` and `authenticated state established`.

## Workflow

1. **Scope** — freeze exact criteria, target URL/environment, safe interaction
   boundary, current candidate identity, and parent approval facts. Do not broaden
   into generic visual critique or reopen settled product decisions.
2. **Prepare** — load only applicable references: [environment](references/environment.md),
   [behavior](references/behavior.md), [visual](references/visual.md),
   [accessibility](references/accessibility.md), and [safety](references/safety.md).
   Prove the auth prerequisite before any parent worker mutates product state.
3. **Launch** — use an available native, Playwright-compatible, MCP, or verified
   CDP route without installing dependencies. Every new Chrome/Chromium process
   must prove exact effective argument `--headless=new` before its first browser
   call; otherwise attach to a directly launched verified headless endpoint or
   return `Unverifiable`.
4. **Run** — prove current-worktree serving source, begin from known state, use
   trusted interactions, inspect required request/response and final state, and
   capture at least one non-empty run-owned screenshot of every decision-relevant
   final state. Actually inspect each cited image.
5. **Verdict** — bind each approved criterion to evidence and report `Pass`,
   `Fail`, `Blocked`, or `Unverifiable`. Classify observed failures as
   `change-related`, `pre-existing`, `environment`, or `unverifiable` only when
   the evidence supports that origin.
6. **Cleanup** — close only run-owned resources and verify capture/redaction
   residue using [session lifecycle](references/session-lifecycle.md).

Long-running verification servers run as owned background processes. Record
PID/cwd/port/command and a bounded log path, poll a concrete readiness signal with
a timeout, and continue after readiness instead of waiting for process exit.

## Evidence and result

Binary evidence may live in a run-owned `.tigerkit/evidence/browser/<run-id>/`
directory; no Markdown file belongs there. Move only proven run-owned captures,
never user fixtures. Sensitive capture is usable only after verified redaction
and residue absence; otherwise return `Unverifiable` and preserve no secret.

A nested result contains only status, per-criterion facts, non-sensitive auth
mode, absolute evidence directory, inspected screenshot paths, limitations, and
cleanup facts. When approved PR evidence is required, also return
`evidence_required: true`, its criterion, and producer `tk-browser-verify`; never
upload it.

A standalone result starts with `## Verdict`, includes `Status: <token>`,
`## Verified`, optional bounded findings/unverified facts, `## Evidence`, and
cleanup facts. `## Evidence` names the absolute evidence directory and every
inspected screenshot. Missing required runtime evidence is `Unverifiable`, never
`Pass`.

| Status | Meaning |
| --- | --- |
| `Pass` | Every approved browser criterion has current inspected evidence |
| `Fail` | Current runtime evidence violates an approved criterion |
| `Blocked` | A user-owned safety or target decision is required before the run |
| `Unverifiable` | Required headless auth, environment, or evidence cannot be established |

Never cause unauthorized payment, external communication, destructive change,
production-data mutation, or account/permission change. Never commit, publish, or
modify product source.
