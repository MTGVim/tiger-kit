# 문서 갱신 절차와 문서 전용 감사

`README: no public change`

영향 경로: `skills/tk-prep/SKILL.md`, `skills/tk-prep/references/local-execution.md`,
`skills/tk-audit/SKILL.md`, `skills/tk-audit/references/audit-playbook.md`,
`skills/tk-audit/references/work-discovery.md`, `skills/tk-audit/references/documentation.md`,
`skills/tk-audit/references/executor-handoff.md`,
`evals/skills/tk-prep/evals.json`, `evals/skills/tk-audit/evals.json`,
`evals/skills/tk-audit/triggers.json`, `evals/skills/tk-audit/fixtures/documentation.md`,
`evals/release-critical.json`.

기존 명시 호출 방식과 카탈로그 설명을 유지하며, `tk-audit` 범주 인자에 `docs`를 추가합니다.
README는 공개 진입점과 한 줄 설명을 이미 정확하게 안내하므로 상세 범주를 복제하지 않습니다.

## 근거와 선택

사용자가 제공한 2026-10-19 회고의 F3·F4만 반영합니다. 보류된 F1·F2는 바꾸지 않습니다.
`tk-prep`이 저장소 문서 절차와 충돌하던 제한을 제거하고 좁은 선택적 검색을 허용합니다.
내부 변경만 있고 저장소 절차가 없다면 문서 검사를 생략하며, 정확한 문장·생성기·지침 파일 경계를 보존합니다.
기존 `prep-unknown-document-owner-skips-broad-search` 평가만 명시적으로 이관하여
전수 검색 금지를 유지하면서 좁은 검색을 허용합니다.

`tk-audit`는 현재 상류 `shadcn/improve`의 고정 커밋
`cac56e1ebd3c279aa9153616cfeac7b174ab90f9`에서 본문·감사 가이드와 저장소 트리를 확인했습니다.
상류의 읽기 전용 경계와 증거·범주별 감사는 유지하고, 포괄적인 문서 범주를
본문·메타데이터·테스트·평가를 대조하는 절차는 조건부 참조가 소유하도록 조정합니다. 상류의 계획 수명주기와
실행 위임·이슈 발행 기능은 기존 TigerKit 경계에 맞춰 제외합니다.
전용 문서 대조의 효과를 입증하는 상류 평가는 확인하지 못했으므로 효과의 근거로 삼지 않습니다.
사용자 회고의 비교 실행은 예비 실험의 근거이며, 이번 변경에서 같은 검출량이나 시간 효과를 주장하지 않습니다.

상시 참조에는 분기 선택만 추가합니다. `docs` 분기 선택 문장을 빼면 문서 전용 대조가
선택되지 않고, 일반 감사 보존 문장을 빼면 회고에서 관찰한 범주 편중을 막는 경계가 없어집니다.
`next` 연결은 문서 기반 부재를 결함으로 잘못 분류하지 않고 최소 제안으로 보내는 역할을 합니다.
세부 절차는 새 조건부 참조 한 개가 소유하며 일반 감사에서 전체 대조를 실행하지 않습니다.

버전별 도구 로딩 규칙, 근거 없는 가이드 개수, 획일적인 휴면 기간, 새 경로 검사기 구현은 제외합니다.
현재 도구의 로딩 조건을 확인하고 실제 탐색 비용과 변경 이력으로 판단합니다.
이름 이관은 자동 제안하지 않고 도구별 진입점이 필요한지 확인하도록 합니다.
테이블 형식 자체를 완결 목록의 증거로 취급하지 않으며, 경로 검사로 의미상 문서 표류를
검출한다고 주장하지 않습니다. #224의 지침 파일 직접 수정 금지는 유지합니다.


독립 검수에서 찾은 원격 커밋에만 있는 근거와 HEAD 검증 규칙의 충돌을 수정했습니다.
비교 SHA를 발견에 고정하고 저장 전 참조 이동은 기존 사전 검사에서 중단하며, 인계에서도
실제 구현 대상에 재검증합니다. 호출 안내의 `argument-hint`에도 `docs`를 포함했습니다.
