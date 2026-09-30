# Shared Verification Contract

The skill owns acceptance, evidence and authority; the selected provider owns interaction.
Provider selection never weakens these requirements. Read before the first runtime observation.

## Acceptance and honesty

Bind each criterion to the exact candidate, target, environment, locale, role and inspected current
evidence. Use the owning skill's UI Evidence collection rules; accessible names, routes and action
success responses alone do not prove visible wording or final behavior. Observe the postcondition
independently after acting. If an action times out, inspect the resulting state before any retry;
never replay a possibly completed mutation blindly. Keep unresolved labels/connections itemized
with evidence, limitation and smallest missing input in QA, handoff and publication preparation.

Return `Pass | Fail | Blocked | Unverifiable` per criterion. Missing required evidence prevents
aggregate `Pass`. A successful baseline is capture-only: `phase: baseline`,
`baseline_capture: Pass`, `verification_complete: false`, and the exact `next_required`.
For a nested baseline also return `resume_parent: required`; the approved parent continues its
implementation. Only a complete after/acceptance phase may set `verification_complete: true`.
Return compact phase evidence to an active owner; never end its approved work at a child boundary.
Do not modify product/test/config source, Git state, or remote state as a verifier.

## Visual comparison

Visible-state claims require a non-empty, actually inspected runtime screenshot containing the
criterion and surrounding context. Direct trace/a11y/runtime evidence can prove nonvisual claims
without a ceremonial image. A render-affecting candidate, including a visual-preservation
refactor, requires comparable baseline/after evidence and a replay procedure bound to the same
candidate provenance, window/viewport, scale/DPR, zoom, fonts, UI state and capture boundary.
Declare nondeterministic exclusions before comparison; preserve immutable failure evidence
before any rerun. Missing provenance or comparable conditions is `Unverifiable`.

Classify every region before capture:

| Intent | Outline placement |
| --- | --- |
| appear | after target only |
| disappear | baseline target only |
| change | corresponding target in both |
| remain unchanged | none |

Judge intended changes separately from preserved regions. An unapproved preserved-region
difference is `Fail`. Inspect asset integrity, content, geometry/layout, typography, color/paint,
imagery, responsive/window sizing and state. Complete every applicable axis on the first attempt,
even after a mismatch; record reference/candidate/delta measurements for geometry and typography
where measurable. Disclose missing measurements; never invent tolerances or turn an unchecked
axis into `Pass`. Exact byte identity may discharge only a comparable, bounded, deterministic
region against its named already inspected baseline, never an unrelated full-screen capture.

Apply the owning surface's annotation mechanics. Browser targets use runtime element outlines;
native windows retain the raw capture and use a labeled annotated derivative with coordinates
mapped from the same capture. Annotation is evidence handling, not product behavior. Always
disclose it in `capture_only_mutation`; an annotated image cannot report `none`.
For a required visual pair, `visual_contract: applied` records completed applicable checks, not
acceptance by itself. An incomplete contract blocks `Pass` and completion. Use `n/a` only with
a reason proving that no visual/pair/render-affecting branch applies.

## Evidence and cleanup

Use the package's Artifact Paths checks before writing run-owned evidence. Record phase, run ID,
provider/version/host, observed input/profile semantics, candidate/build identity, per-criterion
facts, ordered capture paths/state/region/method/effective dimensions, auth mode without secrets,
baseline provenance/replay, visual contract, capture-only mutations, limitations and cleanup.
Keep failure captures separate from later after captures. Redact sensitive pixels before sharing;
exclude credentials, tokens, private screen content and unrelated identity from logs/preferences.
Close only run-owned resources; do not close or kill user apps, windows, profiles or processes.

Publication uses the package's producer-neutral image manifest only for represented `Pass`
criteria. Preserve required baseline/after pairs even when unchanged. Return evidence without
uploading it. Missing publication evidence remains `Blocked | Unverifiable`.
