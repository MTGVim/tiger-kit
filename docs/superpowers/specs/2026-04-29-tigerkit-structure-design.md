# TigerKit Structure Design

## Goal

TigerKit은 요구사항을 정제하는 `tk:req`, 긴 답변의 의미를 해독하는 `tk:what`, 요구사항 대비 남은 차이를 확인하는 `tk:gap`으로 구성된 개인용 agent workflow 보조 키트다.

TigerKit은 구현 계획, 실행, 코드 리뷰, 학습 축적을 대체하지 않는다. Compound Engineering, Superpowers, Claude Reflect 같은 workflow 앞뒤와 중간에서 기준 정리와 차이 확인을 돕는다.

## Current State

현재 저장소는 `tigap-skills` 플러그인으로 구성되어 있고 공개 흐름은 `what → prep → gap`이다.

- `/tigap:what`: 긴 LLM 답변이나 애매한 설명을 짧은 한국어 실행 해설로 바꾼다. 파일 산출물은 만들지 않는다.
- `/tigap:prep`: 아이디어, 대화 맥락, 별도 자료를 `.gap/{work_id}/normalized/source-packet.md`로 정리한다.
- `/tigap:gap`: `source-packet.md`와 현재 구현, 문서, 동작 사이의 갭을 `.gap/{work_id}/analysis/gap-report.md`로 분석한다.

현재 `what`은 이미 “작업 상태 재정렬”이 아니라 “이 말이 뭐라는지 해독”으로 설계되어 있고 eval도 그 역할을 검증한다. 작업 중간/최종 상태 점검은 `gap`의 책임으로 통합하는 것이 더 단순하다.

## Product Model

새 core는 다음 세 개다.

```text
/tk:what  # 긴 답변/애매한 설명 해독
/tk:req   # 요구사항 소스 정제와 기준 문서 생성
/tk:gap   # requirements.md 대비 현재 상태 차이 확인
```

권장 참고 흐름은 다음과 같다.

```text
tk:req
→ ce-plan
→ ce-work
→ tk:gap
→ ce-work
→ ce-code-review
→ tk:gap
→ ce-compound
→ ship
```

이 흐름은 강제가 아니다. TigerKit은 기준 문서와 gap 확인을 제공하고, 실제 계획/실행 workflow 선택은 사용자와 현재 프로젝트가 결정한다.

## Command Responsibilities

### `tk:what`

`tk:what`은 기존 `/tigap:what`의 역할을 유지한다.

사용 시점:

- 긴 LLM 답변이 결국 무슨 말인지 모르겠을 때
- 회의록식 덤프나 애매한 설명을 바로 답할 수 있는 문장으로 줄이고 싶을 때
- “그래서 내가 뭐라고 답하면 되지?”가 핵심 질문일 때

하지 않는 일:

- 현재 작업 상태 점검
- 요구사항 문서 생성
- gap report 생성
- 구현 계획 작성
- 파일 수정

기본 출력은 기존 네 블록을 유지한다.

```md
🐯 제가 요약해드리죠
🎯 하려던 것
😵 막히는 지점
💡 이렇게 답하면 됨
```

### `tk:req`

`tk:req`는 기존 `prep`을 대체하는 요구사항 정제 도구다.

사용 시점:

- 외부 요구사항 소스가 흩어져 있을 때
- CE plan이나 gap 분석 전에 기준 문서가 필요할 때
- Jira, Confluence, PRD, 사용자 메모, 회의 요약, 기존 문서를 하나의 기준으로 정리하고 싶을 때

해야 할 일:

- 입력 소스 목록과 역할 기록
- 중복 제거
- 충돌과 모호점 표시
- 정규화된 요구사항 목록 생성
- acceptance signal 정리
- scope boundary 정리
- `requirements.md` 저장

하지 않는 일:

- 요구사항 임의 창작
- 구현 계획 확정
- 파일별 수정 지시
- 코드 패치 작성
- CE plan을 대체하는 task breakdown 생성

### `tk:gap`

`tk:gap`은 `requirements.md` 대비 현재 상태의 차이를 확인한다.

사용 시점:

- 작업 전 현재 구현과 요구사항 차이를 알고 싶을 때
- 작업 중 남은 gap을 확인하고 싶을 때
- 출고 전 요구사항 대비 확인 가능한 gap이 남았는지 보고 싶을 때

해야 할 일:

- 각 requirement가 현재 구현, 문서, 테스트, 관찰 가능한 동작에서 충족되는지 확인
- evidence와 gap을 분리해서 기록
- ship blocker 여부를 판단할 수 있게 severity를 표시
- 확인 불가 항목은 `Unable to Verify`로 분리
- 다음 행동 후보를 짧게 제시

하지 않는 일:

- 구현 계획 새로 만들기
- 여러 단계 task breakdown 작성
- CE workflow 자동 실행
- 확인 불가 요구사항이 있는데 `NO_GAPS_FOUND`로 판정하기

## Artifact Layout

새 표준 산출물 구조는 다음과 같다.

```text
.tigerkit/{work_id}/
  inputs/
  requirements.md
  requirements.meta.json
  gap.md
  gap.meta.json
```

파일 책임:

| 파일 | 역할 |
|---|---|
| `inputs/` | `requirements.md`를 만들 때 참고한 원문 자료, 메모, 캡처, 참고 코드 보관 위치 |
| `requirements.md` | 이번 작업의 정규화된 요구사항 기준 문서 |
| `requirements.meta.json` | `requirements.md` 재사용 여부를 판단하는 캐시 메타데이터 |
| `gap.md` | 현재 상태와 `requirements.md` 사이의 coverage/gap 분석 |
| `gap.meta.json` | `gap.md` 재사용 여부를 판단하는 캐시 메타데이터 |

