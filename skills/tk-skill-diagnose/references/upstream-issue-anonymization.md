# Upstream issue anonymization

Use this only in a consumer repository for a TigerKit-origin `tk-*` skill.

## Provenance gate

Verify:

1. TigerKit origin from metadata/path;
2. installed ref/version or source snapshot;
3. consumer-local edits or overrides;
4. reproduction against unmodified TigerKit source when possible;
5. separation between local configuration and upstream contract behavior.

A consumer-only reproduction is `local-only`. Local diagnosis may continue when the
exact upstream source cannot be verified, but upstream disposition is
`upstream-unverifiable`.

## Proposal eligibility gate

Do not write a proposed title, body, or draft-template section before verifying all of:

1. canonical origin and exact installed/candidate ref, snapshot, or content hash;
2. two fresh matched reproductions against unmodified upstream source;
3. a nearby control and unused holdout with no critical regression;
4. an accessible open/closed upstream issue search for the same target, symptom, and
   root-cause theme;
5. comparison of every match against the exact ref and known fix ancestry;
6. final `upstream-draft-ready` disposition.

If issue search is inaccessible, exact provenance is missing, upstream reproduction
has fewer than two runs, or control/holdout evidence is incomplete, use
`upstream-unverifiable` and omit proposal content. A consumer-only reproduction remains
`local-only`.

Do not rewrite a matching open issue as a new proposal; cite that issue and its evidence
state. For a matching closed issue, classify a regression candidate only when an exact
later unmodified upstream source satisfies the same two-run, control, and holdout gate.
Otherwise, cite the closed issue and use `upstream-unverifiable`. An
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

## Minimal reproduction

1. ...
2. ...

## Expected

...

## Observed

...

## Reproduction evidence

- Runs: N/N
- Failure plane: ...
- Stable/baseline: ...
- Candidate/current: ...
- Nearby control: ...
- Holdout: ...
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
