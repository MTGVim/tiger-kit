---
name: tk-blind-comparison
description: "[user/auto] 후보 이름을 가린 블라인드 비교·청취 갤러리를 요청하면 사용합니다. 취향·품질 후보 중 사람이 판단해야 할 때는 실행 전에 갤러리를 제안만 합니다. 단일 변경 QA, 장단점을 공개하는 설계 질문, 자동 지표 비교에는 사용하지 않습니다."
disable-model-invocation: false
argument-hint: "<candidate/item/output manifest or exported ratings>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

<a id="blind-comparison"></a>
# 블라인드 비교

<a id="shared-references"></a>
## 공통 참조

현재 설치된 소유 스킬에서 해당 분기의 조건에 따른 기준을 읽습니다. 소유 스킬이나 자원이 없거나 식별이 다르면 해당 행동을 중단하고 `tk-setup-skills`를 사용합니다. 기억, 다른 설치본이나 승인되지 않은 설치로 대신하지 않습니다. 참조를 읽어도 워크플로 실행이나 변경 권한은 부여되지 않습니다.

- 사용자 소유 결정·누락된 승인·미충족 선행 조건을 질문이나 질문 도구 입력으로 제시하기 직전에 [질문 라운드](../tk-questioning/references/questions.md)를 이번 작업에서 읽었는지 확인하고 누락했으면 먼저 읽습니다. 독립적인 결정과 승인은 각각 별도 질문으로 두며, 승인 선택지를 결정 질문에 섞지 않습니다.
- 사용자에게 완료 보고, 산출물 경로 인계 또는 여러 속성을 비교하는 채팅 답변을 전달하기 전에 [채팅 전달](../tk-writing/references/delivery.md)을 읽습니다. 해당 작업의 구체적인 출력 계약이 우선합니다.

기존 후보에 대한 사람의 비교를 담당하며 후보 생성이나 에이전트의 품질 판정을 담당하지 않습니다. 사용자가 블라인드 비교를 요청하면 만듭니다. 단지 주관적인 대안들이 있는 상황이라면 후보를 선택하거나 파일을 만들지 말고 블라인드 갤러리를 제안한 뒤 수락을 기다립니다. 단일 변경 점검은 `tk-qa-sheet`, 절충을 공개하는 질문은 `tk-grill`, 후보 생성은 `tk-prototype`, `tk-tts` 또는 관련 제작자가 담당합니다.

1. 이용 가능한 근거로 공통 비교 질문, 후보, 항목과 동등한 원본 입력을 확인합니다. 최소 두 후보가 필요하며 실패한 출력도 보존합니다.
   [manifest와 명령](references/manifest.md)을 읽습니다. 원본을 불변으로 유지하고 콘텐츠 revision을 기록합니다. 변경된 출력에는 새 평가가 필요하며 변경되지 않은 출력은 평가를 유지합니다.
   갤러리 점수 평가를 기본값으로 유지합니다. 명시적인 일대일 비교 요청에서는 [versus 비교](references/versus.md)를 읽습니다. 동률에서 단일 우승자를 강제하지 않습니다.
2. 쓰기 전에 산출물 경로 기준을 적용합니다. HTML, 표시용 사본과 별도 정답 키는 `.tigerkit/tmp/tk-blind-comparison/<run-id>/`에 두고, 반환된 평가와 요약은 `.tigerkit/evidence/tk-blind-comparison/<run-id>/`에 둡니다.
   명시적인 목적지를 존중합니다. [HTML 출력](../tk-writing/references/html-output.md)을 읽고 설치된 `tk-writing` theme 자원을 인라인으로 포함합니다. 문서 탐색 기능을 추가하지 않고 갤러리 interface를 유지합니다.
3. 신원 단서가 없는 표시용 사본을 준비합니다. 해당하는 [오디오](references/audio.md), [이미지와 UI 캡처](references/images.md), [텍스트](references/text.md) 또는 [동영상](references/video.md) 참조만 읽습니다. versus HTML은 manifest 미리보기 계약에 따라 신원 단서가 없는 자체 완결 사본을 준비합니다.
   manifest 계약에 따라 선택적인 중립 원본/mobile 링크와 공개 주석을 포함합니다.
   비교하는 특성을 지우지 않으면서 표면의 식별자와 메타데이터를 제거합니다.
   변환과 남은 단서를 눈에 보이게 기록합니다. 정규화 실패는 중립적인 사유가 있는 실패 카드로 남기고 진단 세부 사항은 정답 키에 비공개로 보존합니다.
