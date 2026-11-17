# 선정 원칙

## 비용 및 점수 비교

같은 공급자 안에서 비용이 같거나 낮고 점수가 같거나 높으면서 적어도 한 축이 더 나은 칸이 있으면 지배된 칸입니다. validate는 [번들 벤치마크](benchmarks.json)에서 이를 경고하며 선택을 차단하지 않습니다. 미확인 모델이나 effort는 비교할 수 없다고 보고합니다.

번들 수치는 2026-11-17 대화의 인용값을 재구성했으며 원본 대조는 unverified입니다. 해당 자료에서는 Sonnet medium보다 Haiku max의 점수가 높고 비용이 낮았습니다. Terra xhigh/max, Sonnet xhigh/max 등은 같은 공급자의 최상위 모델과 비교할 필요가 있습니다. 지능 점수와 코딩 벤치마크는 서로 다른 측정입니다.

## 도출 규칙

- standard 모드의 light는 경량 모델 low, top은 최상위 모델 medium에서 시작합니다.
- standard 티어는 상위 모델 medium에서 시작합니다. 지배된 칸이면 같은 모델의 high까지 확인합니다. 그래도 지배되면 같은 비용 이하에서 점수가 가장 높은 대체 칸을 사용합니다.
- economy는 standard 티어에 선택된 모델의 effort를 한 단계 낮춘 뒤 같은 비용 이하에서 점수가 가장 높은 비지배 대안을 확인합니다. light와 top은 유지합니다.
- 필요한 벤치마크 칸이 누락되면 추정하지 않고 도출을 중단합니다.
- 사용자 모드는 extends로 기존 모드를 상속하고 변경할 칸만 지정합니다. 경고는 대안을 설명하며 최종 선택은 사용자에게 있습니다.

## 승격과 설정

개별 작업의 승격은 [공통 위임 계약](../../tk-engineering/references/delegation.md)이 정합니다. standard는 high까지 높이고 더 필요하면 top으로 승격합니다. light 상한은 공급자별 대응표에서 정합니다. 명시된 사용자 effort 초기값이 공통 표보다 우선합니다.


최상위 위임 티어의 초기 effort는 [위임 역할 표](../../tk-engineering/references/delegation.md)의 아키텍처·미지 문제 탐사 행을 근거로 정합니다. 해당 행의 초기값은 미검증이므로 기존 medium 도출값은 잠정 유지합니다. 원본 벤치마크 대조 전에는 high로 변경하지 않으며 economy의 top도 유지합니다.
