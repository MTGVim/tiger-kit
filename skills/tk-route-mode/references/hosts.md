# 호스트별 출발점

2026-11-17 사용자 제공 조사 자료의 요약입니다. 현재 호스트 문서와 도구 스키마로 다시 확인한 뒤 적용합니다.

| 호스트 | 설정 위치 | 모델 및 effort | 주의 사항 |
|---|---|---|---|
| Claude Code | `~/.claude/agents/tier-<티어>.md` | frontmatter `model`, `effort` | 호출 인자 및 `CLAUDE_CODE_SUBAGENT_MODEL_FORCE`, `CLAUDE_CODE_EFFORT_LEVEL`의 우선순위를 확인합니다. |
| Codex | `~/.codex/agents/tier-<티어>.toml` | `model`, `model_reasoning_effort` | 에이전트 파일, 호출값, 기본값과 부모 세션의 우선순위를 확인합니다. 스킬 자체의 모델 지정과 혼동하지 않습니다. |
| Hermes | `config.yaml`의 `delegation.backends.model_map.options` | `model`, `provider`, `reasoning_effort` | advanced-delegation 및 `delegation.backend: model_map`의 실제 지원과 활성화를 확인합니다. |

출처: [Claude Code subagents](https://code.claude.com/docs/en/sub-agents), [model configuration](https://code.claude.com/docs/en/model-config), [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [Hermes advanced delegation](https://hermes-agent.nousresearch.com/docs/plugins/advanced-delegation).

사용자 제공 Claude Code 실험에서는 파일 변경 직후 같은 턴의 위임에 이전 정의가 사용됐으며, /reload-plugins 뒤 새 값이 반영됐습니다. 세션의 subagents/agent-<id>.jsonl에서 assistant의 message.model과 effort, .meta.json의 agentType을 대조했습니다. 이번 저장소 변경에서는 호스트별 실행을 재현하지 않았습니다. 같은 방법이 현재 호스트에서도 유효한지 확인합니다.

선택 이름은 tier-light, tier-standard, tier-top이며 Hermes의 선택지형 호스트는 light, standard, top을 사용합니다. 지원되지 않는 effort는 unverified로 남깁니다.
