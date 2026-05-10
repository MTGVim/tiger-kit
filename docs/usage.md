# 사용법

## 언어

명령은 사용자에게 한글로 답하고 작업 산출물도 한글로 작성합니다. 인용한 원문, 코드, 명령어, 경로, 식별자는 원문 그대로 유지할 수 있습니다.

## 브랜치와 작업 ID

변경 가능한 작업 산출물을 쓰기 전에 작업과 연결되는 브랜치 또는 작업 ID를 우선 사용합니다. 현재 브랜치가 `main`, `master`, `develop` 또는 저장소 기본 브랜치라면 작업 브랜치를 만들거나 전환할지, 또는 `.tigerkit/{work_id}/` 아래에서 사용할 작업 ID를 정할지 물어봅니다.

브랜치 생성과 전환은 사용자 승인 없이 조용히 수행하지 않습니다.

## 권장 흐름

```text
/tk:prep      # 요구사항 기준 정리
/tk:gap       # 기준 대비 갭 분석
/tk:plan      # 실행계획 정리
/tk:breakdown  # task 분해
/tk:tasks     # task 상태 관리
/tk:next      # 다음 task 하나 선택
/tk:close     # 종료 전 정리
```

## 1. 답변 해독

긴 LLM 답변, 애매한 설명, 회의록식 덤프가 결국 무슨 말인지 모르겠을 때 실행합니다.

```text
/tk:mwhat <긴 답변, 설명, 또는 정리 요청>
```

`/tk:mwhat`은 command-only입니다. 자연어 자동 트리거용 skill을 등록하지 않습니다.

기본 출력은 두 블록입니다.

```text
뭣? 쉽게 말하면
추천
```

`뭣? 쉽게 말하면`은 최대 3줄, `추천`은 최대 2줄로 유지합니다. 추천은 `이렇게 말하세요: ...` 또는 `이렇게 하세요: ...` 형식으로 적습니다.

이 명령은 코드를 구현하거나 파일을 수정하지 않습니다. 먼저 말뜻과 문제 상황을 짧게 풀고, 사용자가 말하거나 할 수 있는 추천을 제시합니다.

## 2. 요구사항 기준 정리

아이디어, 앞선 대화, 파일 경로, 기획서 URL, 티켓, 메모를 갭 분석 기준으로 정리할 때 실행합니다.

```text
/tk:prep <아이디어, 자료, 또는 정리 요청>
```

이 명령은 먼저 다음을 확인합니다.

1. 앞선 대화 내용을 바탕으로 바로 정리할지
2. 별도 자료를 추가로 제공할지: 파일 경로, 기획서 URL, 티켓, 메모, 스크린샷 등
3. 추론한 스펙명 또는 작업 ID를 그대로 사용할지

아이디어가 흐릿하면 긴 질문지 대신 문제, 목표, 제외 범위, 검증 방법만 짧게 좁힙니다.

주요 산출물:

```text
.tigerkit/{work_id}/requirements.md
.tigerkit/{work_id}/requirements.meta.json
```

동일한 입력 자료, prep 지시문 버전, 범위, input identity로 다시 실행하면 기존 `requirements.md`를 재사용합니다. 하나라도 다르거나 `--force`를 붙이면 다시 생성합니다.

실행 후 채팅 응답은 생성/재사용 여부, 파일 경로, 3줄 이내 요약만 짧게 표시합니다.

## 3. 갭 분석

준비된 요구사항 기준과 현재 구현, 문서, 테스트, 관찰 가능한 동작 사이의 차이를 분석할 때 실행합니다.

```text
/tk:gap
```

`gap`은 다음 파일을 기준으로 분석합니다.

```text
.tigerkit/{work_id}/requirements.md
```

요구사항 기준 파일이 없거나 어떤 작업을 분석해야 하는지 불명확하면 분석을 시작하지 않고 `/tk:prep`로 기준 자료를 먼저 정리하라고 안내합니다.

주요 산출물:

```text
.tigerkit/{work_id}/gap.md
.tigerkit/{work_id}/gap.meta.json
```

동일한 git commit, requirements 해시, gap 지시문 버전, 범위로 다시 실행하고 작업 트리가 clean이면 기존 `gap.md`를 재사용합니다. 하나라도 다르거나 작업 트리가 dirty이거나 `--force`를 붙이면 다시 분석합니다.

실행 후 채팅 응답은 전체 보고서를 길게 출력하지 않고, 보고서 경로, Verdict, 핵심 gap, next move 1개만 표시합니다.

