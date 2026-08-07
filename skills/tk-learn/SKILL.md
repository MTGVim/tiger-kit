---
name: tk-learn
description: "[user/auto] 제공된 경험이나 자료에서 재사용 가능한 repository 또는 user skill을 설계합니다. 명확한 skill-authoring intent가 있으면 draft와 approval checkpoint까지만 진행하며, approval 전에는 쓰지 않습니다."
argument-hint: "<conversation, note, path, URL, workflow, or skill-evolution candidate>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# 스킬 학습

명시적 invocation 또는 재사용 가능한 skill을 작성하려는 명확한 intent에 적용합니다. conversation, note, path, URL, 반복 workflow, 또는 skill-evolution candidate를 `repo skill | user skill` candidate로 전환합니다. 규칙, 일회성 tip, 일반 구현은 범위 밖이며 다른 user-invoked skill은 절대 invoke하지 않습니다.

새 skill과 semantic update를 포함해 skill `create | improve | merge`의 유일한 TigerKit writer입니다. 다른 skill에서 온 candidate/target도 evidence, dedupe, eval, compatibility, apply gate를 통과해야 합니다.

Draft와 apply는 분리됩니다.

- `draft gate`: 검증된 evidence와 확인하지 않은 user statement를 구분하고 `pending` candidate를 설계합니다. evidence가 여전히 `unverified`여도 명확한 설계 요청에는 draft를 제공합니다.
- `apply gate`: skill-path에 쓰기 전에 모든 checklist row가 통과해야 합니다.

## 작업 흐름

1. **Evidence ledger:** 각 case/workflow에 ID, claim, source, `verified | unverified`를 배정합니다. 접근할 수 없는 artifact가 있는 두 user-stated case는 서로 다른 unverified row로 남기고 draft를 지원합니다. Promotion에는 독립적으로 검증된 반복 2건 또는 artifact가 뒷받침하는 재사용 workflow가 필요합니다. Unverified row는 apply를 통과하지 못합니다. 일회성 실수, raw log, 출처 없는 단일 claim은 `no-op`으로 종료합니다.
2. **Promotion and dedupe:** [skill quality](references/skill-quality.md)를 적용한 뒤 기존 repo/user skill, default model capability, short rule과 비교합니다. `merge | no-op | continue | pending` 중 하나를 선택합니다. 카탈로그를 읽을 수 없으면 `pending`에 머물되 draft는 계속합니다.
3. **Candidate proposal:** target, working name, invocation kind, positive/negative trigger를 제시합니다. user domain/workflow 언어를 사용해 64자 이하의 lowercase hyphen-case verb-led name을 정하고, 충돌을 확인한 뒤 `proposed`로 표시합니다. 지원하지 않는 값은 `TBD`로 남깁니다.
4. **Minimum draft:** 최소한의 SKILL.md input, workflow, failure branch, approval boundary, completion criteria, output contract, DO NOT 목록을 보여줍니다. train/validation trigger, success/boundary assertion, no-skill 또는 prior-skill baseline, portable-core/host-extension 판정도 추가합니다.
5. **Approval summary:** 각 apply check와 planned path를 한 번씩 요약하고 checklist가 정의한 상태에서 멈춥니다.
6. **Write, verify, report:** Apply authority가 통과한 뒤에만 before-write content를 보존하고, same-directory temporary target과 atomic rename을 사용해 씁니다. 이후 `applied` 전에 frontmatter, links, evals, target-host invocation을 다시 읽고 검증합니다.

### Apply gate 체크리스트

| 검사 | 통과 증거 | 미통과 |
|---|---|---|
| Promotion threshold | independent case/common workflow가 promotion criteria를 충족함 | `no-op | pending` |
| Dedupe | existing skill/default capability/short rule과의 차이 및 `merge | continue` 근거가 있음 | `no-op | pending` |
| Candidate identity | native target, name, kind, positive/negative trigger를 확인함 | `pending | Unverifiable` |
| Behavior validation | train/validation trigger와 success/boundary assertion이 통과함 | `pending | Blocked` |
| Baseline/compatibility | no-skill/prior baseline 및 portable-core/host-extension 판정을 검증함 | `pending | Unverifiable` |
| Apply authority | current-turn approval이 정확한 candidate와 target path를 지정함 | `pending`; no write |

