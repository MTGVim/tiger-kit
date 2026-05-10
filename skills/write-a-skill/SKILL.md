---
name: write-a-skill
description: 새 Claude Code skill을 짧고 실용적인 구조로 작성합니다. Use when user wants to create, write, simplify, replace, or refine a skill, especially when they want a lighter alternative to a verbose skill creator.
---

# Write A Skill

새 skill을 만들거나 기존 skill을 가볍게 고칩니다.
목표는 장황한 framework가 아니라, 바로 설치 가능한 `SKILL.md`를 만드는 것입니다.

## Workflow

1. 요구를 짧게 확인합니다.
   - skill이 다룰 task 또는 domain
   - trigger 문장 또는 상황
   - instruction만 필요한지, reference나 script도 필요한지
   - 참고할 기존 자료

2. 구조를 최소로 잡습니다.
   - 기본은 `skills/{skill-name}/SKILL.md` 하나
   - 드문 reference만 `REFERENCE.md`나 `EXAMPLES.md`로 분리
   - 반복적이고 deterministic한 작업만 `scripts/`로 분리

3. `SKILL.md` 초안을 작성합니다.
   - frontmatter는 `name`, `description`
   - 본문은 목적, workflow, rules, do not 중심
   - `description`은 capability와 trigger를 구체적으로 적습니다.

4. 검토 포인트를 짧게 확인합니다.
   - trigger가 맞는지
   - 빠진 use case가 있는지
   - 너무 길거나 모호한 부분이 있는지

## Description rules

- 1024자 이하
- 첫 문장은 capability
- 둘째 문장은 `Use when ...` trigger
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

- 기본 산출물은 `SKILL.md` 하나
- `SKILL.md`는 가능하면 70줄 안팎
- 긴 template는 inline으로 늘어놓지 말고 필요할 때만 별도 파일로 분리
- 오래 변하는 버전, 날짜, 외부 상태 넣지 않기
- broad automation보다 명확한 workflow 우선
