# GitHub

<a id="draft-shape-and-formatting"></a>
## 초안 구성과 서식

- GitHub Flavored Markdown을 사용하되, 일반 댓글은 보고서식 제목 없이 짧고 서로 연결되는 몇 개의 문단으로 작성합니다. 핵심 요청 앞에 구체적인 동작과 충분한 맥락을 제시합니다. 식별자, API 경로, 파일명, 상태와 짧은 로그 발췌에는 인라인 코드를 사용하고, 긴 발췌가 필요할 때만 fenced block을 사용합니다.
- 코드 근거를 댓글에서 설명합니다. 기본적으로 코드나 다른 출처 링크를 추가하지 않습니다. 사용자가 출처 링크를 요청하지 않았다면 유용한 이슈나 pull request 링크만 포함합니다. 사용자가 코드 permalink를 요청하면 검증된 commit SHA와 줄 범위로 고정합니다.
- GitHub 식별 정보가 검증된 경우에만 사람이나 팀을 멘션합니다. 유효한 멘션은 저장소 접근 조건이 허용할 때 대상에게 알림을 보낼 수 있습니다. 식별 정보를 모르면 명확한 placeholder를 남깁니다.
- 병합 후 연결된 이슈를 닫으려는 의도가 있을 때만 pull request 설명이나 commit 메시지에 지원되는 이슈 종결 키워드를 넣습니다. 대화 중 일반적인 이슈 참조도 링크를 만들 수 있으므로 유용할 때만 교차 참조를 포함합니다.

<a id="official-references"></a>
## 공식 참조

- [기본 작성 및 서식 문법](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
- [표로 정보 정리하기](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-tables)
- [접힌 구획으로 정보 정리하기](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-collapsed-sections)
- [코드 발췌에 대한 영구 링크 만들기](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-a-permanent-link-to-a-code-snippet)
- [pull request를 이슈에 연결하기](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue)
