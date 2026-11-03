<a id="approved-sweep-execution"></a>
# 승인된 Sweep 실행

일괄 승인 후, 적어도 한 행이 코드/Git을 변경하거나 자식 작업을 배정할 때만 이 참조를 읽습니다.
보고 전용 및 승인 전 경로에는 필요하지 않습니다.

<a id="isolation"></a>
## 격리

자식 담당자의 `tk-pr-respond` 코드 변경 실행에서 명시적으로 승인된 index-only 경로도 격리로 인정합니다. 정확한 PR/head/행 식별 정보와 실행 소유권을 전달하고, workspace 경로를 요구하지 않은 채 해당 담당자가 보호 조건을 입증하게 합니다.
다른 코드 변경 및 Git 변경 자식에는 새로 확립한 전용 workspace가 필요합니다. 답글만 수행하는 자식은 격리만을 위해 workspace를 만들지 않습니다. 부모의 `main` 또는 `develop` 작업 파일, 실제 index, HEAD와 로컬 branch ref를 보존합니다. index-only는 담당자의 무시된 실행 파일과 object store 쓰기만 허용합니다.

workspace를 만들기 전에 행의 Git 상태를 조사합니다. `git rev-parse --show-superproject-working-tree`로 submodule을 제외한 뒤에만 `GIT_DIR != GIT_COMMON`을 linked-worktree 신호로 취급합니다. 이것은 행 소유권을 입증하지 않습니다. 호스트가 만든 workspace는 경로, 정확한 PR head, 행 식별 정보와 전용 출처가 최신이고 모호하지 않을 때만 재사용합니다.

workspace를 만들거나 자식을 배정하기 전에 아래 **자원 제한**에 따라 setup과 실행 동시성 범위를 선택합니다.
새 workspace의 생성·초기화 경로를 선택하기 전에 [호스트 workspace와 setup 경계](../../tk-pr-guidance/references/workspace-setup.md)를 읽습니다. Orca가 설치되어 있으면 [저장소 workspace 설정](workspace-setup.md)도 읽습니다. 수동 생성 경로에서 setup hook을 직접 실행하지 말고 공통 폴백의 결정을 받습니다. 중복 의존성 설치를 추가하거나 lifecycle을 우회하지 않습니다.

`EnterWorktree`, `WorktreeCreate`, `/worktree` 또는 `--worktree`처럼 에이전트가 호출할 수 있는 네이티브 기능이 있으면 우선하고, 이후 경로, 브랜치 또는 detached 상태와 HEAD를 새로 읽습니다. 안전한 네이티브 기능이 없을 때만 수동 `git worktree`를 사용합니다. 승인된 head에서 시작하고 충돌과 무관한 작업을 피하며 결과를 검증합니다. 격리를 위해 무관한 ignore 편집을 하거나 setup commit을 만들지 않습니다. 승인된 `.tigerkit/` workspace에 제외 설정이 필요할 때만 담당 SKILL.md의 산출물 경로 설정을 사용합니다.

workspace 자식은 입증된 workspace를 전달받고 사용할 때만 격리된 것입니다. 다른 행의 workspace를 재사용하지 않습니다. 격리를 입증할 수 없으면 해당 PR만 `Held` 또는 `Blocked`로 보류하고 부모 checkout에서 변경하지 않습니다. 호스트가 관리하는 workspace lifecycle을 보존하고 정리는 명시적으로 승인된 실행 소유 범위로 한정합니다.

<a id="child-scope-and-seed"></a>
## 자식 범위와 Seed

Sweep은 PR 큐 컨트롤러이며 작업 수준 SDD 컨트롤러가 아닙니다. PR 담당자가 하나의 workspace 안에서 Unit과 검토자를 처리합니다. 중첩 컨트롤러가 늘어나지 않도록 담당자가 SDD를 선택한 행은 기본적으로 순차 실행합니다. 다른 모든 행에는 아래 자원 제한을 적용합니다. setup 소유권, 완료 근거와 실행 동시성 범위를 각 자식에게 전달합니다.

Sweep 전체 Seed를 만들지 않습니다. 자식은 담당자가 지속 맥락이나 SDD를 선택할 때만 마커와 정확한 PR/head를 가진 Ready `.tigerkit/seed.md`를 사용합니다. 답글만 수행하는 작업은 Seed도 격리만을 위한 workspace도 사용하지 않습니다. 순수 rebase는 담당자의 격리 계약을 따릅니다. Seed에는 피드백, 목표, 결정, 접근법, AC, 검증과 발행 경계를 포함합니다. 화면에 보이는 UI 텍스트에는 정확히 렌더링된 문자열 또는 검증된 진입 경로와 근거를 전달합니다. 의역, 식별자, enum 추론 또는 검증되지 않은 묶음 주장은 전달하지 않습니다.

`pr-sweep.md`, `pr-respond.md` 또는 worker 영수증을 만들지 않습니다. 다른 PR 식별 정보의 Seed나 `sdd.md`를 재사용하지 않습니다.

<a id="resource-bounds"></a>
## 자원 제한

