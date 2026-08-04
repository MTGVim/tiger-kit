---
name: tk-pr-open
description: "[user] Open or update one GitHub pull request from verified current-branch commits; require exact current-turn approval before remote publication."
argument-hint: "<repository or branch>"
disable-model-invocation: true
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# Open pull request

Start only when the user selects `/tk-pr-open`, `$tk-pr-open`, or the host skill
picker. Do not activate from a generic PR question, code review, implementation
request, or an existing `.tigerkit` artifact.

This skill owns one pull-request draft and its bounded publication plan. It may
inspect local Git and GitHub state and write `.tigerkit/pr-open.md`. It does not
edit product code, create product commits, merge, tag, release, or publish
anything before the approval gate below.

## Workflow

1. Resolve the executing repository, authenticated GitHub identity, current
   branch, `HEAD`, dirty paths, base branch, and any existing PR for the branch.
2. Verify that the intended commits are present, that unrelated dirty paths are
   preserved, and that the proposed PR does not duplicate an existing PR.
3. Consume `PR evidence: required | optional | N/A` from the request or Ready
   contract. Map `required` to `evidence_required: true` and collect only valid
   screenshot handoffs from `tk-browser-verify` or `tk-prototype`; `optional`
   uploads only evidence explicitly included in the approved plan, and `N/A`
   never invokes the uploader. Record the producer, absolute evidence directory,
   screenshot paths, actual inspection, and criterion in the plan. If the
   decision is absent, show `PR evidence: undecided` with one recommendation and
   obtain it before publication approval. Do not infer required evidence from
   arbitrary screenshots or from browser verification alone.
4. Draft the exact title, body, base/head refs, push refspec, evidence state,
   and known exclusions in `.tigerkit/pr-open.md`. Preserve existing PR body
   sections, checklists, attachments, and user-authored notes when updating a
   PR.
5. Before asking for approval, show a user-facing preview in this order:
   included changes, exact PR title and body, base/head and check/evidence state,
   exclusions or risks, and one publish recommendation. Keep refspec, identity,
   and provenance detail in the artifact unless it changes the user's decision.
   Ask one approval question and stop with `Pending`. A generic “go ahead” does
   not approve a different or stale plan.
6. After current-turn approval, recheck branch, `HEAD`, PR identity, and open
   state. Push the explicit refspec and create or update only the named PR.
   When required evidence is valid, hand it to
   `tk-github-image-upload-to-pr` after the PR exists.
7. Re-read the remote PR and report its URL, head SHA, operation result,
   evidence state, and remaining checks. If required evidence is missing or
   upload fails, keep the PR result but return `Blocked` for final completion.
   Do not merge or request a release from this skill.

## 🔴 CHECKPOINT / STOP · Publication gate

The plan must name the repository, PR or create target, base branch, head
branch, exact push refspec, title, body, evidence requirement/state, operation
order, and exclusions.

| Trigger | First action | If unresolved |
| --- | --- | --- |
| Waiting for exact current-turn approval | Make no remote write | `Pending` |
| Branch/PR head, identity, dirty paths, body, or target changed | Invalidate approval and refresh the plan | `Blocked` |
| Required Git or GitHub evidence is unavailable | Record the attempted check and evidence gap | `Unverifiable` |
| Push, create, or update fails or writes only part of the plan | Re-read the remote PR and report exactly what applied | `Fail` |
| Required upload is missing or fails after PR creation | Keep the PR, report the evidence recovery condition | `Blocked` |
| Requested PR operation and required evidence verify | Report the fresh URL and head SHA | `Pass` |

Lead with `## PR open` and show only user-relevant state, verification, and
remaining risks. Keep full provenance in `.tigerkit/pr-open.md`.

### 🔴 HARD GATE · terminal user summary

Begin the terminal response with `## PR open`. Do not emit a receipt heading,
`Outcome:` label, procedural preamble, or bottom metadata block. Expose a path,
ID, commit, or recovery detail only when it changes the user's next action.

### 🔴 HARD GATE · response language

Use the latest explicit user language for all free-form user-facing prose.
Keep headings, statuses, IDs, paths, commands, and exact source literals stable.

## User decision questions

When a user-owned decision blocks publication, ask one self-contained `Question`
before any `Recommendation`, with only decision-relevant evidence and one
recommended option. Render the question and options directly in the chat
response; do not call structured question or input tools. Preserve `Pending`
until the user answers.
