# 출처와 적용 판단

2026-11-18에 GSD Core next revision `80bee56295533893436a0fe9b48939b0b21b5774`의 다음 소스를 확인했습니다.

- **keep:** [autonomous](https://github.com/open-gsd/gsd-core/blob/80bee56295533893436a0fe9b48939b0b21b5774/gsd-core/workflows/autonomous.md)의 단계 실행·검증 미완료 구분·단계마다 로드맵 재독, [execute-phase](https://github.com/open-gsd/gsd-core/blob/80bee56295533893436a0fe9b48939b0b21b5774/gsd-core/workflows/execute-phase.md)의 가벼운 오케스트레이터와 위임.
- **adapt:** [context-budget](https://github.com/open-gsd/gsd-core/blob/80bee56295533893436a0fe9b48939b0b21b5774/gsd-core/references/context-budget.md)의 짧은 결과·컨텍스트 단계·작업 경계 보호. 실제 사용량을 알 수 없으면 추정하지 않습니다. [pause-work](https://github.com/open-gsd/gsd-core/blob/80bee56295533893436a0fe9b48939b0b21b5774/gsd-core/workflows/pause-work.md), [resume-project](https://github.com/open-gsd/gsd-core/blob/80bee56295533893436a0fe9b48939b0b21b5774/gsd-core/workflows/resume-project.md)의 상태·결정·재개를 기존 Handoff와 목표 장부로 조정합니다. TigerKit의 조사·인터뷰·위임 권한 및 전체 목표 독립 평가를 결합합니다.
- **omit:** GSD CLI, 프로젝트 관리 framework, 자동 문서 커밋, 호스트 설정 변경, 제공자 모델명, 자동 세션 초기화 런타임. 기존 tk-mission의 화면 감시와 세션 교체를 제거합니다.

원본 코드는 복사하지 않습니다. 실환경의 Context Rot 감소·비용 절감은 입증하지 않았습니다.
