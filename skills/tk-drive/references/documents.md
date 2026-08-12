# Drive 문서 발급 및 소비

Drive는 user-only `tk-to-spec`, `tk-to-tickets`, `tk-implement` 를 호출하지 않는다.
Prepare에서 세 작업 문서를 다음 순서로 검사하고 controller 준비 과정에서 직접
발급하거나 소비한다.

## 원천 우선순위와 대체

현재 대화의 명시적 사용자 요구와 같은 대화의 확정 결정이 가장 최신 원천이다.
승인된 활성 실행, 현재 원천과 일치하는 `Ready` 문서, 과거 종료 문서와
영속 선행 근거가 그 뒤를 따른다. 과거 `Status: Pass` 문서는 현재 원천을
차단하거나 덮어쓸 수 없다.

1. `spec.md` — 소스 identity/anchor와 lineage, goal, 범위/exclusions, constraints,
   R/AC, 검증, 사실/unknowns/conflicts를 self-contained하게 가진다.
2. `tickets.md` — 새 spec lineage를 참조하고 티켓별 커버리지, 범위, 소유 경로,
   의존성, acceptance, 검증, `model`, `effort` 를 가진다.
3. `implement.md` — 새 Ready 티켓 lineage를 참조하고 현재 단위의 정확한 경로,
   순서, R/AC, verifier, 허용/금지 범위, 실패 경계를 가진다.

누락 문서 또는 현재 원천과 계보가 다른 종료 문서는 사용 가능한 완전한
현재 원천에서 위 필드를 채운 자체 완결형 `Status: Pending` 문서로 직접
발급한다. 새 문서에는 대체된 문서의 절대 경로와 계보를 기록한다.
`drive.md` 에는 문서 경로, 대체 기록, `Pending` 진행만 기록한다. 사용자의
명시적 승인이 표시된 뒤 각 문서는 `Ready`가 되며, 세 문서가 모두 Ready일 때만
Drive 승인 표면과 작업자 dispatch가 가능하다.

기존 `Ready` 문서는 origin 스킬과 무관한 일반 소스로 소비할 수 있다. 단,
소스 anchor와 upstream lineage, content completeness, 현재 소스/HEAD freshness를
다시 읽는다. 현재 대화 원천이 완전하면 낡음/계보 불일치는 supersession으로
정리하고 새 문서를 발급한다. 현재 원천이 불완전·모순·위험하거나, Pending 문서가
승인되지 않았거나, 새 `Ready` 문서의 필수 항목이 빠졌을 때만 정확한 사유와
영향을 받는 절대 경로를 기록하고 `Status: Blocked`로 종료한다. 그 경우
작업자 배정, 제품 변경, stage, commit은 금지한다.

문서 발급/소비는 archive, 현재 pointer, global 상태, work-map을 만들지 않는다.
