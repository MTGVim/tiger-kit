<a id="browser-evidence-and-results"></a>
# 브라우저 근거와 결과

최종 판정 분기의 런타임 근거를 저장하거나 실행한 검증 단계를 반환하기 전에 읽습니다.
명시적 접근성 감사의 범위·완료·발견 반환은 [접근성 결함 탐색](accessibility-audit.md)을 따릅니다.

`.tigerkit/evidence/` 아래에 처음 쓰기 전에
`git ls-files -- .tigerkit/`가 추적 경로를 하나도 반환하지 않고
`git check-ignore -q -- .tigerkit/`가 성공하는지 확인합니다. `git check-ignore -v`에서는 일치한 출처 유형과
패턴만 기록하고 사용자 수준의 절대 경로는 가립니다. 제외 범위가 부족하면 [산출물 경로](../../tk-artifacts/references/artifact-paths.md)의
제외 설정을 적용합니다. 그래도 검사가 실패하면 파일을 쓰거나 외부 대체 경로를 사용하지 말고
`Unverifiable`을 반환합니다.

바이너리 근거는 이번 실행이 소유한 `.tigerkit/evidence/tk-browser-verify/<run-id>/`에 저장할 수 있습니다. 변경 전 기준 비교에는
`baseline/`, `after/`와 변경 불가능한 `failed-<attempt>/` 하위 디렉터리를 사용합니다. 필수로 작성하는 제한된 범위의 `README.md`에는 각
AC를 해당 스크린샷, 발행해도 안전한 정확한 `display_route`, 재실행 절차와 공개된 캡처 전용 또는
비결정적 제외 사항에 대응시킵니다. 이는 근거 색인이지 수명 주기 기록부가 아닙니다.
그곳에 다른 Markdown 파일을 두지 않습니다.
명시적으로 요청받은 [콘택트 시트](contact-sheet.md)는 파생 PNG와 타일에서 원본으로 가는 링크를
같은 README에 추가할 수 있습니다. 생성 생략 사항은 검증 상태를 바꾸지 않고 그곳에 기록합니다.
사용자 픽스처를 옮기지 않습니다. 민감한 캡처는 가림 처리를 검증하고 잔여물이 없음을 확인한 뒤에만 근거로 사용합니다.
결정적이든, 드물든, 간헐적이든 어떤 실패라도 나타나면 이를 덮어쓰거나 삭제할 수 있는 재실행 전에 이번 실행 소유의
스크린샷, 추적, 로그나 덤프를 보존합니다. 변경 전 기준 비교의 실패는 새로운 고유 `failed-<attempt>/` 경로에
보존하며, 이후의 `after/` 경로에는 두지 않습니다. 나중에 실패가 나타나지 않은 표본이 나와도 이미 관찰한 실패가 사라지지는 않습니다.

변경 전/후·실패 시도 캡처를 쓰기 직전에, 해석한 목적지가 이번 실행의 현재 단계 디렉터리
(`baseline/`, `after/`, `failed-<attempt>/`) 안에 있고 아직 존재하지 않는지 확인합니다.
경로 검증에 실패하거나 목적지가 이미 있으면 쓰지 않고 중단합니다. 단계별 경로는 스크립트 텍스트
치환 대신 인수나 단계별 상수로 넘기며, 변경 후 단계에서 `baseline/`을 목적지로 받아들이지 않습니다.
쓴 뒤에는 검증한 바로 그 경로에 파일이 생겼는지 확인합니다. 후보가 바뀌어 이전 변경 후 캡처가
최종 후보를 나타내지 않으면 삭제하지 말고 새로운 고유 `failed-<attempt>/`로 옮깁니다. 옮긴 경로를
기존 근거 색인에 반영하고 이전 후보의 head·출처 정보는 그대로 보존합니다. 이전 후보를 최종 결과로 쓰지 않습니다.

중첩 결과와 독립 결과에는 다음 계약 필드가 필요합니다. 중첩 결과는 다음 항목으로만 제한합니다.

- status
- `provider`: 실제 제공자 ID, 버전, 실행 파일 또는 호출한 호스트 도구 경로와 선택 근거. 예정한 제공자가 아니라
  관찰한 실행 사실을 기록하며, CLI 이름만으로 준비 상태나 검증 성공을 주장하지 않습니다.
