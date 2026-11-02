---
name: tk-prototype
description: "[user/auto] 비교가 필요한 일회성 UI 또는 로직 prototype을 만들고 실행합니다. production 구현이나 대화형 아이디어 탐색에는 사용하지 않습니다."
disable-model-invocation: false
argument-hint: "<idea, screenshot, spec, ticket, code, or design reference>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

<a id="comparison-prototype"></a>
# 비교 prototype

<a id="shared-references"></a>
## 공통 참조

분기 조건에 해당하는 기준은 현재 설치된 소유자에게서 읽습니다. 소유자나 자원이 없거나 일치하지 않으면 해당 행동을 중단합니다. 기억, 다른 설치본이나 승인받지 않은 설치로 대신하지 말고 `tk-setup-skills`를 사용합니다. 읽기는 워크플로나 변경 권한을 부여하지 않습니다.

- 사용자 소유 결정·누락된 승인·미충족 선행 조건을 질문이나 질문 도구 입력으로 제시하기 직전에 [질문 라운드](../tk-questioning/references/questions.md)를 이번 작업에서 읽었는지 확인하고 누락했으면 먼저 읽습니다. 독립적인 결정과 승인은 각각 별도 질문으로 두며, 승인 선택지를 결정 질문에 섞지 않습니다.
- 사용자에게 완료를 보고하거나 산출물 경로를 인계하거나 채팅에서 여러 속성을 비교하기 전에 [채팅 전달](../tk-writing/references/delivery.md)을 읽습니다. 작업의 구체적인 출력 계약이 우선합니다.

<a id="approval-continuity"></a>
## 승인 연속성

동일 작업에 유효한 승인을 턴과 하위 단계(변경 전 기준/변경 후 포함)에 걸쳐 재사용하고, 기존 소유자를 통해 승인된 작업만 계속합니다. 하위 단계·변경 전 기준의 근거를 반환하고 승인된 소유자 작업을 재개합니다. 단계 상태는 완료가 아닙니다. 새로운 중요 결정, 범위·권한 변경 또는 사용자만 제공할 수 있는 입력의 누락이 있을 때만 묻습니다. 호출과 복원된 산출물은 권한을 부여하지 않습니다. 원격 작업과 파괴적 작업에는 명시적인 행동·대상 승인이 필요하며 로컬 승인에서 추론하지 않습니다.

입력으로 `prompt`, 아이디어, 스크린샷, `spec`, `ticket`, 코드 또는 디자인 참조를 받습니다. 독립 산출물은 `.tigerkit/prototypes/<slug>/` 아래에 둡니다. 쓰기 전에 Git이 `.tigerkit/`을 실제로 무시하고 그 아래 경로가 추적되지 않음을 입증합니다. 유효 규칙은 디렉터리별 설정, 로컬 exclude 또는 사용자 수준 exclude 설정에서 올 수 있습니다. ignore 적용이 없으면 산출물 경로 설정을 사용하고 쓰기 전에 다시 점검합니다. 외부 임시 작업 공간으로 대체하지 않습니다. 선택한 런타임에 필요한 경우에만 저장소 고유 route/harness를 허용하며 실행 소유 파일만 기록하고 정리합니다.

<a id="workflow"></a>
## 워크플로

1. `hypothesis/success criteria`: 아이디어, 참조와 검증 질문에서 측정 가능한 기준을 도출합니다.
2. `temporary path/boundary`: 저장소 사전 점검을 수행하고 기존 도구 체계·UI 스택·구성 요소·토큰, 임시 경로, 산출물 소유권과 `fake | real` 통합 경계를 선택합니다.
3. `variants/harness`: 비교에 답하는 데 필요한 대안만 만들거나 현실적인 예시 I/O를 사용하는 `harness`를 만듭니다.
4. `run`: 선택한 `variant`/`harness`를 실행하고 실제 출력 또는 스크린샷과 명령 결과를 수집합니다.

각 실행을 `## Tested` 아래에 다음 receipt 필드로 기록합니다. 명령을 요약하지 말고 실제 실행한 값을 정확히 기록합니다.

```text
Command: <exact command and arguments>
CWD: <absolute worktree or route path>
Exit code: <integer>
Output: <bounded summary or absolute output path>
Artifact: <absolute path | none>; ownership: run-owned | pre-existing
Screenshot: <absolute path | N/A>; actual inspection: yes | no | N/A
```

