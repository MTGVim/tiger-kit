---
name: write-a-skill
description: 새 Claude Code skill을 짧고 실용적인 구조로 작성합니다. Use when user wants to create, write, simplify, replace, or refine a skill, especially when they want a lighter alternative to a verbose skill creator.
---

# Write A Skill

새 skill을 만들거나 기존 skill을 가볍게 고칩니다.
목표는 장황한 framework가 아니라, 바로 설치 가능한 `SKILL.md`를 만드는 것입니다.

## Process

1. 요구를 짧게 확인합니다.
   - skill이 다룰 task/domain
   - trigger 문장 또는 상황
   - instruction만 필요한지, reference/script도 필요한지
   - 참고할 기존 자료

2. skill 구조를 고릅니다.
   - 기본은 `skills/{skill-name}/SKILL.md` 하나
   - `SKILL.md`가 길어지거나 드문 reference가 있으면 별도 파일로 분리
   - 반복적이고 deterministic한 작업만 `scripts/`로 분리

3. draft를 작성합니다.
   - frontmatter: `name`, `description`
   - 본문: 목적, workflow, 규칙, 금지사항, 필요한 예시
   - description은 agent가 trigger 판단에 쓰는 유일한 요약이라고 보고 구체적으로 씁니다.

4. 사용자에게 검토 포인트를 짧게 묻습니다.
   - trigger가 맞는지
   - 빠진 use case가 있는지
   - 너무 길거나 모호한 부분이 있는지

## Structure

```text
skill-name/
  SKILL.md
  REFERENCE.md   # 필요할 때만
  EXAMPLES.md    # 필요할 때만
  scripts/       # 필요할 때만
```

## SKILL.md template

```md
---
name: skill-name
description: Capability summary. Use when [specific triggers].
---

# Skill Name

## Purpose

...

## Workflow

1. ...
2. ...
3. ...

## Rules

- ...

## Do not

- ...
```

## Description rules

- 1024자 이하
- 3인칭으로 작성
- 첫 문장: capability
- 둘째 문장: `Use when ...` trigger
- 애매한 설명 금지

좋음:

```text
Create and refine lightweight Claude Code skills with concise SKILL.md files. Use when user asks to create, replace, simplify, or tune a skill.
```

나쁨:

```text
Helps with skills.
```

## Keep it small

- `SKILL.md`는 가능하면 100줄 이하
- 오래 변하는 버전/날짜/외부 상태 넣지 않기
- reference는 한 단계 깊이까지만 링크
- 예시는 적게, trigger와 edge case 중심
- broad automation보다 명확한 workflow 우선
