<a id="nested-baseline-after"></a>
# 중첩 baseline/after 단축 계약

상위 구현 작업에 종속된 **단순 읽기 전용 UI의 baseline 또는 after 한 단계**에만 사용합니다.
이 문서는 상세 참조를 무조건 읽는 대신 **필수 필드·순서**를 보존하는 한정된 경로입니다.
독립 최종 판정, 접근성 감사, 미디어 캡처, 레이블 조사, 데이터 쓰기·외부 통신·공유 상태 변경,
복잡한 디자인 비교, 애니메이션, 다중 소비자 레이아웃 감사에는 사용하지 않습니다.
조건을 하나라도 증명할 수 없으면 실행 전에 일반 경로로 돌아가 해당 전체 참조를 읽습니다.

## 1. 부모 인계와 선행 조건

첫 제품 상호작용·서버 시작 전에 다음 사실을 상위 작업의 근거와 현재 작업 상태에서 **직접 대조**합니다.

- 저장소/워크트리, baseline 소스의 정확한 HEAD·트리·빌드 입력, after 후보 HEAD·트리,
  기존 `run_id`, 상위 담당자와 유효한 검증 승인. baseline은 **제품 편집 전** 소스에서 캡처합니다.
- 전체 기준 항목 ID/범위, 화면/진입 경로·실제 렌더링 텍스트, 승인된 **읽기 전용** 탐색 단계,
  캡처 목적·상태, `appear | disappear | change | remain unchanged` 분류.
- 제공자의 실제 ID/버전/실행 명령, 설치된 Playwright CLI 기본값 또는 명시적 선택의 출처,
  **현재 확인한** headless 모드·실행 소유 세션/프로필, 개발 서버 명령·준비 상태·소유 PID/핸들.
  이전 실행의 소유권, 포트나 인증된 브라우저를 그대로 재사용하지 않습니다. 부트스트랩/연결 방식이
  미확인이라면 [제공자 선택](../../tk-verification-guidance/references/provider-selection.md),
  [환경](environment.md), [세션 수명 주기](session-lifecycle.md)로 전환합니다.
- 비민감 인증 모드와 현재 인증 상태. **새 인증 수립/갱신·비밀 주입이 필요하면**
  [헤드리스 인증](headless-auth.md)과 [환경](environment.md)으로 전환합니다.
- 동일하게 재현할 viewport, DPR, zoom, font, UI 상태·locale, baseline 출처와 재생 절차.
  모호하거나 비교 조건이 다르면 `Unverifiable`입니다.
- 경로의 실제 소유권·비심볼릭 링크 여부, `git ls-files -- .tigerkit/`에 추적 파일 없음,
  `git check-ignore -q -- .tigerkit/` 성공. 실패하면 쓰지 않고
  [산출물 경로](../../tk-artifacts/references/artifact-paths.md)로 전환합니다.

## 2. 캡처 이전: 가림 선언이 먼저입니다

제품에 상호작용하기 전에 공유 clipboard·사용자 파일·알림·계정·외부 네트워크를 **변경하지 않음**을 확인합니다.
실행 소유 브라우저/서버만 열고 헤드리스를 재확인합니다. 민감한 화면의 선택자를 원시
스크린샷 없이 DOM/사전 계획으로 식별합니다. **첫 캡처 전에** 근거
`.tigerkit/evidence/tk-browser-verify/<run-id>/README.md`를 생성하고,
**첫 줄**을 `sensitive_regions: <selector 목록 | none(이유)>`의 실제 값으로 씁니다.
없음을 확인한 경우에만 구체적인 `none(확인 근거)`를 사용합니다. 누락·불확실·무효 값은
계약 위반이므로 **캡처하지 않고** `Unverifiable`로 중단합니다. 이후 화면이 달라지면
다음 캡처 전에 첫 줄의 선택자를 다시 확인·갱신하고 변경 이유를 색인에 남깁니다.
민감 영역을 캡처 순간에 clip/mask할 수 없으면 이미지 대신 안전한 비시각 런타임 근거를 사용하고
해당 시각 기준은 `Unverifiable`로 유지합니다. **원본 fullPage/비식별화 전 캡처를 저장하지 않습니다.**
민감 데이터의 별도 취급이 필요하면 [안전](safety.md)을 읽습니다.

## 3. 단계별 수행 순서

