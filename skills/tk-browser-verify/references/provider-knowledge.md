# Provider Integration Knowledge

Read only the selected provider's section. Registry capabilities are possible features, not a
runtime matrix. Confirm current version, host/platform, permissions and per-action semantics.
Installation and missing permissions belong to a bounded `tk-wizard` setup handoff; do not
install, enable unrestricted modes or open focus-changing settings during verification discovery.
Use the registry's canonical docs and supplied host guidance rather than remembered API names.

## Distillation provenance

For contract maintenance, use these reviewed sources (2026-09-30 through 2026-10-07), then refresh canonical docs
for the installed provider version. Keep TigerKit's existing headless/evidence ownership; adapt
independent postcondition checks and background/escalation boundaries. Omit upstream installers,
global-input examples and automatic runtime/permission expansion.

- Cua [independent-postcondition example](https://github.com/trycua/cua/blob/0f29c142d7fe3e05ea0ce276cee11b3a9725ba01/libs/cua-driver/examples/agent-sdks/native_driver.py),
  plus official background/platform and verification guides. The example's global desktop input
  is not an approved background adapter; retain only its uncertain-response verification behavior.
- Orca [version-matched guide loader](https://github.com/stablyai/orca/blob/f4068747ac96cb526c7233683fc1cd89cad5f289/skills/computer-use/SKILL.md)
  and official computer-use guide: adapt executable identity and fresh-window snapshot guards;
  omit automatic app opening/restarting and unapproved coordinate fallback.
- Provider registry URLs were reviewed as maintainer/official sources. Host-native support remains
  conditional on actual tool exposure; no native-host live verification is claimed by these docs.
- Cua macOS drag (2026-10-05): `trycua/cua` revision `61ec8ac1d80df191bccd7fc9e9275123a809b2f7`,
  `libs/cua-driver/rust/crates/platform-macos/src/tools/drag.rs` (implementation, schema and refusal
  tests), `libs/cua-driver/rust/Skills/cua-driver/MACOS.md`,
  `docs/content/docs/cua-driver/reference/mcp-tools/pointer.mdx` and commit rationale. Keep independent
  postconditions and exact authority; adapt the foreground-only exception; omit desktop-scope input
  and automatic escalation. Native tests were inspected, not rerun.
- Cua macOS launch (2026-10-02): `trycua/cua` revision `8d4e7a08618611453794035f7ff6187f99f0c1e9`,
  `libs/cua-driver/rust/Skills/cua-driver/MACOS.md`,
  `libs/cua-driver/rust/crates/platform-macos/src/tools/launch_app.rs` and
  `libs/cua-driver/rust/crates/cua-driver-e2e/tests/installed_app_launch_macos_test.rs`. Keep
  provider-owned launch and independent focus checks; adapt the user-supplied raw-executable wrapper
  case with exact identity and cleanup checks; omit activation workarounds. System-temp lookup and
  wrapper success are supplied incident evidence, not a universal upstream claim. Native tests were
  inspected, not rerun.

- Cua scroll/token/snapshot (2026-10-07): `trycua/cua` revision
  `5227ad637590a15976413b1a33f8693fac0e9a7e`, macOS `tools/scroll.rs`, `tools/mod.rs`
  and `tools/get_window_state.rs`, core `snapshot_store.rs` and `window_state_view.rs`.
  Keep independent postconditions and foreground authority; adapt explicit scroll refusal,
  token-owned process identity and optional scoped diff reads; omit global input, automatic
  escalation and cross-provider assumptions. Shared token/window-view tests were inspected,
  not rerun; macOS live delivery remains unverified here.

## Chrome DevTools MCP

Inspect configured launch/attach mode and effective headless setting. A managed pipe needs no
TCP endpoint; a dedicated persistent profile needs an isolation limitation. Network/console/DOM
and performance tools depend on the installed version and exposed tool inventory. Preserve the
browser environment reference's attach, ownership and authentication requirements.

## Playwright

Distinguish installed repository Playwright from MCP. Confirm headless option, browser binary,
context isolation, transport and actual network/console tools. An isolated profile is not proof
of a scenario-isolated context. Resolve selectors from fresh page evidence. Never download a
browser or npm package just to detect readiness.

## Browser CDP

An installed browser CLI or Puppeteer adapter must expose its current documented entry point;
use its version-matched help/repository guidance in addition to the protocol URL. Do not infer
one CLI's flags from another. A live CDP endpoint requires headless and run-ownership proof
before any browser call, and explicit attach selection after observed launch-boundary evidence.

### Installed Chrome CLI capture caveats

A supplied 2026-10-07 incident observed CLI `--screenshot` capturing a blank scrolled region,
a 20000px-tall capture hanging, and effective width clamped to 500px. These are environment-specific
observations, not universal Chrome/CDP limits; verify actual viewport and installed-version behavior.
Prefer bounded captures and a provider-supported region capture when available. Hiding preceding
content for a capture is allowed only as an explicitly recorded `capture_only_mutation`, with exact
source/state retained and the product view restored; it cannot prove unchanged geometry. Measurement
helpers can themselves increase document width: measure first, keep helpers contained, and remove
them before final overflow checks. Blank or truncated pixels never prove acceptance.

## BrowserSkill

The `bsk` CLI requires an extension/daemon and a selected Chrome/Edge profile. Current upstream
uses a visible agent window and can borrow a user tab. This is optional signed-in automation,
not eligible for TigerKit's headless-only browser acceptance. Never borrow a user profile or
start its extension connection as an automatic fallback. Report the mismatch and alternatives.

## BrowserMCP

Keep as historical/reference metadata, outside default recommendations. Recheck maintainer
activity and current docs before an explicit request; do not claim current readiness from the
reference entry or treat an extension connection as a headless provider.

## Cua Driver

Check binary, daemon, doctor warnings and actual driver permissions separately. A version string
alone does not prove desktop access. On macOS check Accessibility and Screen Recording; Windows
requires an interactive user session, and Linux paths depend on accessibility/display support.
Background is best effort. Prefer a fresh semantic token; window-scoped coordinates still need
current capture/scale and observed safe delivery. Off-Space SwiftUI/canvas and Wayland raw-key
limits may block a scenario. Never enable foreground delivery automatically. Verify independent
postconditions after uncertain responses rather than blindly replaying input.

### Semantic identity and snapshot reads

When the installed action schema permits it, a current `element_token` resolves its own
process/window identity; omit redundant `pid` only after matching that snapshot to the exact
candidate. An explicit conflicting `pid` or window ID stops input; do not let either identity
silently win. Unknown/stale tokens require a fresh read, not guessed identity. Snapshot reads
and coordinate actions retain their own required process/window fields.

For supported Cua `get_window_state`, start with a full read (no `since`), using one compact
tree representation when sufficient. In a stable same-process/window and query/node/depth
scope, optionally use `since:<snapshot_id>` against a known full base and coherent diff chain.
Check `since_status`, truncation and reindexing; consume the new snapshot ID and current
tokens, never reuse superseded tokens. Scope changes, stale/unknown bases, truncation,
uncertain chains or insufficient evidence require a full read with enough scope to observe
the criterion. Full means no diff base, not necessarily `full_output:true`. A diff can provide
independent current state evidence, but an empty diff or action success does not establish
the criterion; visual criteria still need inspected current pixels. Do not infer this
capability for other providers.

### macOS Electron/Chromium scroll

When current Cua evidence identifies macOS Electron/Chromium scroll as unsupported in
background, skip that attempt; an observed `background_unavailable` refusal ends identical
background retries. Reuse exact foreground authority or request it before escalation;
without it, leave the required scroll `Blocked`. A token does not bypass this delivery
restriction. Keep click/type/drag, other app surfaces and platforms under their own observed
action contracts; do not generalize this scroll exception.

### macOS drag

On macOS, Cua window-scoped pixel `drag` is foreground-only, not a best-effort
background action. Do not attempt background drag first: it is refused with
`background_unavailable` and sends nothing. When the gesture itself is required,
reuse exact existing foreground authority or request it before input; otherwise
return `Blocked`. Bind exact `window_id` and fresh capture coordinates, disclose
the temporary frontmost window and physical pointer movement, and verify fresh
state, focus and independent postconditions after the driver's attempted restoration.
For a value-change outcome, prefer a supported semantic action when equivalent;
macOS AX has no generic semantic drag. Keep other actions and platforms under
their own observed delivery contract; never substitute global desktop input.

### macOS launch

For native app launch, read the installed version's `launch_app` schema and bundled `MACOS.md`.
Use its documented `launch_app({bundle_id})` path; the reviewed macOS implementation guards
target self-activation and may return `self_activation_suppressed`. A true result supports the
guard outcome, not a universal guarantee: independently compare the prior frontmost app/focus
with fresh post-launch state. A false/missing field is not positive proof. Shell `open` in any
form, AppleScript activation and a self-activating repository command are not background launch
substitutes. Do not use them to bypass the selected provider's launch contract.

For a raw already-compiled candidate without a bundle, a run-owned `.app` wrapper may copy
(not symlink) that exact executable and use a distinct `CFBundleIdentifier` so an installed
release cannot win lookup. Preserve required resources, libraries, working directory and runtime
configuration; if relocation changes the candidate or requires an unsupported signing/setup
workaround, stop instead of claiming equivalence. Verify the registered identifier resolves to
this wrapper's exact path and candidate before `launch_app`, then bind returned process/window
to it. Registration alone does not prove lookup. If the platform ignores system temporary paths,
use a checked run-owned non-system-temp location such as repository `.tigerkit/tmp/`; an unresolved
registration is `Blocked`. Registration is temporary and run-owned, not an app installation or
replacement of an existing identifier. Unregister only this run's registration and delete its
wrapper during cleanup; never unregister or remove the installed release.

Other providers/platforms require their own current launch evidence; these macOS semantics
do not establish their compatibility.

## Orca Computer

Resolve the session's executable from the current upstream guide before any Orca command. Outside
an Orca terminal on Linux, bare `orca` may be the GNOME screen reader; do not run it to detect the
IDE. Load the resolved executable's version-matched `skills get computer-use` guide, then check
status, permissions and capabilities. Refresh app/window snapshots after state changes; indexes
belong to that snapshot. Semantic actions may be direct, while raw keyboard/coordinates or
window restoration may steal focus. Verify the actual path and seek exact escalation authority.

## Codex Native

Read the current official computer-use document and the actual host's advertised API. Expose
this provider only when native app access is enabled and callable. Browser-only capabilities
cannot verify native windows. Standalone Codex CLI, an app name or an installed SDK does not
prove built-in desktop access. Unknown/disabled delivery or permissions blocks the scenario.

## Claude Native

Read the official CLI guide and its linked Desktop guide for the actual host. Current CLI
eligibility differs from Desktop and non-interactive sessions. Per-app grants and tool exposure
must be observed. CLI computer use can hide other apps and lock desktop access for a session;
never advertise it as guaranteed background interaction. Follow host prompts and exact task
authorization; do not bypass app denials or assume Cowork/CLI/Desktop share every capability.

## Open Computer Use

Use the maintainer README and exposed tool schemas. Accessibility, routed/background input,
screen capture and global actions differ per OS. Keep it optional; prove fresh app/window identity
and actual delivery before choosing it for a background-only criterion.

## Munim Computer Use

Use the maintainer README and actual platform/tool schemas. Some Windows paths and Linux pointer
input can move the real pointer despite background-capable paths elsewhere. Signed-in browser
extension attachment is an independent trust boundary. Keep optional and avoid blanket background
or cross-platform capability claims.
