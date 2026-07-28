# Design fidelity

When a Figma frame, screenshot, previous production UI, or specification is
the design basis, run intent preflight before implementation or browser
verification.

## Intent preflight

1. Summarize the instruction's expected result by viewport, state, and region.
2. Find the corresponding design frame/node. Decompose visible spacing across
   page/frame inset, container padding/gap, component padding, child
   margin/gap, and border/stroke; never assign total spacing to one property.
3. Compare `Instruction | Design basis | Spacing stack | Relation | Expected
   implementation | User decision | Status`. Relation is
   `same | different | unclear`; alignment Status is
   `confirmed | pending | Blocked`, never runtime Verdict.
4. For `same`, continue without reconfirmation to screenshot/image inspection.
5. For `different | unclear`, present mutually exclusive options. For each,
   state concrete viewport/region visibility, position, spacing, satisfied
   basis, and violated/deviated basis; ask one explicit choice.
6. Until an explicit answer, do not implement or launch a browser. Return
   `## Verdict: Blocked` without a screenshot because this is pre-session
   decision state. Silence is not approval.
7. Only an explicit approval can create a `documented deviation`; record its
   answer basis and scope. Otherwise follow the design basis or remain pending.

## Visual comparison

For a matching Figma frame, reproduce viewport, DPR, browser, font, assets, and
zoom, then use overlay or pixel diff.

Classify every difference `defect | documented deviation | unverifiable`.
Unexplained difference is `Fail`. A deviation records `region`, `difference`,
`reason`, and `basis`, including user confirmation or specification evidence.

With a design basis, always output `## Alignment`. `## Evidence` links the
design target, comparison screenshot, viewport conditions, and visual result;
the deviation matrix holds classifications. If the frame, spacing hierarchy,
or comparable conditions cannot be obtained after session start, do not guess:
return `Unverifiable`.

User-facing progress and receipt prose follows the user's language.
