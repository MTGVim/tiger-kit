# Triage mode

Triage mode is read-only and deterministic. It may inspect one explicit
repository, the current repository, or explicit repository arguments supplied
for this run. It does not own a persistent repository profile and must not
modify installed skill files or create user configuration implicitly.

## Collection

Resolve the authenticated GitHub login and repository list. Execute
`scripts/triage.mjs` directly with explicit `--repo owner/name` arguments, or
let it derive one current repository from `origin`. The script uses GitHub REST
endpoints, pagination, and rule-based classification; it emits JSON for the
agent to format.

Treat collection failures per repository as partial `Unverifiable`, not as an
empty result. Do not infer missing pages, check states, authors, or review
requests. Reread a pull request when mergeability is temporarily unknown.

## Classification

Present action-bearing states before waiting states:

1. merge conflict;
2. failing checks;
3. changes requested;
4. draft owned by the authenticated user;
5. reply needed on an owned pull request;
6. review requested from the authenticated user;
7. awaiting reviewer re-review.

The latest external message controls reply-needed detection. An older request
must not be resurrected after a newer `LGTM`, approval, or explicit no-action
review. A later author response moves the item to awaiting re-review only when
it follows the exact actionable review or change-request evidence.

## Result

Show repository, PR number/title, head/base, category, decisive evidence, and
one next action. Keep awaiting-re-review items compact. Omit approved and
ordinary review-waiting pull requests unless requested. Do not expose internal
self-check narration or raw API payloads.
