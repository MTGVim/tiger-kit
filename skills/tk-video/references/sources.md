<a id="design-sources"></a>
# 설계 출처

출처 검토에서는 merge `dd53fe0b57223bbbbb8ceae0bda2ba8a26d1c29a`의 `obra/superpowers` PR #2214에서 SKILL.md, rendering-stills.md와 assembling.md를 읽었습니다.
[원래 설계](https://github.com/obra/superpowers/tree/dd53fe0b57223bbbbb8ceae0bda2ba8a26d1c29a/skills/proving-it-works-with-a-movie)는 코드 품질 문제로 릴리즈 전에 [#2335](https://github.com/obra/superpowers/pull/2335)에서 제거되었습니다.
이는 선행 사례이며, 지원하는 런타임 의존성이나 가져온 구현이 아닙니다.

유지: 시퀀스용 정지 이미지, 측정한 내레이션 유지 시간, 실제 사실에 충실한 캡처 경계와 완성본 검사입니다.
적응: 명시적 설명 모드, 결정적인 기본 미디어 검사, libass 사전 점검과 소프트 자막 대체 경로입니다.
명시적인 내레이션 선택과 독립적인 애플리케이션 판정을 보존합니다.
제외: ASR 검증, 자동 도구/모델 획득, 터미널/로그 영상, Windows 지원과 의무적인 커밋 영상 파이프라인입니다.
작성과 근거는 TigerKit 산출물 정책을 따릅니다.

TigerKit은 `1d6630284a9f14491967f2bb5f87f0a62e87571c`에서 GIF/MP4 공통 10fps 인코딩을 도입했습니다.
코드와 변경 기록에는 프레임률이 명시되어 있지만 MP4에 특화한 근거는 없습니다.
위의 원래 조립 예제는 `-r 30`을 사용하며, 공통 10fps를 요구하지 않습니다.
10fps는 GIF의 5MiB 크기 경고와 함께 GIF의 작은 용량을 위한 기본값 및 정지 이미지용으로 유지합니다.
MP4 캡처 프레임률은 원본 메타데이터 또는 공개한 타임스탬프 추정을 따르며 최대 30fps로 제한합니다.
이는 제품의 절충이며 크기를 보장하지 않습니다.


<a id="optional-presentation-effects"></a>
## 선택적 프레젠테이션 효과

2026-10-28 검토: [FFmpeg zoompan 소스](https://github.com/FFmpeg/FFmpeg/blob/c69954c34522c53234dfd43fa7a0cb3b02f39e47/libavfilter/vf_zoompan.c), 해당 필터 문서와 설치된 FFmpeg 6.1 구현,
[libass 형식 지침](https://github.com/libass/libass/wiki/ASS-File-Format-Guide), [Aegisub 그리기 태그](https://aegisub.org/docs/latest/ass_tags/)를 검토했습니다.
원래 타이밍과 고정 출력 크기를 유지하고, 입력 프레임 기반 줌 표현식, 실제 글리프 잉크 측정과 ASS 벡터 카드를 적용합니다.
가장자리 테두리를 보존하기 위해 RGB 자르기 입력과 올림한 원점을 사용합니다. 정수 자르기 위치는 여전히 움직임의 한계입니다.
사각형 상자는 libass의 `BorderStyle=4` 확장을 사용하며 디코딩한 프레임 테스트로 검증했습니다. 이식 가능한 ASS 재생 호환성은 주장하지 않습니다.
전달물은 이미 번인한 영상과 일반 SRT입니다.

제공된 네 변형 실험은 한 제작자의 선호 근거입니다. 결합된 콜아웃/줌 처리를 명시적 선택으로 적용하고 보편적인 스타일 변경은 제외합니다.
[Openscreen](https://github.com/siddharthvaddem/openscreen)은 커서를 따르는 자동 줌의 선행 사례일 뿐이며, 데스크톱 녹화기, 런타임이나 코드를 가져오지 않습니다.
원본 좌표 인계는 기존 캡처 담당자에게 유지합니다.

기존 대기/음량 정책에 대해 [Fluent Spinner](https://fluent2.microsoft.design/components/web/react/core/spinner/usage)와 [Wait UX](https://fluent2.microsoft.design/wait-ux)는 1초 임계값을 뒷받침합니다.
[Primer 로딩](https://primer.style/product/ui-patterns/loading/)은 불확정 진행 피드백을 뒷받침하지만 그 정확한 임계값을 확립하지는 않습니다.
[EBU R128](https://tech.ebu.ch/publications/r128)은 프로그램 음량 -23 LUFS를 뒷받침합니다. tk-tts 기본값 -18과 실제 청취는 유지합니다.

<a id="presentation-planning-slides-and-captions-off-2026-10-29"></a>
## 프레젠테이션 계획, 슬라이드와 자막 끄기 (2026-10-29)

현재 HEAD `31ba826726fd0d1547f2c22e041848d1d7f3f860`의 최신 [FFmpeg 필터 문서](https://github.com/FFmpeg/FFmpeg/blob/31ba826726fd0d1547f2c22e041848d1d7f3f860/doc/filters.texi)를 검사했습니다.
검사에는 subtitles/libass, zoompan의 명시적 크기/프레임률/타이밍과 설치된 FFmpeg의 인코딩/디코딩 동작이 포함되었습니다.
기존 캡처 좌표와 텍스트 효과 검사를 유지합니다. 오디오 검증을 보존하면서 자막 필터/트랙을 생략하는 방식으로 자막 끄기를 적용합니다.
새 렌더러, 도구 설치와 암묵적 효과는 제외합니다.
공유 미디어 선택/저장 계약은 TigerKit의 기존 런타임 검증 선호 계약을 확장합니다.
제공된 반복 조립 사례는 런타임 dispatcher나 새로운 상시 권한을 추가하지 않고, 상위 작업들과 직접 영상 작업 전반에서 첫 라운드에 한 번 결정해야 할 근거가 됩니다.

슬라이드 문구 기준은 TigerKit의 `tk-explain` 명료한 글쓰기/독자용 서식 계약(원본 기준 `e672abcc0fedc8b91766266c8117a21496f02cbe`)을 선택적으로 적용하여 서술어 완결성, 일관된 문체, 자막/내레이션 의미와 비교 대상 가시성을 다룹니다.
실제 프레임 검사와 청취 검사는 분리하여 유지합니다. 형제 패키지 런타임 가져오기나 전체 산문 검토 파이프라인은 제외합니다.
밝은 슬라이드와 슬라이드 내 강조는 이 워크플로의 작성 대체값이며, 보편적으로 더 나은 학습에 대한 실증적 주장이 아닙니다.
명시적/저장된 선택이 우선합니다.

<a id="external-manim-and-selectable-captions-issue-486"></a>
## 외부 Manim과 선택 가능한 자막 (issue 486)

검증한 현재 HEAD의 [adithya-s-k/manim_skill](https://github.com/adithya-s-k/manim_skill/tree/cef045011722d285692e3381d12d4d637da56e18)에서 composer와 ManimCE 스킬 진입점, CLI/config/텍스트 규칙, 테스트 지침/유틸리티와 MIT 라이선스를 검사했습니다.
이를 복사해 넣은 지침이나 템플릿으로 취급하지 않고 변경하지 않은 외부 의존성으로 유지합니다.
호출자의 원본/준비 상태 계약, 선택한 런타임 인계와 연속 미디어 경계만 적용합니다. ManimGL, 자동 설정과 미리보기는 제외합니다.
upstream에는 검증된 SemVer 릴리즈 메타데이터가 없습니다. 설치기 폴더 해시는 커밋이 아닙니다.

설치된 ManimCE 0.20.1 Docker 런타임의 실제 렌더링 도움말이 테스트한 CLI 문법의 정본이며, 최신이라고 주장하지 않습니다.
FFmpeg의 [스트림 선택/streamcopy](https://ffmpeg.org/ffmpeg.html)와 [HTML track 요소](https://html.spec.whatwg.org/multipage/media.html#the-track-element)는 명시적 오디오 매핑과 브라우저 WebVTT 전달의 근거입니다.
분수 원본 프레임률과 네이티브 오디오를 유지하고, 선택 가능한 mov_text와 사이드카를 적용하며, 범용 플레이어나 조용한 타이밍 변경은 제외합니다.
출력된 기본 disposition을 검사합니다. 이를 지워도 MP4 muxer가 첫 자막을 처음부터 비활성화한 상태로 둔다고 보장하지 않습니다.
실제 브라우저/플레이어 검사는 인코딩, 소스 검사, 합성 오디오와 사람의 청취와 구별하여 보고합니다.
upstream 전체 예제 테스트 suite는 실행하지 않았습니다. 이 통합에는 범위를 제한한 실제 렌더링과 회귀 근거를 사용합니다.


<a id="answer-first-opening-and-visible-cc-issue-490"></a>
## 답을 먼저 제시하는 도입과 보이는 CC (issue 490)

[#490](https://github.com/MTGVim/tiger-kit/issues/490)에서 제공된 React/Dijkstra 뷰어 피드백은 전달한 해당 영상에 대한 구체적 수정이며, 보편적 학습 향상의 근거가 아닙니다.
위에서 검증한 revision의 외부 composer 내러티브 패턴에는 궁금증/해소 예제가 남아 있습니다.
짧은 질문 도입과 점진적 객체 움직임을 유지하고, 호출자가 수락한 질문 → 즉시 답/이유 → 풀이 예시 순서를 적용합니다.
외부 스킬 재작성, 의무적인 긴장감 구성과 새로운 전역 자막 선호는 제외합니다.

FFmpeg의 [pad 필터](https://ffmpeg.org/ffmpeg-filters.html#pad-1)와 디코딩한 회귀 프레임은 기존 UI 보존 밴드를 명시적으로 선택한 하드 애니메이션 자막까지 확장하는 것을 뒷받침합니다.
원본 픽셀, 프레임률과 타이밍을 유지하고, 추가된 높이를 공개하며, 가장 긴 큐와 여러 줄 큐를 검사합니다.
soft/off 기본값과 독립 청취는 유지합니다.

<a id="native-manim-explanation-not-screenshot-substitution-2026-10-30"></a>
## 스크린샷 대체가 아닌 네이티브 Manim 설명 (2026-10-30)

upstream 기본 브랜치를 동일한 `cef045011722d285692e3381d12d4d637da56e18`에서 다시 확인했습니다.
원래 composer의 시각적 연속성/점진적 공개 지침과 ManimCE 장면 규칙은 변경하지 않은 외부 자료로 유지합니다.
네이티브 객체 변환과 의미 있는 상태 연속성을 유지합니다. 호출자의 렌더러 선택, 전/연산/후 검사와 원본 출처를 수락한 React/Dijkstra 워크플로에 적용합니다.
복사한 upstream 템플릿, 보편적인 Manim 선행 조건, 장식적 움직임 할당량과 애니메이션 개수에 따른 품질 주장은 제외합니다.
전달한 두 영상은 실제 네이티브 렌더링 경로를 확립하며, 보편적으로 최대한 활용했다거나 학습이 향상되었다는 사실을 확립하지 않습니다.
명시적 HTML/정지 이미지 출력과 관찰한 UI는 각각의 담당자와 승인 경계를 유지합니다.

## 영상 피드백과 원고 점검 (2026-11-02)

사용자가 제공한 review-loop 묶음을 참고 구현으로 검토했습니다. 외부 코드를 복사한 구현이 아닙니다.
[Able Player](https://github.com/ableplayer/ableplayer/tree/3f174b22bd779e42db2959401f1bec003a5b2880)(MIT)의 대본 클릭 이동·현재 위치·키보드 조작과 [hyperaudio-lite](https://github.com/hyperaudio/hyperaudio-lite/tree/8747ce1d9aa607fc020239eb45c7bb3f3cc8775a)(MIT)의 대본 따라가기는 설계 참고입니다.
YouTube·Udemy는 단축키·시각 노트 경험만 참고하며 해당 서비스 코드를 포함하지 않습니다.
`keep`: 단독 MP4, 기존 자막 기본값, 사용자 선택·설치·청취·발행 경계입니다.
`adapt`: 별도 로컬 피드백 HTML, 의미 단위 자막 분할, 사용자별 renderer와 Manim 도입부 선택입니다.
`omit`: 보편적 Manim 기본값, 자동 자막 분할, 작은 SVG 객체 전체를 점으로 치환하는 규칙입니다.
Manim upstream `cef045011722d285692e3381d12d4d637da56e18`의 composer와 narrative-patterns를 재확인했습니다.
질문형 서사는 명시적 선택에만 적용하며 상위에서 확정한 순서를 보존합니다.

## 설명 영상 결함 회고 재검토 (2026-11-03)

사용자가 제공한 2026-11-02 explainer-video-defects 묶음의 33개 항목, 최소 패치와 미검증 도구를 현재 소스 `647c6d76`과 대조했습니다. 바로 앞 review-loop 결정 중 `cards` 대체값과 영상 고지 validator 제외는 이 재검토가 대체합니다. 이는 사용자가 승인한 제작 계약이며 보편적 학습 효과의 증거가 아닙니다.
- `keep`: 캡처 출처·실제 타임스탬프, 명시적 renderer/자막 선택, 원본 보존, leaf symlink 거부, 설치·청취·발행 경계입니다.
- `adapt`: Manim 다크 대체값, 상시 제목 없는 장면, 고정된 피드백 시각과 명시적 재지정, 원본/대본 대조, 문구 검색, 전달 묶음과 receipt를 소비하는 고지 게이트입니다. 첨부 고지 도구의 soft 자막 인정과 중간 공백 허용을 제거하고, 별도 주입 CLI 대신 조립기에 통합했습니다. 빈 본문 도구는 스트리밍과 명시적 짝수 crop, 가장자리·중심 측정을 함께 수행하도록 다시 작성했습니다.
- `omit`: 개인 메모리 의존, 자동 자막 분할, 보편적 학습 우위 주장, 숨겨진 카드 fallback, 자동 설치와 별도 상시 테스트 suite입니다.

[manim_skill `cef045011722d285692e3381d12d4d637da56e18`](https://github.com/adithya-s-k/manim_skill/tree/cef045011722d285692e3381d12d4d637da56e18)의 현재 composer, Golden Layout과 tests/manimce 안내를 재확인했습니다. 원본은 장면 구성·점진적 공개·색 선택을 안내하지만 상시 제목 제거와 문장별 퇴장 기준은 TigerKit의 보강입니다. 원본 스킬과 예제 테스트를 복사하거나 전체 실행하지 않습니다.
[Pycairo 설치 문서](https://pycairo.readthedocs.io/en/latest/getting_started.html), [PyPI pkgconf](https://pypi.org/project/pkgconf/)와 [Homebrew ffmpeg-full](https://formulae.brew.sh/formula/ffmpeg-full)에서 cairo 헤더/pkg-config 필요, venv 스크립트 제공과 libass 의존성을 확인했습니다. macOS 실제 재설치와 사용자 입력·청취는 이 확인에 포함되지 않습니다. 학습 논문을 읽거나 재현하지 않았으므로 회고의 학습 효과 해석을 검증된 사실로 승격하지 않습니다.
