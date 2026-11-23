# Orca의 Task 관리 기능

Orca가 실제 실행되는 환경에서 Bot Item·Orchestration의 사용 권한을 확인했을 때만 읽습니다. 명령은 참고 경로이며 **실제 설치본의 `orca skills get orchestration --full` 및 호스트 CLI 출력**으로 지원·인자·식별자를 확인합니다. 도구가 보이지 않거나 실패했는데 소스코드의 예시를 실행 증명으로 사용하지 않습니다.

## Bot Chat의 Items

Bot Home 및 Bot의 실제 채팅에서 권한이 확인되면 **Items를 사용자 업무의 정본**으로 사용합니다. 사용자와 대화하는 관리자 역할은 Bot Chat이 소유합니다. 등록 전에 해당 업무의 Item, 이미 연결된 PR·이슈·Dispatch와 활성 Worker를 조회해 중복을 피합니다. Item은 하나의 Bot·채팅에 속하므로 다른 Bot 또는 채팅의 소유권을 함부로 추정하지 않습니다.

- 신규 업무를 미루거나 미완료 선행 업무가 있으면 `orca bot item add --title "<업무>" --description "<맥락과 선행 조건>" --done-means "<완료 기준>" --status planned --json`으로 등록합니다.
- 즉시 착수하는 독립 업무는 같은 명령에 `--status in-progress`를 전달합니다. CLI 인자 `in-progress`와 JSON 표시 `in_progress`를 구별합니다.
- 외부 의존 대기에는 `bot item set <id> --status waiting --note "<재개 조건>"`을, 사용자 입력·승인 대기에는 `--status needs-you`와 실제 질문을 사용합니다.
- 실제 작업 결과는 `bot item comment` 또는 상태 변경과 연결된 코멘트에 기록하며, 인수 조건을 충족했을 때만 `bot item done`으로 닫습니다. 취소는 사유를 보존합니다.
- Bot Item은 업무 상태의 정본이고 Worker의 상태는 Dispatch의 정본입니다. **`worker-start --item <Item 번호>`는 Item과 Dispatch를 연결할 뿐, Workspace의 Bot 부모 관계를 생성하지 않습니다.** `--item`은 Bot 자신의 채팅에서 로컬 Worker를 시작할 때만 사용합니다. 원격 `--on`과는 함께 사용할 수 없으며 해당 경로는 시작 뒤 `bot item link`로 실제 Dispatch를 연결합니다. 임의로 ID를 구성하거나 Bot Item을 Orchestration Task라고 부르지 않습니다.

## Worker 감독과 중복 방지

사용자가 실행을 요청했고 **현재 세션이 Coordinator**이며 이미 실행 중인 동일 Worker가 없을 때만 담당 스킬과 완료 조건을 담은 자급자족형 브리프로 Worker를 시작합니다. `planned` Item은 선행 조건이 해결되기 전에는 Worker를 만들지 않습니다.

### Bot Home 하위 Workspace 생성

Orca Bot Chat이 관리하는 새 코드·조사 작업의 기본 Worktree 배치는 **Bot Home의 하위**입니다. Bot Home은 Git 저장소가 아닌 Folder Workspace이므로 `--worktree new-child`뿐 아니라 정확한 `--repo`가 필요합니다. 실행 전에 `orca repo list --json`과 `orca worktree ps --json`으로 프로젝트·기존 Worker·부모를 확인하고 실제 실행 호스트의 사용 가능한 에이전트를 확인합니다.

Bot 자신의 로컬 채팅에서 이미 생성한 Item을 연결해 위임할 때는 설치본에서 인자를 확인한 다음 다음 형태를 사용합니다.

```bash
orca orchestration worker-start --environment local --item <item-number> \
  --worktree new-child --repo id:<repo-id> --agent <agent-id> \
  --spec "<원본 업무, 허용 범위, 담당 TigerKit 스킬 호출, 검증과 반환 조건>" --json
```

