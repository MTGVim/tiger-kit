---
name: tk-handoff
description: "[user/auto] verified handoff artifact를 작성하거나 기존 handoff를 명시적으로 재개합니다. 일반 요약, 상태 질문, 일반적인 continuation에는 적용하지 않습니다."
disable-model-invocation: false
argument-hint: "[goal or target] [--output <path>|--resume]"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# 인수인계

명시적 `invocation` 또는 명확한 `handoff` 작성·재개 요청에 적용합니다. 요약,
상태 질문, 일반적인 계속 요청에는 자동 적용하지 않으며 다른 `skill`을
호출하지 않습니다.

## 작업 흐름

### 새 `handoff`

1. `evidence`: 현재 `branch`, 파일, 명령 결과를 경로를 인용한 사실과
   `verified | unverified` 로 매핑합니다.
2. `schema`: 사실과 사용자 승인을 필수 섹션 스냅샷 및
   `confirmed | pending` 결정으로 매핑합니다. 명시적 새 `handoff` 요청은
   이 산출물을 작성할 권한이며, 제품·외부 변경 승인을 뜻하지 않습니다.
3. `write`: 채팅에 초안 전문을 먼저 출력하지 말고, 기본 경로
   `.tigerkit/handoff.md` 또는 명시된 출력 경로에 `pending` 스냅샷을
   같은 디렉터리의 임시 파일에 쓴 뒤 원자적으로 이름을 바꿉니다. 출력 상위
   디렉터리가 없으면 필요한 스크래치 디렉터리만 만듭니다.
   산출물의 설명 문장과 제목은 한국어로 작성하고, 정확한 필드·상태·ID·명령·경로·URL·리터럴만 원문으로 유지합니다.
4. `reread`: 실제로 쓴 경로를 다시 읽어 필수 필드, `Status` 와
   `Disposition` 의 분리, 현재 증거와의 일치를 확인합니다. 불일치하면
   `applied` 를 사용하지 않고 `pending` 또는 복구 상태로 되돌립니다.
5. `receipt`: 재읽기 결과를 산출물 경로와 1~3줄의 상태 요약으로만
   보고합니다. 스냅샷 본문, 전체 초안, 증거 목록을 채팅에
   복사하지 않습니다.

### 재개

1. 상태 점검: 기존 `handoff`를 현재 Git/파일과 비교하고 일치 항목과
   `drift | conflict` 를 나열합니다.
2. 중요도: 증거와 함께 재개 표로 분류합니다.
3. 계속 또는 체크포인트: 표의 계속/중지 결과를 따릅니다.
4. 계속 또는 중지: 드리프트 없음 승인 또는 명시적 중요 드리프트
   확인으로 다음 작업 또는 중지 사유를 생성합니다.

### 재개 결정표

| 분류 | 증거 | 조치 |
|---|---|---|
| `none` | `branch`, 목표, 결정, 소유권, 검증이 현재 증거와 일치함 | `--resume` 을 승인으로 간주하고 추가 질문 없이 계속 |
| `non-material` | 결과를 바꿀 수 없는 타임스탬프/순서 차이 | 기록하고 추가 질문 없이 계속 |
| `material drift` | `branch`/목표 범위, 확인된 결정, 변경 파일 소유권 또는 검증 결과가 다름 | 필수 결정을 하나 묻고 `pending | Blocked` 에서 중지 |
| `conflict` | `handoff`와 현재 소스가 양립할 수 없는 의도/결과를 요구함 | 두 증거 집합과 선택지를 제시하고 `Blocked` 에서 중지 |
| `unverified` | 필요한 Git/파일 상태를 확인할 수 없음 | 추론하지 말고 `Unverifiable` 에서 중지 |

## 계약

기본 대상 `.tigerkit/handoff.md` 에는 다음이 포함됩니다:

