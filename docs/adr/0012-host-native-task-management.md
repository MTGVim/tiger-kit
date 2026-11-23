# ADR 0012: 호스트 Task를 우선 활용하는 업무 추적 스킬

- 상태: Accepted (2026-11-24)

## 배경

Orca Bot과의 대화에서 조사·검토·구현 요청이 Worker 실행이나 대화 응답으로만 끝나 업무 이력이 누락되는 경우가 있었습니다. 반면 TigerKit 자체 장부나 Runner를 만들면 Orca의 Item/Dispatch와 상태 정본이 중복되고 Worktree 간 동기화 문제가 생깁니다.

## 결정

1. `tk-tasks`는 Task 등록·상태·위임을 위한 자연어 진입점이자 기존 업무 스킬의 공통 참조를 소유합니다. 사용자에게 반환할 독립 결과 단위만 Task로 기록하고 내부 단계마다 새 Task를 만들지 않습니다.
2. 미완료 선행 Task에 의존하거나 사용자가 보류한 일감은 `planned` 의미로 기록합니다. 그 밖의 실행 가능한 요청은 `in_progress` 의미로 등록 후 착수합니다. 호스트마다 다른 상태명을 실제 API에 맞게 사용하며 상태 표시가 실행·완료의 증거는 아닙니다.
3. Orca Bot Chat에서는 Items가 업무 정본이며, 감독형 Worker 상태는 Orchestration/Dispatch에서 확인합니다. 일반 Orca Coordinator는 Orchestration 지원과 소유권이 확인된 경우만 Run/Task/Worker를 활용합니다. 이미 위임받은 Worker는 원본 Task를 재등록하거나 Coordinator로 승격하지 않습니다.
4. Orca 외 환경은 호스트 기본 Todo/Task 도구만 사용합니다. 도구가 없으면 작업을 그대로 수행하고 등록 완료를 주장하지 않습니다. `tasks.py`, `tasks.md`, DB, 전역 장부·daemon·scheduler·새 실행기를 만들지 않습니다. `tk-ralplan`의 목표 장부와 `tk-handoff`는 기존 역할을 유지합니다.
5. Task 생성과 상태 갱신은 해당 업무의 추적에만 적용합니다. 제품 변경·Git 발행·비밀 접근·추가 승인·파괴적 변경 권한은 확대되지 않습니다. 원래 스킬의 읽기 전용 경계와 검증·독립 리뷰를 보존합니다.

## 고려와 위험

- **Keep:** Orca의 Bot Item과 Dispatch 분리, 실제 상태값·완료 증거, 기존 Task 재사용을 도입합니다.
- **Adapt:** Orca 상태를 TigerKit 전용 단일 스키마로 복제하지 않고 호스트별 네이티브 형식에 연결합니다.
- **Omit:** Task 저장 파일 동기화, Orca 명령을 감싼 실행 CLI, 필수 다중 세션 오케스트레이터를 제외합니다.

Task 도구 지원·자연어 자동 선택과 사용자 환경별 영속성은 런타임 검증 대상입니다. 정적 SKILL.md 링크·설치 closure 검증이 자연어 트리거 성공을 보장하지 않습니다.

## 참고

- [Orca Bot Items](https://github.com/stablyai/orca/blob/main/src/cli/specs/bot-items.ts)
- [Orca Orchestration](https://github.com/stablyai/orca/blob/main/docs/site/content/docs/cli/orchestration.mdx)
