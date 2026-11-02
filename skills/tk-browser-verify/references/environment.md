<a id="headless-environment"></a>
# Headless 환경

[제공자 선택](../../tk-verification-guidance/references/provider-selection.md)에 따라 선택한 제공자를 사용합니다.
명시적 선택이 없으면 설치된 `playwright-cli`를 기본으로 사용합니다. 공식 Skill이 없어도 도움말로
실행하며, MCP와 직접 CLI/CDP를 포함한 다른 경로로 조용히 전환하지 않습니다. 필수 기능이 없으면 최종 질문의 현재 결정 경계에 부족한 기능과 선택 가능한
대안을 제시합니다. 한 번의 실행을 위해 브라우저 의존성을 설치하지 않습니다. 선택 경로를
`managed launch | direct launch | attach`로 분류하며, 선택해도 아래 검사는 면제되지 않습니다.

`managed launch`에서는 현재 호스트 설정을 확인하고 제품 상호작용 전에 유효한 headless 옵션을
요구합니다. 제공자는 지연 시작할 수 있으므로 첫 호출 전에 실행 중인 브라우저 프로세스가 없다는
사실은 실패가 아닙니다. 무해한 탐색 호출 한 번으로 부트스트랩한 뒤 확인 가능한 런타임 브라우저/
버전, 전송 방식과 소유권 정보를 기록합니다. 제공자가 관리하는 pipe나 동등한 전송 방식에는 TCP
endpoint가 필요하지 않습니다. 현대적인 `--headless`, `headless: true`와 설치된 버전에서 동등한
다른 headless 설정은 유효하며, 정확히 `--headless=new`라는 텍스트를 요구하지 않습니다.

제공자 격리는 권고이며 별도의 headless 필수 조건이 아닙니다. 새 설정에는 임시 제공자 프로필을
우선하고, 지원되면 시나리오 격리 컨텍스트를 사용합니다. 실제 headless인 제공자 관리 전용 영구
프로필도 사용자의 일반 브라우징 프로필이 아니라면 사용할 수 있습니다. 쿠키, 저장소와 캐시가
제공자 재시작 후에도 남을 수 있음을 공개합니다. `--isolated`를 시나리오 수준 격리의 증거로
취급하지 않습니다.

`direct launch`에서는 실행 명령과 런타임 상태로 유효한 headless 옵션과 실행 소유 브라우저/
프로필을 입증합니다. `attach`에서는 어떤 브라우저 호출보다 먼저 살아 있는 endpoint, 유효한
headless 모드와 외부 브라우저/프로필 소유권을 입증합니다. 고정 `--browserUrl` 제공자는
브라우저를 시작하지 않으므로 이 모든 사실은 외부 실행기의 소관입니다. 저장된 포트, 이전
브라우저 UUID, `DevToolsActivePort`, 제공자 기본값, 설정 주장이나 도구 이름은 충분한 attach
근거가 아닙니다. 연결된 프로세스가 headed이거나 다른 실행 또는 사용자 소유이거나 소유권을
알 수 없으면 페이지를 만들지 않고 `Unverifiable`을 반환합니다.

<a id="direct-launch-endpoint-ownership"></a>
## 직접 실행 endpoint의 소유권

TCP/CDP로 직접 실행할 때는 `/json/*` 조회, WebSocket 연결과 첫 CDP 호출 **전에** 다음을 확인합니다.
제공자가 소유한 pipe에는 TCP 포트 검사를 강제하지 말고 해당 전송 방식의 소유권 근거를 사용합니다.

1. 실행 소유의 고유한 프로필과 실제 시작 PID/핸들, 시작 시각, 명령을 기록합니다. 래퍼가 브라우저를
   자식으로 띄우면 그 시작과 연결된 자식 PID 및 프로필을 입증합니다. 사용자의 일반 프로필을 사용하지 않습니다.
