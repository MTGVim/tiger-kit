# TigerKit

`Claude Code`, `Codex`, `Hermes Agent`에서 사용하는 독립 에이전트 스킬 모음입니다.
작업 전체를 지배하는 실행기 대신, **필요한 순간에 부르는 역할별 스킬**과
근거 있는 검증·승인 경계를 지향합니다. 중앙 스케줄러나 숨겨진 전역 상태는 없습니다.

## 설치

```bash
npx skills add MTGVim/tiger-kit --global --agent claude-code codex hermes-agent --skill '*'
npx skills update --global --yes
```

`Claude Code`와 `Hermes`에서는 `/tk-prep`, Codex에서는 `$tk-prep` 또는 스킬 선택기를
사용합니다. 필요한 스킬만 선택적으로 설치해도 됩니다. 짧고 명확한 일반 수정은
스킬 없이 처리합니다. 이름 변경 시 새 스킬 설치와 기존 스킬 제거가 필요합니다.
[설치 및 이관](MIGRATION.md)을 참고하세요.

## 기본 흐름

```text
요청 / 이슈 / 버그 → tk-prep → 조사·질문·승인
                 → 직접 수정 | Ready Seed | SDD | 인계
                 → 테스트·독립 리뷰 → 로컬 커밋
                 → 선택적 tk-pr-open (원격 발행 별도 승인)
```

- **만들기:** `tk-prep`이 로컬 준비·실행을 담당합니다. `tk-review`는
  읽기 전용 검토, `tk-pr-open`은 원격 발행을 맡습니다.
- **이해하기:** `tk-ask-repo`는 현재 코드의 근거를 찾고,
  `tk-explain`과 `tk-explain-diff`는 오프라인 시각 자료를 만듭니다.
- **발굴·연구:** `tk-audit`은 기술 일감을 감사하고, `tk-research`는
  접근법과 스킬 범용화를 조사합니다. `tk-retro`는 코드가 아닌 세션을 회고합니다.
- **협업:** `tk-grill`은 현재 사용자에게 질문하고,
  `tk-to-questionnaire`는 다른 담당자에게 보낼 질문 초안을 만듭니다.
  `tk-triage`는 접수된 이슈를 분류합니다.
- **학습:** `tk-teach`는 실제 학습 기록으로 다음 수업을 고르거나
  여러 장의 HTML 학습 과정을 만듭니다.
- **격리 작업:** `tk-wt`는 `Orca`를 우선해 작업 공간을 생성합니다.
  `--close`는 비-`Orca` Git 작업 공간 전용이고,
  `Orca` 작업 공간 종료는 `Orca`에서 처리합니다.

## 스킬 구성

