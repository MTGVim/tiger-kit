---
name: tk-code-review
description: "[user/auto] 고정 기준점 이후 diff를 Standards와 Spec 두 축으로 검토합니다. branch, PR, commit 범위 review나 구현 결과의 독립 검토에 사용하고, 코드를 직접 수정하는 요청에는 사용하지 않습니다."
metadata:
  tigerkit:
    kind: hybrid
    origin: mattpocock/skills
    upstream-skill: code-review
    relationship: adapted
---

# 코드 리뷰

사용자가 branch, PR, 특정 commit 이후 변경, spec 준수 또는 구현 결과의 독립 검토를 요청했거나 현재 변경에 수정과 분리된 review가 필요할 때 사용하세요. 코드 수정, 원인 불명 결함 진단 또는 전면 architecture 재설계 요청에는 사용하지 마세요.

## 계약

코드를 편집하거나 자동 재review하지 말고 `fixed point 확정 → diff 전체 확인 → Standards 근거 확인 → Spec 근거 확인 → 축별 finding → verdict` 순서를 지키세요. fixed point, diff 또는 필수 근거에 접근할 수 없으면 `Unverifiable`, 사용자 결정이나 권한이 없어 진행할 수 없으면 `Blocked`, 실제 위반이 있으면 `Changes requested`입니다.

모든 finding에는 severity, 제목, `file:line` evidence, basis, impact가 필요합니다. 일부 파일이나 축만 읽고 전체 review를 통과로 보고하지 마세요. `Pass`는 고정한 diff 전체와 적용 가능한 축을 검사했고 미검증 범위가 없을 때만 사용하세요.

## Workflow

1. `fixed point`: 입력은 사용자의 review 범위와 저장소 ref이고, 출력은 검증된 기준 commit입니다.
2. `diff inventory`: 입력은 기준 commit과 `HEAD`이고, 출력은 전체 diff·변경 파일·범위 log입니다.
3. `standards evidence`: 입력은 전체 diff와 저장소 지침이고, 출력은 적용 가능한 Standards 근거, 조건부 high-risk signal과 축별 findings입니다.
4. `spec evidence`: 입력은 전체 diff와 우선순위에 따른 spec/ticket source이고, 출력은 적용 가능한 Spec ID별 상태·누락·위반 findings 또는 `spec 없음` 판정입니다.
5. `axis verdict`: 입력은 Standards와 Spec 결과이고, 출력은 두 축을 합치지 않은 상태별 verdict입니다.
6. `receipt`: 입력은 fixed point, 검사 범위, findings, 미검증 항목이고, 출력은 `Fixed point / Standards / Spec / Verdict` 보고서입니다.

각 단계의 출력이 없거나 diff가 비어 있으면 다음 단계로 진행하지 마세요. Spec source가 없을 때는 Spec 축을 생략했다는 사실을 receipt에 남기고, 해당 축을 통과했다고 표현하지 마세요.

## Failure paths

- If fixed point가 유효하지 않으면 review를 시작하지 말고 `Unverifiable`로 종료합니다.
- If diff가 비어 있거나 일부만 읽히면 전체 `Pass`를 보고하지 말고 범위와 함께 `Unverifiable`로 종료합니다.
- If 적용 가능한 Spec source가 없으면 Spec 축을 생략하고 Standards와 합친 통과로 표현하지 않습니다.
- If finding 근거가 부족하면 추측을 추가하지 말고 미검증 항목을 receipt에 남깁니다.
- If 사용자가 수정을 요청하면 review에서 직접 편집하지 말고 `tk-implement` 같은 별도 구현 경로를 요청합니다.

## 🔴 CHECKPOINT · 🛑 STOP review 시작 경계

fixed point, 전체 diff, 적용 가능한 Standards/Spec 근거를 확인하기 전에는 review를 시작하거나 finding·verdict를 작성하지 마세요. fixed point나 diff에 접근할 수 없거나 사용자에게 기준점·결정이 필요하면 `Unverifiable` 또는 `Blocked` receipt에서 review를 멈추세요.

