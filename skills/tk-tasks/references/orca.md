# Orca의 Task 관리 기능

Orca가 실제 실행되는 환경에서 Bot Item·Orchestration의 사용 권한을 확인했을 때만 읽습니다. 명령은 참고 경로이며 **실제 설치본의 `orca skills get orchestration --full` 및 호스트 CLI 출력**으로 지원·인자·식별자를 확인합니다. 도구가 보이지 않거나 실패했는데 소스코드의 예시를 실행 증명으로 사용하지 않습니다.

## 사용자에게 보이는 Workspace 소유권

Bot과 연결된 Workspace는 여전히 **기존 프로젝트 Git 저장소의 Worktree**입니다. Bot Home 아래에 표시된다는 것은 Orca의 **Workspace lineage(부모 관계)**이지 코드가 Bot Home 디렉터리에 복사·이동된다는 뜻이 아닙니다. Sidebar의 Bot 아래에 소속되면서 프로젝트 저장소·브랜치·Git 경로는 그대로 유지합니다.

Orca 설정의 `Hide bot workspaces`를 켜면 Bot에 연결된 Worktree는 프로젝트 섹션에서 중복 표시되지 않고 Bot 아래에서만 보여요. 이 표시 설정은 부모 관계를 고쳐 주지 않으므로 실제 `worktree ps`의 부모 식별자가 Bot Home인지 별도로 확인해야 합니다.

## Bot Chat의 Items

Bot Home 및 Bot의 실제 채팅에서 권한이 확인되면 **Items를 사용자 업무의 정본**으로 사용합니다. 사용자와 대화하는 관리자 역할은 Bot Chat이 소유합니다. 등록 전에 해당 업무의 Item, 이미 연결된 PR·이슈·Dispatch와 활성 Worker를 조회해 중복을 피합니다. Item은 하나의 Bot·채팅에 속하므로 다른 Bot 또는 채팅의 소유권을 함부로 추정하지 않습니다.

- 신규 업무를 미루거나 미완료 선행 업무가 있으면 `orca bot item add --title "<업무>" --description "<맥락과 선행 조건>" --done-means "<완료 기준>" --status planned --json`으로 등록합니다.
- 즉시 착수하는 독립 업무는 같은 명령에 `--status in-progress`를 전달합니다. CLI 인자 `in-progress`와 JSON 표시 `in_progress`를 구별합니다.
- 외부 의존 대기에는 `bot item set <id> --status waiting --note "<재개 조건>"`을, 사용자 입력·승인 대기에는 `--status needs-you`와 실제 질문을 사용합니다.
- 실제 작업 결과는 `bot item comment` 또는 상태 변경과 연결된 코멘트에 기록하며, 인수 조건을 충족했을 때만 `bot item done`으로 닫습니다. 취소는 사유를 보존합니다.
- Bot Item은 업무 상태의 정본이고 Worker의 상태는 Dispatch의 정본입니다. **`worker-start --item <Item 번호>`는 Item과 Dispatch를 연결할 뿐, Workspace의 Bot 부모 관계를 생성하지 않습니다.** `--item`은 Bot 자신의 채팅에서 로컬 Worker를 시작할 때만 사용합니다. 원격 `--on`과는 함께 사용할 수 없으며 해당 경로는 시작 뒤 `bot item link`로 실제 Dispatch를 연결합니다. 임의로 ID를 구성하거나 Bot Item을 Orchestration Task라고 부르지 않습니다.

## Worker 감독과 중복 방지

사용자가 실행을 요청했고 **현재 세션이 Coordinator**이며 이미 시작된 동일 업무의 주 Worker나 Workspace가 없을 때만 담당 스킬과 완료 조건을 담은 자급자족형 브리프로 Worker를 시작합니다. **Bot Item/독립 Task 한 개에 주 Worker 한 개, 프로젝트 Worktree 한 개**를 원칙으로 합니다. 작은 Todo, 내부 검증 라운드, 리뷰 의견과 후속 수정은 원래 Worker에 전달하며 새 Orca Worker·새 Worktree를 만들지 않습니다. 기존 Worker가 완료 보고한 뒤 추가 수정이 필요하면 원래 Dispatch에 `orchestration send --to dispatch:<dispatch-id>`로 후속 요청하여 동일 Worktree 재사용을 우선합니다. 원래 Worker가 복구 불가능하다는 근거 없이 대체 Worker를 시작하지 않습니다. `planned` Item은 선행 조건이 해결되기 전에는 Worker를 만들지 않습니다.

