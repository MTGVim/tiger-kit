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

# 스킬 정리 감사

기존 규칙 또는 스킬에 대한 명시적 호출이나 분명한 감사 요청에만
적용합니다. 일반적인 정리나 구현 요청에는 자동 적용하지 않습니다. 암시적
모드는 report-only입니다.

## 작업 흐름

1. `scope`: 요청된 범위, 리터럴 `--apply`, 대상 경로, 허용된 mutation을
   확인합니다. 활성 conversation 또는 durable governing 소스에서 명시한
   exclusion은 재확인하지 않고 유지합니다.
2. `discovery`: 기존 native 경로만 읽고 요청된 영역의 후보 목록을 만듭니다.
3. `evidence`: 모든 후보에 대해 영역별 관찰, 경로, 검증 상태,
   소유권 근거를 기록합니다.
4. `classification/proposal`: 스킬 후보에
   [배치 기준표](references/repository-placement.md)를 적용하고
   `keep | keep (vendor) | tighten | merge | split | move | deprecate
   | delete | fix`로 분류합니다.
5. `🔴 CHECKPOINT · 🛑 STOP`: 범위, 근거, proposal, 허용된 apply를
   receipt에 요약합니다. Literal initial `--apply` 는 정확히 통과한 receipt
   범위만 사전 승인하며, 그 외에는 명시적인 현재 turn 승인 전까지
   멈춥니다.

Receipt에는 다음 필드를 빠짐없이 둔다. 이는 별도 생명주기 출력이 아니라
`.tigerkit/audit.md` 와 승인 판단에 쓰는 단일 근거 기록이다.

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
   있으면 소스를 다시 읽고 승인된 receipt 범위만 변경합니다.
7. `revalidate`: link, duplication, frontmatter를 다시 확인하고 결과,
   검증되지 않은 범위, 미해결 항목을 보고합니다.

요청에서 명시했거나 함의한 저장소 또는 user 스킬 영역만 조사합니다.
[discovery](references/discovery.md)의 실제 호스트-native 스킬 경로를 사용합니다.
없는 파일을 만들지 말고 저장소/user rule 상태나 legacy/global TigerKit
상태를 조사·이관·생성하지 않습니다.

저장소/user 스킬은 파일 전체가 아니라 독립적으로 규범적인
지침/워크플로 단위로 판단합니다. 정확한 native 스킬 대상이 있을 때만
`move` 를 사용하고, 하나의 산출물에 독립적인 결과가 섞였을 때 `split` 을
사용합니다. 소유자, kind, 범위, 의미를 바꾸지 않고 중복/모호성만
제거할 때만 `tighten` 을 사용합니다. 그 외에는 `keep` 을 사용합니다. 경로 또는
소유권 근거가 없거나 충돌하면 해당 영역만
`Partial/Blocked | Unverifiable` 로 처리합니다.

확인된 경로와 link 대상, package-manager 설치 위치,
updater/version 산출물, 확인 가능한 author 이력으로 소유권을 판단합니다.
이름과 convention은 근거가 아닙니다. vendor-managed임이 확인된 후보는
항상 `keep (vendor)` 로 처리하고 품질 발견 사항만 보고하며 proposal이나
편집을 하지 않습니다. 소유권이 불확실하면 편집 제안 전에 멈추고
사용자 관리인지 외부 설치인지 묻습니다.

분류만으로 변경 권한이 생기지는 않습니다. 승인 후에도
의미를 보존하는 `tighten`, 정확한 대상이 있는 기계적인 `move`,
참조되지 않은 `delete`, frontmatter/link `fix`만 직접 소유합니다. 의미적
`merge`, `deprecate`, 워크플로 `split`, 의미적 스킬 재작성은 `pending`인
정확한 proposal로만 남깁니다. 이 제안은 `tk-learn` 으로 전달될 수 있지만
이 스킬은 이를 호출하지 않습니다. Vendor-managed 후보는 모든 적용 모드에서
report-only로 유지합니다.

리터럴 초기 `--apply` 또는 명시적 현재 turn 승인이 정확한 범위를
지정한 뒤에만 적용합니다. 과거 승인이나 일반적인 continuation만으로는
충분하지 않습니다. 변경 전에 소스를 다시 읽고, 삭제 전 reference를
검색하며, 관리/생성 소유권 표기를 보존하고, 광범위한
저장소/user 변경을 섞지 않습니다. 지식을 지어내거나 스킬 학습을
대체하지 않습니다.

활성 대화에서 선언한 exclusion은 해당 대화의 이후 grooming
실행에서도 계속 제외합니다. 관리 기준 저장소/user rule 또는 요청된 다른
지속 소스에 기록된 exclusion은 session을 넘어 계속 제외합니다. 숨은
전역 상태를 만들거나 `.tigerkit/` 에 exclusion을 저장하지 않습니다.

