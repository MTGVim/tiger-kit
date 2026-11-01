<a id="figure-authoring"></a>
# 도해 작성

차트, SVG, 카드 흐름, 진단 요약이나 관련 시각 구성 요소에만 읽습니다. 일반 산문과 의미 기반 표에는 이 참조가 필요하지 않습니다.
공통 셸은 계속 기존 템플릿과 테마 자산이 담당합니다. 이 규칙은 내용 도해에 적용합니다.

<a id="data-visualization"></a>
## 데이터 시각화

수치 데이터나 근거가 있는 관계 그래프에 시각 자료가 도움이 되면 [차트 설계](chart-design.md)를 읽고
독립형 [차트 예제](../assets/chart-examples.html)의 해당 섹션을 검사합니다.
전체 갤러리가 아니라 관련 예제 하나와 범위가 한정된 스타일/상호작용을 적용합니다.
최종 HTML은 자체 완결형으로 유지합니다. 독자에게 설치된 패키지, CDN이나 차트 런타임이 계속 제공되어야 한다고 요구하지 않습니다.


<a id="render-safe-authoring"></a>
## 렌더링에 안전한 작성

첫 렌더링 검사 전에 이 규칙을 적용하여 흔한 배치 결함을 하나씩 발견하는 대신 예방합니다.

간결한 기준/발견 사항 묶음에는 `.ht-card` 컨테이너 하나 안에서 `role="list"`가 있는 의미 기반 목록과 선택적으로 적용하는 `.ht-info-list` 스타일을 사용합니다.
각 `.ht-info-row`는 장식용 `.ht-info-icon`(`aria-hidden="true"`, 인라인 SVG 또는 텍스트)과 축소 가능한 내용 블록 하나를 포함합니다.
항목 번호/레이블, 상태 의미, 판단, 근거와 행동을 DOM 읽기 순서에 따라 보이는 텍스트로 유지합니다.
순서가 중요할 때만 순서 목록이나 명시적인 ASCII 번호를 사용합니다. 아이콘과 CSS를 제거해도 의미가 사라지면 안 됩니다.
실제 참고 사항/한계에는 `.ht-callout` 안에 짧은 제목과 본문을 사용합니다. 정적 콜아웃은 실시간 `alert`가 아닙니다.

진단 요약에는 `<dl>`에 `.ht-kpis`를 사용하고, 뒷받침되는 지표마다 `<div><dt>Label and unit</dt>
<dd>Verified value</dd></div>` 하나를 둡니다. 좁은 화면에서 자동 줄바꿈합니다.
출처 범위/데이터 성격을 눈에 보이게 정의하고 발견 사항 목록에 공급하는 동일 레코드에서 각 값을 계산합니다. 없는 데이터를 0으로 채우지 않습니다.
상태 텍스트 `.ht-status`는 선택 사항으로 유지하고 명시적 의미와 근거를 둡니다.
관련 판단 옆에 일반 번호 인용을 재사용합니다.
의무적인 개별 카드나 큰 배지 대신 간격/구분선으로 행을 나눕니다. 체크리스트/prototype 상호작용 UI를 변경하지 않습니다.

네 가지 기준, 다국어 여러 줄 레이블, 긴 링크와 상태 텍스트를 모든 테마의 데스크톱과 모바일에서 검증합니다.
제목/목록/정의 목록 의미 구조와 접근 가능한 텍스트, 키보드 링크, 동작 줄이기, JS 없는 상태와 아이콘/CSS 제거를 확인합니다.
보고서 fixture에서는 예제 데이터를 명시적으로 표시합니다. KPI 합계/상태를 원본 레코드와 비교하고 빈 데이터와 부분 데이터,
산문/표 부정 사례도 실행합니다. DOM 접근성 검사가 모든 화면 읽기 프로그램을 실행했다는 주장은 아닙니다.

문서 스킬의 시각 문법에 따라 선택한 카드 흐름에는 레이블이 있는 `<figure>`와 순서가 있는 `.ht-flow` 목록을 사용합니다.
각 목록 항목은 한 단계입니다. 출력은 `.ht-card` 요소의 순서 없는 `.ht-flow-results` 목록으로 묶습니다.
DOM 순서를 읽기 순서와 같게 유지하고, 실제 제목과 `.ht-flow-link` 안의 명시적 관계 텍스트를 사용합니다.
장식용 화살표에는 `aria-hidden`을 사용합니다. 빠진 관계를 대신하지 않습니다.
`.ht-flow-focus`는 accent 토큰으로 핵심 과정을 강조할 수 있습니다.
모든 클래스는 선택적으로 적용하며 렌더러나 JS 없이 공통 테마를 재사용합니다.

