---
name: tk-browser-verify
description: "[user/auto] Verify real-page UI accuracy or interaction in a browser. Use Guard mode for disposable HTML, prototypes, layout, hover, and form exploration unless explicitly invoked; explicit invocation overrides Guard and selects Verdict, as do persistent user-visible source changes and official runtime verdict requests. Do not auto-apply to passive web research, document reading, URL extraction, or simple screenshot saving. This skill does not own source mutation or replace sufficient non-browser static verification."
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Browser verification

Apply directly when browser evidence is needed to judge real-page UI accuracy
or interaction. Do not auto-apply to passive web research, document reading,
URL extraction, or simple screenshot saving. Explicit invocation always selects
Verdict mode.

## Mode selection

Before any browser tool or verification server call, choose one mode and apply
only the relevant items in [proactive UI verification](references/ui-verification.md).
Select [accessibility](references/accessibility.md) only for form, dialog,
navigation, keyboard, or focus scope. Run design-intent preflight only when an
actual Figma file, screenshot, or design specification is input; classify it
`same | different | unclear`. Without a design basis, alignment is `N/A`: do
not invent an `## Alignment` receipt.

- **Guard mode**: disposable HTML, prototypes, or exploration without a
  persistent user-visible source change or official verdict. Do not create a
  responsive matrix or terminal verdict; inspect a screenshot only when making
  a visual claim.
- **Verdict mode**: persistent user-visible UI source changes, explicit
  invocation, or an official verdict request. Apply the complete contract.

For a local disposable Guard target with no auth, external mutation, or
sensitive data, pass both hard gates and perform only:
`owned headless session → requested trusted interaction → required screenshot
and computed state → one normal-sensitivity ledger row → owned cleanup`.
Do not create network/HAR/console/video evidence, a responsive matrix, an
environment table, or a terminal verdict unless the observed state requires it.

Never use Guard mode to bypass a Verdict completion gate. Omit N/A receipt
sections in Guard mode and report only requested results and necessary evidence.

Choose the simplest browser-native, Playwright-compatible, MCP, or CDP route
that can observe the target. The default uses a disposable isolated profile;
reuse of an auth profile is optional only for the interactive-auth exception.

## 🔴 HARD GATE · Chrome `--headless=new`

Before the first browser-related tool call in either mode, freeze the launch
route. A newly started Chrome/Chromium defaults to an owned isolated profile,
and tool configuration or process argv must prove that actual launch arguments
contain the exact token `--headless=new`. Record binary, effective arguments,
profile path, and ownership as environment evidence.

Never infer the token from `headless`, `headless: true`, provider defaults, a
tool name, or this instruction. If an auto-launch tool cannot inject and prove
the exact argument, do not use it first. Start Chrome directly with
`--headless=new` and attach to its verified CDP endpoint. If neither route is
possible, do not open a headed browser: Verdict is `Unverifiable`, and Guard
reports why it cannot proceed.

A headed exception is allowed only when the user must directly complete
credential entry, OTP, 2FA/2-step verification, passkey, CAPTCHA, or device
approval. Record the auth barrier, direct-input need, and user approval before
launch. A visible/headed request, headless launch failure, blank screen,
timeout, provider convenience, or debugging is not an exception and cannot
trigger headed fallback.

Interactive login uses a user-local persistent profile outside the repository.
After the user authenticates, close the headed owned browser, verify profile
lock release, restart the same binary and `user-data-dir` with
`--headless=new`, recheck arguments, and only then verify the product. Do not
capture product evidence in the headed session. If the same-profile handoff is
not proven, stop `Unverifiable`. Never output, capture, copy, or commit profile
contents, credentials, OTPs, cookies, or tokens. When the user explicitly
requires Firefox or Safari, use its verified native headless mode; the
headed-first prohibition remains.

## Workflow

1. `mode/scope`: produce Guard/Verdict mode and a safe interaction boundary.
2. `preflight`: produce required decisions, applicable references, and design
   relation only when a design basis exists.
3. `environment`: prove browser binary, exact `--headless=new`, isolated
   profile, auth exception state, and that current-worktree source is served.