5. `compare`: 근거를 기준에 대응시키고 검증된 차이, 미검증 항목과 다음 결정을 요약합니다. 상위 계약에 이미지 `PR evidence: required`가 기록되어 있고 비교가 `Pass`이며 직접 확인한 스크린샷이 이를 바로 입증하면, 실행 소유 절대 경로 `Screenshot: <path>`와 실제 이미지 확인 내용을 `## Tested` 아래에 보존하고 발행 측에서 소비하는 것과 같은 생성 주체에 종속되지 않는 manifest를 제공합니다. `evidence_required: true`, `evidence_kind: visual-change`, `verification_status: Pass`, 기준, 비교, 한계와 함께 역할, 절대 경로, origin이 없는 정확한 `display_route`, 상태/영역, viewport가 있는 직접 확인한 산출물을 포함합니다. `tk-browser-verify`가 반환한 메타데이터를 사용하고 파일명, 원시 URL 또는 생성 주체의 식별 정보에서 도출하지 않습니다. 이는 prototype 비교를 입증하며 공식 제품 런타임 인수 판정은 아닙니다. `Fail | Blocked | Unverifiable`이면 소유한 실패 산출물을 보존하고 실제 상태를 반환하되 `verification_status: Pass` 발행 manifest를 내보내지 않습니다. 필수 이미지 발행을 충족할 수 없으면 해당 발행 요구사항을 차단 또는 검증 불가로 보고합니다.
6. 비교가 후속 구현에 영향을 주면 [선택된 prototype 인계](../tk-engineering/references/selection-handoff.md)를 읽고 해당 선택 기록을 기존 결과에 반환합니다.
7. `terminal summary`: 아래 출력 계약에 해당하는 절을 표시합니다. 별도의 출처·상태 블록을 추가하지 않습니다.

미해결 UI 비교에서는 결정에 관련된 차원만 바꿉니다. 색상, 대비 또는 상태 식별이 질문인 경우 색상만 다른 대안도 유효하며 해당 비교에서 레이아웃과 동작은 유지합니다. 아키텍처, 흐름 또는 탐색은 그것이 실제 질문일 때만 바꿉니다. 로직에는 예시 입력/출력과 최소 어댑터를 사용하는 작은 순수 harness를 우선합니다.

웹 prototype에서는 저장소 실행 명령, 설치된 UI 스택, 구성 요소와 디자인 토큰을 확인합니다. 의존성을 추가하거나 manifest/lockfile을 바꾸지 않고 안전하게 격리된 route/harness를 재사용합니다. 저장소·참조 디자인 토큰이 없는 독립 HTML에는 공통 테마 자산과 가독성·렌더링 요구사항을 위해 [HTML 출력](../tk-writing/references/html-output.md)을 읽습니다. 비교별 디자인 토큰과 prototype 탐색 예외를 유지합니다. 안전한 route/harness가 없으면 작은 `.tigerkit/prototypes/<slug>/index.html`, `styles.css`, `app.js`를 사용합니다.

콘텐츠, 데이터와 상호작용 상태를 동일하게 유지하면서 결정에 관련된 개념 2–3개를 비교합니다. 기본적으로 넓은 화면에서는 2–3개 열을 나란히 배치하고 좁은 화면에서는 세로로 쌓습니다. 동시 렌더링이 개념이나 최소 가독성을 해칠 때만 명시적인 A/B 또는 A/B/C 전환을 사용합니다. 세 번째 선택지가 독립적인 가치를 더하지 않으면 A/B에서 멈춥니다. 저장소 근거가 이미 결정을 해결하면 prototype을 만들지 않습니다.

`tk-browser-verify`로 실제 상호작용, `run URL`/`command`와 `success-criteria` 스크린샷을 포함하여 웹 출력을 검증합니다. 개발 서버가 필요하면 `handoff`로 정확한 `command`/`cwd`/대상 URL/`auth mode`/`readiness` 조건을 전달합니다. 서버 시작, 대기와 종료는 `tk-browser-verify`가 담당합니다. `hypothesis`가 반응형 동작·레이아웃을 다룰 때만 넓은 화면과 좁은 화면을 모두 점검합니다. 실행 소유의 추적 중인 `harness` 파일만 정리하고 `existing route`, `dependency`와 `production source`는 보존합니다.

<a id="failure-paths"></a>
## 실패 경로

쓰기 전에 기존 임시 경로와 실행이 생성한 파일을 기록합니다.

