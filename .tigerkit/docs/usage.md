# TigerKit 운영 사용법

이 문서는 `.tigerkit/docs/` 아래 TigerKit 사용 가이드입니다. 산출물 위치는 `.tigerkit/docs/artifact-layout.md`, 출력 규칙은 `.tigerkit/docs/output-contract.md`를 기준으로 봅니다.

## 언어

명령은 사용자에게 한글로 답하고 작업 산출물도 한글로 작성합니다. URL, 코드, 명령어, 경로, 식별자, commit hash는 원문 그대로 유지할 수 있습니다.

## 핵심 모델

```text
TigerKit = basis gap analysis + durable reflection + safe handoff
```

TigerKit은 요구사항을 재작성하거나 실행 대기열을 관리하지 않습니다. 기준자료와 대상 산출물을 비교하고, 반복되는 피드백을 repo 규칙 후보로 제안하며, 다음 세션이 안전하게 이어받을 문맥을 남깁니다.

## Command Surface

Plugin namespace는 `/tk:*`입니다. 해당 workflow를 명시한 자연어 요청은 대응하는 `/tk:*` command contract로 처리합니다.

| Command | 역할 |
| --- | --- |
| `/tk:gap` | 기준자료와 대상 산출물을 비교해 gap analysis 또는 PR-ready review comment를 만듭니다. |
| `/tk:reflect` | durable feedback, 반복 실수, gap/review 결과에서 `CLAUDE.md`와 `.claude/rules/*` 업데이트 후보를 제안합니다. |
| `/tk:handoff` | 다음 세션이 이어받을 수 있도록 `.claude/handoffs/current.md`를 작성합니다. |

## 사용 예시

```text
/tk:gap spec <url> vs current implementation
/tk:gap pr #123 mode=review
/tk:gap figma <url> vs pr #123 mode=both
/tk:reflect gap 결과에서 반복되는 리뷰 포인트를 rules로 제안해줘
/tk:reflect apply=true 이 copy rule을 반영해줘
/tk:handoff 현재 작업 이어받을 수 있게 남겨줘
/tk:handoff tiger-kit skill refactor archive=true
```

## Command notes

### `/tk:gap`

- 입력된 기준자료와 대상 산출물을 직접 확인 가능한 근거로 비교합니다.
- `mode=analysis`는 gap analysis를 출력합니다.
- `mode=review`는 PR-ready review comment만 출력합니다.
- `mode=both`는 analysis 뒤에 review comment를 출력합니다.
- 근거가 부족하면 확인 불가로 남기고 추측으로 채우지 않습니다.

### `/tk:reflect`

- durable하게 남길 만한 피드백, 반복 실수, gap/review finding을 분류합니다.
- 기본은 제안만 합니다.
- `apply=true` 또는 명시 승인 없이는 파일을 수정하지 않습니다.

### `/tk:handoff`

- 기본 출력 대상은 `.claude/handoffs/current.md`입니다.
- `archive=true` 또는 명시 요청이 있을 때만 dated archive copy를 만듭니다.
- handoff에는 Reader Guide와 Resume Prompt를 포함합니다.

## 운영 범위 메모

세부 정책, 우선순위 규칙, 검증 원칙은 `CLAUDE.md`를 기준으로 봅니다.
