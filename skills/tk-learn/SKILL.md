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

명시적 `invocation` 또는 재사용 가능한 `skill`을 작성하려는 명확한 의도에
적용합니다. 대화, 메모, 경로, URL, 반복 workflow 또는 skill-evolution 후보를
`repo skill | user skill` 후보로 전환합니다. 규칙, 일회성 팁, 일반 구현은 범위
밖이며 다른 사용자 호출 `skill`은 절대 호출하지 않습니다.

새 `skill`과 의미 업데이트를 포함한 `skill` `create | improve | merge`의 유일한
TigerKit 작성자입니다. 다른 `skill`에서 온 후보/대상도 증거, 중복 제거, 평가,
호환성, 적용 게이트를 통과해야 합니다.

Draft와 apply는 분리됩니다.

- `draft gate`: 검증된 증거와 확인하지 않은 사용자 진술을 구분하고 `pending`
  후보를 설계합니다. 증거가 여전히 `unverified`여도 명확한 설계 요청은
  `learn.md` 에 기록하되 채팅에 전문을 출력하지 않습니다.
- `apply gate`: `skill` 경로에 쓰기 전에 모든 체크리스트 행이 통과해야 합니다.

## Artifact-first draft checkpoint

새 초안을 만들 때는 승인 전 최소 초안 전체를 채팅에 출력하지
않습니다. 먼저 저장소 루트의 `.tigerkit/learn.md` 에 `pending` 스크래치 장부를
원자적으로 작성하고 같은 경로를 다시 읽어 검증합니다. 이 파일은 정본
`skill` 경로도 아니고 `.tigerkit/skill-drafts/<skill-name>/` 도 아닙니다.

`learn.md` 는 다음 필드를 한 번씩 소유합니다: 작업 `Status` (`Pending | Blocked`),
`Disposition` (`reported | applied | pending`),
`Decision` (`proposed | merge | no-op | continue | pending`), `Candidate`,
`Evidence` (각 주장에 대한 ID/source/`verified | unverified`), `Checklist` (각
적용 검사의 `passed | pending | failed` 와 근거), `Target path` (정확한
계획 경로와 `not created`), `Not created` (두 정본 쓰기 경계),
`Next step` (하나의 실행 가능한 행동), `Updated` (작성 시각 또는 run ID).

원자적 쓰기와 재읽기가 현재 후보/실행과 일치하면 `Disposition: applied` 를
사용할 수 있지만, 적용 승인 전 작업 `Status: Pending` 은 유지합니다.
`Disposition` 은 장부 쓰기/재읽기 결과이고 `Status` 와 같은 의미가 아닙니다.

같은 디렉터리의 임시 파일을 만든 뒤 원자적으로 이름을 바꾸고 즉시 다시 읽습니다.
필수 필드가 없거나 장부가 오래됐거나 없거나 재읽기 내용이 작성 내용과
다르면 `Blocked` 로 중지하고 정본 경로에는 쓰지 않습니다. 기존 장부가
다른 후보/실행을 가리키면 덮어쓰지 말고 `Blocked` 로 보고합니다.

## 작업 흐름

1. **증거 장부:** 각 사례/workflow에 ID, 주장, source, `verified | unverified` 를
   배정합니다. 접근할 수 없는 산출물이 있는 사용자 진술 사례 두 개는 서로 다른
   `unverified` 행으로 남기고 `learn.md` 에 `pending` 상태를 기록합니다. 승격에는
   독립적으로 검증된 반복 2건 또는 산출물이 뒷받침하는 재사용 workflow가 필요합니다.
   `Unverified` 행은 적용을 통과하지 못합니다. 일회성 실수, 원시 로그, 출처 없는
   단일 주장은 `no-op` 으로 종료합니다.
2. **승격 및 중복 제거:** [스킬 품질](references/skill-quality.md)을 적용한 뒤 기존
   저장소/사용자 `skill`, 기본 모델 capability, 짧은 규칙과 비교합니다.
   `merge | no-op | continue | pending` 중 하나를 선택합니다. 카탈로그를 읽을 수
   없으면 `pending` 에 머물되 그 상태와 근거를 `learn.md` 에 기록합니다.
3. **후보 제안:** 대상, 작업 이름, 호출 종류, 양성/음성 trigger를 제시합니다.
   사용자 도메인/workflow 언어를 사용해 64자 이하의 소문자 하이픈 표기 동사형
   이름을 정하고, 충돌을 확인한 뒤 `proposed` 로 표시합니다. 지원하지 않는 값은
   `TBD` 로 남깁니다.
4. **최소 초안:** 최소한의 SKILL.md 입력, workflow, 실패 분기, 승인 경계, 완료
   기준, 출력 계약, 금지 목록을 `learn.md` 에 직접 기록합니다. train/validation
   trigger, 성공/경계 assertion, 무-skill 또는 prior-skill baseline,
   portable-core/host-extension 판정도 추가합니다.
5. **승인 요약:** `learn.md` 를 다시 읽은 뒤 사용자에게 절대 `learn.md` 경로,
   결정/상태/처리 상태, 짧은 요약과 한 번의 승인 질문만 보고하고 멈춥니다.
6. **쓰기·검증·보고:** 적용 권한이 통과한 뒤에만 쓰기 전 내용을 보존하고,
   같은 디렉터리의 임시 대상과 원자적 이름 변경을 사용해 씁니다. 이후
   `applied` 전에 frontmatter, 링크, evals, 대상 호스트 호출을 다시 읽고 검증합니다.

### Apply gate 체크리스트

