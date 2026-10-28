# 설명 스킬 통합과 블라인드 자료 확장

첨부된 7회 소규모 비교의 반복 관찰을 검토하고 기본 설명을 `archify` `explainer`로 통합했습니다.
평가자 1명의 선호를 일반적인 학습 효과나 통계적 우월성으로 확대하지 않습니다.

- `tk-explain`은 개념·변경·실제 답변 후속을 담당합니다. 근거 고정, 장면 `PNG` 선택,
  조건부 독립 검토와 필수 재검토는 소유 본문 및 조건부 참조에 둡니다.
- 이전 변경 설명·수업 패키지는 실제로 폐기합니다. 두 패키지의 전용 생성기·평가도 폐기하며,
  남는 근거·학습자 판정은 새 평가로 검증합니다. 기존 사용자 학습 공간은 건드리지 않습니다.
- 기존 `HTML` 조립·인터랙션·내용 검토는 명시적 실시간 인터랙션에서 유지합니다.
  테마·공통 셸 평가 4건은 이 분기로 명시 이전하고 다른 근거·접근성·권한 검증을 보존합니다.
- `tk-grooming`은 선언된 의존 스킬 최소 버전을 읽기 전용으로 감사합니다.
- 블라인드 카드의 중립 원본·추가 링크와 이스케이프한 공개 주석을 제공합니다. 변경 없는
  기존 카드의 `fingerprint`는 유지하고 추가 공개 근거가 바뀌면 새 평가를 요구합니다.

## 상류 근거와 선택

`tt-a1i/archify@d6059331abbddb49bca380ff46dca8ce33158b04`의 `skill-release.json`
(3.2.0), `SKILL.md`, `references/explainer-authoring.md`, `references/authoring-contract.md`,
`explainer/render.mjs`, `explainer/diagrams.mjs`와 `explainer` `CLI/packaging` 테스트를 확인했습니다.

- `keep:` 결론 우선 `explainer` 레이아웃, `native` 도식, 단일 `HTML` 내 `PNG`, `finalize`의 `validate/deliver/check.`
- `adapt:` `TigerKit` 근거 고정과 기본 검토 범위, 장면 `SVG`의 `PNG` 변환, 비소프트웨어의 `native` `legend.`
- `omit:` 상류 구현 `vendoring`, 자동 설치·업데이트, 한국어 별도 윤문 단계, 상류 저장소 수정·게시.

영어 `UI` `fallback`과 `compact` 분기 중국어 라벨은 코드로 확인했습니다. `@image` `SVG` 미지원은
작성 계약으로 확인했습니다. 외부 패키지 `B` 항목을 고치거나 관리자에게 전송하지 않았습니다.

## 검증 범위와 지침 부하

새 기본 본문은 기존 장문 제작 지시를 대체합니다. `renderer/evidence`는 모든 기본 실행,
`scene/review/follow-up`은 해당 분기에서만 읽습니다. 최소 버전 확인을 빼면 구버전 렌더링을,
낮음 내용 오류 교정을 빼면 미해결 오류를, `renderer-owned` 분류를 빼면 고정 `UI` 수정을 유발할 수
있어 유지합니다. 한국어 별도 다듬기 지시는 제외하고 정확한 기존 문체를 보존합니다.
검증용 `helper`는 의미 있는 실패·오프라인·평가 유지 회귀를 실행합니다. 새 상시 참조는
실제 기본 경로에 맞춰 `token-budget`의 읽기 목록을 갱신하며 상한을 늘리지 않습니다.

`README:` 공개 스킬 삭제·설명 범위 변경을 카탈로그와 `MIGRATION.md`에 반영했습니다.

독립 검수에서 `viewBox` 단독 `SVG`의 기본 `300px` 축소, 압축 이미지의 신원 문자열 오탐,
링크 확장자 변경 시 평가 재사용, `aria-hidden` 텍스트 누락을 확인하고 각각 회귀를 추가했습니다.
기본 설명과 실시간 인터랙션·답변 전용 분기의 의존성 검사도 분리했습니다.
실제 `Chrome`에서 `SVG` 스크립트 비실행·투명 배경·2배 해상도와 `11000px` 전체 캡처를 검증했습니다.
장면 `PNG`가 포함된 `archify` 페이지는 `finalize`와 독립 내용 검토를 통과했습니다.
`Linux`의 별도 실행용 `Chrome`·폰트를 사용했으며 `Windows/macOS` 실행은 검증하지 않았습니다.
