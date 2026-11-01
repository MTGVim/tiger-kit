<a id="qa-sheet-data-and-rendering"></a>
# QA 시트 데이터와 렌더링

기본 HTML 시트 또는 명시적으로 요청된 HTML 시트를 위해 읽습니다. 번들 템플릿을 복사하고 `script#qa-data` JSON을 교체한 후 번들 도우미로 해당 데이터에서 정적 읽기 인벤토리를 다시 생성합니다. 최종 파일에는 외부 자산이나 런타임 생성기가 필요하지 않습니다.

<a id="authoring-and-inspection-contract"></a>
## 작성과 확인 계약

템플릿 구현을 검색하지 않고 이 대응표를 사용합니다. 런타임 렌더러, 스타일과 제어 요소 연결은 변경하지 않습니다. 이 selector는 점검 대상 제품이 아닌 생성된 시트를 확인합니다. 일치한다는 사실만으로 런타임 결과 통과가 입증되지는 않습니다.

| 용도 | 계약 또는 selector |
| --- | --- |
| 편집 가능한 데이터 | serializer와 아래 이스케이프 규칙을 사용하여 `script#qa-data`의 JSON 텍스트만 교체합니다. |
| 브라우저 탭 제목 | JSON `title`을 설정합니다. 런타임이 이 값에서 `document.title`과 `#title`을 설정합니다. 정적 HTML `<title>`도 HTML 이스케이프를 적용하여 같은 일반 텍스트 제목과 맞출 수 있습니다. 렌더러 코드는 편집하지 않습니다. |
| JavaScript 없는 인벤토리 | `noscript#qa-static`을 `scripts/render_static_inventory.py`로 다시 생성하고 직접 편집하지 않습니다. |
| 렌더링된 제목과 인벤토리 | `#title`, `#main`의 렌더링 텍스트와 행 범위를 최종 JSON과 비교합니다. |
| 편집 가능한 점검 | `#main li.check input[type="checkbox"]:not(:disabled)`를 사용합니다. 생성된 `data-id` 값이 영속화 식별 정보를 소유합니다. |
| 자동 점검 | `#main input[data-auto="true"]`는 초기화 후를 포함하여 체크되고 비활성화된 상태여야 합니다. |
| 미검증 자동 기준 | `#main li.verification-gap`에는 안내 텍스트가 보여야 하고 체크박스가 없어야 합니다. |
| 필터와 초기화 | `#onlyOpen`, `#reset`의 동작을 아래 요구사항에 따라 확인합니다. |
| 메모와 저장 상태 | `#notes`, `#saved`의 상태 레이블을 믿는 대신 다시 로드하여 복원을 테스트합니다. |
| 개수와 저장소 실패 | `#count`, `#storage-warning`의 개수를 데이터와 대조하고 저장소 접근 거부 시 경고 동작을 검증합니다. |

이 selector는 새로운 필수 체크리스트가 아니라 조회 지점으로 재사용합니다. 필수 시나리오는 아래 기존 자체 점검이 소유합니다. selector가 일치하지 않으면 대체 계약을 만들어 내지 말고 설치된 템플릿 버전을 확인합니다.

<a id="data"></a>
## 데이터

```json
{
  "title": "Task QA",
  "storageKey": "task-topic",
  "head": "abc123",
  "environment": {"label": "Local QA", "baseUrl": "http://localhost:3000"},
  "legend": ["Scope, evidence rules and unresolved screens"],
  "groups": [
    {
      "title": "Area",
      "items": [
        {
          "title": "Observed screen hierarchy or known route",
          "provenance": "observed",
          "url": "http://localhost:3000/orders",
          "notes": ["Shared pattern or missing connection"],
          "checks": [
            {
              "criterionId": "UI-001",
              "text": "Observed trigger and expected behavior",
              "provenance": "observed",
              "verification": "auto-verified",
              "evidence": {"ref": "browser-run-123", "head": "abc123"},
              "indent": 0
            },
            {
              "criterionId": "UI-002",
              "text": "Only the unexercised branch remains",
              "provenance": "observed",
              "verification": "partial",
              "evidence": {"ref": ".tigerkit/evidence/tk-browser-verify/run-123", "head": "abc123"},
              "indent": 1
            },
            {"text": "Source-only trigger and expected behavior", "provenance": "code-only", "indent": 1},
            {"text": "Subheading", "heading": true}
          ]
        },
        {"title": "A screen check without children", "provenance": "code-only"}
      ]
    }
  ]
}
```

