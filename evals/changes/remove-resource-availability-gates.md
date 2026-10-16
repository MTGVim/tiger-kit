# 호스트 자원 가용성 규칙 제거

`README: no public change`

영향 경로: `skills/tk-prep`, `skills/tk-browser-verify`, `skills/tk-app-verify`, `skills/tk-pr-rebase`, `skills/tk-pr-respond`, `skills/tk-pr-sweep`, `skills/tk-research`, `skills/tk-prototype`, 그리고 `scripts/`의 공유 런타임 가드·동기화 검사입니다.

호스트 자원 측정, 압력 분류, 자원 상태에 따른 작업 배분 규칙을 제거합니다. 필수 검사는 각 스킬의 기존 검증 계약을 따릅니다. 실행 소유 프로세스 정리와 같은 작업 공간에서 테스트가 겹치지 않게 하는 규칙은 유지합니다.
