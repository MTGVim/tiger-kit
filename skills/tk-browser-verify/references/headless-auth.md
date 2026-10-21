# Headless authentication

All required scenarios must be executable headlessly. Use this priority order:

1. no authentication required
2. reuse an existing safe, verifiable, run-owned authenticated session/profile
3. reuse the same worktree's protected authentication input and restore expired access through the application's supported renewal path under [environment](environment.md)
4. inspect bootstrap and renewal contracts before the first input request under [environment](environment.md); request only missing fields, including refresh material required by that route, then inject through the repository/application-supported bootstrap
5. use username/password only for fully non-interactive login without OTP, MFA, SSO, CAPTCHA, passkey, or device approval

Do not guess the authentication injection method. Tie it to repository/application evidence or a user-specified method and
verify the resulting authenticated state.

Do not store usernames, passwords, tokens, OTPs, cookies, session values, recovery codes, or sensitive identities in
the conversation, `.tigerkit/*.md`, prompts, logs, summaries, or child receipts.
Record only non-sensitive facts such as `auth mode: token-headless` or `authenticated state established`.
Retain authorized non-production access/session and route-required refresh material only in the protected
worktree-local input under [environment](environment.md); stage cleanup and expiry do not delete it.
Never retain production credentials or share token files between worktrees. Never print file contents.

If safe headless authentication cannot be established, do not fall back to a visible browser; return `Unverifiable`.

