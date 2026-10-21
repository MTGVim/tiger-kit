## Publication approval packet

Record the following exact information in the active approval packet. Keep it in the current interaction when the host can
faithfully retain and reread a simple single-PR packet. Use the singleton `.tigerkit/pr-open.md` only for a stack, an
explicit `save`, a multi-turn handoff/recovery need, or when the exact approval state cannot otherwise be retained. Never
create per-run publication files. When the artifact is used, atomically replace stale completed content for the same owner
and reread it before approval.

```text
Repository
Publication shape: single | stacked
PR operation: create | update
PR state: draft | ready
Base
Original head ref + SHA + tree
Template source/compliance
PR evidence requirement/state
Evidence manifest entries/paths
Known exclusions

Single publication:
Head ref + SHA
Push refspec
Title
Title convention basis: <repository instruction | normative template/docs | merged-title evidence | fallback>
Body

Stacked publication:
See the required plan fields in [retrospective stack split](split-to-stack.md).
```

Any artifact owns only the current PR publication plan, not the product work plan or `worker` state.
Create new PRs as `ready` unless the user explicitly requests `draft`.
For an existing same-`head` PR, preserve its fresh-read state unless a state change was requested.

Present the following naturally to the user. Content the user must read before approval appears inline
in the conversation, or in the repository `.tigerkit/` artifact when the packet rules require a file.
Never cite a session-private scratchpad path as reading material. Keep the exact full title/body in the
active packet even when the user-facing preview omits boilerplate.

- Summary of included changes
- Recommended `single | stacked` publication shape and why
- Preview the title and the sections this publication fills or changes for every PR being created or
  updated so the user can quickly decide which items to include or omit. Show each section's item
  arrangement and a one- or two-line summary in rendered Markdown without wrapping the preview
  in a code fence. Use bold section labels instead of copying body `##` headings into the response.
  Summarize GFM tables and image grids in one readable line (for example, two images paired
  before/after); retain any material item-level choice or checklist change outside that summary.
  Omit template boilerplate (HTML comments, unchanged headings and unchanged checklists) from the
  preview; preserve it verbatim in the published body and keep the exact full Markdown in the
  active packet (or `.tigerkit/pr-open.md` only when the packet rules require it). Show the full body
  only on request. Preview formatting never rewrites the publication body or uploaded image Markdown.
- Title-convention evidence and any mismatch with template guidance
- Base/head; for a stack also present the exact bottom-to-top branches and preserved original tree invariant
- Valid `PR state`
- Check/evidence state
- Exclusions/risks
- One publication recommendation

If `PR evidence requirement/state` remains `undecided`, include its image choices in the final question block at this
checkpoint, after the concrete publication preview and before any write. Keep the existing packet fields.

