---
name: tk-learn
description: "[user/auto] 제공된 경험이나 자료에서 재사용 가능한 repository 또는 user skill을 설계합니다. 명확한 skill-authoring intent가 있으면 draft와 approval checkpoint까지만 진행하며, approval 전에는 쓰지 않습니다."
disable-model-invocation: false
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

- `draft gate`: 검증된 evidence와 확인하지 않은 user statement를 구분하고 `pending` candidate를 설계합니다. evidence가 여전히 `unverified`여도 명확한 설계 요청은 `learn.md`에 기록하되 채팅에 전문을 출력하지 않습니다.
- `apply gate`: skill-path에 쓰기 전에 모든 checklist row가 통과해야 합니다.

## Artifact-first draft checkpoint

새 draft를 만들 때는 pre-approval Minimum draft 전체를 채팅에 출력하지
않습니다. 먼저 저장소 루트의 `.tigerkit/learn.md`에 pending scratch ledger를
원자적으로 작성하고 같은 경로를 다시 읽어 검증합니다. 이 파일은 canonical
skill path도 아니고 `.tigerkit/skill-drafts/<skill-name>/`도 아닙니다.

`learn.md`는 다음 필드를 한 번씩 소유합니다: work `Status` (`Pending | Blocked`),
`Disposition` (`reported | applied | pending`),
`Decision` (`proposed | merge | no-op | continue | pending`), `Candidate`,
`Evidence` (각 claim의 ID/source/`verified | unverified`), `Checklist` (각
apply check의 `passed | pending | failed`와 근거), `Target path` (정확한
planned path와 `not created`), `Not created` (두 canonical write 경계),
`Next step` (하나의 실행 가능한 행동), `Updated` (작성 시각 또는 run ID).

atomic write와 reread가 current candidate/run과 일치하면 `Disposition: applied`를
사용할 수 있지만, apply approval 전 work `Status: Pending`은 유지합니다. `Disposition`은
장부 write/readback 결과이고 `Status`와 같은 의미가 아닙니다.

같은 directory의 임시 파일을 만든 뒤 atomic rename하고 즉시 reread합니다.
필수 field가 없거나 장부가 stale/missing이거나 reread 내용이 작성 내용과
다르면 `Blocked`로 중지하고 canonical path에는 쓰지 않습니다. 기존 장부가
다른 candidate/run을 가리키면 덮어쓰지 말고 `Blocked`로 보고합니다.

## 작업 흐름

1. **Evidence ledger:** 각 case/workflow에 ID, claim, source, `verified | unverified`를 배정합니다. 접근할 수 없는 artifact가 있는 두 user-stated case는 서로 다른 unverified row로 남기고 `learn.md`에 pending 상태를 기록합니다. Promotion에는 독립적으로 검증된 반복 2건 또는 artifact가 뒷받침하는 재사용 workflow가 필요합니다. Unverified row는 apply를 통과하지 못합니다. 일회성 실수, raw log, 출처 없는 단일 claim은 `no-op`으로 종료합니다.
2. **Promotion and dedupe:** [skill quality](references/skill-quality.md)를 적용한 뒤 기존 repo/user skill, default model capability, short rule과 비교합니다. `merge | no-op | continue | pending` 중 하나를 선택합니다. 카탈로그를 읽을 수 없으면 `pending`에 머물되 그 상태와 근거를 `learn.md`에 기록합니다.
3. **Candidate proposal:** target, working name, invocation kind, positive/negative trigger를 제시합니다. user domain/workflow 언어를 사용해 64자 이하의 lowercase hyphen-case verb-led name을 정하고, 충돌을 확인한 뒤 `proposed`로 표시합니다. 지원하지 않는 값은 `TBD`로 남깁니다.
4. **Minimum draft:** 최소한의 SKILL.md input, workflow, failure branch, approval boundary, completion criteria, output contract, DO NOT 목록을 `learn.md`에 직접 기록합니다. train/validation trigger, success/boundary assertion, no-skill 또는 prior-skill baseline, portable-core/host-extension 판정도 추가합니다.
5. **Approval summary:** `learn.md`를 reread한 뒤 사용자에게 absolute `learn.md` path,
   decision/status/disposition, 짧은 요약과 한 번의 approval question만 보고하고 멈춥니다.
