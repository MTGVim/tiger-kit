---
name: tk-github-image-upload-to-pr
description: "[user/auto] 기존 GitHub PR body 또는 명시적으로 요청된 comment에 local evidence image를 reviewed gh-attach extension 또는 authenticated CDP browser로 업로드합니다. explicit selection, 명확한 local-image insertion request, active tk-pr-open의 정확한 evidence_required handoff에서 사용하며 generic PR, screenshot 또는 GitHub request에는 적용하지 않습니다."
disable-model-invocation: false
argument-hint: "<PR and local image path(s)>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# GitHub PR Image Upload

Start only when the user selects `/tk-github-image-upload-to-pr` or
`$tk-github-image-upload-to-pr`, explicitly requests local image evidence for an
existing GitHub PR, or an active `tk-pr-open` sends an exact handoff with
`evidence_required: true`. Only the parent handoff is an automatic trigger. Do not
activate for screenshot capture, generic GitHub help, PR creation, PR review, or
issue triage.

## Scope

Handle one bounded upload: validate and stage local images, upload
repository-scoped GitHub attachments, minimally update the PR body or selected
comment, and verify source/render output. The default target is the PR body.

For `tk-pr-open`, accept only producer evidence handoffs from `tk-browser-verify`
or `tk-prototype` with `evidence_required: true`. If required evidence is missing
or invalid, mark the evidence handoff `Blocked`; do not revert an already-created
`tk-pr-open` PR.

Use
[references/upload-workflow.md](references/upload-workflow.md) as the operational
contract. Use `tk-browser-verify` for browser-controlled runtime verification.

## Workflow

1. Confirm `origin`, the current PR, and the executing repository from regular
   local image file(s) or a valid producer evidence handoff. Read the existing PR
   body.
2. Reuse the existing `## 스크린샷` heading. If absent, insert it before the AI
   footer or append it at the end. Preserve unrelated body content.
3. Check `gh attach --help`, authenticated `gh` access, and write capability for
   the target repository. Repository visibility is not a routing signal.
4. When available, use the reviewed extension without `--comment` and collect only
   the generated Markdown. Otherwise, ask before browser mutation: recommend the
   exact pinned `MTGVim/gh-attach` installation or offer CDP.
5. If CDP is selected or target write capability is unavailable, stage a
   meaningful run-owned copy outside `/tmp`, protect any existing composer draft,
   poll the upload placeholder, and clear only run-owned composer content.
6. Update only the requested body or comment through the GitHub API or equivalent.
   Before `Pass`, verify the source Markdown, rendered HTML/page evidence, every
   asset link, and the upload ref.
7. Remove only owned staging files on every exit path. If an upload attempt may
   have created remote state, do not silently switch routes.

## 실행 receipt · 단일 근거 record

모든 업로드 시도는 아래 하나의 receipt로 남깁니다. 이는 별도 생명주기
출력이 아니라 `## GitHub image upload` 결과와 승인/검증 판단에
쓰는 단일 근거 기록입니다. 값이 없으면 `none` 또는 `unavailable` 로
명시하고 추측하지 않습니다.

```text
Repository: <owner>/<repo>
PR / Target: <pr-number> / body | existing comment <comment-id>
Source images: <absolute path list>
Route: gh-attach | CDP
Entry: <exact reviewed command | browser route>
Generated Markdown: <asset refs | none>
Remote ref: <refs/uploads/issues/<pr-number> | none | unknown>
Verification: <source body/comment | rendered HTML/page | unavailable>
Changed: <body/comment changed | unchanged | unknown>
Cleanup: <owned staging path removed | failed | not applicable>
Status: Pass | Fail | Blocked | Unverifiable
```

## 생산자 근거 인계(생산자 증거 인계)

`evidence_required: true` 이면 다음을 요구합니다.

- `producer` 는 `tk-browser-verify` 또는 `tk-prototype` 중 하나여야 합니다.
- 각 산출물은 비어 있지 않은 이미지, 절대 경로, 실행 소유 근거 디렉터리를
  포함해야 합니다.
- 각 image를 inspected 상태로 두고 criterion 또는 caption을 보존합니다.
- `tk-browser-verify` 산출물은 `Pass` 결과에서 나와야 합니다.
- `tk-prototype` 산출물은 테스트된 스크린샷 경로와 실제 이미지 검사을
  포함해야 하며 공식 런타임 판정를 주장하지 않습니다.

임의 screenshot, 누락된 경로, `Unverifiable` 결과 및 현재 실행에 연결되지
않은 산출물은 거부합니다. 필수 근거가 없거나 유효하지 않으면
업로드 전에 `Blocked` 를 반환합니다.

## Prohibitions

- Do not create or merge a PR, change reviewers, publish a release, or insert a
  comment unless the user explicitly selected that comment target.
- Do not install, update, or substitute a GitHub CLI extension without explicit
  user approval. The reviewed command is
  `gh extension install MTGVim/gh-attach --pin v0.7.0-mtgvim.1`.
- Do not bypass `tk-browser-verify` or use Orca or screen control as an automatic
  browser fallback.
- Do not overwrite a pre-existing draft or click comment, close-with-comment, or
  any other submit button.
- Do not choose a route based on public/private visibility or claim success from
  only a placeholder, Markdown presence, fixed delay, or unrendered API response.
- Do not log or return a signed URL JWT or query string.

## Failure Handling

Return `Blocked` for a draft, a rejected installation without a selected CDP
route, or any other unresolved user-owned decision. Return `Unverifiable` if
neither route has authentication or render evidence, and `Fail` for upload,
remote ref verification, or cleanup errors. State whether the selected
body/comment changed and whether an upload ref may remain. After a started
`gh attach` fails, do not silently retry with CDP.

For `tk-pr-open`, preserve the separate PR operation result and return the
evidence state as `uploaded` or `blocked`. While required evidence remains
blocked, the parent cannot claim full completion.

## 결과

terminal 응답은 `## GitHub image upload` 로 시작합니다. 해당하는 경우
`## Uploaded`, `## Verification` 및 `## Cleanup` 을 포함합니다. 결과를 소유하는 section의 끝에는 정확히 하나의
`Status: Pass|Fail|Blocked|Unverifiable` 줄을 둡니다. 안전할 때만 asset URL을
노출하고 서명된 매개변수는 redact합니다.
