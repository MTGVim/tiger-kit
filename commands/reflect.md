---
description: 현재 세션에서 드러난 재사용 가능한 convention, 용어, agent 교정사항을 추출하고 patch 후보를 제안합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 인용한 원문, 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

목표: 현재 세션 conversation에서 재사용 가능한 learning 후보를 추출하고, `CLAUDE.md`, `AGENTS.md`, `.claude/rules`, command docs, README/docs 같은 knowledge source를 기준으로 convention, 용어, agent 교정사항을 정리해 patch 후보를 제안합니다.

기본 출력은 `Session Reflection` 보고서입니다. 명시적으로 승인받지 않는 한 어떤 파일도 수정하지 않습니다.

hook, queue, history scan, automatic memory capture, automatic apply를 구현하거나 실행하지 않습니다.
