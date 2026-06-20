# RFC: TigerKit `reflect`를 skill-only 회고에서 promotion router로 확장

- 상태: Proposed
- 날짜: 2026-06-20
- 작성자: Hermes Agent

## 요약

TigerKit의 `/tk:reflect`를 단순한 reusable learning 정리 명령이 아니라, **세션에서 얻은 learning을 가장 적절한 실행 표면으로 승격시키는 router**로 확장한다.

이번 변경의 핵심은 다음과 같다.

- `reflect`의 출력 대상을 `user skills` 하나로 좁히지 않는다.
- learning을 다음 표면 중 하나로 분류한다.
  - repo `CLAUDE.local.md`
  - repo `CLAUDE.md` proposal
  - user `PROFILE.md`
  - user `CLAUDE.md`
  - user skills
  - hook / hookify proposal
  - command proposal
  - agent proposal
  - discard
- shared rule, source code, branch-specific one-off에 대한 안전 경계를 유지한다.

한 문장으로 말하면, TigerKit `reflect`를 **“무엇을 배웠는가”를 적는 회고 명령**에서 **“이 배움을 어디에 어떻게 남길 것인가”를 결정하는 promotion surface**로 재정의한다.

## 배경

현재 TigerKit의 `reflect`는 세션 내용, 실제 변경 결과, 성공/실패, 사용자 피드백에서 reusable learning과 improvement를 추출하는 contract를 가진다.

현재 public policy는 다음 표면을 정의한다.

- repo `CLAUDE.local.md` -> auto apply
- repo `CLAUDE.md` -> suggest only
- user `PROFILE.md` -> auto apply
- user `CLAUDE.md` -> auto apply
- user skills -> auto apply

이 모델은 이미 안전한 저장 경계와 durable learning 승격 흐름을 잘 제공한다. 그러나 실제 usage를 보면 reusable learning이 항상 skill로 귀결되지는 않는다.

예를 들어:

1. 어떤 learning은 선언적 guidance이므로 `CLAUDE.md` 계열에 더 가깝다.
2. 어떤 learning은 반복 절차이므로 skill에 적합하다.
3. 어떤 learning은 반복적 실수를 자동으로 막는 것이 더 좋으므로 hook/hookify proposal이 더 적합하다.
4. 어떤 learning은 slash command 형태의 reusable workflow로 승격하는 편이 낫다.
5. 어떤 learning은 전문 역할 분리이므로 agent proposal이 더 적합하다.

즉, 현재 `reflect`는 **learning capture는 잘하지만 promotion target taxonomy는 아직 좁다.**

## 목표

- `reflect`를 TigerKit의 lightweight learning router로 확장한다.
- reusable learning을 가장 적절한 실행 표면으로 분류하도록 한다.
- skill / rule / hook / command / agent를 한 taxonomy 안에서 다룬다.
- 기존의 safe boundary를 유지한다.
- shared repo rule을 자동 수정하지 않는 원칙을 유지한다.
- branch-specific one-off와 low-confidence 후보를 durable surface로 승격하지 않도록 한다.

## 비목표

- TigerKit을 workflow runner나 orchestration framework로 바꾸지 않는다.
- hook / command / agent를 자동 생성하는 runtime을 새로 만들지 않는다.
- source code를 `reflect`가 직접 수정하게 만들지 않는다.
- Hermes처럼 usage telemetry, curator, archive/pin lifecycle subsystem을 도입하지 않는다.
- repo shared `CLAUDE.md`를 auto apply 대상으로 바꾸지 않는다.

## 문제 정의

현재 `reflect`는 learning을 잘 뽑아내도, 다음 질문에 대한 구조적 답이 약하다.

- 이건 rule인가, skill인가?
- 이건 사람이 읽고 따를 guidance인가, 아니면 자동 enforcement가 필요한가?
- 이건 개인적/로컬 guidance인가, shared policy proposal인가?
- 이건 command나 agent로 독립시키는 편이 더 좋은가?
- 이건 아예 버려야 하는가?

이 분류가 없으면 다음과 같은 문제가 생긴다.

1. skill 과잉 생성
2. 선언적 규칙과 절차적 규칙 혼합
3. 자동 enforcement가 필요한 learning이 문서에만 남아 재발
4. branch-specific one-off가 durable surface로 오염
5. shared project rule과 private local rule이 섞임

## 제안

### 1. `reflect`의 core mental model을 promotion router로 확장

기존:

```text
reflect = session result + feedback -> safe improvement candidates/apply
```

제안:

```text
reflect = session result + feedback -> classify learning -> promote to the right surface
```

### 2. Promotion target taxonomy 도입

