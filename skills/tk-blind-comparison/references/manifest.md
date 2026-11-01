<a id="manifest-and-commands"></a>
# manifest와 명령

HTML build에는 같은 설치 스킬 모음의 `tk-setup-skills` validator와 PyYAML을 갖춘 Python 3.9+가 필요합니다. build helper를 호출하기 전에 해당 스킬의 [metadata API 계약](../../tk-setup-skills/references/planner-cli.md)을 읽습니다. parser/소유 스킬 지원이 없으면 build를 중단합니다. 별도로 적용되는 승인이 있을 때만 환경을 준비합니다. 채팅 전용 요약은 이 validator를 로드하지 않습니다.

UTF-8 JSON을 사용합니다. 경로는 manifest를 기준으로 해석합니다. 제작자의 원본 HTML이 아니라 신원 단서가 없고 정규화된 사본으로 build합니다. 모든 항목/후보 쌍이 있어야 하며 누락/생성 실패를 명시적으로 표현합니다. study/item/candidate ID를 안정적으로 유지합니다.

```json
{
  "study_id": "voice-study-01",
  "version": "2",
  "seed": "fixed-study-seed",
  "title": "한국어 문장 청취 비교",
  "transformations": ["동일한 음량 기준으로 조정했습니다."],
  "favorite": true,
  "candidates": [{"id": "engine-one", "name": "Engine One"}, {"id": "engine-two", "name": "Engine Two"}],
  "items": [{"id": "sentence-01", "title": "발음과 자연스러움", "script": "오늘은 맑고 따뜻합니다.", "description": "같은 문장을 듣고 발음과 자연스러움을 평가해 주세요."}],
  "outputs": [
    {"item_id": "sentence-01", "candidate_id": "engine-one", "kind": "audio", "path": "prepared/one.wav"},
    {"item_id": "sentence-01", "candidate_id": "engine-two", "kind": "audio", "error": "생성 실패", "diagnostic": "private producer error"}
  ]
}
```

종류는 `audio`(WAV/MP3), `image`(PNG/JPEG/WebP), `video`(MP4/WebM), `text`(인라인 `text`)입니다. 중립적인 공통 제목/항목 설명/변환을 사용하고 비공개 제작자 오류는 `diagnostic`에만 넣습니다. 모든 실패 카드는 같은 중립적인 실패 메시지를 보여주며 원본 사유는 별도 키에 남깁니다. 텍스트는 escape하며 실행하지 않습니다.
선택적인 항목 `title`은 평가 주제에, `script`는 정확한 공통 원문에 사용합니다. `description`은 평가 안내를 제공합니다. 이 중립 필드는 현재 항목의 sticky 맥락에 유지됩니다. 긴 맥락은 내부 scroll을 사용하고 keyboard 접근성을 유지합니다.
helper는 공통 레이블과 텍스트의 literal 이름/ID를 점검합니다. 로고, 음성으로 말한 이름, watermark와 기타 의미상 단서는 수동으로 확인합니다. helper는 의미상 익명성을 입증할 수 없습니다.

패키지 내부 산출물 경로 점검 후 다음을 실행합니다.

```bash
python3 <package>/scripts/build_gallery.py build manifest.json --output <new-run-directory> --theme system
python3 <package>/scripts/build_gallery.py build manifest-v2.json --output <new-run-directory> --previous-key <old-run-directory>/answer-key.json --theme system
python3 <package>/scripts/build_gallery.py summarize ratings.json --key <matching-run-directory>/answer-key.json --output <new-evidence-directory>
python3 <package>/scripts/build_gallery.py summarize - --key <matching-run-directory>/answer-key.json --blind
```

build 전에 HTML 출력 선호 설정에 따라 `--theme`을 결정합니다. 출력 디렉터리는 점검된 Git 제외 실행 경로나 명시적인 목적지 아래의 새 디렉터리여야 합니다. 실행 파일은 symlink 상위 경로, 기존 목적지와 입력 파일을 포함한 목적지를 거부합니다.
소유 스킬의 metadata 검증은 호출자가 먼저 수행해야 하는 Git 제외 및 출력 점검을 대체하지 않습니다.
helper는 준비된 파일을 하나의 오프라인 HTML에 data URL로 포함하고 중립적인 ASCII `item-0001-slot-0001.ext` 표시용 사본도 유지합니다. 정답 키는 불투명 token을 원래 ID, 이름, 항목 콘텐츠 fingerprint, 비공개 실패와 seed 기반 레이블 순서에 연결합니다.
채팅 전용 집계에서는 붙여넣은 JSON을 stdin(`ratings: -`)으로 전달하고 `--output`을 생략합니다. 명령은 입력이나 결과를 저장하지 않고 검증된 요약을 출력합니다. `--blind`는 키에서 도출된 신원을 불투명 ID와 익명 후보 별칭으로 대체합니다. 이 별칭은 항목별로 섞인 표시 레이블이 아닙니다. 승인된 신원 공개에서만 해당 옵션을 생략합니다.

