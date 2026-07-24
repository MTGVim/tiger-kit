---
name: tk-learn
description: "[user/auto] 제공된 경험이나 자료로 재사용 가능한 repository 또는 user skill을 설계할 때 사용합니다. 명확한 skill 작성 의도에서 draft와 approval checkpoint까지만 자동 진행하며 승인 전에는 쓰지 않습니다."
argument-hint: "<대화, 메모, 경로, URL, 워크플로 또는 reflect 후보>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# 학습

명시 호출 또는 재사용 가능한 skill 작성 의도가 분명한 요청에 사용합니다. 현재 대화, 메모, 경로, URL, 반복 workflow 또는 reflect 후보를 `repo skill`이나 `user skill` 후보로 바꾸세요. 규칙 생성, 일회성 팁 적용, 일반 구현은 범위 밖이며 다른 user-invoked skill을 호출하지 마세요.

신규 skill 생성과 기존 skill의 semantic update/merge를 실제로 쓰는 유일한 TigerKit writer입니다. 다른 skill이 제안한 candidate/target도 이 skill의 evidence, dedupe, eval, compatibility와 apply gate를 다시 통과해야 합니다.

Draft와 apply는 서로 다른 gate입니다.

- `draft gate`: 확인된 증거와 아직 확인하지 못한 사용자 진술을 구분해 `pending` 후보를 설계합니다. 증거가 `unverified`여도 명확한 skill 설계 요청이면 초안을 생략하지 않습니다.
- `apply gate`: 아래 checklist의 모든 항목이 통과해야 skill 경로에 쓸 수 있습니다.

## Workflow

다음 순서를 지키세요.

1. **Evidence ledger** — 각 사례·workflow에 ID, 주장, 출처, `verified | unverified`를 붙입니다. 사용자가 서로 다른 두 사례와 공통 workflow가 있다고 명시했지만 artifact를 읽을 수 없으면 그 진술을 별도 `unverified` 항목으로 보존하고 draft를 계속하세요. 한 번 발생한 개인 실수, 원시 log 또는 출처 없는 단일 주장은 threshold 미달 `no-op`으로 끝냅니다.
2. **Promotion과 dedupe** — [스킬 품질](references/skill-quality.md)의 승격 gate를 적용하고 기존 repo/user skill, 기본 모델 기능, 짧은 rule과 비교해 `merge | no-op | continue | pending`을 판정합니다. 목록을 읽을 수 없으면 `pending`으로 표시하되 draft는 계속합니다.
3. **Candidate proposal** — target, working name, invocation kind, positive/negative trigger를 제시합니다. 사용자가 준 도메인·workflow 표현으로 reversible working name과 trigger 예시를 만들고 `proposed`로 표시하세요. 근거가 없는 동작은 발명하지 말고 해당 값만 `TBD`로 남깁니다.
4. **Minimum draft** — 입력, 핵심 workflow, 명시적 실패 분기, approval boundary, 완료 기준, 출력 계약, DO NOT 목록을 포함한 최소 SKILL.md를 보여줍니다. 이어 train/validation trigger, success/boundary assertion, no-skill 또는 이전 skill baseline, portable-core/host-extension 판정을 제시합니다.
5. **Approval summary** — apply gate checklist의 항목별 상태와 계획 경로를 한 번씩 요약하고 checklist가 정한 상태로 멈춥니다.
6. **Write, verify, report** — checklist의 Apply authority가 통과한 뒤 write 전 내용을 보존하고 적용합니다. frontmatter, links, evals, target-host invocation을 검증한 뒤에만 `applied`로 보고합니다.

### Apply gate checklist

| Check | Pass evidence | Not passed |
|---|---|---|
| Promotion threshold | 독립 사례와 공통 workflow가 승격 기준 충족 | `no-op | pending` |
| Dedupe | 기존 skill·기본 기능·짧은 rule과의 차이 및 `merge | continue` 근거 | `no-op | pending` |
| Candidate identity | native target, name, invocation kind, positive/negative trigger 확정 | `pending | Unverifiable` |
| Behavior validation | train/validation trigger와 success/boundary assertion 통과 | `pending | Blocked` |
| Baseline·compatibility | no-skill/이전 skill baseline과 portable-core/host-extension 판정 확인 | `pending | Unverifiable` |
| Apply authority | 현재 turn에 정확한 후보와 target path를 명시 승인 | `pending`; write 금지 |

