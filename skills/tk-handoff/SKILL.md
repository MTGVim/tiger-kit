---
name: tk-handoff
description: "[user/auto] 현재 세션 현황을 짧게 확인하거나, 다른 세션에 인계할 자료를 만들거나 기존 인수인계를 명시적으로 재개할 때 사용합니다. 일반 문서 요약이나 평범한 계속하기에는 적용하지 않습니다."
disable-model-invocation: false
argument-hint: "[current status | goal or target] [--output <path>|--resume]"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

<a id="handoff"></a>
# 인수인계

<a id="shared-references"></a>
## 공통 참조

현재 설치된 소유 스킬에서 해당 분기 조건에 따른 기준을 읽습니다. 소유 스킬이나 자원이 없거나
일치하지 않으면 해당 행동을 중단합니다. 기억, 다른 설치본이나 승인받지 않은 설치를 이용하지 말고
`tk-setup-skills`를 사용합니다. 읽기만으로 workflow 실행이나 변경 권한이 생기지 않습니다.

- 사용자 소유 결정·누락된 승인·미충족 선행 조건을 질문이나 질문 도구 입력으로 제시하기 직전에 [질문 라운드](../tk-questioning/references/questions.md)를 이번 작업에서 읽었는지 확인하고 누락했으면 먼저 읽습니다. 독립적인 결정과 승인은 각각 별도 질문으로 두며, 승인 선택지를 결정 질문에 섞지 않습니다.
- 사용자에게 완료 보고, 산출물 경로 인계나 여러 속성을 비교하는 채팅 응답을 전달하기 전에 [채팅 전달](../tk-writing/references/delivery.md)을 읽습니다. 해당 작업의 구체적인 출력 계약이 우선합니다.

<a id="ui-evidence"></a>
## UI 근거

기존 UI literal은 언어·대소문자·문장부호·공백까지 정확하게 유지하고 제안 문구와 구분합니다.
각 탐색 레이블과 연결에는 대상·환경·locale·역할이 일치하는 근거가 필요합니다.
제목·route·식별자만으로는 진입 경로를 입증할 수 없습니다. 서로 충돌하는 출처도 보존합니다.
필요하지만 뒷받침되지 않는 모든 레이블과 이동 단계는 확보한 출처, 한계와 필요한 최소 입력을
함께 보고합니다. 이를 탐색 경로로 제시하지 않습니다. 사용자가 제공한 텍스트는 독립적인 관찰이
아니며, 그 텍스트가 뒷받침하는 주장만 해소합니다.

이 담당자의 조사 범위에서 UI 근거를 수집하거나 검증하기 전에
[UI 근거 수집](../tk-ui-evidence/references/ui-evidence.md)을 읽습니다. UI와 무관한 분기와 전달만 하는
분기는 수집을 건너뜁니다. 새 조사를 시작하지 말고 제공된 근거와 누락 사항을 전달합니다.

<a id="approval-continuity"></a>
## 승인 연속성

같은 작업에 대한 유효한 승인을 턴과 자식 단계 사이에서 재사용합니다. 변경 전 기준·변경 후 단계도
포함하며, 기존 담당자를 통해 승인된 작업만 계속합니다. 자식 단계·변경 전 기준 근거를 반환하고
승인된 담당 작업을 재개합니다. 단계 상태는 완료가 아닙니다. 새로운 중대한 결정, 범위·권한 변경이나
사용자만 제공할 수 있는 누락 입력이 있을 때만 질문합니다. 호출과 복구된 산출물은 권한을 부여하지
않습니다. 원격 행동과 파괴적 행동에는 행동·대상에 대한 명시적 승인이 필요하며, 로컬 승인에서 추론하지 않습니다.

요청에서 분기 하나를 선택합니다. 현재 세션의 상태나 현황 파악 요청이면
[대화만으로 현황 파악하기](references/orientation.md)를 읽고 간결한 요약을 반환한 뒤,
산출물을 작성하거나 작업을 재개하지 않고 해당 턴을 끝냅니다. 이 보고 경계는 기존 승인을 철회하지
않습니다. 이후 재개 지시가 있으면 그 승인을 재사용할 수 있습니다. 명시적인 인수인계 생성 요청이면
아래 산출물 workflow를 계속합니다. `--resume`이면 작성·재개 체크포인트 이후
[재개와 변동 분류](references/resume.md)를 읽고 최신 상태를 검증한 다음 계속합니다.
일반적인 문서 요약이나 평범한 “계속” 요청은 어느 분기도 선택하지 않습니다. 상태 요약을 위해
지속 보존할 인수인계를 만들거나, 내용을 채우려고 다른 세션이나 원격 PR을 조회하지 않습니다.

역할을 구분합니다.

- `.tigerkit/seed.md`: 무엇을, 왜, 어떤 조건에서 해야 하는지 정의하는 작업 계약입니다.
- `.tigerkit/handoff.md`: 수행한 작업과 현재 상태를 기록하는 진행 `snapshot`입니다.

현재 작업의 Seed가 있으면 계약을 복사하지 말고 참조합니다. 정당한 direct/no-Seed 작업은 Seed를 만들 필요가 없습니다. 다른 세션에서 이해할 수 있도록 최소 목표, 범위·제외 사항, AC와 확인된 승인 경계를 Handoff 자체에 기록합니다.

