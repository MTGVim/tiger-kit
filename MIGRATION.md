## 장기 학습 스킬 전환 (tk-teach)

기존 `tk-study`는 `tk-teach`로 이름을 변경했습니다. 기존 HTML 강의·커리큘럼 생성은 유지하면서, 학습 미션과 실제 답변·오개념을 `learning-records/`에 누적해 다음 수업과 복습에 반영합니다. 자동 숙달 추정이나 글로벌 학습자 DB는 없습니다. 새 기본 과정은 무시된 `.tigerkit/teach/<topic>/`에 저장하며, 이전 `.tigerkit/study/<topic>/`는 신원을 확인한 경우 그 자리에서 이어서 학습할 수 있습니다. 타 장비/팀 공유가 필요하면 명시한 Git 추적 학습 워크스페이스에 승인하여 저장합니다. 기존 자료를 자동 이동·삭제하지 않습니다.

```bash
npx skills add MTGVim/tiger-kit --global --agent claude-code codex hermes-agent --skill tk-teach --yes
npx skills list --global
npx skills remove tk-study --global --agent claude-code codex hermes-agent
```

## 질문 초안 (`tk-to-questionnaire`)

`Slack`·`Jira`·이메일 등 다른 담당자에게 보낼 질문 초안을 만듭니다. 게시나 전송은 수행하지 않습니다. 선택적인 `questionnaire.templates`에 채널별 문자열 템플릿을 저장할 수 있습니다.

프로젝트 공유 정책은 `tigerkit.config.json`, 개인 정책은 무시된 `.tigerkit/repository.json`에 둡니다. 스크립트가 소비하는 ID와 경로는 정형 타입을 유지하고, 모델이 판단하는 정책은 `key: string`으로 작성합니다. 설정 저장은 원격 변경 권한이 아닙니다.

격리 체크아웃은 기존 `tk-prep` 절차를 사용합니다. `Orca` 작업 공간은 `Orca`가 계속 관리하며, 여러 PR의 분류와 사용자 단위 `pr-triage.json` 설정은 `tk-pr-sweep`이 유지합니다. 기존 설정에 남은 이슈 분류·워크트리 예시는 자동 실행하거나 다른 설정으로 옮기지 않습니다.

## 문서 최신화 릴리즈 게이트

공개 `SKILL.md`가 변경되면 README도 업데이트하거나 변경된 `evals/changes/*.md`에 `README: no public change`를 명시하고 영향받는 스킬 경로와 이유를 남겨야 합니다. `scripts/check_docs.py` 정적 목록·호출 검사와 `run_seed_release_gate.py`의 기준 버전 비교 기반 최신화 검사를 함께 통과해야 합니다.

---

# TigerKit 마이그레이션

이 문서는 이전 TigerKit 설치를 `Seed-first` 구조로 갱신할 때 필요한 현재 절차만 다룹니다.
과거 CHANGELOG, `closed` `issue`/PR은 `provenance`이며 `current` `execution` `contract`가 아닙니다.

현재 동작의 정본 순서:

1. `README.md`
2. 현재 `skills/tk-*/SKILL.md`
3. `evals/skills/<skill>/`의 저장소 전용 `eval` + `evals/catalog-routing.json`
4. `AGENTS.md`

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
두 새 패키지는 공통 참조 문서와 라이선스를 각각 포함하므로 서로 따로 설치할 수 있습니다.

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
SDD는 `tk-prep`/`tk-pr-respond`의 생성된 패키지 로컬 공유 절차를 사용합니다. 제공자와 `model` 값 및 원격
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
  `toolAuthoredCommentMarkers` HTML 주석 접두어만 유지합니다. 마커는 답글 컨펌에만 사용하며 재리뷰 대상은
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

## `Release` `validation`

`Breaking` `eval`/`catalog` 전환은 다음 `gate`를 사용합니다.

```bash
python3 scripts/run_seed_release_gate.py \
  --baseline "<previous-tag-or-commit>" \
  --candidate HEAD
```

🤖 본 문서는 AI가 작성했습니다.
