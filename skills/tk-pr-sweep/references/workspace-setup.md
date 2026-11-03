<a id="repository-workspace-setup"></a>
# 저장소 workspace 설정

Orca가 설치되어 있고 승인된 Sweep 행에 workspace가 필요할 때만 읽습니다. [호스트 workspace와 setup 경계](../../tk-pr-guidance/references/workspace-setup.md)를 먼저 적용합니다. 설치된 CLI/runtime에서 지원하는 읽기 전용 저장소/설정 조회 기능을 찾아 저장소 origin/경로와 실행 호스트를 대조하고, 실제 적용되는 setup/archive 스크립트와 실행/출처 정책을 조사합니다. 참조된 스크립트 본문 조사는 동작 파악을 위한 것이며 직접 실행을 허용하지 않습니다. 이 경로를 가능하게 하려는 목적으로 Orca를 설치하거나 열거나, 설정을 바꾸거나, 이름이 비슷한 파일에서 hook을 추론하지 않습니다.
자원 사용을 평가할 때 자동 시작/탭 명령도 포함합니다.

<a id="effective-configuration"></a>
## 실제 적용 설정

로컬 Git worktree에서는 `orca.yaml`과 저장소 로컬 Orca 설정을 함께 조사합니다. `scripts.setup`과 `scripts.archive`는 hook입니다. 로컬 재정의와 명령 출처 정책은 이를 대체하거나 결합할 수 있습니다. 새 worktree의 revision이 YAML setup을 제공하며, 등록된 primary checkout이 archive와 공유 경로 규칙을 제공합니다. primary checkout의 setup만으로는 승인된 PR head의 setup을 입증할 수 없습니다. 다른 대상에는 현재 설치된 동작을 사용합니다.
`worktree.sharedDirectories`와 설정된 공유 경로는 반복 설치를 피하게 할 수 있지만, 새 링크를 만들거나 재사용이 안전하다고 가정하지 말고 의존성/lockfile 호환성과 공유 쓰기 영향을 검증합니다.

<a id="run-once-and-verify"></a>
## 한 번 실행하고 검증

실제 적용 setup과 필수 환경을 적용하는 승인된 호스트 네이티브 생성 경로를 우선합니다. Orca의 hook 신뢰와 실행 정책을 보존합니다. 스크립트가 있다는 사실은 추가 권한을 부여하지 않습니다. 자동 setup을 한 번 실행하게 하고 실제 완료를 관찰하며, 의존 작업을 배정하기 전에 필수 의존성/준비 상태 사후 조건을 검증합니다.
생성 성공이나 에이전트 터미널의 출현은 setup 성공이 아닙니다. setup과 에이전트 시작은 비동기일 수 있습니다.
정확히 준비된 workspace, setup 담당자/상태와 생략한 중복 설치를 자식에게 전달합니다. setup이 성공한 뒤에는 부모나 자식 모두 hook을 다시 실행하거나 `npm install`을 추가하지 않습니다. 호스트 생성 경로가 막히면 setup hook을 직접 실행하지 않고 공통 폴백에 따라 요약·선택지를 제시하고 해당 행의 결정을 받습니다. hook이 없다고 확인된 경우에만 [승인된 실행](execution.md)의 한 행 자원 제한 아래에서 저장소의 입증된 초기화를 사용합니다.

setup 스크립트는 실제로 수행하는 초기화를 대체하며 더 가벼운 작업량의 근거는 아닙니다.
실제 적용 명령을 조사하고 무겁거나 알 수 없는 setup에는 순차 실행을 유지합니다. 실패하거나 결과가 불확실하면 재시도 전에 소유한 setup 상태를 대조합니다. 준비 상태나 필수 신뢰를 확립할 수 없으면 해당 행만 보류합니다. 필수 hook을 일반 설치로 조용히 우회하거나 아직 실행 중인 setup을 반복하지 않습니다.

<a id="authorized-cleanup"></a>
## 승인된 정리

workspace archive/제거가 이미 승인되었으면 소유 호스트의 lifecycle과 실제 적용 archive hook을 한 번 사용합니다.
범위를 조사합니다. hook은 의존성보다 더 많은 것을 제거할 수 있습니다. archive hook 실패는 해당 정리를 막지만 이후의 안전한 행을 막지는 않습니다. workspace를 보존하고 잔여물을 보고합니다. 강제 제거하거나, teardown 스크립트를 별도로 호출하거나, 공유 의존성을 삭제하지 않습니다. [승인된 실행](execution.md#authorized-cleanup)의 실행 생성 출처, 깨끗한 상태, 원격 head와 인벤토리 점검을 적용합니다. 일괄 승인은 해당 행에 명시적으로 포함된 경우에만 정리를 승인합니다. Sweep 완료는 기존 또는 범위 밖 workspace나 사용자 소유 자원의 제거를 승인하지 않습니다.
