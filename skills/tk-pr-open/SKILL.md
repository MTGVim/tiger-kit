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
If a prepared `.tigerkit/seed.md` exists, read the work `goal`, `acceptance`, and `browser evidence requirement`, but the `Seed` itself does not grant publication authority.

Do not repeat implementation, create a `worker`, or add product `commit`s.

## Current state

First, verify the following.

- Repository and authenticated GitHub account
- Current branch and `HEAD`
- Base branch
- Target `commit` and changed paths
- Whether a `PR` already exists for the same `head`
- Unrelated dirty/staged paths
- Target repository's `PR template`

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

## Evidence

Determine whether `PR evidence` is needed from the prepared `Seed` or the currently verified work.

```text
required | optional | N/A | undecided
```

If a prepared `Seed` marks `tk-browser-verify` screenshot evidence as required for `browser-visible acceptance`, use only validly inspected evidence.
Approved `tk-prototype` evidence may also be used.

Do not upload actual secret-bearing screenshots or unverified captures.
If an image is required, pass the exact evidence path to `tk-github-image-upload-to-pr` after the `PR` exists.

## Publication plan

Maintain `.tigerkit/pr-open.md` as this skill's independent publication plan.
Record and reread the following exact information.

```text
Repository
PR operation: create | update
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

Present the following naturally to the user instead of hiding information behind a file they must open.

- 포함되는 변경 요약
- 정확한 제목/본문 또는 중요한 템플릿 섹션
- 기준/헤드
- 검사/증거 상태
- 제외 범위/위험
- 한 가지 발행 추천

## 🔴 CHECKPOINT · 🛑 STOP · Publication boundary

Before any remote write, reread the plan and obtain one exact current-turn approval; do not treat the natural-language request “PR 열어줘” itself as publication approval.
STOP if the plan, approved `commit`, template/evidence state, or current repository state cannot be reverified.

## Publication

After approval, recheck the repository, account, branch, `HEAD`, base, existing `PR`, and template source.
Invalidate the approval if any material `drift` exists.

`push` only the exact approved `refspec`, and create or update only the specified `PR`.
Do not `merge`, `close`, `tag`, or `release`.

After creating or updating the `PR`, reread the remote `PR` and verify its URL, `head SHA`, template compliance, and evidence state.
If evidence is required, use the image uploader after the `PR` exists.
If the `PR` was created but the required evidence upload fails, preserve the actual remote state and report completion as `Blocked`.

## Completion

사용자에게 중요한 결과만 보여줍니다.

- `PR` URL
- 생성/업데이트 여부
- 현재 `head`
- 검증/증거 결과
- 남은 차단 요인

Do not show provenance dumps or product implementation receipts.