- **`--item`은 업무 연결, `--worktree new-child`는 부모 Worktree 연결**입니다. 어느 하나만으로 두 관계가 만들어진다고 추정하지 않습니다. `--worktree current`는 Bot Home 자체에서 실행하는 것이고 `new-top-level`은 하위로 배치하지 않습니다. 명시적인 사용자 요청이나 기존 격리 상태가 없는 새 Bot 코드 작업에 이 둘을 기본으로 사용하지 않습니다.
- 다른 컴퓨터의 연결된 Orca 서버에서 실행해야 하면 `--item` 없이 `worker-start --on <server> --worktree new-child --repo id:<서버의-repo-id> --agent <agent-id> --spec "<업무>" --json`을 사용합니다. 성공 응답의 Dispatch ID를 확인한 뒤 Bot의 원래 채팅에서 `orca bot item link <item-number> dispatch:<dispatch-id> --json`으로 연결합니다. 원격 하위 관계는 실행 호스트의 cross-store lineage 지원이 있어야 하며, 지원되지 않는다는 경고가 나왔으면 top-level 생성 사실을 숨기지 않습니다.
- 실행 응답을 받은 뒤 `orca orchestration worker-show --dispatch <dispatch-id> --json`, `orca bot item show <item-number> --json`, `orca worktree ps --json`에서 **실제 Dispatch·Item 링크·Bot Home 부모 관계**를 각각 확인합니다. Item에 연결되었어도 Workspace가 최상위이면 성공적인 Bot 하위 생성으로 보고하지 않습니다.
- 이미 만든 Worker의 Workspace가 분리되어 있다면 **새 Worker를 만들지 않고** 먼저 현재 부모·Bot 소유권·실행 호스트를 조회합니다. 사용자 소유 또는 다른 Bot 소유 Workspace를 임의로 이동하지 않습니다. 현재 Bot이 소유한 같은 호스트의 Worktree로 확인되면 Bot Home 채팅에서 `orca worktree set --worktree <정확한-worker-selector> --parent-worktree current`를 이용해 연결을 복구하고 다시 `worktree ps`로 확인합니다. 원격 Worktree의 부모 변경은 `--parent-environment`와 해당 호스트의 cross-store 지원을 확인한 뒤 공식 계약으로 수행합니다. 불확실하면 그대로 두고 원인과 복구 조건을 보고합니다.



- 위임하기 전에 대상 Worker 실행 호스트에서 선택된 TigerKit 스킬과 필수 의존성을 실제로 찾고 로드할 수 있는지 확인합니다. Bot Home에 설치됐다는 사실만으로 다른 Worktree·SSH·WSL 호스트에서도 설치됐다고 가정하지 않습니다. 누락되면 무단 설치 대신 `tk-setup-skills`의 범위별 설치 계획을 안내하고, 가능한 독립 작업은 계속 진행합니다.
- 브리프에는 원본 요청, 저장소·작업 식별, 허용된 변경 범위·기존 승인, 대상 스킬의 **실제 호출 지시**(`tk-prep`, `tk-review` 등), 검증·반환 계약을 적습니다. 설치되어 있다는 주장만으로 스킬 호출을 완료했다고 보지 않습니다.
- Orca Worker 기본 지침은 하위 에이전트를 제한합니다. TigerKit 구현·독립 리뷰에서 하위 위임이 필요한 업무라면 **위임 브리프에서 그 허용 범위와 기존 사용자 권한을 명시**합니다. 독립 리뷰·검증 요구를 조용히 생략하거나 호스트 권한을 우회하지 않습니다.
- 실제 Dispatch·Task ID가 주입된 Worker는 새 Item 또는 같은 작업의 새 Worker를 생성하지 않습니다. 질문·차단·`worker_done`은 Orchestration의 주입된 식별자·호스트 프로토콜을 따릅니다. Coordinator는 실제 `worker_done`과 Dispatch 상태를 확인하고 필요한 Item 상태를 갱신합니다.
- 잘못된 시작·유실·응답 없음은 실행 종료 증명이 아닙니다. 기존 Task/Dispatch/Worker를 조회하고 호스트 공식 복구 절차를 따릅니다. 응답이 없다는 이유로 새로운 Worker를 중복 시작하지 않습니다.

## 일반 Orca Coordinator

Bot Chat이 아니고 Orca Orchestration이 실제 활성화된 **관리자 세션**이라면 해당 Run·Task·Dispatch를 이용합니다. `run-create`로 Run을 확보하고 `task-create`로 의존성(`--deps`)과 작업 명세를 등록하며, 실행 가능한 Task만 `worker-start --task <task-id>`로 감독합니다. 작업에 Worktree 격리가 필요하면 Orca가 Worktree를 관리하게 합니다. `pending` 및 `ready`는 미실행, `dispatched`는 위임, `completed`는 확인된 `worker_done`입니다. 일반 독립 세션·Orca Worker·일방향 Handoff를 관리자 Run으로 가장하지 않습니다.

Orchestration 기능이 비활성화되거나 관리자 권한이 없으면 독자 Task DB를 만들지 않습니다. 실제로 제공되는 Todo 도구가 있으면 사용하고, 없으면 현재 업무를 계속합니다. Bot Items, Orchestration, 호스트 Todo 중 둘 이상에 **같은 Task의 상태 정본**을 이중 생성하지 않습니다.

## 근거

- [Orca Bot Items 명령 계약](https://github.com/stablyai/orca/blob/main/src/cli/specs/bot-items.ts)
- [Orca Worker 위임과 재개](https://github.com/stablyai/orca/blob/main/skill-guides/orchestration.md)
- [Orca Orchestration 사용법](https://github.com/stablyai/orca/blob/main/docs/site/content/docs/cli/orchestration.mdx)

상류 소스를 참고한 설계이며 실제 사용자 호스트의 설치 버전과 실행 성공을 검증한 것은 아닙니다.
