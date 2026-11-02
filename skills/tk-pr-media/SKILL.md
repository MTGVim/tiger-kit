---
name: tk-pr-media
description: "[user/auto] 기존 GitHub PR 본문 또는 지정된 댓글에 로컬 이미지·GIF·MP4를 첨부합니다. 명시적 미디어 요청이나 정확한 근거 인계에만 사용합니다."
disable-model-invocation: false
argument-hint: "<PR and local media path(s)>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

<a id="github-pr-media-upload"></a>
# GitHub PR 미디어 업로드

<a id="shared-references"></a>
## 공통 참조

현재 설치된 담당 스킬에서 해당 분기의 조건에 따라 기준을 읽습니다. 소유자나 자원이 없거나 일치하지 않으면
해당 작업을 중단합니다. 기억, 다른 설치본이나 승인되지 않은 설치 대신 `tk-setup-skills`를 사용합니다.
참조 읽기는 워크플로 실행이나 변경 권한을 부여하지 않습니다.

- 사용자 소유 결정·누락된 승인·미충족 선행 조건을 질문이나 질문 도구 입력으로 제시하기 직전에 [질문 라운드](../tk-questioning/references/questions.md)를 이번 작업에서 읽었는지 확인하고 누락했으면 먼저 읽습니다. 독립적인 결정과 승인은 각각 별도 질문으로 두며, 승인 선택지를 결정 질문에 섞지 않습니다.
- 사용자에게 완료 보고, 산출물 경로 인계나 여러 속성을 비교하는 대화 응답을 전달하기 전에 [대화 전달](../tk-writing/references/delivery.md)을 읽습니다. 작업별 구체적인 출력 계약이 우선합니다.

기존 GitHub PR에 대한 명시적인 로컬 이미지·동영상 근거 요청이나
`evidence_required: true`가 있는 정확한 `tk-pr-open` 범용 manifest 인계를 처리합니다.
자동 호출 조건은 상위 인계뿐입니다.

<a id="optional-motion-supplements"></a>
## 선택적 동작 보충 자료

선택한 MP4에는 [기본 동영상 첨부](references/video-upload.md)를 읽습니다. 이미지 전용 확장 단계와 다른 업로드·바이트·플레이어 검사는 해당 참조가 담당합니다. 유효한 선택적 보충 자료에는 미디어 타입, 실행 소유 경로, 기준·head, 재생 시간·viewport, 검사한 프레임과 샘플링 경고가 포함됩니다. 필수 이미지 manifest 형식을 흉내 내도록 요구하지 않습니다. `publication_selected: true`이거나 사용자가 정확한 산출물·대상을 명시적으로 선택했을 때만 업로드합니다.

선택된 GIF 프레임 조립에는 검토된 확장 기능을 `--gif`, 명시적인 `.gif` 이름과 프레임 열에 맞는 지연 시간으로 사용합니다. v0.7.0에서는 `--json` 없이 stderr를 별도로 수집합니다. 모든 프레임 상한·축소·크기 초과 경고를 보존하고, 실제 image/gif 바이트와 여러 디코딩 프레임을 검증하며, 재생을 주장할 때는 애니메이션을 확인합니다. 5MiB 목표는 엄격한 한도가 아닙니다. 크기 초과와 변경된 타이밍을 공개합니다. 기존 필수 스크린샷 쌍은 그대로 유지합니다.

<a id="scope"></a>
## 범위

범위가 정해진 업로드 하나를 처리합니다. 로컬 이미지를 검증하고 staging하며,
저장소 범위의 GitHub 첨부 파일을 업로드하고, PR 본문이나 선택한
댓글을 최소한으로 업데이트한 뒤 소스 Markdown과 업로드된 이미지 객체를 검증합니다. 기본 대상은 PR 본문입니다.

`tk-pr-open`에서는 생성자와 무관한 근거 필드를 검증하며, 생성한
스킬 이름에 따라 분기하거나 허용 목록을 만들거나 그 이름을 요구하지 않습니다. 필수 근거가 없거나 유효하지 않다면
근거 인계를 `Blocked`로 표시합니다. 이미 생성된 `tk-pr-open` PR을 되돌리지 않습니다.

