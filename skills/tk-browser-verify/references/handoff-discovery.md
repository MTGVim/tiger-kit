## Parent Handoff

Use parent-provided values when available:

- exact criterion, target/environment, and current candidate;
- headless authentication and secret-free bootstrap method;
- viewport, initial state, and server command/cwd/readiness;
- screenshot mapping, replay procedure, nondeterministic exclusions, and allowed capture-only adjustments;
- any approved test-data mutation scope: exact non-production environment, allowed entity types and create/update/delete
  operations, and cleanup policy; absent or ambiguous scope means no data-changing interaction;
- exact UI strings or verified entry paths;
- exact visual reference or pre-change provenance and comparable viewport/DPR/zoom/font state when a design node,
  mockup, baseline screenshot, as-is/to-be comparison, or render-affecting candidate exists;
- redaction rule, `Pass` condition, and automated-regression disposition.

If the Ready Seed already owns this information, do not ask for the same decisions again.
If required values are missing but can be safely determined from repository evidence, fill them in.
Return only outcome-changing user-owned decisions to the parent owner.

## Read-only UI evidence discovery

An evidence-discovery request may identify a known target URL, environment, role, and the missing label/path as its
question; the unknown label is not a prerequisite for this mode. Keep all provider, headless, authentication, readiness,
and interaction boundaries. Inspect visible text and navigation connections without submitting business mutations.
After entry and initial rendering, perform the UI Evidence text inventory before selector-level lookup; use the safe scoped fallback when full-body output would expose sensitive data. Capture visible breadcrumbs/headers, then verify actual menu clicks separately when a traversed path is required.
Return observed literals, displayed hierarchy, and actually traversed connections separately with provenance, plus an itemized list of unresolved labels/connections, limitations, and requested inputs. A successful locator match
or accessible name alone does not prove visible wording; inspect the actual visible text. This discovery is not a
Content comparison pass and never invents the parent's missing acceptance basis. Return evidence to the requesting owner.

