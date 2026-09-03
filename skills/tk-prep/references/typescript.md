# TypeScript review

Read this only when JavaScript or TypeScript semantics are in review scope.

- At external request/response boundaries, verify field shape, nullability, conditional omission, and any runtime
  validation; declaration shape alone is not runtime proof.
- Check whether `any`, type assertions, non-null assertions, unchecked indexing, or optional access hides an invariant
  that callers can violate. Do not flag a value already narrowed by reachable control flow.
- Trace promises for floating rejection, `async forEach`, ordering, race, cancellation, and swallowed error behavior.
  Intentional fire-and-forget needs an explicit error owner.
- When compiler configuration changes, report only a demonstrated loss of safety in the touched build path.
- Use the repository's typecheck/lint command when safe and relevant. A missing tool or one command failure does not
  authorize a new dependency or end the rest of the review.
