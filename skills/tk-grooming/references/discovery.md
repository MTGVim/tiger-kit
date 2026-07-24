# 탐색 후보

저장소 규칙에는 root 또는 중첩 `AGENTS.md`, `CLAUDE.md`, `CLAUDE.local.md`, `.claude/rules/**/*.md`, `SOUL.md`, 실제 host-native 저장소 지침이 포함될 수 있습니다. 저장소 스킬은 `.agents/skills/`, `.claude/skills/` 또는 `.hermes/skills/`에 있을 수 있습니다. 사용자 스킬은 호스트의 `.agents`, `.claude`, `.codex` 또는 `.hermes` 스킬 디렉터리 아래에 있을 수 있습니다. 현재 host를 실제 경로나 host discovery evidence로 식별하고 그 host의 native target만 해석하세요. Host를 식별할 수 없으면 target을 발명하지 말고 `Unverifiable`로 남기세요. 한 host 전용 위치를 다른 host에 강제하거나 여러 host로 fan-out/sync하지 마세요. 공유 repo rule은 사용자가 지정했거나 tracked shared instruction file로 발견된 경우에만 후보로 삼고, `.tigerkit/`을 영구 장부로 사용하지 마세요.
