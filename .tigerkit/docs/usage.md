# TigerKit 운영 사용법

이 문서는 TigerKit Slim command surface 사용 가이드입니다. 산출물 위치는 `.tigerkit/docs/artifact-layout.md`, 출력 규칙은 `.tigerkit/docs/output-contract.md`를 기준으로 봅니다.

## 언어

명령은 사용자에게 한글로 답하고 작업 산출물도 한글로 작성합니다. URL, 코드, 명령어, 경로, 식별자, commit hash, contract field name은 원문 그대로 유지할 수 있습니다.

## 핵심 모델

```text
TigerKit Slim = gap + grill + afk + reflect + setup
```

- `gap`: SoT와 Current Implementation의 차이를 한 번 분석합니다.
- `grill`: 설계, 계획, 변경안, reviewer 판단을 질문 렌즈로 압박 검증합니다.
- `afk`: 사용자에게 물어볼 decision point를 temporary Patron에게 위임합니다.
- `reflect`: 세션 learning과 개선 후보를 추출합니다.
- `setup`: setup, preferences, Patron, Vowline, recommended tools를 관리합니다.

Launch/workflow freezing/autopilot/mandatory runner 실험은 종료되었습니다.

## Command Surface

| Command | 역할 | 저장 성격 |
|---|---|---|
| `/tk:gap` | SoT와 Current를 비교해 missing, mismatch, overbuilt, ambiguous를 보고합니다. | optional generated report |
| `/tk:grill` | proposal/review context와 evidence를 비교해 닫힌 질문과 열린 질문을 분리합니다. | optional generated report |
| `/tk:afk` | temporary Patron에게 scoped decision을 위임하고 ledger를 남깁니다. | decision ledger |
| `/tk:reflect` | session result와 feedback에서 개선 후보를 추출합니다. | user/repo/Patron candidates |
| `/tk:setup` | setup, AFK default, Patrons, Vowline, recommended tools를 관리합니다. | user config |

## 사용 예시

```text
/tk:gap "PRD와 현재 구현 차이 봐줘" --target commands/gap.md
/tk:grill "이 계획 구멍 찾아줘" --target commands/grill.md
/tk:afk "검증 범위 결정 필요" --patron tester
/tk:reflect --dry-run
/tk:setup
/tk:setup afk status
/tk:setup patrons list
```

## `/tk:gap`

`/tk:gap`은 workflow generator가 아닙니다.

절차:

1. SoT refs와 access status를 고정합니다.
2. Current Implementation evidence를 확인합니다.
3. missing, mismatch, overbuilt, ambiguous를 분류합니다.
4. P0/P1/P2 finding만 Findings에 둡니다.
5. P3, duplicate, unverifiable, source conflict, missing evidence는 Ambiguities 또는 Not accepted summary에 둡니다.
6. Recommended Next Steps를 짧게 제시합니다.

## `/tk:grill`

`/tk:grill`은 workflow generator가 아닙니다.

절차:

1. Proposal과 target surface를 고정합니다.
2. repo rule, docs, current implementation evidence를 먼저 확인합니다.
3. 코드나 문서에서 답할 수 있는 질문은 Closed Questions에 둡니다.
4. owner decision이 필요한 질문은 Open Questions에 둡니다.
5. 필요한 경우 Patron candidate를 추천합니다.
6. reviewer loop에서 나온 질문은 confirmed defect가 아니라 review prompt로 취급합니다.

## `/tk:afk`

AFK는 current session decision delegation입니다.

- 기본 default는 off입니다.
- `/tk:afk` 명시 호출 시에만 켜집니다.
- Patron 선택은 phase가 아니라 question type 기준입니다.
- Patron output은 Driver가 merge합니다.
- Patron decision ledger는 reflect input이 됩니다.

## `/tk:reflect`

Reflect target policy:

| Target | Policy |
|---|---|
| repo `CLAUDE.local.md` | auto apply |
| repo `CLAUDE.md` | suggest only |
| user `PROFILE.md` | auto apply |
| user `CLAUDE.md` | auto apply |
| user skills | auto apply |
| Patron profiles | auto apply candidates or improvements |

## `/tk:setup`

`/tk:setup`은 askUserQuestion 기반 단계형 wizard와 management subcommands를 제공합니다.

First-use setup suggestion은 non-blocking이며 기본 선택은 “이번엔 그냥 진행”입니다.

Recommended tools는 기타 메뉴에서 사용자가 선택한 경우에만 보여줍니다.

## Deprecated commands

아래 command는 launch-era surface로 deprecated 처리되었고 active manifest에 포함되지 않습니다.

- `/tk:config`
- `/tk:launch`
- `/tk:review`
- `/tk:next`
- `/tk:handoff`
- `/tk:meta-feedback`

## Generated state

`.claude/tigerkit/`은 generated branch/workspace-local memory입니다. durable repo knowledge가 아닙니다.
