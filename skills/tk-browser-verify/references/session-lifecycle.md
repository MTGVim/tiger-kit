# Headless session lifecycle

Classify ownership before interaction. An owned browser/context/page/process was
created by this run; an attached resource is independently proven to have existed
before the run. Close only owned resources. If ownership is unknown, do not close it.

For a direct run-owned Chrome/Chromium launch, use a run-owned isolated profile and an
effective modern headless setting. For a managed provider, the provider owns its server,
browser process, and provider profile; the verification run owns only the pages, scenario
contexts, evidence, and development server that it creates. Prefer an ephemeral provider
profile, but allow a headless dedicated persistent provider profile with a disclosed storage
limitation. Never reuse the user's default browsing profile. If effective headless mode or
ownership cannot be proven after the permitted managed-launch bootstrap, return
`Unverifiable`; do not retry with a visible browser.

Before the first write to repository-local evidence, prove that
`git ls-files -- .tigerkit/` returns no tracked path and
`git check-ignore -q -- .tigerkit/` succeeds. Classify the matching rule from
`git check-ignore -v` as `per-directory | info-exclude | user-level` and record the
pattern without exposing an absolute user-level path. Use the owning SKILL.md Artifact Paths
setup when ignore coverage is missing. If checks still fail, do not create evidence or
switch to an external path; return `Unverifiable`.

Place binary evidence in the parent-provided or standalone run-owned evidence
directory. Only a bounded `README.md` AC-to-file evidence index may accompany it; do not
create a Markdown lifecycle ledger. Every cited screenshot must exist, be non-empty, and
be actually inspected. If the directory cannot be resolved, the image is missing, or
inspection fails, required browser evidence is `Unverifiable`.

After file-mediated authentication injection, independently verify the authenticated state.
For an explicitly authorized shared development cache, commit the verified token atomically
from the *same* validated input file and owned refresh claim; do not retain or cache a token
that did not authenticate successfully. Whether cache commit succeeds or fails, immediately
stop the exact run-owned loopback secret server, delete the mode-`0600`
`.tigerkit/secret-input/tk-browser-verify-<run-id>/input.json` file and its mode-`0700` run
directory, and verify none remains. On failure, interruption or exception, always remove
temporary secret input as well; release only this run's pending claim where possible.
Do not defer secret cleanup until browser-session cleanup.

After any baseline, after, or acceptance capture, close run-owned browser resources and stop the
run-owned development server immediately through the exact supervisor run ID when using the
project-scoped guard. Do not release or assume release of the Git-common-dir lock until the
run-owned child shutdown is confirmed; never delete a held lock file to break a wait.
Waiting for an active user's input or token update is not an excuse to retain the lease.
If an abnormal exit leaves a suspected server orphan, report it for ownership-based
recovery without broad process termination. Persist the inspected evidence and a replay recipe, not
live processes or an authenticated browser profile. A parent continuing to implement or review
must never hold these processes merely to avoid a later startup; an immediate final-head replay
starts a fresh owned browser/server and reestablishes the scoped authentication state if required.
The immutable baseline provenance stays usable for comparable after capture when viewport,
DPR, fonts, UI state, target environment, and replay conditions are independently reproduced.
When those conditions cannot be reproduced, report `Unverifiable`, not a silently comparable pair.

On interruption, timeout, failed capture, or parent handoff, perform the same owned-resource
cleanup; do not keep background dev servers during a suspended workflow. Cleanup failures and
unowned/provider-owned resources are reported rather than terminated blindly.

Clean up success, failure, interruption, and exception paths in this order:

1. run-created pages/tabs;
2. run-created contexts;
3. direct browser instances started by this run;
4. run-owned development server (graceful stop first, then exact verified process group if needed);
5. run-owned `.tigerkit/tmp/tk-browser-verify/<run-id>/baseline-source/` trees after their servers have stopped.

Before forced termination, match the PID and profile against process arguments. Never
use `killall`, broad `pkill`, or task-name bulk termination. Preserve evidence directories, provider-owned and
attached browsers, user tabs/profiles, shared MCP/CDP instances, other verification runs,
and user-owned servers. Provider shutdown owns cleanup of its browser and temporary profile.
Report cleanup residue without changing the application verdict.
