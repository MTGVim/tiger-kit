<a id="illustration-presets"></a>
# 용도별 프리셋

프리셋을 지정했거나 추천할 때 읽습니다. 프리셋은 다음 축의 축약이며 개별 명시 옵션이 항상 우선합니다. `mode`, 레이아웃·비율·이미지 수는 결정하지 않습니다. 팔레트의 `기본`은 해당 스타일의 기본 색상을 뜻합니다. 정보 구조와 목적이 같으면 상위 요청의 이미 확정된 값을 재질문하지 않습니다.

| 프리셋 | 타입 | 스타일 | 팔레트 |
| --- | --- | --- | --- |
| `tech-explainer` | `infographic` | `blueprint` | 기본 |
| `system-design` | `framework` | `blueprint` | 기본 |
| `architecture` | `framework` | `vector-illustration` | 기본 |
| `science-paper` | `infographic` | `scientific` | 기본 |
| `knowledge-base` | `infographic` | `vector-illustration` | 기본 |
| `saas-guide` | `infographic` | `notion` | 기본 |
| `tutorial` | `flowchart` | `vector-illustration` | 기본 |
| `process-flow` | `flowchart` | `notion` | 기본 |
| `warm-knowledge` | `infographic` | `vector-illustration` | `warm` |
| `edu-visual` | `infographic` | `vector-illustration` | `macaron` |
| `hand-drawn-edu` | `infographic` | `sketch-notes` | `macaron` |
| `hand-drawn-edu-flow` | `flowchart` | `sketch-notes` | `macaron` |
| `hand-drawn-edu-compare` | `comparison` | `sketch-notes` | `macaron` |
| `ink-notes-compare` | `comparison` | `ink-notes` | `mono-ink` |
| `ink-notes-flow` | `flowchart` | `ink-notes` | `mono-ink` |
| `ink-notes-framework` | `framework` | `ink-notes` | `mono-ink` |
| `data-report` | `infographic` | `editorial` | 기본 |
| `versus` | `comparison` | `vector-illustration` | 기본 |
| `business-compare` | `comparison` | `elegant` | 기본 |
| `storytelling` | `scene` | `warm` | 기본 |
| `lifestyle` | `scene` | `watercolor` | 기본 |
| `history` | `timeline` | `elegant` | 기본 |
| `evolution` | `timeline` | `warm` | 기본 |
| `opinion-piece` | `scene` | `screen-print` | 기본 |
| `editorial-poster` | `comparison` | `screen-print` | 기본 |
| `cinematic` | `scene` | `screen-print` | 기본 |

`--preset tech-explainer --style notion`은 `infographic + notion`입니다. `--style hand-drawn-edu`는 같은 이름의 프리셋과 다르며 해당 스타일 카드를 그대로 선택합니다. 프리셋 이름으로 출판 품질·학술 정확성·제공자 기능을 보장하지 않습니다. 실제 수치 차트나 정확한 도해가 필요한 `science-paper/data-report` 요청에는 정적 제작 경로를 우선 제안합니다.
