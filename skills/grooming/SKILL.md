---
name: grooming
description: guidance 정비 트리거입니다.
---

# Grooming

guidance 파일(`CLAUDE.md`, `.claude/rules/**`)이 쌓이면서 생기는 오염, 충돌, 죽은 참조, 사실 부정확을 평가하고 정비하는 skill입니다.

## Goal

- guidance drift를 report-first로 드러냅니다.
- 승인된 범위만 apply합니다.
- user-global만 direct apply하고 repo 쪽은 suggestion-only로 유지합니다.
- 적용 후에는 readback / re-grep 같은 검증 근거를 남깁니다.

## Scope

지원 scope는 `user | repo | all`입니다.

- `user`: `~/.claude/CLAUDE.md`, `~/.claude/rules/<rule-name>/CLAUDE.md`
- `repo`: `<repo>/CLAUDE.md`, `<repo>/CLAUDE.local.md`, `<repo>/.claude/rules/**`
- `all`: user + 현재 repo에서 실행 중이면 repo까지 포함

기본값은 `user`입니다.

## Process

### Phase 1: 평가 (report-only 기본)

1. 원본 파일을 직접 읽습니다.
2. 아래 문제 클래스를 탐지합니다.
   - 위치 오염
   - 자기모순
   - 죽은 참조
   - 실효성 없는 룰
   - 사실 부정확
   - 방어적 반복
   - 추가 제안 후보
3. 결론 / 근거 / 후속 액션 형태로 보고합니다.
4. 승인 전에는 write하지 않습니다.

### Phase 2: 승인 후 apply

1. direct apply 후보와 suggestion-only 후보를 분리합니다.
2. direct apply는 `user-global` exact target이 확정된 변경만 허용합니다.
3. repo shared / repo local guidance는 항상 suggestion-only입니다.
4. user-global direct apply와 repo suggestion-only가 한 변경 안에 섞이면 partial apply를 하지 않고 preview-only로 남깁니다.
5. apply 뒤에는 readback 또는 re-grep로 결과를 검증합니다.

## Direct-apply boundary

직접 쓸 수 있는 대상은 user-global guidance뿐입니다.

```text
~/.claude/CLAUDE.md
~/.claude/rules/<rule-name>/CLAUDE.md
```

원칙:
- exact target이 확정되지 않으면 direct apply하지 않습니다.
- repo의 `CLAUDE.md`, `CLAUDE.local.md`, `.claude/rules/**`는 전부 suggestion-only입니다.
- mixed-scope change는 preview-only입니다.

## Protected exclusions

기본 보호 대상:
- 역사 기록물: branch spec snapshot, `*.original.md`, transcript/history
- 서드파티 관리 블록: `CODEGRAPH_START`, `vowline:start` 같은 marker block
- TigerKit 관리 섹션: 죽은 참조 제거 등 최소 수정만 허용
- import(`@...`) 및 plugin 주입 블록: 명시 요청이 없으면 범위 밖

## Role split

- grooming: 기존 guidance의 이동·병합·교정·삭제·죽은 참조 정리 제안 / 제한된 apply
- reflect: 세션 결과에서 durable learning 분류
- learn: reusable skill 생성

새 guidance 후보는 grooming이 직접 추가하지 않고 reflect/learn으로 넘깁니다.

## Verification

- report-only면 preview-only 사유가 분명해야 합니다.
- user-global apply면 exact target path와 readback 근거가 남아야 합니다.
- repo suggestion-only면 suggestion 대상과 보호 대상 제외 이유가 남아야 합니다.
