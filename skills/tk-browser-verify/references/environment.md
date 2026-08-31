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

When no safer temporary secret-input channel exists, first prove with `git check-ignore -v`
that a repository-tracked ignore rule covers `.tigerkit/`; global excludes and
`.git/info/exclude` are insufficient. Then create
`.tigerkit/secret-input/tk-browser-verify-<run-id>/token` with directory mode `0700` and
file mode `0600`. Leave the file empty, then give the user both the repository-relative
and absolute paths plus a host-appropriate clipboard-to-file command that does not place
the secret in command arguments or shell history. Do not launch an editor, file opener,
GUI, terminal UI, or focus-changing application merely to collect the secret. Open it
only after the path is shown and the user explicitly asks. Never ask for or accept the
value in chat. If the path is not ignored, writable, or user-accessible, do not edit
`.gitignore` or choose an external scratch path; return `Unverifiable`.

After the target hostname and port are final, a no-log one-shot server bound only to
loopback may read the file and return `Access-Control-Allow-Origin: *`. Fetch it inside
the page and apply only the repository/application-supported cookie, header, or storage
bootstrap. Return only injection success and value length, never the value.

Stop the loopback server and delete the token file and its run directory immediately
after injection, then verify all are absent. Perform the same cleanup after failure,
interruption, or exception. Cookie scope follows hostname rather than port: if the hostname
changes, establish the approved state again. For OAuth plus OTP or any other interactive
flow, use the approved transient injection path or return `Unverifiable`.

## Server and serving source

In a `standalone` run with multiple viable `dev-server` commands, present the candidates
and selection to the user and obtain confirmation before starting one. In a `nested`
run where the `parent` supplied the exact command, do not ask for the same decision
again. Include `BROWSER=NONE`, or the repository-documented equivalent `auto-open`
suppression, for a `react-scripts`/CRA server. Start a `long-running server` as a
`run-owned` background process with an exact PID, `cwd`, command, `port`, and bounded
`log` path. Poll a concrete `HTTP`/`port` `readiness signal` under a `bounded timeout`;
continue after `readiness` instead of waiting for process exit.

Before selecting or starting the server, inspect the relevant package script and environment
file for the intended hostname, port, and API target without exposing secret values. Follow
that repository convention instead of drifting to a default port. Readiness requires both a
live response and a project-specific identity such as the expected `<title>`, page marker, or
current bundle fingerprint; an open port alone may belong to another project.

If the selected script uses `A && B` and `A` is the long-running server, `B` cannot execute.
When repository evidence identifies `B` as a required asset/build step and its missing output
causes the observed compile failure, run `B` once as a run-owned prerequisite and record it.
Do not edit source or generalize this into an alternate server workflow.

Reuse an existing server only when its cwd matches the worktree, its asset/watch
pipeline is current, and a bundle/response or changed render proves the serving
version. The cwd alone is insufficient. Preserve other worktrees and user processes;
use a separate port when ownership or freshness is uncertain.

Record concise facts for browser/version, target, viewport/DPR when relevant, working
tree, server process/cwd, asset pipeline, and serving-version proof.
