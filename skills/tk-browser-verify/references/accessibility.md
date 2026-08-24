# Conditional accessibility verification

Apply this only when the current scope includes a form, dialog, navigation, keyboard
shortcut, or focus behavior. Do not impose a complete checklist on a visual-only
layout check.

## Evidence

- **Keyboard path:** Use the trusted `Tab`, `Shift+Tab`, `Enter`, `Space`, `Escape`,
  and arrow-key inputs required by the actual flow.
- **Focus:** Verify visible focus, a reasonable initial dialog target, return to the
  trigger after close, and modal focus containment.
- **Accessible name:** Observe whether controls, links, and dialogs expose names that
  explain their purpose.
- **Errors:** Verify that a validation error is associated with its field and can be
  discovered through focus or announcement.
- **State:** Verify that expanded, selected, checked, and disabled visual states agree
  with their semantic states.

A screenshot supports visible-focus and layout claims, but does not prove keyboard
reachability, accessible names, or error association. DOM/accessibility-tree evidence
alone does not prove visible focus.

## Scope facts

Record the inspected flow, keyboard path, focus results, semantic evidence, findings,
and exclusions. Do not claim full WCAG or product-wide accessibility conformance from
a limited rule set or a single flow.
