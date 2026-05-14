# 사용법

## 언어

명령은 사용자에게 한글로 답하고 작업 산출물도 한글로 작성합니다. URL, 코드, 명령어, 경로, 식별자, commit hash는 원문 그대로 유지할 수 있습니다.

## 핵심 모델

```text
TigerKit = source-of-truth index + reproducible gap record + session reflection
```

TigerKit은 LLM의 장기 절차 기억에 실행 순서나 진행 상태를 맡기지 않습니다.

권장 순서:

```text
/tk:prep
/tk:gap
/tk:reflect
```

## Command Surface

| Command | 역할 |
| --- | --- |
| `/tk:prep` | source-of-truth reference와 직접 사용자 인터뷰를 `.tigerkit/requirements.md`에 인덱싱 |
| `/tk:gap` | indexed SOT reference와 특정 code baseline을 비교해 `.tigerkit/gap.md`에 evidence-based gap 기록 |
| `/tk:reflect` | session 전체를 재구성해 `.tigerkit/reflect.md`를 갱신하고 derived repo docs 업데이트 제안/적용 |

## 1. Source index

```text
/tk:prep <요구사항 source, 티켓, Figma, PRD, issue, 직접 인터뷰>
```

하는 일:

1. 외부 source와 직접 사용자 인터뷰를 분리
2. 외부 source는 reference만 저장
3. 현재 session 사용자 인터뷰는 raw text에 가깝게 저장
4. derived interpretation은 별도 표시
5. ambiguity를 숨기지 않고 기록

하지 않는 일:

- external source 내용을 local requirement로 재작성
- source summary를 official requirement처럼 저장
- 실행 대기열 생성
- `DESIGN.md` 또는 `reuse-map.md` 업데이트
- 구현, commit, push, PR 생성

권장 구조:

```md
# TigerKit Requirements Index

## External Sources

- PRD: https://...
- Figma: https://...
- GitHub Issue: https://...

## Interviewed Requirements

### Raw

> 사용자 원문에 가까운 내용

### Derived Interpretation

- 명시적으로 파생 해석임을 표시

## Ambiguities

- 확인되지 않은 점
```

## 2. Gap record

```text
/tk:gap
```

하는 일:

1. `.tigerkit/requirements.md`에서 compared SOT reference 확인
2. code baseline 확인
3. working tree가 clean하지 않으면 commit 또는 정리 요청
4. 관련 code path inspection
5. evidence와 interpretation 분리
6. `.tigerkit/gap.md`에 gap 기록

baseline 원칙:

```text
clean working tree + HEAD commit hash = required baseline
```

gap은 evidence record입니다.

```md
## GAP-001 — Tooltip copy mismatch

Type: mismatch
Resolution: open

### Compared SOT
- Source: PRD
- Reference: https://...
- Section: Tooltip copy

### Compared Code
- Baseline: abc1234
- Files inspected:
  - src/...

### Evidence
SOT:
> short exact excerpt or pointer

Code:
> short exact excerpt or pointer

### Finding
PRD copy와 구현 tooltip copy가 다릅니다.

### Interpretation
implementation drift로 보입니다.

### Required Resolution
사용자 확인 또는 code update 필요.
```

하지 않는 일:

- gap을 실행 대기열로 변환
- ambiguity를 조용히 해소
- `DESIGN.md` 또는 `reuse-map.md` 업데이트
- 구현, commit, push, PR 생성

## 3. Reflection

```text
/tk:reflect
```

하는 일:

1. 현재 conversation/session review
2. `.tigerkit/requirements.md` review
3. `.tigerkit/gap.md` review
4. 최근 diff/commit review
5. durable learning과 one-off correction 분리
6. `.tigerkit/reflect.md` 갱신
7. `DESIGN.md`/`reuse-map.md` 업데이트 제안 또는 적용

reflect는 저장된 진행 상태에 의존하지 않습니다. session 전체를 재구성합니다.

## Evidence Rule

중요 claim은 아래 중 하나에 근거해야 합니다.

- external SOT reference
- direct user interview text
- code path
- commit hash
- observed diff
- explicit user confirmation
- gap record
- derived artifact clearly marked as derived

항상 분리합니다.

```text
Evidence = directly observed
Interpretation = inferred from evidence
Decision = confirmed by user or SOT
Suggestion = proposed, not confirmed
```

## Ambiguity Rule

source가 결론을 지지하지 않으면 추측하지 않습니다.

```text
record gap, not work plan
ask user, do not guess
```

## 검증

TigerKit 저장소에는 package manager 기반 build/test/lint 설정이 없습니다. 명령, manifest, eval fixture를 수정한 뒤에는 다음 검증을 기본으로 실행합니다.

```bash
claude plugin validate .claude-plugin/plugin.json
claude plugin validate .
python3 -m json.tool evals/evals.json >/dev/null
git diff --check
```

`evals/evals.json`은 자동 실행 테스트가 아니라 fixture입니다. JSON 문법 검증과 수동 기대 동작 검토만 의미합니다.
