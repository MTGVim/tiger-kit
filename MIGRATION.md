## 공통 참조 스킬과 의존성 설치

공통 문서의 패키지별 사본을 제거하고 참조 전용 스킬에 정본을 둡니다. 기존 업무 스킬의 이름과 권한은
유지하며, 각 `dependencies.json`이 필요한 설치 의존성을 선언합니다. 참조 호출은 다른 업무의 실행을
시작하거나 변경·비밀 접근·게시 권한을 부여하지 않습니다. 필요한 소유 스킬이 없으면 해당 단계만
중단하고 `tk-setup-skills`로 안내합니다. 기억한 내용이나 구 사본을 대체 정본으로 사용하지 않습니다.

처음에는 전체 묶음을 설치하거나 `tk-setup-skills`를 먼저 설치합니다. 선택 설치는 이 스킬로 필요한
업무 스킬과 공통 의존성을 함께 계획합니다. `npx skills` 자체의 자동 의존성 해결을 전제하지 않습니다.
기존 프로젝트·전역 범위와 호스트 대상을 확인하고 승인한 명령만 실행하며, 기존 설치와 프로젝트 정책을
자동 삭제·이동·덮어쓰지 않습니다. 이 저장소의 로컬 변경만으로 사용자 설치본이 갱신되지는 않습니다.

모든 공통 기준을 한 번에 읽지 않습니다. 기존 분기에 도달했을 때 요청한 참조만 읽습니다.
공통 HTML theme CSS·JS, document shell·예제와 assembly/highlight/package/Chrome capture/SVG 도우미는
`tk-writing`이 소유합니다. app/browser 공통 `verify_preferences.py`와 `providers.json`은
`tk-verification-guidance`가 소유합니다. 구 업무 패키지의 자원 사본·wrapper·symlink는 제공하지 않습니다.
문서의 `<tk-writing>`·`<tk-verification-guidance>`는 같은 현재 설치 컬렉션에서 확인한 정확한 소유 패키지
경로이며 호출자 별칭이 아닙니다. 기존 명령·자동화도 새 소유 경로로 바꿔야 합니다. 공유 도우미의 출력·
임시 파일·승인·정리 책임은 호출한 업무에 남고 설치 패키지 안에 결과를 쓰지 않습니다.

공통 builder의 기본 reader 출력은 유지합니다. 자산이 없어 이미 실패하던 `--profile lesson`과
`--profile change`만 제거했습니다. `tk-explain`의 업무 모드와 `archify` 렌더러는 바꾸지 않습니다.
프로젝트별 정책은 기존 `tigerkit.config.json`과 `.tigerkit/repository.json`을 재사용하며 새 범용 상태
저장소나 전역 실행기를 만들지 않습니다. 한 LICENSE 안의 byte-identical 완전 MIT notice만 중복을 줄이고
고유 완전 고지·저작권·attribution은 보존합니다. 독립 배포 패키지 사이의 필요한 LICENSE 반복은 유지합니다.

설계 근거는 [ADR 0004](docs/adr/0004-shared-reference-skills.md)에 있습니다. 기존 ADR 0003의 독립 설치·
문서 사본 계약은 이 전환 범위에서 대체되며, 전환 전 설치는 과거 동작입니다.

## 영상 조립을 `tk-video`로 분리

- `tk-browser-verify`의 조립·내레이션 스크립트는 `tk-video`로 이동합니다. 영상을 사용하는 경우 이 스킬도 설치하세요.
- 브라우저·데스크톱 검증은 캡처와 판정을 계속 담당하며 `tk-video` 없이도 기본 스크린샷 검증을 수행합니다.
- 기존 증거 매니페스트는 `mode: evidence`로 호환됩니다. 설명용 스틸은 별도의 `explainer` 모드를 씁니다.

## PR 미디어 첨부 스킬 전환 (`tk-pr-media`)

`tk-pr-image`는 GIF와 MP4 첨부를 지원하는 `tk-pr-media`로 바뀌었습니다. 이전 호출명 별칭은 없습니다. 새 패키지를 설치한 뒤 이전 패키지를 제거하고 문서·자동화의 호출명을 갱신합니다. 기존 이미지·비교 쌍과 선택된 게시 대상은 유지됩니다.