- `Goal`: 목표와 범위
- `Status`: `pending | in_progress | completed | aborted | Blocked`
- `Repository state`: 현재 브랜치, HEAD, worktree
- `Handoff path`: 정확히 쓰고 읽은 경로
- `Decisions`: 답변/승인과 연결된 결정만 `confirmed`; 나머지는 `pending`
- `Changed files`: 관찰된 경로만
- `Commands`: 실제 실행한 정확한 명령
- `Verification`: 검사별 결과, `verified | unverified`, 증거 위치
- `Remaining work`: 완료되지 않은 모든 작업
- `Open questions`: 진행 전에 필요한 결정
- `Risks`: 질문과 분리한 남은 실패/회귀 위험
- `Next step`: 남은 작업에서 선택한 하나의 즉시 조치
- `Resume hints`: `Next step`을 반복하지 않고 재개에 필요한 환경/순서/명령만

`handoff.md` 는 아래 단일 스냅샷 골격을 사용합니다. 각 필드는 산출물이
한 번만 소유하며, 실행하지 않은 값은 `unverified` 또는 `pending` 으로 둡니다.

```text
Goal: <goal and scope>
Status: pending | in_progress | completed | aborted | Blocked
Repository state: <branch, HEAD, worktree>
Handoff path: <exact path>
Decisions: <confirmed | pending decisions>
Changed files: <observed paths | none>
Commands: <exact executed commands | none>
Verification: <check/result/evidence location>
Remaining work: <unfinished work | none>
Open questions: <required decisions | none>
Risks: <failure/regression risks | none>
Next step: <one exact immediate action>
Resume hints: <environment/order/command>
Disposition: reported | applied | pending
```

`Next step` 은 대화를 재구성하지 않고 실행 가능해야 합니다. 정확한 대상,
충족한 선행 조건 또는 섹션 참조, 관찰 가능한 완료 증거를 포함합니다. 열린
질문이 작업을 막으면 `Next step`은 후속 실행이 아니라 해당 결정을 얻는
조치여야 합니다.

이번 실행에서 확인한 증거에만 `verified` 를 사용합니다. 이전 `handoff` 주장,
계획, 모델 추론, 실행하지 않은 명령은 `unverified` 로 둡니다. 소유권은
엄격히 지킵니다. `Repository state`는 브랜치/HEAD를, `Handoff path`는 경로를,
`Commands`는 실행한 명령 문자열만, `Verification`은 결과를,
`Next step`/`Resume hints`는 미래 명령을 소유합니다. `reported | applied | pending` 은
산출물 상태이지 작업 `Status`가 아닙니다. 원자적 쓰기와 재읽기가 현재 저장소
상태와 일치한 뒤에만 `applied` 를 사용합니다. 산출물 쓰기가 필요 없는 검증된
드리프트 없음 재개/보고에는 `reported` 를 사용합니다. 그 외에는 `pending` 또는
해당 복구 표의 중지 상태를 사용합니다.

`handoff` 산출물이 disposition과 섹션 참조를 소유합니다. 최종 요약에는 경로,
Git 상태, 명령, 결과, 향후 작업을 중복하지 않으며 메타데이터도 넣지 않습니다.
빈 섹션은 생략하고, 기존 spec/ticket/diff를 복사하지 말고 참조합니다. 복합
결과는 현재 상태, 완료한 작업, 다음 조치, 차단 요인을 2~5개의 짧은 글머리표로
요약하고, 단일 결과는 1~3개의 짧은 줄로 작성할 수 있습니다. 하위 항목이
8개 이상이면 상위 5~7개만 보여주고 전체 목록을 소유한 산출물 경로를 제시합니다.
이는 할당량이 아니라 예산입니다.

## 출력 계약

새 `handoff` 작성이 성공하면 채팅에는 다음만 보고합니다.

- 경로: `<absolute path>`
- `Status: <pending | in_progress | completed | aborted | Blocked>`
- `Disposition: <reported | applied | pending>` 와 필요한 경우 1~2줄의 차단 요인 또는 다음 조치

