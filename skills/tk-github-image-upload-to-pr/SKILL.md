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

# GitHub PR 이미지 업로드

사용자가 `/tk-github-image-upload-to-pr` 또는
`$tk-github-image-upload-to-pr` 를 선택하거나, 기존 GitHub PR에 로컬 이미지
근거를 명시적으로 요청하거나, 활성 `tk-pr-open` 이
`evidence_required: true`인 정확한 handoff를 보낼 때만 시작합니다. 상위 인계만 자동 trigger입니다. 스크린샷 캡처, 일반적인 GitHub 도움말,
PR 생성, PR 검토 또는 이슈 triage에는 활성화하지 않습니다.

## 범위

하나의 제한된 업로드를 담당합니다: 로컬 이미지 검증 및 staging,
저장소 범위의 GitHub attachment upload, 최소한의 PR body 또는 선택한
comment update, 소스/render 검증입니다. 기본 대상은 PR body입니다.

`tk-pr-open` 에서는 `evidence_required: true`인 `tk-browser-verify` 또는
`tk-prototype` 의 생산자 근거 handoff만 받습니다. 필수 근거가
누락되거나 유효하지 않으면 근거 handoff를 `Blocked` 로 만들며, 이미
생성된 `tk-pr-open` PR은 되돌리지 않습니다.

운영 계약은
[references/upload-workflow.md](references/upload-workflow.md)를 사용합니다.
브라우저 제어 런타임 검증에는 `tk-browser-verify` 를 사용합니다.

## 워크플로

1. `origin`, 현재 PR, 일반 로컬 이미지 파일(s) 또는 유효한 생산자
   근거 handoff에서 실행 중인 저장소를 확인합니다. 기존 PR body를
   읽습니다.
2. 기존 `## 스크린샷` 제목을 재사용하고, 없으면 AI footer 앞에 삽입하거나
   끝에 추가합니다. 관련 없는 본문 내용는 보존합니다.
3. `gh attach --help`, 인증된 `gh` 접근 및 대상 저장소 쓰기
   capability를 확인합니다. 저장소 visibility는 라우팅 신호이 아닙니다.
4. 사용 가능하면 `--comment` 없이 검토된 extension을 사용하고 생성된
   Markdown만 수집합니다. 없으면 브라우저 변경 전에 질문합니다: 정확히 고정된
   `MTGVim/gh-attach` 설치를 권장하거나 CDP를 제시합니다.
5. CDP를 선택했거나 대상 write capability를 사용할 수 없으면 `/tmp` 밖에
   의미 있는 실행 소유 복사본을 staging하고, 기존 composer draft를 보호하며,
   업로드 placeholder를 polling하고, run-owned composer content만 지웁니다.
6. GitHub API 또는 equivalent를 통해 요청된 body 또는 comment만 업데이트합니다.
   `Pass` 전에 소스 Markdown, rendered HTML/page 근거, 모든 asset link와
   upload ref를 검증합니다.
7. 모든 종료 경로에서 owned staging 파일만 제거합니다. 업로드 시도가
   원격 상태를 만들었을 수 있으면 경로를 조용히 전환하지 않습니다.

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

## 금지 사항

- 사용자가 해당 comment 대상을 명시적으로 선택하지 않았다면 PR을 만들거나,
  merge하거나, 검토자를 바꾸거나, release를 발행하거나, comment를
  삽입하지 않습니다.
- 명시적인 사용자 승인 없이 GitHub CLI extension을 install, update 또는
  substitute하지 않습니다. 검토된 명령은
  `gh extension install MTGVim/gh-attach --pin v0.7.0-mtgvim.1`입니다.
- `tk-browser-verify` 를 우회하거나 Orca 또는 screen control을 automatic
  브라우저 대체 경로로 사용하지 않습니다.
- pre-existing draft를 덮어쓰거나 comment, close-with-comment 또는 다른
  submit button을 클릭하지 않습니다.
- public/private visibility로 경로를 정하거나 placeholder, Markdown
  presence, fixed delay 또는 unrendered API 응답만으로 성공을 주장하지
  않습니다.
- signed URL JWT 또는 query string을 log하거나 반환하지 않습니다.

## 실패 처리

초안, 선택한 CDP 경로가 없는 거부된 설치 또는 다른 미해결
사용자 소유 결정에는 `Blocked` 를 반환합니다. 어느 경로에도 authentication
또는 렌더링 근거가 없으면 `Unverifiable` 을, upload, remote ref
검증 또는 정리 오류면 `Fail` 을 반환합니다. selected body/comment가
변경되었는지와 upload ref가 남을 수 있는지를 명시합니다. 시작된
`gh attach` 가 실패한 뒤에는 CDP로 조용히 retry하지 않습니다.

`tk-pr-open` 에서는 별도의 PR 작업 결과를 보존하고 근거 상태를
`uploaded` 또는 `blocked` 로 반환합니다. 필수 근거가 계속 blocked인
동안 상위는 전체 완료를 주장할 수 없습니다.

## 결과

terminal 응답은 `## GitHub image upload` 로 시작합니다. 해당하는 경우
`## Uploaded`, `## Verification` 및 `## Cleanup` 을 포함합니다. 결과를 소유하는 section의 끝에는 정확히 하나의
`Status: Pass|Fail|Blocked|Unverifiable` 줄을 둡니다. 안전할 때만 asset URL을
노출하고 서명된 매개변수는 redact합니다.
