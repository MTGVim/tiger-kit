# 로컬 제어 어댑터 계약

현재 워크트리와 실행 호스트에서 확인한 제어 수단이 있는 경우에만 사용합니다. Orca의 기본 연결은 포함된 스크립트가 소유합니다. 이 인터페이스는 동일한 상태 머신을 다른 터미널에서 사용할 수 있도록 마련한 좁은 경계이며, 임의 명령 실행 API나 중앙 라우터가 아닙니다.

어댑터는 실행 소유의 사용자 전용 디렉터리에 둔 Python 파일입니다. 저장소 내부, symlink, 다른 사용자가 쓰는 파일, 사용자 비밀을 기록하는 파일을 사용할 수 없습니다. `init` 이전에 실행 디렉터리의 형제 경로 등에 만들고, 직접 의존하는 파일 및 실행 명령도 검토합니다. 컨트롤러는 어댑터 파일 해시를 고정하고 `sys.executable <adapter>`로 실행합니다. 셸을 거치지 않습니다.

표준 입력에는 한 JSON 객체가 전달됩니다. `version: 1`, `operation`, `root`, `host`, `worktree_id`, `profile`, `model`, `effort`와 작업별 인수가 있습니다. 표준 출력에는 `{"ok":true,"result":...}` 한 객체만 반환합니다. 알 수 없는 작업, 확인되지 않은 값, 애매한 명령 결과는 실패로 반환합니다. stdout 및 오류에 비밀이나 전체 대화를 출력하지 않습니다.

| operation | 인수 | result |
| --- | --- | --- |
| caller | 없음 | 호출 프로세스가 속한 실제 고유 handle 문자열 |
| show | handle | handle, worktreeId, worktreePath, executionHostId, incarnationId, agentIdentity, connected, writable, orphaned, verdict, agentWait |
| screen | handle | source (`screen`), status (`running`), tail (현재 화면 행 배열), draft (실제 현재 입력) |
| wait | handle, condition | satisfied, status, exitCode, blockedReason |
| send | handle, text | accepted |
| notify | handle, request_path | 선택적인 전달 결과 |
| launch | prompt | outcome: {kind: terminal, handle}, worktreeId, operationId |

`show`는 안정적인 handle과 프로세스 생애마다 다른 incarnation을 실제 근거에서 구분합니다. `worktreeId`는 최초 바인딩 전에는 인수로 받지 않으므로 직접 조사합니다. 실행 호스트와 워크트리 절대 경로가 일치해야 합니다. `agentIdentity`는 `claude`, `codex`, `hermes` 중 확인된 종류입니다. `verdict: live`는 실제 연결 및 쓰기 가능 상태일 때만 반환합니다. `agentWait: null`은 승인/사용자 입력 대기가 없다는 증거가 있을 때만 반환합니다. 알 수 없으면 필드를 생략하거나 실패합니다.

`screen.tail`에는 누적 로그가 아니라 현재 화면의 마지막 행을 반환합니다. `draft`는 확인 가능한 현재 입력만 사용하고 모르면 성공 응답을 만들지 않습니다. `wait`의 조건은 `exit`와 `tui-idle`입니다. 정상 종료는 실제 원래 프로세스의 `status: exited` 및 `exitCode: 0`을 모두 반환할 때만 인정됩니다. 터미널이 사라졌다는 사실만으로 정상 종료라고 주장하지 않습니다. 새 사용자 입력이 없고 기존 승인·작업이 종료된 유휴 상태만 `tui-idle` 성공으로 반환합니다.

`send`는 해당 인스턴스에 대한 정상 종료 명령만 전달하며 사용자의 승인이나 입력을 대신하지 않습니다. `launch`는 같은 작업 공간에 검증된 프로필로 새 provider 세션을 실행하고 실제 새 terminal handle과 worktree ID를 반환합니다. 이전 세션의 resume 인수를 전달하지 않습니다. 불확실한 launch 결과를 자동 재시도하지 않습니다. `notify`는 선택적인 협력 요청이며 요청 파일이 정본입니다.

격리된 테스트에서 실제 fresh session, 종료 증거, 모델/effort/계정/권한, ACK 및 실패 시 중단을 확인하지 못하면 자동 교체를 활성화하지 않습니다. tmux의 `capture-pane`과 `send-keys`만으로 임의 에이전트의 안전한 유휴 상태를 확인할 수 있다고 가정하지 않습니다.
