# `CDP` fallback

Read this reference only when `CDP` was explicitly selected instead of `gh-attach`, or
when the user chose to continue with `CDP` after target write access was unavailable.

## Preparation and browser identification

After `git check-ignore -v` proves that a repository-tracked ignore rule covers it,
create `.tigerkit/tmp/tk-github-image-upload-to-pr/<run-id>/` as the run-owned staging
directory. Use a safe, descriptive filename as the image alt text. If the path is not
ignored, writable, or accessible to the browser, do not edit `.gitignore` or switch to an
external scratch path; return `Unverifiable`.

Use this browser order:

1. an authenticated existing `Chrome` session through `CDP` or `Chrome DevTools MCP`;
2. an authenticated persistent browser profile through `CDP` and `Playwright`;
3. stop as `Unverifiable` and explain how to restore `CDP` access.

For the first option, explain that `chrome://inspect/#remote-debugging`, `--autoConnect`
for `Chrome DevTools MCP`, and a one-time `Chrome` permission prompt may be required.
Do not print cookies, tokens, or private identity details. Do not launch `Orca` or
another desktop controller as a fallback.

`Chrome 136+` ignores remote-debugging switches for the default data directory. A
directly launched endpoint requires a dedicated `--user-data-dir` and one-time login.
Supported `--autoConnect` can connect to an existing profile only after the user's
explicit permission action. Do not trust a `DevToolsActivePort` file alone; verify the
current socket and browser endpoint.

## Upload and composer protection

Use the visible attachment control on the target PR page rather than relying on a
hidden file input. Poll with a bounded retry count until every `![Uploading ...]()`
placeholder becomes an actual `user-attachments/assets/...` URL or equivalent image
element. On timeout, preserve the last visible diagnostic.

Inspect the composer before entering anything. A non-empty user draft is a blocker;
do not overwrite or submit it. After collecting asset URLs, clear only run-owned
composer content and verify that the text area is empty and the comment button is
disabled. Do not submit an empty comment to test the upload.

## Rendering verification and cleanup

After the skill updates the requested body/comment, verify on the rendered PR page
that every asset appears as the expected image. Do not treat a placeholder, Markdown
presence, or fixed delay as success. Do not expose JWTs or query strings from signed
URLs.

Delete only the run-owned staging directory and verify its removal. If cleanup fails,
report the exact owned path and do not claim `Pass`. After an upload or verification
failure, do not submit a comment or silently retry through another path.

This procedure draws conceptually from
[`github-upload-image-to-pr`](https://github.com/tonkotsuboy/github-upload-image-to-pr)
without copying the upstream source.
