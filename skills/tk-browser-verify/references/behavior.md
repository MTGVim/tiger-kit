# Behavior verification

## Exact target and trusted input

Identify the exact control. If it is missing, inspect mode, tab, scroll, and
toggle state instead of iterating over similarly labeled buttons.

Use provider-native trusted pointer and keyboard APIs. Use `evaluate_script`
only to observe state, computed values, and coordinates; never treat
`element.click()`, `form.submit()`, or `dispatchEvent()` as interaction
evidence.

A mutation claim requires the related network request and response. Acceptance
verification links UI transition, request/response, and final UI state in one flow.
A response, toast, or local DOM change alone is insufficient.

## Gated states and dialogs

When UI appears only for a particular API state, prefer an `initScript`
response mock over real sending or saving. Match the envelope actually parsed
by the application; inspect source mapping instead of guessing shape.

Install native alert/confirm handlers before interaction. If a blocking dialog
is already open, accept or dismiss it before continuing.

## Motion

Do not infer absent animation from CDP round-trip snapshots. Before the
trigger, register `animationstart`, `animationend`, `transitionstart`,
`transitionend`, and any required `MutationObserver`; then inspect one event
timeline after trusted input.

Synthetic DOM probes are valid only for pure CSS calculation. When framework
mount/unmount lifecycle matters, verify replay through a real component render
cycle.

## Field clearing

Confirm whether provider `fill(uid, "")` clears the value. If empty fill is a
no-op, fill a nonempty value and use trusted Backspace, or send one Backspace
per actual character from the field end. Reobserve an empty value before save.
