# Upstream issue anonymization

Use this only in a consumer repository for a TigerKit-origin `tk-*` skill.

## Provenance gate

Verify:

1. TigerKit origin from metadata/path;
2. installed ref/version or source snapshot;
3. consumer-local edits or overrides;
4. reproduction against unmodified TigerKit source when possible;
5. separation between local configuration and upstream contract behavior.

When an installed skill has no Git ref or version but a canonical upstream source is known,
retrieve the current upstream source and compare the target passage before downgrading provenance.
If retrieval or comparison is unavailable, preserve the verified local evidence as an
`installed snapshot observation`, ask the maintainer to verify current upstream `HEAD`, use
`upstream-unverifiable`, and do not present it as an upstream contract proposal. A consumer-only
behavioral reproduction remains `local-only`.

## Proposal eligibility gate

Do not write a proposed title, body, or draft-template section before verifying all of:

1. canonical origin and exact current upstream ref, snapshot, or content hash;
2. claim type `documentary | behavioral`;
3. either exact current source location, quote, and adjacent contract contrast for a
   documentary claim, or two fresh matched reproductions plus a nearby control and unused
   holdout with no critical regression for a behavioral claim;
4. an accessible open/closed upstream issue search for the same target, symptom, and
   root-cause theme;
5. comparison of every match against the exact ref and known fix ancestry;
6. final `upstream-draft-ready` disposition.

If issue search or exact current provenance is inaccessible, use `upstream-unverifiable` and
omit proposal content. Apply the same disposition when documentary source/contrast evidence is
incomplete, or when a behavioral claim has fewer than two upstream runs or incomplete
control/holdout evidence. A consumer-only behavioral reproduction remains `local-only`.

Do not rewrite a matching open issue as a new proposal; cite that issue and its evidence
state. For a matching closed issue, classify a regression candidate only when an exact
later unmodified upstream source satisfies the applicable documentary or behavioral evidence
gate. Otherwise, cite the closed issue and use `upstream-unverifiable`. An
`upstream-candidate` may identify a matching issue or remaining owner work, but does not
include a new title/body proposal.

## Required de-identification

Remove or generalize:

- company, organization, product, and repository names;
- internal tickets, issues, PRs, users, customers, and account identifiers;
- internal URLs, hosts, API endpoints, credentials, tokens, cookies, and secrets;
- home directories and absolute paths;
- raw logs and screenshots;
- private UI literals and business data;
- private package or infrastructure names.

After drafting, search for every original identifier and sensitive literal. Separately
verify that technical reproduction details remain. If either check is impossible, do
not use `upstream-draft-ready`.

## Draft template

Use this template only after the proposal eligibility gate reaches
`upstream-draft-ready`.

```markdown
## Summary

<which tk-* contract regresses under which condition>

## Environment

- TigerKit version/ref: <verified ref>
- Host: Claude Code | Codex | Hermes Agent
- Invocation: explicit | automatic | handoff
- Consumer repository: anonymized external repository

## Evidence method

Documentary exact source/contrast | Behavioral minimal reproduction

## Expected

...

## Observed

...

## Claim evidence

- Current source/ref and location: ...
- Exact quote and adjacent contrast: ...
- Runs, when behavioral: N/N
- Failure plane: ...
- Stable/baseline: ...
- Candidate/current: ...
- Nearby control, when behavioral: ...
- Holdout, when behavioral: ...
- Resource metrics: ...

## Root cause

- Issue: ...
- Cause: ...
- General Fix Rule: ...

## Proposed contract or eval change

...

## Acceptance criteria

- [ ] Incident no longer reproduces
- [ ] Existing positive/control behavior remains valid
- [ ] Boundary/holdout case remains unchanged
- [ ] Supported host compatibility remains intact
- [ ] Any resource claim reproduces under matched conditions

## Privacy note

This report was derived from an external consumer repository. Names, paths,
URLs, domain data, identifiers, and private literals were removed.
```

Return the title and body only as a proposal. As part of diagnosis, do not create,
comment on, label, publish, or otherwise mutate GitHub.
