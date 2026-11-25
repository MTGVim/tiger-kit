# ADR 0012: 호스트 Task를 우선 활용하는 업무 추적 스킬

- 상태: Superseded (2026-11-25, [ADR 0014](0014-retire-redundant-task-skill.md))

## 배경

Orca Bot과의 대화에서 조사·검토·구현 요청이 Worker 실행이나 대화 응답으로만 끝나 업무 이력이 누락되는 경우가 있었습니다. 반면 TigerKit 자체 장부나 Runner를 만들면 Orca의 Item/Dispatch와 상태 정본이 중복되고 Worktree 간 동기화 문제가 생깁니다.

## 결정

1. `tk-tasks`는 Task 등록·상태·위임을 위한 자연어 진입점이자 기존 업무 스킬의 공통 참조를 소유합니다. 사용자에게 반환할 독립 결과 단위만 Task로 기록하며 **독립 Task당 주 Worker 하나·Workspace 하나**를 기본으로 사용합니다. 내부 Todo·리뷰·검증 라운드는 기존 주 Worker와 Worktree에서 수행하고, 별도 Orca Worker·Worktree를 증식시키지 않습니다. 검증용 내부 서브에이전트는 같은 Workspace와 기존 승인 범위 안에서만 사용합니다.
2. 미완료 선행 Task에 의존하거나 사용자가 보류한 일감은 `planned` 의미로 기록합니다. 그 밖의 실행 가능한 요청은 `in_progress` 의미로 등록 후 착수합니다. 호스트마다 다른 상태명을 실제 API에 맞게 사용하며 상태 표시가 실행·완료의 증거는 아닙니다.
3. Orca Bot Chat에서는 Items가 업무 정본이며, 감독형 Worker 상태는 Orchestration/Dispatch에서 확인합니다. Bot 코드·조사 Worker는 기본적으로 선택한 **프로젝트 Git 저장소의 Worktree**를 만들고, Orca 사이드바에서 Bot Home의 자식으로 연결하는 `new-child` 배치를 사용합니다. Bot Home 디렉터리에 소스를 저장하지 않으며 Folder Workspace에서 출발하므로 명시적 저장소 선택이 필요합니다. `--item`의 Dispatch 링크와 Workspace 부모 계층은 따로 확인합니다. 원격 위임에서는 `--item`과 `--on`을 조합하지 않고 생성된 Dispatch를 후속 연결합니다. 일반 Orca Coordinator는 Orchestration 지원과 소유권이 확인된 경우만 Run/Task/Worker를 활용합니다. 이미 위임받은 Worker는 원본 Task를 재등록하거나 Coordinator로 승격하지 않습니다.
4. Orca 외 환경은 호스트 기본 Todo/Task 도구만 사용합니다. 도구가 없으면 작업을 그대로 수행하고 등록 완료를 주장하지 않습니다. `tasks.py`, `tasks.md`, DB, 전역 장부·daemon·scheduler·새 실행기를 만들지 않습니다. `tk-ralplan`의 목표 장부와 `tk-handoff`는 기존 역할을 유지합니다.
5. Task 생성과 상태 갱신은 해당 업무의 추적에만 적용합니다. 제품 변경·Git 발행·비밀 접근·추가 승인·파괴적 변경 권한은 확대되지 않습니다. 원래 스킬의 읽기 전용 경계와 검증·독립 리뷰를 보존합니다.

## 고려와 위험

- **Keep:** Orca의 Bot Item과 Dispatch 분리, 실제 상태값·완료 증거, 기존 Task 재사용을 도입합니다.
- **Adapt:** Orca 상태를 TigerKit 전용 단일 스키마로 복제하지 않고 호스트별 네이티브 형식에 연결합니다.
- **Omit:** Task 저장 파일 동기화, Orca 명령을 감싼 실행 CLI, 필수 다중 세션 오케스트레이터를 제외합니다.

Bot에 소속된 Worktree는 Orca의 lineage만 관리하며 프로젝트 Git 저장소·경로를 그대로 보존합니다. 사용자가 원하면 `Hide bot workspaces` 설정으로 프로젝트 목록의 중복 표시를 숨길 수 있습니다. 기존에 분리된 Worker는 중복 생성하지 않고 소유권이 확인된 Worktree의 부모 관계를 복구합니다. `worker_done`은 Task 정산이며 실행 프로세스 Release와 Worktree 제거는 별개입니다. 지원되는 Orca의 자동 Release와 명시적 `worker-release`는 터미널 자원을 정리하지만 Worktree를 삭제하지 않습니다. Bot은 납품 증거를 인수하고 PR 발행·병합·보류 등 사용자 소유 결정을 먼저 처리한 뒤, 해당 Task의 Worktree 삭제 여부를 한 번 묻습니다. 정리 승인·안전한 Git 상태·정확한 Workspace 소유권이 확인될 때만 강제 옵션 없이 한 Worktree를 제거합니다. 완료된 Task 기록은 유지하고 정리를 위한 중복 Task를 만들지 않습니다. Task 도구 지원·자연어 자동 선택과 사용자 환경별 영속성은 런타임 검증 대상입니다. 정적 SKILL.md 링크·설치 closure 검증이 자연어 트리거 성공을 보장하지 않습니다.

## 참고

- [Orca Bot Items](https://github.com/stablyai/orca/blob/main/src/cli/specs/bot-items.ts)
- [Orca Orchestration](https://github.com/stablyai/orca/blob/main/docs/site/content/docs/cli/orchestration.mdx)