<a id="new-handoff"></a>
## 새 인수인계

현재 저장소 근거를 읽습니다.

- `branch` / `HEAD` / `worktree`
- 정확한 `path`와 `status`를 확인합니다. 현재 `Seed`가 있는 경우에 해당합니다.
- 실제 변경 파일
- 실제 실행한 명령
- 실제 검증 결과
- 완료한 작업과 남은 작업
- 현재 차단 요인과 다음 행동

관찰한 사실만 `verified`로, 사용자와 확인한 결정만 `confirmed`로 표시합니다.
실행하지 않은 명령, 이전 주장과 모델의 추론은 `unverified`입니다.

기본 경로는 `.tigerkit/handoff.md`입니다. 같은 디렉터리의 임시 파일에 작성하고, 대상을 원자적으로 교체한 뒤 다시 읽습니다.
산출물을 만드는 것 자체는 제품, Git이나 원격 상태를 변경할 권한을 부여하지 않습니다.

Handoff에는 적어도 다음 의미를 보존합니다.

```text
Goal/Seed: <seed path 또는 current goal reference>
Status: pending | in_progress | completed | aborted | Blocked | Unverifiable
Repository state: <branch, HEAD, worktree>
Decisions: <confirmed progress-relevant decisions>
Changed files: <observed paths | none>
Commands: <actually executed commands | none>
Verification: <check/result/evidence>
Completed work: <done items | none>
Remaining work: <unfinished items | none>
Open questions: <required decisions | none>
Risks: <remaining failure/regression risk>
Next step: <one executable immediate action>
Resume hints: <environment/order/command hints>
Disposition: reported | applied | pending
```

`Disposition`은 이 인수인계에 기록된 작업을 설명합니다. 조사·보고 전용 작업은 `reported`,
이미 수행한 승인된 변경은 `applied`, 아직 적용하지 않은 제안은 `pending`입니다. 권한을 부여하지 않습니다.

Seed가 있는 작업은 정확한 계약 절·경로를 참조합니다. direct/no-Seed 작업은 위의 최소한의 독립적인 계약을 기록하고 `Seed: none`을 명시합니다. 관련 없거나 모호한 이전 Seed는 제외합니다.

<a id="-checkpoint---stop--writeresume-boundary"></a>
## 🔴 CHECKPOINT · 🛑 STOP · 작성·재개 경계

새 `Handoff`를 작성하거나 `--resume`을 계속하기 전에 다음을 확인합니다.

- branch, HEAD, worktree와 필요한 근거를 새로 읽습니다. 새 Handoff가 미리 존재할 필요는 없으며, 선택적인 Seed가 없는 것도 정당할 수 있습니다. 재개할 때는 참조한 Handoff와 작업에 연결된 Seed를 읽을 수 있어야 합니다. 필요한 산출물이 없거나 읽을 수 없으면 `Unverifiable`이며, 추측으로 재구성할 권한이 생기는 것은 아닙니다.
- 근거가 충돌하면 STOP하고 `Blocked`로 표시하며, `Seed` 계약에 변동이 있어도 동일하게 처리합니다. 두 조건 모두 `Handoff` 안에서 해결하지 않습니다.
- 원자적 교체를 완료할 수 없거나 다시 읽기에 실패하면 작성 전에 STOP합니다. 기본적으로 `.tigerkit/handoff.md`를 사용하고, 명시적인 `--output <path>`를 정확히 따릅니다.
- 제품, Git이나 원격 발행의 승인 경계에서는 STOP합니다. 산출물은 해당 권한을 부여하지 않습니다.
- 위 조건에 해당하지 않으면 일상적인 산출물 갱신에 추가 질문을 하지 않고 계속합니다.

<a id="output"></a>
## 출력

새 `handoff`를 성공적으로 생성한 뒤에는 채팅에 경로, 현재 상태와 다음 행동만 짧게 표시합니다.
`Handoff` 본문 전체나 근거 대장을 출력하지 않습니다.

재개할 때는 완료한 작업, 남은 작업, 차단 요인과 바로 다음 행동을 사람이 이해하기 쉽게 설명합니다.

`.tigerkit/`을 보관소, 현재 항목 pointer나 전역 상태로 사용하지 않습니다.
ignore 수정은 산출물 경로 설정으로 제한하고, 자동으로 commit하거나 발행하지 않습니다.

<a id="artifact-paths"></a>
## 산출물 경로

승인된 산출물 작성, checkout·전송·ignore 설정이나 임시 입력 소비 전에
[산출물 경로](../tk-artifacts/references/artifact-paths.md)를 읽습니다. 저장소 임시 작업에는 소유권이
확인된 안전한 nonsymlink 경로와 입증된 Git 제외를 사용합니다. 점검에 실패하면 해당 파일 분기를
중단합니다. 명시적인 최종 목적지와 담당자별 기본값을 보존합니다. 미리 채워진 입력은 완료된 입력이 아닙니다.
정리 대상은 기록된 리터럴 형태의 해석된 절대 경로 중 해당 실행이 소유한 경로뿐입니다.
cwd 상대 경로나 glob은 사용하지 않습니다.
