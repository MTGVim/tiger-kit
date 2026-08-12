# ADR 0002: Local reflection targets and durable ledger

- Status: Superseded by ADR 0003
- Date: 2026-07-31
- Candidate release: v21.0.9
- Superseded by: `0003-external-memory-and-central-skill-evolution.md`

> 역사 기록입니다. 이 ADR은 제거된 `tk-reflect`의 local rule mutation과
> `.tigerkit/reflect.md` 계약을 설명하며 **현재 TigerKit 실행 계약이 아닙니다**.
> 현재 persistent memory/rule lifecycle 경계와 skill evolution ownership은 ADR 0003을 따릅니다.

## 당시 배경

당시 TigerKit은 successful drive 뒤 reflection을 수행하고, repository/user rule 후보를
제한적으로 적용하는 흐름을 갖고 있었습니다. 실제 사용에서 다음 문제가 관찰됐습니다.

1. 이미 untracked/ignored인 repository-local rule도 Git 상태를 확인하기 전에 위험 대상으로
   오분류되어 멈출 수 있었습니다.
2. `git check-ignore` exit `1`을 오류처럼 취급해 untracked-visible local rule을 다루지 못했습니다.
3. reflection 결과가 어떤 실행에서는 `.tigerkit/reflect.md`에 남고 어떤 실행에서는 chat에만 남아
   investigation surface가 일관되지 않았습니다.

## 당시 결정

이 ADR은 다음 historical behavior를 승인했습니다.

- 완료된 `tk-reflect` 실행은 bounded `.tigerkit/reflect.md`를 기록합니다.
- repository target은 `git ls-files`, `git check-ignore`, `git status`로 실제 상태를 먼저 분류합니다.
- 검증된 기존 untracked repository rule 또는 user-level current-host-native rule 하나만 제한적으로
  local apply할 수 있습니다.
- local mutation은 before-image와 hash를 보존하고, 실패 시 exact rollback을 검증합니다.
- reflection 변경은 product commit과 섞지 않고 commit-free local mutation으로 유지합니다.

## Supersession

Issue #224와 ADR 0003에서 TigerKit은 persistent memory와 rule lifecycle 자체를 제품 경계 밖으로
이동했습니다. 그 결과 다음 historical owner는 모두 retired되었습니다.

- `tk-reflect`
- `.tigerkit/reflect.md` lifecycle ownership
- repository/user rule promotion 또는 local apply
- reflection backup/rollback workflow
- drive의 post-verification reflection tail

따라서 이 ADR의 Git 상태 판정, local target eligibility, rollback, reflection ledger 요구사항을
현재 skill에 적용하거나 복원해서는 안 됩니다.

현재 장기 결정은 ADR 0003을, 실제 공개 skill과 실행 동작은 `README.md`, 현재
`skills/tk-*/SKILL.md`, 해당 eval 정본을 참조하세요.