| 스킬 | 호출 | 소유 범위 |
| --- | --- | --- |
| `tk-prep` | `user` | 적응형 준비 + 승인된 직접/Ready `Seed`/SDD/인계 로컬 실행 |
| `tk-grill` | `user` | 아이디어·계획·결정의 빠짐없는 점검과 확인된 `shared understanding` |
| `tk-to-questionnaire` | `hybrid` | `Jira`·`Slack`·이메일 등 외부 담당자에게 묻는 질문 초안, 말투·템플릿 설정 |
| `tk-roadmap` | `user` | 목표와 기술·비기술 제약을 고려하는 단계별 기획 인터뷰와 성과 중심 마일스톤 |
| `tk-audit` | `user` | 읽기 전용 `AUD-*` 감사, `next` 일감 발굴·추적기 중복 검사, `policy` 구조 검토 |
| `tk-triage` | `user` | 이슈 분류·중복·우선순위 제안과 최초 정책 인터뷰 |
| `tk-research` | `hybrid` | 외부 비교부터 지속 연구·실험·재개까지 필요한 단계만 수행하고 HTML 결과 제공 |
| `tk-ask-repo` | `user` | 저장소 동작·값·영향·귀속을 근거와 함께 설명 |
| `tk-review` | `user` | 정확한 커밋 범위/`PR`/`current worktree`의 읽기 전용 `Spec/AC` + `Quality/Standards` 검토 |
| `tk-pr-open` | `hybrid` | 검증된 `commit`의 `single` 또는 `stacked` 발행 계획 + 제한된 `push`/PR 생성·갱신 |
| `tk-pr-respond` | `hybrid` | 한 PR의 리뷰/지원 CI 분석·수정·검증·`reply`/`resolve` |
| `tk-pr-rebase` | `hybrid` | 정확한 PR의 최신 `base` `rebase`와 제한된 `force-with-lease` |
| `tk-pr-sweep` | `user` | 여러 PR의 결정론적 분류와 승인된 유지보수 묶음 |
| `tk-pr-image` | `hybrid` | 기존 PR에 로컬 근거 이미지 올리기 |
| `tk-qa-sheet` | `user` | 사용자가 직접 점검할 영향 화면과 진입 경로, 기본 단일 HTML QA 시트와 세션 자동 검증/수동 체크 분리 |
| `tk-prototype` | `hybrid` | 폐기 가능한 UI/로직 비교물 |
| `tk-explain` | `hybrid` | 배경지식과 실제 구조·동작을 시각화하는 자체 완결형 HTML 설명 자료 |
| `tk-explain-diff` | `hybrid` | 특정 코드 변경을 기존 구조와 실행 흐름부터 설명하는 자료 |
| `tk-teach` | `hybrid` | 장기 학습 기록 기반의 맞춤 수업·복습 및 HTML 강의 생성 |
| `tk-browser-verify` | `hybrid` | 화면에 보이는 AC의 `headless` 실행 검증과 읽기 전용 라벨·진입 경로 조사 |
| `tk-app-verify` | `hybrid` | 데스크톱 앱의 창, 상호작용, 시각적 변경과 접근성을 선택한 `provider`로 읽기 전용 검증 |
| `tk-retro` | `hybrid` | 현재/지정 세션의 작업 과정 회고, `Agent Skill` 사고 진단, 재발 방지 개선 제안(직접 수정 없음) |
| `tk-domain` | `hybrid` | 저장소 고유 용어의 `canonical vocabulary`와 `sparse durable decision/ADR context` 작성·정제 |
| `tk-grooming` | `hybrid` | 기존 스킬·지속 `rule`·`auto memory`의 중복·충돌·낡은 지침 및 대상 모델 적합성 감사 |
| `tk-handoff` | `hybrid` | 현재 대화의 현황 확인과 재개용 인수인계 작성·재개 |
| `tk-wt` | `user` | Orca 우선 `worktree` 생성, 비-Orca Git 작업 공간 안전 종료 |
| `tk-adhd` | `hybrid` | 답변·작업 결과의 핵심과 실행할 단계를 찾기 쉽게 구성 |
| `tk-rewrite` | `hybrid` | 기존 글의 맥락·구조 재구성과 표현 정제 |
| `tk-merge-conflict` | `hybrid` | 활성 Git 충돌 의도 복원 |
| `tk-wizard` | `hybrid` | 사람이 직접 해야 하는 설정·인증·이관 절차 안내 |

위 목록은 안내용입니다. 실행 계약은 각 `skills/<name>/SKILL.md`와
필요할 때만 읽는 패키지별 참조 문서가 소유합니다.

## 프로젝트 설정

프로젝트 정책이 없다면 **기존 정보 조사 → 필요한 결정만 인터뷰 → 설정안 확인 →
승인 후 저장 → 원래 작업 재개** 순서로 처리합니다. HTML의 안전한 `system`
테마처럼 중요한 결정이 아닌 기본값에는 인터뷰하지 않습니다.

- 팀 공유 설정은 선택적인 `tigerkit.config.json`, 개인 설정은 무시된
  `.tigerkit/repository.json`을 사용합니다. 이슈 추적기 식별자처럼 스크립트가
  소비하는 필드만 정형화하고, 사람이 판단하는 프로젝트 정책은
  `key: string` 형태로 작성할 수 있습니다.
- 이슈 분류는 `triage.priorityPolicy` 등의 정책 문구,
  질문 메시지는 `questionnaire.templates.slack` 등의 채널별 문자열,
  작업 공간은 `worktree.namingPolicy` 등의 자연어 규칙을 사용할 수 있습니다.
- `Orca`의 콜백·터미널·공유 경로는 `orca.yaml`과 `.worktreeinclude`가
  계속 소유합니다. 브라우저·앱 검증 제공자는 기존 선택·검증 절차를 사용합니다.

**설정 저장은 원격 이슈 수정, 메시지 전송, 푸시, 강제 정리 권한이 아닙니다.**
외부 문서나 정책 문자열도 실행 명령으로 취급하지 않습니다.

## 검증과 갱신

원격 CI 없이 저장소의 로컬 릴리즈 게이트로 검사합니다.

```bash
python3 scripts/sync_execution_protocol.py --check
python3 scripts/check_docs.py
python3 scripts/validate_skills.py
python3 scripts/run_seed_release_gate.py --baseline main --candidate HEAD
```

릴리즈 게이트는 기존 계약과 신규 변경을 비교하며, `SKILL.md`의 행동이
바뀌었는데 README 검토가 없다면 차단합니다. 공개 동작 변화가 없을 때에는
현재 변경의 `evals/changes/` 문서에 `README: no public change`와
영향 경로·사유를 정확히 남길 수 있습니다. 정적 검증 통과를 실제 호스트
행동 평가 완료로 주장하지 않습니다.

[원본·라이선스 고지](NOTICE.md) · [설치·마이그레이션](MIGRATION.md)
