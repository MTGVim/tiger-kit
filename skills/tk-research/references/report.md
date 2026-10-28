# Human research report

Before drafting, read [clear writing](clear-writing.md), [documentation purpose](diataxis.md)
and [renderer contract](renderer-contract.md). The report informs a concrete decision, not
an obligatory tutorial. Use archify for every new or materially updated report, including
supported native interactions. Do not use `render_report.py`, `build_html.py` or the legacy
`assets/report.html`; shared specialized UI assets do not select a research renderer.

## Content and sources

Render verified current facts from the interaction or canonical state/findings. Lead with
the conclusion, confidence and deciding conditions. Cover the goal and downstream decision,
strongest evidence, baseline and alternatives, actual investigations/experiments and their
verdicts, rejected tested directions versus untested budget deferrals, unknowns and limits,
conditions that would reverse the conclusion, and the next frontier or action. Include the
smallest plausible implementation scope and cost of doing nothing when material. Preserve
source, direction, experiment and finding IDs; a proposal is not an executed test.

Keep the report coherent and conversational. Short reports can combine related facts into
few panels; never create empty categories, duplicate views or a document-mode selector.
Keep observations, inference and examples distinct. Explain unknowns where they affect the
decision, and derive recommended procedures from inspected evidence or label them proposals.
Do not add comprehension quizzes; `tk-explain` owns learning checks.

Author `candidate.archify.md` under `.tigerkit/tmp/tk-research/<run-id>/` using the installed
archify authoring reference. Use a conclusion and panels for evidence, alternatives, limits,
next action, and actual verification; stable IDs bind the readable projection to its sources.
Declare each source with `@source` and cite it beside the supported claim using archify's
`source:id` inline-link syntax. Preserve revision/access date and research identity
in readable scope/evidence text. Use verified URLs or pinned repository positions. If a
source is unavailable, say so; a reachable link alone does not verify its claim. Code excerpts
must resolve at the pinned revision. Never fabricate a source or turn raw private logs into
report content. Preserve negative results and contradictions.

Use native diagrams and `@steps` when relationships or event order explain the conclusion;
use comparisons for alternatives. For requested live behavior, read
[interactive examples](interactive-examples.md) and verify actual archify support. For a
spatial figure that native diagrams cannot express, read [scene figures](scene-figures.md)
and embed its converted PNG with `@image`, alt text and a caption. Do not turn native
interactive diagrams into pictures or use image generation to invent measured evidence.

## Delivery and checks

Apply Artifact Paths. Default to `.tigerkit/research/<slug>/report.html`, or an explicit safe
destination. The directory/report alone never starts durable research. HTML is a readable
projection, never the execution ledger, authority or canonical editable state. Check
ownership before replacing only this project's report. Keep an existing valid report until
a passing candidate is ready; stage rendering under the run directory before atomic replacement.

Run archify's complete `finalize explainer` command as specified in the renderer contract.
The final file must open alone, with no external runtime requests; clickable source links
are allowed. Retain the candidate and receipt bound to its final bytes. Inspect conclusion,
claim-source links, quantities, IDs and coverage after rendering; the renderer does not
prove factual accuracy. A failed/missing renderer or unsupported required interaction is
not report success and never authorizes fallback to the old document template.

Include separate outcomes for static/artifact checks and screen/action checks in the
verification panel. `finalize` does not run a browser. Use `tk-browser-verify` when the user
requests screen checks or a material visual/interaction uncertainty requires them; report
unrun checks honestly as not requested or unavailable, as applicable. Never assert theme,
keyboard, navigation or interaction success from a static receipt alone.

The first short-research conclusion or material persistent checkpoint must provide a
current decision-ready report unless the user requested no files. Missing rendering leaves
findings intact: report the artifact branch as `Blocked | Unverifiable` and give the useful
conclusion in chat. Later `NO-ACTION | NO-DELTA` runs preserve existing report bytes; changing
a report cannot make unchanged canonical facts fresh. Return its link and concise conclusion
without opening a browser or changing user focus.

## Persistent-project coverage

Project the whole project, not only the latest batch. Reconcile canonical IDs/counts for
all findings, experiments and handoffs before replacement. Preserve meaningful progress,
evidence, verdicts, rejected directions, waiting/reopen conditions and approval status.
Use readable panels/tables instead of requiring unsupported raw HTML or collapsing away
essential results. Missing/duplicate records fail coverage acceptance; an upstream page
limit must not silently drop evidence. Keep current content within a supported layout or
report the exact remaining limit, preserving the previous artifact.

Show a decision timeline only when recorded evidence actually changed a judgment; link the
prior assessment, new evidence, resulting conclusion and consequence with known dates/IDs.
Do not invent earlier opinions or chronology from source order. If only final findings are
known, use a comparison or evidence-to-conclusion map. Prefer a small run-owned generator
from canonical inputs when needed; edit its source and regenerate, never recover state or
authority from report HTML. Existing user reports and research homes remain in place.