새 시트는 자신이 나타내는 영향 인벤토리의 후보를 가리키는 최상위 `head`가 공백이 아니어야 합니다. 렌더러는 이전 시트에만 `head` 생략을 허용합니다. 브라우저 검증기는 해당 계보를 알 수 없는 것으로 취급하고 런타임 전에 조정해야 합니다. `title`, `storageKey`, 그룹·항목 제목과 점검 텍스트는 공백이 아니어야 합니다. `groups` 배열과 `items`는 비어 있지 않아야 하며 선택적인 `legend`/`notes`는 문자열 배열입니다. `checks`가 없거나 비어 있으면 항목 자체가 점검 항목이 됩니다. `heading: true`는 체크박스를 만들지 않습니다. 항목마다 실제 점검이 하나 이상 있어야 합니다. `indent`는 0에서 3 사이의 정수입니다.

`provenance`는 `observed | code-only`이며 값이 없으면 기본값은 `code-only`입니다. 상위 항목과 하위 항목이 모두 명시적으로 관찰된 경우에만 하위 항목을 관찰된 것으로 봅니다. 근거 없는 상위 항목이 있으면 전체 점검을 관찰된 탐색 주장으로 만들 수 없습니다. 정확히 관찰한 UI 레이블에만 backtick을 사용합니다. 소스에 정확한 문자열이 있어도 소스만 있는 레이블은 일반 텍스트를 사용합니다. 알려진 route는 기술 literal로 코드 서식에 넣을 수 있으며 탐색과 별도로 그 상태를 알립니다. 사용자 제공 텍스트와 누락된 클릭 연결을 메모·범례·한계에 명시적으로 나열합니다.

모든 새 점검 행에는 안정적인 `criterionId`가 있습니다. 영향 인벤토리·브라우저 검증기의 ID를 그대로 유지하거나, 제공된 ID가 없으면 진입점을 분리한 뒤 `QA-001`, `QA-002`, ...를 할당합니다. 같은 작업을 재생성할 때 ID를 보존하고 시트 전체에서 고유하게 유지합니다. 렌더러는 이전 시트에만 ID 생략을 허용합니다. `verification-gap` 행은 인자 없는 검증기 실행이 대상으로 삼고 반환할 수 있도록 ID가 있어야 합니다. 렌더러는 행 옆에 이를 표시합니다. 생성되는 체크박스 ID는 별도로 유지되며 콘텐츠에 연결됩니다.

검증기 행 매핑을 사용할 때는 `evidence_ref`를 `evidence.ref`로 복사하고 `head`를 변경하지 않습니다. `Pass`와 `covered-by:<criterion_id>`는 해당 행 ID에 매핑된 근거가 있을 때만 `auto-verified`로 매핑하며 `covered-by`의 동등성 이유를 유지합니다. `Fail`은 같은 기준의 `failed`로 유지합니다. 승인된 `out-of-scope` 또는 `not-executed` 행에 입증된 수동 차단 요인이 없으면 `verification-gap`으로 바꿉니다. 입증된 차단 요인이 있으면 `manual`로 바꾸고 `reason`을 `manualReason`으로, `search_scope`를 `searchScope`로 매핑하며 구체적인 `unblock`을 포함합니다.