보고서는 다음을 분리해서 정리합니다.

- Verdict
- Requirement Coverage
- Remaining Gaps
- Unable to Verify
- Notes

`Requirement Coverage`, `Remaining Gaps`, `Unable to Verify`는 항상 Markdown 표로 작성합니다. 해당 항목이 없더라도 표 섹션과 헤더를 생략하지 않고 `없음` 행을 남깁니다.

각 finding은 요구사항 ID, 상태, 근거, 갭, 다음 행동을 포함합니다.

분석 후에는 특정 계획/실행 명령으로 자동 연결하지 않습니다. 보고서 끝의 `Next Move` 하나를 참고해 사용자가 구현, 보류, 추가 확인 같은 다음 행동을 고릅니다.

## 4. 실행계획

`requirements.md` 또는 `gap.md` 기준으로 구현 전에 실행 순서와 검증 방식을 정리할 때 실행합니다.

```text
/tk:plan
```

주요 산출물:

```text
.tigerkit/{work_id}/plan.md
```

계획에는 Context, Recommended Approach, Task Breakdown, Dependencies, Verification을 포함합니다.

`plan`은 승인 전 `tasks.md`를 만들지 않습니다. 사용자가 구현을 요청하지 않았다면 코드를 수정하지 않습니다.

## 5. task 분해

`gap.md` 또는 `plan.md`를 작은 실행 task로 내릴 때 실행합니다.

```text
/tk:breakdown
```

주요 산출물:

```text
.tigerkit/{work_id}/tasks.md
```

각 task는 ID, 상태, 목적, 체크리스트, 완료 기준, blocker를 짧게 포함합니다. 상태값은 `todo`, `in_progress`, `blocked`, `done`, `dropped`만 사용합니다.

## 6. task 상태 관리

작업 목록을 만들거나 현재 상태를 업데이트할 때 실행합니다.

```text
/tk:tasks
```

출력은 현재 task, 완료 수, blocked 수, 다음 후보 1개만 짧게 표시합니다.

## 7. 다음 task 선택

지금 할 일 하나만 고를 때 실행합니다.

```text
/tk:next
```

선택 규칙:

- `in_progress`가 있으면 그것을 우선 표시합니다.
- `in_progress`가 없으면 첫 번째 `todo`를 표시합니다.
- `blocked`, `done`, `dropped`는 실행 후보에서 제외합니다.

`tasks.md`가 없으면 새로 만들지 않고 `/tk:breakdown` 또는 `/tk:tasks` 실행을 제안합니다.

## 8. 종료 정리

세션 종료 전 남은 gap, task, 검증, cleanup 후보를 정리할 때 실행합니다.

```text
/tk:close
```

기본 출력은 `Close Report`입니다. 필요하면 사용자의 승인 후 `.tigerkit/{work_id}/close.md`를 작성할 수 있습니다.

확인 항목:

- 남은 gap 또는 blocked task
- 완료한 task와 아직 남은 task
- 실행한 검증과 실패한 검증
- archive 또는 cleanup 후보
- 다음에 이어갈 명령 1개

branch 생성, commit, push, PR 생성, 파일 삭제는 사용자 승인 없이 실행하지 않습니다.

## 9. 계획 압박 질문

구현 전에 계획, 설계, 결정의 허점을 파고들 때 실행합니다.

```text
/tk:grill-me
```

활성 세션 중에는 응답 한 턴에 질문 하나만 합니다. 질문 전에 현재 working assumption과 추천 기본값을 짧게 밝히고, 답이 모호하면 더 좁혀 묻습니다.

## 10. 초압축 응답 모드

응답을 더 짧게 만들고 싶을 때 실행합니다.

```text
/tk:caveman
```

`/tk:caveman`은 `caveman` skill alias입니다. 자연어로 `caveman mode`, `less tokens`, `be brief`처럼 요청해도 활성화될 수 있습니다.

기술 용어, 코드 블록, 오류 메시지는 유지하고 filler와 장황한 설명을 줄입니다. 보안 경고, 되돌리기 어려운 action 확인, 순서가 중요한 절차에서는 일시적으로 더 명확히 씁니다.

## 11. skill 작성

새 Claude Code skill을 만들거나 기존 skill을 가볍게 고칠 때는 `write-a-skill` skill을 사용합니다.

자연어 예시:

```text
새 skill 하나 만들어줘.
skill-creator 말고 짧은 SKILL.md로 정리해줘.
이 workflow를 skill로 바꿔줘.
```

