# Design choice evidence

Before presenting a design choice, read the PR body, linked ticket and relevant parent/discussion,
and the cross-team contracts it depends on. Inspect open counterpart PRs changing that same API:
use changed file paths as well as keywords, and inspect the bounded open list before claiming none
exist. State unavailable evidence in one or two lines. Resolve existing edit/copy behavior and a
proposed document's repository convention, tracking and ignore status before asking about them.
When the PR body or linked ticket references a precedent or sibling PR for the same change in another
repository, inspect how it settled the same choice before recommending; cite the evidence and explain
any deliberate divergence. Limit cross-repository precedent lookup to referenced PRs and same-ticket-family
PRs within the configured scope; without such a reference, do not search other repositories for precedents.
An unmerged counterpart change cannot supersede an agreed task requirement: retain that premise,
disclose the conflict as a verification item, and change the requirement only with user direction.
