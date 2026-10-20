# Native video attachments

Read only for an explicitly selected MP4 or optional motion supplement; the existing image/GIF
extension and CDP routes keep their own guards. Accept H.264 MP4 with optional AAC mono audio.
Inspect local MIME/container, dimensions/duration and decoded frames before upload. Preserve the
selected PR/comment and actual write authority. Default video budget is 10MB unless the target
owner's paid-plan allowance is proved; image/GIF limits and encoding targets are different.

## Native CLI route

Inspect the host's actual `gh pr edit --help` and authentication before choosing the built-in
`--attach` capability. The extension command `gh attach` is a different interface. Do not install
or upgrade gh implicitly. Native CLI attachment supports the PR body here; do not use `--edit-last`
to guess a selected comment. For a comment target use only an explicitly selected capable CDP route
or report the missing capability. Never create a new comment as a workaround.

For an existing PR body, write a run-owned UTF-8 body file preserving all unrelated bytes and the
existing screenshot section/pairs. Add a separate motion section with observed-flow captions and
one video placeholder alone in its paragraph:

Use a Markdown image reference with empty alt text and the actual absolute video path;
keep the entire reference alone in its paragraph before the command.

Run `gh pr edit <number> --repo <owner/repo> --body-file <file> --attach <exact-video>`.
This command uploads AND changes the body; do not perform a second body replacement afterward.
Use the native CLI's documented video rewrite, not an image table or inline paragraph link.
Never copy the extension's `refs/uploads/issues` reachability test to native attachments.
This route has no such ref. A failed command may already have changed remote state: reread it
and report partial success before any retry; never switch routes silently.

## Verification

Reread the raw body and require one reference to each uploaded object in the intended standalone
position. Authenticated-fetch the exact object, require nonempty `video/mp4` bytes and decode them
with an available trusted media decoder. Check expected duration/dimensions, video and selected
audio streams. Then inspect the rendered player: metadata loads and currentTime advances after
playback. An HTML video element alone does not prove playback. When browser playback is unavailable,
report upload-byte verification separately and playback as `Unverifiable`, not a full media Pass.
Keep signed fetch values private and never feed redacted diagnostic URLs back into the body.
Clean only this run's staging/body files. Optional media failure does not invalidate the independently
verified application or required screenshot publication; an explicitly requested media delivery
remains incomplete and must be reported as such.
