# Usage evidence

Read only when usage frequency or inactivity is in the approved audit scope. Use
read-only evidence from the current host; never enable telemetry, run audited code,
refresh counters, or create a usage registry in `.tigerkit/`.

## Classify before interpreting

For each item, verify its identity and the signal's semantics from native metadata,
diagnostic documentation or implementation. Distinguish execution-only counters,
install/activation-prepopulated counters, session-history matches, and passive
components with no execution signal (such as a display panel). A zero, missing field,
disabled setting, file age, or absent session match alone does not prove inactivity.

Record source/path, counter semantics/value, last execution, installation or tracking
start, resets/retention, observation interval and session search coverage. Match exact
item identity and aliases; distinguish actual execution from a mention or installation.
Do not expose raw session contents or credentials. Incomplete identity, unknown counter
semantics, missing timestamps or reset/retention gaps make the affected inference
`Unverifiable`, not zero usage.

Use the requested inactivity interval, or 30 days when none is specified, and report
that threshold. Propose `deprecate` only when verified execution tracking covers the
whole interval and either (a) its execution-only counter is zero with no corroborating
execution in available sessions, or (b) its last actual execution predates the interval
and no later execution is recorded. For zero counters, verify tracking/installation
started before the interval; for positive counters, a verified last-execution timestamp
can establish inactivity. Resolve conflicting later session executions before proposing.

Installation/activation counts cannot establish execution. Session search alone can
support inactivity only with verified complete execution coverage for the whole interval;
otherwise defer. A short recent-history sample cannot prove month-long inactivity or
invalidate a longer verified counter history: state each source's coverage separately.
For a passive component without a usage signal, leave a user question about actual use,
not a data-based removal recommendation. Never classify a working panel as unused from
its zero counter. Short observation periods defer the proposal.

## Locate evidence on the current host only

| Host | Read-only source discovery | Counter fallback |
| --- | --- | --- |
| Claude Code | Resolve the active configuration root and native diagnostics/history through installed help or metadata; inspect only verified in-scope sources. | Counter location/semantics are `Unverifiable` until confirmed locally; use available session evidence with its actual coverage. |
| Codex | Resolve the active Codex home and exposed native session/history or diagnostic tools from current host evidence. | Same: never assume a skill counter exists or equate a skill-list entry with execution. |
| Hermes | Resolve the active Hermes home and native diagnostic/session backend from installed help or metadata. | Same: confirm the installed backend/schema before reading a counter; never guess database tables. |
| Other identified host | Read its exposed native diagnostics or verified metadata paths; if no location is verified, leave the source `Unverifiable`. | Use only accessible, verified session evidence; no cross-host probing. |

These are discovery routes, not claims that every host/version exposes counters.
Read only necessary records within approved scope. An unavailable counter does not
justify guessing its location or widening the audit to unrelated sessions.

## Report without changing host settings

Put the threshold, signal semantics, coverage, values/last execution and evidence paths
in the existing Disposition Basis; no extra ledger or report format is needed. For
user-managed items, `deprecate` remains an exact pending recommendation to the owner.
For vendor-managed items keep Action `keep (vendor)` and report only the usage finding;
never propose editing the vendor package. Disabling skills/plugins, uninstalling,
changing host settings or telemetry stays advice-only in every apply mode, including
`--apply`. Preserve the ordinary ownership, tier and evidence-gap rules.