- `contract: <metadata.tigerkit.version>`. 현재 계약은 `1.2.0`입니다.
- `scope: full-inventory | explicitly-scoped`. 범위를 제한했다면 사용자가 지정한 정확한 범위를 식별합니다.
- `coverage: planned <N> / executed <n> / covered-by <c> / out-of-scope <o> / not-executed <m>`. 개수는 조사한 전체 항목 목록과 일치하도록 대조해야 합니다.
- `human_action: none | <N> (criterion IDs, reason and next action)`. 남은 작업을 모두 상위 작업이 담당하면 중첩 반환에서는 `none`을 사용합니다.
- `phase: baseline | after | acceptance`. 편집 전 변경 전 기준 캡처에 성공했다면 `baseline_capture: Pass`,
  `verification_complete: false`, `run_id`, `replay_procedure`와 정확한 `next_required`도 반환합니다.
  활성 상위 작업에 승인된 구현 작업이 남아 있다면 `resume_parent: required`를 포함합니다.
- `visual_contract: applied | n/a`. `n/a`에는 시각 참조, 변경 전/후,
  여러 캡처, 시각/반응형 또는 렌더링 영향 분기가 어느 것도 해당하지 않음을 입증하는 사유가 필요합니다.
- `capture_only_mutation: <description> | none`은 근거 색인에도 기록합니다. 외곽선/레이블,
  숨김/제거와 런타임 모의를 포함하고, 캡처 전용 변경이 없었다면 `none`을 명시합니다.
- 승인된 기준 항목마다 `criterion_id`, `result`, `route`, `entry`, `trigger`, `operation: read | create | update`, `input`, `evidence_kind`, `evidence_ref`와 `head`를 포함한 사실 행 하나
- 사용자의 명시적인 범위 제한만을 이유로 제외한 항목 목록 행에는 `result: out-of-scope`를 사용합니다. 전체 행 대응표에 해당 ID와 범위 제외 사유를 유지합니다.
- 다른 행으로 검증이 충족되는 행에는 `result: covered-by:<criterion_id>`를 사용하고, 참조한 행의 `evidence_ref`와 `head`를 포함합니다. 전체 행 대응표에 동등성 근거를 보존합니다.
- `input: trusted | synthetic(<reason>) | not-run`. 합성 입력으로 수행한 제품 상호작용은 Pass가 될 수 없습니다. 합성 근거는 기준 항목 자체가 상호작용 없는 탐침을 허용할 때만 허용됩니다.
- `evidence_kind`: `blocked-intercept | request+response | reread-runtime | reread-image | visual-pair | trace | accessibility | dom-runtime | none` 중 하나 이상. 어느 시도에서도 근거를 얻지 못했다면 `none`과 `evidence_ref: none`을 사용합니다.
- 모든 `create` 또는 `update` 행의 `Pass`에는 같은 화면의 같은 필드에서 수행한 `reread-runtime`이 필요합니다. `reread-image`를 사용하면 검사한 이미지에 판정할 필드가 보여야 합니다.
- 실행하지 않은 모든 행의 `reason`, `search_scope`(페이지, 필터, 데이터 조건이나 정확한 사전 점검 경계), `unblock`(실행을 가능하게 할 구체적인 단계)
- 민감하지 않은 인증 모드
- 근거 디렉터리의 절대 경로
- 시각 비교 쌍이 필요할 때는 변경 전 기준의 출처 정보와 재실행 절차
- 검사한 스크린샷마다 순서대로 한 행씩 기록한 경로, 오리진을 제외한 정확한 `display_route` 또는 명시적인 생략,
  기준 항목, 상태/영역, `capture_method`, 실제 적용된 뷰포트, 역할과 비교 결과. 그 외에는 직접적인 추적/접근성/DOM/런타임/요청 근거
- 예외의 사유와 영향을 포함하여 근거 색인에도 같은 캡처별 방법/실제 적용 뷰포트 기록
- 시각 캡처마다 대상 외곽선에 대한 `annotation: visible (pixel-checked) | none (remain unchanged) | none (target absent by intent)`와
  `target in frame: yes | no`. 대상이 없다면 나타남/사라짐 의도와 화면에 보이는 주변 맥락이 필요합니다.
