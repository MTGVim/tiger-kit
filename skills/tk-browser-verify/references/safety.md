# Browser safety

Without a safe environment and explicit authority, do not cause payment, external
communication, irreversible deletion, production-data mutation, account changes,
permission changes, or equivalent side effects. For an approved UI state, prefer an
exact repository-evidence-based response mock over sending, saving, or paying.

Headless-only is absolute. Interactive authentication has no visible-browser exception.
Do not request secrets in ordinary chat or place secret-bearing values or commands in
prompts, output, ledgers, logs, screenshots, HAR, console captures, or receipts. Use
only an available temporary secret-input channel under the ignored repository-local
`.tigerkit/secret-input/` contract and record only non-sensitive authentication-mode
facts. A user calling the value a development token does not relax this boundary.

Separate screenshot/video inventory from network/HAR/console inventory. A capture is
sensitive if it contains Authorization data, cookies, tokens, credentials, or sensitive
bodies. After proving the repository-tracked ignore rule, stage an unavoidable sensitive
capture only in `.tigerkit/tmp/tk-browser-verify/<run-id>/sensitive/`. Use a redacted copy
only after confirming that neither the original nor transfer path retains residue, then
delete the staging directory and verify its absence. If the path cannot be used, do not
choose an external fallback; safely delete owned captures and return `Unverifiable`.

Do not use a request-inspection tool that returns raw `authorization`, `cookie`, or other
headers merely to inspect a payload. When an approved non-secret request body is required,
intercept only the body inside the page by wrapping `fetch` or `XMLHttpRequest.send`; do not
return headers, cookies, or transient authentication material.

Never move or delete user screenshots, fixtures, profiles, or artifacts with unknown
ownership. Never change `.gitignore` for evidence handling.
