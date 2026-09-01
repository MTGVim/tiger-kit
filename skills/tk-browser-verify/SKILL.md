---
name: tk-browser-verify
description: "[user/auto] 로컬 앱·prototype의 실제 화면, interaction, responsive·visual 일치, render 결함을 headless browser로 검증하고 근거를 반환합니다. 구현, 일반 웹 조사, visual 대조나 결함 확인이 없는 단순 이미지 저장에는 사용하지 않습니다."
disable-model-invocation: false
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Browser Verification

Verify only `browser-visible` acceptance criteria that require runtime evidence.
Explicit invocation provides the criteria directly. Nested execution uses the target,
scenario, authentication, and evidence plan already defined by its parent.

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

Before the first browser call or server execution, treat unresolved target, criterion,
authentication, readiness, evidence path, effective headless process arguments, endpoint,
or run ownership as a hard stop. Return `Blocked` for a user-owned decision or
`Unverifiable` when safe verification cannot be established. A provider or MCP tool name
never proves these prerequisites.

## Parent Handoff

Use parent-provided values when available:

- exact criterion, target/environment, and current candidate;
- headless authentication and secret-free bootstrap method;
- viewport, initial state, and server command/cwd/readiness;
- screenshot mapping and allowed capture-only adjustments;
- exact UI strings or verified entry paths;
- exact visual reference and comparable viewport/DPR/zoom/font state when a design node,
  mockup, baseline screenshot, or as-is/to-be comparison exists;
- redaction rule, `Pass` condition, and automated-regression disposition.

If the Ready Seed already owns this information, do not ask for the same decisions again.
If required values are missing but can be safely determined from repository evidence, fill them in.
Return only outcome-changing user-owned decisions to the parent owner.

## Execution

1. **Scope**: Fix the exact criteria, target/environment, current candidate, and approved interaction boundary. Browser evidence is an independent acceptance oracle; it never substitutes for appropriate automated regression protection.
2. **Preparation**: Read only references whose branch applies:
   - [environment](references/environment.md) when launching/attaching a browser, establishing authentication, or owning a development server;
   - [behavior](references/behavior.md) for trusted interaction, network effects, dialogs, motion, or field clearing;
   - [visual](references/visual.md) whenever a design node, mockup, baseline screenshot,
     as-is/to-be comparison, visual/fidelity/responsive criterion, or multi-capture evidence exists;
   - [accessibility](references/accessibility.md) only for form, dialog, navigation, keyboard, shortcut, or focus criteria;
   - [safety](references/safety.md) when the scenario can create external/data/account effects or sensitive captures;
   - [session lifecycle](references/session-lifecycle.md) when creating, attaching, reusing, or cleaning browser/server/evidence resources.
3. **Evidence reuse**: Before starting a server/browser or rerunning an expensive scenario, reread supplied run-owned evidence and its current candidate/environment provenance. Reuse it only when it already proves the exact current criterion; stale, mismatched, incomplete, or uninspected evidence requires a justified fresh run. Do not rerun merely because a previous producer already returned evidence.
4. **Execution setup**: Without installing new dependencies, use a native, Playwright-compatible, MCP, or verified CDP path. Before any browser call, prove the live target process, effective `--headless=new`, endpoint, and isolated profile ownership for both launch and attach paths. If an attached process is headed, belongs to another run or the user, or cannot be proven, make no browser call and return `Unverifiable`.
5. **Server**: If the parent requires a development server, this verifier owns starting the background process, readiness checks, and cleanup. For standalone execution, present multiple plausible commands and get the user's choice before starting; do not choose arbitrarily. Resolve the selected script and environment's host, port, and API target before launch, then prove project identity rather than accepting an open port alone. When the selected server is `react-scripts`/CRA, include `BROWSER=NONE` or the repository-documented equivalent to suppress auto-open. Manage PID/cwd/port/command and bounded logs as run evidence, and wait for a readiness signal rather than process exit.
6. **Verification**: Start from a known state and inspect the required interaction and final state. Capture and actually inspect at least one non-empty run-owned screenshot for every final state relevant to the decision. Before citing a screenshot for an AC, verify that the image visibly contains that exact criterion and its necessary context; a non-empty capture with the target outside the captured viewport or scroll position cannot support that AC.
7. **Decision**: Map each criterion to current evidence and assign `Pass | Fail | Blocked | Unverifiable`. When a visual reference exists, record `Pass | Fail | Unverifiable` for asset/content/geometry/typography/color/imagery/responsive/state, include reference/candidate/delta measurements for geometry and typography, and report every measured mismatch. An unchecked axis or missing required measurement blocks aggregate `Pass`. For UI `Content` criteria, require exact rendered strings or a verified entry path from the parent basis; if neither exists, do not infer the element from a paraphrase, code identifier, or enum and return `Unverifiable`.
8. **Cleanup**: Close only run-owned browser/server/resources and check for residue according to [session lifecycle](references/session-lifecycle.md).

## Evidence

Before the first write under `.tigerkit/evidence/`, verify that
`git ls-files -- .tigerkit/` returns no tracked path and
`git check-ignore -q -- .tigerkit/` succeeds. Record only the matching source class and
pattern from `git check-ignore -v`, redacting an absolute user-level path. If the checks
fail, do not write, edit `.gitignore`, or use an external fallback; return `Unverifiable`.

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
