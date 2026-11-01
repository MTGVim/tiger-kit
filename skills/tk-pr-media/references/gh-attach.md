<a id="gh-attach-path"></a>
# `gh-attach` 경로

<a id="host-cli-and-authentication-boundary"></a>
## 호스트 CLI와 인증 경계

먼저 호스트에 작동하는 `gh` 실행 파일이 있는지 확인합니다. 없거나 에이전트가 안전하게
수행할 수 없는 호스트 수준 복구가 필요하다면, 정확한 설치·복구 완료 신호와 업로드 재개
행동을 담아 `tk-wizard`를 호출합니다. 업로드의 부수적인 의존성으로 호스트 CLI를
설치하지 않습니다.

대화형 `gh auth login`, 계정·저장소 권한 변경과 그 밖의 사용자만 수행할 수 있는
인증 단계도 `tk-wizard`의 담당입니다. 해당 인계가 대기 중인 동안에는 업로드하지
않습니다. `gh auth status`로 입증되면 이미 인증된 CLI를 비대화형으로 재사용합니다.
일반적인 인증 확인은 이 스킬에서 수행합니다.

<a id="trust-preflight-without-execution"></a>
## 실행 없는 신뢰 사전 점검

`gh attach --help`를 포함하여 확장 명령을 실행하기 전에
`gh extension list`를 읽습니다. 명령이 성공하면 `NAME`이 정확히 `gh attach`인
단일 행의 `REPO`와 `VERSION`을 확인합니다.

```text
reviewed-upstream
  REPO=enthus-appdev/gh-attach
  VERSION=v0.7.0
  COMMIT=663d13d6e42b98eadf6f1d9a517813b8a0f4eaf1

reviewed-fork (existing installation only)
  REPO=MTGVim/gh-attach
  VERSION=v0.7.0-mtgvim.1
  COMMIT=77e51e2a0b8e099b6e9fc7310ad0c2d5a319c60b

unreviewed-upstream
  REPO=enthus-appdev/gh-attach
  VERSION=<other proven version/ref, or reviewed tag with a different commit>

absent
  gh extension list succeeded, but no gh attach row exists

unknown
  list failed; or the row is duplicate, incomplete, ambiguous, or belongs to
  another distribution; or provenance/version/commit cannot be proved
```

검토된 두 배포본 중 하나로 분류하기 전에 GitHub Git refs API로 정확한 태그를
해석하고, 객체 타입이 `commit`이 될 때까지 Git tags API로 annotated tag 객체를
벗겨 냅니다. 위의 전체 `COMMIT`과 일치해야 합니다. 태그
객체 SHA, 축약 SHA, 버전 문자열이나 release의 `target_commitish`는 해당
커밋이 아닙니다. 이번 실행 안에서 일치하는 최신 근거를 재사용하고, 설치 후나
설치 상태가 바뀐 뒤에는 다시 확인합니다. 입증된 upstream 불일치는 `unreviewed-upstream`이며,
대응 관계를 확인할 수 없거나 fork가 불일치하면 `unknown`입니다. 이 근거를 알아내려고
확장 기능을 실행하지 않습니다. 소스 revision 대응 관계가 설치된 바이너리의 무결성을 입증하지는 않습니다.

`GitHub CLI` 확장 기능은 `GitHub`가 검증, 서명하거나 보증한 실행 파일이
아닙니다. `gh attach --help` 성공, 실행 파일의 존재, 공개 저장소나
추정한 설치 경로는 신뢰 근거가 아닙니다. `gh extension list` 출력을
안전하게 해석할 수 없다면 내부 디렉터리 구조 지식이나 느슨한 파서로 보완하지 말고
`unknown`으로 분류합니다.

`reviewed-fork`와 `reviewed-upstream`은 추가 신뢰 질문, 경고,
재설치나 fork 교체 없이 사용합니다. `unreviewed-upstream`이면 공급망
위험을 간단히 설명하고, 실행 전에 현재 턴에서 다음 중 하나를 명시적으로 선택받아야 합니다.

- 현재 설치된 버전을 사용합니다.
- `gh extension install enthus-appdev/gh-attach --pin v0.7.0`으로 교체합니다.
- `CDP` 대체 경로를 사용합니다.

태그가 고정한 커밋으로 해석되는 동안에만 검토된 upstream 설치를 제안합니다.
이동된 태그를 재설치해도 해당 커밋을 복구하지 못합니다. 대신 출처
복구나 `CDP`를 제안하고, 변경된 revision의 사용이 승인되었다면 검토되지 않은 것으로 명시합니다.

승인 전에 설치된 확장 기능을 실행하거나 교체하지 않습니다. `unknown`이면
바이너리를 실행하지 않고 출처 복구, 검토된 upstream이나 `CDP`를 제안합니다.
`absent`이면 검토된 고정 upstream을 권고하고 `CDP`도 제안하되 자동으로 설치하지 않습니다.
사용자가 검토된 설치를 선택하고 승인한 뒤 태그 대응 관계를 검증하고,
고정된 `gh extension install` 명령을 한 번 실행합니다. 에이전트가 실행할 수 있는 이 단계를
`tk-wizard`에 위임하지 않습니다. 바이너리 확장 기능 고정에는 임의의 소스 커밋 SHA가 아니라 release 태그를 사용합니다.
확장 기능을 실행하기 전에 `gh extension list`를 다시 읽고 커밋 대응 관계를 재확인합니다.
별도로 승인된 검토 fork 설치는 보존합니다. 기본값으로 요구하거나,
upstream을 사용할 수 없을 때 알리지 않고 개인·비공개 미러로 바꾸지 않습니다.

<a id="execution-authority-and-operation"></a>
## 실행 권한과 작업

