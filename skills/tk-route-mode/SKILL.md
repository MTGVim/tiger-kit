---
name: tk-route-mode
description: "[user] 현재 사용자 위임 티어의 모델·effort를 조회하고 고성능·균형·절약 관점에서 최신 코딩 에이전트 실측과 커뮤니티 근거로 변경을 제안합니다. 승인 후에만 사용자 대응표와 호스트 설정을 적용·검증합니다. 메인 세션 모델은 변경하지 않습니다."
disable-model-invocation: true
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---
<!-- tigerkit:universal-authoring-gate -->
## 공통 저작 품질 관문

이 스킬에서 질문·메시지·설명·보고서·Markdown·HTML·대본·자막·문서·스킬 본문 등 사람이 읽는 텍스트를 **새로 작성하거나 의미·표현을 수정하기 전에**, 설치된 `tk-writing`의 [모든 저작의 공통 관문](../tk-writing/references/authoring-gate.md)과 [명확한 글쓰기](../tk-writing/references/clear-writing.md)를 이번 작업에서 읽고 적용합니다. 최종 산출물을 인계하기 전에 같은 기준으로 원고를 검사하고 문제를 수정합니다. 이미 읽은 기준을 반복 로드하거나 별도 재작성 스킬·에이전트·승인 라운드를 추가하지 않습니다. 코드·명령·식별자·기계 판독 형식·인용과 고정 문구는 보호하며, 이 참조로 변경·전송·발행 권한이 생기지 않습니다. 이 스킬이 작성 작업을 수행하지 않는 경우에는 추가 읽기가 필요하지 않습니다.
<!-- /tigerkit:universal-authoring-gate -->

# 위임 모델 추천 및 설정

사용자 호출은 **`tk-route-mode` 하나**입니다. 인자로 모드를 지정하지 않습니다. 저장되는 `standard`·`economy` 모드와 모델 자동 도출 `derive()`는 폐기했습니다. 다만 능력 티어인 `light`, `standard`, `top`과 위임 대상 이름 `tier-light`, `tier-standard`, `tier-top`은 그대로 유지합니다. 메인 세션의 모델, 자동 라우터 또는 런타임 훅을 변경하지 않습니다.