### Bot Home 하위 Workspace 생성

Orca Bot Chat이 관리하는 새 코드·조사 작업의 기본 배치는 **선택한 프로젝트 저장소에 만든 Worktree를 Orca의 Bot Home 사이드바 하위로 연결하는 것**입니다. Bot Home은 Git 저장소가 아닌 Folder Workspace이므로 `--worktree new-child`뿐 아니라 정확한 `--repo`가 필요합니다. 새 Git Worktree의 실제 디렉터리는 해당 프로젝트의 Orca 관리 위치에 보존하며 Bot Home 디렉터리에 옮기지 않습니다. 실행 전에 `orca repo list --json`과 `orca worktree ps --json`으로 프로젝트·기존 Worker·부모를 확인하고 실제 실행 호스트의 사용 가능한 에이전트를 확인합니다.

Bot 자신의 로컬 채팅에서 이미 생성한 Item을 연결해 위임할 때는 설치본에서 인자를 확인한 다음 다음 형태를 사용합니다.

```bash
orca orchestration worker-start --environment local --item <item-number> \
  --worktree new-child --repo id:<repo-id> --agent <agent-id> \
  --spec "<원본 업무, 허용 범위, 담당 TigerKit 스킬 호출, 검증과 반환 조건>" --json
```

- **`--item`은 업무 연결, `--worktree new-child`는 부모 Worktree 연결**입니다. 어느 하나만으로 두 관계가 만들어진다고 추정하지 않습니다. `--worktree current`는 Bot Home 자체에서 실행하는 것이고 `new-top-level`은 하위로 배치하지 않습니다. 명시적인 사용자 요청이나 기존 격리 상태가 없는 새 Bot 코드 작업에 이 둘을 기본으로 사용하지 않습니다.
- 다른 컴퓨터의 연결된 Orca 서버에서 실행해야 하면 `--item` 없이 `worker-start --on <server> --worktree new-child --repo id:<서버의-repo-id> --agent <agent-id> --spec "<업무>" --json`을 사용합니다. 성공 응답의 Dispatch ID를 확인한 뒤 Bot의 원래 채팅에서 `orca bot item link <item-number> dispatch:<dispatch-id> --json`으로 연결합니다. 원격 하위 관계는 실행 호스트의 cross-store lineage 지원이 있어야 하며, 지원되지 않는다는 경고가 나왔으면 top-level 생성 사실을 숨기지 않습니다.
- 실행 응답을 받은 뒤 `orca orchestration worker-show --dispatch <dispatch-id> --json`, `orca bot item show <item-number> --json`, `orca worktree ps --json`에서 **실제 Dispatch·Item 링크·Bot Home 부모 관계**를 각각 확인합니다. Item에 연결되었어도 Workspace가 최상위이면 성공적인 Bot 하위 생성으로 보고하지 않습니다.
- 이미지처럼 프로젝트 목록에만 보이는 기존 Worktree도 **사용자가 해당 Bot에게 소속시키기로 요청했다면**, 새 Worker 없이 현재 소유권과 실행 호스트를 확인해 부모 관계를 옮깁니다. 프로젝트의 Git 저장소·브랜치·소스 파일을 이동하거나 다시 clone하지 않습니다.
- 이미 만든 Worker의 Workspace가 분리되어 있다면 **새 Worker를 만들지 않고** 먼저 현재 부모·Bot 소유권·실행 호스트를 조회합니다. 사용자 소유 또는 다른 Bot 소유 Workspace를 임의로 이동하지 않습니다. 현재 Bot이 소유한 같은 호스트의 Worktree로 확인되면 Bot Home 채팅에서 `orca worktree set --worktree <정확한-worker-selector> --parent-worktree current`를 이용해 연결을 복구하고 다시 `worktree ps`로 확인합니다. 원격 Worktree의 부모 변경은 `--parent-environment`와 해당 호스트의 cross-store 지원을 확인한 뒤 공식 계약으로 수행합니다. 불확실하면 그대로 두고 원인과 복구 조건을 보고합니다.



