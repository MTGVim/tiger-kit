# Open mode

Open mode prepares or updates one draft pull request from already verified
commits. It does not own product mutation, commit cleanup, history rewriting,
or implicit commit creation.

## Preflight

1. Resolve repository instructions, current branch, authenticated GitHub user,
   upstream remote, remote default branch, current `HEAD`, dirty paths, and any
   existing pull request for the exact head branch.
2. Stop `Blocked` when the worktree contains product changes not already owned
   by verified commits. Never turn dirty files into a PR by committing them.
3. Refresh the selected base ref. Prefer an explicit base, then repository
   instructions or an existing PR, then the remote default branch. Do not
   invent `main`, `develop`, or a Git-flow mapping.
4. Inspect the complete base-to-head commit and diff range, pull-request
   template, recent merged pull-request conventions, linked issue evidence,
   and required checks. Flag unrelated commits or unsafe ancestry before a
   draft is proposed.

## Draft

Build a title and body from repository evidence, not organization-specific
assumptions. Preserve exact issue-closing syntax, source literals, required
template sections, and existing media links. Do not invent tracker fields,
release versions, emojis, labels, reviewers, or AI footers.

When an exact-head pull request already exists, default to an update draft.
Read its current title/body and patch only evidence-backed sections. Preserve
unknown sections, user-authored notes, images, attachments, checklists, and
HTML comments unless the user explicitly removes them.

Write the proposed base/head, title, body, draft/update disposition, push
command, and exclusions to `.tigerkit/pr.md`. Show a bounded preview and stop
`Pending` at the publish checkpoint.

## Publish

After current-turn approval, recheck identity, branch, `HEAD`, base ref,
existing PR state, and duplicate PR detection. Abort on material drift.

Execute in this order:

1. push with explicit remote and `HEAD:<branch>` refspec, never force;
2. create one draft pull request or update the exact existing pull request;
3. reread the remote pull request and verify title, body, base/head, draft
   state, and URL.

A push succeeds but PR mutation fails is `Fail` with the pushed SHA and one
safe recovery command. Never create a second pull request to hide a partial
failure.
