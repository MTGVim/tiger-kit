# 런타임 검증 불편 개선

기준: `MTGVim/tiger-kit` `main` `92364e8a1e0e8ab1f565623dbf7bc7c755ae89a7`.
범위: 사용자가 보고한 검증 세션 후속 수정. 새 런타임 재현이나 `macOS` 자원 측정은 수행하지 않았다.

## 변경 내용

- `skills/tk-prep/SKILL.md`, `skills/tk-prep/references/repository-context.md`: 구조화된 사용자 관리 `verificationDataPolicy`가 정확한 QA/`dev` 범위를 허용하면 `policy-file authority`로 기록하고 재질문하지 않는다. 되돌릴 수 없다고 분류하기 전에 원복 경로를 확인한다.
- `skills/tk-browser-verify/references/safety.md`: 구조화 정책의 권한 범위를 확인하며 원복·잔여 부작용 확인과 운영 데이터 경계를 보존한다.
- `skills/tk-browser-verify/references/behavior.md`: 기본 드래그, 헤드리스 기본 선택 상자 우회와 날짜 선택기 입력 방법을 안내한다.
- `skills/tk-browser-verify/references/environment.md`: 같은 세션에서 같은 형식의 비밀 입력을 반복 요청할 때 이유와 절대경로만 표시한다.
- `skills/tk-qa-sheet/SKILL.md`, `skills/tk-qa-sheet/references/qa-sheet-data.md`: 현재 권한으로 실행 가능한 미실행 행과 데이터 변경이 필요한 행 수를 구분한다. 편집 행이 두 개보다 적을 때 자체 점검 기준을 적용하고, 승인된 저장 결과 증거를 자동 확인으로 인정한다.
- `skills/tk-retro/SKILL.md`: 상세 처분은 보고서에 두고 대화 응답은 핵심 발견과 보고서 경로로 제한한다.
- `scripts/sync_execution_protocol.py` 및 공용 블록 복사본: 경로를 완전한 절대경로로 표시하고 생략 부호로 줄이지 않는다.

평가 계약을 `tk-prep`, `tk-browser-verify`, `tk-qa-sheet`, `tk-retro`에 추가했다.

## README 판정

`README: no public change`

스킬 이름, 호출 방식, 카탈로그 설명은 바뀌지 않았다. 변경한 설명은 각 스킬 내부의 절차와 출력 규칙이다. 아래 공개 계약이 있는 스킬 파일을 포함해 공용 경로 표기 블록 소비처를 동기화했다.

- `skills/tk-prep/SKILL.md`
- `skills/tk-qa-sheet/SKILL.md`
- `skills/tk-retro/SKILL.md`
- `skills/tk-browser-verify/references/safety.md`
- `skills/tk-prep/references/repository-context.md`

## 보존 경계

운영 데이터 변경, 기존 데이터 삭제, 결제, 외부 발송, 계정·권한 변경, 채팅을 통한 비밀 입력, QA 시트 자동 실행을 허용하지 않는다. 추적형 팀 설정의 자유 문구는 권한을 부여하지 않는다. 구조화 `verificationDataPolicy`만 정확히 일치하는 비운영 작업에 한해 제한된 권한을 부여한다. 원복은 복구 및 비교 경로가 확인된 경우에만 인정하며 잔여 효과를 공개한다.

## 검증 한계

정적 검사와 릴리즈 체크리스트는 지침, 링크, 평가 계약과 설치 결과를 검사한다. 실제 브라우저 제공자에서 드래그와 선택 상자가 동작하는지, 토큰 왕복이 줄어드는지는 입증하지 않는다. `macOS` 부하 재현은 하지 않았다.