새로 작성한 `pending` `handoff`에는 위 간결한 보고 뒤에 정확히 하나의 승인
질문을 둡니다. `--resume` 의 검증된 드리프트 없음 보고와 실패/`Blocked`
보고에는 새 승인 질문을 만들지 않습니다.

`Goal`, `Decisions`, `Commands`, `Verification`, `Remaining work` 등 스냅샷
필드의 전문을 채팅에 덤프하지 않습니다. 쓰기 또는 재읽기가 확인되지 않으면
경로를 성공한 산출물처럼 보고하지 않습니다.

`.tigerkit/handoff.md` 만 재개 스냅샷입니다. Drive가 원본 실행을 소유하면
`.tigerkit/drive.md` 의 durable R/AC 및 multi-unit ID를 참조합니다. 절대로
`.tigerkit/work-map.md`, 아카이브, 현재 포인터 또는 전역 상태를 만들지
않습니다. 기존 work-map은 레거시 스크래치로 취급하며 수정·이주·삭제하지
않습니다.

## CHECKPOINT / STOP (승인·중단 지점)

`--resume` 은 재개를 승인하며, 계속 작업은 재개 표만 따릅니다.

스크래치 상위 디렉터리는 필요할 때만 만들고, 같은 디렉터리의 임시 파일에 쓴 뒤
원자적으로 이름을 바꾸고 다시 읽습니다. 실패하면 복구 표를 따릅니다. 아카이브/
현재 포인터를 만들거나 `.gitignore` 를 수정하지 않습니다. 스크래치가 무시되지
않았으면 경고합니다. 요청된 `handoff` 파일이 미해결 결정을
`confirmed` 로 만들지는 않습니다.

명시적 `handoff` 산출물 자체는 `pending` 스냅샷이므로 새 작성 승인 전에 쓸 수
있습니다. 그러나 제품, 테스트, 설정, Git 발행 또는 기타 외부 변경은 별도 승인
전에는 절대 쓰거나 실행하지 않습니다. `--resume` 은 계속 작업을 승인하지만
중요 드리프트/충돌을 해결할 승인을
대신하지 않습니다.

재개할 때 `handoff`와 현재 Git/파일을 읽고 분류합니다. 현재 증거가
없는 내용은 `unverified` 로 유지합니다.

## 실패 복구

| 조건 | 첫 조치 | 계속 실패할 때 |
|---|---|---|
| `handoff`가 없거나 읽히지 않음 | 경로/접근을 보고하고 새 쓰기와 재개를 구분한다 | 증거로 재개 상태를 재구성할 수 없으면 `Unverifiable` 에서 중지한다 |
| 임시 쓰기/교체 실패 | 기존 `handoff`를 보존하고 실행 소유 임시 파일만 정리한 뒤 `pending` 을 보고한다 | 보존 여부를 알 수 없으면 추가 쓰기를 중지하고 `Blocked` 로 둔다 |
| 재읽기 결과가 스키마/현재 상태와 다름 | `applied` 로 표시하지 말고 불일치를 `unverified` 로 되돌린다 | 안전한 재읽기가 불가능하면 `Unverifiable` 에서 중지한다 |
| 레거시 work-map이 존재함 | 레거시 스크래치로 무시한다 | 현재 `handoff`/spec/ticket 증거만 사용하고 절대 변경하지 않는다 |

대화 기록을 복사하거나 아카이브/현재 포인터를 만들지 않으며, 자동으로
commit/publish하지 않습니다.

## 금지 사항 / 안티패턴

- 실행하지 않은 명령, 검사 또는 결정을 `verified | confirmed` 로 표시하지 않습니다.
- 중요 드리프트/충돌을 해결하거나 확인 없이 계속하지 않습니다.
- 아카이브, 현재 포인터, 자동 commit 또는 publication을 만들지 않습니다.
