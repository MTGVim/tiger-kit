<a id="illustration-production"></a>
# 프롬프트와 실제 이미지 제작

이미지 생성 또는 외부 생성용 프롬프트 작성 전에 읽습니다. 도구 유무와 관계없이 동일한 근거·콘티·프롬프트를 준비합니다.

## 실제 기능 확인

현재 호스트가 노출한 네이티브 이미지 도구의 설명·스키마에서 생성, 참조 이미지 입력, 비율·크기, 배치·병렬 호출, 결과 접근과 보존 방법을 확인합니다. 기능 지원 여부는 실제 제공자와 모델에서 확인합니다. 실제 도구가 제공하는 형식과 사용 지침을 따르며 지원이 확인된 파라미터만 사용합니다.

사용자가 지정한 엄격한 비율이나 필수 참조 기능을 지원하지 않으면 해당 요구는 차단 상태입니다. 근사 비율이나 텍스트 설명으로 대체하려면 그 요구를 바꿀 수 있는지 확인합니다. 단순 동시 생성 미지원은 내용 변경이 없으므로 순차 처리로 계속하며 알려 줍니다. 이미지 도구가 없으면 [로컬 폴백 선택](../../tk-writing/references/local-image-fallback.md)을 적용합니다. 선택·설치 승인을 받지 않은 백엔드·CLI·API 우회나 자격 증명 탐색은 하지 않습니다. 폴백을 선택하지 않거나 실행할 수 없으면 [외부 인계](handoff.md)를 완성합니다.

## 폴백의 그림·텍스트 분리

로컬 폴백을 선택한 경우에만 [분리 식질](../../tk-writing/references/local-image-fallback.md#분리-식질)을 따릅니다. 장면 프롬프트에는 글자·제목·말풍선·패널 ID를 그리지 말라고 명시하고, 정확한 모든 문구는 별도 텍스트 명세에 보존합니다. 아래 `Exact text`는 이 경로에서 모델에 전달할 문구가 아니라 최종 조립용 명세입니다. 네이티브 도구에는 기존 완전한 프롬프트와 실제 참조 전달을 유지합니다.

## 실제 참조 이미지

각 참조의 실제 위치·접근 가능 여부·용도(`direct/style/palette`)·사용 조건을 `references/manifest.md`에 기록합니다. 로컬 파일은 열어 확인하고 호스트 첨부는 지원되는 자산 참조를 사용합니다. 실제로 생성되고 확인된 이미지 파일만 이미지 산출물로 전달합니다. 직접 전달이 필요하면 도구 입력에 실제 자산이 포함되었는지 확인합니다.

`style/palette`를 텍스트 특징으로 추출한 경우 그 사실을 표시합니다. 이는 동일 인물·객체 재현을 보장하지 않습니다. 원본 정체성 유지가 필수인데 직접 참조가 불가능하면 이미지 제작을 차단하고 인계 패키지에 빠진 기능을 기록합니다. 허가받은 참조 파일만 패키지로 복사합니다. 권한이 없는 원문·비밀·자산은 프롬프트와 외부 패키지에서 제외하고 필요한 입력을 따로 밝힙니다.

## 저장한 프롬프트 사용

이미지 호출 전에 실행 소유 `prompts/<ID>-<slug>-<candidate>.md`에 해당 그림의 완전한 프롬프트를 저장합니다. 각 프롬프트에 필요한 내용을 포함해 독립적으로 이해할 수 있게 작성합니다. 첫 후보도 파일을 먼저 만들고 실제 호출에는 그 전체 내용과 확인된 실제 참조를 전달합니다. 원본 수치 문자열·단위·조건·정확한 레이블을 보존합니다.

선택한 레이아웃·스타일 카드만 읽고 다음 틀을 모두 채웁니다. 아래 영문 필드 이름은 예시이며 출력 언어는 확정된 독자 언어입니다.

```markdown
# Image specifications
- ID / candidate: <stable image ID and new candidate ID>
- Mode / type: <single, article or infographic / content type>
- Layout: <selected ID, zones and reading order>
- Style / palette: <confirmed treatment and color roles>
- Aspect / display size: <requested ratio and intended viewing size>
- Language: <confirmed reader language>

## Source-bound objective
<Reader question, conclusion, prerequisites and allowed facts.>

## Storyboard and layout
<Each zone's position, subject, action, connectors and sequence.>

## Exact text
<Complete titles, labels, number strings, units, conditions and captions.>

## Style directions
<Lines, shapes, texture, contrast, text treatment, color semantics.>

## References
<Actual authorized references and direct/style/palette use; unavailable inputs stated.>

## Constraints
<No invented facts, values, measurement ticks, causal links or unlabeled assumptions.
No additional text or borrowed characters. Keep required caveats and reading order.>
```

출처 연결을 포함한 내부 근거와 외부 전송 가능한 프롬프트를 구분합니다. 원문이 길면 정확한 라벨과 필요한 주장만 프롬프트에 넣습니다. 배치를 줄일 때도 중요한 조건을 유지합니다. 정확한 데이터 그림은 별도 정적 제작이 필요한지 판단합니다.

## 생성과 복구

필요한 모든 프롬프트를 저장·검사한 뒤 생성합니다. 동시에 실행할 수 있는 서로 독립적인 이미지만 `--batch-size` 범위 안에서 처리합니다. 실제 기능·호출 제한·승인된 비용 범위를 넘지 않고, 이미지마다 프롬프트·실제 참조·출력·도구·가능하면 모델 식별값을 기록합니다. 모델명·토큰·금액은 실제 제공된 근거를 기록하며 공백은 미확인으로 둡니다.

실패한 항목은 원인을 확인하여 같은 승인 범위에서 한 번 수정·재시도할 수 있습니다. 반복 실패는 자동으로 무한 생성하지 않고 해당 ID의 준비물과 실패를 전달합니다. 성공한 항목은 보존하고 실패한 항목만 복구 대상으로 삼습니다. 이전 후보를 덮어쓰지 않고 새 프롬프트·이미지 경로를 사용하며, 검사에 통과한 후보만 최종 참조로 선택합니다.

도구가 결과를 자동 보존하면 그 결과 참조를 유지합니다. 다른 산출물에 내장하는 데 실제 로컬 바이트가 필요한 경우에만 호스트가 허용한 저장 방법을 사용합니다. 결과에 접근하지 못하면 경로·해시·픽셀 검사를 만들어 내지 않고 해당 검사를 `Unverifiable`로 남깁니다. 최종 가독성·정확성은 실제 이미지로 검사합니다.
