---
name: tk-audit
description: "[user] 저장소를 읽기 전용으로 감사하고, 다른 실행자나 `tk-prep`이 재사용할 수 있는 우선순위가 있는 근거 기반 `AUD-*` `finding`을 작성합니다."
license: MIT
argument-hint: "[quick|standard|deep] [security|perf|tests|architecture|branch|next]"
disable-model-invocation: true
metadata:
  tigerkit:
    kind: user-invoked
    origin: shadcn/improve
    upstream-skill: improve
    relationship: adapted
---

# 감사

명시적으로 `$tk-audit` 또는 `/tk-audit`를 선택한 경우에만 사용합니다.
읽기 전용 코드베이스 자문이며 소스, 테스트, 설정, 이력을 수정하지 않습니다.
소유하는 유일한 산출물은 저장소 로컬의 `.tigerkit/audit.md`입니다.

## 호출

- `bare`: 표준 깊이로 모든 범주를 감사합니다.
- `quick | standard | deep`: 깊이와 제한된 커버리지를 바꿉니다.
- `security | perf | tests | architecture`: 하나의 범주에 집중합니다.
- `branch`: merge-base 변경과 직접 소비자를 확인하고 `introduced | pre-existing`를 표시합니다.
- `next`: 근거가 있는 방향 후보를 결함 finding과 분리합니다.

수정자를 조합할 수 있습니다. 구현, Seed 작성, 이슈 발행, worktree 생성은 하지 않습니다.

## 워크플로

1. 저장소 지침, 루트 설정, 검증 명령, 구조와 관련 Git 이력을 읽습니다.
2. [audit-playbook.md](references/audit-playbook.md)를 사용해 선택한 범주를 확인합니다.
3. 인용 근거를 다시 열어 중복, 의도된 동작, 잘못된 귀속을 제거합니다.
4. 영향 ÷ `effort`, `confidence`, `fix risk`, `dependency` 순으로 `finding`을 정렬합니다.
5. `.tigerkit/audit.md`를 원자적으로 갱신하고 안정적인 `AUD-*` ID와 상태를 보존합니다.

## Finding 계약

각 열린 finding에는 최소한 다음이 있어야 합니다.

- 안정적인 `AUD-*` ID와 제목
- 범주와 정확한 `path/line` 또는 `symbol` 근거
- 영향, `effort`, `fix risk`, `confidence`
- 관련 진입점과 저장소 관례
- 검증 `baseline`
- 짧은 `fix sketch`
- `dependency/order hint`
- 다음 경로 추천: `prep | investigate | no-action`

`finding`은 후보일 뿐 `Seed`, 티켓, 구현 계획, 승인 자체가 아닙니다.
`secret` 값은 복사하지 않고 위치와 자격 증명 유형만 기록합니다.

## 다음 실행자 인계

모든 finding에는 [executor-handoff.md](references/executor-handoff.md)를 적용합니다.
다음 실행자가 `audit` 대화 없이 이해할 수 있도록 `audited HEAD`, 정확한 경로/`symbol`,
현재 근거, 저장소 규칙, `in/out` 경계, 가정, 검증 명령과 `drift handling`을 포함합니다.

[plan-template.md](references/plan-template.md)의 품질 기준은 이 계약을 보완하지만,
`tk-audit` 자체가 별도 plan lifecycle을 만들지는 않습니다.

작업을 실제로 준비하려면 사용자가 `$tk-prep AUD-003`처럼 현재 `finding`을 출처로 줄 수 있습니다.
`tk-prep`은 `finding`을 현재 저장소 증거와 다시 대조해 실행 가능한 `Seed`로 준비합니다.
`Audit finding`만으로 제품 변경이나 원격 권한이 생기지 않습니다.

## 안전

부분 감사 중에는 기존 finding을 삭제하지 않고 미감사 범위를 표시합니다.
현재 HEAD에서 근거를 재현할 수 없으면 검증됐다고 주장하지 않습니다.
`.tigerkit/`은 로컬 scratch이며 전역 archive나 current pointer를 만들지 않습니다.

완료 시 핵심 `finding`과 감사하지 못한 범위를 간결하게 요약합니다.
