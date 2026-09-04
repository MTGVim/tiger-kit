# Publication evidence handoff

Read this whenever a screenshot is captured or an inspected image may support PR review. This
verifier produces image-publication metadata only; it never uploads or publishes evidence. Direct
trace, accessibility-tree, DOM/runtime, and request/response evidence stays in the ordinary verifier
result and does not require an image manifest or a ceremonial screenshot.

## Exact display route

For every screenshot row, derive a `display_route` from the actual captured URL by removing only
the scheme, username/password, hostname, and port. Preserve the pathname, query, and fragment
exactly, including hash-router paths, dynamic development or verification fixture IDs, and
state-bearing values. Keep an environment label separate when local, preview, or staging context
matters.

Before returning or recording it, verify that the complete route is safe for the PR audience.
Dynamic IDs, query parameters, and fragments are not sensitive merely because they vary. Do not
mask, normalize, truncate, or substitute a value that a reviewer needs to land on the captured
view.

If the route contains an actual credential, token, session secret, signed parameter, personal
data, or another value unsafe for publication, omit the entire `display_route`. Do not create a
plausible but non-replayable masked route. State the reproduction limitation, and return
`Blocked | Unverifiable` when the claim requires an exact landing route. Secret-bearing URLs must
not be written to the evidence index or result.

## Producer-neutral manifest

When an inspected image materially supports a passing acceptance or regression-preservation claim,
return a producer-neutral PR evidence manifest entry with:

```text
evidence_required: true | false
evidence_kind: behavior | visual-change | visual-preservation
verification_status: Pass
criterion: <exact criterion>
artifacts:
  - role: baseline | after | acceptance
    path: <absolute inspected image path>
    display_route: <exact origin-free route | omitted with limitation>
    state_region: <captured state and region>
    viewport: <width x height, DPR, zoom>
    inspected: true
comparison: <not-applicable | byte-identical bounded region | inspected axes and result>
limitations: <none | exact limitation>
```

`behavior` means that the inspected image itself directly proves the behavior or visible final state;
it is not a wrapper for a trace or other non-image evidence. The schema contains no
implementation-controller or publication-skill fields. A consumer validates
generic required entries and does not need to recognize the producing skill. Keep run provenance
in the verifier result, outside the consumer branching contract.

Emit a publication manifest entry only when the represented criterion and image inspection are
`Pass`. For `Fail | Blocked | Unverifiable`, preserve any run-owned failure artifact under the
failure-evidence contract, return the real criterion status, and mark required image publication as
blocked or unverifiable. Never encode a failed or incomplete run as `verification_status: Pass`.

Set `evidence_required: true` when the inspected image materially supports acceptance or regression
preservation. Use `false` only for an inspected optional image that may help a reviewer but is not
needed to support a claim. Do not represent an absent or uninspected image as optional evidence.

For a visual `preserve` claim, return the representative baseline and after as a labeled pair and
set `evidence_kind: visual-preservation` plus `evidence_required: true`, even when the bounded files
are byte-identical or all inspected axes pass with declared nondeterministic exclusions. The pair
is the evidence for “no visual change”; never downgrade it to optional/N/A or return only `after`.

For multiple layout-context samples, include the bounded pairs needed to make the shared-component
claim reviewable and disclose known unrepresented contexts. Avoid an undifferentiated image dump.
