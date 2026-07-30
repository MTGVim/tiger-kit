# Drive procedure graph

`tk-drive` owns one continuous `Preparing → Executing → aggregate verification
→ reflection → finalization` run. A source enters only through an explicit
drive invocation or a pending answer in the same active conversation.

## Canonical nodes

- Internal: `tk-drive preflight`, `aggregate verification`,
  `tk-drive finalization`, `tk-drive non-success finalization`
- Preparing: `tk-grill-me`, `tk-prototype`, `tk-to-spec`, `tk-to-tickets`
- Executing: `tk-implement`, `tk-merge-conflict`
- Verification and tail: `tk-browser-verify`, `tk-reflect`

Unknown nodes, aliases, misspellings, and implicit sibling calls are invalid.

## Complete edge table

| From | To | Entry condition | Success condition | Failure behavior | Next edge |
| --- | --- | --- | --- | --- | --- |
| `tk-drive preflight` | `tk-grill-me` | material decisions remain | decisions confirmed | use an allowed alternate edge; otherwise finalize terminal non-success | `tk-prototype` or `tk-to-spec` |
| `tk-drive preflight` | `tk-to-spec` | no material decision remains | Ready spec verified | use an allowed alternate edge; otherwise finalize terminal non-success | `tk-to-tickets` or `tk-implement` |
| `tk-grill-me` | `tk-prototype` | bounded comparison reduces uncertainty | comparison evidence produced | return to decision closure when supported; otherwise finalize terminal non-success | `tk-grill-me` |
| `tk-prototype` | `tk-grill-me` | comparison completed | decision confirmed | use an allowed alternate edge; otherwise finalize terminal non-success | `tk-to-spec` |
| `tk-grill-me` | `tk-to-spec` | decision confirmed without comparison | Ready spec verified | use an allowed alternate edge; otherwise finalize terminal non-success | `tk-to-tickets` or `tk-implement` |
| `tk-to-spec` | `tk-to-tickets` | multiple independently verifiable units exist | ticket ledger verified | use an allowed alternate edge; otherwise finalize terminal non-success | `tk-implement` |
| `tk-to-spec` | `tk-implement` | one independently verifiable unit exists | unit verified and committed | use an allowed alternate edge; otherwise finalize terminal non-success | `tk-implement` or `aggregate verification` |
| `tk-to-tickets` | `tk-implement` | ordered ticket ledger verified | unit verified and committed | use an allowed alternate edge; otherwise finalize terminal non-success | `tk-implement` or `aggregate verification` |
| `tk-implement` | `tk-merge-conflict` | an actual operation conflict is active | conflict resolved | use conflict recovery when supported; otherwise finalize terminal non-success | interrupted `tk-implement` |
| `tk-merge-conflict` | `tk-implement` | conflict resolution verified | interrupted unit verified and committed | use an allowed alternate edge; otherwise finalize terminal non-success | `tk-implement` or `aggregate verification` |
| `tk-implement` | `tk-implement` | another selected unit remains | next unit verified and committed | use an allowed alternate edge; otherwise finalize terminal non-success | `tk-implement` or `aggregate verification` |
| `tk-implement` | `aggregate verification` | all selected units are committed | aggregate obligations verified | correct an isolated failure when supported; otherwise finalize terminal non-success | `tk-browser-verify`, corrective `tk-implement`, `tk-reflect`, or finalization |
| `aggregate verification` | `tk-browser-verify` | preflight or changed UI requires browser evidence | required scenarios verified | use an allowed alternate edge; otherwise finalize terminal non-success | `aggregate verification` |
| `tk-browser-verify` | `aggregate verification` | browser evidence completed | aggregate browser obligation satisfied | use an allowed alternate edge; otherwise finalize terminal non-success | corrective `tk-implement`, `tk-reflect`, or finalization |
| `aggregate verification` | `tk-implement` | an isolated correctable failure remains and fewer than three cycles ran | corrective unit verified and committed | finalize terminal non-success on repeated, exhausted, or unisolated failure | `aggregate verification` |
| `aggregate verification` | `tk-reflect` | product verification passed and a valid reflection handoff exists | classification completed or no-op | restore safely when supported; otherwise finalize terminal non-success | `tk-drive finalization` |
| `aggregate verification` | `tk-drive finalization` | product verification passed and reflection is not applicable | final evidence reread | finalize terminal non-success on evidence drift | terminal response |
| `tk-reflect` | `tk-drive finalization` | reflection completed safely | final evidence reread | finalize terminal non-success on unrestored or unverifiable state | terminal response |
| `tk-drive preflight` | `tk-drive non-success finalization` | terminal native non-success and no allowed alternate edge remains | scope accounted and recovery derived | preserve originating native status and available evidence | terminal response |
| `tk-grill-me` | `tk-drive non-success finalization` | terminal native non-success and no allowed alternate edge remains | scope accounted and recovery derived | preserve originating native status and available evidence | terminal response |
| `tk-prototype` | `tk-drive non-success finalization` | terminal native non-success and no allowed alternate edge remains | scope accounted and recovery derived | preserve originating native status and available evidence | terminal response |
| `tk-to-spec` | `tk-drive non-success finalization` | terminal native non-success and no allowed alternate edge remains | scope accounted and recovery derived | preserve originating native status and available evidence | terminal response |
| `tk-to-tickets` | `tk-drive non-success finalization` | terminal native non-success and no allowed alternate edge remains | scope accounted and recovery derived | preserve originating native status and available evidence | terminal response |
| `tk-implement` | `tk-drive non-success finalization` | terminal native non-success and no allowed alternate edge remains | scope accounted and recovery derived | preserve originating native status and available evidence | terminal response |
| `tk-merge-conflict` | `tk-drive non-success finalization` | terminal native non-success and no allowed alternate edge remains | scope accounted and recovery derived | preserve originating native status and available evidence | terminal response |
| `aggregate verification` | `tk-drive non-success finalization` | terminal native non-success and no allowed alternate edge remains | scope accounted and recovery derived | preserve originating native status and available evidence | terminal response |
| `tk-browser-verify` | `tk-drive non-success finalization` | terminal native non-success and no allowed alternate edge remains | scope accounted and recovery derived | preserve originating native status and available evidence | terminal response |
| `tk-reflect` | `tk-drive non-success finalization` | terminal native non-success and no allowed alternate edge remains | scope accounted and recovery derived | preserve originating native status and available evidence | terminal response |

