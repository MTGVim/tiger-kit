# Drive ledger

`.tigerkit/drive.md`는 하나의 Drive run을 위한 유일한 Markdown lifecycle
ledger다. Repo/worktree-local file의 current task를 atomically replace하고
다시 읽는다. Old task를 archive하거나 pointer, cursor, scheduler, global
state를 만들지 않는다. Artifact가 존재한다고 권한이 생기지는 않는다.

다음 progress/approval/receipt만 compact하게 유지한다.

- repository snapshot과 네 작업 문서의 absolute path, status, lineage/freshness verdict;
- 명시적 user decision과 approved snapshot;
- unit dependency/wave, execution strategy, dispatch tier와 realized axes;
- dispatch, verifier/gap, correction, commit, aggregate/terminal/recovery receipt.

Goal, scope, exclusion, frozen literal, R/AC, 구현 지시와 verifier detail은 `spec.md`,
`tickets.md`, `implement.md`에만 둔다. `drive.md`에 복사하지 않는다.

Nested worker, reviewer, verifier는 경쟁하는 Markdown ledger를 작성하지 않는다.
Binary evidence는 run-owned directory를 참조하는 방식으로 둘 수 있다. Raw
transcript, chain of thought, full log/diff, provider/model name, password,
token, cookie, OTP, private identity 또는 다른 secret value는 저장하지 않는다.
