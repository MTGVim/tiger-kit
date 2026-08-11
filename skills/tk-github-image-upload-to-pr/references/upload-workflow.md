# 업로드 워크플로

## 사전 점검

- 실행 중인 checkout의 `origin` 에서 저장소를 확인합니다. TigerKit을
  hardcode하지 않습니다.
- `gh pr view --json number,url,body` 또는 동등한 읽기 작업으로 기존
  PR을 확인합니다.
- 모든 입력 경로가 일반 이미지 파일인지 검증하고, browser가 접근할 수
  없을 때 허용된 workspace 경계 밖의 경로는 거부합니다.
- 기존 PR body 전체를 읽고 warning, notes, checklist, links, images, footer 및
  줄바꿈을 보존합니다.
- 기본 대상은 PR body입니다. 사용자가 comment 대상을 지정하거나 comment
  insertion을 명시적으로 요청한 경우에만 comment를 사용합니다.
- `evidence_required: true` 이면 `tk-browser-verify` 또는 `tk-prototype` 의
  생산자 인계만 받습니다. 임의 image 파일이 있다는 이유로 requirement를
  추론하지 않습니다.
- `gh attach --help`, `gh auth status` 및 `gh api repos/<owner>/<repo>` 를 통한
  대상 저장소 `.permissions.push` 를 확인합니다. public/private
  visibility로 capability를 추론하지 않습니다.

## 경로 선택 및 설치

`gh attach --help` 가 성공하고 현재 `gh` session이 authenticated이며 대상
저장소 write capability가 true일 때 `gh-attach` 를 사용합니다.

extension이 없으면 browser identity 또는 mutation gate 전에 멈추고 다음 중
하나를 선택하도록 질문합니다.

- **권장:** 다음을 approve합니다.
  `gh extension install MTGVim/gh-attach --pin v0.7.0-mtgvim.1`;
- 지금 CDP로 계속합니다. dedicated profile과 one-time GitHub login이 필요할
  수 있습니다.

extension을 자동으로 install, update 또는 replace하지 않습니다. 검토하지 않은
upstream, 고정되지 않은 설치, secret gist 또는 public image host를 동등한
대안으로 제시하지 않습니다. extension은 설치되어 있지만 대상 write
capability를 사용할 수 없으면 그 결과를 설명하고 설치 질문 없이
CDP 경로로 계속합니다.

## 검토된 extension 경로

실행:

```text
gh attach --repo <owner>/<repo> <pr-number> <image>...
```

`--comment` 를 전달하지 않습니다. 이 스킬이 정확한 body/comment 배치를
유지할 수 있도록 생성된 image Markdown만 수집합니다. 빈 출력,
예상하지 못한 비-Markdown 출력, 다른 저장소/ref 또는 모든 입력 image를
포함하지 않는 생성 link는 거부합니다.

예상 원격 ref는 `refs/uploads/issues/<pr-number>`입니다. upload는 이후
실패 전에 해당 ref를 create 또는 update할 수 있습니다. 명령이 시작되면
CDP로 조용히 전환하지 말고, 멈춰서 선택한 body/comment 변경 여부를 보고하며
upload ref가 남을 수 있음을 명시합니다.

## CDP staging 및 브라우저

명시적으로 선택한 뒤 또는 대상 write capability를 사용할 수 없을 때만 이
경로를 사용합니다. browser automation workspace 아래에 run-owned directory를
만듭니다. browser가 접근하지 못할 수 있으므로 `/tmp` 를 기본 staging 위치로
사용하지 않습니다. image alt text에는 안전하고 설명적인 filename을 사용합니다.

browser 순서는 다음과 같습니다.

1. CDP 또는 Chrome DevTools MCP를 통한 authenticated existing Chrome session;
2. CDP/Playwright를 통한 authenticated persistent browser profile;
3. `Unverifiable` 로 중단하고 CDP recovery 경로를 설명한다.

첫 번째 선택지에서는 사용자에게
`chrome://inspect/#remote-debugging`, Chrome DevTools MCP의
`--autoConnect` 및 one-time Chrome Allow prompt가 필요할 수 있음을
설명합니다. cookies, tokens 또는 private identity details를 출력하지
않습니다. Orca 또는 다른 desktop controller를 대체 경로로 실행하지
않습니다.

Chrome 136+는 default data directory에 대한 remote-debugging switch를
무시합니다. 사용자의 default profile을 port와 함께 재실행하면 동작한다고
약속하지 않습니다. 직접 실행한 endpoint에는 dedicated `--user-data-dir` 와
one-time login이 필요합니다. 설치된 Chrome/DevTools MCP가 지원하면
`--autoConnect` 는 사용자의 명시적 Allow action 이후에만 이미 실행 중인
profile에 attach할 수 있습니다. `DevToolsActivePort` 파일은 availability
근거가 아니므로 현재 socket과 browser endpoint를 확인합니다.