Literal `--apply`도 checkpoint를 건너뛰지 않습니다. 같은 실행에서 일치하는
근거/대상 receipt만 사전 승인합니다. 범위, 근거, 대상이 drift하면
새 결정을 위해 `Partial/Blocked` 로 멈춥니다.

## 실패 경로

- 누락/읽을 수 없는 경로: 해당 영역만 `Unverifiable` 로 표시하고 다른 영역은
  읽기 전용으로 유지하며 필요한 접근 권한을 보고합니다.
- 알 수 없는 소유권: 편집 제안이나 변경을 만들지 않고 소유권
  질문 하나와 함께 `Partial/Blocked` 를 반환합니다.
- 분류 후 vendor 소유권이 확인됨: 모든 편집 동작을
  `keep (vendor)` 로 바꾸고 산출물을 보존하며 근거를 보고합니다.
- 충돌하는 범위/적용 권한: 변경하지 않고 필요한 결정 하나와
  함께 `Partial/Blocked` 를 반환합니다.
- 참조된 삭제/이동 대상: 변경하지 않고 제안을 `keep | tighten` 으로
  바꾸며 reference를 인용합니다.
- 체크포인트 후 대상 drift: 변경하지 않고 최신 근거와 함께
  `Partial/Blocked` 를 반환하며 새 제안을 요구합니다.
- 적용 후 검증 실패: 절대 `Complete` 이라고 주장하지 않습니다. 이
  run의 delta가 정확히 되돌릴 수 있을 때만 복원/재검증하고 근거와
  함께 `Fail` 을 반환합니다. 보존 또는 복원이 불확실하면 mutation을
  `Unverifiable` 로 중단하고 검사, 경로, 관찰된 상태를 보고합니다.

## 계약

근거는 각 영역의 실제 경로/내용을 기록합니다. 필요한 근거가 없으면
해당 영역을 `Unverifiable` 로 처리합니다. 차단된 영역이 하나라도 있으면 전체
완료를 주장할 수 없으며 `Complete | Fail | Partial/Blocked | Unverifiable` 를 사용합니다.

## 출력 계약

독립적인 규범적 지침/워크플로마다 최초 식별 순서대로 `GR-01`,
`GR-02`, ...를 한 번씩 부여합니다. 하나의 `## Disposition` 표를 먼저
출력합니다.

| ID | Item | Action | Target | Basis |
| --- | --- | --- | --- | --- |
| GR-01 | `<short name>` | `<classification>` | `<target>` | `<evidence refs>` |

적용 변경과 검증에는 같은 ID를 재사용합니다. 근거 공백, 소유권
충돌, 미해결 범위, 실패한 검증이 있을 때만 `## Exceptions` 를
추가합니다. mutation 후에만 `## Applied` 와 `## Verification` 을 추가합니다.
발견 사항은 두 개에서 일곱 개까지 행으로 표시합니다. 여덟 개 이상이면 상위
다섯 개에서 일곱 개를 표시하고 나머지는 감사한 대상 경로별로 묶습니다.
출력만을 위해 산출물/생명주기 동작을 만들지 않습니다. 이는 quota가
아니라 budget입니다.

전체 `report-only | applied` 처분은 `## Disposition` 에 기록하되 table을
반복하거나 메타데이터를 덧붙이지 않습니다. 항목이 없으면
`— | None | keep | — | no finding` 행 하나를 출력합니다. Vendor 행에는
`keep (vendor)` 를 사용합니다.

## CHECKPOINT / STOP (승인·중단 지점)

감사 receipt가 근거와 허용 범위를 식별하기 전에는 `--apply` mutation을
시작하지 않습니다. 모호한 범위 또는 delete/move에 필요한 reference
근거가 없으면 `Partial/Blocked | Unverifiable` 로 멈춥니다.

## 금지 사항 / 반패턴

- 적용 권한 없이 변경하거나 delete/move의 참조 검사를 건너뛰지
  않습니다.
- 요청하지 않은 저장소/user 파일을 조용히 섞지 않습니다.
- 이름으로 소유권을 추정하거나 알 수 없는 소유권에 편집 제안을 만들지
  않으며, `--apply` 가 있어도 vendor-managed 산출물을 변경하지 않습니다.
- legacy/global TigerKit 상태를 조사하거나 이관하지 않습니다.
- 의미적 변환/분할/재작성를 적용하거나 `tk-learn` 을 호출하지 않습니다.
- 항목 ID를 생략·재사용·재번호 매기지 않으며 `## Disposition` 결과 뒤에
  duplicate summary를 덧붙이지 않습니다.
