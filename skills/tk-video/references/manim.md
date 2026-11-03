<a id="external-manim-dependency-and-rendering"></a>
# 외부 Manim 의존성과 렌더링

Manim 작업을 선택한 경우에만 읽습니다. `manim-composer`는 장면을 계획하고 `manimce-best-practices`는 Manim Community Edition 구현을 안내합니다. 둘 다 [adithya-s-k/manim_skill](https://github.com/adithya-s-k/manim_skill)의 외부 의존성입니다. 호스트가 지원하는 스킬 catalog/loader로 설치 경로를 찾고 원래 `SKILL.md`와 요청된 참조를 읽습니다. 변경 없이 유지합니다. TigerKit 사본, 다시 작성한 대체물, 자동 설치/업데이트나 필수 ManimGL 의존성은 두지 않습니다.

<a id="identity-and-freshness"></a>
## 식별과 최신성

폴더 이름만이 아니라 정확한 설치 이름과 읽을 수 있는 참조를 검증합니다. 설치기 lock이나 일치하는 Git checkout에서 소스 식별 정보를 확립합니다. Skills CLI lock v3의 `source`, `sourceType`과 `skillPath`는 주장된 출처를 식별합니다. `skillFolderHash`는 Git commit이나 SemVer가 아닙니다. 주변 애플리케이션의 Git remote는 해당 스킬의 출처가 아닙니다.

이 경로에서만 현재 upstream 기본 branch commit과 선택한 스킬 tree를 조회합니다. Git 설치라면 실제 commit과 로컬 변경을 기록합니다. 복사 설치라면 선택한 스킬 전체의 일반 파일 경로/바이트를 해당 upstream tree와 비교합니다. 설치 commit을 만들어 내지 말고 `content_matches_revision`을 기록합니다. 필요한 참조 파일을 검증합니다. 수정되었거나 불일치하는 설치 파일을 보존합니다. 이 upstream에는 검증된 Archify 방식 release manifest/버전 gate가 없습니다. `skill-release.json`을 요구하거나 버전을 만들어 내지 않습니다.

미설치, 알 수 없거나 수정된 콘텐츠, 검증된 이전 콘텐츠와 네트워크 불가를 구별합니다. 실제 상태와 검증 가능한 최신 상태를 보고하고 현재 소스/commit을 제안합니다. 알 수 없는 출처는 통과가 아닙니다. Renderer를 바꾸지 말고 해당 Manim 분기를 중단합니다. 최신 조회 실패는 `Unverifiable`이며 업데이트 권한이 아닙니다. 사용자가 명시적으로 수용한 오프라인 범위 아래에서만 검증된 설치 snapshot을 오프라인으로 재사용합니다.

<a id="runtime-and-setup-handoff"></a>
## 런타임과 설정 인계

선택한 경로만 검사합니다. 전용 native Python의 `-m manim --version`과 render help, 또는 이미 사용 가능한 Docker engine/image와 해당 image의 ManimCE 버전/help를 확인합니다. `manimlib`/ManimGL이 아니라 `manim`인지 확인합니다. 두 경로를 모두 제안하려고 Docker를 시작하거나 native 의존성을 설치하지 않습니다. 설치, image tag와 버전 문자열만으로는 render를 입증하지 못합니다.

설정이 없으면 현재 upstream 설치 안내와 [Manim PyPI 메타데이터](https://pypi.org/pypi/manim/json) 같은 선택한 release 메타데이터를 검사합니다. 스킬 출처/revision, 선택한 환경/image, 누락 capability와 알려진/알 수 없는 다운로드 용량 및 설치 용량을 보고합니다. 조립에는 FFmpeg를, 선택한 텍스트에는 font를, TeX 객체에만 LaTeX를, 선택한 합성에만 `tk-tts`를 요구합니다. 전역 pip 설치, 모델 다운로드나 Docker pull로 이어지지 않습니다.

필요한 사용자 행동/권한에는 정확한 소비자 `tk-video`, 선택한 Manim 기준, 호스트/런타임/소스 사실, 제안한 설정 범위, 누락 capability, 사용자 행동과 완료 신호를 `tk-wizard`에 인계합니다. 해당 행동 후 식별 정보, 버전, 관련 capability와 작은 실제 render를 다시 확인한 뒤 재개합니다. 일상적인 승인된 CLI 작업은 구현 담당자에게 남습니다.

<a id="author-and-render"></a>
## 작성과 렌더링

렌더링 전에 [합성 전 원고 점검](narration.md#pre-synthesis-copy-check)을 수행합니다. 실물과 수치는 [시각 표현](slide-authoring.md#objects-and-values)을 따릅니다.

선택한 설명의 기하 구조, graph 순회, 알고리즘 상태와 관계에는 Manim native 객체와 의미 있는 전환을 사용합니다. 작업 중 객체 식별을 보존하여 시청자가 무엇이 이동하거나 변경되었는지 볼 수 있게 합니다. 작성 편의를 위해 Manim으로 설명할 수 있는 내용을 HTML screenshot, 평면화한 diagram 카드나 정적 slide deck으로 대체하지 않습니다. 움직임이 의미를 더하지 않는 곳에는 정적 제목, label과 정지를 사용합니다. Animation 수만 늘리려고 모든 요소를 움직이거나 장식적인 움직임을 추가하지 않습니다. 실제 UI와 인용 이미지는 출처가 있는 제공 자산으로 남을 수 있으며 조작된 Manim 재연으로 바꾸지 않습니다.

관련 변경 전/작업/변경 후 상태와 내레이션 anchor를 계획한 뒤 디코딩된 전환 frame을 검사하여 단순한 fade나 hold의 연속이 아니라 작동 원리가 보이는지 확인합니다. 기존 검사 근거에 장면 소스/class, 실제 render 영상, 표본 전환과 Manim이 아닌 부분 및 그 이유를 명시합니다. 성공한 render나 `Played N animations` log는 의미 있는 움직임, 최대 활용이나 설명 품질을 입증하지 않습니다. 명시적인 정적/HTML 선택은 이 경로 밖에 두고 Manim을 사용할 수 없으면 기존의 몰래 renderer를 전환하지 않는 조건와 설정/승인 경계를 유지합니다.

설명 MP4는 별도 선택이 없으면 hard 자막본과 SRT, 내레이션이 있으면 무자막본도 만듭니다. 명시적 soft/off 선택과 이미 답한 선택은 재사용합니다. Manifest의 `caption_delivery`를 전달하고 저장 선호 key를 추가하지 않습니다. Slide 전용 theme/강조 기본값으로 연속 영상의 색이나 타이밍을 바꾸지 않습니다.

수용된 독자/주장, 장면 사실, 미디어 선택과 실행 소유 출력 경로를 외부 composer에 전달한 뒤 외부 ManimCE 지침을 로드합니다. 이미 답한 질문은 재사용합니다. 외부 composer의 mystery/payoff 예시는 수용된 도입 순서를 재정의하지 않습니다. 결론 먼저를 선택했으면 풀이 예시 전에 답과 초점을 전달하고, 질문형을 선택했으면 질문·관찰 뒤 본론에서 답을 밝힙니다. 자막을 추가할 때 점진적인 객체 움직임을 유지합니다. 어느 외부 스킬도 설치, preview, 발행이나 파일시스템 권한을 확대하지 않습니다. 장면 코드와 캐시는 두 스킬 밖의 호출 실행 안에 둡니다. 실제 설치된 CLI 구문으로 preview/자동 열기 없이 headless render를 수행합니다. Light slide/10fps 기본값을 적용하지 말고 선택한 theme, 해상도, FPS와 timeline을 보존합니다. 성능은 동일한 장면/rate/오디오 조건과 측정한 시간/최대 메모리로만 비교합니다. 크기를 만들어 내지 않습니다.

화면 literal `2`와 `DOM`을 낭독 `이`와 `돔`과 분리하고 맥락에서 의미를 확인합니다. Native 장면 강조, 자막 안전 영역과 render 출처 tag를 사용합니다. 초기/최종 상태, 전환과 내레이션 beat를 검사합니다. 발음/clipping은 들을 때까지 대기로 유지합니다. ASR은 추가하지 않습니다. 완전한 MP4 하나를 [애니메이션 조립](assembly.md#continuous-rendered-video)에 제공합니다. 무관한 영상을 정지시키거나 타이밍을 바꾸거나 섞는 대신 그 render 안에 여러 beat를 작성합니다. 음성이 맞지 않으면 측정한 오디오를 가지고 장면 작성으로 돌아갑니다. 입력/코드를 보존합니다. 의존성과 인코딩 점검은 설명 품질이나 자막 player 지원을 입증하지 않습니다.

## SVG와 LaTeX가 없는 차트

Lucide 등 round-cap의 길이 0인 선으로 점을 그리는 SVG는 `SVGMobject`에서 점이 사라질 수 있습니다.
원본 SVG와 렌더링을 비교하여 해당 선만 `Dot` 또는 원으로 복원합니다. 아이콘 높이의 8% 미만이라는 이유만으로
모든 작은 하위 객체를 점으로 바꾸지 않습니다. 짧은 선과 다른 세부까지 훼손할 수 있습니다.
LaTeX가 없으면 `BarChart`나 숫자를 켠 `NumberLine` 대신 `Rectangle`과 `Text`로 막대·값·축을 직접 작성합니다.
TeX를 쓰지 않는 장면을 위해 LaTeX를 자동 설치하지 않습니다.

<a id="manim-theme-and-scene-checks"></a>
## 테마와 장면 점검

애니메이션 목록을 미리 만들면 `.animate`가 작성 시점 상태로 목표를 만들 수 있습니다. 앞 비트에서
이동·변형한 객체에 미리 만든 `.animate`를 그대로 재생하지 않습니다. 실행 시점에 애니메이션을 만드는
factory를 쓰거나 정확한 끝 상태 객체를 만들고 `ReplacementTransform`으로 바꿉니다. 색만 바꾸다가
위치가 되돌아가지 않는지 시작·중간·끝 프레임을 확인합니다. 장면 하나만 고치면 그 장면까지 `-ql`로
미리보기한 뒤 전체를 렌더링합니다. 화면 문구가 길어지면 렌더 전 폭·줄 수를 주변 요소와 대조하고
미리보기에서 겹침·잘림을 확인합니다. 글자 크기를 줄이기 전에 문구 분할·배치를 함께 검토합니다.


현재 선택과 저장된 `manimTheme`을 우선하고 값이 없으면 다크를 사용합니다. 카드의 `slideTheme`을 가져오지 않습니다. 다음은 작성 시작값이며 실제 프레임에서 대비를 확인합니다.

| 역할 | 다크 | 라이트 |
| --- | --- | --- |
| 배경 | `#151514` | `#fafaf7` |
| 본문 | `#ecebe6` | `#242421` |
| 보조 글자 | `#b4b3ad` | `#62625c` |
| 선 | `#4b4a46` | `#b8b8af` |
| 강조 | `#6aa8f0` | `#246fc0` |
| 경고 | `#f07a7a` | `#bd3333` |
| 정상 | `#4cc764` | `#247b36` |
| 면 | `#1f1f1d` | `#eeeee7` |

면을 흰색 상수로 채우지 말고 테마의 면 색을 사용합니다. 다크의 rounded 자막 상자는 `caption_box_color`와 `caption_box_alpha`로 배경과 구분하며 글자 대비도 검사합니다.
상시 제목은 기본으로 두지 않습니다. 장면 이동은 질문과 그림으로 알리고, 필요할 때만 장면의 요지를 담는 짧은 핵심어를 표시합니다. 구간 이름을 쓰면 표시·제거 시각을 계획에 적고 외부 composer의 Golden Layout 제목 줄을 의무로 해석하지 않습니다.

문장별 표시 객체와 제거 시점을 계획합니다. 다음 설명에 쓰이지 않는 객체는 문장 시작에 `FadeOut`하거나 흐리게 줄이고, 동시에 설명하는 그룹은 세 개 이하를 출발점으로 삼습니다. 같은 시간·수량·상태는 앞서 쓴 축·기호·색을 재사용하고 바뀐 값만 움직입니다. 형식이 바뀌면 이유를 적습니다.
가장자리 텍스트는 `to_edge`·`to_corner`의 `buff`와 `next_to`로 배치하고 바깥쪽 끝을 기준으로 정렬합니다. 긴 문구는 나누며, 최종 렌더 전에 `-ql` 렌더의 beat 끝 프레임 타일을 확인하여 잘림·겹침·자막 영역 침범을 고칩니다.

그림 묶음은 자막 없는 원본 화면의 세로 중심에 맞추되 아래 끝이 자막 상자 위에 있어야 합니다. 제목·고지 줄을 추가하거나 빼면 끝 프레임의 그림 위·아래 끝과 중심을 다시 측정합니다. 중심은 원본 높이의 중앙 ±5%를 점검 기준으로 삼고 충돌하면 먼저 장면 크기·배치를 고칩니다. 카메라를 옮기면 고정 요소의 반대 보정도 재확인합니다. 자막본과 무자막본은 같은 렌더를 사용합니다.

최종 자막 없는 영상에 `scripts/scan_visual.py --video <render.mp4> --captions <out.srt> --top <fraction> --bottom <fraction>`을 실행합니다. 제목·고지·자막을 제외한 실제 본문 띠를 지정하고 초당 2프레임에서 빈 본문과 좌우 가장자리 12px의 잉크를 찾습니다. 1초 이상 내레이션과 겹치는 빈 구간에는 다음 그림까지 유지할 요약 한 줄을 두거나 장면 전환을 고칩니다. 시작 페이드인도 자동 제외하지 말고 판정합니다. 고정 요소와 의도적인 가장자리 표시의 오탐은 이유와 해당 프레임을 남깁니다. 수정 전·후를 같은 설정으로 비교하고 후보 구간 수, 처리 결과와 중심 측정 표를 기존 검사 근거에 남깁니다. 자동 검출은 의미·겹침 검사나 육안 확인을 대신하지 않습니다.

### macOS pycairo 복구

선택한 venv 안 설치가 승인되어 있고 cairo 헤더가 이미 있을 때 `pkg-config`만 없으면 PyPI `pkgconf`를 같은 venv에 설치하는 경로를 제안합니다. `PATH`에는 그 venv의 `bin`을 앞에 두고, `PKG_CONFIG_PATH`에는 실제 `brew --prefix`에서 확인한 `lib/pkgconfig`, `share/pkgconfig`와 해당 macOS 주 버전에 존재하는 Homebrew `Library/Homebrew/os/mac/pkgconfig/<major>`를 사용합니다. 이 경로를 추측하거나 cairo 부재를 숨기지 않습니다. cairo/전역 도구 추가 설치는 별도 승인 범위입니다. 설치 뒤 `import cairo`와 작은 Manim 장면의 실제 렌더를 확인합니다. 이 안내는 macOS 재현 근거를 바탕으로 하며 다른 호스트에서 실행했다고 주장하지 않습니다.
