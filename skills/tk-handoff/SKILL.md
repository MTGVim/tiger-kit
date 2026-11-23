---
name: tk-handoff
description: "[user/auto] 현재 작업의 인수인계 스냅샷을 파일로 저장하거나 기존 스냅샷을 선택해 재개합니다. 인자 없는 호출은 반드시 파일을 생성합니다. 일반 현황 질문에는 적용하지 않습니다."
disable-model-invocation: false
argument-hint: "[topic] | resume [<handoff-path>]"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---
<!-- tigerkit:universal-authoring-gate -->
## 공통 저작 품질 관문

이 스킬에서 질문·메시지·설명·보고서·Markdown·HTML·대본·자막·문서·스킬 본문 등 사람이 읽는 텍스트를 **새로 작성하거나 의미·표현을 수정하기 전에**, 설치된 `tk-writing`의 [모든 저작의 공통 관문](../tk-writing/references/authoring-gate.md)과 [명확한 글쓰기](../tk-writing/references/clear-writing.md)를 이번 작업에서 읽고 적용합니다. 최종 산출물을 인계하기 전에 같은 기준으로 원고를 검사하고 문제를 수정합니다. 이미 읽은 기준을 반복 로드하거나 별도 재작성 스킬·에이전트·승인 라운드를 추가하지 않습니다. 코드·명령·식별자·기계 판독 형식·인용과 고정 문구는 보호하며, 이 참조로 변경·전송·발행 권한이 생기지 않습니다. 이 스킬이 작성 작업을 수행하지 않는 경우에는 추가 읽기가 필요하지 않습니다.
<!-- /tigerkit:universal-authoring-gate -->

`tk-handoff`의 사용자 동작은 **인수인계 생성**(인자 없음 또는 주제 지정)과 **`resume`**(경로 선택 또는 지정) 둘뿐입니다. 인자 없이 호출하면 반드시 파일을 만듭니다. 일반 현황 질문·문서 요약·평범한 “계속”에는 이 스킬을 자동 적용하지 않습니다. `현황만`, `output`, `strategy`를 별도 명령이나 모드로 제공하지 않습니다. 주제 문자열이나 경로 내부 단어를 명령으로 오인하지 않습니다. 기존 승인과 실행 경계는 그대로 유지합니다.


<a id="handoff"></a>
# 인수인계

<a id="shared-references"></a>
## 공통 참조

현재 설치된 소유 스킬에서 해당 분기 조건에 따른 기준을 읽습니다. 소유 스킬이나 자원이 없거나
일치하지 않으면 해당 행동을 중단합니다. 기억, 다른 설치본이나 승인받지 않은 설치를 이용하지 말고
`tk-setup-skills`를 사용합니다. 읽기만으로 workflow 실행이나 변경 권한이 생기지 않습니다.

- 기존 Task를 인계하거나 다른 세션에서 재개하는 명시적인 요청이라면 [호스트 Task 생명주기](../tk-tasks/references/lifecycle.md)를 읽어 원래 Task ID·담당자와 상태를 대조합니다. Handoff 산출물 작성 자체를 이유로 Task를 중복 생성하지 않고, 실제 재개·차단 근거를 Task 소유자에게 반환합니다.
- 사용자 소유 결정·누락된 승인·미충족 선행 조건을 질문이나 질문 도구 입력으로 제시하기 직전에 [질문 라운드](../tk-questioning/references/questions.md)를 이번 작업에서 읽었는지 확인하고 누락했으면 먼저 읽습니다. 독립적인 결정과 승인은 각각 별도 질문으로 두며, 승인 선택지를 결정 질문에 섞지 않습니다.
- 사용자에게 완료 보고, 산출물 경로 인계나 여러 속성을 비교하는 채팅 응답을 전달하기 전에 [채팅 전달](../tk-writing/references/delivery.md)을 읽습니다. 해당 작업의 구체적인 출력 계약이 우선합니다.

<a id="ui-evidence"></a>
## UI 근거

기존 UI 문구는 언어·대소문자·문장부호·공백을 보존하고 제안 문구와 구분합니다. 근거 없는 탐색 경로를 안내하지 않습니다.
UI 문구·경로를 인용·검증·전달할 때 [UI 근거](../tk-ui-evidence/references/ui-evidence.md)를 읽고, 대상에 맞는 근거와 충돌·미확인 사항을 보존합니다.
전달만 하는 분기는 새 조사를 시작하지 않으며, 수집은 담당자의 기존 조사 권한 안에서만 수행합니다. UI와 무관하면 이 참조를 읽지 않습니다.

<a id="approval-continuity"></a>
## 승인 연속성

