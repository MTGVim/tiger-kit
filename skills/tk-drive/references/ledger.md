# Drive ledger

`.tigerkit/drive.md`는 하나의 Drive run을 위한 유일한 Markdown lifecycle
ledger다. Repo/worktree-local file의 current task를 atomically replace하고
다시 읽는다. Old task를 archive하거나 pointer, cursor, scheduler, global
state를 만들지 않는다. Artifact가 존재한다고 권한이 생기지는 않는다.

다음 evidence를 compact하게 유지한다.

- task/source identity, R/AC, source anchor;
- scope, exclusion, frozen source literal, durable prior art;
- 근거와 material alternative를 포함한 controller-resolved assumption/ambiguity;
- 명시적 user decision과 approved plan snapshot;
- unit dependency graph, wave, execution strategy, requested dispatch tier, symbolic realized
  model/effort axes or `host-default`, ownership;
- test/browser obligation과 non-sensitive auth mode;
- unit별 candidate, changed path, verifier/gap verdict, correction, commit;
- aggregate verification, terminal status, non-success recovery evidence.

Nested worker, reviewer, verifier는 경쟁하는 Markdown ledger를 작성하지 않는다.
Binary evidence는 run-owned directory를 참조하는 방식으로 둘 수 있다. Raw
transcript, chain of thought, full log/diff, provider/model name, password,
token, cookie, OTP, private identity 또는 다른 secret value는 저장하지 않는다.