`verification`은 `manual | verification-gap | auto-verified | partial | failed`이며 이전 시트에서 값이 없으면 기본값은 `manual`입니다. `verification-gap`은 확립된 권한 안에 있지만 실행 기록, 기록된 `searchScope`와 검증된 기능 공백이 없는 미실행 행에 사용합니다. 이 상태에는 자동 근거가 없으며 편집 가능한 체크박스 없이 별도로 표시합니다. 사람에게 맡길 작업이 아닙니다.
독립 항목이나 제목이 아닌 하위 점검에 적용되며 `provenance`와 독립적입니다. 하위 점검을 포함한 항목에는 자체 검증 상태를 두지 않습니다. `auto-verified`, `partial`, `failed` 행에는 `evidence` 객체가 필요하며 공백이 아닌 `ref`와 `head`를 가져야 합니다. `ref`는 실행 ID 또는 근거 경로이고 `head`는 근거가 연결된 commit head입니다. 수동 행은 `evidence`를 생략합니다. 새로 작성하는 사람 전용 `manual` 행은 모두 `manualReason`을 `unauthorized-or-irreversible`, `data-unavailable-after-search` 또는 `verified-capability-gap`으로 설정하고 `unblock`에는 구체적인 다음 단계를 설정합니다. 뒤의 두 사유에는 기록된 검색이나 시도한 기능 점검을 설명하는 공백 아닌 `searchScope`가 필요합니다. 쓰기 권한 누락·비가역성 문제만 시도 전에 쓰기를 제외할 수 있는 사유입니다. 사용자가 사람용 체크리스트를 명시적으로 요청하면 공백을 대신 편집 가능한 `manual` 행으로 만들고 `automatable: true`를 지정할 수 있습니다. 이는 명시적인 체크리스트 예외이며 사람만 할 수 있는 차단 요인이라고 주장하지 않습니다. 하위 호환성을 위해 렌더러는 `manualReason` 없는 이전 수동 행을 허용하지만 새 스킬 출력은 반드시 이를 제공해야 합니다.
이후 diff가 화면에 영향을 주어 상태가 낮춰진 수동 행은 대신 `previousEvidence`를 가질 수 있으며 같은 `ref`와 `head` 구조를 사용합니다. 한 번도 실행하지 않은 수동 행은 두 필드를 모두 생략하며 `previousEvidence`는 행을 자동 검증으로 승격하지 않습니다.

검증기의 `Fail` 행은 통과한 부분과 수동 나머지로 나누지 않고 `failed`로 설정합니다. 검증기 근거를 `evidence`에 보존합니다. 행은 편집 가능한 수동 목록에 남아 사람이 후속 점검을 기록할 수 있고 `failed` 결과와 근거도 계속 보입니다. 수동 체크박스가 검증기 결과를 다시 쓰지는 않습니다.

같은 화면, 진입 경로, 트리거와 기대 결과를 실행한 실행 소유 자동 런타임 근거에만 `auto-verified`를 사용합니다. 일반적으로 해당 근거는 현재 head에 있습니다. 대상 head가 이동하면 근거 head에서 현재 head까지 diff를 확인합니다. diff가 해당 화면의 렌더링 경로나 요청 경로에 닿을 때만 행이 영향을 받는 것으로 취급합니다. 해당 경로가 그대로면 이전 근거는 계속 `auto-verified`일 수 있습니다. 원래 head를 유지하고 경로 기반의 계속 적용 이유를 보고합니다. 행이 영향을 받으면 런타임 세션이 남아 있는 동안 현재 head에서 다시 수집하는 것을 우선합니다. 그렇지 않으면 `manual`로 낮추고 이전 실행을 `previousEvidence`로 옮깁니다. 다른 화면이나 진입 경로의 근거는 `partial`이며 해당 행 텍스트가 실행하지 않은 부분만 설명하도록 다시 씁니다. 단위 테스트만으로 화면 점검을 승격하지 않습니다. 데이터를 변경하는 점검은 정확한 변경을 명시적으로 승인받고 실제 실행했으며, 현재 head에 연결된 실행 소유 런타임 근거가 독립적 재읽기를 통해 같은 화면, 진입 경로, 트리거, 작업과 기대 저장 결과를 입증할 때 `auto-verified`일 수 있습니다. backend 제출 없이 요청 본문만 수집했다면 payload 구성 점검만 자동 검증할 수 있고 저장 결과 점검은 자동 검증할 수 없습니다. 근거의 `ref`와 `head`를 보존합니다. 레이블은 검증 근거를 기록하며 제품 인수 판정이 아닙니다. 권한이나 현재 head 근거가 없으면 데이터 변경 결과를 `manual`로 유지합니다.

HTML 렌더러는 `auto-verified` 행을 접힌 `Automated` 그룹에 근거 참조와 함께 체크되고 비활성화된 제어 요소로 배치합니다. `verification-gap` 행은 체크박스 없는 별도의 보이는 `자동 검증 필요` 절에 표시하며 인자 없이 `/tk-browser-verify`를 실행한 후 시트를 재생성하라는 안내를 제공합니다. `partial`, `failed`, `manual` 행은 수동 목록에서 편집 가능하게 유지합니다. `partial`, `failed` 행은 현재 근거를 보여 주고, head 변경으로 낮춰진 수동 행은 이전 head임을 명시하는 레이블과 함께 `previousEvidence`를 보여 줍니다. `failed` 행은 같은 기준에 남습니다. 수동 체크박스는 실패 결과를 바꾸지 않고 후속 작업을 기록합니다.

