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
PR evidence requirement/state
Evidence manifest entries/paths
Known exclusions

Single publication:
Head ref + SHA
Push refspec
Title
Title convention basis: <repository instruction | normative template/docs | merged-title evidence | fallback>
Body

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
  템플릿 상용구(HTML 주석, 바뀌지 않은 제목과 체크리스트)는 미리보기에서
  생략하되 발행 본문에는 그대로 보존하고, 정확한 전체 Markdown은
  활성 자료에 유지합니다(자료 규칙이 요구할 때만 `.tigerkit/pr-open.md`에 보관합니다). 전체 본문은
  요청받을 때만 표시합니다. 미리보기 서식은 발행 본문이나 업로드된 이미지 Markdown을 재작성하지 않습니다.
- 제목 관례의 근거와 템플릿 지침과의 불일치를 제시합니다.
- base/head를 제시합니다. 스택이라면 정확한 하위→상위 브랜치와 보존되는 원본 트리 불변 조건도 제시합니다.
- 유효한 `PR state`를 제시합니다.
- 검사·근거 상태를 제시합니다.
- 제외 사항과 위험을 제시합니다.
- 발행 권고 하나를 제시합니다.

`PR evidence requirement/state`가 여전히 `undecided`라면 이 점검 지점에서 구체적인 발행 미리보기 뒤,
어떤 쓰기보다 앞에 최종 질문 블록에 이미지 선택 사항을 포함합니다. 기존 자료 필드를 유지합니다.
