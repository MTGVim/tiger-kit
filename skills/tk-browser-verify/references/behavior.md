# Behavior verification

## Exact target and trusted input

Identify the exact control. If it is missing, inspect the mode, tab, scroll, and toggle
state instead of repeatedly searching for a button with a similar label.

Choose side-effect-free controls for click-delivery comparisons. Before any clipboard,
file or notification write, apply [user shared-state safety](verification.md#user-shared-state);
headless input does not isolate the user's system clipboard or files.

Use provider-native trusted pointer and keyboard APIs. Use `evaluate_script` only to
observe state, computed values, or coordinates. Never treat `element.click()`,
`form.submit()`, or `dispatchEvent()` as interaction evidence.

Enter form values through trusted keyboard input and operate native date/select controls through
their visible keyboard or pointer behavior. Do not assign DOM values or use scripted input that may
bypass constraints such as `maxLength` or fail to exercise native control behavior. If a provider's
`fill` operation is used, first establish that it produces user-equivalent trusted input and honors
the control's constraints; otherwise type through the keyboard. Inspect the resulting visible value
and, for save flows, the captured request body.

A mutation claim requires the related network request and response. Acceptance
verification connects the UI transition, request/response, and final UI state in one
flow. A response, toast, or local DOM change alone is insufficient.

For native HTML drag-and-drop controls such as SortableJS, enable CDP
`Input.setInterceptDrags`, press and move from the handle to obtain the intercepted drag
data, then use `Input.dispatchDragEvent` with `dragEnter`, `dragOver`, and `drop` at the
target. For a closed native `<select>` that ignores trusted keyboard selection in headless
mode, set the option value and dispatch `change` only as a documented input limitation;
verify the resulting request and UI state independently, and do not describe this workaround
as trusted user input.

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

For native date pickers, use trusted pointer input to select the date; do not set the control
value through DOM evaluation and count that as interaction evidence.
