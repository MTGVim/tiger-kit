<a id="video-assembly"></a>
# 영상 조립

- [입력과 타이밍](#inputs-and-timing)
- [연속 렌더링 영상](#continuous-rendered-video)
- [선택적 자막, 콜아웃과 확대](#optional-captions-callouts-and-zoom)
- [품질과 복구](#quality-and-recovery)

이미 설치된 ffmpeg와 ffprobe로 이 패키지의 `scripts/build_movie.py`를 사용합니다. 도구를 자동으로 설치하지 않습니다. 안전한 입력/출력 규칙은 패키지 위치와 독립적으로 적용됩니다.

<a id="inputs-and-timing"></a>
## 입력과 타이밍

절대 경로의 일반 nonsymlink JSON manifest와 그 실행 소유 디렉터리 안의 비어 있지 않은 PNG/JPEG frame을 사용합니다. 공통 캡처 입력은 인계가 해당 위치의 출력을 허용할 때 생성 검증 담당자의 실행 디렉터리에 그대로 둘 수 있습니다. 출처를 결합할 때는 승인된 frame 바이트를 하나의 영상 실행으로 복사하고 인계에 원래 경로/해시를 보존합니다. 상태를 변경하는 흐름을 다시 캡처하지 않습니다.

관찰 캡처는 기존 schema와 실제 경과 시간을 유지합니다.

```json
{"mode":"evidence","frames":[{"path":"/absolute/run/frame-0.png","timestamp_ms":0},{"path":"/absolute/run/frame-1.png","timestamp_ms":100}],"end_ms":1000,"captions":[{"start_ms":0,"end_ms":1000,"text":"Observed result"}]}
```

이벤트 기반 screencast에서 구간을 골라 이어 붙일 때는 원본 캡처와 원본 시각을 보존하고,
다음 순서로 편집용 타임라인을 만듭니다.

1. 원본의 반열린 구간 `[시작, 끝)`마다 시작 시각 이전 또는 같은 시각에 마지막으로 관찰한
   프레임을 찾아, 그 구간 출력 시작점에 한 번 배치합니다. 당시 화면이 입증되지 않으면 뒤에 온
   프레임을 앞당겨 채우지 말고 그 구간을 보류합니다. 원본 프레임 자체의 관찰 시각은 바꾸지 않습니다.
2. 구간 안의 나머지 프레임에는 `출력 누적 길이 + (원본 시각 - 구간 시작)`을 적용합니다.
   구간 끝에 정확히 걸린 프레임은 다음 구간이 포함하는 경우 그 구간에서 처리합니다.
3. 첫 구간 시작 프레임은 `0ms`에 두고 밀리초 변환 뒤 같은 출력 시각은 하나로 합칩니다.
   구간 경계에서는 뒤 구간의 시작 상태를 유지합니다. 이후 모든 시각이 엄격하게 증가하는지
   확인하고, `end_ms`는 실제로 선택한 구간 길이의 합이며 마지막 프레임보다 뒤에 있어야 합니다.
4. 안정된 화면에는 새 이벤트가 없어도 마지막으로 입증한 프레임을 해당 구간 끝까지 유지합니다.
   원본 종료를 넘기거나 알 수 없는 시간을 채우지 않습니다. 원본 구간·프레임 경로/해시와 출력
   구간의 대응은 기존 실행 근거에 남깁니다. 편집된 영상임을 밝히고, 압축·접합한 출력 시각을
   연속된 실제 지연·성능 측정이나 독립 인수 근거로 사용하지 않습니다.

원본 캡처 manifest를 덮어쓰지 않고 새 실행 소유 manifest를 조립기에 전달합니다. 중복 시각이나
늦은 첫 프레임을 조립기가 자동 보정한다고 가정하지 않습니다.

MP4는 실제 캡처 메타데이터의 선택적 양수 숫자 `source_fps`를 사용하며 최대 30fps로 제한합니다. 값이 없으면 마지막 hold를 제외한 인접 frame timestamp 간격의 중앙값으로 주기를 추정합니다. `fps_source: timestamps`와 event-driven/idle 캡처의 불확실성을 보고합니다. Frame이 3개 미만이면 주기를 확립할 수 없으므로 경고와 함께 10fps로 대체합니다. GIF와 `explainer` 기본값은 10fps입니다. 정지 이미지의 hold는 캡처 rate 측정값이 아닙니다. `--fps <number>`는 두 format 모두에서 최대 30의 양수 출력 rate를 명시적으로 선택하며 원본 timestamp, 장면 hold나 오디오 offset을 바꾸지 않습니다. 결과는 측정한 인코딩 `fps`, `selected_fps`, `fps_source`와 `encoded_duration_ms`를 manifest 길이와 구별합니다. 분수 rate는 분수로 유지합니다. 인코딩은 최종 끝점을 frame 간격으로 양자화합니다. 150ms와 한 frame 중 더 큰 값 이하의 허용 오차로 길이/디코딩 점검을 유지합니다. 비공개로 생성한 concat 목록은 마이크로초 이미지 time base를 사용하여 선택 rate filter가 실행되기 전에 25fps 이미지 기본값이 40ms 미만 캡처 간격을 버리지 못하게 합니다.

브라우저 MP4의 캡처 목표는 별도 선택이 없으면 30fps로 계획하되, 요청한 목표와 실제 움직임 구간의
고유 프레임 빈도, 인코딩 FPS를 구분합니다. 목표값을 `source_fps`에 쓰지 않습니다. 필요하면
선택한 출력 rate를 `--fps`로 전달하며, 출력 FPS를 올려도 누락된 실제 상태나 부드러운 원본 움직임이
복구되었다고 주장하지 않습니다. GIF·explainer의 10fps, MP4 캡처/정지 이미지의 30fps 상한과
원본 timestamp 기반 자동 추정은 유지합니다.

정지 이미지 설명에는 명시적 hold를 사용합니다. Hold가 없으면 3000ms, 자막 글자당 125ms와 측정 내레이션에 800ms를 더한 값 중 최댓값을 사용합니다. 이 읽기 시간 경험칙은 독자 관점의 검사가 필요합니다. 명시적으로 선택한 hold는 여전히 우선합니다.

```json
{"mode":"explainer","frames":[{"path":"/absolute/run/diagram.png","source_kind":"rendered","source_in_picture":true,"caption":"The request enters the queue","hold_ms":3000},{"path":"/absolute/run/actual-state.png","source_kind":"capture","caption":"Observed result","hold_ms":4000}]}
```

Render된 카드의 `source_in_picture: true`는 이미지에 이미 존재하며 검사된 출처 tag를 선언하고 자막 prefix를 생략합니다. 이 선언은 frame을 캡처로 표시하지 않습니다. 값이 없으면 `source_label`로 독자 언어의 비어 있지 않은 label을 제공합니다. 한국어 기본값은 `렌더링 장면`입니다. 이미지에 출처가 나타나더라도 사용자가 `caption_style: none`을 명시적으로 선택하지 않았다면 빈 내레이션 자막은 여전히 자막 범위 점검에 실패합니다. 자막이 비활성화되면 모든 render 카드 안에 출처 tag를 유지합니다.

관찰된 장면별 내레이션은 `evidence` manifest에 `scenes: [{"start_ms": 0, "audio_path": "/absolute/run/scene.wav"}]`를 추가합니다. 시작점은 `end_ms` 안의 실제 장면 경계이며 엄격히 증가해야 합니다. 측정한 클립은 다음 장면/종료 전까지 들어맞아야 합니다. 초기 간격과 무음 장면을 보존합니다. 개별 evidence frame에 장면 오디오를 할당하지 않습니다. 내레이션 속도에 맞춘 재캡처는 캡처 담당자에게 속하며 승인된 비변경 시나리오로 제한됩니다.

`explainer`의 장면별 오디오는 해당 frame에 `audio_path`를 추가합니다. 도우미는 실제 길이를 측정하고 위 읽기/내레이션 규칙으로 기본 hold를 정하며 각 장면을 hold까지 채우고 클립을 순서대로 연결합니다. 오디오보다 짧은 명시적 hold는 거부합니다. `narration_requested: true`는 선택한 내레이션이 없거나 무음일 때 실패 미디어 결과를 유지합니다. 내레이션을 선택하지 않았거나 자막 전용 fallback을 수용한 경우에만 false를 사용합니다. 장면 오디오와 별도의 전체 track `--audio` 입력을 결합하지 않습니다. 글자 수로 길이를 추측하지 않습니다. 수용된 현재 장면 텍스트에만 오디오를 연결하고 자막이 켜져 있으면 이를 모두 다루도록 합니다. 내레이션 실패는 어떤 경우에도 관찰 대기 시간을 만들어 낼 권한을 주지 않습니다. `evidence`는 `timing: observed`를 반환하고 `explainer`는 `timing: presentation`을 반환합니다. 어느 쪽도 타이밍 판정이 아닙니다.

Frame, 장면 WAV와 출력은 manifest 디렉터리 안에 둡니다. 출력은 새 경로여야 합니다. `python3 <loaded-package>/scripts/build_movie.py --manifest <json> --output <owned.mp4-or.gif>`를 실행합니다. 선택적 `--audio <wav>`는 별도로 준비한 track을 받습니다. Assembler는 엔진을 import하지 않습니다. `--ffmpeg <path>`는 `TIGERKIT_FFMPEG`와 자동 탐색보다 우선합니다. 먼저 PATH를 확인하고 자막이 없으며 override를 선택하지 않았다면 `brew --prefix ffmpeg-full`로 설치된 Homebrew `ffmpeg-full` keg를 확인합니다. 패키지를 설치하거나 PATH를 바꾸지 않습니다. Receipt는 `ffmpeg_path`와 `ffprobe_path`를 보고합니다. 일치하지 않거나 너무 긴 선택적 track은 경고와 함께 생략합니다. 선택했지만 누락된 내레이션의 한계는 유지합니다. 출력 및 screenshot manifest와 독립적으로 원본 소스를 보존합니다.

<a id="continuous-rendered-video"></a>
## 연속 렌더링 영상

선택한 [Manim 경로](manim.md) 이후에는 PNG frame을 추출하는 대신 이 실행 안의 일반 MP4를 사용합니다. 이 경로는 완전한 고정 frame rate render 하나를 소비합니다. 여러 beat는 그 안에서 구성합니다. Frame/영상 혼합 manifest와 직접 작성한 `end_ms`는 거부합니다. 가변적이거나 모호한 rate에는 추측이 아니라 명시적으로 선택한 변환이 필요합니다. 이는 render된 animation이며 관찰된 애플리케이션 타이밍이 아닙니다.

```json
{"mode":"animation","video_path":"/absolute/run/render.mp4","caption_delivery":"soft","captions":[{"start_ms":0,"end_ms":2000,"text":"Version 2 and DOM"}]}
```

기본 MP4 FPS는 분수 rate와 30 초과 rate를 포함하여 stream에서 가져옵니다. 길이/해상도를 보존합니다. H.264/yuv420p는 홀수 치수를 짝수 픽셀로 채우고 이를 보고합니다. 명시적 `--fps` 변환과 GIF의 10fps/오디오 생략도 보고합니다. 영상은 선택한 CRF로 재인코딩합니다. 바이트 동일/무손실 출력이 아닙니다. Receipt는 `source_video`, 실제 출력 기하/rate/길이와 render 타이밍을 구별합니다.

내장 오디오는 stream copy를 사용하여 몰래 downmix/교체하지 않고 channel을 유지합니다. 추가 `scenes` 내레이션이나 `--audio`는 충돌하여 실패합니다. 오디오 출처 하나를 선택합니다. 내장 오디오가 없으면 측정 장면 offset이나 전체 track을 재사용합니다. 너무 길거나 사용할 수 없는 animation 오디오는 몰래 생략하지 않고 실패합니다. 선택한 내레이션이 무음이거나 자막 범위가 부족하면 계속 실패입니다. TTS 엔진은 import하지 않습니다.

직접 작성하는 설명 MP4는 별도 선택이 없으면 `caption_delivery: hard`를 사용합니다. 저수준 조립기의 animation 대체값 `soft`와 구별하여 manifest에 명시합니다. 명시적 `none | soft | hard` 선택을 보존하고 frame 경로는 기존 기본값을 유지합니다. `caption_style: none`이나 delivery `none`은 track/sidecar를 비활성화하며 내레이션 guard를 비활성화하지 않습니다. 활성화된 delivery와 style `none`을 결합하지 않습니다. Animation 자막은 순서가 있고 겹치지 않으며 측정 길이 안에 있어야 합니다. 화면 텍스트는 TTS 철자가 아니라 원래 표기를 유지합니다.

Soft MP4에는 강제 표시되지 않는 `mov_text` track과 SRT/WebVTT sidecar가 있으며 libass가 필요하지 않고 픽셀에 텍스트를 입히지 않습니다. 선택한 sidecar를 영상과 함께 전달합니다. Muxer/player는 track을 기본값으로 표시할 수 있습니다. 처음에 숨겨진다고 약속하지 말고 측정한 `subtitle_default`를 보고합니다. 브라우저는 일반적으로 내장 MP4 텍스트만이 아니라 same-origin WebVTT `<track>`이 필요합니다. 선택한 player에서 cue 로딩과 실제 on/off control을 검증합니다. File-origin 규칙이 WebVTT를 막으면 소유권이 확인된 로컬 HTTP origin을 사용합니다. 그렇지 않으면 해당 player를 미지원으로 보고하고 별도 파일을 보존합니다. 범용 player UI는 추가하지 않습니다. 명시적 hard delivery에는 선택한 style과 기존 libass/fallback 계약을 사용합니다. 지원 누락은 계속 blocked입니다. 서로 다른 sidecar, 영상과 contact sheet를 덮어쓰지 않습니다.

명시적 style이 없는 animation hard 자막은 `overlay-rounded`를 사용하고 원본 canvas를 유지합니다. Hard delivery는 letterbox, 추가 band나 종횡비 변경을 허용하지 않습니다. 사용자가 해당 배치를 별도로 요청한 경우에만 `band`를 선택합니다. Overlay가 충돌하면 몰래 band로 전환하지 말고 자막을 줄이거나 나누거나 diagram의 안전 영역을 다시 작성합니다. Animation에 명시적인 hard `band`를 사용할 때는 전체 원본 사각형을 보존하고 최대 3줄과 여유 공간을 담을 크기의 검정 자막 전용 band를 추가합니다. 너비, FPS와 타이밍은 바꾸지 않습니다. 추가된 출력 높이를 보고합니다. 특히 가장 긴 cue와 전환을 포함한 모든 cue를 검사합니다. 글리프가 band를 벗어나면 작성한 텍스트를 줄이거나 나누거나 `--caption-size`를 조정합니다. 읽기 쉬운 단어 경계 줄바꿈을 작성합니다. SRT/WebVTT는 이를 유지하되 cue를 나누게 될 빈 줄은 제거합니다. 기하 receipt는 겹침이 없음을 입증하지 않습니다. Soft/off animation은 원래 치수를 유지합니다. 이는 기본 delivery나 사용자가 선택한 style을 바꾸지 않습니다.

<a id="optional-captions-callouts-and-zoom"></a>
## 선택적 자막, 콜아웃과 확대

제작 전에 [미디어 선택](../../tk-writing/references/media-preferences.md)으로 이 필드를 확정합니다. 저장된 선택을 재사용하고 기본값 저장 승인은 정확한 값 확정 뒤 별도 질문으로 처리합니다. 선택한 표현 처리에만 사용합니다. 관찰 캡처·카드 대체값은 기존 `band`와 변환하지 않은 frame을 유지하고, Manim hard 자막의 대체값은 `overlay-rounded`입니다. 현재 명시적·저장된 style은 대체값보다 우선합니다. 평가자 한 명의 변형 선호는 해당 제작자의 선택을 뒷받침하며 보편적 기본값이나 학습 개선의 근거가 아닙니다.

```json
{
  "caption_style": "overlay-rounded",
  "callouts": [{"start_ms": 1000, "end_ms": 4000, "x": 620, "y": 340, "text": "Revenue, margin and orders", "size": 24}],
  "highlights": [{"start_ms": 1000, "end_ms": 4000, "rects": [{"x": 120, "y": 320, "w": 420, "h": 120}], "zoom": true, "margin": 32, "max_scale": 2}]
}
```

모든 좌표는 짝수 padding, zoom이나 자막 band 적용 전의 동일 크기 원본 캡처 frame 안의 픽셀입니다. 기록기의 viewport `cue_targets`는 실제 screenshot 배율, crop 원점과 frame 치수로 변환합니다. 이 매핑과 캡처 전용 출처를 보존합니다. 관찰한 beat 시간을 재사용하고 scroll/레이아웃 변경 후 좌표를 갱신합니다. 기하 구조가 바뀌면 구간을 나눕니다. 오래된 사각형은 움직이는 대상을 보호할 수 없습니다. `rects`는 이미 캡처한 강조 영역을 설명합니다. 조립은 UI 상태를 만들어 내거나 사라짐 badge를 그리지 않습니다. 필요한 이미지 내 출처 tag를 보호 사각형에 포함하거나 자막에 출처 label을 유지합니다.

- `caption_style`: `none`(사용자의 명시적 선택: hard/soft 자막, band와 SRT 없음), `band`(기본값), `overlay`(모서리가 각진 50% 검정 libass 상자) 또는 `overlay-rounded`(50% 검정 ASS vector 상자와 흰 텍스트)입니다. Overlay는 기존 짝수 padding을 제외하고 원본 높이를 보존합니다. 기본 글자 크기는 그 높이의 5%이며 `--caption-size`도 계속 적용됩니다. 상자는 하단에서 6% 위에 놓입니다. Style은 SRT sidecar를 변경하지 않습니다. `none`일 때도 선택한 내레이션에는 `narration_requested: true`를 유지합니다. 자막 범위만 건너뛰며 누락/무음 오디오는 여전히 실패합니다. Receipt는 `subtitles: none`, `subtitles_reason: user-disabled`, `captions_path: null`을 반환하며 sidecar는 없습니다. 기본 hold에서 자막 전용 읽기 시간은 제외하지만 측정 오디오와 여유 공간 및 명시적 hold는 계속 적용됩니다. 작성한 자막 텍스트는 원본에 남을 수 있으나 render되지 않습니다. Callout은 별도로 선택된 상태를 유지하고 여전히 libass가 필요합니다. 자막 끄기는 선택한 callout이나 그 점검을 비활성화하지 않습니다.
- `callouts`: 원본 frame의 왼쪽 위 `x/y`, 일반 `text`, 관찰 구간과 선택적 명목 `size`(기본값은 원본 높이의 2.5%, 최소 12px)입니다. 얇은 테두리, 왼쪽 강조선, 어두운 텍스트와 옅은 그림자가 있는 흰 카드를 render합니다. 실제 libass 글리프 경계로 줄바꿈과 padding을 결정하며 추가 이미지 library는 필요하지 않습니다. 너무 큰 카드, 누락 글리프, 겹치는 카드나 활성 대상을 가리는 카드는 실패하며 작성 수정이 필요합니다.
- `highlights`: 순서가 있고 겹치지 않는 구간입니다. 동시 group은 하나의 `rects` 목록에 결합합니다. `zoom` 기본값은 true이며 false는 확대하지 않고 대상을 자막으로부터 보호합니다. 모든 사각형과 구간에 겹치는 모든 callout의 합집합에 `margin`(기본값 32px, 정수 crop을 위해 내부적으로 최소 2px)을 더하고 출력 종횡비에 맞춘 뒤 원본 범위로 제한합니다. 배율은 영역 맞춤과 `max_scale`(기본값 2, 허용 1-10)로 제한됩니다. 고정 크기 `zoompan`은 입력 frame 번호/출력 fps를 사용하며 양 끝에 500ms smoothstep을 적용합니다. 1초 미만 구간은 각 전환에 길이의 절반을 사용합니다. 원본 타이밍을 늘이지 않습니다. 정수 crop에도 약간의 움직임 떨림이 생길 수 있습니다. 원점을 범위 제한하고 올림 처리한 RGB crop은 최종 4:2:0 인코딩 전에 원본 가장자리에 맞닿은 테두리를 보존합니다.

Filter 순서는 fps/짝수 padding, callout, 고정 canvas zoom, 선택적 band, 자막 순입니다. 카드는 UI와 함께 확대되지만 자막 크기는 유지됩니다. 가변 크기 `scale` 뒤의 `crop`은 filter를 재초기화하고 시간/frame counter를 재설정할 수 있습니다. Animation zoom에 사용하지 않습니다.

각 overlay 자막은 실제 ASS centisecond 경계(요청 시간과 함께 보고됨)를 사용하여 전체 구간과 zoom 전환에 걸쳐 보호 대상/카드 기하 구조를 점검합니다. 아래 상자가 겹치면 위 위치를 사용하고 `caption moved to top to keep highlights visible: <time>`을 기록합니다. 두 위치 모두 충돌하면 실패 처리하고 `band`를 사용하거나 명확한 안전 영역으로 다시 캡처합니다. 반환된 `presentation` 기하 정보를 읽고 디코딩 frame을 검사합니다. 기하 점검은 cue 사실, 글리프 가독성이나 미관을 입증하지 못합니다. 각 callout의 중간 frame과 각 zoom의 전환/중간 frame을 확인합니다. 실제 상자 padding을 비교합니다(자막 좌우 차이는 글자 크기의 최대 30%, 카드 상하 차이는 최대 20%). 다른 style을 위해 원본 캡처 frame을 보존합니다. libass가 없으면 필수 텍스트 효과와 그에 의존하는 zoom을 차단합니다. 의존성 설치나 완료 주장 권한을 부여하지 않습니다.

<a id="quality-and-recovery"></a>
## 품질과 복구

MP4는 `libx264`, `yuv420p`와 명시적 CRF 18을 사용합니다. `--crf <integer>`는 MP4에만 0-51을 선택합니다. 낮은 값은 더 많은 세부를 보존하지만 크기가 커질 수 있습니다. GIF는 명시적 `--crf`를 거부합니다. 동일 크기 원본 frame에는 짝수 치수 padding과 기본 evidence 자막 band만 적용하여 치수를 유지합니다(선택한 overlay style은 band를 생략합니다). 작성이나 캡처 중 해상도 변경을 피합니다. Receipt는 `encoder`, 요청한 `crf`, 인코딩된 `width`/`height`와 `pixel_format`을 보고합니다. CRF는 encoder 설정이며 측정한 시각 품질 점수나 무손실 주장이 아닙니다. 4:2:0 색 변환은 CRF 0에서도 가느다란 유색 텍스트를 흐리게 할 수 있습니다. 실제 편집본을 검사합니다.

도우미는 실제 codec, 길이와 전체 디코딩을 확인하고 미디어 품질을 기존 애플리케이션 필드 `verification_status: not-assessed`와 별도로 보고합니다. 사실 내용을 판단하거나 사람이 내레이션을 들었음을 입증할 수는 없습니다. Contact sheet와 실제 frame을 검사합니다. 반복 frame 경고는 `evidence`에 관한 것입니다. `explainer`에서 정지 이미지를 유지하는 것은 의도적입니다.

Hard 자막에는 실제 `subtitles` filter를 사전 점검하고 이름이 지정된 `filename` 옵션을 사용합니다. Filter가 없으면 exit 2가 `media_status: blocked`, 선행 조건 `ffmpeg-subtitles-filter`, 일치하는 SRT와 디코딩 가능한 영상을 반환합니다. MP4에는 soft 자막 track도 포함되고 GIF에는 sidecar만 있습니다. 이는 복구 가능한 출력이며 화면에 입힌 자막 성공이 아닙니다. Blocked 결과를 반환하거나 우회책을 고려하기 전에 정확한 누락 capability로 `tk-wizard` 설치 안내 질문을 제시합니다. Frame 합성 자막을 구현하지 않습니다. ffmpeg-full 같은 플랫폼별 패키지를 제안하기 전에 기존 패키지/PATH 충돌을 검사합니다.

UI 녹화(`evidence`)의 기본 hard 자막은 검정 하단 band(`pad`)를 추가하여 전체 UI를 보존합니다. 기본 명목 글자 크기는 최종 출력 높이의 5%입니다. `--caption-size <px>`로 재정의합니다(양수이며 최대 원본 높이의 절반). Band는 글자 높이 2개를 담으며 최소 48px입니다. 도우미는 크기와 가운데 정렬 세로 여백을 libass의 288-unit SRT 좌표계로 변환합니다. Receipt는 명목 `caption_size_px`와 `caption_band_px`를 노출합니다. 실제 글리프 경계는 설치 font에 따라 달라집니다. Soft 자막 style은 player가 계속 담당합니다. 디코딩 frame에서 글리프 지원, 줄바꿈과 band 넘침을 검사하고 필요하면 자막을 줄이거나 나눕니다. Render된 explainer 카드는 작성한 레이아웃을 유지합니다.

인코딩 실패는 exit 1과 범위가 제한되고 민감 정보가 제거된 진단을 반환하며 입력과 이전 출력을 보존합니다. 준비된 출력은 exit 0을 반환합니다. 무관한 파일을 덮어쓰거나 용량이 큰 GIF를 잃지 않습니다. 5MiB는 목표이며 눈에 보이는 경고를 제공합니다. 미리 만들어 검사한 GIF는 `tk-pr-media`를 통해 이미지로 업로드합니다. Extension 측 `--gif` 조립에는 별도로 선택한 발행이 필요합니다.

<a id="caption-splitting"></a>
## 긴 자막의 의미 단위 분할

한 줄 너비를 넘는 cue만 분할 대상으로 삼습니다. `caption_lines_estimate > 1` 경고는
전각·반각 글자 폭, 선택 글자 크기와 원본 너비의 90%를 이용한 근사치이며 실제 폰트 측정이 아닙니다.
렌더링한 프레임에서 최종 확인합니다. 자동 분할하지 않습니다.
한국어에서는 절 어미 뒤 쉼표(`-고,`, `-면,`, `-지만,`, `-서,`, `-는데,`), 주제어·주어 조사 뒤,
나머지 띄어쓰기 순으로 검토합니다. 나열 쉼표와 관형어·명사 사이(`그 사람`, `약 10분`, `다른 방법`)는
피하고 8자 미만의 짧은 조각은 다른 경계를 고르거나 문장을 다시 씁니다.
측정된 문장 오디오 구간에서 조각 사이 50ms를 뺀 나머지를 글자 수 비율로 배분하되,
실제 발화 경계가 있으면 이를 우선합니다. 원래 cue의 시작·끝을 넘기거나 다음 cue와 겹치지 않게 하고
읽기 시간과 발화 정렬을 다시 검사합니다. 글자 수로 전체 오디오 길이를 추정하지 않습니다.

<a id="feedback-player"></a>
## 피드백 플레이어

MP4와 SRT sidecar를 만든 뒤 다음 명령으로 영상 옆의 `<stem>.feedback.html`을 만듭니다.

```sh
python3 <loaded-package>/scripts/make_feedback_player.py --video <out.mp4> --captions <out.srt>
```

기존 출력은 덮어쓰지 않고 새 이름을 선택합니다. HTML과 MP4는 함께 전달하며 영상은 상대 경로로만
참조하고 내장하거나 업로드하지 않습니다. GIF·자막 없음·sidecar 없는 soft 자막은 생략합니다.
생성 실패는 사유와 함께 보고하며 완성 영상 전달은 계속합니다.
플레이어는 대본 클릭 이동·현재 cue 강조·대본 상자 안에서만 따라가기, 현재 자막과 배속(0.75×–2×),
시스템/라이트/다크 테마와 좁은 화면의 1열 배치를 제공합니다. 영상 로드 실패 시 로컬 파일 선택을 제공합니다.
입력 시작(focus 또는 첫 input)의 시각을 기록하고 기본적으로 일시정지합니다. 입력 중 seek는 기록 시각을 바꾸지 않습니다. 내용이 있고 현재 위치와 기록 시각이 1초 이상 다르면 `지금 위치(mm:ss)로 바꾸기` 버튼을 보여 줍니다. 버튼은 기록 시각과 자막만 바꾸고 쓴 내용과 입력 커서는 유지하며 툴팁으로 동작을 설명합니다.
저장 버튼 또는 Ctrl/⌘+Enter로 누적하며 IME 조합 중에는 확정 뒤 저장합니다. 빈 내용은 거부합니다.
목록은 시각순으로 선택·이동·삭제할 수 있고 선택 항목을 Markdown으로 복사합니다. 모두 지우기는 확인을 거칩니다.
`localStorage` 키는 `video-feedback:<영상 경로>:<cue 해시 12자>`이며 저장 불가 시 복사를 안내하고 계속 동작합니다.
대본이 달라지면 별도 목록이 됩니다. 외부 요청·CDN·폰트 다운로드는 없습니다.
입력 밖 K/스페이스는 재생·정지, J/L은 5초 이동, </>는 배속, N은 입력, Esc는 입력 종료입니다.

복사 결과는 제목·영상 파일명·건수와 `- [00:12] 피드백` 및 그 시각 자막을 포함합니다.
피드백 본문의 줄바꿈은 ` / `로 합칩니다. 붙여 넣은 피드백은 시각으로 beat을 찾고 같은 지적이
다른 장면에도 해당하는지 원고 전체를 검색해 함께 고칩니다. 실제 OS 한글 입력기·클립보드와 브라우저별
동작을 검사하지 않았다면 합성 이벤트나 문자열 확인을 실제 입력·복사 검증으로 보고하지 않습니다.

<a id="narrated-output-bundle"></a>
## 설명 MP4 전달 묶음

내레이션이 있는 직접 작성 설명은 hard 자막 MP4, 자막 없는 MP4, SRT를 기본으로 전달합니다. 내레이션이 없으면 hard MP4와 SRT를 전달하며, 명시적 soft/off 요청이 우선합니다. 같은 렌더·오디오·타임라인에서 별도 출력 이름과 manifest 사본으로 조립하고 각 receipt의 실제 경로와 측정 길이를 대조합니다. 자막 없는 사본은 `caption_box_color`와 `caption_box_alpha`를 제거하고 `caption_delivery: none`과 `caption_style: none`으로 만들되 `narration_requested`와 `tts_receipts` 및 화면 고지는 보존합니다. 피드백 플레이어에는 자막 없는 MP4와 자막본의 SRT를 함께 넘깁니다.
macOS에서는 먼저 설치된 FFmpeg의 `subtitles` 필터를 확인합니다. Homebrew 기본 빌드에 없다면 libass를 포함한 `ffmpeg-full`의 실제 실행 파일을 `--ffmpeg`로 지정할 수 있습니다. 새 설치는 별도 권한을 따릅니다. 반환값 `subtitles: hard`, `media_status: ready`와 경고를 확인한 뒤 프레임에서 자막을 확인합니다. 현재 receipt에는 `caption_delivery` 대신 `subtitles`가 실제 결과 필드입니다.

<a id="tts-disclosure-gate"></a>
## TTS 고지 게이트

TTS를 사용한 모든 합성 receipt를 실행 소유 폴더로 복사하여 `tts_receipts: ["/absolute/run/tts.json"]`에 전달합니다. 하나라도 `disclosure_required: true`이면 그 receipt의 `disclosure_notice`가 전체 영상에 보이도록 작성합니다. 이는 라이선스가 표시 위치·전 구간을 지정했다는 뜻이 아니라 이 워크플로의 누락 방지 계약입니다. 조립기는 실제로 그리는 callout, hard 자막, 또는 `disclosure_scene: [{start_ms, end_ms, text}]` 선언만 인정합니다. soft/off 자막과 지원 부재로 그리지 못하는 효과는 고지가 아닙니다. 첫·끝의 최대 1초만 허용하며 중간 공백은 허용하지 않습니다. 요구 문구가 빠지거나 잘못된 receipt·구간이면 인코딩 전에 실패합니다.
장면이 직접 그리면 조립기는 픽셀을 입증하지 못하므로 반환한 `disclosure.notices[].human_action`에 따라 첫·중간·끝 프레임을 직접 확인합니다. 기본 배치는 자막과 떨어진 하단 가는 경계선 아래의 읽을 수 있는 작은 한 줄이며 처음부터 끝까지 유지합니다. 본문보다 낮은 대비를 쓰되 읽을 수 없어서는 안 됩니다. 별도 자동 콜아웃 삽입으로 위치·겹침 점검을 우회하지 않습니다. SRT와 피드백 플레이어에 고지 반복을 강제하지 않습니다.

<a id="feedback-revision-loop"></a>
## 피드백을 반영하는 새 판

새 판마다 이전 장면 코드·원고·측정 타이밍·수동 자막 분할 표를 보존하고 새 번호와 새 출력 경로를 사용합니다. 바뀐 문장만 재합성하고 나머지 오디오는 일반 파일로 복사합니다. 문장 시작과 측정 길이에 애니메이션을 묶고, 길이가 바뀌면 뒤 장면과 자막을 다시 계산합니다. 시작할 때마다 설치된 `tk-video`, `tk-writing`, `tk-tts`의 revision 또는 콘텐츠 해시/수정 시각을 이전 기록과 비교하고 달라진 관련 지침을 다시 읽어 적용합니다. 재합성 수·보존 파일·revision 비교를 기존 근거에 남깁니다.
렌더를 중단하면 실행 소유 셸뿐 아니라 렌더·조립·인코딩 자식 프로세스의 종료까지 확인합니다. 기존 종료/정리 소유권 계약을 따르고 이전 출력은 보존하여 식별합니다. 같은 판 번호를 재사용하지 않습니다.

`overlay-rounded`는 `caption_box_color: "RRGGBB"`와 `caption_box_alpha`(0은 투명, 1은 불투명)를 받을 수 있습니다. 대체값은 검정(`000000`), 0.5이며 다크 배경에서는 예를 들어 `5A5A5A`, 0.65부터 대비를 확인합니다. 다른 style에 두 필드를 넘기면 실패하며 자막 없는 사본에서는 제거합니다.
