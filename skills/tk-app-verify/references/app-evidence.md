<a id="native-app-evidence"></a>
# native 앱 근거

캡처, 근거 쓰기 또는 실행한 단계의 반환 전에 읽습니다. [공통 검증 계약](../../tk-verification-guidance/references/verification.md)과 [산출물 경로](../../tk-artifacts/references/artifact-paths.md)를 적용합니다. native 근거는 URL/DOM이 아니라 창에 연결됩니다. 실행 소유 근거는 `.tigerkit/evidence/tk-app-verify/<run-id>/` 아래에 저장하고, 해당할 때 `baseline/`, `after/` 및 불변 `failed-<attempt>/` 캡처를 둡니다. 필수적인 범위 한정 `README.md`가 유일한 Markdown AC/근거 색인이며 수명 주기 장부가 아닙니다.

<a id="capture-and-annotations"></a>
## 캡처와 주석

기준과 필요한 맥락을 포함하는 가장 작고 읽을 수 있는 창 캡처를 사용합니다. 기본적으로 관련 없는 전체 desktop을 캡처하지 않습니다. 전체 desktop 캡처에는 이를 요구하는 기준과 검증된 비식별 처리가 필요합니다. process/app/build, 창 ID/제목, OS, locale, 역할, 크기, 배율, 캡처 원점/방법과 UI 상태를 기록합니다. 창 제목/경로는 민감할 수 있습니다. 비공개 값은 가리되 생략된 레이블을 검증했다고 주장하지 않습니다.

변경 전 기준과 변경 후 상태는 창 크기/배율/글꼴/상태/캡처 경계를 일치시켜 재현합니다. 이름이 있는 각 영역을 `appear | disappear | change | remain unchanged`로 분류하고 공통 윤곽선 표를 적용합니다. 원본 screenshot은 불변 런타임 근거로 보존합니다. native 화면에서는 같은 캡처의 대상 경계를 사용해 레이블이 있는 주석 파생본을 만들고, 원본과 주석본의 대응 및 좌표/배율 변환을 기록합니다. UI를 다시 그리거나 결함을 지우거나 주석을 원래 pixel인 것처럼 제시하지 않습니다. 정확한 경계나 주석 도구를 사용할 수 없으면 윤곽선을 생략하지 말고 필수 시각적 계약에 대해 `Unverifiable`을 반환합니다.
디코딩한 원본과 주석 이미지를 확인하고 필요한 모든 윤곽선과 레이블이 보이는지 확인합니다. 주석이 없거나 잘렸다면 캡처 실패입니다. 한계를 덧붙여 수용하지 말고 보존 후 다시 캡처합니다. 선택한 제공자가 지원하는 캡처/주석 경로를 사용합니다. 브라우저 DOM 변경은 native 주석 수단이 아닙니다.
`capture_only_mutation`은 각 윤곽선/레이블과 비식별 처리를 식별합니다. 캡처된 창이나 scroll 위치 밖의 대상은 그 기준의 근거가 아닙니다.

의도한 변경과 보존 영역은 별도로 판정합니다. 적용 가능한 모든 공통 시각적 축, geometry와 typography의 기준/후보/차이, 불일치 근거와 명시적인 편차를 기록합니다. native 창 크기 조절은 승인된 기준일 때만 브라우저 breakpoint를 대체합니다. native screenshot에 computed CSS나 DOM 출처를 지어내지 않습니다. 측정할 수 없는 값은 명시적인 한계이며 그에 해당하는 엄격한 충실도 주장을 막습니다.

<a id="result-fields"></a>
## 결과 필드

실행한 결과에는 다음을 포함합니다.

- 각 기준과 종합 결과의 `status`를 포함합니다.
- `phase: baseline | after | acceptance`, `run_id`, candidate/build 식별 정보와 재현 절차를 포함합니다.
- `provider`, version/host/OS와 관찰한 기능/입력 전달/권한 상태를 포함합니다.
- 민감하지 않은 app/process/창 식별 정보와 소유권, 인증 방식, 크기와 배율을 포함합니다.
- `visual_contract: applied | n/a`와 공통 계약에서 적용되는 점검/사유를 포함합니다.
- `capture_only_mutation: <description> | none`과 비식별 처리 사실을 포함합니다.
- 순서가 있는 캡처 행에 원본/주석본 절대 경로, 기준, 창/상태/영역, 캡처 방법, 유효 크기/배율과 실제 확인한 결과 또는 직접적인 비시각적 근거를 포함합니다.
- 각 시각적 캡처에는 대상 윤곽선의 `annotation: visible (pixel-checked) | none (remain unchanged) | none (target absent by intent)`과 `target in frame: yes | no`를 포함합니다. 대상이 없는 쪽에는 나타남/사라짐의 의도와 눈에 보이는 맥락이 필요합니다.
- 비교 쌍이 적용되면 비교 가능한 변경 전 기준의 출처, 축별 판정/측정값과 실패를 포함합니다.
- `verification_complete`, 정확한 `next_required`, 한계, focus 영향과 정리/잔여물을 포함합니다.
- 부모 또는 검증된 처리 결정에 따른 `automated_regression: protected | N/A | exception | unknown`을 포함합니다.

