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

## CHECKPOINT / STOP

fixed point나 diff를 해석·접근할 수 없으면 `Unverifiable`, 사용자에게 기준점이나 결정이 필요하면 `Blocked`로 멈추세요. 그 상태에서는 review를 시작하지 말고 receipt를 남기세요.

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

Spec에서는 누락 또는 부분 구현, 요청하지 않은 동작, acceptance criteria 미충족, 잘못 구현된 동작, 테스트/검증 누락, 범위 밖 변경을 검사하세요.

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
