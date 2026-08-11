# 작업자 소스 완전성

Drive가 dispatch하는 새 작업자는 원래 대화, 소스 조사, 다른 작업자 receipt를
읽지 않았다고 가정한다. brief에는 현재 대상 checkout의 저장소 루트에서 파생한 다음 네
absolute 경로를 항상 넣는다. `<repository-root>`는 `git rev-parse --show-toplevel`의 실제
결과로 치환한다.

```text
<repository-root>/.tigerkit/drive.md
<repository-root>/.tigerkit/spec.md
<repository-root>/.tigerkit/tickets.md
<repository-root>/.tigerkit/implement.md
```

`drive.md` 는 진행 상태, 승인 snapshot, dispatch/검증 receipt만
전달한다. 새 작업자가 시작하는 데 필요한 goal, 소스 anchor, 범위/exclusions,
정확한 R/AC, 소유 경로, 구현 순서, verifier, 실패 경계, lineage는
`spec.md`, `tickets.md`, `implement.md` 가 직접 제공한다. “위 대화”, “앞서 논의한
pattern” 또는 receipt만 참조하는 소스는 incomplete다.

허용 소스는 대화/요청, 읽을 수 있는 이슈/티켓, spec, 티켓, 또는
approved 활성 run이다. Drive는 소스가 complete한지 확인하고, 필요한 세 작업
문서가 self-contained인지 확인한 뒤에만 dispatch한다. 소스 또는 문서가 missing,
incomplete, stale, 또는 lineage mismatch이면 정확한 상태와 경로를 `drive.md` 에
기록하고 `Status: Blocked` 로 멈춘다. controller는 그 경우 product를 수정하거나
조용히 direct 대체 경로로 전환하지 않는다.
