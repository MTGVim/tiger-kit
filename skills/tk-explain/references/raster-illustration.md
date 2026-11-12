<a id="ai-raster-illustration"></a>
# AI 래스터 일러스트레이션

AI로 그린 인포그래픽, `baoyu`와 유사한 결과, 캐릭터 일러스트레이션 또는
선택된 래스터 형식이나 요청된 설명 페이지의 기본 그림을 제작할 때 읽습니다. 출력을 정의하는 동작은 래스터 이미지 생성입니다. 주제가 기술적이어도 HTML/SVG,
canvas 또는 코드로 그린 그림은 AI 래스터 생성의 성공적인 대체물이 아닙니다. 도구 부재에 한해 아래의 명시적 임시 대체물 분기를 사용합니다.
정확한 소스 코드·측정값 그림을 요청하면 별도의 정적 요약 이미지 경로를 사용합니다.
이를 대안으로 제시하고, AI 일러스트레이션을 완료한 것처럼 조용히 대체하지 않습니다.

<a id="bind-content-before-appearance"></a>
## 외관보다 먼저 콘텐츠를 결합한다

실행의 `evidence.md`와 정확한 원본 스냅샷을 재사용합니다. 실행의
임시 디렉터리에 독자 목표, 결론, 절, 출처가 결합된 주장,
시각적 관계와 정확한 라벨·데이터 목록을 구조화된 콘텐츠로 작성합니다. 새 사실을 추가하지 않습니다. 출처의 숫자
문자열, 단위, 분모, 한정 조건과 조건 경계를 보존합니다.
관련 작업 권한 없이 비밀이나 비공개 소스 코드를 이미지 도구에 보내지 않습니다.

콘텐츠에서 정보 배치를 추론합니다(예: 순서, 비교, 중심
장면 또는 그룹화된 사실). 선택 참조의 세 번째 라운드에서 구체적인
배치를 스타일 선택지 및 목표 종횡비와 함께 보여주고, 미확정 스타일·종횡비 선택을
생성 전에 확인합니다. 이 확인은 독립 F3 그림의 미확정 축에 적용합니다. 기본 설명 페이지 안의 한 장은 이미 선택·위임받은 페이지 구성을 재사용하고 그에 맞는 배치·스타일·종횡비를 알려 진행하며 별도의 세 번째 이미지 질문을 추가하지 않습니다. 사용자가 그림의 스타일·종횡비를 지정했다면 그대로 보존합니다. 내부 배치 이름을 다른 축으로 질문하지 않습니다. 명시적인 스타일,
종횡비 또는 위임된 `알아서` 선택은 이미 확정된 것입니다. 모든 축이 지정되어 있다면
추론한 배치×스타일·종횡비를 알리고 진행합니다. 이는 원본의 Step 4를 사용자의
순차 선택 계약에 맞게 조정한 것이며, 두 번째 승인 절차나 고정된 기본 조합이 아닙니다.
손그림 캐릭터 일러스트레이션, 절제된 그래픽 표현,
채색 동화책 또는 기술 일러스트레이션처럼 적합한 선택지를 사용합니다. 그러한 스타일이 사실상의 축척을 입증한다고 암시하지 않습니다.

<a id="save-the-prompt-then-generate"></a>
## 프롬프트를 저장한 뒤 생성한다

이미지 도구를 호출할 때마다 호출 전에 실행의 `prompts/` 아래에 새 독립형 프롬프트 파일을 만듭니다.
아래 프롬프트 틀을 사용합니다. 사양(배치,
스타일, 종횡비, 언어), 핵심 제약, 텍스트 요구 사항, 배치·스타일 지침,
구조화된 콘텐츠와 완전하고 정확한 라벨 목록을 포함합니다. 모든 필드를 채우고, 저장한
프롬프트의 전체 내용과 확인된 참조 이미지·종횡비를 실제 계약에 따라 런타임 네이티브 이미지
생성 도구에 전달합니다. 필수 라이선스·자산 출처 표시를 유지합니다.
캐시된 백엔드 명령을 복사하거나 이 경로의 일부로 생성기를 설치하지 않습니다.

