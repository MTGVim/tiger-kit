# `gh-attach` path

## Host CLI and authentication boundary

First determine whether the host provides a working `gh` executable. If it is absent or needs
host-level repair that the agent cannot safely perform, invoke `tk-wizard` with the exact
installation/repair completion signal and upload resume action. Do not install the host CLI as
an incidental upload dependency.

Interactive `gh auth login`, account/repository permission changes, and another user-only
authentication step also belong to `tk-wizard`. Perform no upload while that handoff is
pending. Reuse an already authenticated CLI non-interactively when `gh auth status` proves it;
ordinary auth inspection remains in this skill.

## Trust preflight without execution

Read `gh extension list` before running any extension command, including
`gh attach --help`. When that command succeeds, inspect the `REPO` and `VERSION` for
the single row whose `NAME` is exactly `gh attach`.

```text
reviewed-fork
  REPO=MTGVim/gh-attach
  VERSION=v0.7.0-mtgvim.1

reviewed-upstream
  REPO=enthus-appdev/gh-attach
  VERSION=v0.7.0

unreviewed-upstream
  REPO=enthus-appdev/gh-attach
  VERSION=<other proven version/ref>

absent
  gh extension list succeeded, but no gh attach row exists

unknown
  list failed; or the row is duplicate, incomplete, ambiguous, or belongs to
  another distribution; or provenance/version cannot be proved
```

A `GitHub CLI` extension is not an executable verified, signed, or endorsed by
`GitHub`. Successful `gh attach --help`, executable presence, a public repository, or
an assumed installation path is not trust evidence. If `gh extension list` output
cannot be interpreted safely, classify it as `unknown` rather than compensating with
internal layout knowledge or a loose parser.

Use `reviewed-fork` and `reviewed-upstream` without extra trust questions, warnings,
reinstallation, or fork replacement. For `unreviewed-upstream`, briefly explain the
supply-chain risk and require one explicit current-turn choice before execution:

- use the currently installed version;
- replace it with `gh extension install MTGVim/gh-attach --pin v0.7.0-mtgvim.1`;
- use the `CDP` fallback.

Do not execute or replace the installed extension before approval. For `unknown`, do
not execute the binary; offer provenance recovery, the reviewed fork, or `CDP`. For
`absent`, recommend the reviewed pinned fork and also offer `CDP`, but do not install
automatically. After the user selects and authorizes the reviewed fork, this skill may run the
pinned `gh extension install` command once; do not delegate that agent-executable step to
`tk-wizard`. Read `gh extension list` again and reclassify before executing the extension.

## Execution authority and operation

Only after execution is authorized, check `gh attach --help`, `gh auth status`, and
`.permissions.push` from `gh api repos/<owner>/<repo>`. Do not infer access from whether
the target is public or private. If authentication or write access needs a human action, hand
that exact action to `tk-wizard`; otherwise, if target write access is unavailable, do not
execute the extension and switch only to the user-selected `CDP` path.

Run:

```text
gh attach --repo <owner>/<repo> <pr-number> <image>...
```

Do not pass `--comment`. Collect only the generated image Markdown so the skill can
preserve exact body/comment placement. Reject empty output, unexpected non-Markdown
output, links for another repository or reference, and output that omits any input
image.

The expected remote reference is `refs/uploads/issues/<pr-number>`. An upload may
create or update it before a later failure. After the command starts, do not silently
switch to `CDP` on failure. Report whether the selected body/comment changed and that
the upload reference may remain.

## Verification

Re-read the raw selected body/comment and verify in `GitHub`-rendered HTML, such as
`REST body_html` or `GraphQL bodyHTML`, that every asset appears as an image element or
link. Inspect `git/ref/uploads/issues/<pr-number>` in the target repository and verify
that each generated link names that reference.

Allow `GitHub` to rewrite asset URLs to `private-user-images.githubusercontent.com`.
Do not claim `Pass` from Markdown presence or a successful update response alone. Do
not expose JWTs or query strings from signed URLs in logs, artifacts, or the final
response.

## Reviewed dependencies

Only these two distributions are trusted without another question:

- [`MTGVim/gh-attach@v0.7.0-mtgvim.1`](https://github.com/MTGVim/gh-attach/releases/tag/v0.7.0-mtgvim.1)
- [`enthus-appdev/gh-attach@v0.7.0`](https://github.com/enthus-appdev/gh-attach/releases/tag/v0.7.0)

The reviewed fork release has no application-source changes from upstream `v0.7.0`
and includes `LICENSE`, `THIRD_PARTY_NOTICES.txt`, and checksums. `TigerKit` does not
vendor the source, prebuilt binaries, or a checksum database.