- 위임하기 전에 대상 Worker 실행 호스트에서 선택된 TigerKit 스킬과 필수 의존성을 실제로 찾고 로드할 수 있는지 확인합니다. Bot Home에 설치됐다는 사실만으로 다른 Worktree·SSH·WSL 호스트에서도 설치됐다고 가정하지 않습니다. 누락되면 무단 설치 대신 `tk-setup-skills`의 범위별 설치 계획을 안내하고, 가능한 독립 작업은 계속 진행합니다.
- 브리프에는 원본 요청, 저장소·작업 식별, 허용된 변경 범위·기존 승인, 대상 스킬의 **실제 호출 지시**(`tk-prep`, `tk-review` 등), 검증·반환 계약을 적습니다. 설치되어 있다는 주장만으로 스킬 호출을 완료했다고 보지 않습니다.
- Orca Worker 기본 지침은 하위 에이전트를 제한합니다. TigerKit 구현·독립 리뷰에서 하위 위임이 필요하면 **위임 브리프에 기존 사용자 승인 범위와 검증 역할을 명시**합니다. 이때 호스트가 지원하는 **동일 Workspace의 내부 서브에이전트**를 활용하고 별도 Orca Worktree·주 Worker를 내부 Todo마다 만들지 않습니다. 독립 리뷰·검증 요구를 생략하거나 호스트 권한을 우회하지 않습니다. 반드시 별도 Worktree가 필요한 예외는 이유와 영향을 사용자에게 설명하고 승인을 확인합니다.
- 실제 Dispatch·Task ID가 주입된 Worker는 새 Item 또는 같은 작업의 새 Worker를 생성하지 않습니다. 질문·차단·`worker_done`은 Orchestration의 주입된 식별자·호스트 프로토콜을 따릅니다. Coordinator는 실제 `worker_done`과 Dispatch 상태를 확인하고 필요한 Item 상태를 갱신합니다.
- 잘못된 시작·유실·응답 없음은 실행 종료 증명이 아닙니다. 기존 Task/Dispatch/Worker를 조회하고 호스트 공식 복구 절차를 따릅니다. 응답이 없다는 이유로 새로운 Worker를 중복 시작하지 않습니다.

## `worker_done` 이후 리소스 정리

`worker_done`은 **Task·Dispatch 결과 정산**이지 Worktree 삭제나 에이전트 프로세스 종료 명령이 아닙니다. 최신 Orca는 Bot Chat이 생성한 Worker(`new-child` 포함)의 기본 `keepOpenByDefault`를 `false`로 두고, 지원하는 호스트에서는 수락한 완료 보고 뒤 약 2분 후 유휴 Worker 터미널·세션을 자동 Release합니다. 하위 위임의 원래 Bot 세션이 확인되지 않거나 `--keep-open`이 설정됐거나 호스트가 오래된 경우 자동 종료를 장담하지 않습니다.

