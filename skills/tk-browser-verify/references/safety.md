# Browser safety

Without a safe environment and explicit authority, do not cause payment, external
communication, irreversible deletion, production-data mutation, account changes,
permission changes, or equivalent side effects. For an approved UI state, prefer an
exact repository-evidence-based response mock over sending, saving, or paying.

Protect local user shared state as well: apply [user shared-state safety](verification.md#user-shared-state)
before clipboard, file or notification writes. Do not use those actions as default diagnostic
controls. Necessary clipboard mutation requires a complete protected backup before execution,
restoration and independent verification afterward, and disclosure of unsupported type coverage.

Headless-only is absolute. Interactive authentication has no visible-browser exception.
Do not request secrets in ordinary chat or place secret-bearing values or commands in
prompts, output, ledgers, logs, screenshots, HAR, console captures, or receipts. Use
only an available temporary secret-input channel under the ignored repository-local
`.tigerkit/secret-input/` contract and record only non-sensitive authentication-mode
facts. A user calling the value a development token does not relax this boundary.

Separate screenshot/video inventory from network/HAR/console inventory. A capture is
sensitive if it contains Authorization data, cookies, tokens, credentials, or sensitive
bodies. After proving Git's effective ignore decision for `.tigerkit/`, stage an
unavoidable sensitive capture only in `.tigerkit/tmp/tk-browser-verify/<run-id>/sensitive/`.
Use a redacted copy
only after confirming that neither the original nor transfer path retains residue, then
delete the staging directory and verify its absence. If the path cannot be used, do not
choose an external fallback; safely delete owned captures and return `Unverifiable`.

Do not use a request-inspection tool that returns raw `authorization`, `cookie`, or other
headers merely to inspect a payload. When an approved non-secret request body is required,
intercept only the body inside the page by wrapping `fetch` or `XMLHttpRequest.send`; do not
return headers, cookies, or transient authentication material.

Before classifying an approved data-changing check as `unauthorized-or-irreversible`, inspect
the available restore path. If saving the original values again restores the state, treat the
write as reversible; capture a minimal snapshot, restore it after the check, and compare the
restored state with the snapshot. Disclose residual side effects such as a formerly empty field
being populated. Stop and report the cleanup limitation if restoration cannot be verified.
Apply an established user-owned verification-data policy only within its named nonproduction
environment and operation scope; never infer authority from a tracked team setting or from the
verifier's own role.

For every in-scope save handler, first prefer a page-scoped pre-backend capture that records only
allowlisted, non-sensitive body fields and cancels the request before it can reach the backend.
Verify and record that the request was blocked before transmission. This is the default when data
mutation authority is absent; it proves client-side payload construction only, not backend acceptance
or persistence. Never capture or retain a sensitive body. If safe body capture is unavailable,
insufficient, or unsupported, do not send the request without explicit parent-scoped mutation
authority. With authority for that exact environment, entity, operation, and cleanup policy, the
fallback is one trusted UI submission followed by an independent reread; inspect the postcondition
before considering any retry, and restore run-owned test data under the approved cleanup policy.
Keep only the minimum authorized snapshot needed for restoration; never print or log sensitive
original values. If safe snapshot, restoration, or comparison cannot be established, leave the
saved-result check unexecuted and report the limitation.

Never move or delete user screenshots, fixtures, profiles, or artifacts with unknown
ownership. Limit ignore edits to the owning SKILL.md Artifact Paths setup; verify coverage before evidence writes.
