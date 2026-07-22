# Unknown-cause failure investigation

Use this loop only when the implementation input is a bug whose cause is not yet established, an intermittent failure, or a performance regression:

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

Create a fast, repeatable red-capable feedback loop and run it before proposing a patch. If the symptom cannot be reproduced faithfully, do not guess-patch; record attempts and missing environment or artifacts as `Unverifiable`.

Minimize while preserving the symptom. Rank 3–5 hypotheses from observed evidence, attach a falsifiable prediction to each, and change one variable per probe. Patch only after evidence isolates the root cause.

When a correct public regression seam exists, capture the minimum reproduction there and observe `red → fix → green → original reproduction`. When no useful seam exists, do not add a shallow test; report the missing seam and another verification route. Remove temporary instrumentation and throwaway artifacts, then rerun clean verification. Investigation inside `tk-implement` never creates a separate commit; the implementation contract owns final review and commit.