확장 경로를 분류하고 실행하려면 [references/gh-attach.md](references/gh-attach.md)를 사용합니다.
[references/cdp-fallback.md](references/cdp-fallback.md)는
CDP를 선택했거나 확장 경로가 대상 쓰기
기능을 사용할 수 없는 경우에만 읽습니다. 사람이 수행해야만 하는 정확한 호스트 설정,
인증, 권한이나 재시작 단계에만 `tk-wizard`를 호출합니다. 인계 전후에 이 스킬의 업로드 대상과 경로를
유지합니다. 브라우저로 제어하는 런타임 검증에는 `tk-browser-verify`를 사용합니다.

<a id="-checkpoint---stop--upload-mutation-boundary"></a>
## 🔴 점검 지점 · 🛑 중단 · 업로드 변경 경계

업로드나 PR 본문·댓글 업데이트 전에 명시적으로 선택된 대상, 유효한 로컬 근거나 생성자 인계, 인증된 경로와 요청된 쓰기 범위를 재검증합니다. 이러한 선행 조건을 확립할 수 없으면 `Blocked`나 `Unverifiable`로 중단합니다.

<a id="workflow"></a>
## 워크플로

1. 일반 로컬 이미지 파일이나 유효한 생성자 근거 인계에서 `origin`, 현재 PR과
   실행 저장소를 확인합니다. 기존 PR
   본문을 읽습니다.
2. 기존 `## 스크린샷` 제목을 재사용합니다. 없다면 AI
   footer 앞에 삽입하거나 끝에 추가합니다. 무관한 본문 내용을 보존합니다. manifest 산출물의 캡션에는 제공된 기준,
   역할, 정확한 `display_route`, 상태·영역, viewport와 비교를 사용합니다. 파일명,
   OCR, 원시 URL이나 생성자 신원에서 이를 도출하지 않습니다. `visual-preservation`의 baseline과 after를 한 쌍으로 명확히 표시합니다.
   manifest 유무와 관계없이 모든 쌍에 검증된 경로·화면을 명시하는 제목,
   기대 동작을 설명하는 한 문장, `수정 전` / `수정 후` 같은 역할 머리글, 이미지 행 하나와
   그 아래 각 이미지의 관찰 내용을 설명하는 캡션 행을 추가합니다. 제공된 근거를 전달하고,
   경로·화면 근거가 없으면 만들어 내지 말고 누락을 공개합니다. staging 파일명은
   머리글, 캡션이나 충분한 설명이 아닙니다.
3. [gh-attach](references/gh-attach.md)를 사용하여 적격 경로를 선택하고
   실행하거나, CDP를 선택한 뒤에만
   [CDP 대체 경로](references/cdp-fallback.md)를 읽습니다.
   저장소 공개 여부는 경로 선택 신호가 아니며, 원격 상태를 생성했을 수 있는
   경로에서 알리지 않고 다른 경로로 전환해서는 안 됩니다.
4. 선택한 경로에 사람이 수행해야만 하는 호스트 행동이 필요하면 범위를 한정한 인계를
   `tk-wizard`에 전달하고, 완료 신호 전에는 업로드하지 않습니다. 에이전트가 승인받아 수행하는 검토된
   확장 기능 설치는 여기서 계속 담당합니다. 마법사가 끝난 뒤 정확한 저장소, 대상, 이미지 집합과
   경로를 재개합니다.
5. 본문·댓글을 쓰기 직전에 [GFM 렌더링](../tk-pr-guidance/references/gfm-rendering.md)을 읽고, 생성된 미디어 토큰까지 반영한 정확한 후보를 검사합니다. 미디어 섹션 삽입도 포함하며, 실패·확인 불가 상태에서는 해당 쓰기를 보류합니다. 업로드와 본문 변경이 결합된 경로는 같은 참조의 사전 작성 본문 확인·사후 토큰 치환 확인을 구분합니다. GitHub API나 동등한 수단으로 요청된 본문이나 댓글만 업데이트합니다.
   `Pass` 전에 대상을 다시 읽고, 생성된 모든 이미지 토큰이 바이트까지 일치하게 정확히 한 번 나타나는지,
   쌍의 역할·캡션이 올바르게 연결된 상태인지, 인증된 fetch에서 모든 자산이
   디코딩 가능한 `image/*` 바이트인지, 연결된 모든 업로드 객체가 업로드 ref에서 도달 가능한지 검증합니다. 브라우저에서 실제 페이지를 열어 보는 검사는
   선택 사항이며, 쓰기 전 GFM 확인을 대신하거나 면제하지 않습니다. `Pass`의 선행 조건으로 삼지 말고 검사 여부를 receipt에 보고합니다.
