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
preserve exact body/comment placement. Insert that Markdown verbatim; add captions outside the generated block.
Keep display redaction separate from the private mutation input. Reject empty output, unexpected non-Markdown
output, links for another repository or reference, and output that omits any input
image.

The expected remote reference is `refs/uploads/issues/<pr-number>`. An upload may
create or update it before a later failure. After the command starts, do not silently
switch to `CDP` on failure. Report whether the selected body/comment changed and that
the upload reference may remain.

## Verification

Re-read the raw selected body/comment and compare the inserted Markdown byte-for-byte with the extension's generated
Markdown. For every asset, verify all of the following before `Pass`:

- The inserted URL resolves to image content, not a file-view HTML page. A `blob` page without a rendering parameter
  such as `raw=true` is not image content; that parameter is an example, not a required URL format for every route.
- An authenticated fetch of the same uploaded object returns non-empty, decodable image bytes with an `image/*` content
  type. A raw content endpoint at the upload ref is one option; verify the exact repository, commit/object and path match
  the inserted asset. A JSON metadata response, filename extension or successful HTTP status is insufficient.
- The authenticated browser session's rendered PR/comment actually loads each expected image; inspect the image itself
  and its load state (for example, nonzero natural dimensions and no broken-image state). `REST body_html` or
  `GraphQL bodyHTML` can establish markup presence, but an `<img>` element alone is not render proof.

Inspect `git/ref/uploads/issues/<pr-number>` in the target repository and verify that every linked upload commit/object
is reachable from that ref, including immutable commit URLs. The "commit does not belong to any branch" notice for an
upload ref is expected and does not by itself indicate failure.

Allow `GitHub` to rewrite rendered asset URLs to `private-user-images.githubusercontent.com`; compare the raw inserted
Markdown with the original output, not with rewritten browser URLs. Return `Fail` for altered Markdown, non-image bytes
or a known broken image. If authenticated fetching or browser-session rendering cannot be checked, report the concrete
limitation as `Unverifiable` instead of `Pass`, and preserve the actual remote state.
Redact only secret-bearing values in displayed diagnostics; preserve safe rendering parameters. Never expose signed
values in logs, artifacts, or the final response, and never feed redacted diagnostics back into the body/comment.

## Reviewed dependencies

Only these two distributions are trusted without another question:

- [`MTGVim/gh-attach@v0.7.0-mtgvim.1`](https://github.com/MTGVim/gh-attach/releases/tag/v0.7.0-mtgvim.1)
- [`enthus-appdev/gh-attach@v0.7.0`](https://github.com/enthus-appdev/gh-attach/releases/tag/v0.7.0)

The reviewed fork release has no application-source changes from upstream `v0.7.0`
and includes `LICENSE`, `THIRD_PARTY_NOTICES.txt`, and checksums. `TigerKit` does not
vendor the source, prebuilt binaries, or a checksum database.
