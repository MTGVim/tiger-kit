# Explanation selection

## Select known axes in order

Resolve three axes: technique, compatible format, then image style/aspect when relevant.
Reuse the current request and confirmed choices; skip every resolved axis. When all axes are
specified, announce the concrete treatment and generate without another question. Keep source,
feasibility and artifact checks. A request to compare subjects is not a request for variants.
Ordinary unspecified requests now wait for these selections rather than auto-picking a shortlist.
Do not ask abstract questions about learning style or intended use instead of naming techniques.

### 1. Show the whole catalog by theme

Show every technique below, including low-ranked and request-only choices, with stable IDs and
concrete names in the user's language. Mark one fitting recommendation per theme, with a short
reason and limitation; if none fits, state why and leave that theme without a recommendation.
Never hide/remove a technique because it lost an earlier comparison. Keep the full numbered menu
in readable chat; put theme recommendations in the input tool up to its actual choice capacity,
and explicitly accept any catalog ID typed in free text. Tool limits never truncate the catalog.
Do not dump internal renderer/schema names or ask which archify diagram grammar to use.

| Theme | Technique IDs and concrete names |
| --- | --- |
| Diagrams and evidence | 03 Real Output; 15 Before/After Comparison; 16 Concept Map; 26 Annotated Code; A Archify Panel Board |
| Stories and actors | 04 Zine Comic; 07 Group Chat; 08 Sketch Comedy (request-only); 10 Incident Postmortem |
| Participation | 02 Hands-on Simulator or Calculator; 09 Socratic Questions; 12 Choose-Your-Own Path; 19 Predict First; 20 Quiz; 21 Flashcards; 22 Invent Before Reveal; 23 Feynman Technique (request-only); 24 Hint Ladder |
| Correction and reference | 01 Five-Step Ladder; 06 Misconception Correction; 25 Cheat Sheet; 28 Failure Modes |
| Scenes and visual treatments | 05 Scrollytelling; 11 Illustrated Intuition; 18 Animated Metaphor; P1 Layout/style separation; P2 Design philosophy and restrained hierarchy; P3 Central scene; P4 Independent hand-drawn SVG |

Keep all original [30 entries](explanation-techniques.md) addressable. The six entries below
belong to another axis; show this compact relocation list with the catalog so none disappears:
13 Sequence Diagram and 14 Waterfall Timeline are diagram details, chosen from the content;
17 Infographic Poster, 27 Terminal Replay, 29 Slide Deck and 30 Social Thread are formats.
Accept an explicit ID at any axis and carry it forward; #30 stays request-only. Selecting #08,
#23 or #30 explicitly is the request that enables it; do not recommend them unsolicited.
A diagram-detail request constrains the automatic figure choice, not a second technique prompt.

### 2. Offer only compatible formats

Ask this after the technique is settled; never send technique and format questions concurrently.
Respect an explicit format (for example `이미지로`) and skip this question. If an explicit pair
conflicts, explain the lost requirement and ask only which bound requirement to change. Never
silently flatten interaction or rasterize exact code. With just one feasible format, announce it.

Use these stable format IDs in every format question: show both ID and concrete name and accept
the ID alone (for example `F1`). Filter to compatible choices without renumbering. `F` IDs are
format choices, independent of the unchanged technique/principle IDs `01`-`30`, `A`, `P1`-`P4`.

| Format ID | Concrete format |
| --- | --- |
| F1 | Offline HTML, interactive when the technique requires it |
| F2 | Precise static PNG |
| F3 | AI illustration (raster) |
| F4 | #17 Infographic Poster |
| F5 | #29 Slide Deck |
| F6 | Standalone SVG, animated only when explicitly selected |
| F7 | Video, only when explicitly selected |
| F8 | #27 Terminal Replay |
| F9 | #30 Social Thread (request-only) |

An ID resolves only its format axis; retain the selected technique and remaining style/aspect
question. Reject an incompatible ID with its lost requirement instead of silently remapping it.
Explicit legacy IDs #17/#27/#29/#30 and format names remain accepted aliases. F9 enables #30 only
when explicitly requested; do not offer it unsolicited. F4/F5 are compositions rather than a
request to replace their facts with AI-generated text; infer their compatible rendering route.