```bash
npx skills add MTGVim/tiger-kit --global --agent claude-code codex hermes-agent --skill tk-pr-media --yes
npx skills remove tk-pr-image --global --agent claude-code codex hermes-agent
```

## 설명 스킬 통합

`tk-explain-diff`와 `tk-teach`를 제거했습니다. PR·브랜치·커밋 범위 설명은
`tk-explain`의 `change` 모드, 실제 답변을 바탕으로 한 다음 수업은 `follow-up` 경로를 사용합니다.
설명과 조사 보고서 HTML에는 별도 설치된 `archify 3.2.0` 이상이 필요합니다. 명시한
상호작용도 `archify`의 지원 기능으로 작성하며 구 문서 렌더러로 전환하지 않습니다.
지원되지 않는 임의 입력 시뮬레이션은 제한을 알리고 완료로 주장하지 않습니다.
장면 그림은 SVG를 PNG로 바꾸어 `@image`에 넣습니다. QA 시트·블라인드 갤러리·시제품·
시각 질문은 별도 인터페이스를 유지합니다. 기존 학습 자료와 학습 공간은 이동·삭제하지 않습니다.


## 질문 초안 스킬 이름 변경 (`tk-inquiry`)

`tk-to-questionnaire`의 현재 이름은 `tk-inquiry`입니다. 이전 이름을 호출하는
문서·예약·자동화는 새 이름으로 바꿔야 하며, 이전 호출명을 위한 별칭은 제공하지
않습니다. 새 스킬은 다른 담당자에게 보낼 질문 초안만 작성하며 게시나 전송은
수행하지 않습니다. 조사에서 경위를 재구성한 경우에는 관찰 사실과 추정을 구분한
뒤 확인 요청을 작성합니다. `Slack`, `GitHub`, `Jira`, 이메일, 독립 Markdown 문서는
채널별 레퍼런스에 따라 서식을 적용합니다. 선택적인 `questionnaire.templates`에는
채널별 문자열 템플릿을 저장할 수 있습니다.

전역 설치에서 새 이름을 확인한 뒤 이전 패키지를 제거합니다.

```bash
npx skills add MTGVim/tiger-kit --global --agent claude-code codex hermes-agent --skill tk-inquiry --yes
npx skills list --global
npx skills remove tk-to-questionnaire --global --agent claude-code codex hermes-agent
```

프로젝트 공유 정책은 `tigerkit.config.json`, 개인 정책은 무시된 `.tigerkit/repository.json`에 둡니다. 스크립트가 소비하는 ID와 경로는 정형 타입을 유지하고, 모델이 판단하는 정책은 `key: string`으로 작성합니다. 설정 저장은 원격 변경 권한이 아닙니다.

격리 체크아웃은 기존 `tk-prep` 절차를 사용합니다. `Orca` 작업 공간은 `Orca`가 계속 관리하며, 여러 PR의 분류와 사용자 단위 `pr-triage.json` 설정은 `tk-pr-sweep`이 유지합니다. 기존 설정에 남은 이슈 분류·워크트리 예시는 자동 실행하거나 다른 설정으로 옮기지 않습니다.

## README 카탈로그 최신화

README는 짧은 프로젝트 소개, 설치 방법, 간결한 스킬 카탈로그와 참고 링크를 소유합니다. 스킬의 상세 동작은 각 `SKILL.md`와 패키지 참조에 둡니다.

스킬 동작 본문만 바뀌면 README를 갱신하지 않습니다. 스킬 추가·삭제·이름 변경이나 공개 카탈로그 메타데이터(호출 방식·한 줄 역할)가 바뀌면 카탈로그와 링크를 갱신합니다. 별도 변경 manifest는 만들지 않습니다.

게시 전 실제 기능·설치·문서 확인은 [릴리즈 체크리스트](RELEASE_CHECKLIST.md)를 따릅니다. 저장소 전용 테스트·eval·문구 검사 framework는 제거했으며 과거 파일은 Git 이력에서 확인합니다.

