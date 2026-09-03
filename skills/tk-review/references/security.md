# Security review

Read this only when review scope reaches authentication or authorization, attacker-controlled input/file/path/command/URL,
secrets or sensitive data, an API endpoint, payment, webhook, external integration, or security configuration.

Trace an attacker-controlled source to the sensitive sink and verify the repository/runtime guard before reporting. Check
object-level authorization; SSRF across redirects and resolved destinations; path traversal and symlinks; command/query
injection; XSS through framework escape hatches; secret leakage in logs, URLs, or artifacts; webhook signature, replay,
and idempotency; and race/TOCTOU/transaction/lock boundaries when the touched behavior makes them reachable.

Do not impose universal rate limiting, CSRF, storage, dependency scanning, or sanitization rules. Framework defaults,
deployment topology, repository policy, and the concrete exploit path decide whether a finding exists. Never introduce a
new scanner or dependency merely to complete review.
