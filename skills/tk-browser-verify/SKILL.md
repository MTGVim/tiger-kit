---
name: tk-browser-verify
description: "[user/auto] 승인된 browser-visible acceptance criteria를 headless browser에서 검증합니다. 명시적 real-page verification 또는 정확한 parent verifier handoff에 사용하며 passive web research, generic design critique, implementation, screenshot-only request에는 사용하지 않습니다."
disable-model-invocation: false
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Browser Verification

Verify only `browser-visible` acceptance criteria that require runtime evidence.
Explicit invocation provides the criteria directly. Nested execution uses the target, scenario, authentication, and evidence plan already defined by a parent task such as a Ready `seed.md`, `tk-pr-respond`,
`tk-pr-sweep`, or `tk-prototype`.

This is a read-only acceptance verifier. Do not modify product/test/configuration source, Git commits, or remote state.
Do not create a Markdown lifecycle ledger. For nested execution, return only compact evidence to the parent task.

## Headless Prerequisites

All required scenarios must be executable headlessly. Use this priority order:

1. no authentication required
2. reuse an existing safe, verifiable, run-owned authenticated session/profile
3. temporarily inject user-supplied short-lived token/session material through a repository/application-supported header, cookie, or storage bootstrap
4. use username/password only for fully non-interactive login without OTP, MFA, SSO, CAPTCHA, passkey, or device approval

Do not guess the authentication injection method. Tie it to repository/application evidence or a user-specified method and
verify the resulting authenticated state.

Do not store usernames, passwords, tokens, OTPs, cookies, session values, recovery codes, or sensitive identities in
the conversation, `.tigerkit/*.md`, prompts, logs, summaries, or child receipts.
Record only non-sensitive facts such as `auth mode: token-headless` or `authenticated state established`.

If safe headless authentication cannot be established, do not fall back to a visible browser; return `Unverifiable`.

## 🔴 CHECKPOINT · 🛑 STOP · Verification readiness

Before browser or server execution, treat unresolved target, criterion, authentication, readiness, or evidence inputs as a hard stop: return `Blocked` for a user-owned decision or `Unverifiable` when safe verification cannot be established.

## Parent Handoff

When possible, the parent task provides:

- exact acceptance criterion
- target URL/environment
- headless requirement
- auth strategy and secret-free bootstrap method
- viewport/state
- development server command/cwd/readiness
- required screenshot evidence, AC-to-file mapping, and allowed capture-only layout adjustments
- exact verbatim strings or verified entry paths for UI `Content` criteria
- sensitive capture/redaction rule
- Pass condition
- automated regression evidence or explicit `N/A`/engineering-exception disposition owned by the parent

If the Ready Seed already owns this information, do not ask for the same decisions again.
If required values are missing but can be safely determined from repository evidence, fill them in.
Return only outcome-changing user-owned decisions to the parent owner.

## Execution

1. **Scope**: Fix the exact criteria, target/environment, current candidate, and approved interaction boundary. Browser evidence is an independent acceptance oracle; it never substitutes for appropriate automated regression protection.
2. **Preparation**: Read only the required references: [environment](references/environment.md), [behavior](references/behavior.md), [visual](references/visual.md), [accessibility](references/accessibility.md), [safety](references/safety.md).
3. **Evidence reuse**: Before starting a server/browser or rerunning an expensive scenario, reread supplied run-owned evidence and its current candidate/environment provenance. Reuse it only when it already proves the exact current criterion; stale, mismatched, incomplete, or uninspected evidence requires a justified fresh run. Do not rerun merely because a previous producer already returned evidence.
4. **Execution setup**: Without installing new dependencies, use a native, Playwright-compatible, MCP, or verified CDP path. Any new Chrome/Chromium process must prove effective `--headless=new`.
5. **Server**: If the parent requires a development server, this verifier owns starting the background process, readiness checks, and cleanup. For standalone execution, present multiple plausible commands and get the user's choice before starting; do not choose arbitrarily. Resolve the selected script and environment's host, port, and API target before launch, then prove project identity rather than accepting an open port alone. When the selected server is `react-scripts`/CRA, include `BROWSER=NONE` or the repository-documented equivalent to suppress auto-open. Manage PID/cwd/port/command and bounded logs as run evidence, and wait for a readiness signal rather than process exit.
6. **Verification**: Start from a known state and inspect the required interaction and final state. Capture and actually inspect at least one non-empty run-owned screenshot for every final state relevant to the decision.
7. **Decision**: Map each criterion to current evidence and assign `Pass | Fail | Blocked | Unverifiable`. When visual comparison is required, cover asset/content/geometry/typography/color/imagery/responsive/state axes. For UI `Content` criteria, require exact rendered strings or a verified entry path from the parent basis; if neither exists, do not infer the element from a paraphrase, code identifier, or enum and return `Unverifiable`.
8. **Cleanup**: Close only run-owned browser/server/resources and check for residue according to [session lifecycle](references/session-lifecycle.md).

## Evidence

Binary evidence may be stored in run-owned `.tigerkit/evidence/browser/<run-id>/`. A bounded `README.md` may map each
AC to its screenshot and disclose capture-only hidden/removed elements; it is an evidence index, not a lifecycle ledger.
Do not place other Markdown files there.
Do not move user fixtures. Use sensitive captures as evidence only after verifying redaction and absence of residue.

Limit nested results to:

- status
- Facts per criterion
- non-sensitive auth mode
- absolute evidence directory
- inspected screenshot path
- limitation
- cleanup fact
- `automated_regression: protected | N/A | exception | unknown` as supplied/verified parent disposition

When PR evidence is required, also return `evidence_required: true`, the criterion, and producer `tk-browser-verify`; do not upload it.

A standalone result starts with `## Verdict` and exact `Status: <token>`, then shows verified facts, required limitations, evidence paths, and the cleanup fact.
Never promote a result to `Pass` without required runtime evidence.

| Status | Meaning |
| --- | --- |
| `Pass` | Current inspected evidence covers every approved browser criterion |
| `Fail` | Current runtime evidence violates a criterion |
| `Blocked` | A user-owned safety or target decision is required before execution |
| `Unverifiable` | Required headless auth, environment, or evidence cannot be established |

Do not cause unauthorized payments, external communications, destructive mutations, production-data mutations, or account/permission changes.