`.gap/`은 기존 tigap 모델의 이름이므로 TigerKit 전환에서는 `.tigerkit/`으로 바꾼다. 기존 `.gap/` 산출물 마이그레이션은 자동 수행하지 않는다. 필요하면 사용자가 특정 work_id를 지정했을 때 읽기 전용 legacy input으로만 다룬다.

## Requirements Document Format

`requirements.md`는 다음 구조를 기본으로 한다.

```md
# Requirements

## Source Inputs
| Source | Type | Role | Status | Notes |
|---|---|---|---|---|

## Normalized Requirements
| ID | Requirement | Priority | Source | Acceptance Signal |
|---|---|---|---|---|

## Scope Boundary
### In Scope
-

### Out of Scope
-

## Conflicts / Ambiguities
| ID | Issue | Sources | Impact | Suggested Resolution |
|---|---|---|---|---|

## Assumptions
| ID | Assumption | Reason | Risk |
|---|---|---|---|

## Unknowns
| ID | Question | Impact | Suggested Next Step |
|---|---|---|---|

## Gap Check Basis
- `tk:gap`은 이 문서의 Normalized Requirements와 Acceptance Signal을 기준으로 현재 상태의 차이를 확인한다.
```

## Gap Report Format

`gap.md`는 다음 구조를 기본으로 한다.

```md
# Gap Report

## Verdict
GAPS_FOUND / NO_GAPS_FOUND / UNVERIFIABLE

## Requirement Coverage
| Requirement ID | Status | Evidence | Gap |
|---|---|---|---|

## Remaining Gaps
| Gap ID | Requirement ID | Severity | Description | Suggested Next Move |
|---|---|---|---|---|

## Unable to Verify
| Requirement ID | Reason | Needed Evidence |
|---|---|---|

## Notes
-
```

판정 규칙:

- 남은 gap이 있으면 `GAPS_FOUND`다.
- 확인 불가능한 requirement가 있으면 `NO_GAPS_FOUND`를 쓰지 않는다.
- 확인 가능한 기준에서 충족되고 확인 불가 항목이 없을 때만 `NO_GAPS_FOUND`를 쓴다.
- `NO_GAPS_FOUND`는 “현재 확인 가능한 기준에서는 남은 gap 없음”으로 표현한다.

## Migration Strategy

### Minimum viable implementation

1. `prep`을 `req`로 rename/reframe한다.
2. command namespace를 `/tk:req`, `/tk:what`, `/tk:gap`로 바꾼다.
3. 산출물을 `.tigerkit/{work_id}/requirements.md`와 `.tigerkit/{work_id}/gap.md`로 바꾼다.
4. README, docs, CLAUDE.md, evals, install scripts, plugin manifests를 새 이름으로 정렬한다.
5. 기존 `/tigap:*`와 `.gap/`은 문서에서 primary로 다루지 않는다.

### Legacy handling

기존 `tigap` command와 `prep` skill을 alias로 남길지는 별도 선택이다. 기본 설계는 새 namespace로 단순화하는 것이다.

호환성을 남긴다면:

- `/tigap:what` → `/tk:what`
- `/tigap:prep` → `/tk:req`
- `/tigap:gap` → `/tk:gap`

단, alias가 늘어나면 manifest와 문서가 복잡해지므로 첫 구현에서는 권장하지 않는다.

## User-Facing Notification Policy

각 명령은 상세 본문을 채팅에 길게 출력하지 않는다.

### `tk:what`

```text
🐯 제가 요약해드리죠
...
🎯 하려던 것
...
😵 막히는 지점
...
💡 이렇게 답하면 됨
...
```

### `tk:req`

```text
생성: .tigerkit/{work_id}/requirements.md
요약:
- 외부 요구사항 소스 N개를 정제했습니다.
- 정규화된 요구사항 M개와 모호점 K개를 기록했습니다.
- 다음 단계는 ce-plan 등 구현 계획 workflow에서 requirements.md를 기준으로 계획을 세우는 것입니다.
```

### `tk:gap`

```text
결과: GAPS_FOUND / NO_GAPS_FOUND / UNVERIFIABLE
보고서: .tigerkit/{work_id}/gap.md
핵심 gap:
- ...
다음 행동:
- ...
```

## Validation

변경 후 기본 검증은 다음을 사용한다.

```bash
claude plugin validate .claude-plugin/plugin.json
claude plugin validate .
git diff --check
```

문서/스킬 일관성은 grep으로 확인한다.

```bash
grep -R "tigap\|/tigap\|prep\|source-packet\|gap-report\|\.gap/" -n CLAUDE.md README.md docs commands skills evals .claude-plugin scripts
```

의도적으로 남긴 legacy 설명이 없다면 출력이 없어야 한다.

## Implementation Decisions

첫 구현은 다음 기준으로 진행한다.

- 기존 `/tigap:*` alias는 남기지 않고 `/tk:*`로 단순화한다.
- 기존 `prep` command/skill은 `req`로 대체한다.
- 산출물 루트는 `.gap/`에서 `.tigerkit/`으로 바꾼다.
- 저장소 디렉터리나 GitHub repository 이름 변경은 이번 구현 범위에서 제외한다.
- plugin/package 이름, 문서의 제품명, namespace, standalone install 안내는 TigerKit과 `tk:*` 기준으로 바꾼다.

저장소 이름 변경은 marketplace 배포와 기존 설치 안내에 영향을 주므로 별도 작업으로 다룬다.
