# Upstream issue anonymization

Use only in a consumer repository whose target is a TigerKit-origin `tk-*`
skill.

## Provenance gate

Verify:

1. TigerKit origin from metadata/path;
2. installed ref/version or source snapshot;
3. consumer-local edits or overrides;
4. reproduction against unmodified TigerKit source when possible;
5. separation of local configuration from upstream contract behavior.

Consumer-only reproduction is `local-only`. If exact upstream source cannot be
checked, local diagnosis may continue but upstream disposition is
`upstream-unverifiable`.

## Proposal eligibility gate

Do not write a proposed title, body, or any draft-template section until all
of these are verified:

1. canonical origin plus the exact installed/candidate ref, snapshot, or
   content hash;
2. two fresh matched reproductions against unmodified upstream source;
3. a nearby control and unused holdout with no critical regression;
4. an accessible open and closed upstream issue search covering the same
   target, symptom, and root-cause theme;
5. reconciliation of every match with the exact ref and known fix ancestry;
6. the final `upstream-draft-ready` disposition.

If issue search is inaccessible, exact provenance is missing, upstream has
fewer than two fresh reproductions, or control/holdout evidence is incomplete,
use `upstream-unverifiable` and omit proposal content. A consumer-only
reproduction remains `local-only`.

Cite a matching open issue and its evidence state instead of drafting another
proposal. For a matching closed issue, classify a regression candidate only
when an exact later unmodified upstream source satisfies the same two-run,
control, and holdout gates; otherwise cite the closed issue and use
`upstream-unverifiable`. `upstream-candidate` may identify the matching issue
or remaining owner work, but it never includes a new title/body proposal.

## Required redaction

Remove or generalize:

- company, organization, product, and repository names;
- internal tickets, issues, PRs, users, customers, and account identifiers;
- internal URLs, hosts, API endpoints, credentials, tokens, cookies, secrets;
- home directories and absolute paths;
- raw logs and screenshots;
- private UI literals and business data;
- private package or infrastructure names.

After drafting, search for every original identifier and sensitive literal.
Then separately verify that technical reproduction details still remain. If
either check is unavailable, do not use `upstream-draft-ready`.

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
- [ ] Boundary/holdout cases remain unchanged
- [ ] Supported host compatibility remains intact
- [ ] Resource claim, if any, is reproduced under matched conditions

## Privacy note

This report was derived from an external consumer repository. Names, paths,
URLs, domain data, identifiers, and private literals were removed.
```

Return title and body as a proposal only. Never create, comment on, label,
publish, or otherwise mutate GitHub as part of diagnosis.