| Selected requirement | Compatible formats / exclusions |
| --- | --- |
| Participation (#02, #09, #12, #19-#24, including request-only #23) | F1 only, interactive offline HTML; native disclosure/links and a static no-JS reading path. No still image/video/slide replacement. |
| A Archify Panel Board or #05 Scrollytelling | F1 preserving the actual board or scroll behavior; do not replace the defining form with a still image. |
| P4 Independent hand-drawn SVG | F6 or F1 containing the actual vector sketch; an AI raster is a different treatment, not this SVG execution. |
| Exact code or command output (#26, #27, or another technique whose claim needs exact source bytes) | F1 selectable-text HTML, or explicit F8 terminal replay. Exclude F3 AI raster illustration. |
| General static explanation | F1, F2, F3 and fitting explicit F4/F5; choose only options that preserve the needed facts. |
| Motion essential (#18) | F1 live HTML or explicitly selected F6 animated SVG/F7 video, with static equivalent. A still image cannot satisfy motion. |
| #30 Social Thread | F9 request-only separate sharing summary, retaining a link/reference to the full explanation; never auto-select it. |

For an unspecified single HTML without a technique-specific form, archify remains the page
renderer. A choice of HTML is not a choice of image style; do not ask a third question for HTML.
#13/#14 diagram detail, archify type, chart type and layout are inferred from evidence, not user
menu axes. Preserve an explicit correct detail without requiring another selection.
The PR/issue summary PNG destination remains a resolved format under its own contract.

### 3. Confirm image style and aspect only when needed

For AI illustration, read [raster illustration](raster-illustration.md). Show the automatically
chosen information layout as a concrete composition alongside 3-4 suitable style treatments and
`알아서`, plus only unresolved aspect choices. This confirms layout×style/aspect without asking
users to choose an internal layout taxonomy. Existing explicit choices win. If an axis has zero
or one feasible choice, report the decision/limit instead of asking; with multiple choices, wait
for the answer. If the input tool has fewer slots, keep the full numbered options in chat and
accept typed IDs; never silently pick a missing answer. “Choose for me” delegates only that axis.
Precise static PNG/SVG uses applicable style/aspect choices without invoking AI raster generation;
HTML has no third-round image question. The raster reference owns prompt persistence and checks.

### Context-bound evaluation influence

Only authorized, relevant external preference evidence may reorder choices inside a theme.
When used, show topic type, number of evaluated comparisons/topics and evaluator count alongside
the observed result; distinguish match wins/reached round from a cardinal score. Unknown counts
stay unknown. The supplied 19-candidate, one-PR, one-evaluator tournament is one comparison,
not 19 independent ratings and not general superiority. Its unidentified first-round losers do
not justify inventing a per-technique ranking. Keep all entries visible and request-only status.
Use the consent rules below before saving any result or reason; this menu creates no memory store.

## Archify panel board

Include one additional choice alongside the original 30-entry catalog and four principles: **archify panel
board** (conclusion first, native diagrams, table panels). Use it for an ordinary single page
without a technique-specific form or when explicitly selected. Its fixed panel grammar cannot
express arbitrary HTML treatments. A request for a particular form takes precedence; requested
variant sets include at most one archify panel board, not repeated boards with different wording.

## Four available distilled principles

Always include these in the selection pool. No further trial or favorable evaluation is a
condition of availability. When combined with an existing technique, retain the principle's name
and source as a separately selectable treatment; do not collapse all four into “infographic.”
Each is a partial adaptation, not the original skill's formal execution or a replacement for it. An HTML/SVG treatment
using one of these principles is not an original upstream output. For an original-like AI
illustration, select the raster route; the independent SVG option remains explicitly a sketch,
never an Excalidraw export or a substitute for requested raster art.

| Choice / source | Apply when | Limitation |
| --- | --- | --- |
| Layout/style separation, from `baoyu-infographic` | First map the information order and relationships, then choose a visual treatment independently. Useful for a process whose structure must survive style changes. | A style cannot establish sequence, causality or a measurement; use raster generation for an original-like illustrated output; HTML/SVG-only adaptation is a different output. |
| Design philosophy and restrained hierarchy, from `canvas-design` | State a brief visual intent for emphasis, spacing and grouping, then use a few clear levels to expose the main relationship. | Restraint cannot delete prerequisites, qualifications or causal steps; this is explanation, not an art-only text quota. |
| Central scene, from `Epic Infographics` | Put a concrete subject or mechanism at the center and attach verified facts to the relevant parts, with a legible reading path. | Decorative atmosphere must not imply unsupported dimensions, magnitude or causality; a scene is not mandatory for every subject. |
| Independent hand-drawn SVG, contrasted with `Excalidraw` | Use original slightly irregular strokes, simple shapes and legible labels for an approachable spatial or conceptual sketch. | This is independently authored SVG, not an Excalidraw export, editor integration or fidelity claim; rough strokes must not distort geometry or arrows. |

Sources, exact revisions, keep/adapt/omit decisions, license and evidence limits are recorded in
[selection provenance](sources.md#explanation-selection-and-four-principles-2026-10-30).
Do not fetch upstream at explanation runtime. Reuse the current renderer and figure contracts:
Archify owns only the selected panel-board branch and its native diagrams/interactions.
Technique-specific HTML follows the common renderer contract and may embed original inline SVG;
figures entering archify still use scene-figure restrictions and PNG conversion for `@image`. The PR/issue summary
PNG route stays the default for that destination, and explicit standalone SVG/video keeps its
own route. No principle skips source, author, accuracy, accessibility or offline checks.
Use an available image tool only when raster generation is actually selected and authorized;
do not claim that these principles remove image-generation dependencies. Unavailable/failed
generation is a disclosed failure, not a successful image or a silently substituted original skill.

## Requested variants

An explicit request to compare explanation techniques/treatments permits up to five suitable
variants. An explicit request for broad exploration, including a request for fifteen treatments,
permits up to fifteen. These are ceilings, not quotas. A request to compare two subjects in one
explanation does not select either branch. Ordinary explanation never starts a gallery.
For exploration, select the requested suitable treatments from the complete catalog and show
each choice's reason and limitation before generation; do not reopen already specified axes. Preserve an explicit smaller requested count.
Disclose fewer fitting choices, tool/cost limits and failed variants without inventing coverage.

Use the same run `evidence.md` for all variants: essential facts, source bindings, inputs,
conditions and known limits. For each final variant separately verify factual coverage, units,
causal/spatial relationships and all rendered text against that evidence. Check for missing
conditions even when another variant is correct. Keep the same necessary facts while varying
presentation; do not fill source gaps for visual symmetry. Perform the applicable author check,
renderer/static gates and accuracy review on each candidate's final bytes, not one representative.

Before comparison, inspect each variant's **form fidelity**, not just its facts. Name its
core form (for example dialogue bubbles, crossed-out misconception, a `<details>` answer,
fixed figure, scroll-linked step emphasis or inline SVG) and verify that it actually exists
and remains usable in the chosen renderer. Different panel order or prose alone is not a
technique distinction. If the renderer cannot express that form, mark the variant `limited`,
name the lost behavior and notify the user before starting comparison. Keep it out of a
fully implemented technique set; do not silently substitute a list/next panel or claim success.
A disclosed limited candidate may enter evaluation only when the user explicitly accepts it.
Keep factual and form checks separate; all steps and core facts must remain readable without JS.

Before evaluation, show the technique names/reasons/limits but keep the mapping to anonymous
samples private. Explain that visual style may still allow guessing. Hand generated candidates,
their actual success/failure states and the private mapping to `tk-blind-comparison`; read its
current invocation/manifest contract rather than inventing flags or copying its protocol here.
That owner evaluates existing candidates and owns gallery/versus/delivery/privacy contracts;
it does not generate variants. Use that owner's embedded-self-evaluation or separate-distribution key contract and disclose
sample identity only through its explicit reveal flow. Keep a separate key private when that
delivery mode is selected; an embedded key is encoded and validated, not visible before reveal. Do not leak it through filenames,
captions, metadata or recommendation ordering. If the owner is unavailable, report the blocked
evaluation instead of claiming a blind gallery or constructing a replacement evaluation UI.

## Consent-based external preferences

The current request wins over remembered preferences. Use only relevant preferences the user
authorized for reuse, and retain their topic/audience/context limits. A rating is an observation,
not evidence of its cause or a permanent trait. One evaluator on one topic does not establish
general superiority; earlier baoyu/canvas examples were reference-based adaptations, not formal
upstream executions, and two trials used the built-in image generator.

After actual evaluation, offer saving only if useful and unanswered. Show the exact proposed
record and the available external memory owner/destination before asking for consent. Separate:
- context: topic, audience, task and compared treatments, with the scope of future reuse;
- observations: actual scores, choices and sample identity after authorized reveal;
- reasons: only what the user stated and confirmed, distinct from any unconfirmed hypothesis.

Confirm an ambiguous reason before proposing it as fact. Approval of generation, scoring,
exporting evaluation records or this-run choices is not approval of durable preference storage.
No consent or no user-approvable external provider means no preference writes: say so briefly
and keep any preference inference within the current conversation only. Do not create a TigerKit
memory backend, settings fallback or hidden preference file. Requested evidence/score exports
remain evaluation artifacts, not automatic cross-run recommendation memory.

With explicit consent to the exact record, destination and reuse scope, delegate the bounded
save to the available external memory owner under its supported contract. Confirm the outcome;
unsupported or failed writes are not saved preferences. Later correction/deletion uses that same
owner's current capabilities and user authority; report unsupported actions without promising
erasure or silently writing a contradictory replacement. A refusal is not itself a preference
to persist. Do not automatically write scores, explanations, inferred reasons or raw session logs.
