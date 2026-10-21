# Headless environment

Use the provider selected under [provider selection](provider-selection.md).
Discover native, Playwright-compatible, MCP and installed CLI/CDP paths without silently routing
between them. When a required capability is missing, present the deficit and eligible alternatives
in the final question frontier. Do not install a browser dependency for one run. Classify the
selected path as `managed launch | direct launch | attach`; selection never waives the checks below.

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
      "args": ["-y", "chrome-devtools-mcp@latest", "--headless", "--isolated", "--no-usage-statistics"]
    }
  }
}
```

Disable usage statistics in new configurations to avoid the optional telemetry watchdog.
Existing registrations are unchanged. For clients that launch user-scoped MCP servers per session,
consider project scope when verification is needed only in selected repositories; derive the actual
client lifecycle and scope from current evidence rather than assuming one shared server.

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
device approval. First recover existing scoped authentication through the supported application
session/refresh path. Request missing token/session or renewal input only when recovery is
unavailable or fresh login is required. State the exact target environment and repository-verified
login origin; do not infer either from token validity. If that origin is unknown, resolve it
before requesting input. If no approved state can be established, return `Unverifiable` before
product mutation.

## Worktree-local authentication reuse and renewal

Establish readiness during prep before baseline. Public targets and safe existing sessions need
no token input. Apply [worktree-local authentication](authentication.md)'s contract for every related consumer. Keep the same protected
`.tigerkit/secret-input/tk-browser-verify-<run-id>/input.json` across baseline, after and revisions,
including access expiry, capture failure and interruption; preserve the non-secret path/target
binding in active-task handoffs. Reuse is limited to the verified application/login origin,
environment and account/role in this task/worktree. Remove it on explicit user direction or
authorized worktree cleanup, not ordinary phase cleanup. Keep directory `0700` and file `0600`;
recheck Git exclusion, ownership, nonsymlink regular-file status and single hard link before use.

Privately check a finite numeric JWT `exp` or documented non-JWT expiry before injection;
decoding is not signature verification or proof of access. Never inject expired/rejected access
material. Unknown lifetime requires the application's supported readiness check, not an invented
expiry. An authentication rejection does not establish that a separate refresh grant is invalid.

Before the first input request and any later request, inspect the existing application auth client and supported refresh contract:
trusted endpoint, required client authentication/header/cookie/body, response fields and rotation.
Use the existing authorized renewal route; collect a refresh token only if that route needs one.
When it requires user-supplied refresh material, include that field as required in the first input
template, alongside the bootstrap fields; do not defer it until access expires. If no renewal route
exists or it uses existing browser-managed state, request no extra refresh field.
Prefer a separate login session for headless work rather than a rotating grant shared with the
user's daily browser. Sharing a grant may create refresh races; a 401 alone does not prove that
diagnosis. Confirm the app's actual renewal request before changing its transport contract.
Keep refresh material in the protected file/approved secret consumer, never page-visible storage
or the bootstrap server; inject only the app-required access/session fields. If the app itself
requires browser-managed refresh, use its documented isolated bootstrap rather than exposing
extra fields. Serialize renewal through one task owner, validate and atomically save rotated
values without overwriting concurrent edits, then re-read and independently verify target auth.
Before closing an owned browser that performed renewal, privately reconcile only the app's
approved credential fields with its current cookies/session state and atomically update the
same bound protected file under that renewal owner. Validate target/cookie scope and file
permissions again; preserve unrelated fields and concurrent user edits. Do not export the whole
cookie jar or replace accepted material from an unauthenticated/uncertain state. A failed
reconciliation preserves the file and reports the reuse limitation while resource cleanup proceeds.
If a rotating request's result is uncertain, reconcile supported state before retrying. Network
failure alone does not prove invalidation or justify deleting the file/requesting new credentials.
If restoration is unavailable, report the concrete limitation and request only necessary input.
Do not replay a product write automatically after an auth error; first reconcile its outcome
under the owning mutation authority.

Stop the run-owned loopback secret server immediately after every injection; close owned
browser/dev-server resources after capture. Authentication-file retention never keeps processes
or a user browser profile alive. Never print tokens/claims or store them in evidence, Git,
parent/child receipts, another worktree or a global cache. Production credentials, passwords,
OTPs and recovery codes keep their transient lifecycle. This procedure creates no background
refresher or cross-process lock and cannot guarantee continuation after a host session ends.

When no safer temporary secret-input channel exists, first prove that
`git ls-files -- .tigerkit/` returns no tracked paths and
`git check-ignore -q -- .tigerkit/` succeeds. Accept Git's effective ignore decision
whether it comes from a per-directory `.gitignore`, `.git/info/exclude`, or the configured
user-level excludes file. Then create
`.tigerkit/secret-input/tk-browser-verify-<run-id>/input.json` with directory mode `0700` and
file mode `0600`. Apply the user-editable input branch in [artifact paths](artifact-paths.md):
seed a plain JSON object using the bootstrap and renewal fields identified above, with empty strings.
For access-only input use `{"token": ""}`; when the verified route requires both, use the app's exact
field names, for example `{"accessToken": "", "refreshToken": ""}`.
Before showing paths or input mechanics, state in one sentence which pending verification step
needs this user-only input and why the existing evidence or authenticated state cannot satisfy it,
using the user's terms. For example, say that the earlier run verified a different head or that
the previous authenticated session expired. Do not lead with SSO, token-file, provider, or storage
mechanics when the reason is the missing final-head verification.
Give the user both the repository-relative and absolute paths, the secret-free template,
and instructions to fill and save it. A clipboard command must JSON-serialize into the
named field, preserve other fields and keep secrets out of arguments/history.
When the same session already received these instructions for the same input format, later
requests show only one short reason and the actual absolute path. Repeat the template, issuing
location, and input steps only for the first request or when the format changes. Do not preface
the path with a progress plan.
Do not launch an editor, file opener,
GUI, terminal UI, or focus-changing application merely to collect the secret. Open it
only after the path is shown and the user explicitly asks. Never ask for or accept the
value in chat. Use the owning SKILL.md Artifact Paths setup when ignore coverage is missing.
If the path remains unignored, unwritable, or inaccessible, use no external scratch path;
return `Unverifiable`.

Before showing the paths, start bounded metadata-change polling in the background
when supported; the path message is the final text message of the turn, with no tool
calls after it (see [artifact paths](artifact-paths.md), including the unsupported-host fallback).
Release this run's server/browser resources before waiting;
do not launch replacements until input is ready. Never report content, size or
modification time. The initial JSON is non-empty and must remain `Pending`.
On change, use a trusted local reader to validate JSON and all required fields without
returning values or parser excerpts; malformed, blank or partial input remains `Pending`.
Recheck safe path, ownership and mode `0600`, then validate and consume the same current
snapshot and continue directly to the approved injection. Do not ask for a completion
message. Renew an expired wait window
while the task remains active. Only when the runtime can no longer wait, leave the
run-owned input path in place and report how monitoring can resume; never treat a timeout
as proof that no value will be supplied.

After the target hostname and port are final, a no-log one-shot server bound only to
loopback may extract only the validated credential field and return `Access-Control-Allow-Origin: *`. Fetch it inside
the page and apply only the repository/application-supported cookie, header, or storage
bootstrap. Return only injection success, never the value or the JSON wrapper.

Stop the exact run-owned loopback server after injection. Apply the token retention and
cleanup rules above; cookie scope follows hostname rather than port, so a hostname change
requires establishing the approved state again. For interactive OAuth/OTP, use the supported
injection path or return `Unverifiable`.

## Run-owned development server

Choose an available port consistent with repository configuration and the approved API target;
preserve ports already used by the user or another run. Launch the repository-proven server
command and record the PID returned by that launch, cwd, command, host/port and bounded log
path. Use the host's owned process handle when available. Independently check HTTP readiness
and current-project build identity under a bounded timeout. There is no worktree mutex,
Git-common-directory lock, supervisor or server lease.

After each capture phase, stop only the process created by this launch, using its recorded
PID/handle and independently verified process identity. If it creates children, record those
owned child PIDs/handles during launch and stop only those verified children; never search by
port or process name to terminate. An already exited owned process needs no signal. Confirm
owned processes have exited and check the selected port without killing its current occupant.
If ownership is uncertain or shutdown fails, report the observed cleanup residue, never a
successful cleanup or a broad process termination. Do not stop user-owned or other-run servers.

## Server and serving source

In a `standalone` run with multiple viable `dev-server` commands, present the candidates
and selection to the user and obtain confirmation before starting one. In a `nested`
run where the `parent` supplied the exact command, do not ask for the same decision
again. Include `BROWSER=NONE`, or the repository-documented equivalent `auto-open`
suppression, for a `react-scripts`/CRA server. Start a `long-running server` through the host-supported background process API;
record its launch-returned owned PID/handle, `cwd`, command basis, `port`, and bounded `log` path.
Poll a concrete `HTTP`/`port` `readiness signal` under a `bounded timeout`;
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
