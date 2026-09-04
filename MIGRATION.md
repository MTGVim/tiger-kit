# TigerKit 마이그레이션

이 문서는 이전 TigerKit 설치를 `Seed-first` 구조로 갱신할 때 필요한 현재 절차만 다룹니다.
과거 CHANGELOG, `closed` `issue`/PR은 `provenance`이며 `current` `execution` `contract`가 아닙니다.

현재 동작의 정본 순서:

1. `README.md`
2. 현재 `skills/tk-*/SKILL.md`
3. `skill-local` `eval` + `evals/catalog-routing.json`
4. `AGENTS.md`

## 설치 갱신

```bash
npx skills update --global --yes
```

`checkout` `catalog` 확인:

```bash
npx --yes skills@1.5.9 add . --list
npx --yes skills add . --list
```

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
- TigerKit `skill` 반복 `failure` → `tk-skill-diagnose` / `tk-learn`
- 개인 `cross-repo` `memory` → 외부 `memory`

## `Release` `validation`

`Breaking` `eval`/`catalog` 전환은 다음 `gate`를 사용합니다.

```bash
python3 scripts/run_seed_release_gate.py \
  --baseline "<previous-tag-or-commit>" \
  --candidate HEAD \
  --output /tmp/tigerkit-release-gate
```
