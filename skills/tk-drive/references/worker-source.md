# Worker source completeness

Drive가 dispatch하는 fresh worker는 원래 대화, source 조사, 다른 worker receipt를
읽지 않았다고 가정한다. brief에는 다음 네 absolute path를 항상 넣는다.

```text
/home/tigeryoo/workspace/tiger-kit/.tigerkit/drive.md
/home/tigeryoo/workspace/tiger-kit/.tigerkit/spec.md
/home/tigeryoo/workspace/tiger-kit/.tigerkit/tickets.md
/home/tigeryoo/workspace/tiger-kit/.tigerkit/implement.md
```

`drive.md` 는 진행 상태, approval snapshot, dispatch/verification receipt만
전달한다. fresh worker가 시작하는 데 필요한 goal, source anchor, scope/exclusions,
exact R/AC, owned paths, implementation order, verifier, failure boundary, lineage는
`spec.md`, `tickets.md`, `implement.md`가 직접 제공한다. “위 대화”, “앞서 논의한
pattern” 또는 receipt만 참조하는 source는 incomplete다.

허용 source는 conversation/request, readable issue/ticket, spec, tickets, 또는
approved active run이다. Drive는 source가 complete한지 확인하고, 필요한 세 작업
문서가 self-contained인지 확인한 뒤에만 dispatch한다. source 또는 문서가 missing,
incomplete, stale, 또는 lineage mismatch이면 정확한 상태와 path를 `drive.md`에
기록하고 `Status: Blocked`로 멈춘다. controller는 그 경우 product를 수정하거나
silent direct fallback하지 않는다.
