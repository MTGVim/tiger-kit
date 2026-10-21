# Tutorial input displays

Use only when the selected video needs cursor, click, key or region displays. Evaluate this
package's [capture overlay](../scripts/capture_overlay.js) in the already selected provider's
page context. It injects an isolated, pointer-transparent, aria-hidden shadow layer; product
source stays untouched. Record `capture_only_mutation`, its installation/removal and limitations
in capture provenance. Full navigation needs reinjection; SPA navigation does not.

The helper follows mouse moves, animates clicks and shows keycaps beside the cursor, clamped
to the viewport. Letters within 900ms group; repeated special keys show `×n`; displays expire
after 1.8s. Password, OTP, card-number and `[data-tigerkit-sensitive]` targets mask their labels
before DOM/grouping state; opaque custom-element targets are also masked. Other private fields require existing redaction or disabling input
displays; this helper does not certify a page safe to publish.

`window.__tigerkitCapture.highlight(element)` marks a measured element rectangle;
`clear()` clears highlights. Refresh them after scrolling/layout changes. Before a cropped
scene, first mark its region in the full view. `remove()` releases all owned nodes, listeners
and timers; verify removal before an assertion screenshot and on every capture exit, even failure.
No overlay frame substitutes for that independent screenshot.

Use the provider's actual input API. On an already approved CDP surface, interpolate
`Input.dispatchMouseEvent` mouse moves over roughly 500-1500ms (about 30ms steps), then pause
briefly before the press/release at a freshly measured target center. Do not use DOM `.click()`
as proof of real pointer input. Character `Input.dispatchKeyEvent` uses `keyDown` with `text`;
special keys use `rawKeyDown`, followed by `keyUp`. `Input.insertText`/IME does not produce the
same keydown sequence: use `text(approvedPublicLiteral, target)` only when a visible label is
needed, never read or echo a secret field. Composition events are otherwise omitted.

For segmented inputs such as `type=time`, establish focus and the intended initial segment
from current provider behavior before sending keys; do not rely on a click offset or a fixed
arrow sequence across locales. Privately assert the resulting value immediately and stop on
mismatch. Record only publication-safe observed values. Use one clock for scene/frame times,
normalizing all timestamps to the first frame; wait only the remainder of a measured narration
hold after actions, rather than adding the full hold again. Deliberate waits are not latency proof.
