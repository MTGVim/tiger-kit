# Headless environment

승인된 evidence를 만들 수 있는 가장 단순한 native, Playwright-compatible, MCP
또는 CDP route를 선택합니다. 한 번의 run을 위해 새 browser dependency를
설치하지 않습니다. 새 Chrome/Chromium process는 첫 browser call 전에 exact
effective `--headless=new`, binary, PID/provider process ID, isolated run-owned
`user-data-dir`를 반드시 증명해야 합니다.

CDP에서는 live endpoint, actual process, port, profile ownership을 확인합니다.
저장된 port, prior browser UUID, `DevToolsActivePort`, provider default, tool
name은 evidence가 아닙니다. unknown/user-owned browser에 절대 attach하거나
변경하지 않습니다.

## Authentication

이미 사용 가능하고 이 run이 소유하며 headless임이 검증된 safe authenticated
session만 재사용합니다. 그 외에는 exact repository/application-supported
header, cookie, storage, session bootstrap 또는 fully non-interactive login path를
통해 transient material을 사용합니다. secret value를 capture하지 않고
authenticated target state를 확인합니다.

interactive login, OTP, MFA, SSO, CAPTCHA, passkey, device approval에는 browser
fallback이 없습니다. ephemeral secret-input channel을 통해 short-lived
token/session을 요청합니다. 승인된 state를 확립할 방법이 없으면 product
mutation 전에 `Unverifiable`을 반환합니다.

## Server와 serving source

long-running server는 exact PID, cwd, command, port, bounded log path를 가진
run-owned background process로 시작합니다. runner가 지원하면 auto-open을
억제하고, bounded timeout의 concrete HTTP/port readiness signal을 poll합니다.
process exit를 기다리지 말고 readiness 후 계속합니다.

existing server는 cwd가 worktree와 일치하고 asset/watch pipeline이 current하며
bundle/response 또는 changed render가 serving version을 증명할 때만 재사용합니다.
cwd만으로는 불충분합니다. other-worktree와 user process를 보존하고 ownership
또는 freshness가 불확실하면 별도 port를 사용합니다.

browser/version, target, 필요한 경우 viewport/DPR, working tree, server
process/cwd, asset pipeline, serving-version proof를 compact fact로 기록합니다.
