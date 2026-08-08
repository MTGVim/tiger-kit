---
name: tk-github-image-upload-to-pr
description: "[user/auto] 기존 GitHub PR body 또는 명시적으로 요청된 comment에 local evidence image를 reviewed gh-attach extension 또는 authenticated CDP browser로 업로드합니다. explicit selection, 명확한 local-image insertion request, active tk-pr-open의 정확한 evidence_required handoff에서 사용하며 generic PR, screenshot 또는 GitHub request에는 적용하지 않습니다."
argument-hint: "<PR and local image path(s)>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# GitHub PR 이미지 업로드

사용자가 `/tk-github-image-upload-to-pr` 또는
`$tk-github-image-upload-to-pr`를 선택하거나, 기존 GitHub PR에 local image
evidence를 명시적으로 요청하거나, active `tk-pr-open`이
`evidence_required: true`인 정확한 handoff를 보낼 때만 시작합니다. Parent
handoff만 automatic trigger입니다. screenshot capture, generic GitHub help,
PR creation, PR review 또는 issue triage에는 활성화하지 않습니다.

## 범위

하나의 bounded upload를 담당합니다: local image validation 및 staging,
repository-scoped GitHub attachment upload, 최소한의 PR body 또는 selected
comment update, source/render verification입니다. 기본 target은 PR body입니다.

`tk-pr-open`에서는 `evidence_required: true`인 `tk-browser-verify` 또는
`tk-prototype`의 producer evidence handoff만 받습니다. required evidence가
누락되거나 유효하지 않으면 evidence handoff를 `Blocked`로 만들며, 이미
생성된 `tk-pr-open` PR은 되돌리지 않습니다.

operational contract는
[references/upload-workflow.md](references/upload-workflow.md)를 사용합니다.
browser-controlled runtime verification에는 `tk-browser-verify`를 사용합니다.

## 워크플로

1. `origin`, current PR, regular local image file(s) 또는 valid producer
   evidence handoff에서 executing repository를 확인합니다. 기존 PR body를
   읽습니다.
2. 기존 `## 스크린샷` heading을 재사용하고, 없으면 AI footer 앞에 삽입하거나
   끝에 추가합니다. 관련 없는 body content는 보존합니다.
3. `gh attach --help`, authenticated `gh` access 및 target repository write
   capability를 확인합니다. repository visibility는 routing signal이 아닙니다.
4. 사용 가능하면 `--comment` 없이 reviewed extension을 사용하고 생성된
   Markdown만 수집합니다. 없으면 browser mutation 전에 질문합니다: 정확한
   pinned `MTGVim/gh-attach` install을 권장하거나 CDP를 제시합니다.
5. CDP를 선택했거나 target write capability를 사용할 수 없으면 `/tmp` 밖에
   의미 있는 run-owned copy를 staging하고, 기존 composer draft를 보호하며,
   upload placeholder를 polling하고, run-owned composer content만 지웁니다.
6. GitHub API 또는 equivalent를 통해 요청된 body 또는 comment만 업데이트합니다.
   `Pass` 전에 source Markdown, rendered HTML/page evidence, 모든 asset link와
   upload ref를 검증합니다.
7. 모든 exit path에서 owned staging file만 제거합니다. upload attempt가
   remote state를 만들었을 수 있으면 route를 조용히 전환하지 않습니다.

## 실행 receipt · 단일 evidence record

모든 upload attempt는 아래 하나의 receipt로 남깁니다. 이는 별도 lifecycle
output이 아니라 `## GitHub image upload` 결과와 approval/verification 판단에
쓰는 단일 evidence record입니다. 값이 없으면 `none` 또는 `unavailable`로
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

## Producer evidence handoff(생산자 증거 인계)

`evidence_required: true`이면 다음을 요구합니다.

- `producer`는 `tk-browser-verify` 또는 `tk-prototype` 중 하나여야 합니다.
- 각 artifact는 non-empty image, absolute path, run-owned evidence directory를
  포함해야 합니다.
- 각 image를 inspected 상태로 두고 criterion 또는 caption을 보존합니다.
- `tk-browser-verify` artifact는 `Pass` result에서 와야 합니다.
- `tk-prototype` artifact는 tested screenshot path와 actual image inspection을
  포함해야 하며 official runtime verdict를 주장하지 않습니다.

임의 screenshot, 누락된 path, `Unverifiable` result 및 current run에 연결되지
않은 artifact는 거부합니다. required evidence가 없거나 유효하지 않으면
upload 전에 `Blocked`를 반환합니다.

## 금지 사항

- 사용자가 해당 comment target을 명시적으로 선택하지 않았다면 PR을 만들거나,
  merge하거나, reviewer를 바꾸거나, release를 publish하거나, comment를
  삽입하지 않습니다.
- 명시적인 user approval 없이 GitHub CLI extension을 install, update 또는
  substitute하지 않습니다. reviewed command는
  `gh extension install MTGVim/gh-attach --pin v0.7.0-mtgvim.1`입니다.
- `tk-browser-verify`를 우회하거나 Orca 또는 screen control을 automatic
  browser fallback으로 사용하지 않습니다.
- pre-existing draft를 덮어쓰거나 comment, close-with-comment 또는 다른
  submit button을 클릭하지 않습니다.
- public/private visibility로 route를 정하거나 placeholder, Markdown
  presence, fixed delay 또는 unrendered API response만으로 성공을 주장하지
  않습니다.
- signed URL JWT 또는 query string을 log하거나 반환하지 않습니다.

## 실패 처리

draft, selected CDP route 없는 rejected installation 또는 다른 missing
user-owned decision에는 `Blocked`를 반환합니다. 어느 route에도 authentication
또는 render evidence가 없으면 `Unverifiable`을, upload, remote ref
verification 또는 cleanup error면 `Fail`을 반환합니다. selected body/comment가
변경되었는지와 upload ref가 남을 수 있는지를 명시합니다. 시작된
`gh attach`가 실패한 뒤에는 CDP로 조용히 retry하지 않습니다.

`tk-pr-open`에서는 별도의 PR operation result를 보존하고 evidence state를
`uploaded` 또는 `blocked`로 반환합니다. required evidence가 계속 blocked인
동안 parent는 full completion을 주장할 수 없습니다.

## 결과

terminal response는 `## GitHub image upload`로 시작합니다. 해당하는 경우
`## Uploaded`, `## Verification` 및 `## Cleanup`을 포함합니다. owning result
section의 끝에는 정확히 하나의
`Status: Pass|Fail|Blocked|Unverifiable` line을 둡니다. 안전할 때만 asset URL을
노출하고 signed parameter는 redact합니다.
