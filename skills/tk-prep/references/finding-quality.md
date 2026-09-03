# Finding quality

Read this for every code review before reporting findings.

Report a finding only after identifying the exact changed or affected location, a reachable input/state/sequence, and a
concrete observable impact. Inspect surrounding guards, callers, imports, tests, types, and framework/runtime defaults;
repository behavior outranks a generic heuristic. Set severity from impact and reachability, discard taste or speculation,
and allow zero findings.

Cluster manifestations only when evidence proves the same causal root, correction boundary, and failure class. Similar
symptoms or a report's proposed mechanism are not proof.

Check for silent failures: empty catches or ignored exceptions, errors converted without evidence into `null`, empty data,
or default success, log-and-continue paths that lose required context, partial mutation reported as success, and missing
propagation or rollback. Do not flag an intentional fallback when its observable contract, telemetry, or caller handling
makes the behavior explicit and safe.

Treat apparent issues as questions until context confirms them. Caller-side validation, proven narrowing, intentional
fire-and-forget, fixed-cardinality loops, test literals, framework guarantees, and unchanged code often reject a finding.
Runtime breakage, data loss, security, or payment risk is not dismissed merely because the affected line is unchanged.
