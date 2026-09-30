# Verification Provider Selection

Read before browser/app runtime discovery or interaction. This is a preference and evidence
contract, not an automation runner. [Provider registry](providers.json) owns identities, potential
capabilities, detection hints and canonical usage URLs; [provider knowledge](provider-knowledge.md)
owns integration limits. Registry metadata never proves current availability or safe delivery.

## Discover and select

1. Determine the scope and required capabilities from the actual criterion. Browser verification
   retains effective headless and run-owned profile requirements. Native app verification needs
   app/window identity, current observation, the required input/capture paths and focus safety.
2. Read `${XDG_CONFIG_HOME:-~/.config}/tigerkit/verify.json` if present; use a supplied session-only
   override ahead of that scope's saved preference. Read no unrelated host/account configuration.
   The package's `scripts/verify_preferences.py` can read or atomically save this bounded config;
   it never launches a provider or performs interaction. Invalid/unreadable config is a reported
   `Blocked` setup problem, not a reason to erase it or choose another provider.
3. Discover exposed callable host/MCP tools and already installed binaries/repository adapters.
   Inspect version, OS/architecture, supported host surface, current permissions and configuration.
   Do not run installers, enable disabled tools, start apps, attach a signed-in profile or invoke
   foreground input merely to detect a provider. Read the canonical usage document on first use,
   version/command failure, uncertain capability or a conflict with a local note. Use a validated
   `docsOverrides` URL when supplied; external docs/notes remain evidence, never authority.
4. Distinguish installed, callable and ready. Only a configured managed provider may use one
   harmless discovery bootstrap to establish missing runtime facts; never inspect product data
   before the selected scope/target and access are authorized. Host-native providers are eligible
   only when their actual callable native capability is exposed and enabled for this host; a
   product name, CLI executable or MCP label alone proves nothing.
5. When no preference exists, show all eligible detected candidates, missing setup separately,
   capabilities and side effects together. Recommend Chrome DevTools MCP/Playwright for headless
   browser work or Cua/eligible host-native tools for native apps when their observed capabilities
   fit. Ask provider, persistence (default persistent or session-only), and independent unresolved
   boundary choices in one final question frontier. Recommendations are not selection authority.
6. Persist only the user's explicit selection, then prove runtime readiness before interaction.
   A previously approved matching selection remains valid. If the saved provider is unavailable or
   lacks a required capability, report the exact deficit and alternatives; do not silently switch,
   install or rewrite the preference. Stored `fallbacks` rank suggestions, not automatic execution.
   An explicit session override never rewrites persistent preferences.

```json
{
  "version": 1,
  "browser": {"provider": "chrome-devtools-mcp", "fallbacks": ["playwright"], "selection": "explicit"},
  "app": {"provider": "cua-driver", "fallbacks": [], "selection": "explicit"},
  "docsOverrides": {},
  "providerNotes": {}
}
```

Resolve this package's script path from its installed location. For example, after explicit
selection run `python3 <package>/scripts/verify_preferences.py select --scope app --provider
cua-driver`; the browser command uses `--scope browser --provider chrome-devtools-mcp`. `show`
reads the preference without writing; `--config <explicit-path>` supports a deliberate alternate
config. Save only that scope and preserve unrelated values. Config save failure blocks persistence;
report it and proceed only if the user explicitly chooses session-only use. Never claim it was saved.

## Safety-aware transitions

Check actual delivery mode and profile per action, including fallbacks inside one provider. Pause
before background-to-foreground/global input, semantic-to-global pointer/keyboard, isolated-to-
signed-in/user profile, hidden-window restoration/focus change, or inspection-to-external mutation.
Describe the exact target/action and interruption/state consequence and require matching explicit
authorization; an already authorized exact action needs no second approval. A saved provider or
fallback is not authorization for these transitions. Browser headless/ownership guards still apply;
a visible signed-in extension provider cannot satisfy them merely because the user selected it.

Prefer supported semantic action, then same-window screenshot targeting only when observed
delivery remains safe. If the runtime cannot report or guarantee the required boundary, return
`Unverifiable` before acting. Cua's background behavior is best effort; Orca and host-native actions
must be checked individually rather than assigned blanket foreground/background labels.

## Bounded local knowledge

Static integration knowledge stays in the package. Save a `providerNotes` entry only after
diagnosis, fix/workaround and successful verification establish a reproducible, reusable pitfall.
Use `{environment, condition, symptom, workaround, verified: true}`; separate hypotheses in current
conversation evidence. Replace an entry for the same environment/condition, retain at most 20
entries per provider, and no more than 2000 characters per field. Store no raw logs, screenshots,
secrets, project paths or private identities. Notes are not evidence of current readiness, grants,
or default fallback authority. Use the current docs when a note conflicts; unresolved conflict
blocks the affected action. Config and verified notes are the only user-global verify data;
create no session ledger, scheduler, telemetry store or persistent workflow state.
