# Committed Assertion Evidence

Read this reference only when implementation adds or changes either:

- a code comment or JSDoc statement that asserts a measurable count, exhaustive scope,
  exclusivity, or current behavior; or
- a hand-written type/schema that models an external API, SDK, persisted payload, or
  another input outside the current implementation's control.

Do not load it for ordinary local intent comments, names, internal types derived entirely
from current code, documentation/wording-only work, or generated contracts.

## Factual comments

Back a measurable or exhaustive statement with fresh evidence from the same candidate.
For claims such as “used by N components” or “reads only X,” inspect the complete applicable
surface and retain the command/query output that proves the count or boundary. Rerun the
evidence after the candidate changes; evidence from before the diff is stale when the diff
can change the result.

If the claim cannot be proved, do not write it as fact. Prefer a stable rationale or
invariant that the code establishes, or omit the comment. Do not replace one unverified
exact claim with vague certainty such as “all,” “always,” or “never.”

## External input contracts

Verify field presence, omission, explicit `null`, container shape, and value type
independently. Use the first applicable evidence:

1. a current authoritative schema or generated contract;
2. server DTO/serializer/handler code, including permission, feature, version, and error branches;
3. fresh runtime responses that cover each relevant variant;
4. supplied versioned API documentation or specification with provenance;
5. one happy-path payload, local call-site assumptions, names, or analogous fields, which
   do not prove required presence, non-nullability, or shape.

A field appearing once does not prove that it is required or non-null. A `null` observation
does not prove that omission is impossible, and omission does not prove that `null` is
impossible. Do not declare a field required/non-null or collapse `T[]`, record/map, and `T`
without evidence that covers the applicable variants.

When the contract remains unverified, preserve that uncertainty at the boundary using the
repository's existing validation or conservative typing convention; do not invent a precise
contract. If no safe representation exists without changing product behavior or compatibility,
return to preparation with the exact missing evidence instead of guessing.

## Verification boundary

This gate changes the evidence needed for durable assertions; it does not create a new test
ceremony. Follow `testing.md` only when observable code behavior changes. Before completion,
recheck every changed qualifying assertion against the final candidate and report any
remaining unverified contract rather than converting it into a success claim.
