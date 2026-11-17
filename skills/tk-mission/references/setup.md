# 환경 연결과 최초 검증

## 실행 범위

Python 3.10 이상, Git과 POSIX 로컬 워크트리가 필요합니다. TUI는 표준 라이브러리 `curses`를 사용하며 설치되지 않았거나 터미널을 사용할 수 없으면 `watch --plain`을 사용할 수 있습니다. Windows 네이티브 및 서로 다른 파일시스템을 사용하는 원격 세션은 이 구현에서 검증하지 않았습니다. WSL이나 SSH에서는 모든 프로세스와 실행 상태가 실제로 같은 호스트 및 파일시스템에 있는지 확인합니다.

현재 설치 컬렉션의 실제 `tk-mission/scripts/rollover.py`를 찾아 절대 경로로 사용합니다. 설치 패키지에 실행 파일이나 결과를 쓰지 않습니다. 대상 저장소에서 Git 루트를 확인하고 다음 명령으로 실행 경로를 구합니다.

```bash
SCRIPT='<installed tk-mission absolute path>/scripts/rollover.py'
ROOT="$(git rev-parse --show-toplevel)"
RUN="$(python3 "$SCRIPT" path --root "$ROOT")"
```

이 경로는 `XDG_STATE_HOME` 또는 사용자 홈의 로컬 state 아래에 워크트리 절대 경로 해시로 계산됩니다. 동일한 워크트리는 한 실행만 등록할 수 있습니다. 디렉터리의 소유권과 권한을 확인하며 symlink 및 저장소 내부 경로를 사용하지 않습니다. 이미 등록되었다면 `status`로 확인합니다. 등록 중인 실행을 재사용하거나 중단 원인을 해결하지 않은 상태에서 다른 디렉터리로 우회하지 않습니다.

## Orca 환경

현재 호스트에서 설치된 Orca CLI와 도움말을 우선 읽습니다. `ORCA_TERMINAL_HANDLE`이 실제 자신의 값인지 `terminal show`와 `worktree current`로 대조합니다. 메인 에이전트가 지원되는 터미널 세션이어야 합니다. Orca Chat 표면 또는 지원되지 않는 CLI는 확인되지 않은 터미널에 바인딩하지 않습니다.

- Claude Code: statusline의 `context_window.used_percentage`를 사용합니다. 기존 statusline을 보존하고 이미 제공되는 사용률을 읽거나 그 표시만 최소한으로 추가합니다.
- Codex: `/statusline`에서 context-used 또는 context-remaining을 확인합니다. remaining이면 `--pressure-kind remaining`을 사용합니다.
- Hermes: status bar의 `context_pct`를 확인합니다. 유휴 판정과 정상 종료 지원은 별도 확인이 필요합니다.

실제 화면 마지막 네 줄에서 정확히 한 줄에 일치하는 정규식을 사용합니다. `percent`라는 이름의 캡처 그룹이 필요합니다. 예를 들어 상태 표시줄의 전체 행이 실제로 `TK_CTX_USED=42%`인 경우에만 다음 패턴이 적합합니다.

```bash
--pressure-regex 'TK_CTX_USED=(?P<percent>[0-9.]+)%'
```

5시간/주간 사용량, 로그에 남은 과거 숫자, 추정치, 잘린 행을 현재 컨텍스트로 처리하지 않습니다. 압축 기준에 충분한 여유가 있는 임계치를 선택합니다. 사용자 수준 설정을 바꾸거나 외부 패키지를 설치해야 한다면 기존 설정과 승인 범위를 확인합니다.

```bash
python3 "$SCRIPT" --run "$RUN" init --root "$ROOT" \
  --host codex --orca '<absolute Orca executable>' \
  --pressure-regex '<verified full-line regex>' --threshold 60
```

`--host`는 실제 `claude`, `codex`, `hermes` 중 하나입니다. `--handle`을 생략하면 현재 자신의 handle을 사용합니다. 명시해도 자신의 handle과 같아야 합니다. `--seed <exact path>`는 실제 현재 작업에 연결된 경우에만 추가합니다. 모델과 effort는 실제 값으로 지정할 수 있습니다. 기본값으로 실행할 때는 기존 프로세스의 계정, 권한, 모델, effort가 자동 상속된다고 가정하지 않습니다.

`--auto-exit`을 선택하기 전에 동일 호스트의 격리된 무해한 테스트 세션에서 다음을 검증합니다.

1. 자신의 정확한 세션/워크트리 식별 및 현재 컨텍스트 값이 맞는지 확인합니다.
2. 진행 중인 입력이나 작업이 있는 세션은 종료하지 않는지 확인합니다. `tui-idle`, 빈 draft, 승인 대기 없음 및 작업 담당자의 안전 경계 확인을 모두 사용합니다.
3. 해당 CLI의 정상 종료 명령(Claude/Hermes `/exit`, Codex `/quit`)이 실제로 PTY를 정상 종료하는지 확인합니다. 셸로 돌아오기만 하면 종료 증거가 아니므로 새 세션을 시작하지 않습니다.
4. 같은 워크트리에 fresh launch하고 provider session ID가 실제로 달라졌으며 계정, 권한 및 모델/effort가 그대로인지 확인합니다. 이 테스트는 사용자의 제품 파일을 수정하거나 원격 발행하지 않습니다.