증분 build에서는 `--previous-key`를 재사용합니다. ID는 쉽게 추측할 수 있는 모델명 hash가 아니라 무작위 불투명 token에 연결됩니다. 후보 추가/제거 시 새 후보 집합으로 각 항목을 다시 섞고, 변경되지 않은 콘텐츠 fingerprint는 점수를 보존합니다. 관련 없는 비교에 study ID를 재사용하지 않습니다. 새 키를 export한 revision과 함께 유지합니다. HTML을 이동할 때는 로컬 파일 storage가 파일을 따라간다고 가정하지 말고 평가를 명시적으로 export/import합니다.

<a id="additional-public-evidence"></a>
## 추가 공개 근거

출력에는 `annotation`(비어 있지 않은 일반 텍스트)과 `links`를 포함할 수 있습니다.
`[{"label": "Mobile capture", "path": "prepared/mobile.png"}]` 형식을 사용합니다.
링크는 준비된 PNG/JPEG/WebP, HTML, TXT 또는 PDF 사본을 허용합니다. 연결된 HTML은 자체 완결적으로 만듭니다. build 전에 문서 metadata, 제목, script, alt text, embedded 콘텐츠와 눈에 보이는 신원 단서를 정규화합니다. builder는 annotation, 레이블과 UTF-8 HTML/TXT 내용(디코딩한 HTML entity 포함)의 literal 후보 이름/ID를 점검합니다. binary metadata, PDF 텍스트, 인코딩/pixel/의미상 신원은 여전히 수동 확인이 필요합니다. 압축된 byte는 텍스트가 아닙니다. 제작자 원본 HTML이나 정답 키를 공개 링크로 제공하지 않습니다.
원본 파일명은 비공개로 유지하고 복사 이름은 `item-NNNN-slot-NNNN-link-NNNN.ext`를 사용합니다.

이미지 카드는 언제나 중립 표시용 사본을 원본 크기로 새 tab에 여는 링크를 제공합니다. 이 로컬 링크를 위해 HTML과 표시용 사본을 함께 유지합니다. 주요 embedded media는 HTML만 이동해도 작동합니다. annotation은 escape된 텍스트이며 HTML이 아닙니다. 원본 파일은 수정하지 않습니다.
이 필드가 없는 기존 출력은 정확히 같은 fingerprint 알고리즘을 유지합니다. 공개 근거를 추가/변경하면 해당 카드의 fingerprint가 바뀌므로 변경된 평가 대상에 이전 점수를 말없이 적용할 수 없습니다. 변경되지 않은 근거를 다시 build하면 fingerprint가 보존됩니다.


<a id="optional-modes-and-split-delivery"></a>
## 선택적 방식과 split 전달

`build --mode gallery|versus --delivery single|split`의 기본값은 `gallery`와 `single`입니다.
두 옵션은 독립적입니다. versus는 같은 준비된 media/텍스트 manifest, 불투명 식별 정보, 항목별 seed 기반 섞기와 근거 fingerprint를 사용합니다. 상호작용, export와 재생 규칙은 [versus](versus.md)를 읽습니다. gallery는 media/텍스트 주요 출력을 유지합니다. versus는 준비된 자체 완결 HTML `path`가 있는 `kind: html`이나 준비된 HTML `links`가 있는 이미지 screenshot도 허용합니다. 첫 HTML 링크가 live preview가 됩니다. 대안은 명시적인 링크에 넣습니다. screenshot fallback이 필요하면 이미지와 HTML 링크를 사용합니다.

builder는 literal 이름/ID(디코딩한 entity 포함)를 점검하고 byte를 중립적인 `item-NNNN-slot-NNNN-link-NNNN.html` 이름으로 복사하며 fingerprint를 계산합니다. 원본을 수정하거나, 제작자 원본 HTML을 정규화하거나, 의존성을 재귀 수집하거나, 연결 파일을 순회하지 않습니다.
script, metadata, 인코딩된 단서와 의미상 단서를 수동으로 확인하고 외부 요청이 없는지 확인합니다.
현재 쌍의 preview만 `sandbox="allow-scripts allow-popups"` iframe으로 mount합니다. `allow-same-origin`, 부모 DOM 접근, form이나 최상위 탐색은 허용하지 않습니다. 숨겨진 frame은 단순히 숨기지 않고 제거합니다. 단일 우승자는 preview 하나를 유지할 수 있지만 공동 우승자 목록은 모든 우승자를 로드하지 않습니다. 다시 방문한 preview는 새로 시작합니다. 후보의 상호작용 상태는 비교 storage가 아닙니다. 이 sandbox는 격리 수단이며 sanitizer나 암호학적 익명성이 아닙니다.
로컬 iframe 실행을 사용할 수 없으면 카드의 캡처 toggle이나 중립 원본 링크를 사용합니다.
single 전달에서도 HTML과 복사 자원을 함께 유지합니다. `gallery.html`만 이동하면 embedded screenshot/media는 유지되지만 연결된 대화형 문서는 유지할 수 없습니다.