4. 준비한 manifest로 패키지에 포함된 builder를 실행합니다. 후보를 추가/제거/재정렬할 때 같은 study ID와 이전 정답 키를 재사용하고 새 출력 디렉터리를 만듭니다.
   불투명하고 안정적인 candidate ID, item ID와 콘텐츠 fingerprint를 보존합니다. 항목별 seed 기반 섞기와 후보 이름과 겹치지 않는 중립 레이블을 사용합니다. 후보 신원이 파일명, DOM ID, 접근성 이름, 기본 텍스트나 정렬에 드러나서는 안 됩니다.
   요청이 있거나 실제 전송/열기 환경이 정당화할 때 split 전달을 선택합니다. 지어낸 크기 기준이나 검증되지 않은 브라우저 실패 진단을 근거로 삼지 않습니다. [manifest와 명령](references/manifest.md)의 split 계약을 읽습니다. 상위 출력 디렉터리가 아닌 `comparison.zip`만 배포합니다. 별도 정답 키는 비공개로 유지합니다. 기본 single-versus 자기 평가에는 인코딩된 최소 키를 포함합니다. separate-key single과 split 전달에는 일치하는 선택된 키가 필요합니다. 두 versus 키 경로는 같은 validator와 명시적인 공개 절차를 사용합니다. manifest 계약을 읽습니다. 기존 single gallery는 동작을 유지합니다.
   명시적인 공개 toggle과 선택한 전달 방식의 정답 키 경계를 유지합니다. 오프라인 블라인드 처리는 우연한 단서를 막지만 소스 검토를 막지는 않습니다. 암호학적 보안이나 시험 보안을 주장하지 않습니다.
   비교 주제, 항목 제목, 공통 원문과 평가 안내를 현재 항목의 sticky 맥락 안에 보이게 유지합니다. 긴 맥락의 높이를 제한해 점수 입력에 계속 접근할 수 있게 합니다.
5. 저장한 로컬 HTML을 `tk-browser-verify`로 검증합니다. desktop/mobile과 두 theme, media 디코딩, 원본 크기/추가 링크, escape된 주석, 모든 실패 카드, keyboard 제어와 선택한 방식의 제어를 확인합니다. embedded 원클릭 versus 결과, separate-key 안내/파일 선택, 키 검증 실패와 재생으로 도출한 전체 결과 표를 검증합니다. 갤러리 점검에는 native 1-5 점수, 메모와 선택적인 선호 후보, reload, 후보 추가, JSON import/export, 평가 복사와 clipboard 거부, 부분 공개 확인/취소, 공개 후에만 보이는 평균과 storage 거부를 포함합니다.
   복사는 export와 같은 blind-key payload를 사용합니다. clipboard 접근이 실패하면 평가를 유지하고 파일 export를 제공합니다.
   versus에서는 round/VS/카드 선택 배치, 긴 이미지의 내부 scroll, live HTML 공개/단계 제어와 현재 쌍만 유지하는 iframe 정리, 홀수 부전승, 반복적인 양쪽 진출, 후반 round의 공동 우승 확인/취소, 완료 후 undo와 항목 간 재생도 검증합니다.
   hosting 없이 `file://`로 엽니다. single 전달은 주요 media를 포함합니다. split 전달은 ZIP을 모든 중립 자원과 함께 추출한 뒤 외부 요청이나 누락 링크 없이 작동해야 합니다. 로컬 파일의 브라우저 `localStorage`는 환경마다 다릅니다. 저장 실패를 표시하고 JSON 백업/import를 제공합니다. 파일 이동이나 다른 브라우저 사용 시 이전 export를 import해야 할 수 있습니다. 실행하지 않은 점검은 정직하게 보고합니다.
6. 로컬 HTML과 정답 키 경로, revision/개수, 변환, 실제 점검과 남은 사람 평가를 반환합니다. 명시적인 요청이 있을 때만 발행합니다. 실제 평가를 기다리고 점수를 지어내지 않습니다. 복사한 JSON이나 JSON export가 도착하면 [결과](references/results.md)를 읽고, 일치하는 키에 대조해 검증하며, 방식에 맞는 개수/평균 또는 선택 transcript와 항목 표를 집계하고 평가자 수, 누락 점수, 실패와 표본 한계를 명시합니다. 주관적 평균을 통계적 증명으로 취급하지 않으면서 이용 가능한 객관적 지표를 낮은 점수 항목과 비교합니다.

서버, 공통 데이터베이스, 실시간 다중 평가자 수집, 통계 검정, 자동 우승자, 소스 변경, 모델 설치나 합성을 수행하지 않습니다. 기존 오디오/동영상 비교는 새로운 TTS를 허용하지 않습니다. 사용자가 별도로 새 narration을 요청했고 선택이 미정인 경우에만 TTS에 관해 묻습니다.

<a id="artifact-paths"></a>
## 산출물 경로

승인된 산출물 쓰기, checkout/전송/제외 설정 또는 임시 입력 소비 전에 [산출물 경로](../tk-artifacts/references/artifact-paths.md)를 읽습니다. 저장소 임시 자원에는 안전한 소유 경로로서 symlink가 아닌 경로와 입증된 Git 제외를 사용합니다. 점검에 실패하면 해당 파일 분기를 중단합니다. 명시적인 최종 목적지와 소유자별 기본값을 보존합니다. 미리 채워진 입력은 완성된 입력이 아닙니다.
정리는 기록된 literal로서 해석이 완료된 실행 소유 절대 경로만 대상으로 하며 cwd 상대 경로나 glob은 사용하지 않습니다.

갤러리 builder가 현재 원본에서 studio를 생성하고 split ZIP에 포함하므로 이를 다시 중복 주입하지 않습니다. 기본 링크는 single의 `gallery.studio.html`, split의 `index.studio.html`이며 정답 키를 별도 보존합니다. HTML을 사람에게 전달할 때는 현재 설치된 `tk-writing`의 [공통 피드백 후처리](../tk-writing/references/feedback-studio.md)를 적용하고 studio를 기본 열람본으로 안내합니다. 원본·기존 전용 인터페이스·검증 의무를 유지합니다.
