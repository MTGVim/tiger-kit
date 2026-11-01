<a id="publication-evidence-handoff"></a>
# 발행 근거 인계

Screenshot을 캡처하거나 검사한 이미지가 PR 검토를 뒷받침할 수 있을 때마다 이 문서를 읽습니다. 이 검증 담당자는 이미지 발행 메타데이터만 만들며 근거를 업로드하거나 발행하지 않습니다. 직접적인 trace, accessibility tree, DOM/런타임과 요청/응답 근거는 일반 검증 결과에 유지하며 이미지 manifest나 형식적인 screenshot을 요구하지 않습니다.

<a id="exact-display-route"></a>
## 정확한 표시 경로

각 screenshot 행에 대해 실제 캡처 URL에서 scheme, 사용자 이름/비밀번호, hostname과 port만 제거하여 `display_route`를 도출합니다. Hash router 경로, 동적 개발 또는 검증 fixture ID와 상태를 담은 값을 포함하여 pathname, query와 fragment를 정확히 보존합니다. 로컬, preview 또는 staging 맥락이 중요하면 환경 label을 별도로 유지합니다.

캡처한 웹 URL이 없는 native 앱/창에서는 native 표면의 한계를 밝히고 `display_route`를 명시적으로 생략하며, 민감하지 않은 앱/창/build 식별 정보는 일반 근거에 유지합니다. URL을 만들어 내거나 존재하지 않는 웹 route를 필수 native 기준의 누락으로 취급하지 않습니다. Manifest의 `viewport`는 해당 native 표면의 실제 캡처 치수/배율을 설명합니다.

반환하거나 기록하기 전에 전체 경로가 PR 독자에게 안전한지 확인합니다. 동적 ID, query parameter와 fragment는 값이 달라진다는 이유만으로 민감하지 않습니다. 검토자가 캡처한 화면에 도달하는 데 필요한 값을 마스킹, 정규화, 잘라내기 또는 대체하지 않습니다.

경로에 실제 자격 증명, token, 세션 비밀, 서명된 parameter, 개인 데이터 또는 발행하기에 안전하지 않은 다른 값이 있다면 `display_route` 전체를 생략합니다. 그럴듯하지만 재현할 수 없는 마스킹 경로를 만들지 않습니다. 재현 한계를 밝히고, 주장이 정확한 도착 경로를 요구하면 `Blocked | Unverifiable`을 반환합니다. 비밀이 포함된 URL을 근거 index나 결과에 기록해서는 안 됩니다.

<a id="producer-neutral-manifest"></a>
## 생성자에 종속되지 않는 manifest

검사한 이미지가 통과한 수용 판정이나 회귀 보존 주장을 실질적으로 뒷받침할 때 다음 항목을 포함한 생성자 중립 PR 근거 manifest 항목을 반환합니다.

```text
evidence_required: true | false
evidence_kind: behavior | visual-change | visual-preservation
verification_status: Pass
criterion: <exact criterion>
artifacts:
  - role: baseline | after | acceptance
    path: <absolute inspected image path>
    display_route: <exact origin-free route | omitted with limitation>
    state_region: <captured state and region>
    viewport: <width x height, DPR, zoom>
    inspected: true
comparison: <not-applicable | byte-identical bounded region | inspected axes and result>
limitations: <none | exact limitation>
```

`behavior`는 검사한 이미지 자체가 동작이나 눈에 보이는 최종 상태를 직접 입증한다는 뜻입니다. Trace나 그 밖의 비이미지 근거를 감싸는 용도가 아닙니다. Schema에는 구현 controller나 발행 스킬 필드가 없습니다. 소비자는 일반 필수 항목을 검증하며 생성 스킬을 알아볼 필요가 없습니다. 실행 출처는 소비자 분기 계약 밖의 검증 결과에 유지합니다.

표현된 기준과 이미지 검사가 `Pass`일 때만 발행 manifest 항목을 출력합니다. `Fail | Blocked | Unverifiable`이면 실패 근거 계약에 따라 실행 소유 실패 산출물을 보존하고 실제 기준 상태를 반환하며 필수 이미지 발행을 차단 또는 검증 불가로 표시합니다. 실패하거나 미완료인 실행을 `verification_status: Pass`로 인코딩하지 않습니다.

검사한 이미지가 수용 판정이나 회귀 보존을 실질적으로 뒷받침하면 `evidence_required: true`를 설정합니다. 검토자에게 도움이 될 수 있지만 주장을 뒷받침하는 데 필요하지 않은, 검사한 선택적 이미지에만 `false`를 사용합니다. 없거나 검사하지 않은 이미지를 선택적 근거로 표현하지 않습니다.

시각적 `preserve` 주장에서는 대표 baseline과 after를 label이 있는 쌍으로 반환하고 `evidence_kind: visual-preservation` 및 `evidence_required: true`를 설정합니다. 한정된 파일이 바이트 단위로 동일하거나 선언한 비결정적 제외 사항을 적용해 검사한 모든 축이 통과했어도 동일합니다. 이 쌍은 “시각적 변경 없음”의 근거입니다. 선택적/N/A로 낮추거나 `after`만 반환하지 않습니다.

여러 레이아웃 맥락을 표본으로 삼을 때는 공통 컴포넌트 주장을 검토할 수 있게 하는 데 필요한 한정된 쌍을 포함하고, 표현되지 않은 것으로 알려진 맥락을 밝힙니다. 구별 없이 이미지를 쏟아내지 않습니다.
