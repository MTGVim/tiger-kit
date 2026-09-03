# React review

Read this only when React component, hook, JSX, or React Server Component semantics are in review scope.

- Follow actual closures and lifecycle for effect dependencies, cleanup, subscriptions, timers, and requests. Report a
  missing dependency or cleanup only when it changes reachable behavior.
- Check stale closures, duplicated derived state, effect chains, and synchronization for a concrete inconsistent state.
- Judge list keys and identity from possible insertion, reorder, and stateful children; a static list is not a defect.
- Trace server/client boundaries for serializable data, secret exposure, and server-action authorization.
- For changed interaction, check the semantic control, accessible label, keyboard path, and necessary ARIA.
- Do not request memoization, virtualization, smaller components, or shallower props from a numeric threshold. Require an
  observed hot path or concrete correctness, accessibility, or maintenance failure.
