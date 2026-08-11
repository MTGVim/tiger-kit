# Drive 문서 발급 및 소비

Drive는 user-only `tk-to-spec`, `tk-to-tickets`, `tk-implement` 를 호출하지 않는다.
Prepare에서 세 작업 문서를 다음 순서로 검사하고 controller 준비 과정에서 직접
발급하거나 소비한다.

1. `spec.md` — 소스 identity/anchor와 lineage, goal, 범위/exclusions, constraints,
   R/AC, 검증, 사실/unknowns/conflicts를 self-contained하게 가진다.
2. `tickets.md` — 새 spec lineage를 참조하고 티켓별 커버리지, 범위, 소유 경로,
   의존성, acceptance, 검증, `model`, `effort` 를 가진다.
3. `implement.md` — 새 Ready 티켓 lineage를 참조하고 현재 단위의 정확한 경로,
   순서, R/AC, verifier, 허용/금지 범위, 실패 경계를 가진다.

누락 문서는 사용 가능한 완전한 소스에서 위 필드를 채운 self-contained
`Status: Pending` document로 직접 발급한다. `drive.md` 에는 문서 경로와 Pending
progress만 기록한다. Drive는 Pending을 Ready로 승격하지 않는다. 사용자의 명시적
승인 뒤에만 각 문서는 `Ready` 가 되며, 세 문서가 모두 Ready일 때만 Drive 승인
표면과 작업자 dispatch가 가능하다.

기존 `Ready` 문서는 origin 스킬과 무관한 일반 소스로 소비할 수 있다. 단,
소스 anchor와 upstream lineage, content completeness, 현재 소스/HEAD freshness를
다시 읽어 서로 일치시켜야 한다. 다시 읽은 결과가 달라지거나 Pending/missing/incomplete/
stale/lineage mismatch이면 정확한 reason과 영향을 받는 absolute 경로를 기록하고
`Status: Blocked` 로 종료한다. dispatch, product mutation, stage, commit은 금지한다.

문서 발급/소비는 archive, 현재 pointer, global 상태, work-map을 만들지 않는다.
