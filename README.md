# TigerKit

`Claude Code`, `Codex`, `Hermes Agent`에서 골라 쓰는 작고 조합 가능한 에이전트 스킬 모음입니다.

## 설치

```bash
npx skills add MTGVim/tiger-kit --global --agent claude-code codex hermes-agent --skill '*'
npx skills update --global --yes
```

선택 설치는 `tk-setup-skills`로 필요한 업무 스킬과 공통 의존성을 함께 준비합니다. 설치기는 의존성을 자동 해결하지 않습니다.
`Claude Code`·`Hermes`에서는 `/tk-setup-skills`, `Codex`에서는 `$tk-setup-skills`로 호출합니다. 설치 실행은 대상·범위를 확인하고 승인한 뒤 진행합니다.
설치 도우미의 소스·설치본 검사에는 `Python 3.9+`와 `PyYAML`이 필요합니다. 빈 대상에 동봉 카탈로그로 계획만 만들 때는 표준 라이브러리만 사용합니다. 파서가 없으면 검사를 중단하며 자동 설치하지 않습니다.

## 스킬 구성

`user`는 직접 호출하며, `hybrid`는 작업에 맞게 자동 선택할 수도 있습니다. 상세한 동작과 권한은 각 스킬 문서에 있습니다.

### 개발·기획

| 스킬 | 호출 | 소유 범위 |
| --- | --- | --- |
| [tk-prep](skills/tk-prep/SKILL.md) | `user` | 작업을 준비하고 승인된 로컬 구현·검증을 진행합니다. |
| [tk-roadmap](skills/tk-roadmap/SKILL.md) | `user` | 목표와 제약을 정리해 마일스톤을 만듭니다. |
| [tk-audit](skills/tk-audit/SKILL.md) | `user` | 저장소의 기술 일감을 읽기 전용으로 감사합니다. |
| [tk-prototype](skills/tk-prototype/SKILL.md) | `hybrid` | UI·로직 대안을 비교하는 시제품을 만듭니다. |
| [tk-domain](skills/tk-domain/SKILL.md) | `hybrid` | 저장소 용어와 지속할 결정을 정리합니다. |
| [tk-merge-conflict](skills/tk-merge-conflict/SKILL.md) | `hybrid` | 활성 Git 충돌의 의도를 복원하고 해결합니다. |

### 검토·검증

| 스킬 | 호출 | 소유 범위 |
| --- | --- | --- |
| [tk-review](skills/tk-review/SKILL.md) | `user` | 지정한 변경을 명세와 품질 기준으로 검토합니다. |
| [tk-browser-verify](skills/tk-browser-verify/SKILL.md) | `hybrid` | 브라우저 화면과 동작을 검증하거나 데모 영상을 위해 판정 없이 캡처합니다. |
| [tk-app-verify](skills/tk-app-verify/SKILL.md) | `hybrid` | 데스크톱 앱의 동작·화면·접근성을 검증합니다. |
| [tk-blind-comparison](skills/tk-blind-comparison/SKILL.md) | `hybrid` | 정체를 가린 후보의 점수와 메모를 로컬 갤러리에서 비교합니다. |
| [tk-qa-sheet](skills/tk-qa-sheet/SKILL.md) | `user` | 수동 점검을 기록하는 HTML 시트를 만듭니다. |

### PR 관리

| 스킬 | 호출 | 소유 범위 |
| --- | --- | --- |
| [tk-pr-open](skills/tk-pr-open/SKILL.md) | `hybrid` | 검증된 변경의 PR 발행을 준비하고 승인된 작업을 수행합니다. |
| [tk-pr-respond](skills/tk-pr-respond/SKILL.md) | `hybrid` | 한 PR의 리뷰와 지원 CI에 대응합니다. |
| [tk-pr-rebase](skills/tk-pr-rebase/SKILL.md) | `hybrid` | 지정 PR의 기준 브랜치 갱신과 `tk-pr-sweep`·`tk-pr-respond`의 승인된 작업 넘김을 처리합니다. |
| [tk-pr-sweep](skills/tk-pr-sweep/SKILL.md) | `user` | 여러 PR을 분류하고 승인된 유지보수를 처리합니다. |
| [tk-pr-media](skills/tk-pr-media/SKILL.md) | `hybrid` | PR에 로컬 이미지·GIF·영상을 올립니다. |

### 이해·연구·학습

개념·상황·코드 변경 설명과 실제 답변에 맞춘 후속 수업은 `tk-explain`을 사용합니다.

