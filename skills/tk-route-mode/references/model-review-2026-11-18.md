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

[Artificial Analysis 출시 분석](https://artificialanalysis.ai/articles/openai-has-the-2-model-in-the-intelligence-index-with-the-release-of-gpt-6-2-astra-and-gpt-6-2-sol/)에 따르면 **Coding Agent Index의 max 설정은 신형이 3점 낮습니다.** 원인의 하나로 SWE-Atlas-QnA-AA 14점 하락을 지목했습니다. medium의 코딩 성능까지 동일하게 낮다고 단정하지 않습니다.

## 최신 버전 우선 적용 결정

**2026-11-18 당시 신규 기본 대응표의 OpenAI top은 `gpt-6.2-sol` / `medium`입니다.** GPT-6.2 Sol은 기존 6.1과 API 토큰 가격이 같고, 동일 effort에서 종합 지능과 작업시간이 개선됐습니다. Coding Agent Index의 max effort 3점 하락은 주의 신호이지만, medium에서의 중대한 코딩 회귀까지 입증하지는 않습니다. 신형 출시 후 구버전을 기본으로 고정하는 정책의 향후 이전 비용도 함께 고려합니다.

공식 [OpenAI API 지원 종료 안내](https://developers.openai.com/api/docs/deprecations)에는 **2026-11-18 기준 GPT-6.1 Sol의 Deprecated 또는 Shutdown 일정이 공지되지 않았습니다.** 최신 버전이 존재한다는 사실과 공식적인 지원 중단을 구분합니다. 공식 수명주기는 Active / Deprecated / Shutdown으로 나누며, 일반 출시 모델에는 원칙적으로 최소 6개월의 종료 사전 통지가 제공됩니다.

현재 공개 자료에서 GPT-6.2 Sol의 **모든 effort별 작업당 비용**은 확인하지 못했습니다. 따라서 당시 번들 `benchmarks.json`에는 `gpt-6.1-sol`의 역사적 측정값만 기록했습니다. 이 정적 파일은 단일 대응표 전환 시 제거했으며 신형 수치를 추정하지 않습니다. 그러나 이 결측만으로 최신 버전의 기본 채택을 무기한 보류하지 않습니다. 현재 정책에서는 자동 선정 함수 `derive`를 폐기했습니다. 이후 호출에서는 당시 결론을 고정 추천으로 사용하지 않고 최신 코딩 에이전트 실측을 다시 확인합니다.

변경은 **새 기본 대응표에만 해당**합니다. 기존 사용자의 저장된 설정, 수동 override, Hermes·Codex·Claude Code 프로필을 자동 변경하지 않습니다. 실제 호스트가 `gpt-6.2-sol`과 `medium`을 지원하는지 확인하고 승인받은 뒤 적용·검증합니다. 작업에서 재현되는 중대한 회귀가 확인되면 그 작업에 한정해 구버전을 예외로 유지하고 재평가 기준을 기록합니다.