같은 작업에 대한 유효한 승인을 턴과 자식 단계 사이에서 재사용합니다. 변경 전 기준·변경 후 단계도
포함하며, 기존 담당자를 통해 승인된 작업만 계속합니다. 자식 단계·변경 전 기준 근거를 반환하고
승인된 담당 작업을 재개합니다. 단계 상태는 완료가 아닙니다. 새로운 중대한 결정, 범위·권한 변경이나
사용자만 제공할 수 있는 누락 입력이 있을 때만 질문합니다. 호출과 복구된 산출물은 권한을 부여하지
않습니다. 원격 행동과 파괴적 행동에는 행동·대상에 대한 명시적 승인이 필요하며, 로컬 승인에서 추론하지 않습니다.

명시적인 `resume`이면 [인수인계 재개](references/resume.md)에 따라 파일을 선택하고,
작성·재개 체크포인트 이후 현재 상태를 검증하여 원래 작업을 계속합니다. 그 외 명시적인
`tk-handoff` 호출은 **기본적으로 새 인수인계 파일을 생성**하고 저장·재독 후 턴을 종료합니다.
인자가 없는 호출도 작성 분기입니다. 다른 세션 내용을 조회해 현재 세션의 사실인 것처럼
합치지 않으며, 대화 현황 요약만 반환하는 분기는 없습니다.

역할을 구분합니다.

- `.tigerkit/seed.md`: 무엇을, 왜, 어떤 조건에서 해야 하는지 정의하는 작업 계약입니다.
- `.tigerkit/handoffs/<YYYYMMDD-HHmmss>-<topic>.md`: 현재 worktree에서 작성한 **독립적인 진행 스냅샷**입니다. 기존 파일을 덮어쓰지 않습니다.
- 기존 `.tigerkit/handoff.md`: 과거 단일 파일 형식입니다. 신규 작성 대상이 아니며 `resume`의 레거시 후보로만 유지합니다.
- 명시적인 장기 작업 인계에만 전략 문서를 연결합니다. [장기 전략](references/strategy.md)을 읽되 새 스냅샷과 연결된 독립 파일을 사용합니다. 일반적인 인계에는 추가하지 않습니다.

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

기본 목적지는 **현재 Git worktree 루트**의 `.tigerkit/handoffs/`입니다. 파일명은 실제 작성 시점의
로컬 시간으로 `YYYYMMDD-HHmmss-<topic>.md`를 만듭니다(예: `20261124-015033-login-refactor.md`).
실제 시간대 오프셋을 문서의 `Created at`에 남기며, 주제는 현재 작업의 목표·Task 이름에서 짧은
소문자 영문 `kebab-case`로 추출합니다. 주제를 제공했다면 그것을 우선합니다. 실제 목표를 확인할
수 없으면 추측하지 않고 필요한 최소한의 주제·작업 맥락만 묻습니다.

동일 주제도 새 파일을 만들고, 동일 초·파일명 충돌 시 `-02`, `-03` 같은 고유 접미사를 붙입니다.
경로의 기존 파일이나 심볼릭 링크를 덮어쓰지 않습니다. 같은 디렉터리에 실행 소유 임시 파일을
작성하고 **대상 경로가 여전히 존재하지 않을 때만 배타적·원자적으로 발행**한 뒤 다시 읽어 확인합니다.
동시 작성으로 경합하면 다른 고유 이름으로 재시도합니다. 단순 `rename`이나 `replace`로 기존
스냅샷을 덮어쓰지 않습니다. 인계 생성은 스냅샷만 저장하며 제품·Git·원격 변경 권한을 부여하지 않습니다.

새 문서에는 주제, 작성 시각·시간대, 저장소 및 **정확한 worktree 절대 경로**, 알 수 있으면 호스트
세션/Task 식별자를 기록합니다. 다른 세션 ID를 만들어 내거나 접근 가능한 대화가 있다고 추측하지 않습니다.
기존 `.tigerkit/handoff.md`는 만들거나 갱신하지 않습니다. 재개 시에는 `resume <path>`로
정확한 파일을 지정할 수 있고, 인자 없는 `resume`은 [재개 절차](references/resume.md)로 후보를 선택합니다.
산출물을 만드는 것 자체는 제품, Git이나 원격 상태를 변경할 권한을 부여하지 않습니다.

Handoff에는 적어도 다음 의미를 보존합니다.

```text
Topic: <current work item, not guessed>
Created at: <local ISO 8601 timestamp with timezone offset>
Worktree: <verified absolute worktree root>
Session/Task: <verified identifiers | unverified>
Goal/Seed: <seed path 또는 current goal reference>
Status: pending | in_progress | completed | aborted | Blocked | Unverifiable
Repository state: <branch, HEAD, worktree>
Decisions: <confirmed progress-relevant decisions>
Approval boundary: <confirmed prior approvals, exact targets, unapproved actions>
Changed files: <observed paths | none>
Commands: <actually executed commands | none>
Verification: <check/result/evidence>
Completed work: <done items | none>
Remaining work: <unfinished items | none; criterion IDs must include definitions or exact definition file paths>
Open questions: <required decisions | none>
Risks: <remaining failure/regression risk>
Owner skill: <verified owner skill and remaining generation/verification/delivery phase | none>
Next step: <one executable immediate action>
Resume hints: <owner phase plus environment/order/command hints>
Disposition: reported | applied | pending
```

