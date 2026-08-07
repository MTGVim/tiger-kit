# Browser session lifecycle

Classify session ownership before browser interaction and clean up only
run-owned resources regardless of verdict. Every Guard and Verdict run creates
an evidence ledger before its first persisted capture and leaves at least one
non-empty screenshot plus actual image inspection. This applies to native browsers,
Playwright-compatible drivers, MCP, and CDP.

## Session ownership

An **owned session** is a browser, context, window, tab, page, or process
created by this verification run. A provider that lazily launches on its first
`list`, `snapshot`, or `navigate` call makes that resource owned. An initial
`about:blank` that was not proven to pre-exist does not make it attached.

An **attached session** was independently proven to exist before this run and
was only attached for verification. Never close its browser, pre-existing
windows/tabs, or process. Close only pages clearly created by this run. Unknown
ownership means do not close.

## Chrome headless-new launch

Every new owned Chrome/Chromium process includes exact `--headless=new`.
Before the first browser call, record binary, effective arguments, PID or
provider process ID, and isolated `user-data-dir`. Provider defaults are not
proof.

If auto-launch cannot inject and prove the argument, attach to a directly
started verified Chrome endpoint. Never retry headed after headless failure.
Use a pre-approved headed exception only for user-completed interactive auth.

Perform interactive login only in a user-local profile outside the repository.
After auth, close the headed browser, prove process exit and profile-lock
release, and restart the same binary/profile with `--headless=new`. Verify
arguments and authenticated target state before product evidence. A failed
handoff is `Unverifiable`. Preserve the user's persistent auth profile at
cleanup.

## CDP availability and profile recovery

Do not treat the user's default Chrome profile as a reusable
`--remote-debugging-port` launch target. Chrome 136+ ignores remote-debugging
switches against its default data directory. A directly started CDP endpoint
therefore needs a dedicated `--user-data-dir` outside the repository; when
authentication is required, that profile needs one user-completed login before
the verified headless restart described above. See Chrome's
[remote-debugging security change](https://developer.chrome.com/blog/remote-debugging-port).

Where the installed Chrome and Chrome DevTools MCP support it,
`--autoConnect` may attach to an already running signed-in profile through
`chrome://inspect/#remote-debugging` only after the user's explicit Chrome
Allow action. Classify that browser as attached: never close its process,
pre-existing windows, or tabs. Follow the
[Chrome DevTools MCP running-instance contract](https://github.com/ChromeDevTools/chrome-devtools-mcp#connecting-to-a-running-chrome-instance),
including its supported Chrome version and approval prompt.

`DevToolsActivePort`, a saved port number, or a prior browser UUID can be
stale. Availability requires a current socket connection and successful
endpoint/browser inspection. If no authenticated live endpoint or safe
dedicated-profile recovery exists, return `Unverifiable` with the two
supported recovery paths; do not launch a desktop-controller fallback.

## First-run UI suppression

When supported, prefer native options such as:

```text
--headless=new
--no-first-run
--no-default-browser-check
```

Do not pass Chrome flags to an unknown browser or retroactively to an attached
session. An unsupported suppression flag alone does not stop verification, and
no flag may alter target-application behavior.

## Remaining onboarding

Before verification, inspect browser-owned login, sync, or setup UI. Only
unambiguous skip/later/continue-without-login actions and closing run-owned
onboarding tabs/windows are safe. Never sign into a browser account, enable
sync, change default-browser settings, register a persistent profile, request
credentials, or guess an ambiguous consent action.

If browser UI cannot be distinguished from the target or safely dismissed,
return `Unverifiable`.

## Evidence ledger

Resolve `.tigerkit/browser-verify/runs/<run-id>/` to an absolute path before the
first capture. Record `Evidence directory: <absolute path>` and each
`Screenshot: <path>` in the result. A missing screenshot, empty file, failed
image inspection, or unresolved directory is `Unverifiable`; never report a
relative directory as a successful evidence location.

## Cleanup

On success, failure, interruption, or exception, attempt cleanup in order:

1. run-created pages/tabs;
2. run-created contexts;
3. run-started browser instances;
4. only when normal shutdown failed, the exact proven owned process.

Record PID and exact `user-data-dir` at launch. Before forced termination,
match both against process arguments; a shared port is not ownership. If server
auto-open could not be suppressed, close only tabs created by this run.

Never use `killall`, `pkill chrome`, broad `pkill -f`, or task-name bulk kills.
Do not close unknown PIDs, user windows/tabs/processes, shared MCP/CDP
browsers, other verification runs, or delete user profiles.

Closing the last page is not proof that a provider-owned browser exited. If no
explicit close method or process identifier exists, do not guess-kill; report
the remaining owned session under `Unverified`. Cleanup failure does not change
the application verdict; `Unverified` is a result section, not another verdict.

User-facing progress and receipt prose follows the user's language.