```bash
python3 <package>/scripts/build_gallery.py build manifest.json --output <new-run-directory> --mode versus --theme system
python3 <package>/scripts/build_gallery.py build manifest.json --output <new-run-directory> --mode versus --delivery split --theme system
python3 <package>/scripts/build_gallery.py build manifest.json --output <new-run-directory> --delivery split --theme system
```

single 전달은 `gallery.html`, 중립 표시/링크 파일과 `answer-key.json`을 유지합니다.
기본 single-gallery 렌더링과 평가 schema는 기존 인코딩 공개 매핑을 포함하여 변경되지 않습니다. 기본 single-versus 전달은 인코딩된 최소 정답 키(이름과 검증 명단/revision만 포함하며 비공개 진단은 제외)를 포함합니다. 명시적 공개 전에는 눈에 보이는 DOM/콘텐츠 밖에 유지됩니다. 오프라인 인코딩은 소스 검토에 대한 비밀 보장이 아닙니다.
우승자 화면의 `결과 보기`는 선택한 파일과 같은 loader로 embedded 키를 검증한 뒤 한 번의 행동으로 결과 표를 공개합니다. 완료/reload 후 자동 공개하지 않습니다.

다른 평가자나 separate-key single HTML에는 `--answer-key separate`를 사용합니다. split 전달은 항상 별도 키를 사용하며 `--answer-key embedded`를 거부합니다. 결과 버튼은 계속 활성 상태입니다. 로드된 키가 없으면 분리를 설명하고 파일 선택기를 엽니다. 해당 공개 행동에서 일치하는 키를 선택하면 결과 표로 이어집니다(필요하면 부분 비교 확인을 거칩니다). 관리 기능에서 키를 수동 선택하는 것만으로는 여전히 이름을 공개하지 않습니다. 취소되거나 유효하지 않은 파일 선택은 기록과 노출 상태를 보존합니다. 평가자 ZIP과 별도 키를 함께 배포하지 않습니다. 명시적인 자기 평가 전달에서는 embedded 경로를 사용할 수 있습니다.

split 전달은 `index.html`, `assets/item-NNNN-slot-NNNN.ext`와 선택적인 `assets/item-NNNN-slot-NNNN-link-NNNN.ext`, `comparison.zip`, 별도 `answer-key.json`을 씁니다.
ZIP에는 `index.html`과 참조하는 중립 자원만 포함합니다. 정답 키나 인코딩된 후보 이름 매핑은 포함하지 않습니다. 인라인 theme/application 자원은 네트워크 요청이 필요 없습니다. ZIP을 추출한 뒤 `file://`로 `index.html`을 엽니다. archive viewer 안에서 열지 않습니다. `assets/`는 `index.html` 옆에 유지합니다. 추출한 자원이 누락되거나 수정되면 변경된 자료에 평가를 재사용하지 말고 온전한 새 추출과 검증을 수행해야 합니다. builder는 준비된 입력을 검증하지만 추출 파일의 hash를 계속 계산하지는 않습니다.

상위 출력 디렉터리가 아니라 `comparison.zip`만 배포합니다. 공개가 승인될 때까지 키를 비공개로 유지합니다. `정답표 선택`은 명시적으로 선택한 키를 메모리로 읽고 study, version, versus revision, 모든 불투명 출력 식별 정보/fingerprint와 실패 상태를 확인합니다.
수동 선택 자체로 이름을 공개하거나 키 내용을 storage/export에 저장하지 않습니다.
`결과 보기`가 명시적인 공개 행동입니다. 부분 비교에서는 여전히 확인을 요청합니다. 이전 `revealed` flag는 이력이지 에이전트가 신원을 공개해도 된다는 허가가 아닙니다.

요청이나 실제 환경 근거로 split 전달을 선택합니다. media 크기 기준이나 지어낸 브라우저 실패 설명을 사용하지 않습니다. 연결된 HTML, metadata와 인코딩/pixel/의미상 단서를 포함한 전체 배포물을 검토합니다. 정확한 이름과 매핑이 비공개여도 스타일이 기법을 암시할 수 있습니다. packaging은 암호학적 익명성이나 HTML sanitization이 아닙니다.
