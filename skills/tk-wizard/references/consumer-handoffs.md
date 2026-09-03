# Consumer setup handoffs

Read this only when another skill delegates a human-only host setup, authentication,
permission, or restart step. The consumer retains its target, operation, mutation authority,
and verdict. Guide one current user action, observe its completion signal, then return the
exact resume action.

Require a bounded handoff with:

- consumer and exact pending criterion;
- detected host/client and current capability state;
- missing or incompatible capability;
- required and recommended properties;
- verifiable completion signal;
- exact resume action;
- fallback eligibility and enabling evidence, when applicable.

Use installed/local host evidence before current official documentation. Derive the exact
configuration file, scope, command shape, UI literal, and restart instruction; do not invent
them. Preserve unrelated configuration and show the smallest user-controlled change. Never
silently edit host configuration.

## Browser provider setup

For a new Chrome DevTools MCP route, require effective headless mode and recommend an
isolated provider profile. Use the consumer-provided conceptual default:

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

TigerKit installs no browser provider or upstream provider skills. Do not add
`--browserUrl`, `--wsEndpoint`, a remote-debugging port, or port `9222` to an ordinary new
setup. Offer attach only when the handoff contains observed managed/direct launch failure or
equivalent sandbox/VM/container/host-boundary evidence. Before the user selects attach,
explain that the external launcher owns headless mode, endpoint exposure, and profile data.

Preserve an existing MCP entry and unrelated settings. If effective headless mode is missing,
guide only the smallest supported correction. Treat provider isolation as recommended: explain
the persistence limitation if omitted, but do not present it as the headless safety gate.

If the client must restart, return `Status: Pending`, the observed completion signal so far,
and the exact instruction that reruns `tk-browser-verify` for its original criterion. Do not
claim that browser verification passed.

## GitHub image upload setup

Accept only human actions such as host-level `gh` installation or repair when agent execution
is inappropriate, interactive `gh auth login`, account/repository permission changes, or an
explicitly selected CDP route's Chrome permission/restart step. Do not take over reviewed
extension selection or installation, image staging/upload, PR mutation, or render verification.

After a completion signal that needs no client restart, return control to
`tk-github-image-upload-to-pr` with its original repository, PR/comment target, image set, and
selected route intact. If restart is required, return `Status: Pending` and an exact resume
action without claiming that any image was uploaded.
