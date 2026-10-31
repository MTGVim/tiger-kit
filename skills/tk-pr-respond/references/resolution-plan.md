# Resolution plan details

At minimum, cover:

- each finding's disposition, causal evidence, and whether it changes code
- implementation approach and existing code to reuse
- how unnecessary complexity will be avoided
- regression and new-test plan
- any approved follow-up issue creation; otherwise state that follow-ups will not be ticketed
- any special security or user-experience concerns
- the `tk-browser-verify` plan for browser-visible changes
- bounded publication scope for push/reply/resolve/re-review
- whether the exact PR needs a base update or rebase, with the evidence and route if included
- practical execution shape: reply-only, direct, or SDD

When the plan covers two or more findings, present them as one narrow GFM table with
columns for location, finding, kind (`종류` in Korean output), disposition and approach. For kind, reuse the
reviewer's own category when present; otherwise use one of comment, refactor, test,
logic, type or conflict. Keep long evidence below the table instead of inside cells.

For every code-changing route, keep the semantic Review Plan from the code-change reference in the approved current
interaction even when no Seed is needed. Do not expose reviewer/model/worker routing as part of the user plan.

For a code-changing plan, inspect the actual repository test surface and use [behavior-first testing](../../tk-engineering/references/testing.md)
to resolve RED feasibility or pre-edit GREEN for behavior-preserving refactoring, the focused command, required suite,
realistic mutation, and any `N/A` or engineering exception.
Explain the practical route among reply-only, direct+TDD, and SDD+TDD without exposing an internal classification form.
Once a code-changing route is selected, read [code-change execution](code-change.md) before requesting approval;
use its workspace and Seed sections for the plan, but perform no mutation until approval.

Send feedback/CI failures with an obvious cause and exact regression seam directly through the existing testing path.
Lazy-load [shared diagnosis](../../tk-engineering/references/diagnosis.md) only for unknown-cause, intermittent/flaky, performance, or
difficult-to-reproduce hard CI/regression cases, and establish a red-capable feedback loop before a fix hypothesis.
Do not lock the first guess into a change without evidence that such a loop cannot be established.

TigerKit decides only `reply-only | direct | SDD`; host/user model selection remains outside durable artifacts.
Do not mark the task `Blocked` merely because model-control capability is unavailable.