- 민감한 화면은 캡처 계획의 민감 영역과 캡처 전 자르기/마스킹. 전체 페이지/가공 전 원본은 절대로 보존하지 않습니다.
- limitation
- 정확한 실행 소유 서버/브라우저 종료, 기록된 시작 PID/핸들, 확인된 종료와 검증된 잔여물을 포함한 정리 사실. 변경 전 기준부터 최종 헤드까지 프로세스를 유지하지 않습니다.
- 상위 작업의 제공되거나 검증된 처리 방침인 `automated_regression: protected | N/A | exception | unknown`

상위 작업이 제공하거나 조사로 얻은 항목 목록 행 ID를 그대로 `criterion_id`로 사용합니다. ID가 없는 직접 호출에서는 항목 목록 순서대로 `BV-001`, `BV-002`, ...를 한 번만 부여하고 재시도와 단계 사이에 그 대응을 유지합니다. 인자 없이 또는 범위만 지정한 독립 호출은 런타임 시작 전에 같은 작업의 전체 항목 목록을 조사하고 대조합니다. 명시적인 범위 축소로 제외한 행은 `out-of-scope`로 기록합니다. `tk-prep`은 인계 전에 ID를 부여합니다. QA 시트의 `criterionId`에도 같은 ID를 유지하고, `evidence_ref`를 시트의 `evidence.ref`에 대응시키며, `head`를 변경 없이 복사합니다. 한 행의 일부가 실패했다고 두 번째 기준 항목을 만들지 않습니다.

런타임 근거가 있으면 범위를 한정한 실행 소유 `README.md` 하나를 근거 색인과 전체 행 대응표의 정본으로 유지합니다. 각 행에 위의 모든 필드, 상세 사실, 캡처 대응 관계와 실행하지 않은 행의 세부 사항을 포함합니다. 독립 대화 결과에는 아래의 간결한 행 요약만 보여 주고 전체 대응표 대신 README의 완전한 절대 경로를 제시할 수 있습니다. 근거 디렉터리에 다른 Markdown 파일을 추가하지 않습니다.

변경 전/후 비교에는 장면마다 간결한 행 하나를 사용합니다.
`scene | baseline observed value | after observed value | verdict`. 관찰값은 캡처 시점의
DOM/런타임에서 읽습니다. 해당 단계의 관찰값 문구를 정확히 그대로 캡처 레이블로 사용하고
필수 가림 처리를 유지합니다. 근거가 있을 때만 `match`, `intended change`나 `pre-existing issue`를 사용합니다.
예상하지 못한 변경이나 누락된 근거는 `regression` 또는 `unverifiable`로 보고합니다.
이 장면 설명은 기준 항목 상태를 대신하거나 기존 문제를 `Pass`로 바꾸지 않습니다.
의도상 대상 외곽선이 필요하지 않더라도 레이블은 픽셀로 확인하고,
`capture_only_mutation`에 레이블을 공개합니다. 기준 대상이 프레임 밖에 있는 캡처는 DOM 근거가 있더라도
해당 시각 기준을 뒷받침할 수 없습니다. 나타남/사라짐 비교에서 대상이 없는 쪽은 화면 밖 대상을 만들어 내지 말고,
화면에 보이는 주변 맥락에서 예상된 부재를 입증합니다.

선택적 HTML 갤러리나 콘택트 시트는 파생 보기이며, 필수 `README.md`나 원본 검사를 대신하지 않습니다.
근거의 절대 경로를 반환합니다. 사용자가 명시적으로 요청하지 않았다면 사용자 소유 브라우저나
데스크톱 열기 도구로 파일, 갤러리나 페이지를 열지 않습니다.
이 금지는 검증에 필요한 실행 소유 헤드리스 캡처/재실행을 막지 않습니다.

성공한 변경 전 기준은 중간 근거일 뿐 최종 판정이 아닙니다. 검증기는 상위 작업에 단계 근거를 반환하기 전에
자신이 소유한 서버, 컨텍스트와 브라우저를 해제해야 합니다. 이후 최종 헤드 재실행에는 새로운 실행 소유
런타임 자원과 저장된 변경 전 기준/재실행 조건을 사용합니다. 상위 작업은 PID나 살아 있는 브라우저 핸들이
아니라 근거의 출처 정보를 보존해야 합니다.

