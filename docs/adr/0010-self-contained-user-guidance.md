# ADR 0010: 사용자 레벨 한국어 지침을 TigerKit에 포함

- 상태: 채택
- 작성: 2026-11-21

## 배경

이전에는 개인 `tigeryoo-ai-setup` 저장소가 `fluent-korean` 전체 본문을 Claude Code의 `CLAUDE.md`, Codex의 `AGENTS.md`, Hermes의 `SOUL.md`에 설치했습니다. 긴 지침은 자연스러운 채팅 말투를 충분히 개선하지 못했고, 개인 저장소를 삭제하면 재설치 경로도 사라집니다.

TigerKit의 `tk-writing/references/clear-writing.md`는 스킬을 실행할 때 조건에 따라 읽는 문서입니다. 에이전트의 일반 채팅에서는 파일이 자동으로 로드되지 않으므로 짧은 사용자 레벨 지침을 따로 제공해야 합니다.

## 결정

1. 공개해도 되는 공통 문체·작업 보고·도구 호출·Git 지침을 `tk-setup-skills/references/user-guidance.md`에 포함합니다. 이 파일이 설치본의 정본이며, 개인 저장소나 네트워크에 의존하지 않습니다.
2. `tk-setup-skills/scripts/install_user_guidance.py`가 이를 `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`와 이미 존재하는 `~/.hermes/SOUL.md`에 설치합니다. 읽기 전용 `--check`가 기본이고 명시적인 사용자 설정 변경 승인 후에만 `--apply`를 실행합니다.
3. 최초에는 `MTGVIM_SHARED_AGENT_BASE` 마커를 재사용했습니다. 2026-11-22부터 관리 마커를 `TIGERKIT_USER_GUIDANCE_BEGIN/END`로 통일합니다. 기존 `MTGVIM_SHARED_AGENT_BASE_START/END`와 `MTGVIM_FLUENT_KOREAN_START/END`는 설치 시 감지해 공통 지침 교체와 함께 정리합니다. 이전 본문과 무관한 사용자 문구는 유지하며 백업합니다. 손상·중복·중첩된 마커와 심볼릭 링크는 수정하지 않습니다.
4. `tk-rewrite`는 이미 작성된 글의 어조와 뉘앙스 변경을 담당합니다. `tk-writing`의 명확한 글쓰기 기준은 스킬을 통한 산출물에 적용합니다. 사용자 지침 전체를 매번 읽는 새로운 에이전트·훅·라우터를 만들지 않습니다.
5. `tigeryoo-ai-setup` 저장소를 유지하거나 삭제할지는 사용자에게 남깁니다. TigerKit은 해당 저장소에 대한 읽기 권한, 파일 경로, API 접근을 요구하지 않습니다.

## 제외

- `SOUL.md`의 생성이나 기존 역할·정체성 지침 교체
- 스킬 설치 승인만으로 사용자 환경 수정
- `tk-writing`의 전체 기준을 사용자 지침에 복제
- 모델 A/B 효과에 대한 검증 없는 주장, 강제 AI 문체 탐지기나 점수 체계

## 검증

격리된 홈 디렉터리에서 `--check`와 `--apply`의 차이, 재실행 멱등성, 백업, 사용자 영역 보존, 구 마커 제거, 손상된 마커·심볼릭 링크 거부와 Hermes 파일 부재를 확인합니다. 런타임에서 실제 모델의 자연스러움 향상 여부는 별도로 평가합니다.

## 2026-11-22 후속 결정: 공통 관리 마커 형식

- 사용자 지침: `<!-- TIGERKIT_USER_GUIDANCE_BEGIN -->` / `<!-- TIGERKIT_USER_GUIDANCE_END -->`.
- 위임 규칙: `<!-- TIGERKIT_ROUTE_MODE_BEGIN -->` / `<!-- TIGERKIT_ROUTE_MODE_END -->`.
- 마커 이름은 대문자 `SCREAMING_SNAKE_CASE`와 `TIGERKIT_` 접두어로 통일합니다. 사용자 지침 및 위임 규칙은 각 담당 스킬이 별도로 관리합니다.
- `tk-setup-skills`는 일반 점검에서 과거 `route-mode:begin/end`를 발견하면 이전을 제안합니다. `--migrate-route-mode` 인자를 명시하지 않으면 위임 규칙을 변경하지 않습니다. 승인된 `--apply --migrate-route-mode`는 기존 위임 규칙의 본문을 그대로 두고 마커 문자열만 교체합니다.
- `tk-route-mode`는 새/구 마커를 조회·갱신·제거할 수 있고, `rule migrate`로 본문 내용이 변하지 않는 별도 마커 이전을 지원합니다. 기존 백업과 적용 기록을 유지합니다.
- 두 형식이 동시에 나타나거나 마커가 빠지거나 서로 겹치면 임의 복구하지 않고 중단합니다. 기존 설정의 사용자 소유 영역이나 승인 범위를 확대하지 않습니다.

## 2026-11-22 후속 결정: 공통 지침 축약과 호스트 권한 보존

- 사용자 공통 지침은 짧은 일반 채팅·판단·실행·도구 원칙을 소유하고, 자연스러운 한국어와 AI Slop 세부 기준은 설치된 `tk-writing`의 `authoring-gate.md` 및 `clear-writing.md`를 조건부로 참조합니다. 일반 채팅에서 불필요한 참조 파일 로딩을 강제하지 않습니다.
- 사용자 대신 실제 외부에 발행하는 산문 저작물의 AI 작성 고지는 `tk-writing/references/authoring-gate.md`에서 담당합니다. 기존 채널별 고지·HTML 파일 예외와 기계 판독/도구 인자 보호를 유지합니다.
- 정상적인 호스트 위임·승인된 구현에 필요한 branch/worktree 생성을 전역 지침 하나로 막지 않습니다. 호스트의 실제 도구 스키마·승인 절차와 작업별 권한 경계가 우선합니다. 이 결정만으로 새로운 원격 발행·파괴적 변경 권한은 생기지 않습니다.

## 2026-11-24 후속 결정: 판단·실행 원칙의 정밀화

- 일반 세션에서 목표 달성 여부와 확인된 실패를 우선 판단합니다. 이미 확인한 실패를 미확인으로 표현하거나, 작업 내역만 나열하고 후속 조치를 사용자가 설계하도록 떠넘기지 않습니다.
- 승인된 실제 업무는 담당 작업에서 계속 수행하지만, 사용자가 진단·검토·제안만 요청했거나 명시적 `tk-sowhat` 교정 중이면 실행하지 않습니다. 판단 교정과 사용자 결정은 [ADR 0013](0013-judgment-correction-boundaries.md)이 담당합니다.
- 출력의 세부 구성과 선택적 후속 작업 제안은 `tk-writing`에서만 소유합니다. 사용자 공통 지침의 짧은 판단 원칙을 유지하며 매번 참조 로드나 새 자동 스킬 호출을 강제하지 않습니다.
