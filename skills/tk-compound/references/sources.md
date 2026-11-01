<a id="source-dispositions"></a>
# 출처별 채택 판단

2026-10-13에 `EveryInc/compound-engineering-plugin@50532b00de523980010d97fe950965b35382a3b7`
(MIT)의 `docs/guides/ce-compound.md`, `skills/ce-compound/SKILL.md`와
`skills/ce-compound/references/grounding-validation.md`를 검토했습니다. 안내와 구현 근거는
확인했지만 upstream 런타임과 별도의 행동 효과는 검증하지 않았습니다.

- `keep`: 재발 방지는 기존 코드/테스트를 넘어서는 실질적 지식을 더해야 합니다. 가장 좁고 효과적인
  소유자를 우선하며 주장/revision 출처와 내부 집계를 확인합니다.
- `adapt`: 범위가 제한되고 명시적으로 요청된 저장소 진단에서 완료된 PR 전반의 과거 주장, 수정과
  현재 보호 장치를 비교합니다. 기존 지침 준수 실패에는 지침을 다시 복사하는 대신 인과 근거가 필요합니다.
- `omit`: 자동 세션 완료 기록, `docs/solutions/`, `CONCEPTS.md`, pack 뼈대 생성,
  광범위한 세션 이력 탐색, 자동 문서/색인 편집, corpus 수명주기와 subagent 런타임은 제외합니다.

TigerKit 이슈 #224, #346과 #368과의 호환성은 유지됩니다. 메모리/규칙 수명주기를 도입하지 않고,
기계적 재발 방지를 우선하며 지식 제안은 프로젝트 고유 방식으로 유지합니다. 이슈 #455는 명시적인
재사용 워크플로와 구체적인 반복 리뷰 실패를 제공합니다. 단일 세션 사건은 `tk-retro`가, 기존 지침
정비는 `tk-grooming`이, 도메인/ADR 작성은 `tk-domain`이 소유합니다. 이슈의 이전 `tk-learn`
이름은 과거 명칭이며, 현재 승인된 구현 담당자가 변경을 소유합니다.
원본 MIT 고지는 이 패키지의 `LICENSE.txt`에 보존되어 있습니다.
