# TigerKit 운영 Output Contract

이 문서는 TigerKit Slim command의 출력 계약을 정의합니다.

## 공통 원칙

- 사용자-facing label은 한글로 씁니다.
- 코드, path, URL, identifier, status code, field name은 원문을 유지할 수 있습니다.
- Evidence, Interpretation, Decision, Suggestion을 구분합니다.
- 검증하지 않은 success를 선언하지 않습니다.
- command가 파일을 쓰면 path를 출력합니다.

## `/tk:gap` Output Contract

`/tk:gap`은 SoT와 Current Implementation의 one-shot gap analysis입니다.

기본 stdout/report shape:

```md
## Gap Summary

| Area | SoT | Current | Gap | Impact | Priority |
|---|---|---|---|---|---|

## Findings

### 1. <finding title>
- SoT:
- Current:
- Evidence:
- Impact:
- Priority:
- Suggested fix:

## Ambiguities / Missing Evidence

| Ref | Question | Evidence checked | Impact | Recommendation |
|---|---|---|---|---|

## Recommended Next Steps

1. <next step>
```

Gap values:

- `missing`
- `mismatch`
- `overbuilt`
- `ambiguous`

Priority values:

- `P0`
- `P1`
- `P2`
- `P3`

Findings에는 P0/P1/P2만 둡니다. P3, duplicate, unverifiable, source conflict, missing evidence는 Ambiguities 또는 Not accepted summary에 둡니다.

`/tk:gap`은 아래를 출력하거나 생성하지 않습니다.

- `GAP_READY`
- `GAP_AUTO_LAUNCHED`
- sealed workflow
- workflow hash
- `tigerkit-launch-workflow`
- launch next action
- autopilot policy
- runner/advisor receipt

## `/tk:grill` Output Contract

`/tk:grill`은 설계, 계획, 변경안, reviewer 판단을 압박 검증하는 optional active command입니다.

기본 stdout/report shape:

```md
## Grill Summary

| Area | Proposal | Evidence checked | Risk | Question | Recommendation |
|---|---|---|---|---|---|

## Closed Questions

| Question | Answer | Evidence |
|---|---|---|

## Open Questions

### 1. <question title>
- Type:
- Evidence checked:
- Why it matters:
- Recommendation:
- Patron candidate: <none|reviewer|tester|security|webperf|steward|simplifier|cartographer>

## Recommended Next Steps

1. <next step>
```

`/tk:grill` output은 confirmed defect가 아니라 질문/리스크 목록입니다. PR comment나 reviewer verdict로 승격하려면 direct evidence와 required change를 다시 확인해야 합니다.

## `/tk:afk` Output Contract

```text
AFK 결정 위임 완료: <DEC-ID>
Patron: <id>
결정: <selected|blocked>
근거: <한글 1-3줄>
Ledger: .claude/tigerkit/branches/<scope-key>/afk/decisions/<DEC-ID>.md
다음 행동: <driver next step>
```

Decision ledger는 아래 schema를 따른다.

```yaml
decision:
  topic: <topic>
trigger:
  - <delegation reason>
patron:
  id: <id>
  source: source-derived | tigerkit-native
  mode: primary | fanout
  temporary: true
context:
  constraints: []
  evidence: []
options:
  - id: A
    summary: <option>
decision_result: <selected or blocked>
rationale: []
confidence: low | medium | high
follow_up: []
```

## `/tk:reflect` Output Contract

```text
Reflect 완료
적용 대상:
- repo CLAUDE.local.md: <applied|not_applicable>
- repo CLAUDE.md: suggest_only:<count>
- user PROFILE.md: <applied|not_applicable>
- user CLAUDE.md: <applied|not_applicable>
- user skills: <applied|not_applicable>
- Patron profiles: <candidate_count>

## Repo 후보
n. <candidate or NONE>

## User 후보
n. <candidate or NONE>

## Patron 후보
n. <candidate or NONE>

## 충돌 / 적용 조건
- <condition or none>

## 다음 행동
- <next step or 없음>
```

`--dry-run` 또는 `--apply=false`이면 preview만 출력하고 파일을 수정하지 않습니다.

## `/tk:config` Output Contract

`/tk:config`는 단계형 wizard 또는 subcommand receipt를 출력합니다.

Subcommand receipt:

```text
Config 완료
명령: <subcommand>
Config state: ~/.claude/tigerkit/config.json
변경: <changed|unchanged>
Bridge: <updated|not_changed|approval_required|not_applicable>
다음 행동: <next step or 없음>
```

First-use suggestion은 non-blocking입니다.

선택지:

- 지금 설정
- 이번엔 그냥 진행
- 오늘은 묻지 않기
- 다시 묻지 않기

기본 선택은 “이번엔 그냥 진행”입니다.

## Deprecated output surfaces

아래 status/output surfaces는 Slim active flow에서 새로 생성하지 않습니다.

- `GAP_READY`
- `GAP_BLOCKED` as workflow readiness status
- `GAP_AUTO_LAUNCHED`
- `SUCCESS`/`ABORTED` launch receipts
- `REVIEW_PASS`, `REVIEW_PARTIAL`, `REVIEW_FAIL`, `REVIEW_BLOCKED`
- `NEXT_DONE`, `NEXT_PARTIAL`, `NEXT_BLOCKED`, `NEXT_SKIPPED`
- handoff receipt
- meta-feedback privacy gate receipt
