# TigerKit 18

<p align="center">
  <img src="assets/tigerkit-cover.png" width="960" alt="TigerKit Agent Skills 표지">
</p>

TigerKit은 Claude Code, Codex, Hermes Agent용 소규모 엔지니어링 Agent Skills 모음입니다. 버전 18.0.0은 Agent Skills 형식을 사용하며 더 이상 Claude Code 플러그인 런타임을 제공하지 않습니다.

## 설치

최초 지원 대상인 모든 호스트에 전체 스킬을 전역으로 설치합니다.

```bash
npx skills add MTGVim/tiger-kit \
  --global \
  --agent claude-code \
  --agent codex \
  --agent hermes-agent \
  --skill '*'
```

선택한 스킬만 설치합니다.

```bash
npx skills add MTGVim/tiger-kit \
  --global \
  --agent claude-code \
  --agent codex \
  --agent hermes-agent \
  --skill tk-implement \
  --skill tk-browser-verify
```

변경되지 않는 18.0.4 스냅샷을 설치합니다.

```bash
npx skills add "MTGVim/tiger-kit#v18.0.4" \
  --global \
  --agent claude-code \
  --agent codex \
  --agent hermes-agent
```

Claude Code와 Hermes Agent에서는 설치한 스킬이 `/tk-implement` 같은 슬래시 명령으로 표시됩니다. Codex에서는 `$tk-implement` 또는 스킬 선택기를 사용합니다.

## 스킬 목록

- **`[user]` 사용자 호출**: 사용자가 `/tk-implement` 또는 `$tk-implement`처럼 스킬을 명시적으로 선택합니다.
- **`[auto]` 모델 호출**: 관련 작업에 해당 규율이 필요하면 모델이 스킬로 연결합니다.
- **`[user/auto]` 혼합 호출**: 사용자의 명시적 선택과 모델 연결을 모두 지원합니다.

### 구체화

| 스킬 | 호출 방식 | 목적 |
| --- | --- | --- |
| `tk-grill-me` | 사용자 호출 | 중요한 결정을 한 번에 하나의 질문으로 철저히 검토합니다. |
| `tk-grill-with-docs` | 사용자 호출 | 결정을 검토하면서 합의된 용어와 조건에 맞는 ADR을 기록합니다. |
| `tk-grilling` | 모델 호출 | 한 번에 하나씩 질문해 의사결정을 수렴하는 모델 규율입니다. |
| `tk-domain-modeling` | 모델 호출 | 도메인 용어와 개념의 경계를 명확하게 다듬습니다. |
| `tk-prototype` | 사용자 호출 | 폐기할 수 있는 UI 또는 로직 검증물을 만듭니다. |
| `tk-codebase-design` | 모델 호출 | 근거를 바탕으로 가장 작은 구조 개선안을 제안합니다. |

### 문서화

| 스킬 | 호출 방식 | 목적 |
| --- | --- | --- |
| `tk-to-spec` | 사용자 호출 | 근거와 결정을 종합해 명세를 작성합니다. |
| `tk-to-tickets` | 사용자 호출 | 각각 독립적으로 검증할 수 있는 수직형 티켓을 만듭니다. |

### 구현

| 스킬 | 호출 방식 | 목적 |
| --- | --- | --- |
| `tk-implement` | 사용자 호출 | 요청한 변경을 구현하고 검증합니다. |
| `tk-browser-verify` | 혼합 호출 | 실제 브라우저에서 UI, 동작, 환경, 디자인 충실도를 검증합니다. |

### 학습

| 스킬 | 호출 방식 | 목적 |
| --- | --- | --- |
| `tk-reflect` | 사용자 호출 | 재사용할 수 있는 저장소/사용자 규칙 또는 스킬 후보를 제안합니다. |
| `tk-learn` | 사용자 호출 | 근거를 재사용할 수 있는 저장소 또는 사용자 스킬로 만듭니다. |
| `tk-grooming` | 사용자 호출 | 기존 규칙과 스킬을 점검하고 선택적으로 수정합니다. |

### 이어가기

| 스킬 | 호출 방식 | 목적 |
| --- | --- | --- |
| `tk-handoff` | 사용자 호출 | 검증된 작업 상태를 기록하거나 이어서 진행합니다. |

### 작업 규율

| 스킬 | 호출 방식 | 목적 |
| --- | --- | --- |
| `tk-tdd` | 모델 호출 | 가치 있는 동작 경계에 red-green-refactor를 적용합니다. |
| `tk-diagnosing-bugs` | 모델 호출 | 어려운 버그를 재현하고, 최소화하고, 진단하고, 수정한 뒤 회귀 여부를 확인합니다. |
| `tk-code-review` | 모델 호출 | 수정하지 않고 확정된 diff를 검토합니다. |
| `tk-merge-conflict` | 모델 호출 | 양쪽 의도를 모두 보존하면서 현재 충돌을 해결합니다. |

## 스킬 조합 방식

TigerKit은 반드시 따라야 하는 파이프라인이 아닙니다. 작은 변경에는 다음 스킬 하나만 사용할 수 있습니다.

```text
tk-implement
```

복잡한 설계에는 다음과 같이 사용할 수 있습니다.

```text
tk-grill-me
→ optionally tk-to-spec
→ optionally tk-to-tickets
→ tk-implement
```

사용자 호출 스킬은 후속 작업을 제안하지만 서로를 자동으로 호출하지 않습니다. 모델 호출 규율은 관련 작업을 안내할 수 있습니다. 위임과 검토의 범위는 제한적으로 유지합니다.

## `.tigerkit/`

`.tigerkit/`은 현재 명세, 티켓, 인수인계, 프로토타입, 스킬 초안, 브라우저 증거를 보관하는 선택적 worktree 로컬 임시 공간입니다. 이 저장소에서는 gitignore 대상으로 지정되어 있으며, 영구 프로젝트 문서가 아니고, 보관용 데이터베이스나 현재 항목을 가리키는 포인터가 없으며, 전역 TigerKit 상태 디렉터리에 저장되지 않습니다. TigerKit은 다른 저장소의 `.gitignore`를 수정하지 않습니다. `.tigerkit/`이 무시 대상이 아니면 스킬이 그 사실을 알립니다. TigerKit은 `docs/tigerkit/`를 만들지 않습니다.

## 버전 관리

`main`은 지속적으로 갱신되는 최신 소스입니다. Git 태그는 안정적이며 변경되지 않는 스냅샷입니다. 저장소는 하나의 제품으로서 SemVer를 따릅니다. 스킬 이름 변경/삭제, 호출 방식 변경, 호환되지 않는 `.tigerkit/` 변경, 배포 방식 변경은 메이저 릴리스에 해당합니다.

## 출처 표기

다음 각색 스킬은 [`mattpocock/skills` 저장소](https://github.com/mattpocock/skills)의 이름과 동작 방식에서 받은 영향을 유지합니다. `grilling`, `domain-modeling`, `grill-me`, `grill-with-docs`, `to-spec`, `to-tickets`, `tdd`, `diagnosing-bugs`, `code-review`, `implement`. TigerKit은 `tk-` 접두사를 추가하고 각 스킬에 `relationship: adapted`를 기록합니다. 라이선스 출처는 `NOTICE.md`에서 확인할 수 있습니다.

TigerKit 16.x에서 이전하시나요? `MIGRATION.md`를 읽어보세요.
