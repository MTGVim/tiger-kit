# ADR 0010: 사용자 레벨 한국어 지침을 TigerKit에 포함

- 상태: 채택
- 작성: 2026-11-21

## 배경

이전에는 개인 `tigeryoo-ai-setup` 저장소가 `fluent-korean` 전체 본문을 Claude Code의 `CLAUDE.md`, Codex의 `AGENTS.md`, Hermes의 `SOUL.md`에 설치했습니다. 긴 지침은 자연스러운 채팅 말투를 충분히 개선하지 못했고, 개인 저장소를 삭제하면 재설치 경로도 사라집니다.

TigerKit의 `tk-writing/references/clear-writing.md`는 스킬을 실행할 때 조건에 따라 읽는 문서입니다. 에이전트의 일반 채팅에서는 파일이 자동으로 로드되지 않으므로 짧은 사용자 레벨 지침을 따로 제공해야 합니다.

## 결정

1. 공개해도 되는 공통 문체·작업 보고·도구 호출·Git 지침을 `tk-setup-skills/references/user-guidance.md`에 포함합니다. 이 파일이 설치본의 정본이며, 개인 저장소나 네트워크에 의존하지 않습니다.
2. `tk-setup-skills/scripts/install_user_guidance.py`가 이를 `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`와 이미 존재하는 `~/.hermes/SOUL.md`에 설치합니다. 읽기 전용 `--check`가 기본이고 명시적인 사용자 설정 변경 승인 후에만 `--apply`를 실행합니다.
3. 종전 `MTGVIM_SHARED_AGENT_BASE` 마커를 재사용하고 오래된 `MTGVIM_FLUENT_KOREAN` 마커 구간만 제거합니다. 다른 사용자 작성 내용은 유지하며 원본 파일을 백업합니다. 손상된 마커, 심볼릭 링크는 수정하지 않습니다.
4. `tk-rewrite`는 이미 작성된 글의 어조와 뉘앙스 변경을 담당합니다. `tk-writing`의 명확한 글쓰기 기준은 스킬을 통한 산출물에 적용합니다. 사용자 지침 전체를 매번 읽는 새로운 에이전트·훅·라우터를 만들지 않습니다.
5. `tigeryoo-ai-setup` 저장소를 유지하거나 삭제할지는 사용자에게 남깁니다. TigerKit은 해당 저장소에 대한 읽기 권한, 파일 경로, API 접근을 요구하지 않습니다.

## 제외

- `SOUL.md`의 생성이나 기존 역할·정체성 지침 교체
- 스킬 설치 승인만으로 사용자 환경 수정
- `tk-writing`의 전체 기준을 사용자 지침에 복제
- 모델 A/B 효과에 대한 검증 없는 주장, 강제 AI 문체 탐지기나 점수 체계

## 검증

격리된 홈 디렉터리에서 `--check`와 `--apply`의 차이, 재실행 멱등성, 백업, 사용자 영역 보존, 구 마커 제거, 손상된 마커·심볼릭 링크 거부와 Hermes 파일 부재를 확인합니다. 런타임에서 실제 모델의 자연스러움 향상 여부는 별도로 평가합니다.
