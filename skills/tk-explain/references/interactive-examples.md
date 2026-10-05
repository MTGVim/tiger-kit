# Interactive Examples and Controlled Mechanisms

Read only when a concept's cause and effect depends on input, identity, state, or event order. Follow [HTML output](html-output.md); use inline HTML/CSS/SVG/JavaScript without a framework, build step, server, or runtime network dependency. This reference adds no course, research, product-prototype, or video-rendering responsibility.

## Let the reader cause the difference

Choose the smallest useful experiment: edit a value, reorder items, toggle a condition, or trigger an event. For stateful concepts, include an editable local state and a separate causal change; fixed initial values plus an outcome selector cannot test state retention. Give one short experiment instruction, such as predict the outcome, change the input, then compare what actually happened. Every instruction must correspond to a working control. Keep prerequisites, mechanism, and material caveats beside the experiment rather than replacing them with controls.

Use the shared pure `model(settings)` result for diagrams, values, and explanatory sentences. Keep independent inputs and genuine state history in `settings`; calculate derived labels, mappings, and conclusions together. Generate the conclusion from the current result, rather than hardcoding one example behind a generic changed/not-changed flag. A stateful mechanism must preserve relevant history across events, rather than silently recalculating local state from the current item data. Clearly distinguish data identity, persistent state, and display position when those differ. Label a simplified model and its assumptions; do not imply that it executes the real library or measures its runtime.

Keep the small set of causally useful controls. Use native labeled controls and predictable keyboard behavior. Render user-entered text as text, never as unescaped HTML. Preserve the focused control across updates, including repeated button activation as well as an input's caret; replacing its entire container must not drop keyboard focus.

Build the baseline diagram, values, and conclusion as static HTML before adding JavaScript. Do not leave empty containers that only `render()` fills. Start interactive controls hidden and baseline input fields read-only; reveal/enable them after their handlers are attached. Enforce `[hidden] { display: none !important; }` when a control's layout rule sets `display`, since that rule can override the browser's hidden styling. With JavaScript disabled, the example must still show a meaningful outcome and no inert experiment controls. Test the actual script-disabled render separately; finding `hidden` in the source is not proof that a control is invisible.

## Show intermediate steps when they teach the mechanism

For identity/history mechanisms, protocols, or algorithms with meaningfully distinct intermediate states, provide both direct experimentation and a manual sequence starting paused, with previous/next, current step or progress, and reset. Derive the visible entities, connections, and state ownership from the current stage, so an initial stage does not already display the final matching/state result. An order-reversal button is a data action, not a substitute for mechanism steps. Show what changes and why at each step. Animate the causal transition or match, not an unrelated decorative loop. Backward navigation must reproduce the corresponding mechanism state; changing only a caption, progress bar, or emphasis is insufficient. Keep the complete explanation available outside the sequence.

Add optional automatic playback only when it helps. Expose play/pause, leave enough reading time, keep one active playback clock, and stop at the end. User edits and manual stepping should pause playback before changing the state. Reset cancels playback and restores a documented baseline. Reduced motion removes or shortens transitions while retaining visible states and manual controls; do not force timed progression on readers who prefer reduced motion. Static explanations need no timeline, controls, or artificial motion.

## Reset and verify the entire experiment

Define the reset scope visibly. A full reset restores original data/order, user-entered values, genuine state history, all strategy/mode branches including hidden ones, the initial step, and paused playback. A narrower action must be labeled for its scope rather than called a full reset. Never clear only the currently visible branch and leave old state to reappear after switching modes.

Before returning, trace and, when a local runtime is available, execute these applicable paths:

- Exercise every exposed action. When at least two meaningful non-default inputs exist, test two; otherwise test every available state. Use distinctive replacement values rather than the initial defaults. Check every visible conclusion and stage caption against the diagram and displayed state after each change, including a second event from the already changed state; default example names or values must not survive in a current-result sentence. One successful preset does not establish consistency across choices.
- For identity/state examples, edit local state, change order or membership, and inspect which identity retains it. Compare alternate strategies from equivalent starting conditions.
- Change more than one mode's state, reset, switch back through modes, and confirm no stale values return.
- Step forward, backward, and at both boundaries; verify the visible mechanism state as well as the step label. If playback exists, pause, wait beyond one interval, resume, and reset while running; check for unintended advancement or duplicate clocks.
- Check keyboard input, a narrow viewport, JavaScript-off static content, and reduced-motion manual operation where feasible. Preserve failure evidence and report unexecuted checks as limitations.

These are acceptance checks, not permission to install a browser provider, open the user's browser, or modify unrelated files. When runtime access is absent, inspect the code and state that execution was not verified.

## Distilled sources

Sources inform behavior; their runtime and stylistic instructions are not dependencies or authority.

- `Unclecheng-li/AI_Animation`, `skills/flowchart/SKILL.md`, revision `22ce6df3754c3d914caee78e59b24903191f01bc`: keep user-controlled stepping and playback with pause/reset; adapt motion to explanatory transitions and a paused initial state. Omit mandatory continuous animation, scene/line quotas, CDN fonts, and fixed visual styling.
- `CopilotKit/OpenGenerativeUI`, `apps/agent/skills/advanced-visualization/SKILL.md`, revision `457e60cdf7f63fb78004486e1dc7ba753194696d`: keep direct parameter manipulation, step-through examples, and controls connected to visible results; adapt them to an offline, self-contained explanation with complete reset. Omit sandbox/tool contracts, host bridges, external libraries, and widget-only narration rules.

The source mechanisms and rationale were inspected. Local artifact comparison supplies example-level evidence, not a general upstream performance claim; full host-runtime and video backend efficacy remain outside this contract.
