# 업로드 워크플로

## 사전 점검

- executing checkout의 `origin` 에서 repository를 확인합니다. TigerKit을
  hardcode하지 않습니다.
- `gh pr view --json number,url,body` 또는 equivalent read operation으로 기존
  PR을 확인합니다.
- 모든 input path가 regular image file인지 검증하고, browser가 접근할 수
  없을 때 allowed workspace boundary 밖의 path는 거부합니다.
- 기존 PR body 전체를 읽고 warning, notes, checklist, links, images, footer 및
  line ending을 보존합니다.
- 기본 target은 PR body입니다. 사용자가 comment target을 지정하거나 comment
  insertion을 명시적으로 요청한 경우에만 comment를 사용합니다.
- `evidence_required: true` 이면 `tk-browser-verify` 또는 `tk-prototype` 의
  producer handoff만 받습니다. 임의 image file이 있다는 이유로 requirement를
  추론하지 않습니다.
- `gh attach --help`, `gh auth status` 및 `gh api repos/<owner>/<repo>` 를 통한
  target repository `.permissions.push` 를 확인합니다. public/private
  visibility로 capability를 추론하지 않습니다.

## Route 선택 및 installation

`gh attach --help` 가 성공하고 current `gh` session이 authenticated이며 target
repository write capability가 true일 때 `gh-attach` 를 사용합니다.

extension이 없으면 browser identity 또는 mutation gate 전에 멈추고 다음 중
하나를 선택하도록 질문합니다.

- **권장:** 다음을 approve합니다.
  `gh extension install MTGVim/gh-attach --pin v0.7.0-mtgvim.1`;
- 지금 CDP로 계속합니다. dedicated profile과 one-time GitHub login이 필요할
  수 있습니다.

extension을 자동으로 install, update 또는 replace하지 않습니다. unreviewed
upstream, unpinned install, secret gist 또는 public image host를 동등한
대안으로 제시하지 않습니다. extension은 설치되어 있지만 target write
capability를 사용할 수 없으면 그 결과를 설명하고 installation question 없이
CDP route로 계속합니다.

## 검토된 extension 경로

Run:

```text
gh attach --repo <owner>/<repo> <pr-number> <image>...
```

`--comment` 를 전달하지 않습니다. 이 skill이 정확한 body/comment placement를
유지할 수 있도록 generated image Markdown만 수집합니다. empty output,
unexpected non-Markdown output, 다른 repository/ref 또는 모든 input image를
포함하지 않는 generated link는 거부합니다.

expected remote ref는 `refs/uploads/issues/<pr-number>`입니다. upload는 later
failure 전에 해당 ref를 create 또는 update할 수 있습니다. command가 시작되면
CDP로 조용히 전환하지 말고, 멈춰서 selected body/comment 변경 여부를 보고하며
upload ref가 남을 수 있음을 명시합니다.

## CDP staging 및 browser

explicit selection 이후 또는 target write capability를 사용할 수 없을 때만 이
route를 사용합니다. browser automation workspace 아래에 run-owned directory를
만듭니다. browser가 접근하지 못할 수 있으므로 `/tmp` 를 기본 staging location으로
사용하지 않습니다. image alt text로 안전한 descriptive filename을 사용합니다.

browser 순서는 다음과 같습니다.

1. CDP 또는 Chrome DevTools MCP를 통한 authenticated existing Chrome session;
2. CDP/Playwright를 통한 authenticated persistent browser profile;
3. `Unverifiable` 로 중단하고 CDP recovery path를 설명한다.

첫 번째 선택지에서는 사용자에게
`chrome://inspect/#remote-debugging`, Chrome DevTools MCP의
`--autoConnect` 및 one-time Chrome Allow prompt가 필요할 수 있음을
설명합니다. cookies, tokens 또는 private identity details를 출력하지
않습니다. Orca 또는 다른 desktop controller를 fallback으로 실행하지
않습니다.

Chrome 136+는 default data directory에 대한 remote-debugging switch를
무시합니다. 사용자의 default profile을 port와 함께 재실행하면 동작한다고
약속하지 않습니다. 직접 실행한 endpoint에는 dedicated `--user-data-dir` 와
one-time login이 필요합니다. 설치된 Chrome/DevTools MCP가 지원하면
`--autoConnect` 는 사용자의 명시적 Allow action 이후에만 이미 실행 중인
profile에 attach할 수 있습니다. `DevToolsActivePort` file은 availability
evidence가 아니므로 current socket과 browser endpoint를 확인합니다.

