---
name: tk-grooming
description: "[user/auto] 기존 repository 또는 user skill의 중복·범위·배치·trigger를 감사합니다. 기본값은 report-only이며 literal --apply 또는 current-turn approval 전에는 절대 변경하지 않습니다."
disable-model-invocation: false
argument-hint: "[scope] [--apply]"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Skill Grooming 감사

기존 rule 또는 skill에 대한 명시적 invocation이나 분명한 감사 요청에만
적용합니다. 일반적인 정리나 구현 요청에는 자동 적용하지 않습니다. Implicit
mode는 report-only입니다.

## 작업 흐름

1. `scope`: 요청된 범위, literal `--apply`, target paths, 허용된 mutation을
   확인합니다. active conversation 또는 durable governing source에서 명시한
   exclusion은 재확인하지 않고 유지합니다.
2. `discovery`: 기존 native path만 읽고 요청된 영역의 후보를 inventory합니다.
3. `evidence`: 모든 후보에 대해 영역별 observation, path, verification state,
   ownership evidence를 기록합니다.
4. `classification/proposal`: skill 후보에
   [placement rubric](references/repository-placement.md)을 적용하고
   `keep | keep (vendor) | tighten | merge | split | move | deprecate
   | delete | fix`로 분류합니다.
5. `🔴 CHECKPOINT · 🛑 STOP`: scope, evidence, proposal, 허용된 apply를
   receipt에 요약합니다. Literal initial `--apply` 는 정확히 통과한 receipt
   scope만 사전 승인하며, 그 외에는 명시적인 current-turn approval 전까지
   멈춥니다.

Receipt에는 다음 필드를 빠짐없이 둔다. 이는 별도 lifecycle output이 아니라
`.tigerkit/audit.md` 와 approval 판단에 쓰는 단일 evidence record다.

```text
Scope: <exact repository/user skill scope>
Target paths: <exact paths | none>
Evidence refs: <path:line or unavailable>
Proposal IDs: <GR-## list | none>
Apply authority: report-only | literal --apply | current-turn approval
Audited: <covered paths/categories>
Unaudited: <excluded or incomplete paths/categories>
Verification: <check results or unavailable>
Drift rule: <scope/evidence/target change => Partial/Blocked>
```

6. `apply/report`: report-only는 proposal/receipt를 출력합니다. authority가
   있으면 source를 다시 읽고 승인된 receipt scope만 변경합니다.
7. `revalidate`: link, duplication, frontmatter를 다시 확인하고 결과,
   검증되지 않은 scope, 미해결 항목을 보고합니다.

요청에서 명시했거나 함의한 repository 또는 user skill 영역만 조사합니다.
[discovery](references/discovery.md)의 실제 host-native skill path를 사용합니다.
없는 파일을 만들지 말고 repository/user rule state나 legacy/global TigerKit
state를 조사·이관·생성하지 않습니다.

repository/user skill은 파일 전체가 아니라 독립적으로 규범적인
instruction/workflow 단위로 판단합니다. 정확한 native skill target이 있을 때만
`move` 를 사용하고, 하나의 artifact에 독립적인 outcome이 섞였을 때 `split` 을
사용합니다. owner, kind, scope, meaning을 바꾸지 않고 duplication/ambiguity만
제거할 때만 `tighten` 을 사용합니다. 그 외에는 `keep` 을 사용합니다. path 또는
ownership evidence가 없거나 충돌하면 해당 영역만
`Partial/Blocked | Unverifiable` 로 처리합니다.

resolved path와 link target, package-manager installation location,
updater/version artifact, 확인 가능한 author history로 ownership을 판단합니다.
이름과 convention은 evidence가 아닙니다. vendor-managed임이 확인된 후보는
항상 `keep (vendor)` 로 처리하고 quality finding만 보고하며 proposal이나
편집을 하지 않습니다. ownership이 불확실하면 edit proposal 전에 멈추고
user-managed인지 externally installed인지 묻습니다.

Classification만으로 mutation authority가 생기지는 않습니다. 승인 후에도
meaning-preserving `tighten`, 정확한 target이 있는 mechanical `move`,
unreferenced `delete`, frontmatter/link `fix`만 직접 소유합니다. Semantic
`merge`, `deprecate`, workflow `split`, semantic skill rewrite는 `pending`인
정확한 proposal로만 남깁니다. 이 proposal은 `tk-learn` 으로 전달될 수 있지만
이 skill은 이를 호출하지 않습니다. Vendor-managed 후보는 모든 apply mode에서
report-only로 유지합니다.

literal initial `--apply` 또는 명시적 current-turn approval이 정확한 scope를
지정한 뒤에만 적용합니다. 과거 승인이나 일반적인 continuation만으로는
충분하지 않습니다. 변경 전에 source를 다시 읽고, 삭제 전 reference를
검색하며, managed/generated ownership marking을 보존하고, 광범위한
repo/user 변경을 섞지 않습니다. 지식을 지어내거나 skill learning을
대체하지 않습니다.