- 완료 보고를 받으면 `orca orchestration worker-list --include-remote --json`과 `orca orchestration worker-show --dispatch <dispatch-id> --json`에서 실제 완료·프로세스 상태·`autoReleaseAt`·Keep open 여부를 확인합니다. Worker가 스스로 '보고했다'고 말한 것만으로 수락된 `worker_done`이라고 판정하지 않습니다.
- 작업이 정산됐고 더 이상 Worker에 수정·검증을 맡길 필요가 없다면 `orca orchestration worker-release --dispatch <dispatch-id>`로 **그 Worker가 소유한 터미널만** Release합니다. Orca의 안전한 자동 Release는 그대로 사용합니다. 결과가 `retained`·`release_pending`·`release_unknown`이면 공식 복구 지침을 따르고, 완료되지 않은 작업이나 후속 작업이 남은 Worker는 무리하게 닫지 않습니다. 사용자에게 묻는 Worktree 삭제 승인과 Worker 터미널 Release는 서로 구분합니다.
- Release 후에도 **Worktree와 Bot 아래의 목록은 남습니다.** 보존된 Worktree의 존재만으로 RAM을 소비하는 에이전트가 계속 실행 중이라고 판단하지 않습니다. Worktree는 `worker_done`이나 `done`만으로 자동 삭제되지 않습니다. Bot은 검증 결과를 인수한 다음 PR 열기·병합·변경 보류 등 **사용자에게 필요한 납품 결정을 먼저 처리**합니다. 추가 수정이나 검증이 필요하면 기존 Worker·Workspace를 재사용합니다.
- 납품 결정이 끝나고 실제 Task가 완료되면 Bot은 **"이 작업의 Worktree도 정리할까요?"를 한 번만 질문**합니다. 사용자가 보존·삭제를 선택할 수 있도록 정확한 Worktree와 관련 PR·브랜치 및 정리 영향을 설명합니다. 답변이 없으면 보존하며, 이미 사용자가 해당 Task의 정리까지 명시적으로 승인했다면 중복 질문하지 않습니다. 완료한 Task는 기록으로 남기고 정리를 위한 새 Task를 만들거나 완료 상태를 취소하지 않습니다.
- 삭제 승인을 받으면 `orca worktree ps --json`, `orca worktree show --worktree <정확한-selector> --json`과 Git 상태·발행 결과를 확인합니다. 해당 Task가 소유한 Worktree인지, 다른 활성 Worker가 없는지, 원격에 보존하지 않은 커밋·미추적 파일·미병합 변경·미완료 PR 작업이 없는지 확인한 경우에만 **정확한 한 Workspace**를 `orca worktree rm --worktree <정확한-selector> --json`으로 정리합니다. `--force`·`--delete-branch`를 사용하지 않고 호스트의 브랜치 보존 정책을 확인합니다. 위험하거나 실제 상태를 확인할 수 없으면 삭제하지 않고 남은 조건을 보고합니다. 이 과정에서 사용자 소유 다른 Worktree를 일괄 삭제하지 않습니다.
- 상태 확인이나 Release 때문에 대기·폴링 스크립트를 만들지 않습니다. 완료 메시지에 반응하는 기존 Orca 동작과 필요 시 일회성 조회만 사용합니다.

## 일반 Orca Coordinator

Bot Chat이 아니고 Orca Orchestration이 실제 활성화된 **관리자 세션**이라면 해당 Run·Task·Dispatch를 이용합니다. `run-create`로 Run을 확보하고 `task-create`로 의존성(`--deps`)과 작업 명세를 등록하며, 실행 가능한 Task만 `worker-start --task <task-id>`로 감독합니다. 작업에 Worktree 격리가 필요하면 Orca가 Worktree를 관리하게 합니다. `pending` 및 `ready`는 미실행, `dispatched`는 위임, `completed`는 확인된 `worker_done`입니다. 일반 독립 세션·Orca Worker·일방향 Handoff를 관리자 Run으로 가장하지 않습니다.

Orchestration 기능이 비활성화되거나 관리자 권한이 없으면 독자 Task DB를 만들지 않습니다. 실제로 제공되는 Todo 도구가 있으면 사용하고, 없으면 현재 업무를 계속합니다. Bot Items, Orchestration, 호스트 Todo 중 둘 이상에 **같은 Task의 상태 정본**을 이중 생성하지 않습니다.

## 근거

- [Orca Bot Items 명령 계약](https://github.com/stablyai/orca/blob/main/src/cli/specs/bot-items.ts)
- [Orca Worker 위임과 재개](https://github.com/stablyai/orca/blob/main/skill-guides/orchestration.md)
- [Orca Orchestration 사용법](https://github.com/stablyai/orca/blob/main/docs/site/content/docs/cli/orchestration.mdx)

상류 소스를 참고한 설계이며 실제 사용자 호스트의 설치 버전과 실행 성공을 검증한 것은 아닙니다.
