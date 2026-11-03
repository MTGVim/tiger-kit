<a id="publication-approval-packet"></a>
## 발행 승인 자료

활성 승인 자료에 다음의 정확한 정보를 기록합니다. 호스트가 단순한 단일 PR 자료를 충실하게
유지하고 다시 읽을 수 있다면 현재 대화에 보관합니다. 단일 파일 `.tigerkit/pr-open.md`는 스택,
명시적인 `save`, 여러 턴에 걸친 인계·복구 필요 또는 정확한 승인 상태를 다른 방식으로 유지할 수 없을 때만 사용합니다.
실행별 발행 파일은 만들지 않습니다. 산출물을 사용한다면 같은 담당자의 오래된 완료 내용을 원자적으로
교체하고 승인 전에 다시 읽습니다.

```text
Repository
Publication shape: single | stacked
PR operation: create | update
PR state: draft | ready
Base
Original head ref + SHA + tree
Template source/compliance
Template checklist: exact item + checked/unchecked + required/observed environment + evidence/limitation
PR evidence requirement/state
Evidence manifest entries/paths
Reviewed head/tree + diff basis + coverage/evidence (publication input)
Publication candidate head/tree + comparison with reviewed target
Known exclusions: unreviewed delta + re-review result | optional omission reason/approval
Remote actions: operation + exact target + proposed change + order + explicit approval

Single publication:
Head ref + SHA
Push refspec
Title
Title convention basis: <repository instruction | normative template/docs | merged-title evidence | fallback>
Body
Additional remote actions: selected tracker target + current/goal state + transition ID, or N/A

Stacked publication:
See the required plan fields in [retrospective stack split](split-to-stack.md).
```

산출물은 현재 PR 발행 계획만 담당하며, 제품 작업 계획이나 `worker` 상태를 담당하지 않습니다.
사용자가 `draft`를 명시적으로 요청하지 않으면 새 PR은 `ready`로 만듭니다.
같은 `head`의 기존 PR은 상태 변경을 요청받지 않은 한 새로 읽은 상태를 보존합니다.

다음을 사용자에게 자연스럽게 제시합니다. 사용자가 승인 전에 읽어야 할 내용은
대화 안에 표시하거나, 자료 규칙이 파일을 요구할 때 저장소의 `.tigerkit/` 산출물에 표시합니다.
세션 비공개 임시 메모 경로를 읽을 자료로 인용하지 않습니다. 사용자에게 보이는 미리보기에서
상용구를 생략하더라도 정확한 전체 제목·본문은 활성 자료에 유지합니다.

- 포함된 변경의 요약을 제시합니다.
- 권고하는 `single | stacked` 발행 형태와 이유를 제시합니다.
- 생성하거나 업데이트할 각 PR에 대해 제목과 이번 발행에서 채우거나 바꾸는 섹션을 미리 보여주어,
  사용자가 포함하거나 제외할 항목을 빠르게 결정할 수 있게 합니다. 각 섹션의 항목
  배치와 한두 줄 요약을 렌더링된 Markdown으로 표시하며 미리보기를
  코드 fence로 감싸지 않습니다. 응답에 본문의 `##` 제목을 복사하는 대신 굵은 섹션 라벨을 사용합니다.
  GFM 표와 이미지 그리드는 읽기 쉬운 한 줄로 요약합니다(예: 수정 전·후 이미지 두 장을 한 쌍으로 표시).
  중요한 항목별 선택이나 체크리스트 변경은 그 요약 밖에 유지합니다.
  체크리스트는 항목별 정확한 문구·최종 체크 상태와 환경 대조 결과를 반드시 보여줍니다. 템플릿 상용구(HTML 주석, 바뀌지 않은 제목)는 미리보기에서
  생략하되 발행 본문에는 그대로 보존하고, 정확한 전체 Markdown은
  활성 자료에 유지합니다(자료 규칙이 요구할 때만 `.tigerkit/pr-open.md`에 보관합니다). 전체 본문은
  요청받을 때만 표시합니다. 미리보기 서식은 발행 본문이나 업로드된 이미지 Markdown을 재작성하지 않습니다.
- 제목 관례의 근거와 템플릿 지침과의 불일치를 제시합니다.
- base/head를 제시합니다. 스택이라면 정확한 하위→상위 브랜치와 보존되는 원본 트리 불변 조건도 제시합니다.
- 유효한 `PR state`를 제시합니다.
- 검사·근거 상태를 제시합니다.
- 검토 대상과 발행 후보의 비교 결과, 바뀐 범위의 재검토 결과 또는 허용된 생략 사유를 제시합니다.
- 원격 행동별 대상·변경·순서와 개별 승인 여부를 제시합니다. 부가 행동이 없으면 `N/A`로 둡니다.
- 제외 사항과 위험을 제시합니다.
- 발행 권고 하나를 제시합니다.