<a id="screen-links"></a>
## 화면 링크

`environment`는 선택 사항입니다. 제공할 때는 공백이 아닌 `label`과 URL 자격 증명이 없는 절대 HTTP(S) `baseUrl`이 필요합니다. 선택적인 항목 `url`은 해당 환경 origin의 절대 HTTP(S) 도착 URL이며 링크에는 `environment`가 필요합니다. 템플릿은 환경 이름과 별도의 `화면 열기` 링크를 표시하며 체크리스트를 토글하지 않습니다. 링크는 `noopener noreferrer`와 referrer 없음으로 새 탭을 엽니다. 링크를 인용한 UI 텍스트 밖에 둡니다.

실제 대상 ID와 route/query/fragment를 검증한 경우 근거가 있는 상세·섹션 URL을 우선합니다. ID를 사용할 수 없으면 알려진 목록 URL을 사용하고 레코드 선택을 수동 점검으로 설명합니다. 근거가 있는 정확한 도착 URL을 재사용하고 ID, fragment, host/port 또는 hash-router 경로를 만들어 내지 않습니다. 환경이나 도착 route를 모르면 링크를 생략하고 한계를 보고합니다. 알려진 route·base 근거에서 도출한 링크는 클릭한 탐색 연결을 입증하지 않습니다. 관찰하지 않은 레이블에는 `code-only` 상태를 보존합니다. 생성자는 비밀이 포함되거나 서명된 URL과 민감한 개인정보를 제외해야 합니다. 구조적 URL 검증만으로 발행 안전성을 확립할 수는 없습니다.

실제 serializer로 JSON을 직렬화한 후 삽입 전에 모든 `<`를 JSON 이스케이프 `\u003c`로 바꿉니다. 이는 `</script>`와 HTML comment 시퀀스가 데이터 블록을 끝내지 못하게 합니다. JSON을 HTML 이스케이프하거나 문자열을 수동 보간하는 것은 안전하지 않습니다. 최종 삽입 블록의 파싱과 예시 작업·영역·트리거 내용이 없음을 검증합니다.

<a id="identity-and-persistence"></a>
## 식별 정보와 영속화

점검 ID는 환경 base URL, 도착 URL, 그룹 제목, 항목 제목과 하위 점검 텍스트(독립 항목이면 null)의 전체 JSON 직렬화 tuple을 인코딩합니다. tuple 경계는 구분자가 포함된 레이블과 독립·하위 점검을 구분합니다. 환경이나 레코드 링크가 바뀌면 이전 점검의 완료를 재사용할 수 없습니다. 전체 tuple 인코딩은 재생성 간 짧은 해시의 충돌을 피합니다. 동일한 tuple은 렌더링 전에 눈에 보이게 거부합니다. 실제로 별개인 점검은 순서에 의존하는 ID가 아닌 정확한 맥락 텍스트로 구분합니다. 동일한 콘텐츠의 순서 변경은 ID를 보존하고 텍스트 변경은 새 ID를 만듭니다. 기존 시트를 다시 쓸 때 이 한계를 설명합니다. 같은 작업과 환경에만 `storageKey`를 재사용합니다. 새 작업, 환경 또는 독립적으로 테스트하는 revision에는 메모·필터에도 새 키를 사용합니다.

저장 키는 `["tk-qa-sheet", storageKey, role, 1]`을 JSON으로 직렬화하며 role은 `checks`, `notes` 또는 `onlyOpen`입니다. 작업과 역할을 별도 tuple 필드로 두면 한 작업 이름이 다른 작업의 메모·점검 키와 충돌하지 않습니다. 테마는 의도적으로 작업 식별 정보 밖에 둡니다. 정본 공통 테마 제어 요소는 원시 `system | light | dark` 값을 `tigerkit-html-theme` 아래에 저장하며 `storageKey`와 독립적입니다. 이를 통해 독자의 명시적 브라우저 선호를 같은 브라우저/localStorage origin을 공유하는 다른 TigerKit HTML 출력에도 이어갈 수 있습니다. 생성 기본값은 공통 사용자 `settings.json` 계약인 `../../tk-writing/references/html-output.md`에서 별도로 가져오며 저장된 독자 선호가 런타임에서 해당 기본값을 덮어씁니다. `file:` URL이나 브라우저 간에는 저장 범위를 브라우저가 정의하므로 파일 간 영속화를 약속하지 않습니다. 테마 저장값이 없거나 유효하지 않거나 읽을 수 없으면 `system`으로 시작합니다. 쓰기가 거부되어도 테마 변경으로 현재 페이지를 갱신할 수 있지만 다시 로드하면 `system`으로 돌아갈 수 있습니다. 점검 초기화는 테마 선호를 지우지 않습니다.

