# 작업자 소스 완전성

Drive가 dispatch하는 새 작업자는 원래 대화, 소스 조사, 다른 작업자 receipt를
읽지 않았다고 가정한다. brief에는 현재 대상 checkout의 저장소 루트에서 파생한 다음 네
absolute 경로를 항상 넣는다. `<repository-root>`는 `git rev-parse --show-toplevel`의 실제
결과로 치환한다.

현재 대화의 명시적 원천이 과거 종료 문서를 `supersede`하면 제어기가 그
결정을 새 작업 문서의 원천 식별자와 계보에 기록한다. 작업자는 과거 문서의
오래된 범위를 현재 요구로 되돌리지 않으며, 새 문서가 소유한 현재 R/AC만 소비한다.

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
승인된 활성 실행이다. 현재 대화의 명시적 요청이 가장 최신이며, Drive는 그 원천이
완전한지 확인한 뒤 필요한 세 작업 문서를 자체 완결형으로 발급·갱신한다.
과거 문서의 낡음/계보 불일치는 현재 원천이 완전하면 Blocked 사유가
아니며 `supersession` 기록으로 남긴다. 현재 원천 또는 새 문서가 누락·불완전,
모순·위험하면 정확한 상태와 경로를 `drive.md`에 기록하고 `Status: Blocked`로
멈춘다. 제어기는 그 경우 제품을 수정하거나 조용히 직접 실행으로 전환하지 않는다.
