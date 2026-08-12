# Drive 장부

`.tigerkit/drive.md` 는 하나의 Drive run을 위한 유일한 Markdown lifecycle
장부다. 저장소/작업 트리 로컬 파일의 현재 task를 원자적으로 교체하고
다시 읽는다. 이전 작업을 archive하거나 pointer, cursor, scheduler, global
상태를 만들지 않는다. Artifact가 존재한다고 권한이 생기지는 않는다.

다음 progress/승인/receipt만 간결하게 유지한다.

- 현재 원천 식별자, `supersedes` 대상, 저장소 snapshot과 네 작업 문서의 absolute 경로, status, lineage/freshness verdict;
- 명시적 user 결정과 approved snapshot;
- 단위 의존성/wave, execution strategy, 선택한 model class;
- `.tigerkit/session.md` 경로/상태, 현재 호스트 라우팅 소스와
  `routing_state=review-required | ready`;
- delegated 단위의 `requested_selector`, `realized_model`, `reasoning_effort`,
  `worker_id`, `receipt_source` (`unavailable` 허용);
- direct 단위의 `requested_selector=n/a`, session `realized_model` 또는
  `unavailable`, `reasoning_effort=inherited`;
- delegated 단위의 정확한 `Frozen receipt`, 호스트 dispatch receipt, `Actual receipt`,
  deviation severity, net-effect 검증과 controller verdict;
- 새 `general-purpose` implementer/검토자, task brief/report/diff package,
  `Spec compliance`와 `Task quality` verdict;
- dispatch, verifier/gap, correction, commit, aggregate/terminal/recovery receipt.

Goal, 범위, exclusion, frozen 리터럴, R/AC, 구현 지시와 verifier detail은 `spec.md`,
`tickets.md`, `implement.md` 에만 둔다. `drive.md` 에 복사하지 않는다.

중첩 작업자, 검토자, verifier는 경쟁하는 Markdown 장부를 작성하지 않는다.
이진 근거는 run-owned directory를 참조하는 방식으로 둘 수 있다. Raw
transcript, chain of thought, full log/diff, credential, password,
token, cookie, OTP, private identity 또는 다른 secret value는 저장하지 않는다.