Target은 실제 경로나 host discovery evidence로 식별된 현재 host의 native repo/user skill 위치만 사용하세요. Current host를 식별할 수 없으면 경로를 발명하지 말고 `Unverifiable`로 멈춥니다. 한 host 전용 위치를 다른 host에 강제하거나 cross-host fan-out/sync하지 말고, `.tigerkit/`을 영구 skill registry나 global state로 사용하지 마세요.

## Failure paths

| Trigger | Immediate action | Still unresolved |
|---|---|---|
| 두 사례·workflow 주장은 있으나 artifact를 읽을 수 없음 | 각 주장을 `unverified`로 기록하고 requested candidate를 `pending` draft로 제시 | 필요한 artifact와 검증 항목을 정확히 요청하고 write하지 않음 |
| 단일 일회성 사례 또는 raw log뿐임 | threshold 미달과 privacy 경계를 기록하고 `no-op` | 후보·경로를 만들지 않음 |
| 기존 skill 또는 기본 기능과 중복 | `merge` 또는 `no-op`과 근거를 보고 | 새 디렉터리를 만들지 않음 |
| target·name·trigger 일부가 미확정 | 근거 있는 값은 `proposed`, 나머지는 `TBD`로 둔 draft를 제시 | Candidate identity 미통과 상태로 멈춤 |
| 증거·대상·승인이 충돌 | 충돌과 필요한 결정을 한 번만 제시 | `Blocked`로 멈춤 |
| write 또는 post-write validation 실패 | 기존 대상을 보존하고 이번 실행의 임시 파일만 정리 | 정확히 복원·재검증 가능할 때만 되돌리고, 아니면 실제 경로와 `Fail | Blocked | Unverifiable` 증거를 보고 |

## 🔴 CHECKPOINT · 🛑 STOP

현재 turn의 명시적 apply 승인 전에는 canonical path와 `.tigerkit/skill-drafts/<skill-name>/` 어디에도 쓰지 마세요. 과거 승인, implicit invocation, “계속” 같은 일반 응답은 승인이 아닙니다. 승인 전 candidate는 항상 `pending`이며 Created path는 계획한 정확한 경로와 `not created`를 표시합니다.

승인 후에도 apply gate checklist의 항목이 하나라도 통과하지 않으면 `applied`로 표시하지 마세요.

## Output contract

Approval 전 출력은 다음 필드를 각각 한 번만 소유합니다.

- `Evidence`: 사례·threshold·출처와 `verified | unverified`
- `Dedupe`: 검사 범위, `merge | no-op | continue | pending`, 근거
- `Candidate`: target, proposed name/kind, positive/negative trigger, 최소 SKILL.md, eval/baseline/compatibility
- `Created path`: 정확한 계획 경로와 `not created`
- `Verification`: 실행한 검사 또는 실행 전 `unverified`
- `Remaining concerns`: 승인 전에 해결할 항목
- `Receipt`: `reported | pending | applied`와 위 필드 참조만 기록

## DO NOT / ANTI-PATTERNS

- 일회성 사례, credential, raw log 또는 screenshot을 재사용 증거로 승격하거나 draft에 복사하지 마세요.
- 명확한 설계 요청에서 증거가 `unverified`라는 이유만으로 requested pending draft 전체를 생략하지 마세요.
- 기존 skill과 동등한 후보, 기본 기능의 장황한 복제, 구별되지 않는 positive/negative trigger를 만들지 마세요.
- 승인 전 skill 경로에 쓰거나 implicit invocation을 write 승인으로 해석하지 마세요.
- 이름·종류·경로·검증·우려 사항을 Receipt에서 다시 설명하지 마세요.
- 자동 보관, `.gitignore` 편집, 다른 user-invoked skill 호출, push·publish를 하지 마세요.
