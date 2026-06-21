# TigerKit 운영 사용법

이 문서는 TigerKit command surface 사용 가이드입니다. 산출물 위치는 `.tigerkit/docs/artifact-layout.md`, 출력 규칙은 `.tigerkit/docs/output-contract.md`를 기준으로 봅니다.

## 언어

명령은 사용자에게 한글로 답하고 작업 산출물도 한글로 작성합니다. URL, 코드, 명령어, 경로, 식별자, commit hash, contract field name은 원문 그대로 유지할 수 있습니다.

## 핵심 모델

```text
TigerKit = gap + reflect
```

- `gap`: SoT와 Current Implementation의 차이를 한 번 분석합니다. evidence-first로 읽고, source conflict나 근거 부족은 `ambiguous`로 남깁니다.
- `reflect`: 세션 result와 feedback에서 재사용 가능한 learning을 추출합니다.

## Core guidance

- SoT가 있으면 구현 전에 `/tk:gap`을 먼저 고려합니다.
- SoT가 없으면 먼저 SoT 제공을 제안합니다.
- 사용자가 바로 진행을 원하면 `/tk:gap` 없이 진행할 수 있지만, 그 경우 가정과 불확실성을 명시합니다.
- 의미 있는 작업이 끝나면 `/tk:reflect`를 고려합니다.

## Command Surface

| Command | 역할 | 저장 성격 |
|---|---|---|
| `/tk:gap` | SoT와 Current를 비교해 missing, mismatch, overbuilt, ambiguous를 보고합니다. | optional external generated report |
| `/tk:reflect` | session result와 feedback에서 개선 후보를 추출합니다. | user/repo candidates |

## 사용 예시

```text
/tk:gap "PRD와 현재 구현 차이 봐줘" --target src/auth
/tk:reflect --dry-run
```

## Generated state

Active TigerKit generated state는 project repository 밖 `~/.tigerkit/` 아래의 file-only state입니다. `.claude/tigerkit/`는 legacy/migration context로만 남기고 새 runtime write path로 사용하지 않습니다.

주요 active path:

```text
~/.tigerkit/local/session-start/worktree-context-declines.json
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/<GAP-ID>.md
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/current.md
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/branch-state.json
```