## Upload 및 composer 안전성

target PR page를 열고 visible attachment control을 사용합니다. hidden file
input에 의존하지 않습니다. 각 `![Uploading ...]()` placeholder가 실제
`user-attachments/assets/...` URL 또는 equivalent image element가 될 때까지
기다립니다. bounded timeout으로 polling하고 실패 시 마지막 visible diagnostic을
보존합니다.

입력 전에 composer를 검사합니다. non-empty user draft는 blocker이므로
교체하지 않습니다. asset URL을 수집한 뒤 run-owned composer content만 지우고
textarea가 비어 있으며 comment button이 disabled인지 확인합니다. upload를
테스트하려고 empty comment를 submit하지 않습니다.

## Body 또는 comment 갱신

generated image Markdown을 requested location에 삽입합니다. location이 없으면
exact source heading `## 스크린샷` 을 우선하고, 없으면 AI footer 앞에 삽입하거나
body 끝에 추가합니다. 그 외에는 original body를 가능한 한 byte-stable하게
유지합니다. GitHub API 또는 equivalent를 통해 body만 업데이트하고 반환된
body에 모든 asset이 포함되는지 확인합니다. 명시적으로 선택한 existing
comment의 경우 해당 comment만 업데이트하고 관련 없는 content를 보존합니다.
temporary composer comment는 절대 submit하지 않습니다.

## Verification 및 cleanup

선택한 body/comment source를 다시 읽습니다. 그 다음 HTML media type을 사용한
REST `body_html` 또는 GraphQL `bodyHTML` 과 같은 GitHub-rendered HTML을
요청하고, 생성된 모든 asset이 expected image element/link로 표현되는지
확인합니다. reviewed extension route에서는 target repository의
`git/ref/uploads/issues/<pr-number>` 도 확인하고 각 generated link가 해당 ref를
이름에 포함하는지 검증합니다. CDP에서는 rendered PR page를 확인합니다.
GitHub가 asset URL을 `private-user-images.githubusercontent.com` 으로 다시
쓸 수 있는데, 이는 mismatch가 아니라 성공적인 rewrite입니다. Markdown
presence 또는 successful update response만으로는 절대 `Pass` 가 아닙니다.
signed URL JWT 또는 query string을 logs, artifacts나 final response에
노출하지 않습니다.

run-owned staging directory만 삭제하고 없어진 것을 확인합니다. cleanup이
실패하면 exact owned path를 보고하고 `Pass` 를 주장하지 않습니다. upload 또는
verification이 실패하면 selected body/comment 변경 여부를 보고하며, comment를
submit하거나 route를 조용히 바꾸어 retry하지 않습니다.

## Producer handoff

handoff는 다음을 포함할 때만 유효합니다.

```text
evidence_required: true
producer: tk-browser-verify | tk-prototype
evidence_directory: <absolute run-owned path>
artifacts:
  - path: <absolute non-empty image path>
    criterion: <criterion or caption>
    inspected: true
```

`tk-browser-verify` 에는 producer의 `Pass` result와 기존 `Evidence directory` 및
`Screenshot` entries가 필요합니다. `tk-prototype` 에는 tested screenshot path와
actual image inspection이 필요하며 Guard comparison을 official runtime
verdict로 설명하지 않습니다. handoff가 required인데 누락되었거나 유효하지
않으면 upload 전에 `Blocked` 를 반환합니다. parent는 created PR을 유지할 수
있지만 full completion 대신 `evidence_state: blocked` 를 보고해야 합니다.

## 검토된 dependency

controlled install은
[`MTGVim/gh-attach@v0.7.0-mtgvim.1`](https://github.com/MTGVim/gh-attach/releases/tag/v0.7.0-mtgvim.1),
reviewed fork of the MIT-licensed `enthus-appdev/gh-attach@v0.7.0`입니다.
해당 release에는 `LICENSE`, `THIRD_PARTY_NOTICES.txt` 및 checksums가
포함됩니다. TigerKit은 그 source를 vendor하거나 auto-install하지 않습니다.

CDP workflow는 다음을 개념적으로 참고했습니다.
[`github-upload-image-to-pr`](https://github.com/tonkotsuboy/github-upload-image-to-pr);
이 package에는 upstream source를 복사하지 않습니다.
