# Reflect promotion helper guide

이 문서는 `/tk:reflect` promotion router 결과를 검토할 때 참고할 수 있는 선택형 helper guide다.

## Status

- Optional helper document
- Non-authoritative for runtime behavior
- Not a command, hook, agent, generator, installer, or generated artifact layout
- Not a replacement for `commands/reflect.md`, `.tigerkit/docs/output-contract.md`, `docs/reflect-file-policy.md`, or `.tigerkit/docs/storage-boundary.md`

이 문서의 예시는 후보를 더 잘 읽고 검토하기 위한 설명이다. 예시가 있다고 해서 hook 설치, settings 수정, command 생성, agent 생성, user skill 생성, plugin manifest 수정, runtime generation이 발생하지 않는다.

## When this guide helps

이 문서는 다음 상황에서만 참고한다.

- `/tk:reflect` receipt에 hook / hookify proposal이 나왔고, 사용자가 후속 검토를 원할 때
- promotion 후보가 rule, skill, hook, command, agent 중 어디에 가까운지 다시 판단할 때
- `.claude/tigerkit/` receipt와 실제 durable target의 역할을 구분해야 할 때
- 제안 문구가 설치됨/활성화됨처럼 과장됐는지 점검할 때

## Promotion target quick guide

| Target | Good fit | Boundary |
|---|---|---|
| repo `CLAUDE.local.md` | 이 repo에만 필요한 local/private guidance | repo shared rule처럼 포장하지 않는다 |
| repo `CLAUDE.md` proposal | 팀이 공유할 repo-wide rule 후보 | suggest-only, 직접 수정 금지 |
| user `PROFILE.md` | 사용자 역할, 협업 방식, 선호 | 불필요한 개인 정보 저장 금지 |
| user `CLAUDE.md` | 여러 repo에 적용되는 user-level guidance | repo-specific one-off 승격 금지 |
| user skills | 반복 가능한 multi-step routine | canonical source는 user skill surface가 소유하며 `.claude/tigerkit/`에 생성/복제하지 않는다 |
| hook / hookify proposal | 반복 누락을 trigger 기반으로 경고/차단/기록할 수 있는 후보 | suggest-only, 설치됨/활성화됨 표현 금지 |
| command proposal | 사용자가 명시적으로 호출할 slash workflow 후보 | command 파일 또는 manifest 생성 금지 |
| agent proposal | 독립 역할, 병렬 조사, 전문 판단이 필요한 후보 | 자동 dispatch 또는 orchestration runtime 생성 금지 |
| discard | branch-specific one-off, 저신뢰, 민감 정보, 중복 | durable surface에 저장하지 않는다 |

## Optional hookify guidance

Hook / hookify proposal은 자동 적용 대상이 아니다. 후보는 아래 조건을 모두 만족할 때만 제안으로 남긴다.

1. 반복되는 실수나 누락이 있다.
2. trigger를 tool event, path, command, prompt pattern 같은 표면에서 설명할 수 있다.
3. action이 warning, reminder, check, block 중 무엇인지 분명하다.
4. false positive risk와 사용자 검토 필요성이 적혀 있다.
5. destructive action, credential handling, external side effect를 자동화하지 않는다.

권장 receipt shape:

```text
## Hook / Hookify proposal 후보
1. <candidate title>
- rationale: <어떤 반복 문제를 줄이는지>
- trigger: <언제 실행되는지>
- action: <무엇을 경고/검사/차단/기록하는지>
- why suggest-only: <왜 설치/활성화 전 사용자 검토가 필요한지>
```

금지 표현:

- hook installed
- hook active
- settings updated
- 자동 적용됨
- 다음부터 반드시 실행됨

허용 표현:

- hook / hookify proposal
- suggest-only
- optional follow-up
- user review required before install

## Promotion receipt and `.claude/tigerkit/`

`.claude/tigerkit/`은 branch/workspace-local generated state 영역이다. 현재 helper guide는 reflect artifact write path를 선언하지 않는다.

Receipt가 기록할 수 있는 것:

- source session summary
- promotion candidate list
- target classification
- applied / suggest-only / discard result
- changed paths when files were written
- durable target path 또는 follow-up proposal pointer

Receipt가 canonical source가 되면 안 되는 것:

- repo shared policy 본문
- user-global guidance 본문
- skill canonical source 복제본
- installed hook config
- generated command or agent source
- source code or product artifact

즉 receipt는 “무엇이 어디로 갔는지”를 남긴다. “그 표면 자체”를 소유하지 않는다.

## Review checklist

Reflect promotion 결과를 볼 때는 아래를 확인한다.

1. 후보가 정확히 하나의 target으로 분류됐는가?
2. shared repo rule 후보가 suggest-only로 남았는가?
3. user skill 후보가 `.claude/tigerkit/` generated source처럼 표현되지 않았는가?
4. hook / hookify, command, agent 후보가 설치됨/활성화됨으로 표현되지 않았는가?
5. 파일을 쓴 경우 changed path가 출력됐는가?
6. `.claude/tigerkit/` receipt가 canonical durable target처럼 설명되지 않았는가?
7. branch-specific one-off, 저신뢰, 민감 정보, 중복 후보가 discard됐는가?
8. 사용자가 직접 검토해야 할 optional follow-up이 분명한가?

## Bottom line

이 문서는 `/tk:reflect` 결과를 읽는 보조 설명서다. TigerKit runtime behavior는 command contract와 output/file policy가 정하고, optional helper docs는 그 contract를 실행하거나 확장하지 않는다.