## Fixed point

검토 전에 commit, branch, tag, `main`, merge-base 표현 또는 `HEAD~N` 형태의 fixed point를 확정하세요. 사용자가 기준점을 제공하지 않았다면 물으세요.

```sh
git rev-parse <fixed-point>
git diff <fixed-point>...HEAD
git log <fixed-point>..HEAD --oneline
```

ref가 유효하지 않거나 diff가 비었거나 범위를 결정할 근거가 없으면 review를 시작하지 말고 이유를 보고하세요.

## 근거

Spec source 우선순위:

1. 사용자 제공 spec 또는 ticket
2. commit/branch의 issue 참조
3. 관련 `.tigerkit/spec.md`
4. 관련 `.tigerkit/tickets.md`
5. 저장소 문서
6. spec 없음

Spec이 없으면 Spec 축을 생략하고 명시하세요.

Standards source는 `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, 저장소 coding standards, 관련 module 지침, formatter/linter/typechecker가 검사하지 않는 규칙입니다.

## Review 축

Standards와 Spec을 구분하고 하나의 순위로 합치지 마세요.

Standards에서는 저장소 규칙 위반, duplication, scope creep, 소유권 혼란, shotgun-style 변경, 불필요한 pass-through, public interface와 implementation 경계 누출, 테스트하기 어려운 public seam, 서로 다른 변경 이유의 집중, side-effect/error boundary, speculative abstraction을 현재 diff에 근거해 검사하세요. 전면 재작성이나 요청 범위 밖 architecture를 제안하지 마세요.

Diff가 인증, 권한, 개인정보, 결제, dependency, migration, data loss, concurrency 또는 public API를 변경할 때만 [고위험 검토](references/risk-checks.md)에서 해당 lane을 선택하세요. Signal이 없으면 reference를 로드하거나 전체 N/A checklist를 만들지 말고 생략 이유만 receipt에 기록하세요. 이는 저장소 전체 vulnerability scan이나 전체 compliance 판정이 아닙니다.

Spec에서는 누락 또는 부분 구현, 요청하지 않은 동작, acceptance criteria 미충족, 잘못 구현된 동작, 테스트/검증 누락, 범위 밖 변경을 검사하세요. Source에 requirement/acceptance ID가 있으면 각 ID를 `implemented | missing | partial | unverified | not-applicable`로 판정하고 file:line evidence를 연결하세요. 하나라도 `missing | partial | unverified`이면 Spec 축 전체를 Pass로 표시하지 마세요. Source에 ID가 없으면 임의로 만들지 마세요.

현재 agent의 순차 검토가 기본입니다. 큰 diff에서 context 격리 가치가 명확할 때만 Standards reviewer 1명과 Spec reviewer 1명, 최대 2명을 사용할 수 있습니다. reviewer는 재위임하거나 코드를 편집하거나 동일 축으로 fan-out하거나 자동 재review하지 않습니다. Spec이 없으면 Spec reviewer를 만들지 마세요.

## Finding과 출력

각 finding 형식:

```text
Severity: Critical | Important | Minor
Title
Evidence: file:line
Basis: 저장소 규칙 또는 spec 근거
Impact
```

발견 사항이 없으면 해당 축에 없다고 명시하세요. 출력:

```text
## Fixed point
## Standards
## Spec
## Verdict
```

Verdict는 `Pass | Changes requested | Blocked | Unverifiable` 중 하나입니다. 수행한 축과 범위, 핵심 evidence, 미검증 항목, verdict를 receipt로 남기세요.

## DO NOT / ANTI-PATTERNS

- 기준점을 추정하거나 빈 diff·부분 diff를 전체 review로 통과시키지 마세요.
- review 대상 코드를 직접 수정하거나 자동 재review하지 마세요.
- 근거 없는 architecture 재작성과 요청 범위 밖 변경을 finding처럼 추가하지 마세요.
- High-risk signal 없이 전체 security checklist를 실행하거나 제한된 diff review를 repository-wide audit로 표현하지 마세요.