| 스킬 | 호출 | 소유 범위 |
| --- | --- | --- |
| [tk-ask-repo](skills/tk-ask-repo/SKILL.md) | `user` | 저장소의 동작과 근거를 설명합니다. |
| [tk-explain](skills/tk-explain/SKILL.md) | `hybrid` | 개념·상황·코드 변경을 설명하고 학습자 답변에 맞춰 후속 수업을 제공합니다. |
| [tk-video](skills/tk-video/SKILL.md) | `hybrid` | 소프트웨어와 개념을 설명하는 MP4·GIF 영상을 만듭니다. |
| [tk-research](skills/tk-research/SKILL.md) | `hybrid` | 근거를 조사하고 접근법을 비교합니다. |
| [tk-tts](skills/tk-tts/SKILL.md) | `hybrid` | 한국어 원고에서 검수 가능한 로컬 음원을 생성합니다. |

### 대화·글쓰기

| 스킬 | 호출 | 소유 범위 |
| --- | --- | --- |
| [tk-grill](skills/tk-grill/SKILL.md) | `user` | 아이디어와 결정을 질문으로 구체화합니다. |
| [tk-inquiry](skills/tk-inquiry/SKILL.md) | `hybrid` | 다른 담당자에게 보낼 질문 초안을 작성합니다. |
| [tk-adhd](skills/tk-adhd/SKILL.md) | `hybrid` | 답변과 결과를 찾기 쉽게 구성합니다. |
| [tk-rewrite](skills/tk-rewrite/SKILL.md) | `hybrid` | 기존 글의 맥락과 표현을 다듬습니다. |

### 세션·환경 관리

| 스킬 | 호출 | 소유 범위 |
| --- | --- | --- |
| [tk-retro](skills/tk-retro/SKILL.md) | `hybrid` | 세션을 회고하고 개선안을 제안합니다. |
| [tk-compound](skills/tk-compound/SKILL.md) | `user` | 완료 PR에서 반복 문제와 예방책을 찾습니다. |
| [tk-grooming](skills/tk-grooming/SKILL.md) | `hybrid` | 스킬과 지속 규칙의 중복·충돌을 감사합니다. |
| [tk-skill-vet](skills/tk-skill-vet/SKILL.md) | `hybrid` | 외부 스킬의 설치 전 보안 위험과 업데이트 동작을 정적으로 검토합니다. |
| [tk-handoff](skills/tk-handoff/SKILL.md) | `hybrid` | 세션 현황을 확인하고 인수인계를 작성합니다. |
| [tk-setup-skills](skills/tk-setup-skills/SKILL.md) | `user` | 필요한 스킬과 공통 의존성의 설치·설정을 지원합니다. |
| [tk-wizard](skills/tk-wizard/SKILL.md) | `hybrid` | 설정·인증·이관 절차를 안내합니다. |

### 공통 참조

| 스킬 | 호출 | 소유 범위 |
| --- | --- | --- |
| [tk-questioning](skills/tk-questioning/SKILL.md) | `hybrid` | 질문·승인 라운드와 시각적 질문 기준을 제공합니다. |
| [tk-artifacts](skills/tk-artifacts/SKILL.md) | `hybrid` | 파일 경로·비밀 입력·인증 보존 기준을 제공합니다. |
| [tk-ui-evidence](skills/tk-ui-evidence/SKILL.md) | `hybrid` | UI 문구와 진입 경로의 근거 기준을 제공합니다. |
| [tk-writing](skills/tk-writing/SKILL.md) | `hybrid` | 글쓰기·설명·HTML 표현 기준을 제공합니다. |
| [tk-engineering](skills/tk-engineering/SKILL.md) | `hybrid` | 테스트·진단·리뷰·SDD 기준을 제공합니다. |
| [tk-repository-guidance](skills/tk-repository-guidance/SKILL.md) | `hybrid` | 저장소 맥락·도메인 문서·외부 계약 기준을 제공합니다. |
| [tk-pr-guidance](skills/tk-pr-guidance/SKILL.md) | `hybrid` | PR 전달·시각 자료·리베이스 준비 기준을 제공합니다. |
| [tk-verification-guidance](skills/tk-verification-guidance/SKILL.md) | `hybrid` | 검증 제공자 선택과 근거·설정 기준을 제공합니다. |

## 참고

- [설치 마이그레이션](MIGRATION.md)
- [릴리즈 체크리스트](RELEASE_CHECKLIST.md)
- [출처와 저작권 고지](NOTICE.md)