---

# TigerKit 마이그레이션

이 문서는 이전 TigerKit 설치를 `Seed-first` 구조로 갱신할 때 필요한 현재 절차만 다룹니다.
과거 CHANGELOG, `closed` `issue`/PR은 `provenance`이며 `current` `execution` `contract`가 아닙니다.

현재 동작의 정본 순서:

1. `README.md`
2. 현재 `skills/tk-*/SKILL.md`
3. `AGENTS.md`와 [릴리즈 체크리스트](RELEASE_CHECKLIST.md)

## 세션 회고 통합 (`tk-retro`)

`tk-learn`과 `tk-skill-diagnose`를 `tk-retro` 하나로 통합했습니다. 세션 회고·스킬 장애 원인 조사·개선안 제안은 `tk-retro`가 맡고, 기존 `tk-learn`의 스킬 생성·수정/적용 권한은 폐기했습니다. 구현은 별도 승인된 변경 담당자가 수행합니다.

```bash
npx skills add MTGVim/tiger-kit --global --agent claude-code codex hermes-agent --skill tk-retro --yes
npx skills list --global
npx skills remove tk-learn tk-skill-diagnose --global --agent claude-code codex hermes-agent
```

옛 이름에 대한 실행 별칭은 없습니다. 진행 중인 `learn-ready` 핸드오프는 이전 권한의 증거가 아니며 현재 근거를 다시 확인해 회고 요청으로 변환합니다.

## 연구 스킬 통합

`tk-autoresearch`와 기존 일회성 `tk-research`를 하나의 `tk-research`로 통합했습니다. 이전 `tk-discover`의 연구 계보도 이어집니다. 일회성 비교부터 지속 연구·실험·재개까지 같은 이름으로 호출하고 연구 과정에서 필요한 단계만 승격합니다. 별칭은 제공하지 않습니다.

전역 설치 예시는 다음과 같습니다. 프로젝트 설치는 기존과 같은 범위에서 처리합니다. 새 스킬이 발견되는지 확인한 뒤 구버전을 제거하세요.

```bash
npx skills add MTGVim/tiger-kit --global --agent claude-code codex hermes-agent --skill tk-research --yes
npx skills list --global
npx skills remove tk-autoresearch tk-discover --global --agent claude-code codex hermes-agent
```

새 호출은 `$tk-research <goal>` 또는 `$tk-research --resume`이며 외부 예약에도 `/tk-research --resume`을 사용합니다. 기본 상태는 필요할 때만 `.tigerkit/research/<slug>/state.md`에 만들고 HTML은 같은 홈의 `report.html`에 제공합니다. 기본 `hybrid` 설정·자동 추적 사본·지식 체크포인트 커밋을 제거했습니다. 명시적인 공유 요청만 정제한 지식을 추적 경로로 저장하며 HTML은 실행 정본이 아닙니다.