이 Sweep의 모든 저장소에 걸쳐 코드/Git 변경 행은 기본적으로 한 개씩 처리합니다. 현재 자식의 setup, 작업, 검증과 소유 프로세스 정리를 끝낸 뒤 다음 workspace를 만들거나 배정합니다. 모든 worktree를 미리 준비하거나 백그라운드 설치를 시작하지 않습니다. setup hook이 없거나 검증되지 않았으면 이 기본값을 유지합니다. 패키지 관리자를 설치하거나 스크립트를 찾았다는 사실은 안전한 동시성의 근거가 아닙니다.

참여하는 모든 행에 검증된 가벼운 setup hook이 있고, 실제 설치, 빌드, 테스트와 서버 작업량이 공유 쓰기 상태 없이 실행 호스트의 가용 자원에 들어갈 때만 코드/Git 행의 동시 실행을 허용합니다. `npm install`, 동등한 의존성 초기화 또는 제한되지 않은 작업을 실행하는 hook은 순차 실행을 유지합니다.
공유 의존성에 동시에 설치하거나 변경하지 않습니다. 독립적인 읽기 전용/답글 전용 행은 안전하면 겹쳐 실행할 수 있습니다.
자식이 무거운 작업을 추가하기 전에 다시 평가합니다. 진행 중인 작업은 끝내게 하고 안전해질 때까지 자원을 많이 사용하는 행을 더 받지 않습니다.
scheduler, 전역 lock, 용량 설정이나 원장을 만들지 않습니다. 기존 큐와 자식 인계를 사용합니다.

<a id="queue-progress"></a>
## 큐 진행

행 내부의 실패가 이후의 독립적인 행을 멈추게 하지는 않습니다. 식별 정보나 권한 오염, 모호한 저장소 범위 또는 신뢰할 수 없는 triage 같은 시스템 전체 실패에만 Sweep을 중단합니다. 자식이 돌아온 뒤 각 PR을 triage합니다.
행의 필수 발행을 검증한 뒤에는 재검토 대기 중이어도 아래 **승인된 정리**에 따라 승인된 실행 소유 workspace 정리를 수행합니다. 보호 조건이나 정리 실패 시에는 해당 행만 유지합니다.
모든 행이 끝나면 설정된 모든 저장소에 대해 최신 triage를 실행하고 실제 정리 결과 또는 보존한 경로를 보고합니다.

<a id="authorized-cleanup"></a>
## 승인된 정리

이번 실행이 만들었고 일괄 계획에서 정리를 명시적으로 승인한 workspace만 제거합니다. 기존 workspace를 재사용했다고 이번 실행에서 생성한 것이 되지는 않습니다. 제거 직전에 정확한 경로/저장소/행 생성 출처, 남은 추적 변경이 없음(staged 변경 포함), 로컬 HEAD가 최신 원격 PR head와 같음을 검증합니다. 미추적 및 무시된 내용도 조사하고 예상하지 못한 사용자 작업이나 복구 자료는 보존합니다. 보호 조건 중 하나라도 실패하거나 입증할 수 없으면 해당 행의 workspace와 로컬 브랜치를 보존하고 이유를 보고합니다. 재검토 대기만으로는 안전하게 발행된 workspace를 보존할 필요가 없습니다. 원격 head에서 다시 만들 수 있습니다.

대상 밖에서 리터럴로 검증된 경로를 사용하고 force 없이 정리를 실행합니다. 소유 호스트의 lifecycle과 archive hook을 사용합니다. Orca는 [저장소 workspace 설정](workspace-setup.md)을 따릅니다. 제거 전에 `git worktree list --porcelain`을 기록하고, 호스트 관리 대상이면 호스트의 workspace 인벤토리도 기록합니다. 직후에 같은 인벤토리를 다시 읽습니다. 정확한 대상이 사라졌고 모든 비대상 항목이 남아 있는지 검증합니다. 예상하지 못한 사라짐은 보고하고 조사할 불일치이며 누가 제거했는지 입증하는 근거가 아닙니다. 소유권이나 범위가 불확실한 동안 추가 정리를 일시 중단합니다. 다른 실행의 workspace나 브랜치를 일괄 정리하지 않습니다.
실행에서 생성한 로컬 브랜치는 승인된 호스트 정리로만 삭제하거나, 다른 workspace가 연결되어 있지 않고 미발행 commit이 없음을 별도로 입증한 정확한 브랜치만 삭제합니다. 원격 브랜치 삭제로 확대하지 않습니다.

PR은 최종 triage가 필수 검사와 발행 상태, 처리 가능한 스레드의 종료, 모든 필수 검토자의 현재 재검토 요청 또는 요약 이후 검토(활성 `CHANGES_REQUESTED` 검토자와 현재 head의 `<!-- tigerkit:pr-rereview:<HEAD_SHA>:<LOGIN> -->` 마커에 명시된 검토자), 필요한 현재 head 요약 마커 `<!-- tigerkit:pr-summary:<HEAD_SHA> -->`를 입증할 때만 완료됩니다. 요약 본문은 담당 SKILL.md의 발행 계약에 따라 검증되어야 합니다.
