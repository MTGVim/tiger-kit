# Drive procedure graph

`tk-drive` owns one continuous `Preparing → Executing → aggregate verification
→ reflection → finalization` run. A source enters only through an explicit
drive invocation or a pending answer in the same active conversation.

## Canonical nodes

- Internal: `tk-drive preflight`, `aggregate verification`,
  `tk-drive finalization`
- Preparing: `tk-grill-me`, `tk-prototype`, `tk-to-spec`, `tk-to-tickets`
- Executing: `tk-implement`, `tk-merge-conflict`
- Verification and tail: `tk-browser-verify`, `tk-reflect`

Unknown nodes, aliases, misspellings, and implicit sibling calls are invalid.

## Complete edge table

| From | To | Entry condition | Success condition | Failure behavior | Next edge |
| --- | --- | --- | --- | --- | --- |
| `tk-drive preflight` | `tk-grill-me` | material decisions remain | decisions confirmed | stop on unresolved user decision | `tk-prototype` or `tk-to-spec` |
| `tk-drive preflight` | `tk-to-spec` | no material decision remains | Ready spec verified | stop on source or decision conflict | `tk-to-tickets` or `tk-implement` |
| `tk-grill-me` | `tk-prototype` | bounded comparison reduces uncertainty | comparison evidence produced | return to decision closure with failure evidence | `tk-grill-me` |
| `tk-prototype` | `tk-grill-me` | comparison completed | decision confirmed | stop on unresolved material decision | `tk-to-spec` |
| `tk-grill-me` | `tk-to-spec` | decision confirmed without comparison | Ready spec verified | stop on spec conflict | `tk-to-tickets` or `tk-implement` |
| `tk-to-spec` | `tk-to-tickets` | multiple independently verifiable units exist | ticket ledger verified | stop on decomposition conflict | `tk-implement` |
| `tk-to-spec` | `tk-implement` | one independently verifiable unit exists | unit verified and committed | stop on unit failure | `tk-implement` or `aggregate verification` |
| `tk-to-tickets` | `tk-implement` | ordered ticket ledger verified | unit verified and committed | stop on unit failure | `tk-implement` or `aggregate verification` |
| `tk-implement` | `tk-merge-conflict` | an actual operation conflict is active | conflict resolved | stop with unresolved conflict evidence | interrupted `tk-implement` |
| `tk-merge-conflict` | `tk-implement` | conflict resolution verified | interrupted unit verified and committed | stop on unit failure | `tk-implement` or `aggregate verification` |
| `tk-implement` | `tk-implement` | another selected unit remains | next unit verified and committed | stop on unit failure | `tk-implement` or `aggregate verification` |
| `tk-implement` | `aggregate verification` | all selected units are committed | aggregate obligations verified | correct an isolated failure or stop | `tk-browser-verify`, corrective `tk-implement`, `tk-reflect`, or finalization |
| `aggregate verification` | `tk-browser-verify` | preflight or changed UI requires browser evidence | required scenarios verified | stop as supported by evidence | `aggregate verification` |
| `tk-browser-verify` | `aggregate verification` | browser evidence completed | aggregate browser obligation satisfied | stop on missing required evidence | corrective `tk-implement`, `tk-reflect`, or finalization |
| `aggregate verification` | `tk-implement` | an isolated correctable failure remains and fewer than three cycles ran | corrective unit verified and committed | stop on repeated or unisolated failure | `aggregate verification` |
| `aggregate verification` | `tk-reflect` | product verification passed and a valid reflection handoff exists | classification completed or no-op | restore safely or stop | `tk-drive finalization` |
| `aggregate verification` | `tk-drive finalization` | product verification passed and reflection is not applicable | final evidence reread | stop on evidence drift | terminal response |
| `tk-reflect` | `tk-drive finalization` | reflection completed safely | final evidence reread | stop on unrestored state | terminal response |

Only the explicitly bounded comparison, conflict-resolution, multi-unit,
browser-verification, and corrective loops are allowed. `tk-drive finalization`
has no outgoing edge.

## Direct continuation

On success, select the next applicable row and invoke it immediately in the
same active turn. Procedure evidence remains internal to the workflow. Do not
wait for a new user turn, ask the caller to resume, or emit a user-facing
phase-complete stopping surface.

On failure, expose one actionable blocking fact. Follow an alternate edge only
when the table permits it and current evidence satisfies its entry condition;
otherwise stop the top-level run without downstream invocation.

## Preparing evidence

Bind source anchors, repository root, worktree, branch, baseline HEAD,
instructions, dirty paths, confirmed decisions, Ready R/AC, exact source UI
literals, prior-art dispositions, selected graph route, unit order,
verification profile, and `.tigerkit/prep.md`.
The route cannot add unsupported verification obligations or remove an
obligation frozen by the material profile.

Browser preflight is `required | optional | N/A`. Treat a private runtime
identity as a material user-owned decision. Store only an opaque profile hint;
credentials and exact identity are intentionally omitted. On cold start,
re-request identity when safe reconstruction is impossible. Re-requesting
that runtime input is not a Preparing amendment.

`tk-to-tickets` is conditional. A single independently verifiable unit routes
from `tk-to-spec` directly to `tk-implement`.

## Execution and correction

Each `tk-implement` owns one verified current-branch commit and its
Standards/Spec review. The multi-unit self-edge continues until no selected
unit remains, then invokes aggregate verification.

The initial implementation has zero corrective cycles when verification
passes. An isolated failure permits at most three corrective cycles through
`aggregate verification → tk-implement → aggregate verification`. Number them
`1`, `2`, and `3`; each cycle must cite the observed failing command or check,
its isolated cause, and the smallest affected unit. A fourth cycle, repeated
unchanged failure, unisolated failure, or scope expansion stops mutation and
reports the remaining failing command and evidence once.

Only one amendment may revisit `tk-grill-me`, Ready-spec validation, and
affected tickets, then refresh current artifacts before resuming. A second
amendment or incompatible committed work stops the run without rewriting
verified history.

## Terminal ownership

Only `tk-drive finalization` emits the active-drive terminal user response.
Progress commentary and internal procedure evidence are not terminal output.
Finalization rereads current artifacts, ancestry, and verification evidence,
then emits one result beginning with the actual outcome and ending
`Verification` with `Status: Pass` only for verified success.
