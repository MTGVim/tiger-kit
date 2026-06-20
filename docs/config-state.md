# Config State

TigerKit Slim config state가 AFK default, Patron preset, Vowline bridge, reflect policy의 source of truth다.

## User-level state

권장 위치:

```text
~/.claude/tigerkit/config.json
```

## Schema

```json
{
  "version": 1,
  "afk": { "default": "off" },
  "vowline": { "enabled": false },
  "patrons": {
    "preset": "minimal",
    "enabled": ["reviewer", "tester", "security"],
    "installed": []
  },
  "reflect": {
    "repo_auto_write": ["CLAUDE.local.md"],
    "repo_suggest_only": ["CLAUDE.md"],
    "user_auto_apply": ["PROFILE.md", "CLAUDE.md", "skills"]
  },
  "recommended_tools": { "shown": false }
}
```

## Bridge files

User `CLAUDE.md` bridge는 activation aid다. Config state를 대체하지 않는다.

## Reset

`/tk:setup reset`은 config state 초기화다. Bridge block 제거는 사용자 확인 후 수행한다.
