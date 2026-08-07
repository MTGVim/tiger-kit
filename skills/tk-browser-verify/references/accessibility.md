# Conditional accessibility verification

Apply only when current scope includes a form, dialog, navigation, keyboard
shortcut, or focus behavior. Do not force the complete checklist on a
visual-only layout check.

## Evidence

- **Keyboard path:** use trusted `Tab`, `Shift+Tab`, `Enter`, `Space`,
  `Escape`, or arrow-key inputs required by the actual flow.
- **Focus:** verify visible focus, a reasonable initial dialog target, return
  to the trigger after close, and modal focus containment.
- **Accessible name:** observe that controls, links, and dialogs expose a name
  that explains their purpose.
- **Errors:** verify that validation errors associate with their field and are
  discoverable through focus or announcement.
- **State:** verify that expanded, selected, checked, and disabled visual state
  matches semantic state.

Screenshots support visible-focus and layout claims but do not prove keyboard
reachability, accessible names, or error association. DOM/accessibility-tree
evidence alone does not prove visible focus.

## Scope facts

Record inspected flow, keyboard path, focus result, semantic evidence,
findings, and omitted scope. Never claim full WCAG or product-wide
accessibility conformance from a limited rule set or single flow.
