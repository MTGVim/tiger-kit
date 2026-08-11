# Headless 세션 생명주기

interaction 전에 소유권을 분류합니다. owned browser/context/page/프로세스는
이 run이 생성한 것이며, attached resource는 사전에 존재함이 독립적으로 증명된
resource입니다. owned resource만 닫고 소유권을 알 수 없으면 닫지 않습니다.

새 owned Chrome/Chromium 프로세스는 run-owned isolated profile과 정확한
`--headless=new` 를 사용합니다. 제공자 launch arguments를 증명할 수 없으면
직접 시작한 verified endpoint에 attach하거나 `Unverifiable` 을 반환하며 visible
browser로 재시도하지 않습니다. default user profile, stale port 파일, prior UUID는
재사용 가능한 세션 근거가 아닙니다.

이진 근거는 parent가 제공한 또는 독립 실행 run-owned 근거 디렉터리에 둡니다.
Markdown 파일을 만들지 않습니다. 인용한 각 screenshot은 존재하고
non-empty이며 실제로 inspect해야 합니다. 디렉터리를 resolve하지 못하거나,
image가 없거나, inspection이 실패하면 필수 browser 근거는
`Unverifiable`입니다.

성공, 실패, interruption, exception 모두 다음 순서로 정리합니다.

1. run-created pages/tabs;
2. run-created contexts;
3. run-started browser instances;
4. normal shutdown이 실패한 경우에만 정확한 owned 프로세스.

forced termination 전에 프로세스 arguments로 PID와 profile을 대조합니다.
`killall`, broad `pkill`, task-name bulk kill을 절대 사용하지 않습니다. attached
browser, user tab/profile, shared MCP/CDP instance, 다른 검증 run,
user-owned server를 보존합니다. application verdict를 바꾸지 않고 정리
residue를 보고합니다.
