# Interaction in archify pages

Read for an explicit interaction request. Keep the complete explanation in archify, with
prerequisites, causal steps, sources and material caveats outside controls. Read the installed
`references/explainer-authoring.md` and, for viewer-specific behavior, `references/viewer-runtime.md`.
Use supported directives and native diagrams; do not insert a TigerKit document shell,
hand-authored script, iframe or post-render patch that invalidates archify's receipt.

## Match the requested action

Use a native diagram with `@steps` for an ordered walkthrough, and native node/route links
for selection, focus and path exploration. Bind targets to real authored node/edge IDs.
The visible label, highlighted entity, step description and source must agree. Native
exploration reveals authored relationships; it does not run the represented application
or prove runtime causality. Preserve any actual spatial relationship with scene images;
do not replace live native controls with screenshots.

Check the installed version's documented capabilities before promising a custom action.
Archify 3.2.0 supports guided steps and viewer exploration, not arbitrary authored JavaScript
or parameter-driven simulation in an explainer. If a requested edit/reorder/calculation
cannot be represented faithfully, report that requirement as `Blocked` with the missing
capability. A static comparison may support the explanation, but cannot silently replace
requested live behavior or turn partial delivery into `Pass`. Do not auto-switch to the
legacy renderer, install/update a dependency or invoke a product-prototype workflow.

## Preserve meaning and verify

For a stateful comparison, preserve common inputs, entity identity, event order and actual
state history across alternatives; visible consequences must follow those inputs. Label
illustrative states and assumptions. A changed caption or highlighted node alone cannot
claim a recalculated result, persistent state change or a successful reset. Unsupported
custom input, branch-wide reset and backward replay remain unmet requirements.

Use the exact saved page for the owning skill's accuracy checks. When screen/action checks
are requested, route them to `tk-browser-verify`: exercise the requested native controls,
forward/back movement where supported, keyboard/focus, and the matching visible states.
Check no-JavaScript/reduced-motion reading when in scope. Keep the full static explanation
available and report any unrun checks. `finalize explainer` alone is not browser evidence.
