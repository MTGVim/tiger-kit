# Headless environment

Choose the simplest native, Playwright-compatible, MCP, or CDP path that can produce
approved evidence. Do not install a new browser dependency for one run. Before the
first browser call, prove the exact valid `--headless=new` argument, binary,
PID/provider process ID, and isolated run-owned `user-data-dir` for every new
Chrome/Chromium process.

For CDP, verify the live endpoint, actual process, port, and profile ownership. A saved
port, prior browser UUID, `DevToolsActivePort`, provider default, or tool name is not
evidence. Never attach to or change a browser whose ownership is unknown or belongs to
the user.

## Authentication

Reuse only a safe authenticated session that is already available, owned by this run,
and verified as headless. Otherwise, use transient material through the exact
repository/application-supported header, cookie, storage, session bootstrap, or fully
non-interactive login path. Do not capture secret values; verify the authenticated
target state.

There is no browser bypass for interactive login, OTP, MFA, SSO, CAPTCHA, passkey, or
device approval. Request a short-lived token/session through the temporary secret-input
channel. If no approved state can be established, return `Unverifiable` before a
product mutation.

## Server and serving source

In a `standalone` run with multiple viable `dev-server` commands, present the candidates
and selection to the user and obtain confirmation before starting one. In a `nested`
run where the `parent` supplied the exact command, do not ask for the same decision
again. Include `BROWSER=NONE`, or the repository-documented equivalent `auto-open`
suppression, for a `react-scripts`/CRA server. Start a `long-running server` as a
`run-owned` background process with an exact PID, `cwd`, command, `port`, and bounded
`log` path. Poll a concrete `HTTP`/`port` `readiness signal` under a `bounded timeout`;
continue after `readiness` instead of waiting for process exit.

Reuse an existing server only when its cwd matches the worktree, its asset/watch
pipeline is current, and a bundle/response or changed render proves the serving
version. The cwd alone is insufficient. Preserve other worktrees and user processes;
use a separate port when ownership or freshness is uncertain.

Record concise facts for browser/version, target, viewport/DPR when relevant, working
tree, server process/cwd, asset pipeline, and serving-version proof.