2. 선택한 제공자가 지원하면 `--remote-debugging-port=0`으로 브라우저가 포트를 정하게 하고,
   이번 시작의 로그 또는 고유 프로필에서 새로 생성된 `DevToolsActivePort`로 실제 endpoint를 확인합니다.
   고정 포트가 필요하면 시작 전에 `lsof -nP -iTCP:<port> -sTCP:LISTEN` 또는 IPv4·IPv6를 모두
   보여 주는 동등한 호스트 도구로 확인합니다. `nc -z 127.0.0.1`만으로 빈 포트를 판정하지 않습니다.
   사전 확인은 예약이나 실행 후 소유권 증명이 아니며, 점유된 포트의 프로세스는 보존합니다.
3. 실제 endpoint의 주소·포트를 리슨하는 PID를 IPv4·IPv6 모두에서 다시 확인하고 기록한 브라우저
   PID 또는 입증된 실행 소유 자식과 대조합니다. 프로세스 시작 시각·명령·고유 프로필도 맞아야 합니다.
   container·sandbox의 실행 API와 OS 조회가 서로 다른 PID namespace를 사용하면 입증된 대응으로
   같은 namespace에 맞춘 뒤 대조합니다. 숫자 일치만 추정하거나 대응을 확인할 수 없으면 중단합니다.
   다른 실행의 리스너가 섞이거나 PID·주소·프로필을 입증할 수 없으면 `Unverifiable`로 중단합니다.
   예상 포트의 `127.0.0.1`에 임의로 붙지 말고 검증한 실제 주소와 WebSocket 경로만 사용합니다.
4. 디버깅 endpoint는 loopback이어야 합니다. 선택한 버전이 지원하면
   `--remote-debugging-address=127.0.0.1`을 명시할 수 있지만, 이 옵션이나 정상 종료 코드·
   `DevTools listening` 한 줄만으로 주소·소유권을 입증하지 않습니다. `Address already in use`,
   주소 계열 전환이나 실제 포트 변경이 보이면 위 대조를 마치기 전에는 조회·탐색하지 않습니다.
   프로세스나 endpoint가 교체되면 소유권을 다시 확인합니다.

Chromium 버전에 따라 같은 포트의 IPv6로 옮기거나 다른 빈 포트를 선택할 수 있으므로, 특정 fallback을
가정하지 않습니다. 실패 시 이번 실행 소유 자원만 정리하고 다른 브라우저나 서버를 종료하지 않습니다.

<a id="provider-readiness"></a>
## 제공자 준비 상태