Only the explicitly bounded comparison, conflict-resolution, multi-unit,
browser-verification, and corrective loops are allowed. `tk-drive finalization`
and `tk-drive non-success finalization` each have no outgoing edge.

## Direct continuation

On success, select the next applicable row and invoke it immediately in the
same active turn. Procedure evidence remains internal to the workflow. Do not
wait for a new user turn, ask the caller to resume, or emit a user-facing
phase-complete stopping surface.

On failure, expose one actionable blocking fact and apply every supported
alternate edge before treating the state as terminal. When no alternate edge
remains, freeze product mutation and enter `tk-drive non-success finalization`;
do not invoke another specialist or leave terminal accounting to the child.

This continuation contract is prompt-directed and probabilistic. It does not
provide durable scheduling, event replay, or guaranteed cross-turn execution.
After a host or process boundary, derive the next node from current artifacts
and repository evidence instead of claiming that an earlier prompt still owns
runtime control.

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

## Non-success finalization

Enter `tk-drive non-success finalization` only after the originating
`Fail | Blocked | Unverifiable` is terminal under the edge table. Entry freezes
source edits, stage/commit, reset/revert/stash/clean, new test/build/server or
browser execution, and every implementation, reviewer, browser, or reflection
invocation. Read-only artifact and Git audits remain allowed. A bounded update
to an existing ticket or implementation ledger remains allowed only under that
artifact's existing ownership and atomicity contract.

Reread applicable prep, spec, tickets, implementation, and browser evidence,
then audit branch, HEAD, current-branch ancestry, and dirty paths. Classify:

- `Completed`: an ancestor commit still binds to matching unit receipt, review,
  and verification evidence;
- `Stopped`: the unit or procedure that produced terminal non-success;
- `Dependency blocked`: an incomplete unit transitively depends on `Stopped`;
- `Not attempted`: an incomplete independent unit was not run after mutation
  froze;
- `Unverified`: a change or completion claim lacks current binding evidence.

Branch, HEAD, ancestry, or receipt drift prevents `Completed` classification.
Pre-existing dirty user paths remain excluded from drive ownership. Preserve
completed ticket receipts, keep incomplete tickets incomplete, and record only
bounded `Last attempt`, `Evidence`, and `Recovery` fields when their current
owner contract permits it. The current implementation attempt may record native
status, branch/HEAD, uncommitted paths, executed verification, unverified scope,
`commit: none`, and one recovery condition. Never store raw logs, full diffs,
transcripts, secrets, or a new lifecycle state.

Recovery is one evidence-derived action: answer a pending decision in the same
conversation, restore environment or tooling and explicitly rerun the same
source, manually clean the failed unit state and explicitly rerun, or start a
fresh drive from source when prep/spec/ticket evidence drifted. Do not promise
automatic continuation or another unit start.

The terminal response leads with one result sentence and omits empty sections.
Use `Completed`, `Stopped`, `Remaining`, and `Recovery` only when applicable.
A multi-unit `Completed` table may use `Unit | Outcome | Commit | Evidence`;
`Outcome` is a table header, never the forbidden top-level `Outcome:` label.
`Stopped` may use `Node/unit`, `Reason`, and `Working state`. `Remaining` uses
`Dependency blocked`, `Not attempted`, or `Unverified`. End with exactly one
originating `Status: Fail`, `Status: Blocked`, or `Status: Unverifiable` line.
Never emit `Status: Pass` or a new partial status. This node has no outgoing
edge.

## Terminal ownership

Only `tk-drive finalization` for verified success or
`tk-drive non-success finalization` for terminal non-success emits the
active-drive terminal user response. Progress commentary and internal
procedure evidence are not terminal output. Each finalization rereads current
artifacts and repository evidence; only successful finalization ends
`Verification` with `Status: Pass`.
