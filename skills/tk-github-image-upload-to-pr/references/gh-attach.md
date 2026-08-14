# `gh-attach` 경로

## 실행 없는 신뢰 사전 점검

`gh attach --help`를 포함한 확장 명령을 실행하기 전에 `gh extension list`를
읽습니다. 이 명령이 성공했을 때 `NAME`이 정확히 `gh attach`인 행 하나의
`REPO`와 `VERSION`을 확인합니다.

```text
reviewed-fork
  REPO=MTGVim/gh-attach
  VERSION=v0.7.0-mtgvim.1

reviewed-upstream
  REPO=enthus-appdev/gh-attach
  VERSION=v0.7.0

unreviewed-upstream
  REPO=enthus-appdev/gh-attach
  VERSION=<other proven version/ref>

absent
  gh extension list succeeded, but no gh attach row exists

unknown
  list failed; or the row is duplicate, incomplete, ambiguous, or belongs to
  another distribution; or provenance/version cannot be proved
```

`GitHub CLI` 확장은 `GitHub`가 검증하거나 서명하거나 보증하는 실행물이
아닙니다. `gh attach --help` 성공, 실행 파일 존재, 공개 저장소 또는 추측한
설치 경로는 신뢰 근거가 아닙니다. `gh extension list` 출력을 안전하게 해석할
수 없으면 내부 배치나 느슨한 해석기로 보완하지 않고 `unknown`으로 처리합니다.

`reviewed-fork`와 `reviewed-upstream`은 추가 신뢰 질문, 경고, 재설치 또는 포크
교체 없이 사용합니다. `unreviewed-upstream`은 실행 전에 공급망 위험을 짧게
설명하고 다음 중 하나를 현재 대화 차례에 명시적으로 선택하게 합니다.

- 현재 설치된 버전 사용
- `gh extension install MTGVim/gh-attach --pin v0.7.0-mtgvim.1`로 교체
- `CDP` 대체 경로

승인 전에는 설치본을 실행하거나 교체하지 않습니다. `unknown`은 실행 파일을
실행하지 않고 출처 복구, 검토된 포크 또는 `CDP`를 제시합니다. `absent`에서는
검토된 고정 포크를 권장하고 `CDP`도 제시하되 자동 설치하지 않습니다. 승인된
설치 뒤에는 `gh extension list`를 다시 읽고 재분류합니다.

## 실행 권한과 수행

실행이 허용된 상태에서만 `gh attach --help`, `gh auth status` 및
`gh api repos/<owner>/<repo>`의 `.permissions.push`를 확인합니다. 공개/비공개
여부로 권한을 추론하지 않습니다. 대상 쓰기 권한이 없으면 확장을 실행하지 않고
그 사실을 설명한 뒤 사용자가 선택한 `CDP` 경로로 전환합니다.

실행:

```text
gh attach --repo <owner>/<repo> <pr-number> <image>...
```

`--comment`를 전달하지 않습니다. 스킬이 정확한 본문/댓글 배치를 유지할 수
있도록 생성된 이미지 마크다운만 수집합니다. 빈 출력, 예상하지 못한 마크다운
외 출력, 다른 저장소나 참조 또는 모든 입력 이미지를 포함하지 않는 생성 링크는
거부합니다.

예상 원격 참조는 `refs/uploads/issues/<pr-number>`입니다. 업로드는 이후 실패
전에 해당 참조를 만들거나 갱신할 수 있습니다. 명령이 시작된 뒤 실패하면
`CDP`로 조용히 전환하지 않습니다. 선택한 본문/댓글 변경 여부와 업로드 참조가
남을 수 있음을 보고합니다.

## 검증

선택한 본문/댓글 원문을 다시 읽고 `REST body_html` 또는 `GraphQL bodyHTML` 같은
`GitHub` 렌더링 HTML에서 모든 자산이 이미지 요소나 링크로 표현되는지
확인합니다. 대상 저장소의 `git/ref/uploads/issues/<pr-number>`를 확인하고 각
생성 링크가 해당 참조를 이름에 포함하는지도 검증합니다.

`GitHub`가 자산 URL을 `private-user-images.githubusercontent.com`으로 다시
쓰는 것은 허용합니다. 마크다운 존재 또는 성공한 갱신 응답만으로 `Pass`를
주장하지 않습니다. 서명된 URL의 JWT나 질의 문자열을 로그, 산출물 또는 최종
응답에 노출하지 않습니다.

## 검토된 의존성

다음 두 배포본만 무질문 신뢰 대상입니다.

- [`MTGVim/gh-attach@v0.7.0-mtgvim.1`](https://github.com/MTGVim/gh-attach/releases/tag/v0.7.0-mtgvim.1)
- [`enthus-appdev/gh-attach@v0.7.0`](https://github.com/enthus-appdev/gh-attach/releases/tag/v0.7.0)

검토된 포크 릴리스는 상위 `v0.7.0` 대비 응용 프로그램 소스 변경이 없고
`LICENSE`, `THIRD_PARTY_NOTICES.txt` 및 체크섬을 포함합니다. `TigerKit`은 소스,
사전 빌드 바이너리 또는 체크섬 데이터베이스를 저장소에 포함하지 않습니다.
