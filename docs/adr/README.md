# TigerKit ADR 색인

ADR은 **자주 바뀌는 skill 실행 절차가 아니라 오래 유지할 architecture decision**만 기록합니다.
현재 skill surface와 세부 동작은 ADR보다 `README.md`, 현재 `skills/tk-*/SKILL.md`, eval 정본이 우선합니다.

## 읽는 순서

1. `Accepted` — 현재도 유효한 장기 architecture decision
2. `Superseded` — 당시 결정을 설명하는 역사 기록; 현재 실행 계약으로 사용하지 않음
3. `CHANGELOG.md`, closed issue/PR — provenance와 과거 migration 맥락

현재 문서와 역사 문서가 충돌하면 다음 정본 순서를 사용합니다.

```text
current SKILL.md / executable eval
> README.md / AGENTS.md
> Accepted ADR
> Superseded ADR / CHANGELOG / closed issue·PR
```

## ADR 목록

| ADR | Status | 범위 |
| --- | --- | --- |
| [`0002-local-reflection-targets-and-durable-ledger.md`](0002-local-reflection-targets-and-durable-ledger.md) | Superseded by ADR 0003 | retired `tk-reflect`의 local rule target, ledger, rollback 계약 |
| [`0003-external-memory-and-central-skill-evolution.md`](0003-external-memory-and-central-skill-evolution.md) | Accepted | persistent memory/rule lifecycle 외부화, `tk-learn` semantic writer 단일화 |

## 번호와 역사 기록

과거 migration 과정에서 `0002-reflection-boundary.md`라는 별도 supersession marker가 만들어져 실제
ADR 0002와 번호가 중복됐습니다. 현재 tree에서는 실제 historical ADR 0002만 남기고 중복 marker는
삭제했습니다. Git history와 관련 issue에는 기존 기록이 보존됩니다.

ADR 0003이나 오래된 issue가 현재 tree에 없는 더 이른 ADR을 언급할 수 있습니다. 이는 당시 provenance를
가리키는 역사 참조이며, 누락된 과거 문서를 현재 계약으로 복원하라는 의미가 아닙니다.

새 ADR을 추가할 때는 catalog 개수, 모델 이름, 세부 CLI, 일시적인 ledger field처럼 빠르게 변하는 값을
architecture invariant로 고정하지 마세요. 그런 계약은 해당 skill과 executable eval이 소유합니다.
