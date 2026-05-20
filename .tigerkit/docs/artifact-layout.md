# TigerKit 운영 산출물 구조

이 문서는 TigerKit 산출물 배치와 책임을 설명합니다. 사용 흐름은 `.tigerkit/docs/usage.md`, 출력 규칙은 `.tigerkit/docs/output-contract.md`를 기준으로 봅니다.

TigerKit은 절차 상태 파일에 의존하지 않습니다. 기본 산출물은 repo rule, gap/review 결과, reflection proposal, continuation handoff입니다.

## 기본 구조

```text
.claude/
  rules/
    **/*.md
  handoffs/
    current.md
    YYYY-MM-DD-task-name.md

.tigerkit/
  docs/
    usage.md
    artifact-layout.md
    output-contract.md
```

## 파일 책임

| 파일 | 역할 |
| --- | --- |
| `.claude/rules/**/*.md` | Repo convention basis used by `/tk:gap` and curated by `/tk:reflect`. |
| `.claude/handoffs/current.md` | Default continuation document written by `/tk:handoff`. |
| `.claude/handoffs/YYYY-MM-DD-task-name.md` | Optional archive copy when `/tk:handoff archive=true` is used. |
| `.tigerkit/docs/*.md` | TigerKit usage, artifact, and output contract documentation. |
| `CLAUDE.md` | Repo instruction and durable project guidance candidate for `/tk:reflect`. |

## 운영 메모

- `/tk:gap`은 기준자료와 대상 산출물의 비교 결과를 채팅에 출력합니다.
- `/tk:reflect`는 기본적으로 patch proposal만 출력하고, 승인된 경우에만 durable rule 파일을 수정합니다.
- `/tk:handoff`는 `current.md`를 갱신하고, archive 요청이 있을 때만 날짜가 포함된 사본을 만듭니다.