6. 모든 종료 경로에서 소유한 staging 파일만 제거합니다. 이번 실행에 이미 기록된 리터럴 형태의 완전히 해석된 실행 소유 staging 절대 경로를 각 삭제 명령에 씁니다. 명령 치환, 다시 읽은 경로 파일이나 `head` 또는 `tail`로 파이프한 glob에서 대상을 도출하지 않습니다. 정확한 리터럴 경로를 모르면 삭제하지 말고 후보를 나열한 뒤 중단합니다.

<a id="execution-receipt--single-evidence-record"></a>
## 실행 receipt · 단일 근거 기록

모든 업로드 시도를 아래 단일 receipt에 기록합니다. 별도의 수명주기
출력이 아니라, 사용자 언어로 작성한 미디어 업로드 결과와
승인·검증 결정에 사용하는 유일한 근거 기록입니다. 없는 값에는 `none`이나 `unavailable`을 사용하며 추측하지 않습니다.

```text
Repository: <owner>/<repo>
PR / Target: <pr-number> / body | existing comment <comment-id>
Source images: <absolute path list>
Route: gh-attach | CDP
Entry: <exact reviewed command | browser route>
Generated Markdown: <asset refs | none>
Remote ref: <refs/uploads/issues/<pr-number> | none | unknown>
Verification: image-token byte match and single occurrence: <Pass | Fail | unavailable>; image bytes/type: <Pass | Fail | unavailable>; upload ref reachability: <Pass | Fail | unavailable>; gfm: <Pass | Fail | unavailable; exact candidate or combined-route pre/post scope>; rendering: <checked | not performed | unavailable>
Changed: <body/comment changed | unchanged | unknown>
Cleanup: <owned staging path removed | failed | not applicable>
Status: Pass | Fail | Pending | Blocked | Unverifiable
```

<a id="evidence-manifest-handoff"></a>
## 근거 manifest 인계

`evidence_required: true`이면 다음을 모두 요구합니다.

- `verification_status: Pass`, 비어 있지 않은 기준, 근거 종류, 비교 결과와 제한 사항이 있어야 합니다.
- 모든 산출물에는 역할, 비어 있지 않은 이미지, 절대 경로, 실행 소유 근거 디렉터리, 상태·영역과 viewport가 있어야 합니다.
- 모든 이미지는 `inspected: true`로 표시되어야 하며, origin이 없는 정확한 `display_route` 또는 명시적인 안전한 생략
  제한 사항이 있어야 합니다. 누락된 경로를 재구성하거나 마스킹하지 않습니다.
- `visual-preservation`에는 검증된 쌍의 baseline 산출물과 after 산출물이 모두 있어야 합니다.

임의의 스크린샷, 누락된 경로, `Pass`가 아닌 결과, 검사하지 않은 산출물, 불완전한 보존 쌍과
현재 실행에 연결되지 않은 산출물은 거부합니다. 필수 근거가 없거나 유효하지 않으면 업로드 전에 `Blocked`를 반환합니다.

<a id="prohibitions"></a>
## 금지 사항

- PR을 생성하거나 merge하거나, 리뷰어를 바꾸거나, release를 발행하거나,
  사용자가 명시적으로 해당 댓글 대상을 선택하지 않았는데 댓글을 삽입하지 않습니다.
- `tk-browser-verify`를 우회하거나 Orca 또는 화면 제어를 자동
  브라우저 대체 경로로 사용하지 않습니다.