1. `baseline`: 편집 전 현재 소스의 출처를 기록하고 `baseline/`에, `after`: 보존한 baseline과
   재생 조건을 재확인한 뒤 새 서버·브라우저에서 `after/`에 캡처합니다. 실패 시도는
   고유 `failed-<attempt>/`에 보존하며 기존 파일은 덮어쓰지 않습니다.
2. 캡처 **직전** 목적지가 해당 단계 디렉터리 안이며 존재하지 않는지 검사합니다.
   민감 영역을 먼저 mask/clip하고 읽을 수 있는 최소 viewport에 기준과 맥락을 담습니다.
   의도된 변화만 윤곽선으로 표시하고 `remain unchanged`에는 표시하지 않습니다.
   대상 외곽선·레이블과 실제 viewport, `capture_method`를 픽셀로 확인합니다.
3. 캡처 뒤 경로에 파일이 존재하고 비어 있지 않은지 확인하고 **실제 픽셀을 검사**합니다.
   `baseline`은 관찰값·캡처 상태와 출처를 기록하며 최종 통과가 아닙니다.
   `after`는 baseline과 비교 가능한 장면별로 의도한 변화·보존 영역을 분리하고,
   기하(위치·크기·간격), 타이포그래피(글꼴·크기·줄바꿈), 색·콘텐츠·클리핑·반응형·
   상호작용의 **해당하는 모든 비교 축**을 검사합니다. 기하/타이포그래피 필수 축은
   참조·후보·차이 측정값을 남깁니다. 미검사 축, 원치 않은 보존 영역 차이나
   기준이 프레임 밖인 이미지는 `Pass`가 아닙니다. 상세 시각 판정이나 콘텐츠 출처
   확인이 필요하면 [시각 검증](visual.md)과 [근거와 결과](results.md)를 읽습니다.
4. 캡처 직후 실행 소유 브라우저/컨텍스트와 개발 서버를 **단계마다 즉시 종료**하고
   실제 PID/핸들·종료·잔여물을 확인합니다. 사용자 자원은 종료하지 않습니다.
   다음 단계에는 살아 있는 세션 대신 같은 `run_id`의 baseline/재생 기록을 사용합니다.

## 4. 근거 README 및 중첩 반환

README 첫 줄의 `sensitive_regions`와 단계별 적용 이유를 지키고, 각 기준 ID를 이미지와
일대일 대응시킵니다. `provider`(실제 ID/버전/경로/선택 근거), `contract: 1.2.0`,
`scope: full-inventory | explicitly-scoped`, `coverage: planned/executed/covered-by/out-of-scope/not-executed`,
`human_action`, `phase`, `visual_contract: applied`, `capture_only_mutation`,
`automated_regression`, 인증 방식(비민감), 근거 절대 경로, 정확한 대상/head/출처,
캡처별 파일·`display_route`·기준/상태·마스킹·뷰포트·`capture_method`·
`annotation`·`target in frame`·관찰값·비교 결과·예외/제외 사유, 재생 절차,
`limitation`과 정확한 실행 소유 자원 정리 사실을 남깁니다.
각 기준의 사실 행에는 `criterion_id`, `result`, `route`, `entry`, `trigger`,
`operation: read`, `input: trusted | not-run`, `evidence_kind`, `evidence_ref`, `head`를 포함합니다.
미실행 행에는 `reason`, `search_scope`, `unblock`; 명시적 제외/다른 행으로 커버한
기준에는 해당 사유·근거 참조를 보존합니다. 장면 비교는
`scene | baseline observed value | after observed value | verdict`로 기록합니다.
다른 Markdown/세션 원장은 만들지 않습니다.

부모에게는 간결한 **단계 사실만** 반환합니다. `baseline` 성공은
`status: Pass`(그 단계 한정), `baseline_capture: Pass`,
`verification_complete: false`, `run_id`, `replay_procedure`,
`next_required: implement candidate, then start fresh runtime resources and capture after with the saved baseline/replay`,
`resume_parent: required`를 포함합니다. `after`도 모든 지정 기준과 비교 축을
확인한 경우에만 `verification_complete: true`가 가능합니다.
누락·불명확한 권한, 출처, 인증, 가림이나 근거 메타데이터가 있으면
`Blocked | Unverifiable`로 반환하며 성공을 꾸미지 않습니다.
`media-capture`나 PR 이미지 발행 매니페스트가 필요하면 전체 분기로 전환합니다.