성공한 경우에만 원래 작업의 등록 시 `--auto-exit --profile <nonsecret verified profile identifier> --session-id <observed provider session ID>`를 추가합니다. `--model`과 `--effort`는 실제 지원되는 값만 지정합니다. 프로필에는 비밀이 아닌 모델/effort, 계정 식별 별칭, 권한 및 실행 옵션의 확인된 요약을 넣습니다. 새 에이전트가 실제 값을 검증하고 ACK에 제출하며, 기계적으로 확인할 수 없는 요소를 추측하면 안 됩니다. 현재 Orca CLI가 기존 프로필을 그대로 재현할 수 없는 경우에는 자동 종료를 켜지 않습니다.

현재 전략을 작성한 뒤 `enroll`, `doctor`를 자기 세션에서 실행합니다. 컨트롤러는 별도 터미널에서 실행합니다.

```bash
python3 "$SCRIPT" --run "$RUN" enroll
python3 "$SCRIPT" --run "$RUN" doctor
```

실제 `orca terminal create --help`에서 지원되는 정확한 옵션을 확인하고, `terminal show`에서 얻은 worktree ID를 명시해 새 터미널을 생성합니다. `--command`에 전달할 Python과 경로는 셸 리터럴로 정확히 인용합니다.

```bash
orca terminal create --worktree 'id:<exact worktree ID>' \
  --title 'TigerKit Mission Control' \
  --command '<quoted absolute Python and rollover.py> --run <quoted run path> watch' --json
```

`terminal read --screen` 등으로 컨트롤러가 정상 실행 중인지 확인합니다. 별도의 에이전트나 Orca Automation은 생성하지 않습니다. 자동 종료가 비활성화된 경우는 안전한 인계까지 진행하고 기존 세션의 확인된 정상 종료를 기다립니다. 컨텍스트 표시를 확인하지 못한 경우 수동 `request`만 가능합니다. 기본 감시 주기는 30초이며 전환 단계에서는 최대 2초 간격으로 상태를 확인합니다. 장시간 도구가 실행 중이면 작업 경계 확인이 늦을 수 있으므로 내장 compact는 비활성화하지 않습니다.

## 다른 터미널 환경

Orca가 없는 환경에서는 현재 도구가 실제로 제공하는 세션 제어 수단을 조사합니다. tmux라면 자신의 `TMUX_PANE`, 정확한 pane, 프로세스와 작업 디렉터리를 확인하고 별도 pane/window를 컨트롤러로 사용할 수 있습니다. 일반 터미널은 해당 호스트의 지원되는 API나 실행 래퍼를 사용합니다. 단순 pane 이름, PID 검색, 프롬프트 문자열이나 `sleep`을 유휴/정상 종료의 증거로 사용하지 않습니다. 일반 셸로 돌아온 것과 provider 프로세스의 정상 종료를 구분합니다.

확인된 제어 API를 사용해 작은 로컬 Python 어댑터를 작성할 수 있습니다. [어댑터 계약](adapter.md)을 읽고 실행 소유 경로에 준비합니다. 해시가 바뀌면 컨트롤러가 중단합니다. 동일한 무해한 테스트에서 실제 종료, 동일 권한의 새 세션과 ACK까지 검증한 후 `init --adapter <absolute file>`을 사용합니다. 컨트롤러는 현재 환경의 별도 터미널에 foreground로 실행합니다. 검증된 제어 수단을 확보하지 못했다면 자동 교체가 가능하다고 주장하거나 임의의 제어 어댑터를 활성화하지 않습니다. 전략 및 수동 인수인계는 사용할 수 있습니다.

## 제어 및 복구

```bash
python3 "$SCRIPT" --run "$RUN" status
python3 "$SCRIPT" --run "$RUN" request
python3 "$SCRIPT" --run "$RUN" pause
python3 "$SCRIPT" --run "$RUN" continue
python3 "$SCRIPT" --run "$RUN" stop --status completed
```

TUI의 H는 전략 및 인계 세부 정보를 표시하고 R은 수동 교체를 요청합니다. P는 active 단계의 감시를 일시 중단하거나 다시 시작하며 Q는 현재 에이전트를 종료하지 않고 이후 교체를 중단합니다. 방향키로 긴 목록을 이동합니다. `stop`의 상태는 `completed`, `blocked`, `aborted`, `waiting_user`, `unverifiable`입니다.

컨트롤러 터미널을 실제로 닫으면 감시가 중단됩니다. 화면 전환이 프로세스 종료를 의미하지는 않습니다. 중단된 실행은 상태 파일과 기존 대화를 보존합니다. `launching`에서 중단되면 새 에이전트가 이미 시작되었을 수 있으므로 중복 launch하지 않습니다. `exit_sent`에서는 정상 종료 증거만 확인합니다. 컨트롤러가 갑자기 중단되면 먼저 상태와 해당 터미널의 실제 프로세스를 확인하고 수동 인계로 복구합니다. `stop.json`을 삭제하여 강제로 재개하지 않습니다. 새 작업은 기존 실행이 종료되고 컨트롤러가 없음을 확인한 뒤 정확한 소유 디렉터리를 별도의 복구 경로로 보존하여 새로 등록합니다. 이때 이전 실행의 전략, 인계와 Git 파일을 자동 삭제하지 않습니다.

## 검증 한계

상태 머신과 모의 어댑터 검증은 실제 Orca/Claude Code/Codex/Hermes 또는 다른 터미널의 기능을 입증하지 않습니다. 실제 정상 종료, 새 provider ID, 프로필 유지, 작업 재개, 자동 압축 대비 토큰 효율은 실환경에서 검증해야 합니다. 문서 해시와 ACK는 자료의 기계적 일치 및 에이전트가 확인했다고 보고한 사실을 보장할 뿐, 인계 내용의 의미 정확성을 독립적으로 증명하지 않습니다.
