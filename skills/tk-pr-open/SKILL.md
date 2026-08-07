---
name: tk-pr-open
description: "[user/auto] Open or update one GitHub pull request from verified current-branch commits; require exact current-turn approval before remote publication."
argument-hint: "<repository or branch>"
disable-model-invocation: false
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Open pull request

Start when the user selects `/tk-pr-open`, `$tk-pr-open`, or host skill picker, or when a clear single-PR request asks to prepare, open, or update one PR in natural language. This includes a post-`tk-drive` handoff such as “the verified commit is done; prepare the PR”: an existing verified current-branch commit is the expected input, not duplicate implementation work. Reuse that commit; never dispatch another product worker or create another product commit for this handoff. Natural-language routing starts only this skill's local preview; it never implies publication. Never activate from a generic PR question, code review, implementation request, merge request, multi-PR maintenance request, or existing `.tigerkit` artifact alone.

Own one pull-request draft and bounded publication plan. May inspect local Git/GitHub state and write `.tigerkit/pr-open.md`. Never edit product code, create product commits, merge, tag, release, or publish before approval gate below.

## Workflow

1. Resolve executing repository, authenticated GitHub identity, current branch, `HEAD`, dirty paths, base branch, and existing PR for branch.
2. Verify intended commits present, unrelated dirty paths preserved, proposed PR not duplicating existing PR.
3. Consume `PR evidence: required | optional | N/A` from request or Ready contract. Map `required` to `evidence_required: true`; collect only valid screenshot handoffs from `tk-browser-verify` or `tk-prototype`. `optional` uploads only evidence explicitly in approved plan; `N/A` never invokes uploader. Record producer, absolute evidence directory, screenshot paths, actual inspection, and criterion in plan. If absent, show `PR evidence: undecided` with one recommendation; obtain decision before publication approval. Never infer required evidence from arbitrary screenshots or browser verification alone.
4. Draft exact title, body, base/head refs, push refspec, evidence state, and known exclusions in `.tigerkit/pr-open.md`. When updating PR, preserve existing body sections, checklists, attachments, and user-authored notes.
5. Before approval request, show preview in order: included changes; exact PR title/body; base/head and check/evidence state; exclusions/risks; one publish recommendation. Keep refspec, identity, provenance in artifact unless decision-relevant. Ask one approval question; stop `Pending`. Generic “go ahead” never approves different/stale plan.
6. After current-turn approval, recheck branch, `HEAD`, PR identity, open state. Push explicit refspec; create/update only named PR. When required evidence valid, hand to `tk-github-image-upload-to-pr` after PR exists.
7. Reread remote PR; report URL, head SHA, operation result, evidence state, remaining checks. If required evidence missing/upload fails, keep PR result but return `Blocked` for final completion. Never merge or request release.

## 🔴 CHECKPOINT / STOP · Publication gate

Plan must name repository, PR/create target, base branch, head branch, exact push refspec, title, body, evidence requirement/state, operation order, and exclusions.

| Trigger | First action | If unresolved |
|---|---|---|
| Waiting for exact current-turn approval | Make no remote write | `Pending` |
| Branch/PR head, identity, dirty paths, body, or target changed | Invalidate approval; refresh plan | `Blocked` |
| Required Git or GitHub evidence unavailable | Record attempted check/evidence gap | `Unverifiable` |
| Push, create, or update fails or partially applies plan | Reread remote PR; report exact applied state | `Fail` |
| Required upload missing/fails after PR creation | Keep PR; report evidence recovery condition | `Blocked` |
| Requested PR operation and required evidence verify | Report fresh URL and head SHA | `Pass` |

Lead with `## PR open`; show only user-relevant state, verification, remaining risks. Keep full provenance in `.tigerkit/pr-open.md`.

### 🔴 HARD GATE · terminal user summary

Begin terminal response with `## PR open`. Never emit receipt heading, `Outcome:` label, procedural preamble, or bottom metadata block. Expose path, ID, commit, or recovery detail only when it changes user's next action.

### 🔴 HARD GATE · response language

When a user-facing result includes an absolute time, convert it to the user's local timezone and label the timezone; keep raw machine timestamps only in owned evidence. Progress is optional and nonterminal: standalone execution is silent by default; emit `🙋 response/approval needed` only when user action is required, `⏳ wait` only when external waiting is next, or `🚗 meaningful boundary` only for long-running work. Put one space after each marker, omit no-op rows, and keep terminal responses free of progress markers while preserving any required terminal `Status: <token>`.

Use latest explicit user language for all free-form user-facing prose. Keep headings, statuses, IDs, paths, commands, and exact source literals stable.

## User decision questions

When user-owned decision blocks publication, ask one self-contained `Question` before any `Recommendation`, with only decision-relevant evidence and one recommended option. Render question/options directly in chat; never call structured question/input tools. Preserve `Pending` until answer.
## Progress

Standalone skills are silent by default. Emit no progress for routine start or success; use `🙋 pr-open · 응답 필요` only for a user decision/approval, `⏳ pr-open · 대기` only when external waiting is next, and `🚗 pr-open · <short state>` only at a meaningful long-running boundary. Omit `tk-` from display names; a parent owns `🚗 parent > pr-open`. Terminal responses contain no progress marker; keep `Status: <token>` unchanged.

## Next-action handoff

Whenever this skill hands control back to the user for a question, `Pending`,
`Blocked`, `Unverifiable`, bounded wait, or an actionable terminal result, end
the visible handoff with exactly one `Next:` line naming the recommended action
or next skill and its condition. Before rendering any user-facing `Question` or
publication/approval plan, emit exactly one nonterminal hand-raise checkpoint
in this skill's `🙋 ... · 응답 필요` form; a parent may own the display in
orchestration. Do not use only a `🤹` or `🚗` boundary marker for a user
decision. Mark the single recommended option with `👍 Recommendation:`.
Do not leave only a child receipt or generic “continue”; omit `Next:` only for
a terminal success with no follow-up action.
