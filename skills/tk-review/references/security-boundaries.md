# Browser and Agent Trust Boundaries

Read only for scoped browser trust decisions or LLM/Agent/MCP execution. Use the
owning audit/review's evidence, finding and read-only rules; these lenses add no
scanner, remote test, mutation authority or separate review procedure.

## Browser code

- For `postMessage`, connect a reachable sender to a sensitive receiver action or
  disclosure. Check exact allowed origins and the expected `event.source` when
  same-origin frames have different trust. A substring origin match or `*` target
  matters only with an unintended recipient or reachable sensitive action.
- For Service Worker caches, Storage and cross-tab messages, trace writer, reader,
  account/tenant key and logout/account-switch/offline/stale-tab lifecycle. Require
  another account or less-trusted context to receive data or stale authority;
  storing a token or registering a worker alone is not a finding.
- For DOM/XSS, trace untrusted content into an executing sink or framework escape
  hatch. Framework interpolation escaping and effective browser policy are controls.
  For prototype pollution, require both a prototype-changing write and a reachable
  security-relevant consumer (gadget); parsing JSON or a gadget-free write is insufficient.

## Model and tool code

- Trace writable documents, retrieval, memory or tool/MCP responses through the model
  to the handler's side effect. Name the requester, affected principal, effective
  execution identity, target and action. Prompt injection text alone is not a finding;
  identify the code-level authority, data or action-binding failure and its effect.
- Check handler-side requester/resource authorization after arguments are final.
  A shared service credential can be safe with enforced per-user scope. A schema or
  guardrail prompt does not establish resource permission or safe sink semantics.
- Compare the intentionally requested/approved action with the normalized tool name,
  complete arguments, requester and target actually executed. Valid resource permission
  alone does not authorize an attacker-induced action. Follow queue, retry, resume and
  batch paths for changed arguments or duplicate side effects and their idempotency guard.
- For retrieval/memory, connect an attacker-controlled write with a cross-user/tenant
  read or privileged decision, including query filters and cache keys. For tool schema
  disagreement, trace coercions, aliases or defaults into a different security-relevant
  handler value; accepting structured output alone proves neither safety nor a defect.

## Evidence limits

Check existing guards before raising a candidate and retain a safe counterexample.
Use bounded local evidence with dummy identities when execution is needed. If a required
browser policy, deployed header, provider identity or external routing fact cannot be
observed, mark that premise `Unverifiable` and name the missing check; do not label the
path confirmed. This does not authorize production probing or broader access.
