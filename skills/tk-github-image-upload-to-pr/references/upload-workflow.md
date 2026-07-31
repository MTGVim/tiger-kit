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

## Staging and browser

Use a run-owned directory under the browser automation workspace. Do not use
`/tmp` as the default staging location because the browser may not be able
to access it. Use descriptive filenames that are safe as image alt text.

The browser order is:

1. authenticated existing Chrome session through CDP or Chrome DevTools MCP;
2. authenticated persistent browser profile through CDP/Playwright;
3. stop with `Unverifiable` and explain the CDP recovery path.

For the first option, explain that the user may need
`chrome://inspect/#remote-debugging`, Chrome DevTools MCP
`--autoConnect`, and the one-time Chrome Allow prompt. Do not print cookies,
tokens, or private identity details. Do not launch Orca or another desktop
controller as fallback.

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

## PR body update

Insert the generated image Markdown at the requested location. If no location
is given, prefer the exact source heading `## 스크린샷`; if it is absent,
insert before the AI footer or append to the body. Keep the original body
otherwise byte-stable where possible. Update only the body through the GitHub
API or equivalent and verify that the returned body contains every asset.

## Verification and cleanup

Re-read the PR body, then verify the rendered PR page contains the image alt
text or image link. GitHub may rewrite an asset URL to
`private-user-images.githubusercontent.com`; this is a successful rewrite,
not a mismatch. Do not expose signed URL JWTs or query strings in logs,
artifacts, or the final response.

Delete only the run-owned staging directory and confirm its absence. If
cleanup fails, report the exact owned path and do not claim `Pass`. If upload
or verification fails, report whether the PR body was changed; do not retry by
submitting a comment.

## Upstream reference

The workflow is adapted conceptually from
[github-upload-image-to-pr](https://github.com/tonkotsuboy/github-upload-image-to-pr).
TigerKit adds its own CDP-first, browser-boundary, cleanup, and safety
contract; no upstream source is copied into this package.
