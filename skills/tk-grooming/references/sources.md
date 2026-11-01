<a id="grooming-source-dispositions"></a>
# Grooming 출처별 판단

<a id="model-fit-audit"></a>
## 모델 적합성 감사

`anthropics/skills`의 `683bc88e56f3e09ba94f7055977f3d3aa499f202`에서
`skills/claude-api/shared/prompt-audit.md`, 그 안의 설계 이유와 검증 절차,
그리고 `skills/claude-api/shared/model-migration.md`의 대상 모델 절을 검토했습니다.
출처는 Apache-2.0이며 비교 자료입니다. 가져와 포함한 텍스트나 런타임 코드가 아닙니다.
prompt-audit의 별도 upstream 동작 평가 결과는 `unverified`입니다.

- `keep`: 대상에 따른 근거, 작성자 맥락과 순서 등에 민감한 계약의 보존, 확신도를 명시한 관찰과 유효한 문제없음·변경 없음 결과를 유지합니다.
- `adapt`: 압박, 출력 제한, 버전 상대적 문장, 런타임 이력, 오래된 사실, 충돌하는 지침, 정확한 문구 모드와 오래된 평가 기대를 기존 GR 발견 사항으로 전환합니다. 명시적인 사용자 형식은 계속 구속력을 가집니다. 모델별 주장에는 최신 1차 근거가 필요합니다. 기존 소유권과 기계적·의미적 권한 구분이 행동을 결정합니다.
- `adapt`: 출처는 조건부 유지보수 기록으로 두고, 동작 비교는 기존 지침 경제성 참조에서 계속 담당합니다. 충돌은 Git 최신성과 관계없이 보류합니다.
- `omit`: 애플리케이션·API 이전, 요청 builder, 도구 description 감사, 모델 라우팅, 자동 광범위 목록 조사, 필수 보고·diff 산출물과 upstream 구현·fixture를 제외합니다.

TigerKit의 구체적인 부족은 임의적인 출력 제한과 서로 다른 패키지 내부 계약이었습니다.
이 분기는 호출 종류, description, vendor 소유권이나 기존 적용 경계를 바꾸지 않고 대상 모델
분류를 추가합니다. 로컬 사례는 이전 동작과 후보 동작을 비교하며, 모든 대상 모델에서의 효과를
입증하지는 않습니다.

<a id="external-behavior-copies-and-usage-evidence"></a>
## 외부 동작 사본과 사용 근거

유지보수 보고서는 구체적이며 독립적으로 확인한 감사 결과 두 가지를 제공했습니다.
네이티브 실행 진단에서는 비활성 스킬을 찾았지만, 맥락이 없는 grooming 감사에서는 경로·lock·내용을
사용하여 새로운 비활성을 찾지 못했습니다. 현재 변경 전 Workflow,
`instruction-economy.md`와 `discovery.md`의
`26890b22bccb54a02f681ac621082a9930dff61c` 내용은 사용 근거 분기와 의도적인
외부 동작 사본의 기준판·설치판 비교가 없음을 확인해 줍니다. 이는 검증된 재사용 가능한 사고 사례이며,
새 upstream 구현 의존성이 아닙니다. 원래 호스트의 비공개 counter, plugin 내부와 진단 구현은
여기서 `unverified`로 남습니다. 호스트별 counter 경로나 schema를 단정하지 않습니다.

- `keep`: 조회 비용이 커서 의도적으로 만든 사본, 현재 호스트만의 탐색, 기존 보고 전용 호스트 설정·vendor 경계와 영속 TigerKit registry를 두지 않는 원칙을 유지합니다.
- `adapt`: 버전 출처와 설치 규칙 비교를 지침 경제성 안에 두고, 사용 의미와 관찰 범위는 범위별 참조 pointer 하나 뒤에 둡니다.
- `omit`: 모델 라우팅, 원시 세션 데이터, telemetry 수집, 자동 비활성화, 추측한 counter schema와 호스트 간 런타임을 제외합니다. 합성 평가 사례는 원래 환경의 세부사항을 공개하지 않고 결정 경계를 시험합니다.
