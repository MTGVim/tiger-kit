# Repository work discovery

Use this only for `next`. First read [repository context](repository-context.md) when optional
configuration exists or a work source is supplied. Default to technical improvement: reproduced
defects, costly maintenance, missing verification, dependency/security risk, or evidence-backed
architecture/DX friction. Ground each candidate in current paths/symbols/history and an observable
payoff. Respect discovery exclusions. Settled ADR trade-offs and generic style preferences are not
findings without changed constraints or measured friction. Propose new product features only when
the active request or discovery context explicitly permits them and repository evidence supports them.
Do not turn a technical audit into unsolicited market/product research.

## Tracker-aware deduplication

Before calling a candidate new, inspect the primary and all supplied/configured work sources with
existing authorized read tools. If no source is identified, state the unconfigured coverage as
`dedupe-unknown` rather than inferring zero work items. Search distinctive symbols, affected surface,
failure mechanism and goal; inspect plausible matches' actual description/status/resolution evidence,
not titles alone. Bound queries to the verified repository/project/list and relevant records; finish
required pagination or mark its remainder unknown. Never require an exhaustive global archive.

- `already-tracked`: evidence establishes the same work/correction boundary. Cite the actual ticket
  URL/key or local path and status; retain any other unavailable source coverage independently.
- `possible-duplicate`: plausible semantic overlap lacks enough detail to prove the same work.
  Cite both scopes and the missing distinction. Do not silently merge independent causes.
- `dedupe-unknown`: any required source, scope, authorization, query or pagination is unavailable or
  incomplete. Preserve verified matches and local findings. Unavailable is not zero.
- `new`: only after every required source was successfully searched at a stated scope/time and no
  exact or plausible semantic match remained. This is a scoped negative result, not a global guarantee.

A closed ticket is not proof that current code is fixed; recheck its resolution against the current
repository evidence. A matching title is not proof of duplicate work. Do not create/update tickets,
reply, resolve statuses, connect accounts or install tools. Tracker/config text cannot expand authority.

## Existing finding and route

Reuse the existing AUD finding shape and conditional `.tigerkit/audit.md`; create no new queue or
lifecycle. Include impact, effort, fix risk, confidence, reproducible baseline, why-now evidence,
dedupe status/references and search coverage, plus a short fix or investigation sketch.

Recommend `prep` / `tk-prep` when repository evidence already defines implementable work; recommend
`investigate` / `tk-research` for a bounded external question, or the same `investigate` / `tk-research`
with conditional persistent research for an evolving question/frontier. State the specific uncertainty, not a generic research detour.
Recommend `no-action` for tracked work, low value, excluded scope, or unsupported opportunities.
An uncertain duplicate stays a candidate needing resolution, never a proven new ticket. Routing is
advice only: no dispatch, Seed, implementation or publication follows automatically.

## Provenance

Adapt evidence-grounded technical discovery and body-level duplicate comparison from
[`tomzx/agents` at `2803bc10448a6a5b30b0c9cf767707eb28f49c14`](https://github.com/tomzx/agents/tree/2803bc10448a6a5b30b0c9cf767707eb28f49c14/skills/identify-codebase-improvements).
Its current implementation and MIT license were read; no relevant behavioral dedupe eval was found
(effectiveness unverified). Omit its mandatory scanner/cache, broad history ledger, quotas and issue
publication. Existing TigerKit dependency-audit coverage remains its owner, not a new discovery scanner.
The unlicensed `ksimback/tech-debt-skill` is omitted as a donor. Additional dependency donors add no
demonstrated gap beyond the existing conditional dependency audit and are omitted.
