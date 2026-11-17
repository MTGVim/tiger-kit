# GPT-6.2 Sol 출시와 TigerKit 맵 검토

**조사 날짜: 2026-11-18**. OpenAI는 2026-11-17 GPT-6.2 Sol을 발표했습니다. 아래 자료는 [Artificial Analysis GPT-6.1 Sol](https://artificialanalysis.ai/models/gpt-6-1-sol)과 [GPT-6.2 Sol](https://artificialanalysis.ai/models/gpt-6-2-sol/)의 Intelligence Index v5.0.1에 근거합니다.

| effort | 6.1 점수 | 6.2 점수 | 6.1 작업 시간(분) | 6.2 작업 시간(분) |
| --- | ---: | ---: | ---: | ---: |
| low | 35 | 41 | 1.9 | 1.4 |
| medium | 46 | 53 | 4.3 | 3.1 |
| high | 50 | 55 | 7.4 | 4.3 |
| xhigh | 52 | 56 | 9.7 | 5.1 |
| max | 55 | 57 | 23.1 | 7.9 |

두 버전의 API 가격은 입력 $2, 출력 $10 / 100만 토큰으로 동일합니다. **Max**의 Intelligence Index 실제 작업당 비용은 6.1 Sol $1.27, 6.2 Sol $1.01입니다. 이 수치를 다른 effort에 전용하지 않습니다.

[Artificial Analysis 출시 분석](https://artificialanalysis.ai/es/articles/openai-has-the-2-model-in-the-intelligence-index-with-the-release-of-gpt-6-2-astra-and-gpt-6-2-sol)에 따르면 **Coding Agent Index의 max 설정은 신형이 3점 낮습니다.** 원인의 하나로 SWE-Atlas-QnA-AA 14점 하락을 지목했습니다. medium의 코딩 성능까지 동일하게 낮다고 단정하지 않습니다.

## 맵 적용 결정

**기존 standard/economy의 OpenAI top 기본값(`sol`, `medium`)과 Hermes에서 실제 시험한 `gpt-6.1-sol`을 자동 교체하지 않습니다.** 연구·설계 목적의 `gpt-6.2-sol` / `medium`은 실험 후보입니다. 코딩 관련 top 위임에는 별도 코딩 성능과 호스트 실효값을 비교해야 합니다.

현재 공개 자료에서 GPT-6.2 Sol의 **모든 effort별 작업당 비용**을 원본 숫자로 확인하지 못했습니다. 기존 `benchmarks.json`의 `[비용, 점수]` 필드를 일부 임의 보간하거나 전날의 `sol` 별칭을 새 버전에 재연결하면 `derive`의 비용·성능 비교가 왜곡됩니다. 그러므로 번들 계산용 테이블은 보존합니다. 신형이 본인 호스트에서 지원되는 정확한 ID와 effort인지, 비용과 코딩 평가가 비교 가능한지 확인한 후 `update`와 사용자 승인으로 맵을 재산출합니다.

이 판단은 새 모델을 사용하지 말라는 뜻이 아니라 **측정 가능한 근거 없이 기본값을 바꾸지 않는다는 의미**입니다.
