# 설명 페이지의 다건 피드백과 영상

설명 HTML을 요청하여 제작했을 때만 읽습니다. 대화 설명에 파일 제작을 추가하는 조건이 아닙니다.
원본 HTML과 archify finalize receipt를 유지하고 별도 studio 사본을 만듭니다.

```sh
python3 <loaded-package>/scripts/add_feedback_studio.py --input <page.html>
python3 <loaded-package>/scripts/add_feedback_studio.py --input <page.html> --video <image-block-id>=<movie.mp4>
```

기본 출력은 원본 옆의 `<stem>.studio.html`입니다. 기존 출력·중복 주입·닫는 body 없음·대상 ID 없음·대상 안 이미지 없음은 거부합니다.
`--output`은 원본과 같은 폴더의 새 이름으로 지정합니다. 상대 이미지·링크가 깨지지 않게 원본 폴더를 유지합니다.
`--video`는 반복할 수 있으며 패널별 영상만 해당 이미지 자리에 넣습니다. archify는 `@image` 블록 ID,
일반 HTML은 이미지를 포함한 요소 ID를 사용합니다. 페이지 전체 영상 하나는 상단 카드로 넣지 않고
`tk-video`의 피드백 플레이어로 따로 전달합니다. MP4를 내장하지 않으므로 함께 보관·전달합니다.
원래 이미지는 poster와 인쇄·내보내기·no-JS·파일 없음 때의 그림으로 유지합니다.

archify의 패널·Ask dialog 구조를 최대 2초 기다려 판별하고 일치하면 기존 Ask·드래그 인용·단건 복사를 보존하며
“목록에 담기”를 추가합니다. Ctrl/⌘+Enter는 조합 확정 뒤 목록에 담습니다.
DOM 계약이 일치하지 않으면 일반 모드에서 섹션 제목 버튼과 드래그 인용 버튼·별도 dialog를 제공합니다.
오른쪽 아래 목록은 선택·위치 이동·삭제·선택 복사를 지원하며 모두 지우기는 확인을 거칩니다.
`page-feedback:<파일 경로>`에 브라우저 내 저장하고 저장소가 차단되어도 현재 페이지에서 계속 동작합니다.
복사 결과는 페이지 제목·경로·건수, 위치 ID·인용·피드백을 포함합니다. 로컬 경로도 복사되므로 외부 공유 전에 확인합니다.
붙여 넣은 목록은 위치 ID 단위로 고치고 같은 표현·유형을 페이지 전체에서 찾아 함께 고칩니다.
archify 원고는 `patch explainer`로 수정하며 ID를 보존하고 재생성·검사한 뒤 새 studio를 만듭니다.

studio는 외부 요청이 없고 원본의 `html[data-theme]`을 따릅니다. 배속은 0.75×–2×를 모든 삽입 영상에 적용합니다.
인쇄에서는 피드백 UI와 영상을 숨기고 원래 이미지를 표시합니다. archify의 `.interactive` 제거 내보내기를 이용하되,
실제 내보내기를 하지 않았다면 인쇄 에뮬레이션이나 소스 관찰만으로 PNG·PDF 내보내기 성공을 주장하지 않습니다.
일반 HTML의 별도 내보내기 구현은 원래 이미지가 남는지 직접 확인합니다.

## 출처와 결합 범위

archify `a4065941f12be7967436261d9934784e381d423c`의 `archify/explainer/reader.js`에서
Ask dialog와 단건 복사, 내보내기 시 `.interactive` 제거를 확인했습니다.
`keep`: 원본·receipt·기존 Ask와 단건 복사. `adapt`: 별도 사본에 다건 목록과 이미지 자리 영상을 추가합니다.
`omit`: archify 코드 복제·수정, 전체 페이지 영상의 상단 삽입, 자동 업로드입니다.
현재 결합 대상은 `.panel`, `.panel-head`, `.panel-id`, `.ask-dialog`, `.ask-button`, `.ask-floating`과 dialog 내부 요소입니다.
의존성 클래스가 바뀌면 완전한 dialog 구조를 확인한 뒤 일반 모드로 전환합니다.