변경 전/후 비교에는 장면마다 간결한 행 하나를 포함합니다.
`scene | baseline observed value | after observed value | verdict`를 사용합니다. 캡처 시점의 현재 앱/접근성/런타임 근거에서 각 값을 읽고 눈에 보인다는 주장은 이미지로 확인합니다. native 화면의 DOM 측정값을 지어내지 않습니다. 필요한 비식별 처리를 거친 같은 단계별 관찰값 텍스트를 캡처 레이블로 사용합니다. 근거가 있을 때만 `match`, `intended change` 또는 `pre-existing issue`를 사용합니다. 예상하지 못한 변경이나 근거 누락에는 `regression` 또는 `unverifiable`을 사용합니다. 실제 기준 상태를 유지합니다. 장면 설명은 면제 사유가 아닙니다. 대상 윤곽선이 필요하지 않은 경우에도 레이블을 pixel로 확인합니다. 프레임 밖의 대상은 시각적 기준을 뒷받침할 수 없습니다. 나타남/사라짐 비교에서 대상이 없는 쪽은 주변 맥락을 보여야 합니다.

전체 결과 필드, 비교 행과 캡처 대응 관계는 근거 `README.md`에 둡니다. 선택적인 HTML gallery/contact sheet는 파생 뷰이며 해당 색인이나 원본 이미지 확인을 대체하지 않습니다. 사용자의 브라우저나 desktop opener로 근거를 열지 않고 절대 경로를 반환합니다. 사용자가 명시적으로 요청한 경우에만 엽니다. 요청받아 여는 경우에도 선택한 제공자의 focus와 승인 요구를 유지합니다.

사전 점검 중단에서는 실제 상태, 누락된 선행 조건과 다음 입력만 반환합니다. 캡처나 완료 필드를 지어내지 않습니다. 변경 전 기준은 캡처만 수행하며 `baseline_capture: Pass`, `verification_complete: false`를 사용하고, 부모가 진행 중이면 `resume_parent: required`를 사용합니다. 변경 후 결과는 같은 실행/출처/재현 절차에 연결되며 모든 기준을 다룬 경우에만 완료됩니다.
독립 실행 출력은 정확한 `Status: <token>`으로 시작하고 간결한 사실/한계/정리 내용을 제시합니다. 중첩 실행은 사용자에게 최종 답변하지 않고 해당 단계의 근거를 반환한 뒤 담당자를 재개합니다.

이미지가 발행을 실질적으로 뒷받침하면 [제작자 중립 발행 manifest](../../tk-verification-guidance/references/publication-evidence.md)를 사용하고, 변경되지 않은 영역도 필요한 변경 전/후 쌍을 반환합니다. 표현한 화면에 실제 route가 있는 경우에만 민감하지 않고 origin이 없는 `display_route`를 사용합니다. native 창은 native 화면이라 생략했다는 사실을 명시하고 app/창 식별 정보는 일반 근거에 유지합니다. 웹 route를 지어내거나 근거를 업로드하거나 검증되지 않았거나 실패한 기준에 `Pass` manifest 항목을 내보내지 않습니다.

<a id="optional-video-handoff"></a>
## 선택적 동영상 인계

요청되거나 승인된 동영상에 한해서만, 선택한 native 제공자가 지원하는 경우 실제 timestamp가 있는 발행에 안전한 프레임을 수집합니다. 인계에는 app/창/build 식별 정보, 배율과 캡처 원점을 유지합니다. 소유한 `mode: evidence` manifest(`frames`에 절대 `path`와 `timestamp_ms`, 추가로 `end_ms`를 포함)를 `tk-video`에 전달합니다. 다른 패키지의 script 경로를 호출하지 않습니다.
실제 캡처, 입력, 권한, 테스트 데이터와 자원 수명 주기는 검증 담당자가 계속 담당합니다.
Screen Recording 권한이 없거나 녹화가 지원되지 않으면 미디어를 생략하되 독립적으로 뒷받침된 앱 판정은 바꾸지 않습니다. 같은 제약이 필수 screenshot도 막는다면 해당 시각적 기준은 검증되지 않은 상태로 남습니다. native 캡처를 브라우저 근거로 대체하지 않습니다.
이 요청은 자동 설치, 권한 변경이나 발행으로 이어지지 않습니다.
