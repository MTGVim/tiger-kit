---
name: tk-diagnosing-bugs
description: "[user/auto] 재현 가능한 feedback loop를 만든 뒤 버그를 최소화하고 가설을 검증합니다. 원인이 불분명한 실패, 간헐 오류 또는 성능 회귀에 사용하고, 원인과 수정 방법이 확정된 단순 변경에는 사용하지 않습니다."
metadata:
  tigerkit:
    kind: hybrid
    origin: mattpocock/skills
    upstream-skill: diagnosing-bugs
    relationship: adapted
---

# 버그 진단

증상은 있으나 원인을 모르거나, 간헐적·환경별 실패, 성능 회귀, 반복 재발, 재현·최소화·가설 검증이 필요한 경우 사용하세요. 조건문 반전, 누락된 prop, 명확한 빠진 분기처럼 원인과 수정 방법이 이미 확정된 변경에는 사용하지 마세요.

## Workflow

1. `feedback loop`: 입력은 사용자 증상·환경·권한이고, 출력은 재실행 가능한 red-capable artifact입니다.
2. `reproduce`: 입력은 loop artifact이고, 출력은 실제 실행 결과와 `red | not reproduced` 판정입니다.
3. `minimize`: 입력은 재현 결과이고, 출력은 증상을 보존하는 최소 입력·환경·실행 명령입니다.
4. `ranked hypotheses`: 입력은 최소 재현의 관찰 증거이고, 출력은 3–5개 가설과 각 반증 가능한 예측입니다.
5. `instrument`: 입력은 우선순위 가설과 최소 재현이고, 출력은 한 변수씩 구분 가능한 관측 증거입니다.
6. `fix`: 입력은 반증 결과와 확인된 원인이고, 출력은 최소 범위의 수정 또는 seam 부재 finding입니다.
7. `regression verification`: 입력은 수정과 원래 reproduction이고, 출력은 원래 증상·regression seam의 `green | failed` 결과입니다.
8. `cleanup/receipt`: 입력은 검증 결과와 임시 artifact 목록이고, 출력은 정리 결과·상태·미검증 및 앞선 근본 원인·fix·regression 출력의 참조를 연결한 receipt입니다. 앞선 본문을 복사하지 마세요.

필요한 입력·환경·권한이 없어 다음 단계로 진행할 수 없으면 `Blocked`, 실행했지만 재현 또는 회귀 증거를 확보하지 못하면 `Unverifiable`, 근본 원인이나 수정이 실패했음이 확인되면 `Fail`입니다. 어느 상태도 해결 완료로 보고하지 마세요.

기본 loop:

```text
feedback loop
→ reproduce
→ minimize
→ ranked hypotheses
→ instrument
→ fix
→ regression verification
→ cleanup
```

## Feedback loop gate

가설을 세우기 전에 사용자 증상을 잡을 red-capable feedback loop를 만드세요. failing test, curl/HTTP script, CLI fixture, browser script, trace replay, throwaway harness, 반복 재현 loop, differential comparison, deterministic performance measurement를 사용할 수 있습니다.

Feedback loop는 다음을 모두 만족해야 합니다.

1. 사용자의 실제 증상을 잡습니다.
2. agent가 다시 실행할 수 있습니다.
3. 최소 한 번 실제 실행합니다.
4. red/green 판정이 가능합니다.
5. 가능한 한 빠르고 반복 가능합니다.

재현할 수 없으면 시도한 방법, 부족한 환경 또는 artifact, 필요한 로그/HAR/fixture/trace/권한을 보고하세요. 추측으로 patch하거나 가설을 확정 사실처럼 표현하지 마세요.

## 🔴 CHECKPOINT · 🛑 STOP 가설·patch 경계

feedback loop의 다섯 조건을 실제 실행으로 확인하기 전에는 가설을 확정하거나 patch하지 마세요. 조건을 충족하지 못하면 필요한 증거와 함께 `Blocked` 또는 `Unverifiable`로 멈추세요.

## 가설과 수정

우선순위 가설 3~5개를 세우고 각 가설에 반증 가능한 예측을 붙이세요. 한 번에 변수 하나만 바꾸고 관찰 결과로 가설을 제거하세요. 증상과 근본 원인을 분리하고 공통 원인을 수정하세요.

올바른 regression seam이 있으면 최소 재현을 failing regression test로 바꾸고 red를 관찰한 뒤 fix, green, 원래 reproduction 재실행 순서로 검증하세요.

올바른 seam이 없으면 얕은 false-confidence test를 만들지 마세요. 실제 bug pattern을 재현할 public boundary 부재, 현재 구조가 regression 잠금을 방해한다는 점, 구조 개선은 bug fix 이후 별도 후속 작업이라는 점을 finding으로 기록하세요. 진단 중 architecture refactor를 먼저 시작하지 마세요.

임시 instrumentation과 throwaway debug artifact를 정리하세요. 상세 절차는 [조사 루프](references/investigation.md)를 참고하세요.

### Clean verification gate

instrumentation이 남은 상태에서 얻은 green은 최종 증거가 아닙니다. red를 만든 원래 reproduction의 명령·입력·fixture·seed/반복 횟수·판정에 필요한 환경을 기록하고, 임시 artifact를 제거한 뒤 작업 diff에 instrumentation이 남지 않았는지 확인하세요. 이어서 같은 전제로 원래 reproduction과 regression seam을 다시 실행하고 이 clean-state 결과만 완료와 commit의 근거로 사용하세요.

cleanup 전후에 reproduction 전제나 대상 source가 달라졌거나 cleanup 뒤 실패·간헐성이 돌아오면 이전 green을 폐기하세요. 원래 red와 비교 가능한 loop를 다시 만들 수 없으면 `Unverifiable`, clean-state 검증이 실패하면 `Fail`로 멈추고 commit하지 마세요.

## Commit 경계

사용자가 `tk-diagnosing-bugs`를 명시적으로 standalone 호출했고 실제 코드를 수정했다면 다음 조건을 모두 만족할 때 current branch에 commit하세요.

- 근본 원인 수정 완료
- 원래 reproduction green
- regression verification 성공
- 임시 instrumentation 제거 후 clean-state verification 성공
- 작업 diff를 기존 사용자 변경과 분리 가능

아직 `tk-implement` 작업이 진행 중이면 별도 commit하지 말고 진단 결과와 수정 사항을 현재 구현에 반환하세요. `tk-implement`가 최종 검증과 commit을 담당합니다.

일반 대화에서 자동으로 진단 규율을 적용한 것만으로 standalone commit 권한을 얻지 않습니다. 기존 작업의 commit 계약을 따르고, 독립 commit이 필요하면 명시 요청을 받으세요.

별도 요청 없이는 push, PR, merge, tag, release 또는 publish를 하지 마세요.

## 완료 보고

원래 증상, 근본 원인, fix, regression 증거, seam 부재 여부, cleanup, commit 또는 미commit 이유를 각각 한 번만 보고하세요. Receipt에는 상태(`Pass | Fail | Blocked | Unverifiable`), 미검증 항목과 해당 보고 항목의 참조만 기록하고 근본 원인·fix·증거 본문을 반복하지 마세요.

## DO NOT / ANTI-PATTERNS

- 재현 전 추측 patch, 반증하지 않은 원인 확정, false-confidence test를 만들지 마세요.
- 임시 instrumentation이나 throwaway debug artifact를 남기지 마세요.
- `tk-implement` 작업 안에서 별도 commit하거나 push하지 마세요.