| 검사 | 통과 증거 | 미통과 |
|---|---|---|
| 승격 기준 | 독립 사례/공통 workflow가 승격 기준을 충족함 | `no-op | pending` |
| 중복 제거 | 기존 skill/기본 capability/짧은 규칙과의 차이 및 `merge | continue` 근거가 있음 | `no-op | pending` |
| 후보 식별 | native target, 이름, kind, 양성/음성 trigger를 확인함 | `pending | Unverifiable` |
| 동작 검증 | train/validation trigger와 성공/경계 assertion이 통과함 | `pending | Blocked` |
| 기준선/호환성 | no-skill/prior baseline 및 portable-core/host-extension 판정을 검증함 | `pending | Unverifiable` |
| 적용 권한 | 현재 턴 승인이 정확한 후보와 대상 경로를 지정함 | `pending`; 쓰지 않음 |

실제 경로 또는 호스트 탐색으로 입증된 현재 호스트의 native repo/user `skill`
경로만 사용합니다. 알 수 없는 호스트는 `Unverifiable`입니다. 위치를 지어내거나
한 호스트의 경로를 다른 호스트에 강제하거나 호스트 간 fan-out/sync를 하거나
`.tigerkit/` 을 영구 `skill` 레지스트리/전역 상태로 사용하지 않습니다.

## 실패 경로

| Trigger | 즉시 조치 | 계속 미해결인 내용 |
|---|---|---|
| 두 사례/workflow를 주장했지만 산출물을 읽을 수 없음 | 각각 `unverified` 로 기록하고 `learn.md` 를 `Blocked` 로 남김 | 정확한 산출물/검사를 요청함; 쓰지 않음 |
| 일회성 사례 하나 또는 원시 로그만 있음 | 기준/개인정보와 `Decision: no-op`, `Status: Pending` 을 기록함 | 후보/경로를 만들지 않음 |
| skill/기본 capability와 중복됨 | `merge | no-op` 과 근거를 보고함 | 새 디렉터리를 만들지 않음 |
| 대상/이름/trigger 일부를 알 수 없음 | 지원되는 값은 `proposed`, 나머지는 `TBD` 로 `learn.md` 에 기록함 | 후보 식별을 `pending` 으로 유지함; 쓰지 않음 |
| 증거/대상/승인이 충돌함 | 충돌과 하나의 결정을 제시함 | `Blocked` 로 중지 |
| 쓰기/쓰기 후 검사가 실패함 | 기존 대상과 실행 임시 파일을 보존하고, 실행 소유임이 입증된 경우에만 부분적으로 생성된 새 대상을 제거함 | 정확히 재현·검증할 수 있을 때만 복구함; 소유권/보존이 불확실하면 `Blocked | Unverifiable`, 그 외에는 실제 경로와 `Fail` 을 보고함 |

## 🔴 CHECKPOINT · 🛑 STOP (승인·중단 지점)

명시적 현재 턴 적용 승인 전에는 정본 경로나
`.tigerkit/skill-drafts/<skill-name>/` 에 쓰지 않습니다. 과거 approval, implicit
invocation, 일반적인 계속 요청은 충분한 권한이 아닙니다. 승인 전 후보는
`pending` 이며 Target path에는 정확한 계획 경로와 `not created` 를 기록합니다.

새 초안의 승인 체크포인트는 반드시 `.tigerkit/learn.md` 작성·재읽기 뒤에
발생합니다. 채팅에 최소 초안 전문, 후보 표 전체, 정확한 계획 파일 본문을
덤프하지 않습니다. 채팅은 장부의 절대 경로, 결정/상태, 1~3줄 요약, 승인 질문
하나만 포함합니다. 장부 작성·재읽기가 실패하면 승인 질문을 내지 않고
`Blocked` 를 보고합니다.

승인 후에도 체크리스트 행이 하나라도 통과하지 않았으면 `applied` 로 보고하지 않습니다.

일회성 `no-op` 경로는 위 표의 `Status: Pending` 을 사용합니다. 이는 해당
경계 결과에만 적용하며, 모든 초안을 `Pending` 으로 바꾸지 않습니다.

## 출력 계약

산출물 작성 후에는 절대 `learn.md` 경로와 `Decision`/`Status`/`Disposition` 를 먼저
보고하고, 핵심 결과를 1~3줄로만 요약합니다. 마지막에는 승인 질문을
정확히 하나만 둡니다. 장부가 소유하는 `Evidence`, `Dedupe`, `Candidate`,
`Target path`, `Verification`, `Remaining concerns` 의 전문을 채팅에 복사하지
않습니다. threshold 실패 또는 중복으로 인한 no-op도 같은 artifact-first 규칙을
따릅니다.

## 금지 사항 / 안티패턴

- 일회성 사례, 자격 증명, 원시 로그, 스크린샷을 재사용 가능한 증거로 승격하거나 초안에 복사하지 않습니다.
- 증거가 `unverified`라는 이유로 요청된 `pending` 초안을 생략하지 않습니다.
- 중복 `skill`, 장황한 기본 capability 래퍼, 구분할 수 없는 trigger 쌍을 만들지 않습니다.
- 승인 전에 쓰거나 암시적 `invocation`을 권한으로 취급하지 않습니다.
- `pending` 초안을 채팅에 전문으로 덤프하고 `learn.md` 를 생략하지 않습니다.
- `learn.md` 의 누락/오래됨/재읽기 실패를 성공 체크포인트로 취급하지 않습니다.
- Receipt에 이름/종류/경로/검증/우려 사항을 중복하지 않습니다.
- 자동 아카이브, `.gitignore` 편집, 다른 사용자 `skill` 호출, push, publish를 하지 않습니다.