실제 업무에서 역할별 티어 선택, 독립 리뷰의 정본은 [위임 계약](../tk-engineering/references/delegation.md)입니다. 모델 설정의 정본은 [단일 기본 대응표](references/route-defaults.json)와 사용자 대응표입니다. [선정 원칙](references/selection.md)을 조회와 분석 전에 읽습니다. 사용자에게 선택·승인을 요청하기 전 [질문 기준](../tk-questioning/references/questions.md)과 [결과 전달](../tk-writing/references/delivery.md#results)을 적용합니다. 비밀을 포함할 수 있는 파일 조회와 백업 전에 [비밀 보호·지속 백업 기준](../tk-artifacts/references/artifact-paths.md)을 확인합니다.

## 실행 순서

1. **조회**: 인자 없이 `python3 scripts/route_mode.py status`를 읽기 전용으로 실행합니다. 스킬 기본값과 현재 저장된 단일 대응표, 사용자 override 및 유효값을 구분합니다. 현재 호스트의 실제 프로필 파일·로드·티어 선택 규칙·위임 결과는 별도 열로 분리하고, 확인하지 못하면 `unverified`로 둡니다. 조회 때문에 새 위임·파일 생성·인증 변경을 하지 않습니다. v1 모드 설정만 있으면 현재 활성 모드의 읽기 전용 이전 미리보기를 표시하고 `migration required`라고 명시합니다.
2. **관점 질문**: 어떤 관점에서 추천할지 **고성능 / 표준(균형) / 절약** 세 선택지를 한 번 묻습니다. 관점은 이번 분석의 우선순위일 뿐 저장 모드나 프로필 이름이 아닙니다. 이미 사용자가 관점을 명시했다면 재질문하지 않습니다.
3. **최신 근거 조사**: 매 실행마다 모델 출시·지원 상태와 현재 공개된 코딩 에이전트 벤치 원본, 비용, 커뮤니티 실험을 확인합니다. 출처·벤치 버전·조회일·호스트·모델 ID·effort를 명시합니다. 자체 코딩 벤치를 실행하지 않습니다. 현재 계정의 정확한 호스트 모델 ID와 effort 지원은 별도로 확인하며 확인 불가 시 `unverified`로 기록합니다.
4. **후보 평가**: 공급자 × 세 티어 각각 `현재값 → 제안 후보 → 판정 및 이유`를 작성합니다. 벤치 측정값, 작업당 API 비용, 측정되면 성공당 비용·실행 시간, 커뮤니티의 구체적인 결과 및 한계를 함께 보여 줍니다. 현 설정과 후보가 **같은 벤치 버전·같은 호스트·각각 실제 사용할 effort**에서 측정되지 않았다면 직접 우위를 주장하지 않습니다.
5. **승인 경계**: 사용자에게 비밀 없는 변경 diff와 근거, 단일 사용자 파일 마이그레이션 필요 여부, 별칭 정리, 호스트별 적용 파일, 백업·복원, 재로드·실효 위임 검증 계획을 한 번에 제시합니다. 사용자에게서 **승인 또는 거절**을 받습니다. 수정 제안이 있으면 반영해 다시 제시합니다. 승인하지 않은 항목은 보존합니다.
6. **적용 및 검증**: 승인된 단일 대응표와 호스트 설정에 한해 적용합니다. 기존 사용자 override를 덮어쓰지 않으며, 적용 전 안전한 백업을 저장합니다. 프로필 파일 생성·로드·규칙 선택·실제 위임의 실효 모델/effort를 서로 다른 검증 상태로 보고합니다. 실패하거나 확인할 수 없으면 성공으로 표시하지 않습니다.

사용자가 명시적으로 상태 조회만 요청한 경우에는 1단계만 수행합니다. 사용자가 변경까지 승인했더라도 외부 배포, 인증 수정, 다른 프로필의 변경을 승인으로 확대하지 않습니다.

## 평가 기준 및 결과 양식

**고성능**은 SWE 작업 완료율·검증 통과율·독립 리뷰 품질을 최우선으로 보고 비싼 비용도 선택할 수 있습니다. **표준**은 실제 코딩 성능과 작업당 비용의 균형을, **절약**은 품질의 허용 하한을 유지하면서 비용 및 재시도로 인한 전체 작업 비용을 고려합니다. 절약이라고 effort를 한 단계 내리거나 `top`을 무조건 고정하지 않습니다. API 비용은 구독 한도 소모량으로 환산하지 않습니다.

제안 결과 표에는 `공급자/티어 | 현재 모델·effort(기본값/override 구분) | 후보 모델·effort | SWE/코딩 벤치명·점수·버전 | 현재/후보 cost per task(USD) | 성공당 비용·시간(있으면) | 판정 | 이유·출처`를 포함합니다. 서로 다른 벤치의 점수를 같은 수치처럼 나란히 비교하지 않고, 행의 측정 조건을 확인할 수 없으면 `미측정`으로 표시합니다. 종합 지능 점수는 후보를 좁힐 때만 사용하고 코딩 성능으로 대체하지 않습니다. 모델 변경과 구식 Codex 별칭 정리는 별도의 제안 항목으로 둡니다.

판정은 세 가지입니다.
- `변경 제안`: 같은 측정 조건의 확인된 실질적 이점 또는 명시적 사용자 운영 정책에 따라 변경을 제안할 이유가 있으며, 근거의 종류를 구분합니다.
- `후보만 제시`: 출시·다른 effort·커뮤니티 사례에서 가능성이 있지만 현재값 대비 직접 비교 우위가 입증되지 않은 상태입니다.
- `유지`: 비교 조건이 부족하거나 변경의 이점이 충분히 확인되지 않았습니다.

실효 구현·리뷰 신뢰성은 작업 범위, 실패·재시도·조기 종료, 검증 통과 여부를 따로 판단합니다. 좁은 구현 성공 사례를 독립 리뷰 품질의 증거로 확장하지 않습니다. Terra 6.1의 Effort 변경 위험은 [ADR 0009](../../docs/adr/0009-route-mode-terra-retrial.md)의 관찰과 미검증 구분을 유지합니다. 새 정책 결정은 [ADR 0010](../../docs/adr/0010-route-mode-single-mapping.md)을 따릅니다.

## 내부 도우미와 저장 형식

```bash
python3 scripts/route_mode.py status
python3 scripts/route_mode.py path
python3 scripts/route_mode.py validate
python3 scripts/route_mode.py plan --provider openai
python3 scripts/route_mode.py migrate                # 읽기 전용 미리보기
python3 scripts/route_mode.py migrate --save --accept-inactive-modes  # 마이그레이션 승인 후
python3 scripts/route_mode.py apply --set openai.standard=gpt-6.2-sol:medium  # 변경 승인 후
python3 scripts/route_mode.py apply --unset openai.standard             # override 해제 승인 후
python3 scripts/route_mode.py rule status --file /absolute/path/to/AGENTS.md      # 구형·신형 마커를 모두 인식
python3 scripts/route_mode.py rule migrate --file /absolute/path/to/AGENTS.md --host codex  # 별도 승인 후 마커만 이전
```

내부 명령에 붙는 인자는 사용자 스킬 호출 인자가 아닙니다. `status`, `path`, `plan`, `validate`, 기본 `migrate`와 `rule status`는 읽기 전용이며, `apply`, `migrate --save`, `rule on/off/migrate`는 쓰기 작업입니다. 지침 블록은 `TIGERKIT_ROUTE_MODE_BEGIN/END`를 사용합니다. 기존 `route-mode:begin/end`를 발견해도 `rule status`는 계속 인식하며, `rule migrate`는 승인 후 블록 본문을 바꾸지 않고 마커만 변환합니다. 변경 전 백업·적용 기록은 기존 방식으로 남깁니다. `tk-setup-skills`의 `user-guidance` 점검에서도 구형 마커의 이전을 별도로 제안할 수 있습니다. `derive`, `derive --save`, 모드 `use`·`add`·`list`·`update <mode>` 명령은 제거합니다.

기본 파일은 `references/route-defaults.json`이며, 사용자 대응표는 `ROUTE_MODE_CONFIG` 또는 `$XDG_CONFIG_HOME/route-mode/routes.json` (XDG 설정이 없으면 `~/.config/route-mode/routes.json`)입니다. **v2 설정**에는 `version`, `tiers`, `efforts`, 단일 `providers`와 `overrides`만 둡니다. `standard`라는 **티어 키**는 유지하지만 `active`, `modes.standard`, `modes.economy`, `extends`는 저장하지 않습니다. 기존 `modes.json`을 발견해도 자동 전환하지 않습니다. 선택된 과거 활성 모드의 실효값과 사용자 override를 읽기 전용으로 미리 보고하고, 사용하지 않을 과거 모드 목록과 그 설정이 새 파일로 이동하지 않는다는 점을 승인받습니다. 이전 시 원본은 보존하고 지속 백업을 만든 뒤 새 파일에 저장합니다. 이미 존재하는 새 파일은 덮어쓰지 않습니다.

현재 Codex 계정의 정확한 모델 ID는 [Codex 카탈로그 대조](references/hosts.md#codex-모델-카탈로그-대조)에 따라 확인합니다. `luna`, `terra`, `sol`을 이름만 보고 치환하지 않습니다. 정확한 ID/effort와 현재 호스트 적용 가능성을 확인하지 못한 모델은 승인된 설정에도 강제로 쓰지 않습니다. Claude Code, Codex 및 Hermes 세부 절차는 [호스트 안내](references/hosts.md)와 [Hermes 안내](references/hermes-setup.md)를 따릅니다.

## 적용 및 실제 검증

기존 설정의 소유권·심볼릭 링크 여부를 확인하고 변경 대상의 정확한 경로, 키, 비밀 없는 전후 diff와 복원 경로를 제시합니다. 인증 정보나 토큰은 표시·복사하지 않습니다. 사용자 설정은 설치 패키지나 저장소에 기록하지 않습니다. 기존 백업/적용 기록은 사용자 설정 경로의 `backups/`, `applied/`에 둡니다. 확인되지 않은 기록을 근거로 이미 적용됐다고 판단하지 않습니다.

호스트 설정 변경 전에는 정확한 모델 ID·effort를 검증하고, Codex는 모델 카탈로그와 실효 agent TOML을 각각 확인합니다. Hermes의 현재 프로필·백엔드, Claude Code와 Codex의 사용자 수준 에이전트 정의·티어 선택 규칙을 별개로 검사합니다. 프로필과 규칙을 변경할 때에는 동등한 규칙이 있으면 중복 생성하지 않습니다. 복구는 자신이 변경한 범위와 지문이 확인된 원본만 사용합니다.

검증은 (1) 단일 표와 별칭 검사, (2) 파일 생성, (3) 현재 호스트 프로필 로드, (4) 위임 티어의 실제 선택, (5) 호스트가 기록한 실효 모델·effort를 분리합니다. 단순 조회에서 새 위임을 하지 않고 **적용 승인 후에만** 각 티어에 짧은 읽기 전용 위임을 실행합니다. 자식의 자기 보고만으로 `verified`라고 하지 않습니다. 현재 세션이 설정을 재로드하지 않았다면 `unverified`이고, 재로드 뒤 값이 다르면 `mismatch`입니다. Terra 시범 검증은 모델과 effort를 새 세션 시작부터 고정하며 중간 변경을 피합니다.

## 회귀 확인

- 기본 스킬 호출은 인자 없이 조회→관점 선택→근거 비교→제안→승인으로 진행되며 조회만으로 파일이나 위임을 만들지 않아야 합니다.
- 저장 파일에 모드 키가 없어야 하고 능력 티어 `standard`는 유지되어야 합니다.
- 벤치마크 결측·호스트 불일치·별칭 미확인 시 추측하거나 자동 적용하지 않아야 합니다.
- v1의 활성 실효값·override를 이전 미리보기에서 보존하고 비활성 모드가 소실됨을 명시해야 합니다.
- 제안은 별도 `변경 제안`·`후보만 제시`·`유지`로 구분하며 절약 선택에서도 `top` 변경을 검토해야 합니다.
- 실제 프로필·위임 검증 없이 `verified`라고 표시하지 않아야 합니다.
