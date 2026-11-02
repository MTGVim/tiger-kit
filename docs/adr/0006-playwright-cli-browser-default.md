# ADR 0006: 일반 브라우저 검증의 기본 제공자를 Playwright CLI로 전환

- 상태: Accepted
- 날짜: 2026-11-03

## 맥락

일반 브라우저 작업의 권고와 초기 설정 예시가 Chrome DevTools MCP를 유도했고, 일반 입력과
네트워크 검증에도 직접 CDP 명령이 포함되어 있었습니다. Microsoft 공식 CLI는 Skill 없이도
도움말로 사용할 수 있고 같은 이름의 세션을 재사용합니다. 제공자의 사용법을 TigerKit에 복제할
필요 없이 기존 검증 기준과 안전 경계를 유지할 수 있습니다.

## 결정

- 명시적 세션/저장 선택이 없을 때 `playwright-cli`를 기본으로 사용합니다. CLI 누락은 설정
  인계이며 MCP·직접 CDP로 자동 전환하지 않습니다. 네이티브 앱 선택 정책은 유지합니다.
- 공식 패키지는 `@playwright/cli`이며 공식 `playwright-cli` Skill은 선택 사항입니다. 설치된
  버전의 도움말을 먼저 확인하고 설치·업데이트·인증은 기존 승인 경계를 유지합니다.
- 기존 `playwright` ID는 MCP/저장소 어댑터를 계속 뜻합니다. Chrome DevTools MCP는 기본
  권고·설치 예시에서 제외하되 기존 명시적 선택을 삭제하거나 설정을 자동 이관하지 않습니다.
- 일반 관찰·입력·캡처는 CLI 또는 같은 세션의 공식 `run-code`로 수행합니다. 독립 화면 근거,
  postcondition, 실패 근거, 비밀 보호, 쓰기 범위와 실행 소유 자원 정리를 완화하지 않습니다.
- 정확한 프레임 시각 계약은 일반 동영상 파일·출력 fps와 구별합니다. CLI 기본 녹화, 같은 페이지의
  `run-code` CDP Session, 이미 승인된 동일 페이지의 라이브러리 CDP Session 순으로 실제 기능을
  확인합니다. 충족하지 못하면 선택적 미디어만 제한하고 별도 브라우저나 시나리오를 암묵적으로 실행하지 않습니다.
- Playwright Trace를 Chrome DevTools Performance Trace로 간주하지 않습니다. 성능 분석과 재현된
  특수 drag에는 명시적으로 선택한 최소 CDP 경로를 유지할 수 있습니다.
- PR 미디어의 `gh-attach` 기본 경로를 유지합니다. 사용자가 고른 브라우저 대체 경로에는 CLI를
  우선 제안하며 인증·정확한 대상·작성창·첨부 완료·바이트·렌더링/재생 검증을 유지합니다.
- `tk-writing`의 `chrome_capture.mjs`, `capture_page.mjs`, `svg_to_png.mjs`는 네트워크가
  차단된 실행 소유 pipe로 로컬 산출물을 렌더링하는 도우미입니다. 일반 앱 검증 제공자가 아니므로
  이번 전환에서 유지합니다. 이 도우미를 CLI 누락 우회나 제품 검증 대체에 사용하지 않습니다.

## 결과와 제한

추가 실행 framework나 새 제공자 추상화는 만들지 않습니다. 공식 Skill을 TigerKit 카탈로그에
복제하지 않으며 위임만 하는 `tk-video`, `tk-tts`, `tk-research`, `tk-app-verify`, `tk-qa-sheet`는
수정하지 않습니다. `tk-explain`의 로컬 콘텐츠 리뷰용 캡처도 기존 소유 경계를 유지합니다.

공식 계약의 고정 revision과 `keep | adapt | omit` 근거는 `tk-verification-guidance`의
`references/provider-knowledge.md`에 둡니다. 현재 환경에는 CLI 실행 파일과 브라우저가 없으므로
실제 페이지·네트워크·SortableJS/HTML drag·픽셀·정밀 영상·성능·인증된 PR 업로드는 `Unverified`입니다.
일반 전환의 지침·registry·설치 경계 변경과 런타임 완료 기준 달성을 구별합니다. 지원 여부를
문서 존재만으로 통과 처리하지 않습니다. 준비된 환경에서 동일 시나리오를 실행하고 기능 성공·명령 수·
시간·재시도·개입·추가 의존성·잔여 자원·근거 품질을 비교합니다. 토큰은 측정할 수 있을 때만 기록합니다.

## 복구

기존 명시적 제공자 설정은 계속 유효합니다. 기본 선택을 되돌려야 하면 이 변경의 registry·선택·
설정 안내를 함께 되돌리며, 사용자 설치본이나 프로필을 자동 삭제/교체하지 않습니다.
