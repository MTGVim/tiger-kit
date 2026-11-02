<a id="consumer-setup-handoffs"></a>
# 소비자 설정 인계

다른 스킬이 사람만 수행할 수 있는 호스트 설정, 인증, 권한이나 재시작 단계를 위임할 때만 읽습니다.
소비자는 대상, 작업, 변경 권한과 판정을 유지합니다. 현재 사용자의 한 가지 행동을 안내하고 완료 신호를 관찰한 뒤 정확한 재개 행동을 반환합니다.

다음 항목을 포함한 범위가 제한된 인계를 요구합니다.

- 소비자와 정확한 대기 기준입니다.
- 감지한 호스트/클라이언트와 현재 기능 상태입니다.
- 누락되었거나 호환되지 않는 기능입니다.
- 필수 속성과 권장 속성입니다.
- 검증할 수 있는 완료 신호입니다.
- 정확한 재개 행동입니다.
- 해당하는 경우 대체 경로 자격과 이를 허용하는 근거입니다.

최신 공식 문서보다 설치된/로컬 호스트 근거를 먼저 사용합니다.
정확한 설정 파일, 범위, 명령 형태, UI literal과 재시작 지시를 도출하며 이를 만들지 않습니다.
무관한 설정을 보존하고 사용자가 제어하는 최소 변경을 보여 줍니다. 호스트 설정을 조용히 편집하지 않습니다.

<a id="browser-provider-setup"></a>
## 브라우저 제공자 설정

일반 브라우저의 새 설정은 Microsoft Playwright CLI를 기본으로 안내합니다. 설치/업데이트는
사용자가 선택한 버전·대상·범위와 별도 설치 승인 경계에 속하며, 이 인계만으로 실행하지 않습니다.
Chrome DevTools MCP 등록·MCP 서버 추가·자동 attach를 기본 해결책으로 제시하지 않습니다.

1. 이미 설치된 `playwright-cli`의 경로·`--version`·`--help`, 필요한 브라우저와 현재 호스트에서
   발견되는 공식 `playwright-cli` Skill을 확인합니다. CLI가 있으면 재설치하지 않습니다.
2. CLI가 없으면 [공식 설치 안내](https://github.com/microsoft/playwright-cli)의 패키지·Node 요구
   조건을 현재 시점에 확인합니다. 2026-11-03 확인 명령은 `npm install -g @playwright/cli@0.1.23`이며
   Node 18+를 요구합니다. 이것은 당시 배포 버전의 고정 예시이며 영구 최소 버전이 아닙니다.
   공식 문서의 `@latest` 예시를 자동 실행 정책으로 옮기지 말고, 실제 설치할 버전을 확인해 안내합니다.
3. 공식 Skill은 선택 사항입니다. 없어도 `playwright-cli --help`와 명령별 도움말로 진행합니다.
   설치를 선택하면 실제 `playwright-cli install --help`를 확인한 뒤
   `playwright-cli install --skills`(기본 `claude`, `.claude/skills/playwright-cli`) 또는
   `playwright-cli install --skills=agents`(`.agents/skills/playwright-cli`)를 안내합니다.
   Claude Code·GitHub Copilot은 공식 안내 대상이며, Codex 등은 현재 호스트의 Skill 탐색 경로가
   해당 대상과 일치하는지 확인합니다. Work의 원격 Skill 저장소와 호환된다고 추정하지 않습니다.
   기존 공식 Skill을 덮어쓰거나 다시 설치하지 않고, TigerKit 카탈로그에 복제/필수 의존성으로 넣지 않습니다.
4. CLI 설치 완료와 브라우저 준비 완료를 구분합니다. `--version`·도움말 성공만으로 headless 실행
   성공을 주장하지 않습니다. 브라우저가 없으면 설치된 버전의 공식 브라우저 설치 도움말에서 정확한
   명령과 시스템 의존성을 확인하여 별도 안내합니다. 자동 다운로드나 권한 확대를 하지 않습니다.
5. 완료 신호는 설치된 CLI 식별/버전·도움말과, 소비자가 실행 소유 세션·명시적 headless 설정으로
   무해한 `open`을 수행하여 관찰한 실행 모드·소유권·종료입니다. 실제 검증은 소비자가 재개합니다.
   현재 호스트의 [제공자 선택](../../tk-verification-guidance/references/provider-selection.md)과
   [연동 지식](../../tk-verification-guidance/references/provider-knowledge.md#playwright-cli)을 적용합니다.

일반 새 설정에는 사용자 프로필, `--persistent`, `--profile`, CDP endpoint나 extension 연결을
추가하지 않습니다. 기존 MCP 항목과 무관한 설정을 보존합니다. 명시적으로 선택된 다른 제공자는
해당 버전의 공식 안내와 기존 소유권·headless 경계를 따릅니다. 관리형/직접 실행 실패나 동등한
sandbox/VM/container/호스트 근거가 있을 때만 attach를 대안으로 제시하고, 사용자가 선택하기 전에
외부 실행기의 headless 모드·endpoint 노출·프로필 데이터 책임을 설명합니다.

클라이언트를 재시작해야 하면 `Status: Pending`, 관찰한 완료 신호와 원래 기준으로
`tk-browser-verify`를 재개하는 정확한 지시를 반환합니다. 브라우저 검증을 통과했다고 주장하지 않습니다.

<a id="github-image-upload-setup"></a>
## GitHub 이미지 업로드 설정

에이전트 실행이 부적절한 경우의 호스트 수준 `gh` 설치/복구, 대화형 `gh auth login`, 계정/저장소 권한 변경이나
명시적으로 선택한 브라우저 경로의 인증/권한/재시작 단계처럼 사람의 행동만 받습니다.
검토된 확장 선택/설치, 이미지 준비/업로드, PR 변경이나 렌더링 검증을 대신 맡지 않습니다.

클라이언트 재시작이 필요하지 않은 완료 신호를 받으면 원래 저장소, PR/댓글 대상, 이미지 집합과 선택한 경로를 그대로 유지하여 `tk-pr-media`에 제어를 돌려줍니다.
재시작이 필요하면 이미지를 업로드했다고 주장하지 않고 `Status: Pending`과 정확한 재개 행동을 반환합니다.