`reflect`는 각 candidate를 아래 target 중 **정확히 하나**로 분류한다.

#### A. repo `CLAUDE.local.md`
언제 쓰나:
- 이 repository나 local workflow에만 유효한 private guidance
- shared project policy까지는 아닌 실무 습관
- repo-local validation order, local guardrail, file-scope reminder

정책:
- auto apply 허용

#### B. repo `CLAUDE.md` proposal
언제 쓰나:
- 팀 전체가 공유해도 되는 project rule
- repo-wide policy, standard, invariant

정책:
- suggest only
- diff proposal만 출력
- direct edit 금지

#### C. user `PROFILE.md`
언제 쓰나:
- 사용자 preference/profile
- stable working preference
- communication or workflow preference

정책:
- auto apply 허용

#### D. user `CLAUDE.md`
언제 쓰나:
- user-level durable guidance
- 여러 repo에 걸쳐 재사용되는 operating preference
- 개인적인 default practice

정책:
- auto apply 허용

#### E. user skills
언제 쓰나:
- 반복 가능한 multi-step routine
- real decision process가 있는 절차
- future session에서 직접 재사용 가능한 workflow

정책:
- auto apply 허용

#### F. hook / hookify proposal
언제 쓰나:
- 같은 실패가 반복됨
- trigger가 명확함
- pattern match 또는 tool event로 자동 감지 가능함
- 문서화보다 enforcement가 더 효과적임

예:
- dangerous bash 차단
- 특정 파일 수정 후 lint/test reminder
- 특정 경로 밖 수정 경고
- reflect 누락 reminder

정책:
- 기본 suggest only
- rationale, trigger, expected action을 proposal로 출력
- v1에서는 auto apply 금지

#### G. command proposal
언제 쓰나:
- 자주 반복되는 workflow를 slash command로 묶는 편이 좋음
- 여러 단계가 있으나 automation surface가 command가 더 적합함

예:
- review-prep
- release-preflight
- repo-specific audit

정책:
- suggest only
- command markdown skeleton proposal 가능

#### H. agent proposal
언제 쓰나:
- 반복되는 전문 역할 분리가 필요함
- same review lens가 여러 작업에서 반복됨
- command보다 specialist role이 더 적합함

예:
- security reviewer
- docs consistency reviewer
- test design reviewer

정책:
- suggest only
- agent frontmatter + role summary proposal 가능

#### I. discard
언제 쓰나:
- branch-specific one-off
- low-confidence
- stale soon
- sensitive or unnecessary personal data
- raw task log / PR number / issue number / temporary workaround

정책:
- 저장 금지

### 3. Skill과 hook의 경계를 contract에 명시

`reflect`는 다음 구분을 따른다.

#### skill로 보내는 경우
- 절차가 multi-step
- 판단이 많이 필요함
- 맥락 해석이 중요함
- 사람이 읽고 따라야 효과적임

#### hook/hookify proposal로 보내는 경우
- 반복적 실패/누락이 있음
- trigger를 기계적으로 잡을 수 있음
- automatic warning/block/reminder가 더 효과적임
- false positive risk가 허용 가능한 수준임

### 4. Apply policy를 표면별로 재정의

| Target | Policy |
|---|---|
| repo `CLAUDE.local.md` | auto apply |
| repo `CLAUDE.md` | suggest only |
| user `PROFILE.md` | auto apply |
| user `CLAUDE.md` | auto apply |
| user skills | auto apply |
| hook / hookify | suggest only |
| command | suggest only |
| agent | suggest only |
| discard | never store |

### 5. Output contract 확장

기존 receipt를 아래처럼 확장한다.

```text
Reflect 완료
적용 대상:
- repo CLAUDE.local.md: <applied|not_applicable>
- repo CLAUDE.md: suggest_only:<count>
- user PROFILE.md: <applied|not_applicable>
- user CLAUDE.md: <applied|not_applicable>
- user skills: <applied|not_applicable>
- hook proposals: <count>
- command proposals: <count>
- agent proposals: <count>

## Repo 후보
n. <candidate or NONE>

## User 후보
n. <candidate or NONE>

## Skill 후보
n. <candidate or NONE>

## Hook / Hookify 제안
n. <proposal or NONE>

## Command 제안
n. <proposal or NONE>

## Agent 제안
n. <proposal or NONE>

## Discard
n. <candidate or NONE>

## 충돌 / 적용 조건
- <condition or none>

## 다음 행동
- <next step or 없음>
```

## 세부 변경 범위

### User-facing docs
- `README.md`
- `commands/reflect.md`
- `docs/reflect-file-policy.md`
- 새 RFC 문서

