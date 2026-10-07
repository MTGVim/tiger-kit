# Human research report

Read when writing the final short-research report or a material persistent checkpoint projection.
Apply [clear writing](clear-writing.md), [HTML output](html-output.md) and Artifact Paths; reuse their
contracts directly without invoking another skill. Default to `.tigerkit/research/<slug>/report.html`,
or an explicit safe destination. The directory/report alone never starts a durable project.

Render only verified current facts from the interaction or canonical state/findings. HTML is a
readable projection, not an execution ledger or editable state UI; never recover authority or merge
edits back from HTML. Bind goal/research identity, evidence revision/date and projection freshness.
Check ownership before overwrite; atomically replace only this project's report and reread it.

Use [the offline template](../assets/report.html) as a minimal starting point, replacing illustrative
content and removing irrelevant sections rather than adding empty ceremony. Core content answers:
goal/downstream decision; recommendation/confidence/why; current stage; baseline and directions;
actual investigations/experiments and their links/verdicts; rejected alternatives and evidence versus
untested budget deferrals; unknowns/limits; next frontier/action and ready handoff candidates; sources.
Show meaningful changes in a timeline only when they exist. Preserve direction/experiment/source IDs
and relationships when relevant. A short report can combine these into a few sections. Label proposed
tests as proposed, never executed. Escape untrusted text/attributes, validate source links and use no
external assets, unsafe URL schemes, raw sensitive logs or HTML injection.

For persistent research, regenerate only after a material checkpoint/conclusion or evidence-producing
blocker. Unchanged resumes and no-action/no-delta runs preserve report bytes. A changed report cannot
make unchanged canonical facts fresh. Report failure leaves canonical facts intact and marks its
artifact branch `Unverifiable`; do not fall back outside the identified repository. Return the file
link and a concise conclusion without automatically opening a browser or changing user focus.
