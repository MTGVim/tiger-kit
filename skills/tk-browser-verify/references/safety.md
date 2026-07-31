# Browser safety

Without a safe test environment or explicit authority, do not cause real
payment, external communication, irreversible deletion, production-data
mutation, account changes, permission changes, or equivalent side effects.
Guard reports the limit without mutation. Verdict captures and inspects the
blocked final state, then returns `Unverifiable`.

Reach API-gated UI through an exact response-envelope mock when possible.
Inspect source response mapping; never send, save, or pay merely to create a
success state.

Allow headed relaunch and user login only for interactive auth such as OTP,
passkey, CAPTCHA, or device approval. Reuse only a user-local profile outside
the repository. Never output, copy, or commit credentials, cookies, tokens,
profile contents, or profile paths.

Every Guard or Verdict success, failure, and runtime-blocked final state needs a
non-empty screenshot and actual image analysis. Missing either prevents a
completed result and makes the run `Unverifiable`.

Separate screenshot/video from network/HAR/console inventory and record
`Sensitivity`, `Redaction`, and `Residue check`. Authorization, cookies,
tokens, credentials, secrets, or sensitive bodies make a capture sensitive.
Use it only after verified redaction and original/move-path residue absence.

When `.tigerkit/` is not ignored, do not persist sensitive captures
repo-locally. Redact and verify in owned external temp, then move only a safe
result. Otherwise the capture is `Unverifiable`. Never move or delete user
screenshots/fixtures or unknown-ownership artifacts.

User-facing progress and receipt prose follows the user's language.