기존 `.tigerkit/autoresearch/state.md`는 [이관 계약](skills/tk-research/references/persistence.md#legacy-migration)에 따라 저장소·연구 식별·홈 소유권을 검증한 뒤 실패 근거·실험·출처·전제·질문·현재 탐색 가능 항목·재개 조건·인계 후보와 안정적인 ID를 보존하여 새 로컬 정본으로 옮깁니다. 원자적 저장과 전체 핵심 필드 재확인 성공 전 원본을 삭제하지 않습니다. 성공 후 이전 정본을 역사 자료로 표시하여 중복 재개를 방지합니다. 기존 `local | hybrid | tracked` 설정은 검증하는 이관 입력이며 새 실행 권한이 아닙니다. 알 수 없는 키·모드·버전, 안전하지 않은 경로, 식별 불일치와 여러 소유 후보는 입력을 고치거나 추측하지 않고 중단합니다. 추적 문서·상태 사본은 역사 자료로 보존하며 자동 갱신·삭제하지 않습니다.

옛 `.tigerkit/discover.md`만 있는 경우에는 목표와 저장소를 확인해 새 연구로 준비하며 실행 상태나 권한을 추측하지 않습니다. 운영·보호 데이터와 원격 발행 권한은 기존과 마찬가지로 별도입니다.

## 설치 갱신

```bash
npx skills update --global --yes
```

`checkout` `catalog` 확인:

```bash
npx --yes skills@1.5.9 add . --list
npx --yes skills add . --list
```

## 글 재작성과 시각 설명 스킬 개편

| 이전 이름 | 현재 이름 | 달라진 동작 |
|---|---|---|
| `tk-plain-writing`, `tk-humanizer-kr` | `tk-rewrite` | 내용 재구성 후 표현을 정제하며 최종 본문 하나를 반환합니다. |
| `tk-eli5` | `tk-explain` | 필요한 배경지식과 실제 작동 방식을 설명하며 비유와 분량 제한을 기본값에서 제거합니다. |

기존 이름의 별칭은 제공하지 않습니다. 기존 설치의 업데이트만으로 새 이름이 추가되거나 구버전이 제거됐다고
가정하지 마세요. 현재 사용 중인 에이전트를 대상으로 새 이름을 설치하고 발견되는지 확인한 뒤,
남은 `tk-plain-writing`, `tk-humanizer-kr`, `tk-eli5` 설치를 제거합니다. 전역 설치 예시는 다음과 같습니다.

```bash
npx skills add MTGVim/tiger-kit --global --agent claude-code codex hermes-agent --skill tk-rewrite tk-explain --yes
npx skills list --global
npx skills remove tk-plain-writing tk-humanizer-kr tk-eli5 --global --agent claude-code codex hermes-agent
```

프로젝트에 설치했다면 같은 설치 범위에서 처리합니다. 확인 후 재작성 호출은 `/tk-rewrite`,
시각 설명 자료 요청은 `/tk-explain`으로 변경합니다. 외부 `fluent-korean`은 변경하지 않습니다.
두 새 패키지의 업무는 별개이며, 현재 설치에는 각 `dependencies.json`에 선언된 공통 참조 스킬도 필요합니다.
공통 참조 도입 전의 패키지별 사본·독립 설치 설명은 현재 설치 계약이 아닙니다.

## 현황 안내와 답변 구조의 역할 분리

이전 `tk-status`와 현황 안내용 `tk-adhd`의 대화 전용 기능은 `tk-handoff`로 옮겼습니다.
설치를 갱신하고 현황 확인에는 `/tk-handoff 현황만`을 사용하세요. 안내 후 턴을 종료하고
다른 세션·원격 상태를 조사하거나 파일을 만들지 않는 동작을 유지합니다. 인수인계 작성·재개도 같은 담당자입니다.
선택 설치에서는 `tk-handoff`를 추가하고 확인한 뒤 남은 `tk-status`를 제거하세요. 별칭은 제공하지 않습니다.
현재 `tk-adhd`는 답변과 작업 결과의 구조를 정리합니다. 기존 설치를 갱신해야 이 역할이 적용됩니다.
출력 구조 변경은 현재 답변에만 적용되며 승인된 작업·상세 설명·안전 경계와 다음 턴의 형식을 바꾸지 않습니다.

## `Adaptive prep` 전환

다음 `public` `skill`은 `retired`됩니다.

```text
tk-drive
tk-to-spec
tk-to-tickets
tk-implement
tk-grill-me
```

새 `product-work` `entry` `point`는 `tk-prep`입니다.

```text
$tk-prep <request / issue / bug / review>
→ conversational interview
→ final local-mutation approval
→ direct/no-Seed | Ready Seed direct | SDD | handoff
→ local implementation/review/verification/commit
```

인터뷰 중 `Pending Seed`를 쓰지 않습니다. 지속 가능한 맥락이 필요할 때만 표시된 현재 작업의 Ready `Seed`를 쓰고,
SDD는 `tk-engineering`이 소유한 참조 절차를 필요한 분기에서 읽습니다. 제공자와 `model` 값 및 원격
발행 권한은 지속되는 산출물이나 로컬 실행에서 확장하지 않습니다.

## 이전 `.tigerkit` `artifact`

다음 `artifact`는 `active` `authority`가 아닙니다.

```text
.tigerkit/spec.md
.tigerkit/tickets.md
.tigerkit/implement.md
.tigerkit/session.md
.tigerkit/drive.md
.tigerkit/pr-respond.md
.tigerkit/pr-sweep.md
```

자동 `migration`하지 않습니다.
새 작업은 `current` `request` + `repository`/PR `fresh` `evidence`에서 새 `Seed`를 만듭니다.

이 파일이 기존 `checkout`에 남아 있다는 이유로 `continuation`/`approval` `authority`를 부여하지 않습니다.
TigerKit은 `consumer` `.gitignore`를 수정하지 않습니다.

## `Model` `routing` 제거

이전 `session`/`model` `routing` `contract`는 제거합니다.

```text
cheapest
standard
strongest
model selector
reasoning effort
session.md routing
```

`Seed`는 필요하면 “중간급 `coding` `model`”, “더 강한 `final` `review`”, “`N-way` `fan-out` 권장”처럼
사람 친화적인 실행 추천을 남깁니다.

`host`가 모델 선택이나 `fan-out`을 지원하지 않는다는 이유만으로 작업을 `Blocked` 처리하지 않습니다.

## PR `workflow`

`tk-pr-open`, `tk-pr-respond`, `tk-pr-rebase`, `tk-pr-sweep`의 `remote` `authority`는 유지합니다.

변경점:

- `Respond`/`Sweep`는 `stale` `lifecycle` Markdown보다 GitHub `fresh` `state`를 `truth`로 사용합니다.
- `code-changing` `Respond`는 작은 명확한 수정이면 승인된 현재 대화의 의미론적 리뷰 계획으로 `direct-TDD`를 실행하고, 격리된 자식 실행·복잡한 검증·다중 `Unit` `SDD`처럼 지속 가능한 컨텍스트가 필요할 때만 해당 `worktree`의 표시된 현재 PR Ready `seed.md`를 사용합니다.
- `Sweep` 전체를 `giant` `Seed`로 만들지 않습니다.
- `Sweep`은 SDD `Unit`을 직접 실행하지 않고 중첩 SDD PR 제어기를 기본 순차 실행으로 제한합니다.
- `parent` `Sweep`에서 이미 승인한 `material` `decision`을 `child`가 반복 질문하지 않습니다.
- `user-level` `pr-triage.json`은 `repository` 범위와 선택적인 댓글별
  `toolAuthoredCommentMarkers` 및 `informationalCommentMarkers` HTML 주석 접두어를 유지합니다. 작성자
  마커는 답글 컨펌에만 사용하고, 정보성 마커는 해당 댓글만 답글 대상에서 제외합니다. 재리뷰 대상은
  계속 계정 상태로 판정합니다.

## 대화형 UX

`tk-prep`, `tk-wizard`, `tk-ask-repo`, `tk-pr-respond`, `tk-pr-sweep`은
“대화는 자연스럽게, 상태는 엄격하게”를 공통 원칙으로 사용합니다.

내부 `stage`/`category`/`routing`/`receipt`를 사용자에게 결재 문서처럼 기본 출력하지 않습니다.

`tk-ask-repo`는 마지막에 타팀 공유용 3~10줄 요약을 제공합니다.

## 반복 발견

별도 `tk-evolve`, `user-level` `pitfalls.md`, `troubleshooting.md`는 만들지 않습니다.

- `current` `task` `contract`가 틀림 → `Seed` `revision`
- `repository` `reusable` `fact` → `repo-native` `owner` 개선 후보
- TigerKit `skill` 반복 `failure`·세션 비효율 → `tk-retro` 진단 및 예방안 제안
- 개인 `cross-repo` `memory` → 외부 `memory`

## 릴리즈 체크리스트

현재 [릴리즈 체크리스트](RELEASE_CHECKLIST.md)에 따라 실제 기능·설치·문서와 최종 변경을 확인합니다. 이전 eval/기준 비교 runner는 폐기했으며 저장소의 현재 실행 계약이 아닙니다.

🤖 본 문서는 AI가 작성했습니다.
