# Headless environment

Choose the simplest native, Playwright-compatible, MCP, or CDP path that can produce
approved evidence. Discover routes in this order: an available host-native or browser MCP
provider, an installed Chrome DevTools CLI, a repository-provided Playwright/Puppeteer path,
then another already available verified CDP route. Do not install a new browser dependency
for one run. Classify the selected path as `managed launch | direct launch | attach`.

For `managed launch`, inspect the current host configuration and require an effective
headless option before product interaction. The provider may start lazily, so a missing live
browser process before its first call is not a failure. Use one harmless discovery call to
bootstrap it, then record available runtime browser/version, transport, and ownership facts.
A provider-managed pipe or equivalent transport needs no TCP endpoint. Modern
`--headless`, `headless: true`, and another installed-version-equivalent headless setting
are valid; do not require the exact text `--headless=new`.

Provider isolation is recommended, not a separate headless requirement. Prefer an ephemeral
provider profile for a new configuration and use a scenario-isolated context when supported.
An effectively headless provider-managed dedicated persistent profile remains usable when it
is not the user's normal browsing profile; disclose that cookies, storage, and cache can
survive provider restarts. Never treat `--isolated` as proof of scenario-level isolation.

For `direct launch`, prove the effective headless option and run-owned browser/profile from
the launch command and runtime state. For `attach`, prove the live endpoint, effective
headless mode, and external browser/profile ownership before any browser call. A fixed
`--browserUrl` provider starts no browser, so all of those facts belong to the external
launcher. A saved port, prior browser UUID, `DevToolsActivePort`, provider default,
configuration claim, or tool name is not sufficient attach evidence. If an attached process
is headed, belongs to another run or the user, or has unknown ownership, return
`Unverifiable` without creating a page.

## Missing provider setup

If no compatible route exists, do not install a provider or edit host configuration. Make no
browser call. Invoke `tk-wizard` with the consumer `tk-browser-verify`, the exact blocked
criterion, detected host/client and provider state, the missing capability, required
effective headless mode, recommended provider isolation, completion signal, and exact resume
action.

For a new Chrome DevTools MCP configuration, pass this conceptual default to the wizard:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest", "--headless", "--isolated"]
    }
  }
}
```

The wizard must derive the exact host-supported file, scope, command shape, and restart step
from current local or official evidence and preserve unrelated configuration. TigerKit skills
do not install Chrome DevTools MCP, its CLI, or its upstream skills.

Do not include `--browserUrl`, `--wsEndpoint`, a remote-debugging port, or port `9222` in the
default. An attach route becomes eligible only after observed managed/direct launch failure or
equivalent sandbox, VM, container, or host-boundary evidence. Pass that evidence to the
wizard, explain the exposed-debugging and external-profile implications, and require the user
to select attach before presenting its configuration.

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

When no safer temporary secret-input channel exists, first prove that
`git ls-files -- .tigerkit/` returns no tracked paths and
`git check-ignore -q -- .tigerkit/` succeeds. Accept Git's effective ignore decision
whether it comes from a per-directory `.gitignore`, `.git/info/exclude`, or the configured
user-level excludes file. Then create
`.tigerkit/secret-input/tk-browser-verify-<run-id>/token` with directory mode `0700` and
file mode `0600`. Leave the file empty, then give the user both the repository-relative
and absolute paths plus a host-appropriate clipboard-to-file command that does not place
the secret in command arguments or shell history. Do not launch an editor, file opener,
GUI, terminal UI, or focus-changing application merely to collect the secret. Open it
only after the path is shown and the user explicitly asks. Never ask for or accept the
value in chat. If the path is not ignored, writable, or user-accessible, do not edit
`.gitignore` or choose an external scratch path; return `Unverifiable`.

After showing the paths, start a bounded watcher or poll for non-empty file state without
reading, echoing, or reporting the content, size, or modification time. Do not ask the user
to send a completion message. When the file becomes non-empty, recheck ownership and mode
`0600`, then continue directly to the approved injection. Renew an expired wait window
while the task remains active. Only when the runtime can no longer wait, leave the
run-owned input path in place and report how monitoring can resume; never treat a timeout
as proof that no value will be supplied.

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
