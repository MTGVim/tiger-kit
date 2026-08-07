# Upload workflow

## Preflight

- Resolve the repository from the executing checkout's `origin`; do not
  hardcode TigerKit.
- Resolve an existing PR with `gh pr view --json number,url,body` or an
  equivalent read operation.
- Validate every input path as a regular image file and reject paths outside
  the allowed workspace boundary when the browser cannot access them.
- Read the complete existing PR body and preserve its warning, notes,
  checklist, links, images, footer, and line endings.
- Default to the PR body. Use a comment only when the user names the comment
  target or explicitly asks for comment insertion.
- When `evidence_required: true`, accept only a producer handoff from
  `tk-browser-verify` or `tk-prototype`; do not infer a requirement from
  the presence of arbitrary image files.
- Probe `gh attach --help`, `gh auth status`, and target repository
  `.permissions.push` through `gh api repos/<owner>/<repo>`. Do not infer
  capability from public/private visibility.

## Route selection and installation

Use `gh-attach` when `gh attach --help` succeeds, the current `gh` session
is authenticated, and target repository write capability is true.

When the extension is absent, stop before browser identity or mutation gates
and ask one decision:

- **Recommended:** approve
  `gh extension install MTGVim/gh-attach --pin v0.7.0-mtgvim.1`;
- continue now through CDP, which may require a dedicated profile and one-time
  GitHub login.

Never install, update, or replace the extension automatically. Do not offer the
unreviewed upstream, an unpinned install, secret gist, or public image host as
an equivalent. When the extension is installed but target write capability is
unavailable, explain that result and continue to the CDP route without an
installation question.

## Reviewed extension route

Run:

```text
gh attach --repo <owner>/<repo> <pr-number> <image>...
```

Do not pass `--comment`: capture only the generated image Markdown so this
skill retains exact body/comment placement. Reject empty output, unexpected
non-Markdown output, a different repository/ref, or a generated link that does
not cover every input image.

The expected remote ref is `refs/uploads/issues/<pr-number>`. An upload may
create or update that ref before a later failure. Once the command starts, do
not silently switch to CDP; stop, report whether the selected body/comment
changed, and state that the upload ref may remain.

## CDP staging and browser

Use this route only after explicit selection or unavailable target write
capability. Create a run-owned directory under the browser automation
workspace. Do not use `/tmp` as the default staging location because the
browser may not be able to access it. Use descriptive filenames that are safe
as image alt text.

The browser order is:

1. authenticated existing Chrome session through CDP or Chrome DevTools MCP;
2. authenticated persistent browser profile through CDP/Playwright;
3. stop with `Unverifiable` and explain the CDP recovery path.

For the first option, explain that the user may need
`chrome://inspect/#remote-debugging`, Chrome DevTools MCP
`--autoConnect`, and the one-time Chrome Allow prompt. Do not print cookies,
tokens, or private identity details. Do not launch Orca or another desktop
controller as fallback.

Chrome 136+ ignores remote-debugging switches against its default data
directory; do not promise that relaunching the user's default profile with a
port will work. A directly launched endpoint needs a dedicated
`--user-data-dir` and one-time login. Where the installed Chrome/DevTools MCP
supports it, `--autoConnect` may attach to an already running profile only
after the user's explicit Allow action. A `DevToolsActivePort` file is not
availability evidence; verify the current socket and browser endpoint.

## Upload and composer safety

Open the target PR page and use the visible attachment control. Do not depend
on a hidden file input. Wait for each `![Uploading ...]()` placeholder to
become a real `user-attachments/assets/...` URL or equivalent image element.
Poll with a bounded timeout and preserve the last visible diagnostic on
failure.

Before typing, inspect the composer. A non-empty user draft is a blocker; do
not replace it. After asset URLs are captured, clear only the run-owned
composer content and verify that the textarea is empty and the comment button
is disabled. Never submit an empty comment to test the upload.

## Body or comment update

Insert the generated image Markdown at the requested location. If no location
is given, prefer the exact source heading `## 스크린샷`; if it is absent,
insert before the AI footer or append to the body. Keep the original body
otherwise byte-stable where possible. Update only the body through the GitHub
API or equivalent and verify that the returned body contains every asset.
For an explicitly selected existing comment, update only that comment and
preserve its unrelated content; never submit a temporary composer comment.

## Verification and cleanup

Re-read the selected body/comment source. Then request GitHub-rendered HTML,
such as REST `body_html` with the HTML media type or GraphQL `bodyHTML`, and
verify that every generated asset is represented by the expected image
element/link. For the reviewed extension route, also verify
`git/ref/uploads/issues/<pr-number>` in the target repository and that each
generated link names that ref. For CDP, verify the rendered PR page; GitHub may
rewrite an asset URL to `private-user-images.githubusercontent.com`, which is
a successful rewrite, not a mismatch. Markdown presence or a successful
update response alone is never `Pass`. Do not expose signed URL JWTs or query
strings in logs, artifacts, or the final response.

Delete only a run-owned staging directory and confirm its absence. If cleanup
fails, report the exact owned path and do not claim `Pass`. If upload or
verification fails, report whether the selected body/comment changed; do not
retry by submitting a comment or silently changing routes.

## Producer handoff

The handoff is valid only when it carries:

```text
evidence_required: true
producer: tk-browser-verify | tk-prototype
evidence_directory: <absolute run-owned path>
artifacts:
  - path: <absolute non-empty image path>
    criterion: <criterion or caption>
    inspected: true
```

For `tk-browser-verify`, require the producer's `Pass` result and its
existing `Evidence directory` and `Screenshot` entries. For
`tk-prototype`, require the tested screenshot path and actual image
inspection; do not describe a Guard comparison as an official runtime verdict.
If the handoff is required but missing or invalid, return `Blocked` before
upload. The parent may keep a created PR, but must report
`evidence_state: blocked` rather than full completion.

## Reviewed dependency

The controlled install is
[`MTGVim/gh-attach@v0.7.0-mtgvim.1`](https://github.com/MTGVim/gh-attach/releases/tag/v0.7.0-mtgvim.1),
a reviewed fork of the MIT-licensed `enthus-appdev/gh-attach@v0.7.0`.
Its release includes `LICENSE`, `THIRD_PARTY_NOTICES.txt`, and checksums.
TigerKit does not vendor or auto-install its source.

The CDP workflow is adapted conceptually from
[`github-upload-image-to-pr`](https://github.com/tonkotsuboy/github-upload-image-to-pr);
no upstream source is copied into this package.
