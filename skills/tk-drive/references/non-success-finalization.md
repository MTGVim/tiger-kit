# Drive 비성공 최종화

허용된 새 작업자 correction, 검토자 escalation, re-prepare 또는 verifier
recovery를 모두 소진한 뒤에만 진입한다. 최초의 `Fail`, `Blocked`,
`Unverifiable` status를 보존하고 product mutation을 동결한다.

새로운 test, build, server, browser, 작업자, 검토자, 정리를 시작하지
말고 현재 소스, `.tigerkit/drive.md`, Git ancestry, dirty 경로, 기존
검증 근거를 읽는다. Approved 범위를 다음처럼 분류한다.

- `Completed`: 일치하는 근거에 계속 연결되는 verified ancestor 단위 commit;
- `Stopped`: terminal 비성공을 만든 단위 또는 verifier;
- `Dependency blocked`: `Stopped` 에 의존하는 미완료 단위;
- `Not attempted`: mutation이 동결된 뒤 실행하지 않은 독립 단위;
- `Unverified`: 현재 binding 근거가 없는 completion.

이 accounting, 실제 브랜치와 `HEAD`, uncommitted owned 경로, 근거, status,
지원되는 recovery 조건 하나만 `.tigerkit/drive.md` 에 원자적으로 update한다.
Non-passing 후보를 reset, revert, stash, clean, verified 이력 rewrite,
stage 또는 commit하지 않는다. `Pre-existing` 사용자 변경을 보존한다.

Terminal 응답에는 유용한 `Completed`, `Stopped`, `Remaining`, `Recovery`
section과 정확히 하나의 최초 `Status:` 줄만 포함한다. User action이
필요할 때만 구체적인 recovery action을 지정한다. Partial 범위를 절대
`Pass` 로 설명하지 않는다.
