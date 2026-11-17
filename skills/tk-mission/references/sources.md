# 설계 근거와 채택 범위

- GSD Core의 [pause-work](https://github.com/open-gsd/gsd-core/blob/next/gsd-core/workflows/pause-work.md), blob `91607e82aae2068d8ea43ee1e8fb30750d3eaf3d`, [resume-project](https://github.com/open-gsd/gsd-core/blob/next/gsd-core/workflows/resume-project.md), blob `818e9db81c2dd4b1f7a8c63021b2f9e490dccc74`: 현재 위치, 의존성, 결정 이유와 실패한 접근을 보존하는 설계를 적용합니다. 계획 엔진, 강제 자동 commit 및 전체 GSD는 도입하지 않습니다.
- [GSD Core의 context engineering](https://github.com/open-gsd/gsd-core/blob/next/docs/explanation/context-engineering.md) 및 [Anthropic의 장기 에이전트 설계](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents): 큰 목표, 단계별 성공 조건, 현재 진행 상황을 분리하고 새 컨텍스트에서 작업을 재개하는 원칙을 참고했습니다. 원본 실행 코드나 프레임워크는 복사하지 않습니다.
- [Orca CLI](https://github.com/stablyai/orca/blob/main/skill-guides/orca-cli.md): 실제 handle, terminal show/read/wait 및 agent launch의 공식 계약을 참고했습니다. 별도 예약 작업이나 orchestration Task를 만들지 않습니다. 설치 버전에 따라 실환경 확인을 요구합니다.

출처의 자체 실험이나 설계 설명은 TigerKit의 실제 토큰 절감 또는 호스트별 세션 교체 성공을 입증하지 않습니다.
