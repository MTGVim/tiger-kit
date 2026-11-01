<a id="provider-integration-knowledge"></a>
# 제공자 통합 지식

선택한 제공자의 절만 읽습니다. Registry capability는 가능한 기능이며 런타임 지원표가 아닙니다. 현재 버전, 호스트/플랫폼, 권한과 행동별 의미를 확인합니다. 설치와 누락된 권한은 범위가 제한된 `tk-wizard` 설정 인계에 속합니다. 검증 탐색 중 설치하거나 무제한 모드를 켜거나 focus를 바꾸는 설정을 열지 않습니다. 기억한 API 이름 대신 registry의 정본 문서와 제공된 호스트 지침을 사용합니다.

<a id="distillation-provenance"></a>
## 증류 출처

계약 유지보수에는 다음 검토된 출처(2026-09-30부터 2026-10-13까지)를 사용한 뒤 설치된 제공자 버전의 정본 문서를 갱신하여 확인합니다. TigerKit의 기존 headless/근거 소유권을 유지합니다. 독립 postcondition 점검과 백그라운드/권한 확대 경계를 적용합니다. Upstream 설치기, 전역 입력 예시와 자동 런타임/권한 확대는 제외합니다.

- Cua [독립 postcondition 예시](https://github.com/trycua/cua/blob/0f29c142d7fe3e05ea0ce276cee11b3a9725ba01/libs/cua-driver/examples/agent-sdks/native_driver.py)와 공식 백그라운드/플랫폼 및 검증 안내를 확인했습니다. 예시의 전역 데스크톱 입력은 승인된 백그라운드 adapter가 아닙니다. 불확실한 응답을 검증하는 동작만 유지합니다.
- Orca [버전 일치 안내 로더](https://github.com/stablyai/orca/blob/f4068747ac96cb526c7233683fc1cd89cad5f289/skills/computer-use/SKILL.md)와 공식 computer-use 안내를 확인했습니다. 실행 파일 식별과 최신 창 snapshot guard를 적용하며 자동 앱 열기/재시작과 승인되지 않은 좌표 fallback은 제외합니다.
- 제공자 registry URL은 유지보수자/공식 출처로 검토했습니다. Host-native 지원은 실제 도구 노출을 조건으로 합니다. 이 문서로 native 호스트의 실제 검증을 수행했다고 주장하지 않습니다.
- Cua macOS drag(2026-10-05): `trycua/cua` revision `61ec8ac1d80df191bccd7fc9e9275123a809b2f7`,
  `libs/cua-driver/rust/crates/platform-macos/src/tools/drag.rs`(구현, schema와 거부 테스트), `libs/cua-driver/rust/Skills/cua-driver/MACOS.md`,
  `docs/content/docs/cua-driver/reference/mcp-tools/pointer.mdx`와 commit 근거를 확인했습니다. 독립 postcondition과 정확한 권한을 유지하고 foreground 전용 예외를 적용합니다. 데스크톱 범위 입력과 자동 권한 확대는 제외합니다. Native 테스트는 검사했지만 다시 실행하지 않았습니다.
- Cua macOS launch(2026-10-02): `trycua/cua` revision `8d4e7a08618611453794035f7ff6187f99f0c1e9`,
  `libs/cua-driver/rust/Skills/cua-driver/MACOS.md`,
  `libs/cua-driver/rust/crates/platform-macos/src/tools/launch_app.rs`와
  `libs/cua-driver/rust/crates/cua-driver-e2e/tests/installed_app_launch_macos_test.rs`를 확인했습니다. 제공자 소유 launch와 독립 focus 점검을 유지합니다. 사용자가 제공한 raw 실행 파일 wrapper 사례를 정확한 식별과 정리 점검을 통해 적용하며 활성화 우회책은 제외합니다. 시스템 임시 경로 조회와 wrapper 성공은 제공된 사건 근거이며 upstream의 보편적인 주장이 아닙니다. Native 테스트는 검사했지만 다시 실행하지 않았습니다.

- Cua scroll/token/snapshot(2026-10-07): `trycua/cua` revision
  `5227ad637590a15976413b1a33f8693fac0e9a7e`, macOS `tools/scroll.rs`, `tools/mod.rs`
  및 `tools/get_window_state.rs`, core `snapshot_store.rs`와 `window_state_view.rs`를 확인했습니다. 독립 postcondition과 foreground 권한을 유지합니다. 명시적 scroll 거부, token 소유 프로세스 식별과 선택적인 범위 제한 diff 읽기를 적용합니다. 전역 입력, 자동 권한 확대와 제공자 간 가정은 제외합니다. 공통 token/window-view 테스트는 검사했지만 다시 실행하지 않았습니다. macOS 실제 전달은 여기서 검증되지 않았습니다.

- Cua macOS 백그라운드 scroll과 축약 메뉴(2026-10-13): `trycua/cua`
  revision `ea32762c9207912eaa73622fda62835d9aef6206`과
  `c1c2b5fee428c3a39bebe5e77549c3d3525a608d`를 확인했습니다. 버전 조건부 AX scroll, 행동별 관찰 이동과 대상별 메뉴 조회를 유지합니다. 자동 foreground fallback은 제외합니다.
- Cua 다른 Space 캡처, 백그라운드 hover와 AX 문서 편집(2026-10-13):
  `trycua/cua` revision `a1637f5e2d7ed156f4f74130484c3ea9140bec3f`,
  `e1ed4f41cdc0bf77dc7d7e8f828ae775c75bf834`와
  `adadbe2f53b9227f95493d2a9a28a2911177001e`를 확인했습니다. 최신성, 행동 권한과 디스크 영속성 경계를 유지합니다. 암묵적 inspector 설정, 창 활성화와 제공자 내부 구현 복사는 제외합니다. Native 호스트 동작은 검증되지 않았습니다.

## Chrome DevTools MCP

설정된 launch/attach 모드와 유효 headless 설정을 검사합니다. 관리되는 pipe에는 TCP endpoint가 필요하지 않습니다. 전용 persistent profile에는 격리 한계를 밝혀야 합니다. 네트워크/console/DOM과 성능 도구는 설치 버전과 노출된 도구 목록에 따라 달라집니다. 브라우저 환경 참조의 attach, 소유권과 인증 요구 사항을 보존합니다.

## Playwright

저장소에 설치된 Playwright와 MCP를 구별합니다. Headless 옵션, 브라우저 바이너리, context 격리, transport와 실제 네트워크/console 도구를 확인합니다. 격리된 profile은 시나리오별로 격리된 context의 증거가 아닙니다. 최신 페이지 근거에서 selector를 확인합니다. 준비 상태를 탐지하려고 브라우저나 npm 패키지를 다운로드하지 않습니다.

## Browser CDP

설치된 브라우저 CLI나 Puppeteer adapter는 현재 문서화된 진입점을 노출해야 합니다. Protocol URL에 더해 버전이 일치하는 help/저장소 지침을 사용합니다. 다른 CLI의 flag에서 해당 CLI의 flag를 추론하지 않습니다. 실제 CDP endpoint에는 브라우저 호출 전에 headless와 실행 소유권 증명이 필요하며, 관찰된 launch 경계 근거 후 명시적인 attach 선택이 필요합니다.

`Page.captureScreenshot`에서는 scroll된 페이지의 `clip`을 전달하기 전에 viewport 상대 대상 사각형을 문서 좌표로 변환합니다. 실제 픽셀을 검사합니다. `captureBeyondViewport: true`이면 보이는 viewport 밖의 fixed 요소가 캡처에 나타날 수 있습니다. Screenshot을 튜토리얼 overlay와 독립적으로 유지하고 캡처 한계를 보고합니다.

<a id="installed-chrome-cli-capture-caveats"></a>
### 설치된 Chrome CLI 캡처 주의 사항

제공된 2026-10-07 사건에서는 CLI `--screenshot`이 scroll된 빈 영역을 캡처했고, 높이 20000px 캡처가 멈췄으며, 유효 너비가 500px로 제한되었습니다. 이는 환경별 관찰이며 Chrome/CDP의 보편적인 한계가 아닙니다. 실제 viewport와 설치 버전의 동작을 검증합니다. 제한된 캡처와, 사용 가능하다면 제공자가 지원하는 영역 캡처를 우선합니다. 캡처를 위해 앞선 콘텐츠를 숨기는 것은 정확한 원본/상태를 보존하고 제품 화면을 복원하는 명시적으로 기록된 `capture_only_mutation`으로만 허용됩니다. 변경되지 않은 기하 구조를 입증할 수는 없습니다. 측정 도우미 자체가 문서 너비를 늘릴 수 있습니다. 먼저 측정하고 도우미가 영역을 벗어나지 않게 하며 최종 overflow 점검 전에 제거합니다. 빈 픽셀이나 잘린 픽셀은 수용 판정을 입증하지 않습니다.

시작 전에 `--user-data-dir`을 감시되는 소스 트리 밖의 literal 절대 실행 소유 경로로 선택하고 산출물 경로 소유권 점검 아래 같은 literal 경로로 삭제합니다. `mktemp`나 명령 치환으로 생성한 뒤 변수를 통해 삭제하지 않습니다. 즉시 정리와 남은 프로세스 점검을 유지합니다.

## BrowserSkill

`bsk` CLI에는 extension/daemon과 선택된 Chrome/Edge profile이 필요합니다. 현재 upstream은 보이는 agent 창을 사용하며 사용자 tab을 빌릴 수 있습니다. 이는 선택적인 로그인 상태 자동화이며 TigerKit의 headless 전용 브라우저 수용 판정에는 적합하지 않습니다. 자동 fallback으로 사용자 profile을 빌리거나 extension 연결을 시작하지 않습니다. 불일치와 대안을 보고합니다.

## BrowserMCP

기본 권고 밖의 역사적/참고 메타데이터로 유지합니다. 명시적 요청 전에 유지보수 활동과 현재 문서를 다시 확인합니다. 참조 항목만으로 현재 준비 완료를 주장하거나 extension 연결을 headless 제공자로 취급하지 않습니다.

## Cua Driver

바이너리, daemon, doctor 경고와 실제 driver 권한을 각각 확인합니다. 버전 문자열만으로는 데스크톱 접근을 입증하지 못합니다. macOS에서는 Accessibility와 Screen Recording을 확인합니다. Windows에는 대화형 사용자 세션이 필요하며 Linux 경로는 accessibility/display 지원에 따라 달라집니다. 백그라운드는 best effort입니다. 최신 semantic token을 우선합니다. 창 범위 좌표에도 현재 캡처/배율과 관찰된 안전한 전달이 필요합니다. 다른 Space의 SwiftUI/canvas와 Wayland raw-key 한계가 시나리오를 막을 수 있습니다. Foreground 전달을 자동으로 켜지 않습니다. 불확실한 응답 후에는 입력을 확인 없이 반복하지 말고 독립 postcondition을 검증합니다.

<a id="semantic-identity-and-snapshot-reads"></a>
### 시맨틱 식별과 스냅샷 읽기

설치된 action schema가 허용하면 현재 `element_token`은 자체 process/window 식별 정보를 해석합니다. 해당 snapshot을 정확한 후보와 대조한 후에만 중복 `pid`를 생략합니다. 명시적인 `pid`나 window ID가 충돌하면 입력을 중단합니다. 어느 식별 정보도 몰래 우선하게 하지 않습니다. 알 수 없거나 오래된 token에는 식별 정보 추측이 아니라 새 읽기가 필요합니다. Snapshot 읽기와 좌표 action에는 각각 요구되는 process/window 필드를 유지합니다.

지원되는 Cua `get_window_state`에서는 전체 읽기(`since` 없음)로 시작하고 충분하다면 축약 tree 표현 하나를 사용합니다. 같은 process/window와 query/node/depth 범위가 안정적이면 알려진 전체 기준과 일관된 diff 연결에 대해 선택적으로 `since:<snapshot_id>`를 사용합니다. `since_status`, 잘림과 재색인 여부를 확인합니다. 새 snapshot ID와 현재 token을 사용하며 대체된 token을 재사용하지 않습니다. 범위 변경, 오래되거나 알 수 없는 기준, 잘림, 불확실한 연결 또는 부족한 근거가 있으면 기준을 관찰할 만큼 충분한 범위의 전체 읽기가 필요합니다. 전체란 diff 기준이 없다는 뜻이며 반드시 `full_output:true`라는 뜻은 아닙니다. Diff는 독립적인 현재 상태 근거가 될 수 있지만 빈 diff나 action 성공은 기준을 입증하지 않습니다. 시각적 기준에는 여전히 검사한 현재 픽셀이 필요합니다. 다른 제공자에 대해 이 capability를 추론하지 않습니다.

macOS의 다른 Space 캡처 지원은 현재 픽셀이나 accessibility 상태를 보장하지 않습니다. Chromium에서 다른 Space의 action이 성공하거나 screenshot에 `on_current_space:false` 또는 명시적인 오래된 상태 메모가 있으면 최신 postcondition 근거가 아닙니다. 숨겨진 페이지는 painting이나 AX 갱신을 멈출 수 있습니다. Action 전달과 상태 최신성을 분리합니다. 현재 UI 기준을 수용하기 전에 검증된 최신 읽기를 확보합니다. 그렇지 않으면 `Unverifiable` 또는 `Blocked`를 보고합니다. 검증만을 위해 다른 Space를 활성화하지 않습니다.

최근 Cua 기본 창 읽기는 닫힌 메뉴를 최상위 제목으로 축약할 수 있습니다. 기본 tree에 닫힌 메뉴의 자식이 없다는 사실은 메뉴 항목이 없다는 증거가 아닙니다. 범위가 제한된 `query`로 숨겨진 항목을 찾고 `invoke_menu`로 실행합니다. 기준에 실제로 전체 tree가 필요할 때만 `full_output`을 요청합니다. 열린 메뉴는 현재 읽기에서 노출되면 계속 관찰할 수 있습니다. 다른 제공자가 이 메뉴 표현을 공유한다고 가정하지 않습니다.

<a id="macos-electronchromium-scroll"></a>
### macOS Electron/Chromium 스크롤

macOS Electron/Chromium에서는 백그라운드 wheel 전달이 실패할 수 있지만 지원되는 Cua 버전은 accessibility hit-testing과 `AXScrollToVisible`로 scroll할 수 있습니다. 백그라운드 지원을 판단하기 전에 설치된 action schema, 버전과 응답을 확인합니다. 지원되는 백그라운드 경로를 우선하며 관찰된 이동을 요구합니다. 이전 또는 알 수 없는 버전의 지원을 추론하지 않습니다. 실제 `background_unavailable`이나 이동 없음 결과는 성공이 아닙니다. 동일한 백그라운드 재시도를 중단합니다. 권한 확대 전에 정확히 일치하는 기존 foreground 권한을 재사용하거나 요청합니다. 그렇지 않으면 기준을 `Blocked`로 남깁니다. `foreground_fallback:true`를 자동으로 켜지 않습니다. 이 action 계약을 drag, 다른 표면, 플랫폼이나 제공자에 일반화하지 않습니다.

<a id="macos-background-hover"></a>
### macOS 백그라운드 호버

Cua는 AX alternate UI, Electron page hover와 Electron main-process inspector 기반 hover에 대해 서로 다른 macOS 경로를 노출할 수 있습니다. 선택 전에 설치된 제공자의 실제 capability와 결과를 확인합니다. `hover`는 수동적 관찰이 아니라 action입니다. 이미 지원되는 제공자 내부 경로가 새 inspector port, 애플리케이션 launch flag, debugging 권한이나 런타임 설정을 허용하지는 않습니다. Action에 그런 권한 확대가 필요하면 자동으로 활성화하지 않습니다. 성공한 hover 응답을 믿는 대신 기대한 UI 변화를 독립적으로 관찰합니다.

<a id="macos-ax-document-text-writes"></a>
### macOS AX 문서 텍스트 쓰기

Accessibility 텍스트 쓰기는 앱의 문서 편집 모델이나 저장 파일을 갱신하지 않고 보이는 필드만 갱신할 수 있습니다. 수용 기준에 파일 영속성이 포함되면 실제 저장된 문서 상태를 검증합니다. 특히 autosave 문서에서는 AX 텍스트와 편집 표시만으로 부족합니다. 제공자의 `document_edited` 경고를 보존하고 최신 저장/readback이 불가능하면 영속성을 미검증으로 표시합니다. 일반 텍스트 입력 기준에는 무관한 디스크 점검이 필요하지 않습니다.

<a id="macos-drag"></a>
### macOS 드래그

macOS에서 Cua 창 범위 픽셀 `drag`는 foreground 전용이며 best-effort 백그라운드 action이 아닙니다. 먼저 백그라운드 drag를 시도하지 않습니다. `background_unavailable`로 거부되며 아무것도 보내지 않습니다. Gesture 자체가 필요하면 입력 전에 정확히 일치하는 기존 foreground 권한을 재사용하거나 요청합니다. 그렇지 않으면 `Blocked`를 반환합니다. 정확한 `window_id`와 최신 캡처 좌표를 연결하고 일시적인 최상위 창과 물리 pointer 이동을 고지하며, driver의 복원 시도 후 최신 상태, focus와 독립 postcondition을 검증합니다. 값 변경 결과가 목적이라면 동등할 때 지원되는 semantic action을 우선합니다. macOS AX에는 일반적인 semantic drag가 없습니다. 다른 action과 플랫폼에는 각각 관찰된 전달 계약을 적용합니다. 전역 데스크톱 입력으로 대체하지 않습니다.

<a id="macos-launch"></a>
### macOS 실행

Native 앱 launch에는 설치 버전의 `launch_app` schema와 포함된 `MACOS.md`를 읽습니다. 문서화된 `launch_app({bundle_id})` 경로를 사용합니다. 검토한 macOS 구현은 대상의 자체 활성화를 막으며 `self_activation_suppressed`를 반환할 수 있습니다. true 결과는 guard의 결과를 뒷받침하며 보편적 보장은 아닙니다. 이전 최상위 앱/focus와 launch 후 최신 상태를 독립적으로 비교합니다. 필드가 false이거나 없으면 긍정적인 증거가 아닙니다. 어떤 형태의 shell `open`이든, AppleScript 활성화나 자체 활성화하는 저장소 명령은 백그라운드 launch의 대안이 아닙니다. 선택한 제공자의 launch 계약을 우회하는 데 사용하지 않습니다.

Bundle이 없는 이미 컴파일된 raw 후보에는 실행 소유 `.app` wrapper가 정확히 그 실행 파일을 복사(symlink가 아님)하고 별도의 `CFBundleIdentifier`를 사용하여 설치된 release가 조회에서 선택되지 않게 할 수 있습니다. 필요한 자원, library, 작업 디렉터리와 런타임 설정을 보존합니다. 이동으로 후보가 달라지거나 지원되지 않는 signing/설정 우회책이 필요하다면 동등성을 주장하지 말고 중단합니다. `launch_app` 전에 등록된 식별 정보가 이 wrapper의 정확한 경로와 후보로 해석되는지 검증하고 반환된 process/window를 연결합니다. 등록만으로 조회를 입증하지 못합니다. 플랫폼이 시스템 임시 경로를 무시하면 저장소 `.tigerkit/tmp/` 같은 점검된 실행 소유 비시스템 임시 위치를 사용합니다. 등록이 미해결이면 `Blocked`입니다. 등록은 일시적이며 실행 소유입니다. 앱 설치나 기존 식별자의 대체가 아닙니다. 정리 시 이 실행의 등록만 해제하고 wrapper를 삭제합니다. 설치된 release의 등록을 해제하거나 제거하지 않습니다.

다른 제공자/플랫폼에는 자체적인 현재 launch 근거가 필요합니다. 이 macOS 의미가 해당 호환성을 입증하지 않습니다.

## Orca Computer

Orca 명령 전에 현재 upstream 안내에서 세션의 실행 파일을 확인합니다. Linux의 Orca terminal 밖에서는 단독 `orca`가 GNOME screen reader일 수 있습니다. IDE 탐지를 위해 실행하지 않습니다. 확인한 실행 파일의 버전과 일치하는 `skills get computer-use` 안내를 로드한 뒤 상태, 권한과 capability를 확인합니다. 상태 변경 후 앱/창 snapshot을 갱신합니다. Index는 해당 snapshot에 속합니다. Semantic action은 직접 수행할 수 있지만 raw keyboard/좌표나 창 복원은 focus를 빼앗을 수 있습니다. 실제 경로를 검증하고 정확한 권한 확대 승인을 구합니다.

## Codex Native

현재 공식 computer-use 문서와 실제 호스트가 알리는 API를 읽습니다. Native 앱 접근이 활성화되어 호출할 수 있을 때만 이 제공자를 노출합니다. 브라우저 전용 capability로는 native 창을 검증할 수 없습니다. Standalone Codex CLI, 앱 이름이나 설치된 SDK는 내장 데스크톱 접근을 입증하지 못합니다. 전달이나 권한이 알 수 없거나 비활성화되어 있으면 시나리오를 차단합니다.

## Claude Native

실제 호스트의 공식 CLI 안내와 거기서 연결하는 Desktop 안내를 읽습니다. 현재 CLI 자격 조건은 Desktop 및 비대화형 세션과 다릅니다. 앱별 권한과 도구 노출을 관찰해야 합니다. CLI computer use는 세션 동안 다른 앱을 숨기고 데스크톱 접근을 잠글 수 있습니다. 보장된 백그라운드 상호작용으로 안내하지 않습니다. 호스트 prompt와 정확한 작업 승인을 따릅니다. 앱 거부를 우회하거나 Cowork/CLI/Desktop이 모든 capability를 공유한다고 가정하지 않습니다.

## Open Computer Use

유지보수자 README와 노출된 도구 schema를 사용합니다. Accessibility, 경로 지정/백그라운드 입력, 화면 캡처와 전역 action은 OS마다 다릅니다. 선택 사항으로 유지합니다. 백그라운드 전용 기준에 선택하기 전에 최신 앱/창 식별 정보와 실제 전달을 입증합니다.

## Munim Computer Use

유지보수자 README와 실제 플랫폼/도구 schema를 사용합니다. 다른 곳에는 백그라운드 지원 경로가 있어도 일부 Windows 경로와 Linux pointer 입력은 실제 pointer를 움직일 수 있습니다. 로그인 상태의 브라우저 extension 연결은 독립적인 신뢰 경계입니다. 선택 사항으로 유지하며 일괄적인 백그라운드 또는 플랫폼 간 capability 주장을 피합니다.