active conversation에서 선언한 exclusion은 해당 conversation의 이후 grooming
run에서도 계속 제외합니다. governing repository/user rule 또는 요청된 다른
durable source에 기록된 exclusion은 session을 넘어 계속 제외합니다. hidden
global state를 만들거나 `.tigerkit/` 에 exclusion을 저장하지 않습니다.

Literal `--apply`도 checkpoint를 건너뛰지 않습니다. 같은 run에서 일치하는
evidence/target receipt만 사전 승인합니다. scope, evidence, target이 drift하면
새 결정을 위해 `Partial/Blocked` 로 멈춥니다.

## 실패 경로

- Missing/unreadable path: 해당 영역만 `Unverifiable` 로 표시하고 다른 영역은
  read-only로 유지하며 필요한 access를 보고합니다.
- Unknown ownership: edit proposal이나 mutation을 만들지 않고 ownership
  question 하나와 함께 `Partial/Blocked` 를 반환합니다.
- Vendor ownership discovered after classification: 모든 edit action을
  `keep (vendor)` 로 바꾸고 artifact를 보존하며 evidence를 보고합니다.
- Conflicting scope/apply authority: 변경하지 않고 필요한 decision 하나와
  함께 `Partial/Blocked` 를 반환합니다.
- Referenced delete/move target: 변경하지 않고 proposal을 `keep | tighten` 으로
  바꾸며 reference를 인용합니다.
- Target drift after checkpoint: 변경하지 않고 최신 evidence와 함께
  `Partial/Blocked` 를 반환하며 새 proposal을 요구합니다.
- Failed post-apply validation: 절대 `Complete` 이라고 주장하지 않습니다. 이
  run의 delta가 정확히 되돌릴 수 있을 때만 restore/revalidate하고 evidence와
  함께 `Fail` 을 반환합니다. 보존 또는 복원이 불확실하면 mutation을
  `Unverifiable` 로 중단하고 check, path, 관찰된 state를 보고합니다.

## 계약

Evidence는 각 영역의 실제 path/content를 기록합니다. 필요한 evidence가 없으면
해당 영역을 `Unverifiable` 로 처리합니다. blocked 영역이 하나라도 있으면 전체
완료를 주장할 수 없으며 `Complete | Fail | Partial/Blocked | Unverifiable` 를 사용합니다.

## 출력 계약

독립적인 normative instruction/workflow마다 최초 식별 순서대로 `GR-01`,
`GR-02`, ...를 한 번씩 부여합니다. 하나의 `## Disposition` table을 먼저
출력합니다.

| ID | Item | Action | Target | Basis |
| --- | --- | --- | --- | --- |
| GR-01 | `<short name>` | `<classification>` | `<target>` | `<evidence refs>` |

적용 변경과 verification에는 같은 ID를 재사용합니다. evidence gap, ownership
conflict, unresolved scope, failed verification이 있을 때만 `## Exceptions` 를
추가합니다. mutation 후에만 `## Applied` 와 `## Verification` 을 추가합니다.
finding은 두 개에서 일곱 개까지 행으로 표시합니다. 여덟 개 이상이면 상위
다섯 개에서 일곱 개를 표시하고 나머지는 audited target path별로 묶습니다.
출력만을 위해 artifact/lifecycle behavior를 만들지 않습니다. 이는 quota가
아니라 budget입니다.

전체 `report-only | applied` disposition은 `## Disposition` 에 기록하되 table을
반복하거나 metadata를 덧붙이지 않습니다. 항목이 없으면
`— | None | keep | — | no finding` 행 하나를 출력합니다. Vendor 행에는
`keep (vendor)` 를 사용합니다.

## CHECKPOINT / STOP (승인·중단 지점)

audit receipt가 evidence와 허용 scope를 식별하기 전에는 `--apply` mutation을
시작하지 않습니다. 모호한 scope 또는 delete/move에 필요한 reference
evidence가 없으면 `Partial/Blocked | Unverifiable` 로 멈춥니다.

## 금지 사항 / 반패턴

- apply authority 없이 변경하거나 delete/move의 reference check를 건너뛰지
  않습니다.
- 요청하지 않은 repository/user file을 조용히 섞지 않습니다.
- 이름으로 ownership을 추정하거나 unknown ownership에 edit proposal을 만들지
  않으며, `--apply` 가 있어도 vendor-managed artifact를 변경하지 않습니다.
- legacy/global TigerKit state를 조사하거나 이관하지 않습니다.
- semantic convert/split/rewrite를 적용하거나 `tk-learn` 을 호출하지 않습니다.
- item ID를 생략·재사용·재번호 매기지 않으며 `## Disposition` 결과 뒤에
  duplicate summary를 덧붙이지 않습니다.
