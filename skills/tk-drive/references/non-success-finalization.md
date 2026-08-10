# Drive non-success finalization

허용된 fresh-worker correction, reviewer escalation, re-prepare 또는 verifier
recovery를 모두 소진한 뒤에만 진입한다. 최초의 `Fail`, `Blocked`,
`Unverifiable` status를 보존하고 product mutation을 동결한다.

새로운 test, build, server, browser, worker, reviewer, cleanup을 시작하지
말고 current source, `.tigerkit/drive.md`, Git ancestry, dirty path, 기존
verification evidence를 읽는다. Approved scope를 다음처럼 분류한다.

- `Completed`: matching evidence에 계속 연결되는 verified ancestor unit commit;
- `Stopped`: terminal non-success를 만든 unit 또는 verifier;
- `Dependency blocked`: `Stopped` 에 의존하는 미완료 unit;
- `Not attempted`: mutation이 동결된 뒤 실행하지 않은 independent unit;
- `Unverified`: current binding evidence가 없는 completion.

이 accounting, 실제 branch와 `HEAD`, uncommitted owned path, evidence, status,
지원되는 recovery condition 하나만 `.tigerkit/drive.md` 에 atomically update한다.
Non-passing candidate를 reset, revert, stash, clean, verified history rewrite,
stage 또는 commit하지 않는다. Pre-existing user change를 보존한다.

Terminal response에는 유용한 `Completed`, `Stopped`, `Remaining`, `Recovery`
section과 정확히 하나의 최초 `Status:` line만 포함한다. User action이
필요할 때만 concrete recovery action을 지정한다. Partial scope를 절대
`Pass` 로 설명하지 않는다.
