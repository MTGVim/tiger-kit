# Headless session lifecycle

interaction 전에 ownership을 분류합니다. owned browser/context/page/process는
이 run이 생성한 것이며, attached resource는 pre-exist가 독립적으로 증명된
resource입니다. owned resource만 닫고 ownership을 알 수 없으면 닫지 않습니다.

새 owned Chrome/Chromium process는 run-owned isolated profile과 exact
`--headless=new`를 사용합니다. provider launch arguments를 증명할 수 없으면
직접 시작한 verified endpoint에 attach하거나 `Unverifiable`을 반환하며 visible
browser로 재시도하지 않습니다. default user profile, stale port file, prior UUID는
재사용 가능한 session evidence가 아닙니다.

Binary evidence는 parent가 제공한 또는 standalone run-owned evidence directory에
둡니다. Markdown file을 만들지 않습니다. 인용한 각 screenshot은 존재하고
non-empty이며 실제로 inspect해야 합니다. directory를 resolve하지 못하거나,
image가 없거나, inspection이 실패하면 required browser evidence는
`Unverifiable`입니다.

success, failure, interruption, exception 모두 다음 순서로 cleanup합니다.

1. run-created pages/tabs;
2. run-created contexts;
3. run-started browser instances;
4. normal shutdown이 실패한 경우에만 exact owned process.

forced termination 전에 process arguments로 PID와 profile을 대조합니다.
`killall`, broad `pkill`, task-name bulk kill을 절대 사용하지 않습니다. attached
browser, user tab/profile, shared MCP/CDP instance, other verification run,
user-owned server를 보존합니다. application verdict를 바꾸지 않고 cleanup
residue를 보고합니다.