이미지 생성 도구를 이용할 수 없다면 빠진 기능과 확인한 범위를 밝힙니다. 먼저 위 틀을 모두 채운 baoyu식 프롬프트를 저장·제공하고 실제 이미지 도구에서 생성하는 것을 우선 권장합니다. 승인된 파일 제작 범위에서 같은 근거를 담은 독립 SVG를 PNG로 실제 변환해 함께 제공하고 페이지에는 그 PNG 한 장만 넣습니다. 캡션과 전달 설명에 `임시 대체물, baoyu 생성본 아님`을 명시합니다. 변환 도구도 없으면 프롬프트와 해당 차단만 제공하며 PNG 완료를 주장하지 않습니다.
AI 래스터 생성 요구는 계속 `Blocked`/`Unverifiable`로 보고합니다. 페이지·대체 PNG를 만들었다는 사실과 미충족 AI 일러스트레이션을 분리하며 전체 성공으로 합치지 않습니다. HTML/SVG나 변환 PNG를 생성 래스터의 성공으로 처리하지 않고 조용히 설치·백엔드 우회하지 않습니다. 생성 실패를 정직하게 보고하며 재시도 때 이전 후보 파일을 유지합니다.
도구가 출력 보존을 담당하면 이미지 바이트를 재구성하지 말고 그 수명주기를
따릅니다. 실제 도구 계약과 요청된 산출물이 요구할 때만 로컬 사본을 저장합니다.

<a id="check-final-pixels-and-facts"></a>
## 최종 픽셀과 사실을 확인한다

의도한 읽기 크기에서 실제 래스터를 확인합니다. 모든 라벨, 숫자 문자열,
단위, 관계, 조건과 강조를 구조화된 원본 콘텐츠에 대조합니다. `change`의 기본
독립 검토를 포함하여 요약 PNG와 동일한
출처·작성자·독립 정확성 검토 정책을 적용합니다. 정확한 최종 이미지와 근거 및 라벨 목록을 사용합니다.
`visible_text.py`는 픽셀을 추출할 수 없으며 이미지 정확성 판정도 아닙니다.

텍스트가 틀리거나 읽을 수 없거나 빠져 있으면 프롬프트를 수정하고 새 프롬프트·이미지
경로에 다시 생성합니다. SVG, Pillow 또는
canvas 오버레이를 포함하여 프로그램으로 텍스트를 덧칠하거나 지우거나 다시 쓰지 않습니다.
결함이 있는 후보는 진단 근거로 비공개 보존합니다. 자르기·크기 조정·
압축으로 텍스트나 의미를 바꾸어서는 안 되며, 필수 검토는 그 결과인 최종 바이트에 결합합니다.
도구가 실패하거나 중요한 그림을 확인하지 않았다면 `Pass`를 부여할 수 없습니다. 실제 래스터,
대체 설명, 선택된 배치·스타일·종횡비와 사실에 맞는 검사 결과를 전달합니다. 발행 권한은 부여되지 않습니다.

이는 런타임 네이티브 도구에 맞게 조정한 경로이며, upstream 스킬이나 그 백엔드 또는
전체 스타일 갤러리를 실행했다는 주장이 아닙니다. 네 가지 HTML/SVG 원칙은 서로 구별되는 조정 방식으로 유지합니다.

<a id="prompt-skeleton"></a>
## 프롬프트 틀

생성 전에 이 완전한 템플릿을 실행 소유 프롬프트 파일에 채웁니다.

```markdown
# Image specifications

- Type: AI-illustrated infographic
- Layout: <content-driven composition and reading order>
- Style: <confirmed visual treatment, characters and line/texture choices>
- Aspect ratio: <confirmed W:H>
- Language: <reader language>

## Core constraints

<Source-bound conclusion, conditions and limits. No invented facts, measurements or causal links.>

## Text requirements

<Legible text at the intended display size; preserve exact numeric strings and label wording.>

## Layout guidelines

<Section positions, verified relationships, sequence and grouping; keep source order where material.>

## Style guidelines

<Confirmed style treatment without decorative scale or causality claims.>

## Structured content

<Reader objective, necessary prerequisites, mechanism, grounded facts and caveats.>

## Exact text labels

<Complete label/title/value list in the selected language, with source bindings in the private evidence.>
```
