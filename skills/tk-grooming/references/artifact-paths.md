# Artifact Paths

Default repository-owned output to `.tigerkit/`: transient files in `tmp/<skill>/<run-id>/`, verification evidence in `evidence/<skill>/<run-id>/`, explanations in `explanations/`, lessons in their owner-specific learning home, and retrospectives in `retro/`. Preserve existing owner-specific paths and explicit user-selected final destinations. Create artifacts only when the active task calls for them. For repository-local artifacts, before writing, verify the repository root, no tracked `.tigerkit` paths, and safe nonsymlink destinations. From the repository root, run `git ls-files -- .tigerkit .tigerkit/` to check tracking, then `git check-ignore -q -- .tigerkit/` to check effective exclusion. Exit 0 means leave ignore files unchanged, including when exclusion comes from `core.excludesFile` (such as configured `~/.gitignore`), the default global ignore file, or `.git/info/exclude`; a missing repository `.gitignore` or missing literal entry is not evidence of missing coverage. Only exit 1 permits creating the root `.gitignore` or appending `/.tigerkit/`, preserving existing bytes and line endings, then rerunning the same check before writing. Any other exit status or command failure blocks the file branch without an ignore edit. Use `git check-ignore -v -- .tigerkit/` only to diagnose the source; a printed negated pattern is not proof of exclusion. This narrow ignore setup is part of an authorized artifact write even for a read-only task; it grants no other source/config/index/commit/publication authority. Existing effective ignore rules need no edit. Do not untrack files or follow a symlinked/nonregular `.gitignore`; if unsafe, unwritable, still unignored, or no repository is identified, hold only the file branch as `Blocked | Unverifiable` and follow the recovery procedure below, without an OS-temp fallback. Briefly report an ignore edit; never stage or commit it solely for setup. Atomic replacement may use a run-owned sibling temporary file on the destination filesystem; clean it after success. External tool caches and isolated test fixtures retain their tool-owned lifecycle.


## Optional durable final artifacts

Only `tk-explain`, `tk-explain-diff` and `tk-teach` may use `artifacts.durableRoot` for
final explanations and newly created learning homes. Explicit destinations win; transient
`tmp/` and `evidence/` stay repository-local. Before the first eligible artifact, run the
package-local `scripts/durable_artifacts.py status`. If `durableRoot` is absent and an
interactive question is possible, ask once before saving whether to use an outside-repository
location, suggesting `~/.tigerkit` and explaining that removing a worktree also removes its
ignored `.tigerkit/` files. Use the accepted path, not an inferred preference.
After the answer, record only that answer using `choose --root <path> --repo <repository>`
or `choose --disable --repo <repository>`. If another writer changes settings before the
choice is recorded, re-read status and preserve any existing choice; do not overwrite it. If the
key remains absent, retry using the already approved answer. A null choice means deliberately
disabled; do not ask again when the key exists. If questioning is unavailable, use the existing default
without recording a choice. Preserve other settings and never replace malformed settings.

For an eligible final artifact, use `resolve --repo <repository> --kind explanations|study
--slug <safe-topic-slug>`. Pass `--explicit <path>` for a user-selected destination; a slug is unnecessary in that case. A configured
root yields `<root>/<repo-key>/explanations/<slug>.html` or `<root>/<repo-key>/study/<slug>/`;
otherwise use the existing owner default. Use `--create` only when ready to create an authorized
durable destination. The helper derives the key from the actual Git common directory, rejects
symlink paths and roots within any worktree, and creates new directories with private mode.
For a durable path, verify repository identity and safe destination but skip `.tigerkit/` Git
ignore setup solely for that final path. Apply ordinary exclusion checks to any local scratch.
Existing default targets get numeric suffixes; explicit targets require overwrite authority.
Invalid configuration falls back without modifying it; report its warning once. Do not move or
copy existing artifacts. Existing teach homes remain where they are and are identity-checked
before continuation; use the owner's resume procedure to inspect durable and legacy candidates.


## Recovering a blocked file branch

