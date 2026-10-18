# Human research report

Before drafting, read [clear writing](clear-writing.md) and this report contract. Consult only the relevant
[technique entry](explanation-techniques.md) for a requested or unfamiliar format. The renderer reads the complete
offline template for you, so do not load `assets/report.html` or the full shared HTML reference.

Read when writing the final short-research report or a material persistent checkpoint projection.
Apply [clear writing](clear-writing.md) and Artifact Paths; reuse their contracts directly without
invoking another skill. Default to `.tigerkit/research/<slug>/report.html`, or an explicit safe
destination. The directory/report alone never starts a durable project.
When a verified structure, flow, timeline or comparison relationship is clearer in a figure
than prose/table, read [visual grammar](visual-grammar.md). Do not add decorative diagrams.

Render only verified current facts from the interaction or canonical state/findings. HTML is a
readable projection, not an execution ledger or editable state UI; never recover authority or merge
edits back from HTML. Bind goal/research identity, evidence revision/date and projection freshness.
Check ownership before overwrite; atomically replace only this project's report and reread it.

Write one coherent report; prose and tables need no technique assignment. Never add duplicate
views, hidden tabs or a document-mode selector. Use a clear conversational voice by default and
preserve evidence, uncertainty, confidence, limitations and next actions in the same document.

Render through `scripts/render_report.py`. Author a JSON content file with this shape:

```json
{
  "title": "Subject and conclusion",
  "topbar_title": "Short reader-facing conclusion",
  "meta": "Evidence date, scope and revision",
  "sections": [
    {"id": "overview", "title": "목표와 결론", "html": "<p>...</p>"},
    {"id": "verification", "title": "검증 및 예외", "html": "<ul>...</ul>"}
  ],
  "sources": [
    {"id": "ref-1", "title": "Source title", "url": "https://example.test/source",
     "local_path": "", "date": "2026-01-01", "revision": "v1",
     "link_unavailable": false, "citations": ["cite-1"]}
  ],
  "extra_css": ""
}
```

Include `overview` and `verification` sections. Add any other relevant sections as `{id, title,
html}` objects; section HTML is a fragment, not a complete page. Put each citation in that content as
`<sup id="cite-1"><a href="#ref-1">[1]</a></sup>` and list the matching citation ID under its
source; the renderer creates reference entries, return links, and the table of contents. Use a
verified HTTPS URL, a local path, or set `link_unavailable` to `true`; the checker warns when all
three are absent. The renderer escapes title, section-title, source and metadata fields, selects the
theme from the user settings (an explicit request wins), and copies the offline shell, navigation,
theme control, scripts and footer. `extra_css` is optional local CSS; the checker rejects network
references and altered scripts. Report any theme-settings bootstrap or invalid-settings warning in
the completion summary.

Run the renderer and then run the package-local checker against the saved output. Preserve the
renderer-owned document shell and replace content only through the declared fields. Long reports
include both navigation structures; the renderer keeps them for short reports too.
The report is decision-ready
at the evidence available now, including the first material persistent checkpoint: it should let the
reader decide whether more research is needed, whether a candidate should become implementation work,
or whether to stop. Core content answers: goal/downstream decision; recommendation/confidence/why;
the strongest evidence; assumptions or evidence that could reverse the recommendation; current stage;
baseline and directions; actual investigations/experiments and their links/verdicts; rejected alternatives
and evidence versus untested budget deferrals; unknowns/limits; the smallest plausible implementation
scope if the recommendation is accepted; the consequence of doing nothing when material; next
frontier/action and ready handoff candidates; sources. Do not add a comprehension quiz by default:
`tk-explain` and `tk-teach` own teaching checks, while this report owns decision readiness.
Show meaningful changes in a timeline only when they exist. Preserve direction/experiment/source IDs
and relationships when relevant. A short report can combine these into a few sections. Label proposed
tests as proposed, never executed. Escape untrusted text/attributes, validate source links and use no
external assets, unsafe URL schemes, raw sensitive logs or HTML injection.

Before reporting the report artifact as successful, run the package-local checker against the saved
file and fix every failure:

    python3 <package>/scripts/render_report.py --input /path/to/report-content.json --output /path/to/report.html
    python3 <package>/scripts/check_report.py /path/to/report.html

The checker verifies that the table of contents links to every section, movement controls link to
the top and bottom, local fragments resolve, citations link to reference entries with return links,
URL schemes are safe, runtime HTML/CSS resources and common JavaScript network APIs are absent, and
the footer has a positive AI-authorship notice. Safe source hyperlinks remain allowed. It does not
establish screen behavior. Use tk-browser-verify for the
template's navigation, links, keyboard, no-JavaScript and reduced-motion checks. If the verifier or
render environment is unavailable, record the screen result as Unverifiable with the reason in the
`검증 및 예외` section and in the completion response.

For persistent research, regenerate only after a material checkpoint/conclusion or evidence-producing
blocker. Unchanged resumes and no-action/no-delta runs preserve report bytes. A changed report cannot
make unchanged canonical facts fresh. Report failure leaves canonical facts intact and marks its
artifact branch `Unverifiable`; do not fall back outside the identified repository. Return the file
link and a concise conclusion without automatically opening a browser or changing user focus.

## Evidence-backed decision evolution

When the research has actual recorded changes of assessment, show a compact decision
timeline only if it helps the reader understand the recommendation. Each stop links
the prior assessment, newly verified evidence, resulting changed judgment and its
consequence. Preserve source IDs, experiment/decision dates when recorded, and whether
a claim is observed, inferred or proposed. Do not infer an earlier opinion from the
final recommendation or convert the order of sources into the order of decisions.

When only final findings are known, prefer a candidate comparison or evidence-to-conclusion
map, not a fabricated chronological narrative. Distinguish candidate exclusion from
untested budget deferral and maintain the report's core evidence and limitations.
Use brief content-specific headings and captions under `clear-writing.md`; optional
semantic emoji in chat summaries must not be imported as decorative HTML requirements.
Reuse the existing `visual-grammar.md` and offline verification requirements.

## Persistent-project coverage

Project the whole research project, never only its latest batch or a paragraph replacing earlier
checkpoints. Include meaningful progress history, every finding and experiment with ID, topic,
verdict and expandable reader-written evidence, rejected tested directions separately from untested
deferrals, waiting/reopen conditions, and handoff/approval status. Keep essential conclusions expanded.
Before replacement, reconcile findings, experiments and handoffs against canonical IDs and counts;
missing or duplicate records fail report acceptance. State the reconciled coverage in the report.
Prefer a small run-owned generator reading canonical inputs. Edit that generator/template and
regenerate instead of patching its output; HTML never becomes canonical research state.
