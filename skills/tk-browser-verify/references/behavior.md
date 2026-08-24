# Behavior verification

## Exact target and trusted input

Identify the exact control. If it is missing, inspect the mode, tab, scroll, and toggle
state instead of repeatedly searching for a button with a similar label.

Use provider-native trusted pointer and keyboard APIs. Use `evaluate_script` only to
observe state, computed values, or coordinates. Never treat `element.click()`,
`form.submit()`, or `dispatchEvent()` as interaction evidence.

A mutation claim requires the related network request and response. Acceptance
verification connects the UI transition, request/response, and final UI state in one
flow. A response, toast, or local DOM change alone is insufficient.

## Conditional state and dialogs

When UI appears only for a particular API state, prefer an `initScript` response mock
over a real send or save. Match the envelope the application actually parses; inspect
the source mapping instead of guessing the shape.

Install native alert/confirm handlers before interaction. If a blocking dialog is
already open, accept or dismiss it before continuing.

## Motion

Do not infer that no animation exists merely because a CDP round-trip snapshot omits
it. Before the trigger, register `animationstart`, `animationend`, `transitionstart`,
`transitionend`, and any required `MutationObserver`; then inspect one event timeline
after trusted input.

A synthetic DOM probe is valid only for pure CSS calculations. When framework
mount/unmount lifecycle matters, verify a replay through the real component render
cycle.

## Clearing fields

Verify that provider `fill(uid, "")` clears the value. If an empty fill is a no-op,
fill a nonempty value and use trusted Backspace, or send one Backspace per actual
character from the end of the field. Observe the empty value again before saving.
