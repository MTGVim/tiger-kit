# Hermes 모델 경로 위임 설정·실행 검증

이 문서는 `tk-route-mode`가 Hermes Agent에 model_map 티어를 적용하거나 검증할 때 사용합니다. [Hermes Advanced Delegation](https://github.com/NousResearch/hermes-official-plugins/blob/main/advanced-delegation/README.md)과 [Subagent Delegation](https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation)을 참고합니다. 사용자 제공 2026-11-18 실행 결과는 다른 호스트에서의 재현 근거가 아닙니다.

## 적용 전 확인

1. 위임을 **시작하는 Hermes 프로필**과 설치 버전을 확인합니다. `advanced-delegation`은 Hermes **0.22.5 이상**이 필요하며, 설치는 프로필별로 관리합니다. 현재 위임 프로필이 다르면 그 프로필에도 확인이 필요합니다. 타 프로필의 설정을 자동 수정하지 않습니다.
2. 정확한 프로필·기존 backend·세 경로·인증된 provider 및 실제 모델 ID를 조사하고, 비밀 없는 변경 계획·백업·복원을 한 번 승인받습니다. 플러그인 설치·설정 편집은 쓰기 작업입니다.
3. 호스트가 제공하는 config 명령을 사용합니다. 기본적으로 `config.yaml`을 임의 직접 편집하거나 자격 증명을 YAML에 삽입하지 않습니다. 확인된 인증 provider를 사용합니다.

```bash
hermes --version
hermes profile list
hermes plugins install advanced-delegation
hermes delegation config
hermes delegation config --show
```

위 설치와 편집 명령은 사전 승인 후 대상 Hermes 프로필에서 실행합니다. `hermes delegation config`에서 **Model routes** (`delegation.backend: model_map`)를 선택하고 각 route의 `name`, `description`, `provider`, `model`, `reasoning_effort`를 설정합니다. Hermes 모델 선택기에서 현재 공급자, 모델 및 effort의 지원을 확인합니다.

| `option` | 역할 | 사용자 검증 사례의 실제 모델 | effort |
| --- | --- | --- | --- |
| `light` | 사실 수집·분류·기계적 검사 | `gpt-6-luna` | `low` |
| `standard` | 구현·독립 리뷰 | `gpt-6.1-terra` | `low` |
| `top` | 아키텍처·미지 문제 조사 | `gpt-6.1-sol` | `medium` |

이는 2026-11-18 사용자가 **새 Hermes CLI 세션에서 검증했다고 보고한 설정**의 예시입니다. 모든 사용자에게 강제할 모델 맵이 아닙니다. 실제 적용 대상은 현재 `tk-route-mode` 단일 대응표와 기존 사용자 override로 결정합니다. 공급자 문자열을 예시에서 추측하지 말고 현재 Hermes 프로필의 유효한 선택기를 사용합니다. 새 기본 맵의 OpenAI top은 `gpt-6.2-sol` / `medium`입니다. 표의 `gpt-6.1-sol`은 이전 세션에서 검증한 사례이며 새 기본 권장이 아닙니다. 모델 변경은 호스트가 정확한 ID와 effort를 지원하는지 확인하고 승인받아야 합니다. 판단 근거는 [모델 검토](model-review-2026-11-18.md)를 따릅니다.

`model_map`은 개별 `delegate_task` 항목의 `option`을 사용합니다. `profile_routes`의 `profile`을 사용하거나 다른 프로필의 인증정보·SOUL.md·터미널 정책을 자동 전달하는 기능과 혼동하지 않습니다. `model_map`이 활성화되면 기본 `delegation.model`·`delegation.provider`는 경로를 결정하지 않습니다. 경로를 고르지 않으면 별도의 default 설정 또는 부모 모델이 사용되므로 테스트 시 명시적으로 `option`을 넘깁니다.

## 새 세션에서의 실제 확인 기준

1. `hermes delegation config --show`로 활성 `model_map` backend와 세 경로를 확인합니다. verified는 실제 실행 증거까지 확인한 경우에만 표시합니다.
2. **새 Hermes CLI 세션**을 시작하고 `delegate_task`의 현재 작업 스키마가 `option` 열거형 `light`·`standard`·`top`을 제공하는지 확인합니다. 실행 중 세션은 이전 도구 스키마를 유지할 수 있습니다.
3. `option`을 각각 명시한 짧은 읽기 전용 작업을 위임합니다. 세 작업 동시 호출이 하위 작업 수 제한에 걸리면, 제한을 변경하지 않고 두 작업과 한 작업 등 허용된 수로 나누어 재시도합니다.
4. 각 실행 결과의 `route` 메타데이터에서 선택 경로 `label`, `provider`, `model`, `reasoning_effort`와 노출된 `backend`를 목표와 대조합니다. 실효값은 실제 위임 도구의 실행 근거로 확인합니다.
5. `mapping`, 프로필별 플러그인 상태, 저장된 routes, 새 세션의 선택 가능 여부, 실제 위임과 실효 모델/effort를 **별도 항목**으로 남깁니다. 각 티어를 verified / mismatch / unverified로 판정하고 근거가 없으면 unverified를 유지합니다.

**호스트 제약:** 현재 연동 도구가 `option` 입력을 제공하지 않는다면 그 표면에서는 세 경로를 명시적으로 시험할 수 없습니다. Hermes CLI에서 기능이 확인됐다는 이유로 다른 클라이언트나 통합 도구에서도 동일하게 지원한다고 주장하지 않습니다. 그런 표면에서 임의의 다른 위임 API로 실행한 결과는 Hermes route 검증이 아닙니다.

## 사용자 제공 검증 결과와 미확인

사용자 제공 실행 회고에 따르면 `light` → `gpt-6-luna` / low, `standard` → `gpt-6.1-terra` / low, `top` → `gpt-6.1-sol` / medium의 세 호출이 성공했으며 각 결과에서 backend=model_map, 선택 경로, provider, model, reasoning effort를 관찰했습니다. 이 실험의 최초 일괄 세 작업은 한도 때문에 거부됐고 두 작업과 한 작업으로 나누어 성공했습니다. **이 문서 작성자는 Hermes CLI 로그 원본을 검증하거나 동일한 위임을 재실행하지 않았습니다.**

## 안전한 복구

설치 실패·모델 미지원·세션 스키마 갱신 실패는 각각 실제 실패 상태로 기록합니다. 스킬의 적용 기록과 승인받은 지속 백업으로 사용자 소유 설정의 변경 범위를 복구합니다. Hermes의 `/delegation default`는 별도 승인된 기본 backend 복원 수단이며 기존 모델 경로 정의를 삭제하지 않습니다. 인증정보와 다른 프로필의 설정을 건드리지 않습니다.
