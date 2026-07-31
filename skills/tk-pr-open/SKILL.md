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
3. Draft the exact title, body, base/head refs, push refspec, and known
   exclusions in `.tigerkit/pr-open.md`. Preserve existing PR body sections,
   checklists, attachments, and user-authored notes when updating a PR.
4. Show a bounded publish plan and stop with `Pending`. A generic “go ahead”
   does not approve a different or stale plan.
5. After current-turn approval, recheck branch, `HEAD`, PR identity, and open
   state. Push the explicit refspec and create or update only the named PR.
6. Re-read the remote PR and report its URL, head SHA, operation result, and
   remaining checks. Do not merge or request a release from this skill.

## Publication gate

The plan must name the repository, PR or create target, base branch, head
branch, exact push refspec, title, body, operation order, and exclusions. Any
branch drift, PR head drift, identity mismatch, dirty-path change, or changed
body invalidates approval and returns `Blocked` with a refreshed plan.

Use `Pass` only when the requested PR operation completed, `Pending` while
waiting for approval, `Blocked` for stale or unsafe scope, `Fail` for a write
failure, and `Unverifiable` when required Git or GitHub evidence is unavailable.

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
recommended option. A failed structured-input call preserves `Pending`.
