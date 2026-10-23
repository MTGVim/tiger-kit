# Finding quality

Read this for every code review before reporting findings.

Report a finding only after identifying the exact changed or affected location, a reachable input/state/sequence, and a
concrete observable impact. Inspect surrounding guards, callers, imports, tests, types, and framework/runtime defaults;
repository behavior outranks a generic heuristic. Set severity from impact and reachability, discard taste or speculation,
and allow zero findings.

When implementation and related tests/evals change together, compare the behavior protected before and after: reduced
counts/ranges/fidelity, relaxed calls/conditions, removed assertions/scenarios, skip/xfail/exception allowances, excluded
tests, or checks of mocks/tools instead of observable results may hide a regression despite GREEN. Compare intent/AC,
the prior contract, a reachable failure and remaining protection; legitimate specification changes are not defects.
Patterns alone establish neither a finding nor severity. Missing material evidence follows the existing Unresolved /
Unverifiable path, not an invented failure or pass.

Support absence/removal-safety claims within the affected system's relevant scope: check plausible name variants,
dynamic imports, string entry points, routes/configuration and registration conventions as applicable. A static zero-match
search alone cannot establish absence when runtime lookup remains unchecked. For API/shape/field/ID/state changes,
trace the producer through relevant direct and indirect consumers and compatibility/migration boundaries; verify actual
read paths rather than only the changed producer. Reuse exact-target fresh-state evidence and refresh affected claims
after edits; do not add a global search ritual, a new review phase or a report ledger.

Cluster manifestations only when evidence proves the same causal root, correction boundary, and failure class. Similar
symptoms or a report's proposed mechanism are not proof.

Check for silent failures: empty catches or ignored exceptions, errors converted without evidence into `null`, empty data,
or default success, log-and-continue paths that lose required context, partial mutation reported as success, and missing
propagation or rollback. Do not flag an intentional fallback when its observable contract, telemetry, or caller handling
makes the behavior explicit and safe.

Treat apparent issues as questions until context confirms them. Caller-side validation, proven narrowing, intentional
fire-and-forget, fixed-cardinality loops, test literals, framework guarantees, and unchanged code often reject a finding.
Runtime breakage, data loss, security, or payment risk is not dismissed merely because the affected line is unchanged.

Use `Critical` only when the exact change cannot safely merge because it creates or exposes a concrete path to broken
required or core functionality, security compromise, payment/data loss or corruption, irreversible migration failure,
or build/deploy/runtime unusability. Use `Important` for a concrete reachable change-owned defect that should be fixed
before merge, including an unmet binding AC, supported-path contract mismatch, bounded recoverable wrong behavior,
incorrect error handling, or a protection gap tied to one named changed behavior and plausible regression.

Architecture, maintainability, or test concerns qualify only when they establish a concrete failure or material cost.
Do not report style, generic requests for more tests, optional optimization, documentation polish, pre-existing unrelated
defects, or subjective preference. Severity reflects impact, reachability, blast radius, and recoverability; record
confidence separately rather than lowering severity.