기본은 `skills/{skill-name}/SKILL.md` 하나입니다. reference나 scripts는 필요할 때만 추가합니다.

## 12. FE prototype 범위 정리

프론트엔드 화면 결정을 production 코드로 확정하기 전에 브라우저에서 비교 가능한 throwaway UI prototype으로 검증할 때 실행합니다.

```text
/tk:prototype
```

기본 방식은 기존 page에 붙이고, `?variant=` URL search param으로 3개 variant를 전환하는 것입니다. 관련 기존 page가 없을 때만 `prototype` 이름이 드러나는 throwaway route를 만듭니다.

variant는 색이나 copy 차이가 아니라 layout, information hierarchy, primary affordance가 구조적으로 달라야 합니다. 화면 하단에는 prototype 전용 floating switcher를 두고, production build에서는 숨깁니다.

완료 후에는 winner와 이유만 남기고 loser variant와 switcher를 삭제합니다. 명시적으로 요청받지 않는 한 코드를 구현하지 않습니다.

## 13. 세션 회고

현재 세션에서 반복된 교정 포인트, 놓친 확인 절차, 다음부터 줄이고 싶은 실수를 짧게 회고할 때 실행합니다.

```text
/tk:reflect
```

`/tk:reflect`는 maintenance alias로 유지합니다. 종료 루틴은 `/tk:close`를 우선합니다.

주요 출력은 `Session Reflection` 형식의 짧은 회고 보고서입니다. 이 명령은 사용자 사전 승인 없이 파일을 수정하지 않습니다. hook, queue, 히스토리 스캔, 자동 memory capture를 수행하지 않고, 현재 세션에서 드러난 내용만 바탕으로 patch proposal 또는 다음 확인 포인트를 정리합니다.

## 14. Knowledge layer 개선 audit

저장소의 CLAUDE.md, command 문서, 운영 메모처럼 knowledge layer에 해당하는 내용을 가볍게 점검하고 개선 후보를 찾고 싶을 때 실행합니다.

```text
/tk:improve
```

주요 출력은 `Improve Report` 형식의 audit finding과 patch proposal입니다. 보고서는 우선순위가 있는 개선 후보를 제안하지만, 범위가 큰 전면 재작성으로 바로 이어지지 않으며 변경을 자동 적용하지도 않습니다. finding ID(`IMP-001` 같은 식별자)는 `Findings` 표와 `Proposed Patches` 요약/상세 섹션에서 같은 값으로 반복해 승인 대상을 쉽게 고를 수 있게 유지합니다.

## 검증

TigerKit 저장소에는 package manager 기반 build/test/lint 설정이 없습니다. 명령, manifest, eval fixture를 수정한 뒤에는 다음 검증을 기본으로 실행합니다.

```bash
claude plugin validate .claude-plugin/plugin.json
claude plugin validate .
git diff --check
```

Eval fixture를 수정했다면 JSON 문법도 확인합니다.

```bash
python3 -m json.tool evals/evals.json >/dev/null
```

현재 저장소 안에서 확인되는 eval 자산은 다음 하나입니다.

| 경로 | 역할 | 현재 가능한 검증 |
| --- | --- | --- |
| `evals/evals.json` | TigerKit command 흐름의 기대 동작 fixture (`expectations` 필드 사용) | `python3 -m json.tool`로 JSON 문법 확인, fixture prompt/expectation 수동 검토 |

Claude CLI의 plugin 명령에는 현재 `validate`가 있지만, 이 저장소의 eval fixture를 자동 실행하는 공식 harness나 명령은 저장소 안에서 확인되지 않습니다. 따라서 “fixture는 있으나 자동 실행 경로는 확인 필요”로 보고하고, 자동 판정이 필요한 변경에서는 별도 eval harness 제공 여부를 먼저 확인해야 합니다.

## 추천 명령 문장

```text
/tk:mwhat 이 긴 답변 뭐라는 건지 정리해줘.
/tk:prep 앞선 대화 기준으로 요구사항 정리해줘.
/tk:gap 방금 정리한 요구사항 대비 현재 구현 갭 분석해줘.
/tk:plan 이 gap 기준으로 실행계획 세워줘.
/tk:breakdown gap을 실행 task로 쪼개줘.
/tk:next 다음 task 하나만 골라줘.
/tk:close 이번 세션 종료 정리해줘.
/tk:improve 이 저장소 knowledge layer 개선 후보를 audit해줘.
```