Apply [prerequisite recovery](questions.md#unmet-prerequisites) within existing authority. If no Git repository is identified, hold artifact writes and offer two concrete options: initialize the current folder, naming its absolute path and the new local Git metadata, or create the artifact in an existing repository selected by the user. Obtain separate explicit approval for initialization unless the same target and action were already approved; an artifact request alone is not initialization approval. Do not automatically initialize, use a temporary directory to bypass checks, commit, or publish. After approval, recheck the selected folder, initialize only if still needed and approved, then verify the repository root and all exclusion/safe-path checks above before completing the original artifact. A missing exclusion alone follows the already-authorized minimal ignore setup above; it needs no extra approval. If recovery is declined or unavailable, continue independent work and report the undelivered file and missing decision.

Keep the shell working directory at the repository root while addressing run-owned files with absolute paths or `git -C`; use a subshell only when a tool requires a different cwd. Never `cd` into a run-owned directory that will be deleted, and never delete the current working directory or one of its ancestors. Run cleanup from the repository root.
Write every cleanup deletion with the literal, fully resolved absolute run-owned path already recorded in this run. Never derive a deletion target from command substitution, a path file read back, or a glob piped through `head` or `tail`. If the exact literal path is unknown, list the candidate paths and stop instead of deleting.

Git exclusion does not guarantee exclusion from build tools that scan the worktree: [Tailwind v4 automatic source detection](https://tailwindcss.com/docs/detecting-classes-in-source-files#which-files-are-scanned) excludes paths in `.gitignore`, while user-level excludes alone left `.tigerkit/` in the confirmed build scan. Build-scan exclusions are a separate repository-local decision; this fact does not change the exit-0 no-edit rule above.

## User-editable temporary input

Apply this branch only when the task requires the user to supply values through a newly created temporary file. Use a UTF-8 `input.json` containing a pretty-printed plain JSON object with double-quoted, task-specific keys; initialize missing text values to `""` and prefill only confirmed non-secret defaults. Include only fields needed for the pending step. For a single token, create:

```json
{
  "token": ""
}
```

Use the same object shape for one or several fields. Keep field meanings, required types and editing instructions outside the file; do not use JSON-LD, comments, trailing commas, instructional placeholder values or a zero-byte/raw-text file. This rule does not convert existing user files, final documents, code/config files, machine transport, or conversational questions into JSON and grants no new write authority.

Put ordinary input in `.tigerkit/tmp/<skill>/<run-id>/input.json`. If any field is secret, keep the entire object in `.tigerkit/secret-input/<skill>-<run-id>/input.json` with directory `0700` and file `0600`. Apply the exclusion, nonsymlink and ownership checks above; create exclusively and never overwrite an unrelated existing file. Require a regular file with one hard link, inside the safe run-owned directory. Reuse an existing run-owned pending file without resetting entered values. Never prefill secrets or expose their contents in chat, commands, logs, receipts or parser errors.

Before the handoff, finish preparation and release this run's waiting-related server/browser resources using their owning cleanup procedure; never stop user-owned or other-run resources. Do not start or hold servers or browsers while waiting for input. Record initial metadata privately and start a bounded, run-owned change watcher in the background before presenting the paths, only when the host supports it across the turn boundary. This is a finite input wait, not a daemon or scheduled task. A normal final-message handoff is not cancellation: preserve the pending file for the supported wait or later resumption. If the host cannot sustain it or resume on completion, disclose the limitation and exact resumption step; preserve the same pending file and never promise automatic continuation.

Present the input handoff as the final user-visible text message of the turn, then end the turn with no further tool calls. Do not deliver it only as a progress/thinking update that the host may summarize. Put each actual path alone on its own line, complete and unabbreviated, with no trailing particle or punctuation. Show both repository-relative and absolute paths, the secret-free initial template, and which fields the user must fill and save. Offer a host-appropriate clipboard-to-field command only when useful; it must JSON-serialize the clipboard value into the named field while preserving other fields, never overwrite the object with raw clipboard text or place values in arguments/history. Do not automatically launch an editor, opener, GUI, terminal UI or change focus. Open the shown path only on explicit user request.

The watcher uses bounded metadata-change polling without reporting content or metadata values. File existence, non-zero size or modification alone is not completion: the seeded template is already non-empty. After a change, a trusted local reader may parse without returning contents, validate the exact requested keys/types and nonblank required text fields, and report only `Pending | Ready | Unsafe`. Reject duplicate or unexpected keys. An unchanged template, missing/blank field, malformed or partly saved JSON stays `Pending`; preserve the user's bytes and wait for the next change. Explain only the missing field name or syntax requirement, never raw values or parser excerpts. Before use, recheck safe path, ownership and secret permissions and reparse the current file; validate and consume the same snapshot. Unsafe replacement stops the file branch as `Blocked | Unverifiable`.

When ready and the host can resume execution, continue the exact authorized pending step without requesting a separate user completion message. Renew bounded waits only while the host-supported task remains active; if the host cannot wait, preserve the same run-owned path and explain resumption. On resumption, privately validate the existing run-owned file once before waiting for another change. Pass only validated fields to the approved consumer, never the JSON wrapper as a credential. Delete one-time secret input and its run directory immediately after consumption on success, failure or exception and verify no residue. Application authentication follows the scoped exception below; ordinary input follows its run-owned temporary lifecycle. Preserve the existing host-native hidden-input option when safer.

For application authentication, read [worktree-local authentication](authentication.md) only when that branch is needed.
