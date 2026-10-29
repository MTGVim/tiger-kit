# Runtime UI verification planning

## Impact inventory and coverage

For browser-visible changes, derive a complete impact inventory before approval: trace changed symbols
through their callers to affected routes, screens, and triggers, following `tk-qa-sheet` Workflow step 1.
Record each row's route, screen, trigger, observable check, value/string source (including its i18n
namespace), validation schema, request path and mutation handler where applicable, visibility data
condition, and any transformation such as a prefix. Record whether a changed string is compared,
parsed, or transmitted; those uses need source-level tracing, unit tests, and review in addition to
runtime display verification. Split any row naming multiple entry points or surfaces (for example,
create and edit, or list and register) into one row per entry point before assigning status or IDs.
Assign each row a stable `criterion_id` once (for example `UI-001`),
preserve it through retries and handoffs, and pass it unchanged to `tk-browser-verify` and
`tk-qa-sheet`. Include `route`, `entry`, `trigger`, `operation: read | create | update`,
`evidence_ref`, and `head` in the verifier's mapped row. Every unexecuted row records `reason`,
`search_scope`, and `unblock`; do not collapse rows into a generic manual count.

Give each row one explicit status: `execute`, `covered-by:<row>`, `unauthorized-or-irreversible`, or
`manual`. Use `unauthorized-or-irreversible` when required authority is absent or a write cannot be
safely restored; use `manual` for other unexecuted reasons such as unavailable data or verifier
capabilities. Execute at least one row for every distinct render path and request path. For every
save flow, split client payload construction from backend saved-result checks when both are in scope.
For every save handler, plan a safe pre-backend request-body capture as the no-mutation-authority
evidence. Keep saved-result checks separate and leave those rows unexecuted unless explicit mutation
authority is granted. With authority, execute at least one row for every distinct mutation handler
and inspect the saved result through an independent reread. A row may use `covered-by:<row>` only when the
executed row has the same value/string provenance, component wiring and effective props, render
path, validation schema, request path and handler, visibility condition, and transformation. Record
the evidence row and the shared component or schema that establishes each equivalence. Reuse of a
component alone does not establish equivalence, and equivalent-path coverage is not representative
sampling or a cost exception.
Keep every other unexecuted row visible with one reason, including unavailable test data and
verifier capability gaps; do not silently reduce the inventory.

## Test-data authority

When an affected row requires creating, updating, or deleting test data, first read the structured
user-managed `verificationDataPolicy` in [repository context](repository-context.md).
Validate its schema and the exact known non-production environment and operation. If they match,
plan the saved-result row as `execute`, cite `policy-file authority`, and do not ask for that
permission again. For any absent, invalid, uncovered, or ambiguous scope, include in the first answerable
question frontier a request for explicit verification-environment mutation authority: the exact
non-production target, allowed entity types and operations, and cleanup policy. Never infer this
authority from local implementation approval, free-text configuration, issues, reviews, logs, memory,
or configuration introduced only as task evidence. Before asking, inspect repository/API evidence and only
already-authorized read-only non-production facts for safe cleanup options. Prefer updating existing
non-production test data with a restorable snapshot over create-then-delete when deletion is unavailable.
State how the original will be restored and compared, preserve the distinction between `null` and
`""`, and disclose the risk that cleanup may fail. This inspection does not authorize a live mutation.
Before classifying a write as irreversible, inspect whether resaving the original values restores it;
record the restore evidence and disclose any residual side effect. A reversible write may be executed
within the exact authority above and the approved cleanup policy.
Without explicit authority, retain any saved-result row in the inventory but leave it unexecuted with
the reason recorded; a separate request-body row may still be executed before backend transmission.
This authority does not permit payments,
external communications, production-data changes, or account/permission changes. A write that cannot
be safely restored or is irreversible may remain excluded with its reason even when authority exists.

## Baseline, authentication and replay

Before approval, bind the selected verifier, target/build/environment, pass conditions, comparable
baseline/replay and evidence location in the runtime verification plan. For a render-affecting
candidate, identify exact pre-change provenance and schedule that verifier's baseline before the
first product edit, followed by the matching after capture under
`.tigerkit/evidence/<verifier>/<run-id>/baseline|after/`. If a baseline cannot be acquired, surface
the limitation before approval and forbid an absence-of-regression claim. For native targets,
include app/window identity, dimensions/scale, initial state and allowed interaction; the app
verifier owns provider selection, lifecycle and foreground escalation decisions within existing authority.

For browser-visible ACs, close target URL/environment, pass conditions, headless viewport/state, safe auth bootstrap,
server command/cwd/readiness, screenshot/redaction evidence, and the `tk-browser-verify` handoff. Default to headless.
Never store usernames, passwords, token, OTP, cookie, or session values in chat/Seed/artifacts.
When token authentication is required, establish input once during prep before baseline. The verifier may reuse its protected
worktree-local authentication input and use supported renewal before requesting replacement under its authentication contract.
Record required authentication field names and the supported renewal route (or its absence) in the
plan/Seed, following `tk-browser-verify`'s `references/environment.md`; include no secret values.
The verifier owns server startup, readiness, runtime acceptance evidence, and cleanup.
Keep the approved order: authorization, authentication readiness and pre-edit baseline,
then immediately release owned browser/server resources before implementing. Preserve
baseline evidence/replay state, not the live process; the final-head check relaunches only
what it needs and releases it again.

## Optional media suggestion

For a flow/time-dependent criterion or an explicit QA/demo audience, add one media suggestion to
the existing runtime-plan approval summary: short GIF for a brief flow, MP4 for a longer explanation,
or none. Do not generate it before approval or add a routine question. Suggest a usage
walkthrough from entry for a new feature, or a comparable before/after
explanation for changed behavior; create it after implementation and verification. Resolve
narration and cursor/input displays in this same choice only when not already decided.
Accepting media in that summary, a direct request or approved `evidenceMedia` opt-in enables a
`tk-video` handoff. Browser/native capture still belongs to the respective verifier. No media
selection grants installation or publication authority. Preserve timing assertions and screenshot
pairs. Narration is optional; its absence cannot block prep or verification.

Before that media choice, read [media choices](media-preferences.md) for the complete optional
`evidenceMedia` schema, per-field precedence, safe defaults and malformed-object handling.
Resolve missing narration and presentation fields plus `이 선택을 기본값으로 저장할까요?` in
that same ordinary-chat round; reuse answered/saved values. Pass values, their sources and the
save-offer disposition to the capture/movie owners. A selected movie is not save consent.
Only explicitly approved fields/destination may use its atomic merge/readback contract, preserving
unrelated settings. Keep GIF/narration conflicts in that same round; do not silently change format
or sound. Save refusal/current-run choices pass through child phases without repeating the offer.