`PR evidence requirement/state`가 여전히 `undecided`라면 이 점검 지점에서 구체적인 발행 미리보기 뒤,
어떤 쓰기보다 앞에 최종 질문 블록에 이미지 선택 사항을 포함합니다. 기존 자료 필드를 유지합니다.
선택 답변을 반영한 뒤 바뀐 항목과 현재의 최종 자료를 제시하고 별도 발행 확인을 받습니다. 같은 정확한 자료를 이미 승인받았다면 반복하지 않습니다.

<a id="reviewed-publication-target"></a>
## 검토 대상 대조

최종 발행 확인 전에 발행 입력으로 받은 검토 대상 head/tree와 현재 발행 후보의 head/tree 및 검토 diff 기준을 비교합니다. 입력이 없거나 대상을 입증할 수 없으면 `Unverifiable`로 발행을 보류하고 구현 담당자에게 필요한 근거를 요청합니다. head가 달라도 tree와 diff 기준이 같다고 입증되면 내용 차이 없음으로 기록합니다.

내용이 다르면 `Known exclusions`에 바뀐 범위와 `재검토 실행 | 재검토 생략(사유)`을 제시하여 미결 선택을 해결하고 최종 확인에 반영합니다. 재검토가 필요하면 구현 담당자에게 반환하여 결과를 받은 뒤 새 후보를 대조합니다. 필수 독립 리뷰를 생략 선택이나 테스트·정적 검사로 대체하지 않습니다. 생략은 기존 담당 절차가 허용하는 선택적 검토에만 가능하며, 미검토 범위와 사유를 명시적으로 승인받아도 검토 완료로 표기하지 않습니다. 스택은 원본 검토 트리와 최종 tip의 일치 및 계층별 검증을 함께 보존합니다.

<a id="additional-remote-actions"></a>
## 부가 원격 행동

PR 본문이나 발행 입력으로 연결이 확인된 티켓이 있으면, 지원된 읽기 도구로 현재 상태·전이 목록과 적용되는 팀 규칙을 조회한 뒤 발행 점검 지점의 질문 라운드에 상태 전이 선택지를 함께 둡니다. ready PR은 팀 규칙이나 트래커 근거로 확인한 리뷰 단계로, draft PR은 팀 규칙이 정한 상태로 옮기거나 그 규칙에 따라 현재 상태를 유지하는 선택지를 추천합니다. 상태명만 보고 목적을 추측하지 않으며, 맞는 목표 상태와 전이를 하나로 좁힐 수 없으면 후보를 보여 주고 추천을 붙이지 않습니다. 현재 상태 유지와 전이하지 않음도 선택할 수 있게 합니다. 사용자가 전이를 거절하면 같은 발행 안에서는 다시 묻지 않습니다. 현재 상태 유지나 전이하지 않음을 선택한 경우에는 원격 쓰기를 하지 않습니다.

연결된 티켓이 없거나 트래커의 현재 상태·전이 목록을 조회할 수 없으면 전이 질문을 생략하고, 부가 행동을 `N/A`와 이유로 기록한 뒤 기존 PR 발행 절차를 계속합니다. 전이를 제안하지 못했다는 이유만으로 PR을 보류하거나 도구 설치·연결을 요구하지 않습니다. PR 생성·업데이트 승인은 트래커 변경 승인이 아니며, 티켓 키가 본문에 있다는 사실도 승인으로 취급하지 않습니다.

전이를 실행할 행동마다 서비스·계정·프로젝트와 정확한 티켓 대상, 현재 상태, 목표 상태와 사용 가능한 전이 식별자, PR 발행 성공 뒤라는 실행 순서를 기록하고 항목별 명시적 승인을 받습니다. 상태명이나 전이 ID를 기억·고정값·다른 티켓에서 가져오지 않습니다. 유효한 경로가 여러 개이면 사용자의 선택을 받기 전까지 해당 행동만 미결로 둡니다. 전이 선택은 실행 승인이 아니며, 선택한 행동을 최종 자료에 반영하여 확인받습니다. 부가 행동을 제외하기로 결정하면 자료에서 제외한 뒤 PR만 확인받을 수 있습니다.

PR의 URL·head·승인한 draft/ready 상태와 실제 상태의 일치 및 필수 본문·근거 발행의 성공을 검증한 뒤 전이 직전에 대상·현재 상태·전이 목록을 다시 조회합니다. 승인한 목표 상태와 전이 ID가 여전히 적용될 때만 지원된 쓰기 도구로 정확한 전이 하나를 수행하고 결과 상태를 다시 읽습니다. 이미 목표 상태이면 추가 전이 없이 달성 상태를 보고합니다. 대상·현재 상태·전이 경로가 바뀌거나 실행 직전 조회가 실패하면 해당 행동을 보류하고 바뀐 제안이나 조회 실패를 보고합니다. 변경된 제안은 다시 확인받습니다. 응답이 유실되면 재시도 전에 실제 상태를 먼저 조회합니다. PR 생성 실패 시 전이를 실행하지 않으며, 부가 행동 실패로 성공한 PR을 되돌리거나 요청하지 않은 댓글·메시지·다른 상태 변경을 추가하지 않습니다.