`Remaining work`에서 이전 세션에만 정의된 기준 ID를 참조할 때는 각 ID마다 실행 가능한 한 줄 정의 또는 정의가 있는 정확한 파일 경로를 함께 적습니다. ID 이름만 남겨 재개한 세션이 기준을 재구성하도록 하지 않습니다.

`Disposition`은 이 인수인계에 기록된 작업을 설명합니다. 조사·보고 전용 작업은 `reported`,
이미 수행한 승인된 변경은 `applied`, 아직 적용하지 않은 제안은 `pending`입니다. 권한을 부여하지 않습니다.

Seed가 있는 작업은 정확한 계약 절·경로를 참조합니다. direct/no-Seed 작업은 위의 최소한의 독립적인 계약을 기록하고 `Seed: none`을 명시합니다. 관련 없거나 모호한 이전 Seed는 제외합니다.

<a id="-checkpoint---stop--writeresume-boundary"></a>
## 🔴 CHECKPOINT · 🛑 STOP · 작성·재개 경계

새 `Handoff`를 작성하거나 `resume`을 계속하기 전에 다음을 확인합니다.

- branch, HEAD, worktree와 필요한 근거를 새로 읽습니다. 새 Handoff가 미리 존재할 필요는 없으며, 선택적인 Seed가 없는 것도 정당할 수 있습니다. 재개할 때는 참조한 Handoff와 작업에 연결된 Seed를 읽을 수 있어야 합니다. 필요한 산출물이 없거나 읽을 수 없으면 `Unverifiable`이며, 추측으로 재구성할 권한이 생기는 것은 아닙니다.
- 근거가 충돌하면 STOP하고 `Blocked`로 표시하며, `Seed` 계약에 변동이 있어도 동일하게 처리합니다. 두 조건 모두 `Handoff` 안에서 해결하지 않습니다.
- 새 고유 스냅샷을 **기존 파일 덮어쓰기 없이** 원자적으로 발행할 수 없거나 다시 읽기에 실패하면 성공으로 보고하지 않습니다. `.tigerkit/handoffs/`의 경로·제외·소유권 안전 조건을 지킵니다. 파일명 경합은 고유 접미사로 해결합니다.
- 제품, Git이나 원격 발행의 승인 경계에서는 STOP합니다. 산출물은 해당 권한을 부여하지 않습니다.
- 위 조건에 해당하지 않으면 일상적인 산출물 갱신에 추가 질문을 하지 않고 계속합니다.

<a id="output"></a>
## 출력

새 `handoff`를 성공적으로 생성한 뒤에는 채팅에 경로, 현재 상태와 다음 행동만 짧게 표시합니다.
`Handoff` 본문 전체나 근거 대장을 출력하지 않습니다.

재개할 때는 완료한 작업, 남은 작업, 차단 요인과 바로 다음 행동을 사람이 이해하기 쉽게 설명합니다.

`.tigerkit/`을 현재 항목 pointer나 전역 실행 상태로 사용하지 않습니다. `.tigerkit/handoffs/`는 현재 worktree의 독립적인 인계 스냅샷 보관 장소입니다. 해당 worktree를 정리하면 무시된 인계 파일도 사라지므로, 정리 전에 필요한 스냅샷의 별도 보존 여부를 확인하고 허가 없이 삭제하지 않습니다. 과거 `Goal run:` 인계가 남아 있으면 정확한 장부 경로와 원래 승인·Git 상태를 읽기 전용으로 확인하되, 제거된 실행기를 재개하거나 일반 Handoff를 근거로 작업을 실행하지 않습니다. 필요하면 새로운 계획 준비를 별도로 요청합니다. 컨텍스트 보호로 자동 인계하는 경우에도 새 고유 파일의 저장·재독 성공과 정확한 경로를 확인한 후 턴을 종료합니다.
ignore 수정은 산출물 경로 설정으로 제한하고, 자동으로 commit하거나 발행하지 않습니다.

<a id="artifact-paths"></a>
## 산출물 경로

승인된 산출물 작성, checkout·전송·ignore 설정이나 임시 입력 소비 전에
[산출물 경로](../tk-artifacts/references/artifact-paths.md)를 읽습니다. 저장소 임시 작업에는 소유권이
확인된 안전한 nonsymlink 경로와 입증된 Git 제외를 사용합니다. 점검에 실패하면 해당 파일 분기를
중단합니다. 명시적인 최종 목적지와 담당자별 기본값을 보존합니다. 미리 채워진 입력은 완료된 입력이 아닙니다.
정리 대상은 기록된 리터럴 형태의 해석된 절대 경로 중 해당 실행이 소유한 경로뿐입니다.
cwd 상대 경로나 glob은 사용하지 않습니다.
