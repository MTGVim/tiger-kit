# 옵션과 제작 조합

옵션을 해석하거나 추천할 때 읽습니다. 다음은 대화형 스킬의 인자 계약이며 별도의 CLI나 이미지 실행기를 제공한다는 뜻이 아닙니다. 명시 옵션 → 선택 프리셋 → 근거에 맞는 미지정 축의 순서로 결정합니다. 이전 패키지를 재개하면 저장된 값을 먼저 보존합니다. 알 수 없는 옵션·중복 충돌·잘못된 값을 조용히 무시하지 않습니다.

| 옵션 | 지원 값과 의미 |
| --- | --- |
| `--art` | `ligne-claire`, `manga`, `realistic`, `ink-brush`, `chalk`, `minimalist` |
| `--tone` | `neutral`, `warm`, `dramatic`, `romantic`, `energetic`, `vintage`, `action` |
| `--layout` | `standard`, `cinematic`, `dense`, `splash`, `mixed`, `webtoon`, `four-panel` |
| `--preset` | `ohmsha`, `four-panel`, `concept-story`, `wuxia`, `shoujo` |
| `--aspect` | 양의 `width:height` 비율입니다. 실제 도구 지원을 확인하며 예시는 `3:4`, `4:3`, `16:9`입니다. 미지원 비율을 다른 값으로 조용히 바꾸지 않습니다. |
| `--pages N` | 양의 정수인 본문 페이지 수입니다. 표지는 별도 요청한 경우에만 ID `0`으로 추가하며 N에 포함하지 않습니다. |
| `--lang` | 결과물 언어입니다. `auto` 또는 미지정이면 현재 대화 언어를 사용하고, 불명확할 때 원문 언어를 참고합니다. |
| `--ref <files...>` | 실제 사용자 참조 이미지입니다. `direct`, `style`, `palette` 용도를 기록하며 `direct`를 텍스트로 대체하지 않습니다. |
| `--batch-size N` | 양의 정수이며 호스트의 실제 동시 호출 한도 이내에서 사용합니다. 미지정이면 현재 지원과 의존성에 맞추고 지원이 없으면 순차 생성합니다. |
| `--storyboard-only` | 근거·outline·콘티·필요한 캐릭터 정의까지 만들고 프롬프트와 이미지는 생성하지 않습니다. |
| `--prompts-only` | 콘티와 완전한 최종 프롬프트까지 만들며 이미지는 생성하지 않습니다. |
| `--images-only` | 기존 유효한 콘티·프롬프트에서 아직 완료되지 않은 이미지를 생성합니다. 이미 검증된 결과는 보존합니다. |
| `--regenerate N[,M...]` | 존재하는 페이지 ID만 재생성합니다. `0`은 패키지에 실제 표지가 있을 때만 허용합니다. |
| `--no-confirm` | 명시한 주제·제작 목표 안의 미지정 표현 축을 위임합니다. 새 비용·외부 행위·덮어쓰기 승인은 대신하지 않습니다. |

부분 실행 플래그는 하나만 선택합니다. 예를 들어 `--prompts-only --images-only`는 모순이며 실행 전에 해소합니다. 페이지·batch 값에 소수, 음수, 0, 빈 목록이나 존재하지 않는 ID를 허용하지 않습니다. 알 수 없는 항목을 임의 프리셋으로 정규화하지 않습니다.

## 선택한 참조만 읽기

확정된 축에 대응하는 파일만 읽고, 전체 카탈로그를 선로드하지 않습니다. 아래 경로는 이름이 지원 목록에 있는지 확인한 다음 현재 설치된 이 패키지를 기준으로 해석합니다. 임의 경로를 옵션으로 받아 읽지 않습니다.

- 표현: `references/art-styles/<art>.md`
- 톤: `references/tones/<tone>.md`
- 레이아웃: `references/layouts/<layout>.md`
- 프리셋: `references/presets/<preset>.md`

## 추천과 충돌 처리

| 정보 구조 | 검토할 조합 | 한계 |
| --- | --- | --- |
| 조작·과정으로 배울 기술 개념 | `ohmsha`, `manga + neutral + webtoon`, `3:4` | 실제 기술 조건을 비유에서 누락하지 않습니다. |
| 한 번의 오해와 발견 | `four-panel`, `minimalist + neutral + four-panel`, `4:3` | 한 페이지 네 컷에 담기지 않는 내용은 줄이지 말고 다른 조합을 검토합니다. |
| 여러 장면에서 쌓이는 이해·습관 변화 | `concept-story`, `manga + warm + standard`, `3:4` | 성장을 장면으로 보여 주며 긴 설명 대사에 의존하지 않습니다. |
| 역사적 기술·인물 | `realistic + vintage + cinematic`, `4:3` | 자료로 확인한 시대·복장과 창작 연출을 구분합니다. |
| 역동적인 비교 비유 | `wuxia`, `ink-brush + action + splash`, `3:4` | 액션 효과가 기술적 인과 관계를 대신하지 않습니다. |
| 관계·감정이 이해의 핵심인 서사 | `shoujo`, `manga + romantic + standard`, `3:4` | 장식이 정보나 말풍선을 가리지 않게 합니다. |

위 표는 고정 기본값이 아닙니다. 주제와 독자에 맞는 세 조합을 구성합니다. `ligne-claire`는 `neutral/warm`, `manga`는 `neutral/romantic/energetic/action`, `realistic`는 `neutral/warm/dramatic/vintage`, `ink-brush`는 `dramatic/vintage/action`, `chalk`는 `neutral/warm/energetic`, `minimalist`는 `neutral`과 잘 맞습니다. 미감상의 낮은 적합도는 금지 규칙이 아니므로 사용자의 명시 조합을 보존하고 가독성 한계만 설명합니다.

개별 값은 프리셋의 기본 축보다 우선합니다. 다만 `four-panel` 프리셋의 한 페이지·네 컷처럼 정체성을 정하는 규칙과 `--pages 4` 또는 `--layout webtoon`이 충돌하면 한쪽을 조용히 버리지 않습니다. 여러 독립 네 컷 작품, 일반 four-panel 레이아웃의 연속 만화, 다른 프리셋 중 사용자가 의도한 결과만 확인합니다. `--layout four-panel` 자체는 페이지당 네 컷을 뜻하며 프리셋의 한 페이지 서사 제한을 자동으로 추가하지 않습니다.
