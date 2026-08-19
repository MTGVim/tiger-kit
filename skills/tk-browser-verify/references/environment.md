# Headless 환경

승인된 근거를 만들 수 있는 가장 단순한 native, Playwright-compatible, MCP
또는 CDP 경로를 선택합니다. 한 번의 run을 위해 새 browser 의존성을
설치하지 않습니다. 새 Chrome/Chromium 프로세스는 첫 browser call 전에 정확한
유효 인자 `--headless=new`, binary, PID/provider process ID, 격리된 run-owned
`user-data-dir` 를 반드시 증명해야 합니다.

CDP에서는 live endpoint, 실제 프로세스, port, profile 소유권을 확인합니다.
저장된 port, prior browser UUID, `DevToolsActivePort`, provider default, tool
name은 근거가 아닙니다. 알 수 없거나 사용자 소유인 browser에 절대 attach하거나
변경하지 않습니다.

## 인증

이미 사용 가능하고 이 run이 소유하며 headless임이 검증된 안전한 authenticated
session만 재사용합니다. 그 외에는 정확한 repository/application-supported
header, cookie, storage, session bootstrap 또는 완전한 비대화형 login 경로를
통해 transient material을 사용합니다. secret value를 캡처하지 않고
authenticated 대상 상태를 확인합니다.

interactive login, OTP, MFA, SSO, CAPTCHA, passkey, device 승인에는 browser
대체 경로가 없습니다. 임시 secret 입력 channel을 통해 short-lived
token/session을 요청합니다. 승인된 상태를 확립할 방법이 없으면 product
mutation 전에 `Unverifiable` 을 반환합니다.

## 서버와 제공 소스

`standalone` 실행에서 가능한 `dev-server` 명령이 둘 이상이면 실행 전에 후보와
선택을 사용자에게 제시하고 확인받습니다. `parent`가 정확한 명령을 넘긴 `nested`
실행에서는 같은 결정을 다시 묻지 않습니다. `react-scripts`/CRA 서버는
`BROWSER=NONE` 또는 저장소가 문서화한 동등한 `auto-open` 억제를 명령에 포함합니다.
`long-running server`는 정확한 PID, `cwd`, 명령, `port`, 제한된 `log` 경로를 가진
`run-owned` 백그라운드 프로세스로 시작하고, `bounded timeout`의 구체적인
`HTTP`/`port` `readiness signal`을 주기적으로 확인합니다. 프로세스 종료를 기다리지
말고 `readiness` 후 계속합니다.

existing server는 cwd가 작업 트리와 일치하고 asset/watch pipeline이 현재이며
bundle/응답 또는 changed render가 serving version을 증명할 때만 재사용합니다.
cwd만으로는 불충분합니다. 다른 작업 트리와 사용자 프로세스를 보존하고 소유권
또는 freshness가 불확실하면 별도 port를 사용합니다.

browser/version, 대상, 필요한 경우 viewport/DPR, working tree, server
프로세스/cwd, asset pipeline, serving-version proof를 간결한 사실로 기록합니다.
