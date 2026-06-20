# Vowline Integration

Vowline은 TigerKit 필수 의존성이 아니다.

## Policy

- Vowline을 TigerKit core skill로 fork/reimplement하지 않는다.
- `/tk:setup`에서 opt-in으로 연결한다.
- TigerKit managed block과 Vowline block은 독립적으로 관리한다.
- Vowline enable/disable은 `/tk:setup vowline on|off`에서 지원한다.
- TigerKit은 Vowline skill을 자동 설치하지 않는다.
- `vowline` skill이 이미 사용 가능할 때만 bridge를 쓴다.
- skill이 없으면 config state를 enable로 확정하지 않고 설치 안내만 한다.

## Blocks

TigerKit block:

```md
<!-- tiger-kit:start -->
## TigerKit

TigerKit user-level guidance lives here.
<!-- tiger-kit:end -->
```

Vowline block:

```md
<!-- vowline:start -->
Always use the skill `vowline` consistently, including for all sub-agents.
<!-- vowline:end -->
```

## Enable

`/tk:setup vowline on` 흐름:

1. `vowline` skill이 사용 가능한지 확인한다.
2. 없으면 아래 설치 안내만 보여주고 상태를 pending으로 둔다.
3. 설치가 확인된 뒤에만 user `CLAUDE.md`에 Vowline block 추가/갱신을 제안하고 승인 후 적용한다.

설치 안내 문구:

```text
Vowline skill이 아직 설치되어 있지 않습니다.

Install Vowline for yourself by following:
https://github.com/chojondocho/vowline/blob/main/INSTALL.md

Verify installation, then run `/tk:setup vowline on` again.
```

## Disable

`/tk:setup vowline off`는 config state를 disabled로 갱신한다. Block 제거 또는 비활성 문구 변경은 사용자 확인 후 수행한다.

## Boundary

Vowline이 없어도 `/tk:gap`, `/tk:afk`, `/tk:reflect`, `/tk:setup` core 기능은 동작해야 한다.
