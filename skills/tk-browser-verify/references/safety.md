# Browser safety

Without a safe environment and explicit authority, do not cause payment, external
communication, irreversible deletion, production-data mutation, account changes,
permission changes, or equivalent side effects. For an approved UI state, prefer an
exact repository-evidence-based response mock over sending, saving, or paying.

Headless-only is absolute. Interactive authentication has no visible-browser exception.
Do not request secrets in ordinary chat or place secret-bearing values or commands in
prompts, output, ledgers, logs, screenshots, HAR, console captures, or receipts. Use
only an available temporary secret-input channel and record only non-sensitive
authentication-mode facts.

Separate screenshot/video inventory from network/HAR/console inventory. A capture is
sensitive if it contains Authorization data, cookies, tokens, credentials, or sensitive
bodies. Use it only after verified redaction and confirmation that neither the original
nor transfer path retains residue. Otherwise, safely delete owned captures and return
`Unverifiable`.

Never move or delete user screenshots, fixtures, profiles, or artifacts with unknown
ownership. Never change `.gitignore` for evidence handling.
