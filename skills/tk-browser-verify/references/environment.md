# Headless environment

Choose the simplest native, Playwright-compatible, MCP, or CDP route that can
produce the approved evidence. Do not install a new browser dependency for one
run. Every new Chrome/Chromium process must prove exact effective
`--headless=new`, binary, PID/provider process ID, and isolated run-owned
`user-data-dir` before its first browser call.

For CDP, verify the live endpoint, actual process, port, and profile ownership.
A saved port, prior browser UUID, `DevToolsActivePort`, provider default, or tool
name is not evidence. Never attach to or alter an unknown/user-owned browser.

## Authentication

Reuse only an already available safe authenticated session that is owned by this
run and verified headless. Otherwise use transient material through the exact
repository/application-supported header, cookie, storage, session bootstrap, or
fully non-interactive login path. Verify the authenticated target state without
capturing secret values.

An interactive login, OTP, MFA, SSO, CAPTCHA, passkey, or device approval has no
browser fallback. Request a short-lived token/session through an ephemeral
secret-input channel; if none can establish the approved state, return
`Unverifiable` before product mutation.

## Server and serving source

Start a long-running server as a run-owned background process with exact PID,
cwd, command, port, and bounded log path. Suppress auto-open when the runner
supports it, poll a concrete HTTP/port readiness signal with a bounded timeout,
and continue after readiness rather than waiting for process exit.

Reuse an existing server only when its cwd matches the worktree, its asset/watch
pipeline is current, and a bundle/response or changed render proves the serving
version. Cwd alone is insufficient. Preserve other-worktree and user processes;
use a separate port when ownership or freshness is uncertain.

Record browser/version, target, viewport/DPR when relevant, working tree, server
process/cwd, asset pipeline, and serving-version proof as compact facts.
