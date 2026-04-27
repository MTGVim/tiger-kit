# 사용법

## 언어

TIGAP 명령은 사용자에게 한글로 답하고 TIGAP 산출물도 한글로 작성합니다. 인용한 원문, 코드, 명령어, 경로, 식별자는 원문 그대로 유지할 수 있습니다.

## 브랜치 구성

변경 가능한 TIGAP 작업을 시작하기 전에 원천 자료와 연결되는 브랜치 또는 작업 ID를 우선 사용합니다. 현재 브랜치가 `main`, `master`, `develop` 또는 저장소 기본 브랜치라면 작업 브랜치를 만들거나 전환할지, 또는 `.gap/{work_id}/` 아래에서 사용할 작업 ID를 정할지 물어봅니다.

브랜치 생성과 전환은 사용자 승인 없이 조용히 수행하지 않습니다.

## 1. 원천 자료 없는 계획

원천 자료가 없고 아이디어부터 구체화해야 할 때 실행합니다.

```text
/tigap:plan <아이디어 또는 문제 설명>
```

예시:

```text
/tigap:plan 아직 티켓은 없는데 인터뷰로 요구사항부터 잡아줘.
/tigap:plan plan mode처럼 먼저 문제와 완료 조건을 정리해줘.
```

이 명령은 구현을 시작하지 않고 문제, 목표, 제약, 인수 조건, 검증 방법을 정리합니다.

## 2. 갭 분석

원천 자료나 자료 추출 지시와 함께 실행합니다.

```text
/tigap:gap <원천 자료 또는 자료 추출 지시>
```

예시:

```text
/tigap:gap GitHub issues를 가져와서 분석해.
/tigap:gap docs/spec.md와 현재 구현을 비교해.
/tigap:gap 인터뷰 방식으로 요구사항부터 정리해.
```

자료가 없으면 분석 전에 멈추고 다음 중 하나를 요청합니다.

- 원천 자료 직접 제공
- Claude에게 자료 가져오기 또는 추출 지시
- 인터뷰 방식 요구사항 수집 시작

사용 가능한 원천 자료 예시는 다음과 같습니다.

- 이슈 트래커 티켓
- 지식베이스 문서
- PRD
- 디자인 문서
- 사용자 작성 브리프
- 스크린샷
- 코드 경로
- 기존 구현 참고 자료

스킬은 다음 산출물을 작성합니다.

```text
.gap/{branch_name}/normalized/source-packet.md
.gap/{branch_name}/analysis/gap-report.md
```

## 3. 계획

실행:

```text
/tigap:gaplan
```

스킬은 갭 보고서를 읽고 먼저 다음 파일을 작성합니다.

```text
.gap/{branch_name}/plan/implementation-plan.md
```

사용자가 구현 계획을 검토하고 승인한 뒤에만 다음 파일을 작성합니다.

```text
.gap/{branch_name}/tasks.md
```

계획 모드처럼 확인, 추론, 분해를 먼저 수행하고 작업 목록이 명확해질 때까지 구현을 미룹니다.

## 4. 실행

실행:

```text
/tigap:go
```

스킬은 `tasks.md`를 읽고, 다음 작은 작업 하나를 선택하고, 관련 코드를 확인하고, 좁게 구현하고, 검증한 뒤 작업 상태를 갱신합니다. 완료 보고에는 `Done`, `In Progress`, `Ready`, `Blocked` 기준 진행률과 다음 작업을 포함합니다. 일반 작업이 끝나고 cleanup 작업가 남아 있으면 archive 대상과 정리 목적을 보고합니다. 변경 파일이 있으면 commit 제안을, cleanup까지 끝났으면 push와 PR 생성 제안을 할 수 있습니다. commit, push, PR 생성은 사용자 승인 없이 실행하지 않습니다.

## 5. 상태 / 다음 행동

실행:

```text
/tigap:next
```

스킬은 파일을 수정하지 않고 `.gap/{branch_name}/` 산출물을 읽어 현재 workflow 단계, 브랜치/작업 ID 맥락, 다음 명령 또는 작업을 보고합니다. `implementation-plan.md`는 있지만 `tasks.md`가 없거나 계획 검토 대기 상태라면 `plan-review-needed`로 보고합니다. 다음 행동이 변경 가능한 작업이고 현재 맥락이 기반 브랜치라면 먼저 작업 브랜치나 작업 ID를 정하라고 권장합니다.

## 추천 명령 문장

```text
/tigap:plan 아직 원천 자료가 없으니 인터뷰로 요구사항부터 잡아줘.
/tigap:gap 이 브랜치 기준으로 원천 자료 요청부터 시작해.
/tigap:gaplan 갭 분석 결과를 바탕으로 계획 모드처럼 구현계획 짜줘.
/tigap:go tasks.md 기준으로 다음 작업 하나만 진행해.
/tigap:next 지금 어느 단계인지랑 다음에 뭐할지 알려줘.
```
