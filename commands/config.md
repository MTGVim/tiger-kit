---
description: Deprecated. TigerKit Slim에서 /tk:config는 active command surface가 아닙니다.
argument-hint: ""
---

`/tk:config`는 TigerKit Slim active command surface에서 제거된 deprecated command입니다.

현재 setup과 management 기능은 `/tk:setup`이 단독으로 담당합니다. 이전 `/tk:config ...` 표현은 같은 하위 동작을 `/tk:setup ...`으로 옮겨 사용합니다.

```text
/tk:setup
/tk:setup show
/tk:setup vowline on
/tk:setup vowline off
/tk:setup patrons list
/tk:setup patrons install <id>
/tk:setup patrons enable <id>
/tk:setup patrons disable <id>
/tk:setup afk default on
/tk:setup afk default off
/tk:setup afk status
/tk:setup reflect show
/tk:setup reset
```

`commands/config.md`는 migration 안내를 위해 남아 있지만 `.claude-plugin/plugin.json` active manifest에 등록하지 않습니다.
