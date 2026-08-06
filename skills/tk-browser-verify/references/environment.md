# Environment comparison

Choose the simplest native, Playwright-compatible, MCP, or CDP route that
supports actual observation. Default to owned Chrome/Chromium whose effective
process arguments prove exact `--headless=new`. Record browser/version, OS,
DPR, fonts, assets, and zoom. Provider defaults are not evidence.

## CDP attachment

Before a CDP provider, verify its debugging endpoint and the actual browser
process on that port. If launching directly, use the browser binary, an
isolated temporary `user-data-dir`, and a verified remote-debugging port.

Confirm whether the provider uses a fixed port. Starting another browser on a
different port does not prove provider attachment. If auto-launch cannot
inject/prove `--headless=new`, attach to a directly launched verified endpoint.
When a user browser occupies the port, do not fall back headed or alter its
profile/login state; preserve the attached-session boundary.

## Screenshot paths

Choose screenshot `filePath` relative to the browser tool's workspace root and
resolve the run ledger to an absolute directory for the user-facing result. If
external scratch paths are rejected, save under the repo/workspace temporarily,
move as required, and leave no residue. Inline capture is enough for a
single-use close-up when supported.

Every Guard and Verdict run records `Evidence directory: <absolute path>` and
at least one non-empty `Screenshot: <path>` after actual image inspection. If
the absolute directory cannot be resolved, return `Unverifiable` and emit
`Evidence directory: unavailable`.

## Server auto-open

Before starting a verification server, inspect runner auto-open behavior and
its suppression. For runners that support it:

```bash
BROWSER=none yarn start
```

Do not use `BROWSER=none && yarn start` as an example of exporting the variable
to a child. Otherwise use a verified flag/configuration. If suppression is
impossible, continue but close only tabs created by this run and report it.

## Server startup and readiness

When this run starts a long-running development or verification server, start it
as a run-owned background process rather than waiting for command exit. Record
the exact PID, cwd, command, port, and bounded log path in the run-owned
evidence. Tail startup output while polling the repository's concrete HTTP,
CDP, or port readiness signal at a bounded interval and timeout. A dev server
continuing to emit logs is not itself a failure or a readiness condition.

After readiness, continue to browser verification. On timeout or process exit,
preserve the last bounded log lines and return `Fail | Unverifiable`; never
guess readiness from a fixed sleep and never kill a process not proven owned by
this run.

## Current verification target

When a server already listens, inspect process cwd, command, ownership,
auto-open suppression, and asset watcher. Terminate/restart a server without
suppression only when owned by this run or explicitly approved; report opened
tabs. Preserve user and other-run processes.

Reuse an existing server only when all are true:

1. process cwd exactly matches the target worktree; preserve other-worktree
   servers and use a separate port or wait;
2. a prebuilt-asset repository has process evidence for a composite server plus
   asset-watch command;
3. a response/bundle contains a current-worktree-only string or the changed
   render is measured. A temporary marker must use
   [visual](visual.md) instrumented/residue rules.

If any gate is unknown, do not reuse. Start safely on a separate port with
auto-open suppression and asset watch, warning about possible new tabs.

For prebuilt CSS/assets, verify regeneration or watch activity after the last
source edit. If a new style appears ignored or inherited, recheck asset
generation, hard reload, and serving version before diagnosing component code.

Verdict `## Evidence` records `Working tree`, `Server process/cwd`,
`Asset pipeline`, and `Serving version proof`. cwd alone is not current-source
proof.

## Interactive auth

Use headed mode only when the user must directly complete credentials, OTP,
2FA, passkey, CAPTCHA, or device approval. Login uses a user-local persistent
profile outside the repository. Never capture login screens or output/copy
profile paths, cookies, tokens, or secrets.

After login, close headed Chrome, prove lock release, and relaunch the same
binary and profile with `--headless=new`. Verify arguments and authenticated
target state before product evidence. If handoff fails, return
`Unverifiable`. Visible requests, headless failure, blank pages, timeout, or
debugging convenience are not auth exceptions.

Compare only named environments, viewports, and flags. Distinguish product
differences from access, data, and infrastructure. Auth/access blockage is a
captured and inspected `Unverifiable` final state in Verdict; Guard reports why
it cannot proceed.

User-facing progress and receipt prose follows the user's language.
