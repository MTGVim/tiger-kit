---
name: tk-artifacts
description: "[user/auto] 파일 산출물 경로와 사용자 비밀 입력·인증 보존의 공통 안전 기준을 조회할 때 사용합니다. 에이전트가 사용자 인증정보를 받아야 하는 실제 절차와 파일 경로 인계는 tk-wizard가 담당합니다. 참조는 업무 실행이나 변경 권한을 부여하지 않습니다."
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


<a id="shared-artifact-safety"></a>
# 공통 산출물 안전 기준

아래 조건을 충족하는 참조만 읽고 기준과 부족한 사항을 호출자에게 반환합니다. 범위, 승인과 완료에 대한 책임은 호출자에게 있습니다. 참조는 워크플로를 호출하지 않으며 설치, 변경, 비밀 접근, Git 또는 발행 권한을 부여하지 않습니다.

소유 스킬은 현재 설치된 스킬 모음(`dependencies.json`)에서 확인합니다. 기억, 다른 설치본, 하드코딩된 홈 경로나 소스 checkout 대신 현재 설치된 소유 스킬의 경로를 사용합니다. 소유 스킬이나 자원이 없거나 식별이 다르면 해당 행동을 중단하고 `tk-setup-skills`를 안내합니다. 필요한 설치는 별도 승인을 받은 뒤에 수행합니다.
`<package>`, "package-local", "this package"는 링크가 다른 소유자를 명시하지 않는 한 호출자의 설치된 패키지를 뜻합니다.

<a id="conditional-references"></a>
## 조건부 참조

- [산출물 경로](references/artifact-paths.md): 승인된 산출물이나 임시 입력을 쓰기 전에 읽습니다.
- [설정 조회 중 비밀 보호](references/artifact-paths.md#secret-safe-inspection): 환경변수나 비밀이 포함될 수 있는 설정을 조회하기 전에 읽습니다.
- [인증](references/authentication.md): 승인된 애플리케이션 인증 입력이나 갱신이 필요할 때 읽습니다.
