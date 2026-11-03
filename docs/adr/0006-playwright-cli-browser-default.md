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
- 정밀 캡처는 같은 CLI 세션의 공식 `run-code`와 `page.context().newCDPSession(page)`로 수행합니다.
  `capture_motion.py`는 기존 페이지에서 원래 프레임 시각·ack·정리와 크기·시간이 제한된 호스트 전달을 담당하며
  브라우저를 시작하거나 별도 endpoint에 연결하지 않습니다. 일반 녹화의 25fps 컨테이너/디코더
  PTS는 원래 프레임 시각 계약을 충족하지 않습니다. `Page.startScreencast` 이벤트 API 자체는
  이 기능 차이 때문에 유지하지만 별도 Chrome DevTools MCP·직접 socket/pipe 수집기를 요구하지 않습니다.
- SortableJS와 네이티브 HTML Drag & Drop은 실제 입력과 POST 결과가 통과한 CLI `drag`,
  같은 세션의 `dragTo`·mouse 경로로 대체합니다. 일반 drag의 직접 CDP 명령 지침을 제거합니다.
  실패한 새로운 사례는 최소 재현과 부족한 기능을 확인하기 전까지 `Unverifiable`이며,
  자동으로 CDP 필수나 별도 브라우저 실행으로 바꾸지 않습니다.
- Playwright Trace와 Chrome DevTools Performance Trace를 구별합니다. 후자는 같은 페이지의
  공개 `browser.startTracing`/`stopTracing` API로 CPU 표본·레이아웃·페인트·User Timing을
  실제 확보했습니다. 이 분석을 위해 별도 MCP나 직접 `Profiler` 명령을 요구하지 않습니다.
- 기존 `chrome-devtools-mcp`·`browser-cdp` ID는 설정 호환성을 위해 `reference`로 보존합니다.
  신규 설치 권고에서 제외하되 명시적 사용자 선택과 설정을 자동 변경하지 않습니다.
- PR 미디어의 `gh-attach` 기본 경로를 유지합니다. 사용자가 고른 브라우저 대체 경로에는 CLI를
  우선 제안하며 인증·정확한 대상·작성창·첨부 완료·바이트·렌더링/재생 검증을 유지합니다.
- `tk-writing`의 로컬 렌더러는 **Keep**입니다. 순수 Playwright 대체 후보를 구현·실행했지만,
  같은 Chrome·입력에서 기본 글꼴이 `Apple SD Gothic Neo`에서 `Times`로 바뀌어 HTML 630픽셀,
  SVG 1682픽셀이 달랐습니다. 100000px 실패 로그는 후속 CDP Session 대체 경로의 실행이므로,
  이를 공개 screenshot API 자체의 한계로 일반화하지 않습니다. Keep 판정은 별도로 확인한
  기본 글꼴·픽셀 불일치에 근거합니다.
  명시적 글꼴의 영역 캡처 성공만으로 기본 글꼴·전체 크기 계약을 완화하지 않습니다.
  후보는 채택하지 않고 기존 pipe를 유지합니다. 이 판정은 해당 버전·계약의 결과이며 CDP가
  보편적으로 필수라는 뜻이 아닙니다. 실행 소유 deny proxy로 iframe·worker·WebSocket/TLS까지
  차단하고 기존 출력·DPR·투명도·덮어쓰기 방지를 보존합니다. 일반 앱 검증이나 CLI 누락 우회에
  이 도우미를 사용하지 않습니다.

## 결과와 제한

추가 실행 framework나 새 제공자 추상화는 만들지 않습니다. 공식 Skill을 TigerKit 카탈로그에
복제하지 않으며 위임만 하는 `tk-video`, `tk-tts`, `tk-research`, `tk-app-verify`, `tk-qa-sheet`는
수정하지 않습니다. `tk-explain`의 로컬 콘텐츠 리뷰용 캡처도 기존 소유 경계를 유지합니다.

공식 계약의 고정 revision과 `keep | adapt | omit` 근거는 `tk-verification-guidance`의
`references/provider-knowledge.md`에 둡니다. PR #497 당시의 CLI/브라우저 부재는 역사적 실행
제약이었으며 대체 불가능성의 증명이 아니었습니다. 후속 실행은 공식 CLI `0.1.23`, 실제 의존
Playwright `1.65.0-alpha-2026-10-30`, Chrome `156.0.8078.74`에서 공식 Skill 없이 수행했습니다.

초기 정밀 캡처에서는 원래 단조 시계 이벤트 193개와 ack 193개, 순서 역행 없음, 마지막 유휴
유지 약 1195ms를 확인했습니다. 움직임 구간의 전달 속도 약 60fps와 출력 인코딩 30fps를
구별하고, 4496ms manifest를 기존 `tk-video` 조립기로 실제 4500ms MP4로 인코딩·검사했습니다.
최종 helper 소스도 별도로 정상·시나리오 예외·기한·예산·SIGINT와 소유 세션 폐기를 실행했습니다.
프레임 시각·ack·원본을 보존하되 프로토콜에 compositor sequence가 없어 원천 브라우저의
모든 프레임 전달/누락까지 보장하지는 않습니다. 이 한계는 직접 CDP 수집기에도 같습니다.

인증된 GitHub 첨부는 승인된 브라우저 인증과 정확한 업로드 대상이 없어 `Unverified`입니다.
로컬 file chooser·파일 선택의 성공을 GitHub 업로드 성공으로 확대하지 않습니다. 재개에는
정확한 PR·본문 또는 기존 댓글과 그 환경에 승인된 브라우저 인증이 필요합니다. 새 계정 연결,
사용자 프로필 접근이나 시험 댓글 생성은 하지 않습니다. `gh-attach` 기본값은 바꾸지 않습니다.
상시 suite·CI·새 제공자 framework를 도입하지 않으며 일회성 실험과 원시 근거는 ignored
`.tigerkit/` 경로에 보존합니다. 시간·명령 수·토큰 비용은 실제 측정한 항목만 보고합니다.

## 복구

기존 명시적 제공자 설정은 계속 유효합니다. 기본 선택을 되돌려야 하면 이 변경의 registry·선택·
설정 안내를 함께 되돌리며, 사용자 설치본이나 프로필을 자동 삭제/교체하지 않습니다.
