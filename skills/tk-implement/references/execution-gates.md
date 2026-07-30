# Implementation gates

Load only the sections that apply to the current unit.

## Tests and coverage

Use TDD when a meaningful public-behavior seam can fail before production code changes. Observe the expected red, implement, then observe green. A bug or regression with a useful seam needs a failing regression test before the fix.

New production behavior needs a durable automated test. Copy, documentation, pure configuration, and mechanical edits may omit a new test with a recorded reason. Run existing coverage commands and thresholds as-is; when no coverage tool exists, report `coverage: unavailable` rather than adding one.

If production behavior has no meaningful test seam, do not silently commit. Ask once whether to add a seam or approve a named deterministic alternative with its residual risk.

## Source UI writing

When source material defines user-visible text, preserve its exact spelling, case, spacing, punctuation, symbols, numbers, and meaningful line breaks unless the user explicitly approves a change. Compare source, current, and target text before mutation and again in the candidate/staged diff.

Missing comparison evidence is `Unverifiable`; an unresolved source/current conflict is `Blocked`; unauthorized drift is `Fail`.

## Browser verification

Visible UI or browser behavior uses `tk-browser-verify` before any browser-tool or verification-server call. The browser skill owns tool choice, runtime evidence, screenshots, and safety. Unit tests, DOM output, or build success do not replace required runtime evidence.

If browser verification is required but unavailable, return `Unverifiable`; do not bypass the skill with direct browser tools.

## Final review and commit

Run focused verification while implementing and the broadest relevant checks for the completed unit. Bind evidence to branch, `HEAD`, and diff/path scope.

Apply the built-in Standards/Spec review in `review-boundary.md`. Use at most one read-only independent reviewer for large work or material authentication, authorization, payment, privacy, migration/data-loss, dependency, concurrency, or public-API risk. The bounded flow is one review, one fix, one regression verification.

Immediately before commit, recheck branch, `HEAD`, staged paths, and pre-existing user changes. Commit exactly once only for `Pass`. Never broaden staging, bypass a failed hook, or call stale evidence current. Audit hook-created drift after commit through `review-boundary.md`.