### Non-goal / no immediate implementation
이번 RFC는 다음을 즉시 요구하지 않는다.

- hook file 생성기
- command scaffold generator
- agent generator
- promotion telemetry
- background reflection daemon

## 저장 경계

기존 TigerKit의 안전 경계를 유지한다.

### 유지되는 금지
- repo shared `CLAUDE.md` 직접 수정 금지
- source code 수정 금지
- branch-specific one-off durable rule 승격 금지
- rejected / low-confidence / 민감 정보 저장 금지

### 새로 명시할 금지
- false-positive risk가 큰 hook를 auto apply하지 않는다.
- command/agent proposal을 “이미 설치된 active surface”처럼 말하지 않는다.
- hookify가 실제 설치/활성화되지 않았는데 installed behavior처럼 설명하지 않는다.

## 왜 이 방향이 TigerKit에 맞는가

TigerKit은 현재 다음 identity를 가진다.

- SoT가 있으면 gap을 먼저 본다.
- 의미 있는 작업이 끝나면 reflect로 learning을 남긴다.
- 공개 실행 표면은 가볍고 좁다.
- orchestration framework가 아니라 lightweight plugin이다.

이 철학에 비추어 보면, TigerKit이 해야 할 일은 “모든 것을 자동화하는 것”이 아니라, **세션에서 배운 것을 올바른 durable surface로 보내는 판단 표면**을 제공하는 것이다.

이 RFC는 TigerKit의 경량성을 유지하면서도 `reflect`의 설명력을 크게 높인다.

## 대안 검토

### A. 현재 모델 유지 (skill 중심)
장점:
- 단순하다.
- 현재 문서와 크게 충돌하지 않는다.

단점:
- 선언적 rule과 절차적 skill이 섞인다.
- hook/command/agent로 더 잘 표현될 learning을 skill로 과승격하게 된다.
- reflection quality가 떨어진다.

### B. hook / command / agent까지 auto apply 허용
장점:
- 자동화 수준이 높아진다.

단점:
- TigerKit이 경량 plugin이라는 정체성과 충돌한다.
- side effect risk가 커진다.
- false positive와 surface sprawl이 빠르게 커진다.

### C. skill과 rule만 유지하고 hook proposal은 배제
장점:
- 문서 구조가 단순하다.

단점:
- 반복되는 실수 방지의 enforcement 경로가 사라진다.
- Claude Code plugin ecosystem의 실제 strengths를 reflect가 활용하지 못한다.

## 단계적 도입안

### Phase 1
- taxonomy를 문서와 contract에 반영
- receipt 섹션 확장
- hook/command/agent는 suggest only

### Phase 2
- proposal skeleton format 정교화
- hook candidate rationale template 추가
- command / agent proposal snippet format 추가

### Phase 3
- optional helper docs 추가
- hookify integration guidance를 optional docs로만 제공
- 필요 시 dry-run promotion report artifact 저장 형식 검토

## 검증 계획

1. `README.md`, `commands/reflect.md`, `docs/reflect-file-policy.md`가 같은 taxonomy를 설명하는지 확인
2. `reflect` output contract가 rule/skill/hook/command/agent/discard를 모두 표현 가능한지 검토
3. shared repo rule auto-edit 금지 경계가 유지되는지 확인
4. hook / command / agent proposal이 설치된 active surface처럼 과장되지 않는지 확인
5. branch-specific one-off discard rule이 examples와 금지 항목에 반영됐는지 확인

## 오픈소스 생태계와의 위치

이 RFC는 TigerKit을 다음 중 어디에도 완전히 같게 만들지 않는다.

- full self-improvement runtime (Hermes)
- session-wide governance methodology (Superpowers / Vowline)
- generic skill library
- hook-only behavior shaper

대신 TigerKit을 다음 위치에 더 선명하게 둔다.

> **TigerKit = lightweight Claude Code plugin for SoT-first gap analysis and reflection-driven promotion routing**

즉, TigerKit `reflect`는 “배움을 적는 회고”가 아니라 **배움을 rule / skill / hook / command / agent 중 어디로 승격할지 결정하는 command**가 된다.

## 결론

TigerKit `reflect`를 skill-only learning capture로 두는 것보다, promotion target taxonomy를 가진 router로 확장하는 편이 더 설명 가능하고 더 실용적이다.

이 변경은 TigerKit의 lightweight identity를 해치지 않으면서도, Claude Code plugin ecosystem의 실제 실행 표면(rule / skill / hook / command / agent)을 더 정직하게 반영한다.

따라서 이번 RFC는 `reflect`를 **safe durable promotion router**로 재정의하는 변경을 제안한다.
