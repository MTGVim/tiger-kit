---
name: tk-pr-open
description: "[user/auto] 검증된 현재 브랜치 `commit`으로 하나의 GitHub `pull request`를 열거나 업데이트하며, 원격 발행 전 정확한 현재 턴 승인을 요구합니다."
argument-hint: "<repository or branch>"
disable-model-invocation: false
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Open a PR

Start when the intent to create or update one `PR` is explicit, such as `/tk-pr-open`, `$tk-pr-open`, selection through the host skill picker, or “현재 브랜치로 PR 열어줘”.

The input is an already implemented and verified current-branch `commit`.
A `.tigerkit/seed.md` is optional publication evidence, not authority. Treat it as the current task Seed only after fresh validation proves all of the following:

- it contains `<!-- tigerkit:seed -->` and `Status: Ready`;
- its repository/worktree/branch or exact PR identity matches the current checkout;
- the current `HEAD` is the recorded implementation head or a descendant of the Seed's recorded base/head on the same task checkout;
- the changed paths/evidence being published remain inside the Seed's approved scope.

A marked Seed whose identity does not match is stale for this publication: do not delete or rewrite it, and do not use its goal, AC, or evidence requirement. An unmarked/legacy/identity-ambiguous Seed is never treated as current. Continue from independently verified current work only when the required goal/template/evidence state can still be proven; otherwise return `Unverifiable` instead of guessing.

Do not repeat implementation, create a `worker`, or add product `commit`s.
template 선택 또는 remote publication approval이 필요하면 host별 native structured question surface를 우선 사용합니다 (Claude Code: AskUserQuestion; Codex: request_user_input; Hermes: clarify). unavailable하면 같은 approval packet을 plain chat으로 fallback하고 exact current-turn approval 전 remote write를 하지 않습니다.

## Current state

First, verify the following.

- Repository and authenticated GitHub account
- Current branch and `HEAD`
- Base branch
- Target `commit` and changed paths
- 같은 `head`의 기존 `PR` 존재 여부와 `observed draft | ready` 상태
- Unrelated dirty/staged paths
- Target repository's `PR template`
- `.tigerkit/seed.md`가 있으면 `current | stale | unmarked/ambiguous` 판정과 그 근거

If the exact current `commit` cannot be proven or unrelated changes are mixed in, do not broaden scope; return `Blocked`/`Unverifiable`.

## `PR template`

Before creating the `PR body`, check supported template locations on the default branch.

- Root
- `docs/`
- `.github/`
- `PULL_REQUEST_TEMPLATE/` under each location

If exactly one template applies, preserve its heading order, checklists, HTML comments, and required sections.
If multiple templates exist and there is no basis for choosing one, explain the candidates with one recommendation and ask the user to choose before publication approval.
If the template cannot be read, do not invent a body.

When the `PR body` or a QA table names a user-visible element, verify the exact rendered string from repository evidence before writing it. Do not copy a ticket paraphrase, code identifier, or enum value; quote the label verbatim. If no visible label exists, use the entry path ending in an exact visible title. If ticket, code, and screenshot disagree, preserve the verified source and tell the user about the mismatch; do not present an unverified server-supplied label as fact.

## Evidence

Determine whether `PR evidence` is needed from the validated current Seed or the currently verified work.

```text
required | optional | N/A | undecided
```

If a validated current Seed marks `tk-browser-verify` screenshot evidence as required for `browser-visible acceptance`, use only validly inspected evidence.
Approved `tk-prototype` evidence may also be used.

Do not upload actual secret-bearing screenshots or unverified captures.
If an image is required, pass the exact evidence path to `tk-github-image-upload-to-pr` after the `PR` exists.

## Publication plan

Maintain `.tigerkit/pr-open.md` as this skill's independent publication plan.
Record and reread the following exact information.

```text
Repository
PR operation: create | update
PR state: draft | ready
Base
Head ref + SHA
Push refspec
Title
Body
Template source/compliance
PR evidence requirement/state
Evidence producer/path
Known exclusions
```

This artifact owns only the current `PR` publication plan, not the product work plan or `worker` state.
새 `PR`은 사용자가 `draft`를 명시할 때만 `draft`로 만들고, 상태를 명시하지 않으면 기존 `ready` 동작을 유지합니다.
기존 같은 `head`의 `PR`은 상태 변경 요청이 없으면 `fresh-read`한 상태를 보존합니다.

Present the following naturally to the user instead of hiding information behind a file they must open.

- 포함되는 변경 요약
- 정확한 제목/본문 또는 중요한 템플릿 섹션
- 기준/헤드
- 유효 `PR state`
- 검사/증거 상태
- 제외 범위/위험
- 한 가지 발행 추천

## 🔴 CHECKPOINT · 🛑 STOP · Publication boundary

Before any remote write, reread the plan and obtain one exact current-turn approval; do not treat the natural-language request “PR 열어줘” itself as publication approval. 승인에는 유효 `PR state`도 포함합니다.
STOP if the plan, approved `commit`, template/evidence state, or current repository state cannot be reverified.

## Publication

After approval, recheck the repository, account, branch, `HEAD`, base, existing `PR`, template source, and any current Seed identity used by the plan.
기존 `PR`의 `actual state`가 승인된 `plan`과 `material`하게 달라졌다면 승인을 무효화합니다.
Invalidate the approval if any material `drift` exists.

`push` only the exact approved `refspec`, and create or update only the specified `PR`.
`Create`에서는 승인된 `PR state`를 적용하고, `update`에서는 명시적으로 승인된 경우에만 상태를 변경합니다.
Do not `merge`, `close`, `tag`, or `release`.

After creating or updating the `PR`, reread the remote `PR` and verify its URL, `head SHA`, actual `draft | ready` state, template compliance, and evidence state.
If evidence is required, use the image uploader after the `PR` exists.
If the `PR` was created but the required evidence upload fails, preserve the actual remote state and report completion as `Blocked`.

## Completion

사용자에게 중요한 결과만 보여줍니다.

- `PR` URL
- 생성/업데이트 여부
- 현재 `head`
- 현재 `PR state`
- 검증/증거 결과
- 남은 차단 요인

Do not show provenance dumps or product implementation receipts.
