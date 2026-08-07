# Browser safety

Without a safe environment and explicit authority, do not cause payment,
external communication, irreversible deletion, production-data mutation,
account change, permission change, or an equivalent side effect. Prefer an
exact repository-evidenced response mock for an approved UI state over sending,
saving, or paying.

Headless-only is absolute. Interactive authentication has no visible-browser exception.
Do not request a secret in ordinary chat or put secret-bearing values/commands in
prompts, output, ledgers, logs, screenshots, HAR, console capture, or receipts.
Use only an available ephemeral secret-input channel and record a non-sensitive
auth-mode fact.

Separate screenshots/video from network/HAR/console inventory. Authorization,
cookies, tokens, credentials, and sensitive bodies make a capture sensitive.
Use it only after verified redaction and absence of the original and moved-path
residue. Otherwise delete the owned capture safely and return `Unverifiable`.

Never move/delete user screenshots, fixtures, profiles, or unknown-ownership
artifacts. Never edit `.gitignore` for evidence handling.