4. `run/evidence`: record target identity, safe initial state, navigation,
   interaction, network/final state, screenshots plus actual image inspection,
   and conditional keyboard/focus/semantic/instrumented evidence.
5. `verdict`: return `Pass | Fail | Blocked | Unverifiable` and unverified scope.
6. `receipt/cleanup`: report the result and clean up only run-owned resources.

Follow [session lifecycle](references/session-lifecycle.md) for every new
browser. Suppress first-run/login/sync UI when possible. Skip or close it
safely without logging in. Clean up only the browser/context/window created by
this run; preserve pre-existing user sessions.

Select only relevant references: [visual](references/visual.md),
[behavior](references/behavior.md), [environment](references/environment.md),
[design](references/design.md), [accessibility](references/accessibility.md),
and [safety](references/safety.md).

## CHECKPOINT / STOP

Immediately before a browser tool or verification server call, confirm mode,
launch configuration, exact `--headless=new` evidence, and safe interaction
scope. Without launch evidence, make no browser call and use the terminal-state
contract below.

### Stop before browser start

When stopping before session creation, do not print the future checklist or
empty evidence sections. For a design blocker, return `## Alignment` and one
choice question. Otherwise return terminal status, one-line cause, and the
input required to resume. Name only the actual blocker. If no resource was
created, cleanup is one sentence.

## 🔴 HARD GATE · capture ledger

Before the first capture in either mode, designate
`.tigerkit/browser-verify/runs/<run-id>/` as this run's only capture ledger and
record destinations for screenshots, traces, video, network/HAR, and console
dumps. Prefer directing tool output there initially.

If a tool forces output to tool temp, default downloads, or user scratch, move
only files proven to be owned by this run immediately after capture. User
screenshots/fixtures and pre-existing or other-run artifacts are input evidence
only; never move, rename, or delete them. Unknown ownership is `Blocked`.

For every inventory item record kind, original/ledger path, ownership, move
result, and:

- `Sensitivity: normal | sensitive`
- `Redaction: N/A | verified | failed | unverifiable`
- `Residue check: verified | unverifiable`

Inspect network/HAR/console and auth-adjacent captures for authorization,
cookies, tokens, credentials, secrets, and sensitive bodies. Use sensitive
captures only after verified redaction and original-path residue absence.
`failed | unverifiable` redaction or unverifiable residue makes the result
`Unverifiable`.

If the parent `.tigerkit/` is not ignored by version control, do not persist
unverified sensitive captures there. Redact in run-owned external temp and move
only a safe result, or stop `Unverifiable`. Never edit `.gitignore`.

Verify every ledger file exists and is non-empty, no run-owned capture remains
outside the ledger, and the receipt cites only ledger paths. Unknown move,
existence, redaction, or residue state is `Unverifiable`. Warn for normal
captures when `.tigerkit/` is not ignored.

## Verdict mode contract

Confirm target URL, environment, success criteria, and safe interactions, then
pass the Chrome gate. Use the headed auth exception only after approval, and
resume the same profile headlessly before verification.

When a design basis exists, run [design](references/design.md) intent preflight
before exploration. Decompose visible spacing across frame, container,
component, and child. If the instruction and design differ or are unclear,
describe both final outcomes, criteria, and evidence; ask one explicit choice
and stop `Blocked` before implementation or browser launch. Silence is not
agreement. Skip this paragraph when there is no design basis.

### Execution evidence and interruption

Preserve this order:
`design intent → decision if needed → environment → navigation → interaction →
transition → network → final state → screenshot → image inspection → verdict`.
DOM, accessibility tree, network success, or visual similarity never replaces
screenshot inspection.

| Status | Trigger | Required receipt |
|---|---|---|
| `Pass` | all criteria, required breakpoints, runtime screenshots, and image inspection verified | per-criterion `Verified` plus ledger evidence |
| `Fail` | runtime requirement violation observed | screenshot, reproduction, and `change-related \| pre-existing \| environment` classification |
| `Blocked` | a pre-session design decision is missing | `## Alignment` decision receipt; no screenshot |
| `Unverifiable` | safe authority/environment or required runtime evidence is unavailable | executed scope, missing evidence, cleanup |