읽기·쓰기는 사용할 수 없는 저장소와 형식이 잘못된 저장 데이터를 견딥니다. 자동 검증 행은 사용자 완료로 저장하지 않습니다. 렌더러는 항목이 자동 검증 상태인 동안 이전에 저장된 완료를 지우므로 이후 수동으로 낮춰져도 낡은 수동 체크가 되살아나지 않습니다. 쓰기가 실패하면 메모리 내 상호작용을 막지 않고 경고를 표시합니다. 메모는 400 ms 후 저장하고 페이지 종료 시 반영합니다. 초기화는 체크를 지우기 전에 확인하고 메모를 보존합니다. 저장소는 브라우저·프로필과 파일·origin에 한정됩니다. 파일 이동이나 브라우저 변경으로 기존 상태에 접근하지 못할 수 있습니다. 파일 간 또는 다중 사용자 영속화를 약속하지 않습니다.

<a id="self-check"></a>
## 자체 점검

`qa-data`를 채운 뒤 생성한 파일에 패키지의 `scripts/render_static_inventory.py`를 실행합니다. 같은 JSON에서 `noscript#qa-static`만 교체하고 설명 텍스트를 이스케이프하며 런타임 렌더러를 보존합니다. 데이터가 바뀔 때마다 재생성하고 두 번째 인벤토리를 유지하지 않습니다. JavaScript를 끈 상태에서 최종 그룹·항목·점검을 읽을 수 있으며 제어 요소가 작동하는 것처럼 표시되지 않는지 검증합니다. 영속화는 JavaScript 전용 기능으로 유지하고 정적 보기에서 알립니다. 정적 범위는 번들 예시가 아닌 최종 JSON과 비교합니다.

정확한 생성 파일, 인증·서버 없음, 일회용 headless 프로필, 모든 필수 [HTML 출력](../../tk-writing/references/html-output.md) 렌더링 점검과 요청된 레이아웃 기준으로 `tk-browser-verify`를 사용합니다. 짧은 시트도 모두 수치 기반 가독성 점검과 확인한 점검·누락된 점검 보고를 포함하는 desktop/mobile, light/dark 범위가 필요합니다. 보이는 분할형 테마 라디오가 `system / light / dark` 순서인지 검증합니다. `system`은 `data-theme`를 설정하지 않고 에뮬레이션한 light/dark OS 선호를 따라야 하며 수동 light/dark 선택은 이를 덮어쓰고 저장소 사용 가능 시 다시 로드한 뒤 복원되어야 합니다. 점검 초기화가 테마를 보존하고 저장소 접근 거부 시에도 시트를 읽을 수 있으며 다음 로드에서는 `system`으로 돌아가는지 확인합니다. 편집 가능한 행이 두 개 이상이면 두 행과 메모가 다시 로드한 뒤 유지되는지 검증합니다. 두 개 미만이면 대신 메모 영속화와 `auto-verified` 불변성을 검증하고 편집 가능 행 점검은 `not applicable`로 보고합니다. ID는 고유하고 개수는 정확하며 code-only 상태는 보여야 합니다. 초기화는 메모를 유지하고 자동 검증 행은 초기화 후에도 체크된 채 편집 불가능해야 하며 partial/manual 행은 수동 목록에 남고 `verification-gap` 행은 체크박스 없이 그 밖에 표시되어야 합니다. 공백 안내는 대화형 보기와 JavaScript 없는 보기 양쪽에서 보여야 합니다. 번들 예시만 보지 말고 최종 데이터로 근거 참조와 접힌 Automated 그룹을 검증합니다. 실제 실패·한계 근거를 보존하고 실행 소유 프로필만 제거합니다. 저장소 접근이 거부된 환경은 정상 렌더링되지만 영속화 수용 기준을 충족할 수 없습니다.