필수 식별 정보/출처 정보나 반환 메타데이터가 없으면 스크린샷을 검사했더라도 해당 단계는 `Unverifiable`입니다.
단계 `Pass`를 반환하기 전에 누락된 필드를 보고하고 수집합니다. 한계 메모나
`verification_complete: false`는 필수 근거 계약을 면제하지 않습니다.

성공한 편집 전 변경 전 기준은 참조 캡처가 존재한다는 사실만 입증합니다.
`next_required: implement candidate, then start fresh runtime resources and capture after with the saved baseline/replay`를 반환하고 종합 완료 표현을 사용하지 않습니다.
중첩 결과에서는 독립 결과용 `## Verdict`나 사용자 대상 완료 요약 없이 단계 필드를 사용합니다.
`status: Pass`는 요청된 단계만 설명합니다. `resume_parent`는 담당자에 대한 지시이지 스케줄러 신호가 아닙니다.
사용자가 독립 캡처만 요청했다면 상위 작업이나 구현 승인을 만들어 내지 말고 그 한정된 요청을 끝냅니다.
일치하는 변경 후 비교나 독립 최종 판정 단계에서 모든 기준 항목이 충족될 때만
`verification_complete: true`를 설정할 수 있습니다. 변경 후 결과는 같은 `run_id`, `baseline_provenance`와
`replay_procedure`에 연결됩니다. 변경 전 기준만 있는 결과는 최종 판정을 충족하거나 그 자체로 제품 편집, 커밋이나 발행을 승인할 수 없습니다.

검사한 이미지가 PR 발행에 필요하고 그 이미지가 나타내는 기준 항목이 `Pass`이면
[발행 근거](../../tk-verification-guidance/references/publication-evidence.md)의 생성자 중립 매니페스트를 반환합니다. 업로드하지 않습니다.
직접적인 추적, 접근성 트리, DOM/런타임과 요청/응답 근거는 일반 검증기 결과에 남기며
이미지 업로더를 작동시키지 않습니다. 상위 작업이 기준 항목을 직접 입증할 수 없는 이미지를 구체적으로 요구해도
형식적인 스크린샷을 만들지 않습니다. 이미지 발행 요구 사항을 `Blocked | Unverifiable`로 반환합니다.
`Pass`가 아닌 기준 항목은 소유한 실패 근거를 보존하고 실제 상태를 반환하며, 이에 대해 절대로
`verification_status:
Pass` 매니페스트 항목을 출력하지 않습니다.

재개할 활성 담당 작업이 없는 독립 결과는 필수 제목인 `## Verdict`와
정확한 `Status: <token>`으로 시작합니다. 계약, 헤드/환경 식별 정보, 범위와 검증 범위 개수를 보존합니다.
빈 절 없이 실제 검증, 실질적 한계, 정리나 잔여물과 사용자에게 남은 행동을 요약합니다.
완전한 기준 항목 행 대응표는 근거 README에 유지합니다.

실행하지 않은 각 행의 사유, `search_scope`와 `unblock`을 전체 대응표에 넣고,
사용자가 행동해야 할 때는 해당 ID와 다음 행동을 포함합니다. 담당 계약에 정확한 상태 꼬리말이 있으면 이를 보존합니다.
독립적인 변경 전 기준 성공은 여전히 캡처 전용이며 `verification_complete: false`를 유지합니다.
필수 런타임 근거 없이 결과를 절대로 `Pass`로 올리지 않습니다.

| 상태 | 의미 |
| --- | --- |
| `Pass` | 현재 검사한 근거가 승인된 모든 브라우저 기준 항목을 충족합니다. `scope`가 `explicitly-scoped`이면 전체 항목 목록의 통과는 아닙니다. |
| `Fail` | 현재 런타임 근거가 기준 항목을 위반합니다. |
| `Blocked` | 실행 전에 사용자가 안전이나 대상에 관한 결정을 내려야 합니다. |
| `Unverifiable` | 필수 헤드리스 인증, 환경이나 근거를 수립할 수 없습니다. |

승인받지 않은 결제, 외부 통신, 파괴적 변경, 운영 데이터 변경이나 계정/권한 변경을 일으키지 않습니다.