On connection loss, crash, navigation timeout, or unexpected route/tab change,
discard partial-flow evidence. Retry once only after rechecking the same target,
environment, and safe initial state; otherwise Verdict is `Unverifiable` and
Guard reports incomplete scope. Always attempt owned cleanup.

Changed behavior needs transition, request/response, and final UI state
evidence. A toast or local DOM change alone is insufficient. Unsafe irreversible
actions without a safe environment and explicit authority are `Unverifiable`.

### Evidence retention and reporting

Keep only useful ledger evidence; create no empty files. Prefer run IDs like
`YYYYMMDD-HHmmss-<short-slug>`. Store verified nonsensitive facts in
`.tigerkit/browser-verify/env.md` or `screens/<screen>.md` only when needed.
Create parents lazily and replace atomically when possible. Do not auto-create
`login.local.md`; if explicitly requested, never print its content and prefer
mode `0600`. Do not inspect or migrate legacy global TigerKit state.

Do not edit production code or promote evidence into a rule/skill, except for
the bounded `instrumented` evidence class in [visual](references/visual.md),
which requires restoration and measured residue absence in Guard and Verdict.

When a design basis exists, `## Alignment` owns `Instruction`, `Design basis`,
`Spacing stack`, `Relation`, `Expected implementation`, `User decision`, and
alignment `Status: confirmed | pending | Blocked`; it is not runtime Verdict.
`## Verdict` owns the overall result, `## Verified` criteria, `## Findings`
deviations, `## Evidence` observations/captures, `## Unverified` omitted scope,
and `## Cleanup` owned-resource results. These sections are the receipt; do not
add `## Receipt` or duplicate facts. Omit empty Findings/Unverified/Cleanup.

User-facing progress and receipt prose follows the user's language while the
canonical headings, fields, and status tokens above remain unchanged.

## User decision questions

When this skill reaches a user-owned decision, ask exactly one question at a
time. Render `Question` before `Recommendation` and the proposals. Offer
two or three mutually exclusive proposals and state the material tradeoff of
each. Make `Question` self-contained: summarize the
evidence-derived context, decision impact, and unresolved axis in user-facing
language before asking. It must not require the user to decode raw `Evidence`.
Mark exactly one best recommendation by ending its label with a localized marker such as
`(Recommended)` or `(추천)`. A host-generated custom or Other choice does not
count as an authored proposal.

When the active question tool exposes
option previews, prototype cards, or equivalent rich choice surfaces and a concrete preview can clarify the
decision, use it proactively. Do not invent unsupported fields or use this
presentation rule to bypass existing prototype or phase boundaries.

If the current execution context exposes a native structured user-input tool,
the skill must call that tool. Plain-text questions are allowed only when no
such tool is exposed. A failed or rejected tool call is not tool absence: report
the failure and preserve the pending or blocked state instead of silently
downgrading to prose. Host examples:

- Claude Code: `AskUserQuestion`
- Codex: `request_user_input`
- Hermes Agent: `clarify`

This contract changes question presentation only. It does not grant new
decision authority or weaken any existing stop, approval, or phase boundary.

## DO NOT / ANTI-PATTERNS

- Do not call an auto-browser without launch configuration and exact
  `--headless=new` evidence, or use headed-first/fallback outside interactive
  auth.
- Do not continue product verification in the headed login session or resume
  through a different profile.
- Do not leave run captures outside the ledger or use sensitive captures
  without redaction and residue proof.
- Do not move user-provided or unknown-ownership artifacts.
- Do not reuse an existing server without current-worktree, asset-pipeline, and
  serving-version proof; never diagnose stale observations as code defects.
- Do not use instrumented evidence instead of cheap direct observation or
  complete without measured cleanup.
- Do not claim `pre-existing` without baseline reproduction or causal `Pass`
  without a negative control.
- Do not replace screenshot inspection with DOM, accessibility tree, network,
  unit-test, or build success.
- Do not perform real payment, deletion, or external sending without a safe
  environment and explicit authority.
- Do not replace relevant keyboard/focus/semantic evidence with screenshots or
  claim full WCAG compliance from a limited flow.
