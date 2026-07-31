# Visual verification

## Runtime evidence

Every Guard and Verdict run requires at least one non-empty inspected
screenshot. Guard visual/layout/style claims also require the necessary
computed state; pure network/DOM exploration does not satisfy the screenshot
contract. If entry flow is unstable and only CSS behavior matters, a
DOM-injected element may use exact production classes, but label the bypass.

After a browser session starts, capture and actually inspect every success,
failure, and runtime-blocked final state. Capture without image analysis is not
evidence and makes the result `Unverifiable`. A pre-session block that cannot
start a safe browser cannot produce a product screenshot; record
`Evidence directory: unavailable` and `Unverifiable` rather than inventing an
image.

## Instrumented evidence

Guard and Verdict permit temporary instrumentation only when the state is
behind an auth gate and occurs solely through an unstable external call, or
when an auto-release timer makes its observation window shorter than the tool
round trip. Verdict records `Evidence class: instrumented` and the reason.

Use this minimum-intrusion order and record why each earlier route is
impossible:

1. existing DOM/class/state toggle with no source change;
2. isolated DOM injection using exact production classes;
3. temporary source instrumentation.

When a timer clears the state before observation, expose a hold variant as
well as the normal setter. Bound source instrumentation with a
`TEMP(<ticket-or-run-id>)` marker. After observation restore it and measure all
three: target-file diff equals the pre-instrumentation state, marker search is
zero, and no marker/instrumentation delta exists in a commit. Any unknown check
returns `Residue check: unverifiable` and overall `Unverifiable`.

User-observed evidence is allowed only when a nondeterministic driver prevents
agent reproduction. Record `Evidence class: user-observed`,
`Computed: not recorded`, and the delegation reason; never report it as
agent-measured computed evidence. Do not delegate when direct observation is
cheap.

## Runtime diagnosis and controls

Attach `change-related | pre-existing | environment` to every runtime `Fail`.
Use `pre-existing` only after reproducing the same procedure on a deployed or
baseline branch. Without baseline access, leave origin unverified.

When declared and computed values differ, inspect `document.styleSheets` and
identify the winning selector and `cssText` before blaming component logic. If
an ancestor state class wins, measure whether runtime removes it. A DOM
simulator such as jsdom that does not implement CSS specificity is not a
cascade oracle.

A causal-fix Verdict requires positive and negative controls in the same
runtime. Do not revert production code: inject the old CSS selector with a
probe, or call the old logic as a separate function with the same input.
Remove injection through the instrumented residue gate. If negative control
does not reproduce failure, report the causal explanation `Unverifiable` and
do not use it as `Pass` evidence.

## Viewport and hover

Verdict defaults to widths `500, 800, 1200, 1600, 1920, 2400`px. Add `375` or
`390` below 500px when supported. For breakpoint `b`, add `b-1`, `b`, `b+1`.
Guard checks only requested state and width.

Measure `window.innerWidth` before judging a breakpoint. If it differs, reset
past the boundary. Measure hover-dependent CSS after trusted hover, not from
rest-state computed values.

At each Verdict width inspect overflow, clipping, overlap, wrapping,
truncation, alignment, spacing, sticky/fixed elements, and off-screen controls.

## Migration baseline

For component/primitive replacement, compare all affected axes such as
`fontWeight`, `fontSize`, `borderRadius`, `justifyContent`, and `padding`, not
only color and size. Include content-width and full-width/stretch consumers.
Before comparing rem values, verify equal root font size.

## Evidence

Guard and Verdict `## Evidence` records the absolute evidence directory, width
when applicable, screenshot path, and visual result.
Missing width/screenshot/analysis belongs in `## Unverified`. Link every
finding to an observed image; irrelevant captures are not evidence.

User-facing progress and receipt prose follows the user's language.
