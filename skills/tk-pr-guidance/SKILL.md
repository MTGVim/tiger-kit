---
name: tk-pr-guidance
description: "[user/auto] PR 본문 GFM·시각 자료·다중 PR 전달·rebase 준비 기준을 참조할 때 사용합니다. 실제 업무 실행이나 변경 권한을 부여하지 않습니다."
disable-model-invocation: false
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: adapted
    role: reference
---
<!-- tigerkit:universal-authoring-gate -->
## 공통 저작 품질 관문

이 스킬에서 질문·메시지·설명·보고서·Markdown·HTML·대본·자막·문서·스킬 본문 등 사람이 읽는 텍스트를 **새로 작성하거나 의미·표현을 수정하기 전에**, 설치된 `tk-writing`의 [모든 저작의 공통 관문](../tk-writing/references/authoring-gate.md)과 [명확한 글쓰기](../tk-writing/references/clear-writing.md)를 이번 작업에서 읽고 적용합니다. 최종 산출물을 인계하기 전에 같은 기준으로 원고를 검사하고 문제를 수정합니다. 현재 작업에서 읽은 기준을 재사용하고 기존 작성·검증·승인 절차 안에서 적용합니다. 코드·명령·식별자·기계 판독 형식·인용과 고정 문구는 보호하며, 변경·전송·발행은 원래 승인된 범위에서만 수행합니다. 작성 작업을 수행할 때만 이 기준을 추가로 읽습니다.
<!-- /tigerkit:universal-authoring-gate -->


<a id="shared-pr-guidance"></a>
# 공통 PR 지침

아래 조건을 충족하는 참조만 읽고, 기준과 부족한 사항을 호출자에게 반환합니다.
범위, 승인과 완료 책임은 호출자가 유지합니다. 참조는 어떤 워크플로도 호출하지 않으며,
설치, 변경, 비밀 접근, Git 작업이나 발행 권한을 부여하지 않습니다.

현재 설치된 스킬 모음(`dependencies.json`)에서 소유자를 확인합니다. 기억,
다른 설치본, 하드코딩한 홈 경로나 소스 checkout으로 우회하지 않습니다. 소유자나 자원이
없거나 일치하지 않으면 해당 작업을 중단하고 `tk-setup-skills`를 안내하며, 필요한 설치는 별도 승인을 받은 뒤에 수행합니다.
`<package>`, "package-local"과 "this package"는 링크가 다른 소유자를 명시하지 않는 한 호출자가 설치한 패키지를 뜻합니다.

<a id="conditional-references"></a>
## 조건부 참조

- [GFM 렌더링](references/gfm-rendering.md): PR 본문·선택된 댓글을 생성하거나 갱신하기 직전, 미디어 섹션을 삽입할 때 읽습니다.
- [GitHub 시각 자료](references/github-visuals.md): PR에 사용할 시각적 근거를 준비할 때 읽습니다.
- [다중 PR 전달](references/multi-pr-delivery.md): 승인된 전달을 의도적으로 여러 PR로 나눌 때 읽습니다.
- [rebase 준비 상태](references/rebase-readiness.md): 특정 PR의 rebase를 준비하거나 rebase 담당자에게 인계할 때 읽습니다.
- [호스트 workspace와 setup 경계](references/workspace-setup.md): 새 workspace의 생성·초기화 경로를 선택하기 전에 읽습니다.
