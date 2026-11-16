---
name: tk-repository-guidance
description: "[user/auto] 저장소 맥락·도메인 문서·외부 계약의 조사 기준을 참조할 때 사용합니다. 실제 업무 실행이나 변경 권한을 부여하지 않습니다."
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


<a id="shared-repository-guidance"></a>
# 공통 저장소 지침

아래 조건에 해당하는 참조만 읽고 기준과 미확인 사항을 호출자에게 반환합니다. 범위, 승인과 완료 책임은 호출자가 유지합니다. 참조는 워크플로를 호출하지 않으며 설치, 변경, 비밀 접근, Git 또는 발행 권한을 부여하지 않습니다.

소유자는 기억, 다른 설치본, 하드코딩한 홈이나 소스 checkout 대체 경로가 아니라 현재 설치된 스킬 모음(`dependencies.json`)에서 확인합니다. 소유자나 자원이 없거나 일치하지 않으면 해당 행동을 중단합니다. 조용히 설치하지 말고 `tk-setup-skills`를 안내합니다.
`<package>`, "package-local"과 "this package"는 링크가 다른 소유자를 명시하지 않는 한 호출자의 설치된 패키지를 뜻합니다.

<a id="conditional-references"></a>
## 조건부 참조

- [도메인 맥락](references/domain-context.md): 저장소가 소유한 어휘나 도메인 의미가 작업에 영향을 줄 때 읽습니다.
- [외부 계약](references/external-contracts.md): 버전에 민감한 외부 계약을 로컬에서 확인할 수 없을 때 읽습니다.
- [저장소 맥락](references/repository-context.md): tracker 식별 정보, 저장소 설정 또는 검증 데이터 정책이 중요할 때 읽습니다.
