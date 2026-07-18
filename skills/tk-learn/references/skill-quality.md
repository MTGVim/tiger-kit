# 스킬 품질

명확한 이름, 범위가 좁고 명확한 설명, 입력, 핵심 동작, 경계, 완료 기준, 최소 출력 형식을 요구하세요. 디렉터리를 자체 완결적으로 유지하세요. 간결한 지침을 우선하고, 반복되는 누락, 비용이 큰 순서 오류, 변경 안전성, 객관적인 완료 증명, 전문 절차 또는 제한된 위임/검토를 위해서만 세부 내용을 추가하세요.

## 승격 gate

- 최소 두 개의 독립된 반복 사례 또는 재사용 가능한 워크플로와 이를 뒷받침하는 artifact가 있어야 합니다. 출처 없는 주장과 단일 일회성 사례는 threshold 미달입니다.
- 기존 skill과의 중복, 기본 모델 기능으로 대체 가능한지, 짧은 rule로 충분한지를 먼저 검사합니다. 중복이면 새 디렉터리보다 `merge` 또는 `no-op`을 우선합니다.
- Positive와 negative trigger를 실제로 구별되는 문장으로 제시하고 description 개선용 train과 회귀 판정용 validation을 분리합니다. Trigger가 불명확하면 생성하지 않습니다.
- 최소 하나의 success와 하나의 boundary/failure behavior eval에 observable assertion을 포함하되, 원시 secret·credential·로그·screenshot을 그대로 저장하지 않습니다.
- 이전 skill, no-skill 또는 명시된 baseline과 비교할 방법을 적습니다. 단일 prose 점수만으로 승격하지 않습니다.
- Agent Skills portable core field와 target host에 필요한 extension을 구분하고, host별 body copy를 만들지 않습니다. Target host에서 invocation 경계를 검증할 수 없으면 `pending`으로 둡니다.
- 사용자 승인 전 후보는 `reported` 또는 `pending`이며 파일 적용은 하지 않습니다. 승인 후에만 `applied`로 receipt를 남깁니다.