실행이 승인된 뒤에만 `gh attach --help`, `gh auth status`와
`gh api repos/<owner>/<repo>`의 `.permissions.push`를 확인합니다. 대상이
공개인지 비공개인지로 접근 권한을 추론하지 않습니다. 인증이나 쓰기 권한에 사용자 행동이 필요하면
정확한 행동을 `tk-wizard`에 인계합니다. 그렇지 않고 대상 쓰기 권한이 없다면
확장 기능을 실행하지 않으며, 사용자가 선택한 `CDP` 경로로만 전환합니다.

다음을 실행합니다.

```text
gh attach --repo <owner>/<repo> <pr-number> <image>...
```

`--comment`를 전달하지 않습니다. 스킬이 본문·댓글의 정확한 배치를 유지할 수 있도록
생성된 이미지 Markdown만 수집합니다. URL과 렌더링 매개변수를 포함하여
생성된 모든 이미지 Markdown 토큰의 바이트를 그대로 보존합니다. 역할 머리글, 이미지 행 하나와
그 아래 캡션 행 하나로 주변 표 배치를 다시 구성하며, 각 이미지의 역할과 쌍을 유지합니다.
표시용 마스킹은 비공개 변경 입력과 분리합니다. 빈 출력, 예상하지 못한 Markdown 이외
출력, 다른 저장소나 참조의 링크, 입력 이미지가 하나라도 누락된
출력은 거부합니다.

예상 원격 참조는 `refs/uploads/issues/<pr-number>`입니다. 업로드가 이후 실패하기
전에 이 참조를 생성하거나 업데이트할 수 있습니다. 명령이 시작된 뒤 실패했다고 알리지 않고
`CDP`로 바꾸지 않습니다. 선택한 본문·댓글이 바뀌었는지와
업로드 참조가 남아 있을 수 있다는 점을 보고합니다.

<a id="verification"></a>
## 검증

선택한 원시 본문·댓글을 다시 읽고, 생성된 모든 이미지 토큰이 바이트까지 일치하게 정확히 한 번 나타나는지 확인합니다.
확장 기능이 생성한 Markdown과 토큰을
비교합니다. `Pass` 전에 각 자산에서 다음을 모두 검증합니다.

- 삽입된 URL이 파일 보기 HTML 페이지가 아니라 이미지 콘텐츠로 연결됩니다. `raw=true` 같은 렌더링 매개변수가
  없는 `blob` 페이지는 이미지 콘텐츠가 아닙니다. 이 매개변수는 예시이며 모든 경로에 요구되는 URL 형식은 아닙니다.
- 같은 업로드 객체를 인증된 요청으로 가져오면 `image/*` 콘텐츠 타입의 비어 있지 않고 디코딩 가능한 이미지 바이트가
  반환됩니다. 업로드 ref의 원시 콘텐츠 엔드포인트도 한 가지 방법입니다. 정확한 저장소, 커밋·객체와 경로가
  삽입한 자산과 일치하는지 확인합니다. JSON 메타데이터 응답, 파일 확장자나 성공 HTTP 상태만으로는 충분하지 않습니다.

대상 저장소에서 `git/ref/uploads/issues/<pr-number>`를 확인하고, 불변 커밋 URL을 포함하여 연결된 모든 업로드 커밋·객체가
해당 ref에서 도달 가능한지 검증합니다. 업로드 ref에 나타나는 "commit does not belong to any branch" 안내는
예상되는 것이며, 그 자체로 실패를 뜻하지 않습니다.

`GitHub`가 렌더링된 자산 URL을 `private-user-images.githubusercontent.com`으로 재작성할 수 있음을 허용합니다.
삽입한 원시 Markdown은 재작성된 브라우저 URL이 아니라 원래 출력과 비교합니다. 브라우저 세션 렌더링은 선택 사항입니다.
요청받거나 수행한 경우에는 각 이미지의 로드 상태를 확인합니다. `REST body_html`, `GraphQL bodyHTML`이나 `<img>` 요소만으로는
렌더링을 입증할 수 없습니다. receipt의 `Verification` 필드에 `rendering: checked | not performed | unavailable`을
기록합니다. Markdown 변경, 이미지가 아닌 바이트, 도달할 수 없는 업로드 객체나 알려진 이미지 오류에는 `Fail`을 반환합니다.
인증된 fetch나 업로드 ref 도달 가능성을 확인할 수 없다면 `Pass` 대신 구체적인 제한을 `Unverifiable`로
보고하고 실제 원격 상태를 보존합니다.
표시하는 진단 정보에서는 비밀을 포함한 값만 마스킹하고 안전한 렌더링 매개변수는 보존합니다. 서명된
값을 로그, 산출물이나 최종 응답에 노출하지 않으며, 마스킹한 진단 정보를 본문·댓글에 다시 넣지 않습니다.

<a id="reviewed-dependencies"></a>
## 검토된 의존성

다음의 정확한 배포본과 해석된 커밋만 검토되어 있습니다.

- [`enthus-appdev/gh-attach@v0.7.0`](https://github.com/enthus-appdev/gh-attach/commit/663d13d6e42b98eadf6f1d9a517813b8a0f4eaf1)은 기본 설치 출처입니다.
- [`MTGVim/gh-attach@v0.7.0-mtgvim.1`](https://github.com/MTGVim/gh-attach/commit/77e51e2a0b8e099b6e9fc7310ad0c2d5a319c60b)은 기존 또는 별도 승인된 설치를 위해 유지합니다.

검토된 fork release는 upstream `v0.7.0`과 애플리케이션 소스 변경이 없으며
`LICENSE`, `THIRD_PARTY_NOTICES.txt`와 체크섬을 포함합니다. `TigerKit`은
소스, 사전 빌드 바이너리나 체크섬 데이터베이스를 vendoring하지 않습니다.
