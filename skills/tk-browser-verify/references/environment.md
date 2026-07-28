# 환경 비교

네이티브 브라우저, Playwright 호환 드라이버, MCP 또는 CDP 드라이버 중 현재 환경에서 실제 관찰을 지원하는 가장 단순한 수단을 선택하세요. 기본 route는 effective process arguments에 정확한 `--headless=new`가 확인된 owned Chrome/Chromium이며 browser·version·OS·DPR·font·assets·zoom을 기록합니다. `headless: true`나 provider 기본값은 이 argument의 증거가 아닙니다. Guard mode도 headed-first 금지와 launch evidence gate를 동일하게 적용합니다.

## CDP 연결

CDP provider를 사용하기 전에 provider가 연결하는 remote-debugging endpoint와 해당 port의 실제 browser process를 확인하세요. 새 browser가 필요하고 실행 인자를 직접 제어할 수 있으면 OS app launcher보다 browser binary를 직접 실행하고, 사용자 profile과 분리된 임시 `user-data-dir`과 확인된 remote-debugging port를 사용하세요.

Provider가 사실상 고정 port에 연결되는지 확인하세요. 다른 port에 browser를 띄웠다는 이유만으로 provider가 그 인스턴스에 연결됐다고 가정하지 마세요. Auto-launch provider가 `--headless=new`를 주입·확인하지 못하면 첫 browser call에 사용하지 말고 직접 시작한 headless Chrome의 endpoint에 연결하세요. 기존 사용자 browser가 고정 port를 점유했다면 그 headed session에 fallback하거나 profile·로그인 상태를 바꾸지 말고 [세션 수명주기](session-lifecycle.md)의 attached session 경계를 따르세요.

## Screenshot 경로

Screenshot `filePath`는 browser 도구의 workspace root 기준으로 선택하세요. 세션 scratchpad 절대경로가 거부되면 repo root 또는 현재 workspace 하위 임시 경로에 저장한 뒤 필요한 위치로 이동하고 repo tree에 잔재를 남기지 마세요. 저장이 필요 없는 단일 close-up 확인은 도구가 지원하면 inline screenshot으로 충분합니다.

## Server auto-open

검증용 server를 실행하기 전에 runner의 browser auto-open 동작과 비활성화 방법을 확인하세요. `BROWSER=none`을 지원하는 runner에서는 다음처럼 command environment로 전달하세요.

```bash
BROWSER=none yarn start
```

`BROWSER=none && yarn start`는 child process에 환경 변수를 전달하는 예시로 사용하지 마세요. Runner가 `BROWSER=none`을 지원하지 않으면 확인된 flag나 configuration을 사용하세요. 비활성화 방법이 없으면 server 실행을 막지 말고 이번 실행이 새로 연 owned tab만 닫고 그 사실을 보고하세요.

## 검증 대상 최신성

이미 server가 LISTEN 중이면 먼저 process cwd, 명령, 소유권, auto-open 억제, asset watcher를 확인하세요. Auto-open을 억제하지 않은 server는 이번 실행 소유이거나 사용자가 종료를 승인한 경우에만 PID를 확인해 종료·재기동하고 이미 열린 tab을 알리세요. 다른 실행이나 사용자의 process는 건드리지 마세요.

기존 server 재사용은 다음을 모두 만족할 때만 허용합니다.

1. process cwd가 현재 검증 대상 worktree와 정확히 같습니다. 다른 worktree의 process는 그대로 두고 별도 port를 사용하거나 대기하세요.
2. 사전 빌드 asset을 쓰면 server와 asset watch를 함께 실행한 composite 명령이라는 process evidence가 있습니다.
3. 현재 worktree에만 있는 문자열이 response/bundle에 존재하거나 해당 변경의 렌더 결과가 나타난다는 serving-version 실측이 있습니다. Marker가 필요하면 [시각](visual.md)의 `instrumented` 및 residue gate를 따르세요.

셋 중 하나라도 확인할 수 없으면 기존 server를 재사용하지 마세요. 안전하게 별도 port에서 auto-open 억제와 asset watch를 포함한 composite 명령으로 시작하고, 새 tab 가능성을 미리 알리세요.

사전 빌드 CSS나 asset을 import하는 저장소에서는 마지막 source 편집 이후 재생성/watch evidence를 확인하세요. 새 style이 무시되거나 상속값으로 보이면 component 결함으로 단정하기 전에 asset 재생성, hard reload, serving-version을 재검증하세요.

Verdict `## Evidence`에는 `Working tree`, `Server process/cwd`, `Asset pipeline`, `Serving version proof`를 기록하세요. cwd 일치만으로 현재 source를 봤다고 주장하지 마세요.

## Interactive auth

Credential 직접 입력, OTP, 2FA/2-step verification, passkey, CAPTCHA, 기기 승인처럼 사용자가 직접 완료해야 하고 headless에서 진행할 수 없는 interactive auth에서만 사용자 승인 후 headed로 전환하세요. Repo 밖 user-local persistent profile에서 사용자에게 직접 로그인하도록 요청하세요. 인증 입력 화면을 screenshot·trace·video로 capture하지 말고 profile 경로, cookie, token, secret도 출력·복사·commit하지 마세요.

사용자가 인증을 완료하면 headed browser를 종료하고 동일한 persistent profile의 lock 해제를 확인한 뒤, 같은 binary와 `user-data-dir`을 `--headless=new`로 재실행하세요. Effective arguments와 인증된 target state를 확인한 뒤에만 제품 검증과 capture를 시작하세요. 이 headless handoff가 불가능하면 headed에서 검증을 계속하지 말고 `Unverifiable`로 보고하세요. 단순 visible/headed 요청, headless launch 실패, blank page, timeout 또는 디버깅 편의를 interactive auth로 분류하지 마세요.

지정된 환경, viewport 또는 feature flag만 비교하세요. 정확한 대상을 기록하고 제품 차이와 접근 권한, 데이터 또는 infrastructure 차이를 구분하세요. 인증이나 권한 때문에 진행할 수 없으면 Verdict mode는 차단된 최종 상태를 캡처·분석하고 `Unverifiable`로 보고하며 Guard mode는 진행할 수 없는 이유를 보고하세요.