| 조건 | 첫 행동 | 계속 실패하는 경우 |
|---|---|---|
| 중단되거나 일부만 완료된 쓰기 | 실행 소유임이 입증된 미완성 산출물만 정리합니다. | `Fail`; 안전하게 정리할 수 없는 경로와 재시작 조건을 보고합니다. |
| 서버/harness 실패 | 명령, 종료 상태, 출력과 fake/real 경계를 보존합니다. | `Fail`; 제품·의존성 범위로 확장하지 않습니다. |
| 실행은 성공했지만 출력·스크린샷 근거가 없음 | 같은 경계 안에서 수집을 한 번 재시도합니다. | `Unverifiable`; `Pass`를 주장하지 않습니다. |
| 기존 산출물과 소유권·상태 충돌 | 기존 경로를 보존하고 근거를 기록합니다. | `Blocked`; 쓰기 전에 다른 경로를 선택합니다. |
| 정리 실패 | 실행 소유 자원만 다시 식별하고 결과를 보고합니다. | `Fail \| Unverifiable`; 기존 route·프로세스를 보존합니다. |
| 범위가 제품 반영·승격·commit으로 확장됨 | prototype을 중단하고 별도의 구현 요청으로 분리합니다. | `Blocked`; 자동으로 승격하지 않습니다. |

<a id="-checkpoint---stop--execution-boundary"></a>
## 🔴 CHECKPOINT · 🛑 STOP · 실행 경계

실행 전에 임시 경로, fake/real 데이터와 검증 질문을 확인합니다. 환경이나 제품 범위가 확장되면 `Blocked | Unverifiable`에서 중단합니다.

보고 전에 명령, 실제 출력·스크린샷, fake/real 경계와 미검증 범위를 대조합니다. 하나라도 없거나 실행이 실패하면 결과는 `Pass`일 수 없습니다. `Fail | Blocked | Unverifiable`을 사용합니다.

<a id="contract"></a>
## 계약

결정에 관련된 상태는 해당 소유 절에 한 번만 기록합니다. `## Confirmed`로 시작하고 `## Production implication`, `## Tested`, `## Variants or harness`, `## Still fake` 순서로 작성하며 빈 절은 생략합니다. `Confirmed`는 근거로 뒷받침되는 결론을, `Production implication`은 폐기·반복 개선·다음 결정을, `Tested`는 명령 결과를, `Variants or harness`는 대안·경로·실행 URL과 최종 `kept | removed` 상태를, `Still fake`는 fake/real과 미검증 범위를 담당합니다. 명령 실행 세부 사항은 결정 뒤에 둡니다.

최종 상태는 `Pass | Fail | Blocked | Unverifiable` 중 정확히 하나만 사용합니다.

여러 기준이나 대안을 비교할 때는 `## Confirmed`를 간결한 `Criterion | A | B [| C] | Conclusion | Evidence` 표로 표시합니다. 사용자에게 관련된 행이 하나뿐이면 문장을 사용합니다. 콘텐츠·데이터·상태를 동일하게 유지했는지 기록합니다. 관찰하지 않은 차이에는 `not observed`를, 근거가 없으면 `unverifiable`을 사용합니다. 검토하지 않은 미적 선호를 결론으로 격상하지 않습니다. 비교 질문에 답하는 짧은 글머리 항목이나 선택지 행으로 결과와 선택 이유를 요약합니다. 결정에 관련된 관찰 내용을 보여 주고 나머지 내용을 소유한 prototype 또는 근거 경로를 인용합니다.

<a id="prohibited-patterns"></a>
## 금지 패턴

- prototype을 제품에 사용할 준비가 되었다고 부르거나 자동 승격·commit하거나 다른 사용자 스킬을 호출하지 않습니다.
- 가짜 통합을 실제 통합으로 보고하거나 실행 근거 없이 성공을 주장하지 않습니다.
- 무관한 대안, 의존성, manifest/lockfile 변경, 불필요한 제품 추상화 또는 가치 없는 세 번째 선택지를 추가하지 않습니다.

<a id="artifact-paths"></a>
## 산출물 경로

승인된 산출물 쓰기, checkout·전송·ignore 설정 또는 임시 입력 소비 전에 [산출물 경로](../tk-artifacts/references/artifact-paths.md)를 읽습니다. 저장소 임시 작업에는 안전한 소유 nonsymlink 경로와 입증된 Git 제외를 사용합니다. 점검이 실패하면 해당 파일 분기를 중단합니다. 명시된 최종 목적지와 소유자별 기본값을 보존합니다. 미리 채운 입력은 완료된 입력이 아닙니다. 정리 대상은 기록된 리터럴 값이자 해석된 절대 경로인 실행 소유 경로뿐이며 cwd 상대 경로나 glob은 사용하지 않습니다.
