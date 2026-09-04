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
pattern without exposing an absolute user-level path. If the check fails, do not create
the evidence directory, edit `.gitignore`, or switch to an external path; return
`Unverifiable`.

Place binary evidence in the parent-provided or standalone run-owned evidence
directory. Only a bounded `README.md` AC-to-file evidence index may accompany it; do not
create a Markdown lifecycle ledger. Every cited screenshot must exist, be non-empty, and
be actually inspected. If the directory cannot be resolved, the image is missing, or
inspection fails, required browser evidence is `Unverifiable`.

Immediately after file-mediated authentication injection, stop the exact run-owned
loopback secret server, delete the mode-`0600`
`.tigerkit/secret-input/tk-browser-verify-<run-id>/token` file and its mode-`0700` run
directory, and verify that none remains. Apply this cleanup on success, failure,
interruption, and exception. Do not defer secret cleanup until browser-session cleanup.

Clean up success, failure, interruption, and exception paths in this order:

1. run-created pages/tabs;
2. run-created contexts;
3. direct browser instances started by this run;
4. exact owned processes, only when normal shutdown fails;
5. run-owned OS temporary baseline source trees after their servers have stopped.

Before forced termination, match the PID and profile against process arguments. Never
use `killall`, broad `pkill`, or task-name bulk termination. Preserve evidence directories, provider-owned and
attached browsers, user tabs/profiles, shared MCP/CDP instances, other verification runs,
and user-owned servers. Provider shutdown owns cleanup of its browser and temporary profile.
Report cleanup residue without changing the application verdict.
