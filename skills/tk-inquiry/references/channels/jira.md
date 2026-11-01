# Jira

- 대상 화면이 초안을 실질적으로 바꾸는 경우에만 이를 확인합니다. Jira Cloud REST API v3의 댓글 본문은 Atlassian Document Format (ADF)을 사용합니다. Jira Server/Data Center와 레거시 연동은 Wiki Markup을 비롯한 다른 형식 경로를 사용할 수 있습니다. 가공하지 않은 Markdown이 의도대로 렌더링된다고 가정하지 않습니다.
- 일반적인 복사용 댓글은 제목 없이 짧고 서로 연결되는 몇 개의 문단으로 작성합니다. 구체적인 동작과 질문 또는 검토 요청을 명시합니다. 서로 다른 답변을 하기 쉬워질 때만 개별 질문에 번호를 붙입니다. 보고서식 구획과 불필요한 중첩이나 표를 피합니다.
- 관련 근거나 행동을 댓글에서 설명합니다. 기본적으로 코드나 다른 출처 링크를 추가하지 않습니다. 유용할 때만 관련 이슈 링크를 포함하고, 다른 링크에는 모순 예외를 포함한 본 스킬의 근거 링크 규칙을 따릅니다.
- 검증된 경우에만 이슈 키와 관련된 현재 상태를 명시합니다. 각 요청에 답하거나 요청을 종결하는 데 필요한 근거를 포함합니다.
- 의도한 Jira 계정이 검증되었고 목적지에서 해당 계정을 식별할 수 있을 때만 사람 멘션을 사용합니다. 멘션 문법이나 계정 식별자를 만들어 내지 않습니다.

<a id="official-references"></a>
## 공식 참조

- [Jira Cloud REST API v3](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/)
- [Atlassian Document Format](https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/)
- [Atlassian Document Format과 Wiki Markup 소개](https://developer.atlassian.com/platform/framework/adf-builder/technical/about-adf/)