의존성을 설치하거나 조용히 전환하지 않고 선택한 제공자의 현재 공식 사용 안내를 따릅니다.
새 adapter나 직접 작성한 검증기에서는 넓은 viewport/테마 캡처 행렬에 앞서 문법, DOM 관찰 한 번,
안전한 네이티브 컨트롤에서 필요한 신뢰 포인터/키보드 동작과 소유 자원 정리를 확인합니다.
이미 검증된 경로가 있으면 재사용하며 새 framework는 필요하지 않습니다. 광범위한 캡처 재생 전에
검증기 결함을 격리하고 수정합니다. 미검증 입력 경로에서 제품 결함을 추론하거나 전체 행렬을
반복하면서 이벤트 옵션을 추측하지 않습니다. [신뢰 입력](behavior.md#exact-target-and-trusted-input)을 참조합니다.

<a id="missing-provider-setup"></a>
## 제공자 설정 누락

호환 경로가 없으면 제공자를 설치하거나 호스트 설정을 편집하지 않습니다. 브라우저 호출도 하지
않습니다. 소비자 `tk-browser-verify`, 정확히 차단된 기준(`Blocked` 유지), 감지한 호스트/클라이언트와
제공자 상태, 누락 기능, 필수 유효 headless 모드, 권고 제공자 격리, 완료 신호와 정확한 재개 동작을
담아 `tk-wizard`를 호출합니다.

기본 인계 대상은 공식 Microsoft Playwright CLI입니다. 버전·명령 도움말, 브라우저 바이너리와
선택적 공식 Skill의 발견 상태를 구별하여 전달합니다. CLI가 이미 있으면 재설치하지 않으며 Skill
부재는 차단 사유가 아닙니다. CLI/브라우저가 없으면 설치 명령은 `tk-wizard`에서 안내하고 실행하지
않습니다. 승인 없는 `npx` 다운로드나 라이브러리 내부 진입점 실행으로 누락을 숨기지 않습니다.
공식 설치 명령과 호스트별 Skill 대상의 안내는 wizard 인계가 소유합니다. 소비자에서 해당 스킬의
파일을 직접 읽거나 설치하지 않고, 사용할 수 없으면 기존 `tk-setup-skills` 안내로 부족한 담당자를 보고합니다.

현재 설치된 CLI의 [연동 지식](../../tk-verification-guidance/references/provider-knowledge.md#playwright-cli)을
적용하여 실행 소유 세션·설정·출력 경로와 실제 headless 모드를 검증합니다. Chrome DevTools MCP의
신규 등록을 기본값으로 만들지 않고, 기존 등록과 사용자 선택도 자동 수정하지 않습니다.

기본값에는 `--browserUrl`, `--wsEndpoint`, remote-debugging 포트나 포트 `9222`를 포함하지
않습니다. 관리형/직접 실행 실패가 관찰되었거나 이에 준하는 sandbox, VM, container 또는 호스트
경계 근거가 있을 때만 attach 경로를 선택할 수 있습니다. 해당 근거를 wizard에 전달하고,
노출되는 디버깅과 외부 프로필의 영향을 설명하며, 설정을 제시하기 전에 사용자가 attach를
선택하도록 요구합니다.

<a id="authentication"></a>
<a id="worktree-local-authentication-reuse-and-renewal"></a>
## 인증

인증을 수립·재사용·갱신하거나 보호 입력을 준비하기 전에 [헤드리스 인증](headless-auth.md)을 읽습니다. 인증 우선순위, 지원 경로 확인, 비밀 입력의 보존·갱신·소비와 실패 조건은 그 문서가 소유합니다. 재사용과 갱신의 상세 기준은 [인증 입력 재사용과 갱신](headless-auth.md#worktree-local-authentication-reuse-and-renewal)에 있습니다. 이 참조는 인증 실행이나 설치 권한을 부여하지 않습니다.

<a id="run-owned-development-server"></a>
## 실행 소유 개발 서버

저장소 설정과 승인된 API 대상에 맞는 사용 가능한 포트를 선택하며, 사용자나 다른 실행이 이미
사용하는 포트를 보존합니다. 저장소에서 입증된 서버 명령을 시작하고 그 시작에서 반환한 PID,
cwd, command, host/port와 제한된 로그 경로를 기록합니다. 가능하면 호스트의 소유 프로세스 핸들을
사용합니다. 제한된 시간 안에 HTTP 준비 상태와 현재 프로젝트 빌드 식별 정보를 독립적으로 확인합니다.
worktree mutex, Git 공통 디렉터리 잠금, supervisor나 서버 lease는 없습니다.

서버가 포트 충돌 시 자동으로 다른 포트로 이동할 수 있으면, 지원되는 strict-port 옵션을 사용하거나
이번 시작 로그에서 실제 바인딩 URL을 읽습니다. HTTP 준비 상태 조회와 브라우저 탐색 전에 실제 포트의
IPv4·IPv6 리스너 PID가 시작한 서버 또는 입증된 실행 소유 자식인지, 그 프로세스의 해석된 cwd가
승인한 정확한 서버 cwd인지, 그 cwd의 Git/worktree 식별이 대상과 일치하는지 확인합니다. monorepo의
승인된 하위 앱 cwd도 허용하며 worktree 루트와 문자열이 같을 필요는 없습니다. 다르면 원래 포트로
접속하지 않고 `Unverifiable`로 중단합니다.
그 뒤 기존의 프로젝트·bundle 식별 검사로 제공 버전까지 입증합니다. 실제 URL·포트·PID·cwd와 버전
근거를 함께 보존하며, strict-port 옵션도 이 실행 후 확인을 면제하지 않습니다.

각 캡처 단계 후에는 기록된 PID/핸들과 독립적으로 검증한 프로세스 식별 정보를 사용하여 해당
시작이 만든 프로세스만 중지합니다. 자식을 만들면 시작 중에 소유 자식 PID/핸들을 기록하고 검증된
자식만 중지합니다. 종료하려고 포트나 프로세스 이름으로 검색하지 않습니다. 이미 종료된 소유
프로세스에는 신호가 필요하지 않습니다. 소유 프로세스의 종료를 확인하고 선택한 포트의 현재
점유자를 죽이지 않고 포트를 확인합니다. 소유권이 불확실하거나 종료에 실패하면 성공적 정리나
광범위한 프로세스 종료를 보고하지 말고 관찰된 정리 잔여물을 보고합니다. 사용자 소유 또는 다른
실행의 서버를 중지하지 않습니다.

<a id="server-and-serving-source"></a>
## 서버와 제공 소스

`standalone` 실행에서는 저장소 스크립트, 문서와 도구가 명확하게 식별하는 정본 안전 명령 하나를
추가 질문 없이 사용합니다. 가능한 `dev-server` 명령이 여러 개인 `standalone` 실행에서는
후보와 선택을 사용자에게 제시하고 하나를 시작하기 전에 확인받습니다. `parent`가 정확한 명령을
제공한 `nested` 실행에서는 같은 결정을 다시 질문하지 않습니다. `react-scripts`/CRA 서버에는
`BROWSER=NONE` 또는 저장소에 문서화된 동등한 `auto-open` 억제를 포함합니다.
호스트가 지원하는 백그라운드 프로세스 API로 `long-running server`를 시작하고, 시작에서 반환한
소유 PID/핸들, `cwd`, 명령 근거, `port`와 제한된 `log` 경로를 기록합니다.
`bounded timeout` 안에 구체적인 `HTTP`/`port` `readiness signal`을 polling하고,
프로세스 종료를 기다리지 말고 `readiness` 후 계속합니다.

서버를 선택하거나 시작하기 전에 관련 package script와 환경 파일에서 의도한 hostname, port와
API 대상을 확인하되 비밀 값은 노출하지 않습니다. 기본 포트로 벗어나지 말고 저장소 관례를 따릅니다.
준비 상태에는 살아 있는 응답과 예상 `<title>`, 페이지 marker 또는 현재 bundle fingerprint 같은
프로젝트 고유 식별 정보가 모두 필요합니다. 열린 포트만으로는 다른 프로젝트일 수 있습니다.

선택한 스크립트가 `A && B`를 사용하고 `A`가 장기 실행 서버이면 `B`는 실행될 수 없습니다.
저장소 근거가 `B`를 필수 자산/빌드 단계로 식별하고 출력 부재가 관찰된 컴파일 실패를 일으키면,
`B`를 실행 소유 선행 단계로 한 번 실행하고 기록합니다. 소스를 편집하거나 이를 대체 서버
워크플로로 일반화하지 않습니다.

기존 서버는 cwd가 worktree와 일치하고 자산/watch 파이프라인이 최신이며, bundle/응답이나
변경된 렌더링으로 제공 버전이 입증될 때만 재사용합니다. cwd만으로는 충분하지 않습니다.
다른 worktree와 사용자 프로세스를 보존하며, 소유권이나 최신성이 불확실하면 별도 포트를 사용합니다.

브라우저/버전, 대상, 관련된 경우 viewport/DPR, 작업 트리, 서버 프로세스/cwd, 자산 파이프라인과
제공 버전 입증을 간결한 사실로 기록합니다.

## 출처와 확인 범위

2026-11-02에 [Chromium `d7abebf49569e8b6d1cd24fba645b1dec8fd6bf6`](https://github.com/chromium/chromium/blob/d7abebf49569e8b6d1cd24fba645b1dec8fd6bf6/chrome/browser/devtools/remote_debugging_server.cc)의
loopback socket factory·port fallback·포트 0 처리와 같은 revision의 `remote_debugging_server_unittest.cc`를
읽었습니다. **keep:** 제공자의 전송 방식과 실제 endpoint를 유지합니다. **adapt:** 직접 실행의
실행 소유 PID/프로필 대조를 연결 전 관문으로 구체화합니다. **omit:** 고정 포트·주소 옵션만으로
소유권을 보장하는 가정과 새 실행 관리 체계를 도입하지 않습니다. Chromium 테스트 실행과 실제
브라우저의 포트 충돌 재현은 이 문서 확인으로 입증되지 않습니다.
