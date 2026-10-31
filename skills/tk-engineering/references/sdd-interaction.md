# SDD User Interaction

Read only when a child needs user input or a host interaction.


The root controller owns user intent, product/scope/acceptance decisions, Seed changes,
new authority (including destructive or publication authority), and host-defined root-only
permission/approval APIs. Leaves return these needs to their controller; a delegated
controller forwards unresolved root-owned needs to the root. A tool form does not turn
such a decision into leaf authority, even on a host with child-safe elicitation.

For a bounded interaction within the approved Unit, a leaf may use the host's supported
child-local elicitation only when current host/tool evidence establishes all of:

- the exact interaction route supports child elicitation;
- the prompt belongs to this leaf's exact pending request;
- the response is bound only to that request, without expanding scope or authority;
- the same approval/security policy applies on the child path;
- the same child execution can safely resume after the response;
- the interaction stays within the approved Unit and the leaf's role authority.

Read the current host/tool contract or verified runtime evidence; provider names, an
empty form, automatic permission settings, or an upstream implementation alone do not
prove that this route is supported here. Do not create a durable capability registry.
When all conditions hold, let the host surface the connector authentication, browser
sign-in continuation, or tool-defined form and receive its bound response; never answer
for the user or collect credentials/OTPs in chat or handoff. Honor decline, cancellation,
and policy denial without retrying or changing routes to bypass them. After a verified
successful outcome, continue the same Unit in the same child without a parent round-trip,
extra approval, or re-dispatch. Authentication acceptance alone does not prove successful
sign-in: follow the supported continuation and verify the resulting state. Preserve the
browser owner's headless and secret-handling constraints and remaining review obligations.

If any condition is unknown or unmet, stop the affected interaction and use the existing
controller handoff in this reference. This also applies when request/response provenance or safe
resume becomes uncertain after interruption; use [recovery](sdd-recovery.md) to reconcile mutations
before retry or replacement. Normal same-child continuation needs no durable state.

Include in the existing child return: Unit and role, exact blocker, requested user
action or decision, non-secret evidence/current state, whether mutation already
occurred (or is unknown), and the safe resume condition. Stop the blocked action;
never include credentials, OTPs, tokens, or session secrets in the handoff.

For escalated interactions, the controller checks existing authorization and resolves
repository/host facts before asking the user. Handle root-owned or unsupported child input
in the root context, using `tk-wizard` only for its existing provisioning/authentication/permission
scope; product decisions stay with the preparation owner. Existing approval avoids
reapproval of the same intent, but does not supply missing human input or override a
host denial. Preserve the browser owner's headless and secret-handling constraints.

After the blocker is verifiably resolved, resume the existing child within the same
approved Unit. If it cannot resume, reconcile prior mutations and child lifecycle
under [recovery](sdd-recovery.md) before dispatching only the remaining bounded work. Preserve
Seed/Unit/BASE/workspace identity and existing review/verification obligations; an
unknown outcome blocks retry. Reuse active optional recovery state without creating
an interaction ledger, durable receipt, or new lifecycle state.

Approved non-interactive tool calls, host-authorized automatic permission handling,
read-only reviewer judgments, repository facts available within the brief, and
reversible engineering choices within leaf authority continue locally. They do not
require parent mediation or user reapproval; existing controller `Ruling:` boundaries
still apply.

