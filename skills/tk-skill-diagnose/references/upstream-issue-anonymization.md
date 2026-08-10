# Upstream issue 익명화

TigerKit-origin `tk-*` skill을 대상으로 하는 consumer repository에서만 사용한다.

## 출처 확인 게이트

다음을 검증한다:

1. metadata/path에서 TigerKit origin;
2. installed ref/version 또는 source snapshot;
3. consumer-local edits 또는 overrides;
4. 가능하면 변경되지 않은 TigerKit source에 대한 reproduction;
5. local configuration과 upstream contract behavior의 분리.

Consumer-only reproduction은 `local-only`다. 정확한 upstream source를 확인할 수
없어도 local diagnosis는 계속할 수 있지만 upstream 처분은
`upstream-unverifiable`다.

## 제안 적격성 게이트

다음 항목을 모두 검증하기 전에는 proposed title, body 또는 draft-template section을
작성하지 않는다:

1. canonical origin과 exact installed/candidate ref, snapshot 또는 content hash;
2. unmodified upstream source에 대한 두 번의 fresh matched reproduction;
3. critical regression이 없는 nearby control 및 unused holdout;
4. 같은 target, symptom 및 root-cause theme를 다루는 accessible open/closed upstream issue search;
5. 모든 match를 exact ref 및 known fix ancestry와 대조;
6. 최종 `upstream-draft-ready` disposition.

issue search에 접근할 수 없거나, exact provenance가 없거나, upstream reproduction이
두 번보다 적거나, control/holdout evidence가 불완전하면
`upstream-unverifiable` 을 사용하고 proposal content를 생략한다. Consumer-only
reproduction은 `local-only` 로 남긴다.

일치하는 open issue를 새 proposal로 작성하지 말고 해당 issue와 evidence state를
인용한다. matching closed issue의 경우 exact later unmodified upstream source가
동일한 two-run, control 및 holdout gate를 충족할 때만 regression candidate로 분류한다.
그 외에는 closed issue를 인용하고 `upstream-unverifiable` 을 사용한다.
`upstream-candidate` 는 matching issue 또는 남은 owner work를 식별할 수 있지만 새
title/body proposal을 포함하지 않는다.

## 필수 비식별화

다음을 제거하거나 일반화한다:

- company, organization, product 및 repository names;
- internal tickets, issues, PRs, users, customers 및 account identifiers;
- internal URLs, hosts, API endpoints, credentials, tokens, cookies 및 secrets;
- home directories 및 absolute paths;
- raw logs 및 screenshots;
- private UI literals 및 business data;
- private package 또는 infrastructure names.

초안을 작성한 뒤 모든 original identifier와 sensitive literal을 검색한다. 그 다음
technical reproduction details가 여전히 남아 있는지 별도로 확인한다. 어느 한쪽 확인이
불가능하면 `upstream-draft-ready` 를 사용하지 않는다.

## 초안 템플릿

제안 적격성 게이트가 `upstream-draft-ready` 에 도달한 뒤에만 다음 템플릿을 사용한다.

```markdown
## Summary

<which tk-* contract regresses under which condition>

## Environment

- TigerKit version/ref: <verified ref>
- Host: Claude Code | Codex | Hermes Agent
- Invocation: explicit | automatic | handoff
- Consumer repository: anonymized external repository

## 최소 재현

1. ...
2. ...

## Expected

...

## Observed

...

## 재현 evidence

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

## 제안 contract 또는 eval 변경

...

## Acceptance criteria

- [ ] Incident가 더 이상 재현되지 않는다
- [ ] Existing positive/control behavior가 유효하게 유지된다
- [ ] Boundary/holdout case가 변하지 않는다
- [ ] Supported host compatibility가 유지된다
- [ ] Resource claim이 있으면 matched condition에서 재현된다

## Privacy note

이 report는 external consumer repository에서 파생했다. names, paths,
URLs, domain data, identifiers 및 private literals는 제거했다.
```

title과 body는 proposal로만 반환한다. 진단의 일부로 GitHub를 create, comment, label,
publish하거나 그 밖의 방식으로 변경하지 않는다.
