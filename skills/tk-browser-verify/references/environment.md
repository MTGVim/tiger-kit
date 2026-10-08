# Headless environment

Use the explicit preference/session choice under [provider selection](provider-selection.md).
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

## Worktree-shared development credentials (opt-in only)

For an explicitly authorized local/development task, prefer a previously verified token in
the same Git common directory before creating another secret-input file. Resolve the exact
application authentication **authority** (not the worktree-specific dev-server port), environment,
role and non-secret account/profile label from repository facts and the user; never merge scopes
or infer a role. Use `python3 <package>/scripts/shared_auth.py inspect --repo <worktree-root>
--authority <auth-origin> --environment <environment> --role <role> --profile <label>`.
It resolves `git rev-parse --git-common-dir`, so linked worktrees share a protected scope even
when their `.tigerkit` directories differ. The helper prints only status, timestamps, revision
and an optional **local** credential-file path; it never prints token contents.

The default cache backend is a **local 0700 directory / 0600 file under Git's common directory**,
not encrypted OS Keychain storage. Other processes running as the same OS user and filesystem
backups may still access its contents. Never claim encryption. Use it only when the user has
authorized development credential retention and local plaintext-at-rest is acceptable; if the
organization requires keychain-backed or nonpersisted credentials, do not create this cache.
An unsupported host ACL/backend, insecure permission, symlink, linked file or ambiguous Git
identity is `Blocked | Unverifiable`, never a reason to downgrade protection. The helper blocks
known production environment labels; never cache actual production credentials under an alias.
The cache is outside the source tree and must never be committed, summarized or used for
publication. Manual deletion/revocation is required when worktree sharing is no longer wanted.

A status of `ready` only means the *known expiration* has not passed;
`needs-verification` means expiration is unknown. Neither proves authenticated access. Verify
the actual target state through the existing approved, no-log header/cookie/storage bootstrap.
A proven authentication failure invalidates only the exact observed cache revision using
`invalidate --revision <observed-revision>`; reread before requesting user input, since another
session may already have refreshed it. Never infer expiry from an arbitrary HTTP failure.

For a missing/expired/invalidated scoped token, invoke `claim` before prompting the user.
A `claimed` response gives a non-secret claim ID. Its owner invokes
`prepare-input --claim-id <id> --run-id <run-id>` with the same trusted scope arguments,
after the normal Artifact Paths ignore checks. This command creates or reuses the exact
private `.tigerkit/secret-input/tk-browser-verify-<run-id>/input.json`, then reports the
**actual absolute and relative paths**, blank JSON template and required field without
printing stored contents. Copy those real paths into the user-visible reply, explain the
exact paused verification and how to fill and save `{"token": ""}`.
Never enter `Pending` or start polling without showing both paths from a successful
`prepare-input` result. Failure to create/read back the path is `Blocked | Unverifiable`,
not a guessed example path. The seeded blank file is `Pending`, never `Ready`.
Run `await-input --claim-id <id> --input <absolute-input-json> --seconds <1..180>`
with the same scope arguments for bounded, no-output-of-secrets readiness polling.
The helper returns only `ready | pending | blocked`. A partial JSON save or empty token remains
`pending`; a permission, ownership or symlink failure blocks immediately. If the active host
permits another bounded wait, renew the owned claim and continue without asking the user for
a completion message. Privately validate and consume the latest safe input snapshot,
inject into the actual target and verify authenticated state; only then invoke
`commit --claim-id <id> --input <absolute-input-json>` to atomically store the shared token.
Pass an `--expires-at` only when verified from the application's contract. Immediately delete
the one-shot input and loopback server on all exit paths regardless of cache write success.

While an input prompt remains active, periodically `renew --claim-id <id>` within its reported
lease. Another worktree receiving `pending` must NOT create its own input; it can use bounded
`wait --since <last-revision> --seconds <1..180>` and re-inspect before using new credentials.
This is live, bounded polling in the **active** agent workflow, not a daemon, background job,
or a promise to restart an ended conversation. On interruption release the owned claim when
possible; after lease expiry another run can claim. Do not overwrite another run's pending
file, renew its claim or delete its tokens. An expired user input wait that can no longer
remain active must report the exact existing input path and resumption procedure. If secure
cache input fails, preserve the verifier's existing transient-only mode without making false
shared-state claims. Project-specific refresh-token/API automation is out of scope.

When no safer temporary secret-input channel exists, first prove that
`git ls-files -- .tigerkit/` returns no tracked paths and
`git check-ignore -q -- .tigerkit/` succeeds. Accept Git's effective ignore decision
whether it comes from a per-directory `.gitignore`, `.git/info/exclude`, or the configured
user-level excludes file. Then create
`.tigerkit/secret-input/tk-browser-verify-<run-id>/input.json` with directory mode `0700` and
file mode `0600`. Apply the user-editable input branch in [artifact paths](artifact-paths.md):
seed a plain JSON object such as `{"token": ""}`, using only the exact required fields.
Before showing paths or input mechanics, state in one sentence which pending verification step
needs this user-only input and why the existing evidence or authenticated state cannot satisfy it,
using the user's terms. For example, say that the earlier run verified a different head or that
the previous authenticated session expired. Do not lead with SSO, token-file, provider, or storage
mechanics when the reason is the missing final-head verification.
Give the user both the repository-relative and absolute paths, the secret-free template,
and instructions to fill and save it. A clipboard command must JSON-serialize into the
named field, preserve other fields and keep secrets out of arguments/history.
Do not launch an editor, file opener,
GUI, terminal UI, or focus-changing application merely to collect the secret. Open it
only after the path is shown and the user explicitly asks. Never ask for or accept the
value in chat. Use the owning SKILL.md Artifact Paths setup when ignore coverage is missing.
If the path remains unignored, unwritable, or inaccessible, use no external scratch path;
return `Unverifiable`.

After showing the paths, start bounded metadata-change polling without reporting content,
size or modification time. The initial JSON is non-empty and must remain `Pending`.
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

Stop the loopback server and delete the JSON input file and its run directory immediately
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