모든 입력, 결과와 뒷받침되는 관계에 이름을 붙여 이 최소 구조를 적용합니다.

```html
<figure class="ht-figure" aria-labelledby="flow-title">
  <figcaption id="flow-title">Input, processing and simultaneous results</figcaption>
  <ol class="ht-flow">
    <li><div class="ht-card"><h3>Input set</h3><p>Verified input scope.</p></div>
      <p class="ht-flow-link"><span aria-hidden="true">↓</span> Inputs enter processing.</p></li>
    <li><div class="ht-card ht-flow-focus"><h3>Central process</h3><p>What changes.</p></div>
      <p class="ht-flow-link"><span aria-hidden="true">↓</span> Produces both results.</p></li>
    <li><h3>Simultaneous results</h3><ul class="ht-flow-results">
      <li class="ht-card"><h4>Result A</h4><p>Its distinct purpose.</p></li>
      <li class="ht-card"><h4>Result B</h4><p>Its distinct purpose.</p></li>
    </ul><p class="ht-flow-link"><span aria-hidden="true">↓</span> Both results support reuse.</p></li>
    <li class="ht-card"><h3>Reuse</h3><p>The supported downstream use.</p></li>
  </ol>
</figure>
```

데스크톱에서는 출력 두 열을 사용하고 600px 미만에서는 한 열을 사용합니다. 출력이 하나면 빈칸 없이 그룹 전체를 차지합니다.
텍스트에 따라 카드가 늘어나게 하고, 축소 가능한 트랙을 사용하며 긴 한국어/영어 레이블을 줄바꿈합니다.
고정 카드 높이, 열 사이의 위치 기반 화살표나 단계/선택지를 색만으로 구별하는 방식을 사용하지 않습니다.
범위에 포함된 화면 검사에서는 출력 1개, 2개와 4개, 긴 레이블, 동시/대안 표현, DOM 순서, JS 없는 읽기,
키보드 대상과 필요한 뷰포트에서 light/dark/system/reduced-motion을 검증합니다.
페이지 너비뿐 아니라 카드 텍스트와 관계 레이블의 겹침/잘림도 확인합니다.

- `pre`, 표, 긴 코드나 길이 제한 없는 산문을 담을 수 있는 grid 또는 flex 트랙은 `minmax(0, 1fr)`를 사용하고 자식은 `min-width: 0`을 사용합니다.
  넘침 결함을 숨기려고 페이지 수준 잘림이나 `overflow-x: hidden`을 사용하지 않습니다.
- 필요한 가장 좁은 뷰포트에 맞춰 인라인 SVG 크기를 정합니다. 축소 후 가장 작은 읽기 가능한 레이블은 최소 11 CSS px여야 합니다(`font-size * rendered-width / viewBox-width`).
  전후 비교나 다중 패널 도해가 이 기준을 충족하지 못하면 텍스트를 줄이는 대신 패널마다 SVG 하나를 쓰고 좁은 화면에서 패널을 쌓습니다.
  열이 의미를 전달하는 시퀀스/아키텍처 다이어그램에는 좁은 화면에서 범위가 제한된 가로 스크롤러를 유지합니다.
  임의의 너비를 선택하지 말고 `viewBox width * 11 / smallest label font-size`를 올림하여 최소 너비를 도출합니다.
  이 최솟값이 실제 1280px 데스크톱 내용 너비 안에 들어가도록 레이블 크기/viewBox를 고릅니다.
  화면 검사가 범위에 있으면 렌더링한 레이블 크기와 넘침을 측정합니다. 세로 배치에서도 의미가 유지되는 도해만 쌓습니다.
- 커밋 SHA, ID와 상태 토큰 같은 표 셀의 짧은 식별자는 한 줄로 유지합니다.
  `.ht-token`이나 동등한 로컬 규칙을 사용합니다. 긴 경로와 URL은 줄바꿈하거나 자체의 범위가 제한된 가로 스크롤러를 사용할 수 있습니다.
- 헤더나 도구 모음에서 `white-space: nowrap`을 사용하는 텍스트는 너비 제한이 입증되어야 하거나 모바일 breakpoint에서 줄바꿈으로 돌아가야 합니다.
  공통 유틸리티 클래스가 의도치 않게 더 긴 환경 레이블이나 제목을 한 줄로 강제하면 안 됩니다.
- 검증 캡처 위치만 맞추기 위한 프로그래밍 방식 스크롤은 즉시 동작을 사용합니다.
  부드러운 스크롤로 인해 의도한 대상이 캡처 뷰포트 밖에 남으면 안 됩니다.
