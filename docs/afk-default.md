# AFK Default

AFK는 background async 작업이 아니다. 현재 세션에서 사용자에게 물어볼 의사결정을 Patron에게 위임하는 모드다.

## Default state

- 설치 직후 기본은 off다.
- `/tk:afk` 명시 호출 시에만 켜진다.
- `/tk:config afk default on|off|status`가 default 상태를 관리한다.
- config state가 source of truth다.
- user `CLAUDE.md` bridge는 activation aid다.
- 명시적 사용자 지시가 AFK default보다 우선한다.

## Config source of truth

권장 user-level config:

```text
~/.claude/tigerkit/config.json
```

예시:

```json
{
  "version": 1,
  "afk": {
    "default": "off"
  }
}
```

## Bridge policy

AFK default on은 user `CLAUDE.md`에 TigerKit managed bridge를 추가/갱신할 수 있다. Bridge는 config state를 대체하지 않는다.

```md
<!-- tiger-kit:start -->
## TigerKit

TigerKit user-level guidance lives here.
<!-- tiger-kit:end -->
```

## First-use suggestion

Config가 없을 때 첫 `tk:*` 사용 시 non-blocking 권유를 보여준다.

선택지:

- 지금 설정
- 이번엔 그냥 진행
- 오늘은 묻지 않기
- 다시 묻지 않기

기본 선택은 “이번엔 그냥 진행”이다. 스킬 실행을 막지 않는다.
