# Drive document 발행 및 소비

Drive는 user-only `tk-to-spec`, `tk-to-tickets`, `tk-implement` 를 호출하지 않는다.
Prepare에서 세 작업 문서를 다음 순서로 검사하고 controller preparation으로 직접
발급하거나 소비한다.

1. `spec.md` — source identity/anchor와 lineage, goal, scope/exclusions, constraints,
   R/AC, verification, facts/unknowns/conflicts를 self-contained로 가진다.
2. `tickets.md` — fresh spec lineage를 참조하고 ticket별 coverage, scope, owned paths,
   dependencies, acceptance, verification, `model`, `effort` 를 가진다.
3. `implement.md` — fresh Ready ticket lineage를 참조하고 현재 unit의 exact paths,
   order, R/AC, verifier, allowed/forbidden scope, failure boundary를 가진다.

누락 문서는 available complete source에서 위 필드를 채운 self-contained
`Status: Pending` document로 직접 발급한다. `drive.md` 에는 문서 path와 Pending
progress만 기록한다. Drive는 Pending을 Ready로 승격하지 않는다. 사용자의 명시적
승인 뒤에만 각 문서는 `Ready` 가 되며, 세 문서가 모두 Ready일 때만 Drive approval
surface와 worker dispatch가 가능하다.

기존 `Ready` 문서는 origin skill과 무관한 generic source로 소비할 수 있다. 단,
source anchor와 upstream lineage, content completeness, current source/HEAD freshness를
reread해 서로 일치시켜야 한다. reread 결과가 달라지거나 Pending/missing/incomplete/
stale/lineage mismatch이면 정확한 reason과 affected absolute path를 기록하고
`Status: Blocked` 로 종료한다. dispatch, product mutation, stage, commit은 금지한다.

문서 발급/소비는 archive, current pointer, global state, work-map을 만들지 않는다.
