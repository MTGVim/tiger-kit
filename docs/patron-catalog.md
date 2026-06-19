# Patron Catalog

Patron은 worker가 아니라 decision policy다. Patron은 temporary decision point에서 판단만 제공하고, Driver가 결과를 merge한다.

## Schema

각 Patron은 최소 필드를 가진다.

```yaml
id: <stable id>
display_name: <user-facing name>
summary: <one sentence>
source: source-derived | tigerkit-native
status: available | candidate | deprecated
use_when:
  - <decision type>
avoid_when:
  - <case>
decision_style: <how it decides>
default_outputs:
  - <output field>
ledger_policy: <what to record>
```

## Source-derived Patrons

아래 Patron은 public agent-skill 역할에서 이름과 관점을 가볍게 차용한다. TigerKit은 외부 도구를 직접 내장하지 않고 decision policy만 제공한다.

### reviewer

```yaml
id: reviewer
display_name: Reviewer
summary: 코드 품질, 변경 준비도, review risk를 판단한다.
source: source-derived
status: available
use_when:
  - code quality / merge readiness
avoid_when:
  - 요구사항 자체가 불분명한 경우
  - security boundary가 핵심인 경우
decision_style: current evidence와 repo convention을 기준으로 actionable risk를 좁힌다.
default_outputs:
  - decision
  - review_risks
  - required_changes
  - confidence
ledger_policy: 판단 근거 파일, diff, rule ref를 기록한다.
```

### tester

```yaml
id: tester
display_name: Tester
summary: 검증 범위와 test strategy를 판단한다.
source: source-derived
status: available
use_when:
  - verification / test scope
avoid_when:
  - product decision이 아직 열려 있는 경우
decision_style: change risk와 available verifier를 맞춰 최소 faithful proof를 고른다.
default_outputs:
  - verification_plan
  - required_checks
  - skipped_checks
  - confidence
ledger_policy: 실행할 검증, 생략 이유, blocking dependency를 기록한다.
```

### security

```yaml
id: security
display_name: Security
summary: 보안 경계, 권한, secrets, destructive action 위험을 판단한다.
source: source-derived
status: available
use_when:
  - security boundary / permissions
avoid_when:
  - purely visual or copy-only decision
decision_style: Critical/High risk를 사용자 승인 gate로 되돌린다.
default_outputs:
  - risk_level
  - decision
  - required_user_approval
  - mitigation
ledger_policy: 위험 축, 승인 필요 여부, 금지 action을 기록한다.
```

### webperf

```yaml
id: webperf
display_name: Web Performance
summary: 웹 runtime 성능과 user-visible latency risk를 판단한다.
source: source-derived
status: available
use_when:
  - web runtime performance
avoid_when:
  - backend-only or non-web decision
decision_style: 측정 가능한 runtime impact와 user-visible path를 우선한다.
default_outputs:
  - performance_risk
  - measurement_needed
  - recommendation
  - confidence
ledger_policy: 관측/미관측 metric, perf budget, follow-up 측정을 기록한다.
```

## TigerKit-native Patrons

### steward

```yaml
id: steward
display_name: Steward
summary: repo convention, reuse, local rule consistency를 판단한다.
source: tigerkit-native
status: available
use_when:
  - repo convention / reuse
avoid_when:
  - source contract 자체가 없는 경우
decision_style: 기존 자산 재사용과 public label 보존을 우선한다.
default_outputs:
  - convention_match
  - reuse_candidate
  - required_alignment
  - confidence
ledger_policy: 확인한 docs/rules/files와 선택한 convention을 기록한다.
```

### simplifier

```yaml
id: simplifier
display_name: Simplifier
summary: scope reduction, essentialism, YAGNI를 판단한다.
source: tigerkit-native
status: available
use_when:
  - simplification / scope reduction
avoid_when:
  - compliance or safety requirement가 확정된 경우
decision_style: 요구사항 충족에 불필요한 complexity를 제거한다.
default_outputs:
  - keep
  - cut
  - defer
  - rationale
ledger_policy: 제거/연기한 범위와 이유를 기록한다.
```

### cartographer

```yaml
id: cartographer
display_name: Cartographer
summary: 구조 지도, flowchart, before/after 설명을 만든다.
source: tigerkit-native
status: available
use_when:
  - visual explanation / structure map
avoid_when:
  - text-only decision이 충분한 경우
decision_style: decision 구조를 layer, flow, ownership map으로 분해한다.
default_outputs:
  - map
  - key_paths
  - decision_points
  - legend
ledger_policy: 어떤 구조가 evidence이고 어떤 구조가 interpretation인지 분리한다.
```

## Presets

| Preset | Patrons |
|---|---|
| Minimal | reviewer, tester, security |
| Web Frontend | steward, reviewer, tester, security, webperf, cartographer |
| Migration | steward, reviewer, tester, simplifier, cartographer |
| TigerKit Maintainer | steward, reviewer, tester, simplifier, cartographer, security |
| Full | steward, reviewer, tester, security, webperf, simplifier, cartographer |