## 업로드 및 composer 안전성

대상 PR page를 열고 표시되는 attachment control을 사용합니다. hidden file
input에 의존하지 않습니다. 각 `![Uploading ...]()` placeholder가 실제
`user-attachments/assets/...` URL 또는 동등한 image element가 될 때까지
기다립니다. bounded timeout으로 polling하고 실패 시 마지막 표시 진단을
보존합니다.

입력 전에 composer를 검사합니다. 비어 있지 않은 user draft는 blocker이므로
교체하지 않습니다. asset URL을 수집한 뒤 run-owned composer content만 지우고
textarea가 비어 있으며 comment button이 disabled인지 확인합니다. upload를
테스트하려고 빈 comment를 submit하지 않습니다.

## 본문 또는 comment 갱신

생성된 image Markdown을 요청된 위치에 삽입합니다. 위치가 없으면 정확한 소스
heading `## 스크린샷` 을 우선하고, 없으면 AI footer 앞에 삽입하거나
body 끝에 추가합니다. 그 외에는 original body를 가능한 한 byte-stable하게
유지합니다. GitHub API 또는 동등한 방법으로 body만 업데이트하고 반환된
body에 모든 asset이 포함되는지 확인합니다. 명시적으로 선택한 existing
comment의 경우 해당 comment만 업데이트하고 관련 없는 content를 보존합니다.
temporary composer comment는 절대 submit하지 않습니다.

## 검증 및 정리

선택한 body/comment 소스를 다시 읽습니다. 그 다음 HTML media type을 사용한
REST `body_html` 또는 GraphQL `bodyHTML` 과 같은 GitHub-rendered HTML을
요청하고, 생성된 모든 asset이 예상한 image element/link로 표현되는지
확인합니다. reviewed extension 경로에서는 대상 저장소의
`git/ref/uploads/issues/<pr-number>` 도 확인하고 각 generated link가 해당 ref를
이름에 포함하는지 검증합니다. CDP에서는 rendered PR page를 확인합니다.
GitHub가 asset URL을 `private-user-images.githubusercontent.com` 으로 다시
쓸 수 있는데, 이는 mismatch가 아니라 성공적인 rewrite입니다. Markdown
presence 또는 성공한 update response만으로는 절대 `Pass` 가 아닙니다.
signed URL JWT 또는 query string을 logs, 산출물이나 final 응답에
노출하지 않습니다.

run-owned staging directory만 삭제하고 없어졌는지 확인합니다. 정리가
실패하면 정확한 owned 경로를 보고하고 `Pass` 를 주장하지 않습니다. upload 또는
검증이 실패하면 selected body/comment 변경 여부를 보고하며, comment를
submit하거나 경로를 조용히 바꾸어 retry하지 않습니다.

## 생산자 인계

인계는 다음을 포함할 때만 유효합니다.

```text
evidence_required: true
producer: tk-browser-verify | tk-prototype
evidence_directory: <absolute run-owned path>
artifacts:
  - path: <absolute non-empty image path>
    criterion: <criterion or caption>
    inspected: true
```

`tk-browser-verify` 에는 생산자의 `Pass` 결과와 기존 `Evidence directory` 및
`Screenshot` entries가 필요합니다. `tk-prototype` 에는 tested screenshot 경로와
실제 image inspection이 필요하며 Guard comparison을 공식 런타임
verdict로 설명하지 않습니다. 인계가 필수인데 누락되었거나 유효하지
않으면 upload 전에 `Blocked` 를 반환합니다. 상위는 created PR을 유지할 수
있지만 full completion 대신 `evidence_state: blocked` 를 보고해야 합니다.

## 검토된 의존성

controlled install은
[`MTGVim/gh-attach@v0.7.0-mtgvim.1`](https://github.com/MTGVim/gh-attach/releases/tag/v0.7.0-mtgvim.1),
reviewed fork of the MIT-licensed `enthus-appdev/gh-attach@v0.7.0`입니다.
해당 release에는 `LICENSE`, `THIRD_PARTY_NOTICES.txt` 및 checksums가
포함됩니다. TigerKit은 그 소스를 vendor하거나 auto-install하지 않습니다.

CDP 워크플로는 다음을 개념적으로 참고했습니다.
[`github-upload-image-to-pr`](https://github.com/tonkotsuboy/github-upload-image-to-pr);
이 package에는 upstream 소스를 복사하지 않습니다.
