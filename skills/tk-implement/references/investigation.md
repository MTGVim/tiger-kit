# Unknown-cause failure investigation

Use this loop only for a bug whose cause is not established, an intermittent
failure, or a performance regression:

```text
feedback loop
→ reproduce
→ minimize
→ ranked hypotheses
→ instrument
→ fix
→ regression verification
→ original reproduction
→ cleanup
```

Create and run a fast, repeatable red-capable feedback loop before proposing a
patch. If the symptom cannot be reproduced faithfully, do not guess-patch;
record attempts and missing environment or artifacts as `Unverifiable`.

Minimize while preserving the symptom. Rank 3–5 hypotheses from observed
evidence, attach a falsifiable prediction to each, and change one variable per
probe. Patch only after evidence isolates the root cause.

When a correct public regression seam exists, capture the minimum reproduction
there and observe `red → fix → green → original reproduction`. When no useful
seam exists, do not add a shallow test or silently continue testless. Report
the missing seam, a possible seam change, and deterministic alternative
verification, then stop for the explicit exception decision required by
`tk-implement`. Remove temporary instrumentation and throwaway artifacts, then
rerun clean verification. Investigation never creates a separate commit; the
implementation-unit contract owns final review and commit.
