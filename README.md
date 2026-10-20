# TigerKit

Claude Code, Codex, Hermes Agent에서 골라 쓰는 작고 조합 가능한 에이전트 스킬 모음입니다.

## 설치

```bash
npx skills add MTGVim/tiger-kit --global --agent claude-code codex hermes-agent --skill '*'
npx skills update --global --yes
```

필요한 스킬만 선택할 수 있습니다. `Claude Code`와 `Hermes`에서는 `/tk-prep`, `Codex`에서는
`$tk-prep` 또는 스킬 선택기를 사용합니다.

## 스킬 구성

`user`는 사용자가 직접 호출하고, `hybrid`는 사용자가 호출하거나 에이전트가 작업에 맞게 선택합니다.
상세한 동작과 권한은 각 스킬 문서를 확인하세요.

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

| 스킬 | 호출 | 소유 범위 |
| --- | --- | --- |
| [tk-ask-repo](skills/tk-ask-repo/SKILL.md) | `user` | 저장소의 동작과 근거를 설명합니다. |
| [tk-explain](skills/tk-explain/SKILL.md) | `hybrid` | 배경지식과 실제 동작을 HTML로 설명합니다. |
| [tk-video](skills/tk-video/SKILL.md) | `hybrid` | 소프트웨어와 개념을 설명하는 MP4·GIF 영상을 만듭니다. |
| [tk-explain-diff](skills/tk-explain-diff/SKILL.md) | `hybrid` | 코드 변경의 배경과 실행 흐름을 설명합니다. |
| [tk-research](skills/tk-research/SKILL.md) | `hybrid` | 근거를 조사하고 접근법을 비교합니다. |
| [tk-teach](skills/tk-teach/SKILL.md) | `user` | 학습 기록에 맞춰 수업과 복습을 구성합니다. |

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
| [tk-handoff](skills/tk-handoff/SKILL.md) | `hybrid` | 세션 현황을 확인하고 인수인계를 작성합니다. |
| [tk-wizard](skills/tk-wizard/SKILL.md) | `hybrid` | 설정·인증·이관 절차를 안내합니다. |

## 참고

- [설치 마이그레이션](MIGRATION.md)
- [릴리즈 체크리스트](RELEASE_CHECKLIST.md)
- [출처와 저작권 고지](NOTICE.md)