- 기존 초안을 덮어쓰거나 comment, close-with-comment 또는
  그 밖의 제출 버튼을 클릭하지 않습니다.
- 공개·비공개 여부로 경로를 선택하거나, 자리표시자, Markdown의 존재, 고정 지연이나
  렌더링하지 않은 API 응답만으로 성공을 주장하지 않습니다.
- 서명된 URL, JWT나 비밀이 포함된 원시 쿼리 문자열을 로그에 남기거나 반환하지 않습니다. 안전성이 검증되고
  origin이 없는 `display_route`는 이 금지 대상이 아닙니다. manifest에서 제공한 pathname, query와 fragment를 정확히 보존합니다.
- 표시되는 출력에서는 비밀이 포함된 값(서명 매개변수, JWT, 토큰)만 마스킹하고, `raw=true` 같은
  렌더링 매개변수는 보존합니다. alt,
  URL과 렌더링 매개변수를 포함하여 생성된 각 이미지 Markdown 토큰의 바이트를 그대로 유지합니다. 주변 표 배치는 이미지 아래 캡션을 두도록 다시 구성할 수 있습니다.
  마스킹하거나 요약한 출력에서 링크를 다시 만들지 않습니다.
  비밀이 포함된 원본을 로그, receipt나 근거 산출물에 복사하지 않습니다.

<a id="failure-handling"></a>
## 실패 처리

확장 기능 부재·미검토 upstream에 관한 선택이나 사람이 수행해야만 하는
`tk-wizard` 완료 신호를 기다리는 동안에는 `Pending`을 반환합니다. 출처가 `unknown`이거나, 초안이 있거나,
설치를 거부했고 선택된 CDP 경로도 없다면 `Blocked`를 반환합니다. 인증,
이미지 바이트 검증이나 업로드 ref 도달 가능성을 확인할 수 없으면 `Unverifiable`을 반환합니다. 렌더링된 페이지
근거는 선택 사항이며 GFM 확인과 구별합니다. GFM 실패·확인 불가로 본문 쓰기를 보류했다면 그 상태를 유지합니다. 업로드, 원격 ref
검증이나 정리 오류에는 `Fail`을 반환합니다. 선택한 본문·댓글이 바뀌었는지와
업로드 ref가 남아 있을 수 있는지를 명시합니다.

`tk-pr-open`에서는 별도의 PR 작업 결과를 보존하고
근거 상태를 `uploaded`나 `blocked`로 반환합니다. 필수 근거가
차단된 상태인 동안 상위 작업은 전체 완료를 주장할 수 없습니다.

<a id="result"></a>
## 결과

결과 제목과 해당하는 업로드,
검증·정리 제목에는 사용자의 응답 언어를 사용합니다. 한국어에서는 `## GitHub 미디어 업로드`,
`## 업로드 결과`, `## 검증`, `## 정리`를 사용하고, 영어에서는 `## GitHub media upload`,
`## Uploaded`, `## Verification`, `## Cleanup`을 사용합니다. 기계 판독 receipt 키와
상태 줄은 그대로 유지합니다. 결과를 담당하는 섹션은 정확히
하나의 `Status: Pass|Fail|Pending|Blocked|Unverifiable` 줄로 끝냅니다. 자산 URL은 안전할 때만 노출하고
서명 매개변수는 마스킹합니다.

<a id="artifact-paths"></a>
## 산출물 경로

승인된 산출물 쓰기, checkout·전송·Git 제외 설정이나 임시 입력 소비 전에
[산출물 경로](../tk-artifacts/references/artifact-paths.md)를 읽습니다. 저장소 임시 파일에는 안전하고 소유권이 확인된 심볼릭 링크가 아닌 경로와
입증된 Git 제외를 사용합니다. 검사에 실패하면 해당 파일 분기를 중단합니다. 명시적인 최종 목적지와
담당자별 기본값을 보존합니다. 미리 채워진 입력은 완료된 입력이 아닙니다.
정리는 기록된 리터럴 형태의 해석 완료된 실행 소유 절대 경로만 대상으로 하며, cwd 상대 경로나 glob을 사용하지 않습니다.
