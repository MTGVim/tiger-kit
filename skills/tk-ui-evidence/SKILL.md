---
name: tk-ui-evidence
description: "[user/auto] UI 문구·진입 경로의 근거 수집 및 전달 기준을 참조할 때 사용합니다. 실제 업무 실행이나 변경 권한을 부여하지 않습니다."
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

이 스킬에서 질문·메시지·설명·보고서·Markdown·HTML·대본·자막·문서·스킬 본문 등 사람이 읽는 텍스트를 **새로 작성하거나 의미·표현을 수정하기 전에**, 설치된 `tk-writing`의 [모든 저작의 공통 관문](../tk-writing/references/authoring-gate.md)과 [명확한 글쓰기](../tk-writing/references/clear-writing.md)를 이번 작업에서 읽고 적용합니다. 최종 산출물을 인계하기 전에 같은 기준으로 원고를 검사하고 문제를 수정합니다. 이미 읽은 기준을 반복 로드하거나 별도 재작성 스킬·에이전트·승인 라운드를 추가하지 않습니다. 코드·명령·식별자·기계 판독 형식·인용과 고정 문구는 보호하며, 이 참조로 변경·전송·발행 권한이 생기지 않습니다. 이 스킬이 작성 작업을 수행하지 않는 경우에는 추가 읽기가 필요하지 않습니다.
<!-- /tigerkit:universal-authoring-gate -->


<a id="shared-ui-evidence"></a>
# 공통 UI 근거

아래 조건이 성립하는 참조만 읽고 기준과 공백을 호출자에게 반환합니다. 호출자는 범위, 승인과 완료에 대한 책임을 유지합니다. 참조는 워크플로를 호출하지 않으며 설치, 변경, 비밀, Git 또는 발행 권한을 부여하지 않습니다.

소유 스킬은 기억, 다른 설치본, 하드코딩한 홈이나 소스 checkout fallback이 아니라 현재 설치된 스킬 모음(`dependencies.json`)에서 확인합니다. 소유 스킬이나 자원이 없거나 식별이 다르면 해당 행동을 중단합니다. `tk-setup-skills`를 안내하며 몰래 설치하지 않습니다. `<package>`, "package-local"과 "this package"는 링크가 다른 소유자를 명시하지 않는 한 호출자의 설치된 패키지를 뜻합니다.

<a id="conditional-references"></a>
## 조건부 참조

- [UI 근거](references/ui-evidence.md): UI label과 진입 경로를 수집, 검증 또는 보고할 때 읽습니다.
