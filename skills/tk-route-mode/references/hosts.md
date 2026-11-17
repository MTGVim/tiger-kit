# 호스트별 출발점

2026-11-17 사용자 제공 조사 자료의 요약입니다. 현재 호스트 문서와 도구 스키마로 다시 확인한 뒤 적용합니다.

| 호스트 | 설정 위치 | 모델 및 effort | 주의 사항 |
|---|---|---|---|
| Claude Code | `~/.claude/agents/tier-<티어>.md` | frontmatter `model`, `effort` | 호출 인자 및 `CLAUDE_CODE_SUBAGENT_MODEL_FORCE`, `CLAUDE_CODE_EFFORT_LEVEL`의 우선순위를 확인합니다. |
| Codex | `~/.codex/agents/tier-<티어>.toml` | `model`, `model_reasoning_effort` | 에이전트 파일, 호출값, 기본값과 부모 세션의 우선순위를 확인합니다. 스킬 자체의 모델 지정과 혼동하지 않습니다. |
| Hermes | 활성 Hermes 프로필의 `config.yaml` 아래 `delegation.backends.model_map.options` | `name`, `description`, `provider`, `model`, `reasoning_effort` | [Hermes 전용 설정·검증](hermes-setup.md)에 따라 0.22.5 이상·프로필별 설치·`hermes delegation config`·새 CLI 세션·`delegate_task.option`과 결과 route를 확인합니다. |

출처: [Claude Code subagents](https://code.claude.com/docs/en/sub-agents), [model configuration](https://code.claude.com/docs/en/model-config), [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [Hermes advanced delegation](https://hermes-agent.nousresearch.com/docs/plugins/advanced-delegation).

사용자 제공 Claude Code 실험에서는 파일 변경 직후 같은 턴의 위임에 이전 정의가 사용됐으며, /reload-plugins 뒤 새 값이 반영됐습니다. 세션의 subagents/agent-<id>.jsonl에서 assistant의 message.model과 effort, .meta.json의 agentType을 대조했습니다. 이번 저장소 변경에서는 호스트별 실행을 재현하지 않았습니다. 같은 방법이 현재 호스트에서도 유효한지 확인합니다.

선택 이름은 tier-light, tier-standard, tier-top이며 Hermes의 선택지형 호스트는 light, standard, top을 사용합니다. 지원되지 않는 effort는 unverified로 남깁니다.

## Codex의 프로필 로드와 실제 선택

[Codex subagents 공식 문서](https://learn.chatgpt.com/docs/agent-configuration/subagents)에 따르면 사용자 custom agent는 `~/.codex/agents/`의 standalone TOML 파일로 정의할 수 있습니다. 필수 키는 `name`, `description`, `developer_instructions`이며 모델과 effort는 `model`, `model_reasoning_effort`를 사용합니다. 이름의 정본은 `name`입니다. 파일에 지정한 모델과 effort의 우선순위 및 지원 범위를 현재 문서와 대조합니다.

현재 호출 도구의 스키마에 이름 선택 인자가 없다는 사실과 호스트 전체의 custom agent 지원 여부는 별개입니다. 먼저 실제 클라이언트 버전과 현재 문서로 지원 여부를 확인합니다. 파일 작성·TOML 검사, 세션의 agent_type 목록 등 로드 증거, 이름을 선택한 실제 위임 실행과 호스트 기록을 따로 확인합니다. 파일이나 목록만으로 실행을 검증했다고 보고하지 않습니다. 현재 세션에서 이름이 보이지 않으면 새 세션이나 확인된 reload 후 다시 확인하고, 그래도 선택 또는 실효값 확인이 불가능하면 unverified로 둡니다. 사용자 수준 지침의 실제 로드 여부와 동등한 티어 선택 규칙도 검사합니다.

## Codex 모델 카탈로그 대조

[Codex App Server 공식 `model/list`](https://learn.chatgpt.com/docs/app-server)은 현재 인증·공급자에 따라 `model`, `id`, `supportedReasoningEfforts`, `hidden`을 반환합니다. 상태 조회에서 이 목록을 **읽기 전용**으로 확인합니다. 모델 ID가 목록에 존재한다는 사실과 실제 위임 실행 성공은 별도 결과입니다.

1. 현재 사용 중인 Codex 계정·공급자 및 `CODEX_HOME`(또는 기본 사용자 설정 위치)을 확인합니다. 활성 대응표의 OpenAI light/standard/top 값과 `agents/tier-light.toml`, `agents/tier-standard.toml`, `agents/tier-top.toml`에 실제로 저장된 `model` 및 `model_reasoning_effort`를 원본 변경 없이 확인합니다. 파일이 없거나 다른 이름의 agent라면 해당 사실을 표시하며 임의로 생성하지 않습니다. 비밀 파일과 인증 값은 출력하지 않습니다.
2. 현재 활성 Codex App Server의 `model/list`를 호출합니다. `includeHidden: true`로 숨김 모델도 포함하고 `nextCursor`가 없어질 때까지 모든 페이지를 조회합니다. 별도 공급자를 사용하는 경우 현재 설정에 맞는 `modelProvider`를 사용합니다. 인증·provider 오류, 부분 페이지만 성공, 호스트 조회 기능 부재는 `unverified`로 표시합니다. 별도 작업 스레드나 추론 요청은 만들지 않습니다.
3. 대응표와 agent에 저장된 각 모델 값은 카탈로그 항목의 **`model` 문자열과 문자 단위로 정확히 비교**합니다. `id` 또는 `displayName`을 `model`의 대용으로 사용하지 않습니다. `luna`와 `gpt-6-luna`, `terra`와 `gpt-6.1-terra`처럼 의미가 유사한 값은 명시적으로 검증된 매핑이 없다면 `alias-unresolved`입니다. 실제 agent TOML에 있는 정확한 ID가 일치한다면 원래 대응표 별칭 및 agent ID를 각각 표시합니다.
4. 일치한 모델은 `supportedReasoningEfforts`에서 해당 effort를 확인해 `supported`·`not-listed`·`unverified`로 분류합니다. 전체 카탈로그에 정확한 모델이 없으면 `not-listed`로 표시합니다. 수동 입력한 모델 ID는 목록에 없더라도 실행될 수 있으므로 `not-listed`는 `invalid`나 `unavailable`을 의미하지 않습니다. effort 정보가 없는 경우에도 추측하지 않습니다.
5. 세 티어마다 `대응표 모델/effort | Codex agent 모델/effort | 정확한 모델 ID 목록 결과 | effort 목록 결과 | 실제 위임 기록`을 보고합니다. 카탈로그 대조만으로 마지막 열을 `verified`로 만들지 않습니다. 인증 오류, 설정과 실제 agent 파일의 불일치도 한 번에 보고하며 수정 전에 승인을 받습니다.

OpenAI 공용 API의 `/v1/models`, `codex debug models --bundled`, 저장된 `models_cache.json`, CLI의 `/model` 표시 목록은 **현재 계정의 완전한 실효 모델 목록**을 대신하지 못할 수 있습니다. 해당 결과를 현재 Codex의 모델 지원 증거로 대체하거나 `codex models list`와 같은 미확인 명령을 가정하지 않습니다. 조회가 불가능하면 이유와 `unverified`를 명시합니다.


Hermes의 `model_map`에는 위임 대상 이름을 `option`으로, `profile_routes`에는 `profile`로 전달합니다. 현 연동 도구의 스키마 제한과 Hermes CLI의 기능 지원은 분리합니다. 현재 세션에 옛 스키마가 남아 있으면 새 세션으로 확인합니다.