6. **Write, verify, report:** Apply authority가 통과한 뒤에만 before-write content를
   보존하고, same-directory temporary target과 atomic rename을 사용해 씁니다.
   이후 `applied` 전에 frontmatter, links, evals, target-host invocation을 다시
   읽고 검증합니다.

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
| 두 case/workflow를 주장했지만 artifact를 읽을 수 없음 | 각각 `unverified`로 기록하고 `learn.md`를 `Blocked`로 남김 | 정확한 artifact/check를 요청함; no write |
| 일회성 case 하나 또는 raw log만 있음 | threshold/privacy와 `Decision: no-op`, `Status: Pending`을 기록함 | candidate/path를 만들지 않음 |
| skill/default capability와 중복됨 | `merge | no-op`과 근거를 보고함 | 새 directory를 만들지 않음 |
| target/name/trigger 일부를 알 수 없음 | 지원되는 값은 `proposed`, 나머지는 `TBD`로 `learn.md`에 기록함 | Candidate identity를 `pending`으로 유지함; no write |
| evidence/target/approval이 충돌함 | 충돌과 하나의 결정을 제시함 | `Blocked`로 중지 |
| write/post-write check가 실패함 | 기존 target과 실행 임시 파일을 보존하고, run-owned임이 입증된 경우에만 부분적으로 생성된 새 target을 제거함 | 정확히 재현·검증할 수 있을 때만 복구함; ownership/preservation이 불확실하면 `Blocked | Unverifiable`, 그 외에는 실제 path와 `Fail`을 보고함 |

## 🔴 CHECKPOINT · 🛑 STOP (승인·중단 지점)

명시적 current-turn apply approval 전에는 canonical path나
`.tigerkit/skill-drafts/<skill-name>/`에 쓰지 않습니다. 과거 approval, implicit
invocation, generic continuation은 충분한 권한이 아닙니다. approval 전 candidate는
`pending`이며 Target path에는 정확한 planned path와 `not created`를 기록합니다.

새 draft의 approval checkpoint는 반드시 `.tigerkit/learn.md` 작성·재읽기 뒤에
발생합니다. 채팅에 Minimum draft 전문, candidate 표 전체, exact planned file
body를 덤프하지 않습니다. 채팅은 장부 absolute path, decision/status, 1–3줄
요약, approval question 하나만 포함합니다. 장부 작성·재읽기가 실패하면
approval question을 내지 않고 `Blocked`를 보고합니다.

approval 후에도 checklist row가 하나라도 통과하지 않았으면 `applied`로 보고하지 않습니다.

일회성 `no-op` 경로는 위 표의 `Status: Pending`을 사용합니다. 이는 해당
경계 결과에만 적용하며, 모든 draft를 `Pending`으로 바꾸지 않습니다.

## 출력 계약

artifact 작성 후에는 absolute `learn.md` path와 `Decision`/`Status`/`Disposition`를 먼저
보고하고, 핵심 결과를 1–3줄로만 요약합니다. 마지막에는 approval question을
정확히 하나만 둡니다. 장부가 소유하는 `Evidence`, `Dedupe`, `Candidate`,
`Target path`, `Verification`, `Remaining concerns`의 전문을 채팅에 복사하지
않습니다. threshold 실패 또는 중복으로 인한 no-op도 같은 artifact-first 규칙을
따릅니다.

## 금지 사항 / ANTI-PATTERNS

- 일회성 case, credentials, raw log, screenshot을 재사용 가능한 evidence로 승격하거나 draft에 복사하지 않습니다.
- evidence가 unverified라는 이유로 요청된 pending draft를 생략하지 않습니다.
- duplicate skill, verbose default-capability wrapper, 구분할 수 없는 trigger pair를 만들지 않습니다.
- approval 전에 쓰거나 implicit invocation을 authority로 취급하지 않습니다.
- pending draft를 채팅에 전문으로 덤프하고 `learn.md`를 생략하지 않습니다.
- `learn.md`의 missing/stale/readback failure를 성공 checkpoint로 취급하지 않습니다.
- Receipt에 name/kind/path/verification/concerns를 중복하지 않습니다.
- auto-archive, `.gitignore` 편집, 다른 user skill invoke, push, publish를 하지 않습니다.
