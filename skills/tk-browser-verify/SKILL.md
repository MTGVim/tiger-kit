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
- required screenshot evidence
- exact verbatim strings or verified entry paths for UI `Content` criteria
- sensitive capture/redaction rule
- Pass condition

If the Ready Seed already owns this information, do not ask for the same decisions again.
If required values are missing but can be safely determined from repository evidence, fill them in.
Return only outcome-changing user-owned decisions to the parent owner.

## Execution

1. **Scope**: Fix the exact criteria, target/environment, current candidate, and approved interaction boundary.
2. **Preparation**: Read only the required references: [environment](references/environment.md), [behavior](references/behavior.md), [visual](references/visual.md), [accessibility](references/accessibility.md), [safety](references/safety.md).
3. **Execution setup**: Without installing new dependencies, use a native, Playwright-compatible, MCP, or verified CDP path. Any new Chrome/Chromium process must prove effective `--headless=new`.
4. **Server**: If the parent requires a development server, this verifier owns starting the background process, readiness checks, and cleanup. For standalone execution, present multiple plausible commands and get the user's choice before starting; do not choose arbitrarily. When the selected server is `react-scripts`/CRA, include `BROWSER=NONE` or the repository-documented equivalent to suppress auto-open. Manage PID/cwd/port/command and bounded logs as run evidence, and wait for a readiness signal rather than process exit.
5. **Verification**: Start from a known state and inspect the required interaction and final state. Capture and actually inspect at least one non-empty run-owned screenshot for every final state relevant to the decision.
6. **Decision**: Map each criterion to current evidence and assign `Pass | Fail | Blocked | Unverifiable`. When visual comparison is required, cover asset/content/geometry/typography/color/imagery/responsive/state axes. For UI `Content` criteria, require exact rendered strings or a verified entry path from the parent basis; if neither exists, do not infer the element from a paraphrase, code identifier, or enum and return `Unverifiable`.
7. **Cleanup**: Close only run-owned browser/server/resources and check for residue according to [session lifecycle](references/session-lifecycle.md).

## Evidence

이진 근거는 run-owned `.tigerkit/evidence/browser/<run-id>/`에 둘 수 있으며 Markdown file은 두지 않습니다.
user fixture를 이동하지 않고, 민감한 capture는 verified redaction과 residue absence를 확인한 경우에만 evidence로 사용합니다.

중첩 결과는 다음 정도로 제한합니다.

- status
- criterion별 사실
- non-sensitive auth mode
- absolute evidence directory
- inspected screenshot path
- limitation
- cleanup fact

PR evidence가 필수이면 `evidence_required: true`, 해당 criterion, producer `tk-browser-verify`도 반환하되 upload하지 않습니다.

독립 실행 결과는 `## Verdict`와 정확한 `Status: <token>`으로 시작하고 verified facts, 필요한 limitation, evidence path, cleanup fact를 보여줍니다.
필수 런타임 evidence가 없으면 절대 `Pass`로 올리지 않습니다.

| 상태 | 의미 |
| --- | --- |
| `Pass` | 승인된 모든 브라우저 기준에 현재 inspected evidence가 있음 |
| `Fail` | 현재 런타임 evidence가 criterion을 위반함 |
| `Blocked` | 실행 전에 user-owned safety/target decision이 필요함 |
| `Unverifiable` | 필수 headless auth, environment, evidence를 확립할 수 없음 |

Do not cause unauthorized payments, external communications, destructive mutations, production-data mutations, or account/permission changes.