실제 path 또는 host discovery로 입증된 current-host native repo/user skill path만 사용합니다. 알 수 없는 host는 `Unverifiable`입니다. 위치를 지어내거나 한 host의 path를 다른 host에 강제하거나 host 간 fan-out/sync를 하거나 `.tigerkit/`을 영구 skill registry/global state로 사용하지 않습니다.

## 실패 경로

| Trigger | 즉시 조치 | 계속 미해결인 내용 |
|---|---|---|
| 두 case/workflow를 주장했지만 artifact를 읽을 수 없음 | 각각 `unverified`로 기록하고 요청된 `pending` draft를 보여줌 | 정확한 artifact/check를 요청함; no write |
| 일회성 case 하나 또는 raw log만 있음 | threshold/privacy와 `no-op`을 기록함 | candidate/path를 만들지 않음 |
| skill/default capability와 중복됨 | `merge | no-op`과 근거를 보고함 | 새 directory를 만들지 않음 |
| target/name/trigger 일부를 알 수 없음 | 지원되는 값은 `proposed`, 나머지는 `TBD`로 draft함 | Candidate identity를 `pending`으로 유지함; no write |
| evidence/target/approval이 충돌함 | 충돌과 하나의 결정을 제시함 | `Blocked`로 중지 |
| write/post-write check가 실패함 | 기존 target과 실행 임시 파일을 보존하고, run-owned임이 입증된 경우에만 부분적으로 생성된 새 target을 제거함 | 정확히 재현·검증할 수 있을 때만 복구함; ownership/preservation이 불확실하면 `Blocked | Unverifiable`, 그 외에는 실제 path와 `Fail`을 보고함 |

## 🔴 CHECKPOINT · 🛑 STOP (승인·중단 지점)

명시적 current-turn apply approval 전에는 canonical path나 `.tigerkit/skill-drafts/<skill-name>/`에 쓰지 않습니다. 과거 approval, implicit invocation, generic continuation은 충분한 권한이 아닙니다. approval 전 candidate는 `pending`이며 Target path에는 정확한 planned path와 `not created`를 보고합니다.

approval 후에도 checklist row가 하나라도 통과하지 않았으면 `applied`로 보고하지 않습니다.

## 출력 계약

promotion/no-op decision을 먼저 제시합니다. 비어 있지 않은 `Evidence`, `Dedupe`, `Candidate`, `Target path`, `Verification`, `Remaining concerns`만 사용합니다. threshold 실패 또는 중복으로 인한 no-op이면 decision에 필요한 경우를 제외하고 `Candidate`와 `Verification`을 생략합니다. candidate가 여러 개면 `Candidate`를 간결한 `Candidate | Disposition | Target` 표로 표시하고, user-relevant row가 하나면 문장으로 표시합니다. candidate, target, remaining-gate 결과가 2–7개면 제한된 row/bullet로 요약합니다. 8개 이상이면 상위 5–7개를 보여주고 나머지를 소유하는 draft/planned target path를 인용합니다. quota가 아니라 budget을 사용합니다. 소유한 candidate/concern section에 `reported | pending | applied`를 기록하며 metadata를 덧붙이거나 candidate 결과를 대체하지 않습니다.

## 금지 사항 / ANTI-PATTERNS

- 일회성 case, credentials, raw log, screenshot을 재사용 가능한 evidence로 승격하거나 draft에 복사하지 않습니다.
- evidence가 unverified라는 이유로 요청된 pending draft를 생략하지 않습니다.
- duplicate skill, verbose default-capability wrapper, 구분할 수 없는 trigger pair를 만들지 않습니다.
- approval 전에 쓰거나 implicit invocation을 authority로 취급하지 않습니다.
- Receipt에 name/kind/path/verification/concerns를 중복하지 않습니다.
- auto-archive, `.gitignore` 편집, 다른 user skill invoke, push, publish를 하지 않습니다.
