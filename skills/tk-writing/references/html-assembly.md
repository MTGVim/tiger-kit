<a id="document-assembly"></a>
# 문서 조립

담당 워크플로가 공통 reader 셸을 선택할 때만 이 기존 공통 문서 빌더를 사용합니다.
설명과 조사에서도 [렌더러 계약](renderer-contract.md)에 따라 일반 문서형 HTML을 선택하면 이 빌더를 사용합니다.
선택한 archify의 실패 대체 경로는 아닙니다. 고유 구조로 독립 작성한 기법 HTML에는 이 셸 요구가 적용되지 않습니다.
공통 reader 문서를 선택했다면 조각을 작성하고 설치된 `tk-writing` 빌더를 실행합니다.
편집에는 생성기를 재사용하며, 특화된 prototype/QA/갤러리 인터페이스는 자체 생성기를 유지합니다.

조각은 승인된 실행 임시 공간에 둡니다. 본문에는 도입 설명과 적절한 중첩 제목 수준을 갖춘
`<section id="..."><h2>...</h2>...</section>` 단위를 넣습니다.
빌더가 title/h1, 상단 바, reader 제어, 계층형 목차, 이동 링크와 변경하지 않은 테마 자산을 제공합니다.
단순히 인라인으로 넣으려고 이 자산을 읽거나 재현하지 않습니다. 구체적인 결함/변경이 있을 때만 구현을 검사합니다.

```bash
python3 <tk-writing>/scripts/build_html.py --body <scratch>/body.html --title '<subject>' --output <final>.html
python3 <tk-writing>/scripts/package_html.py --root <final-directory> --name <filename>.html <filename>.html
python3 <tk-writing>/scripts/package_html.py --check --root <final-directory> --name <filename>.html <filename>.html
```

`<tk-writing>`은 호출자나 소스 checkout이 아닌 현재 설치된 모음의 해당 소유 스킬로 해석합니다.
임시 파일과 최종 출력은 설치된 패키지 밖에 두고 기존 출력 디렉터리를 사용합니다. `--replace`에는 덮어쓰기 권한이 필요합니다.
선택적 UTF-8 `--css`, `--script`, `--footer` 파일은 내용에 한정된 스타일, 검토한 오프라인 도해 코드와 출처 마크업을 제공합니다.
원본/코드와 script/style 종료 시퀀스를 이스케이프합니다.
`--lang`은 언어를 바꿉니다. `--theme`은 명시적 테마를 따르고, 그렇지 않으면 HTML 출력에 따라 설정을 결정/초기화합니다.
출력된 생성/대체 안내를 완료 보고에 전달합니다. 연결된 수업은 위의 단일 파일 명령 대신 최종 모음 내보내기 허용 목록을 사용합니다.
`--check`는 파일을 쓰지 않고 각 HTML의 payload·진입 경로·manifest와 허용 목록 전체의 최종 바이트를 대조합니다.
studio 주입을 포함한 최종 편집 뒤 같은 허용 목록으로 다시 패키징하고 검사합니다. 누락·손상·중복·오래된 payload는 전달 실패입니다.

사전 점검은 조각 균형, 섹션 제목, ID/대상과 summary 배치를 검사하고 공통 테마에 없는 클래스를 경고합니다.
완전한 정적/오프라인 검증이나 산문/렌더링/학습 판정은 아닙니다. 담당자의 모든 내용/출처/연습 검사와 HTML 출력 검사를 보존합니다.
조립한 셸만으로 설명/수업 제작에 브라우저 검증을 요청한 것이 되지는 않습니다.
화면/행동 검사를 명시적으로 요청하면 먼저 내용을 확정하고 호환되는 검사를 묶어 수행하며 기존 재실행 규칙을 보존합니다.
조각을 편집하고 영향을 받은 출력을 다시 빌드합니다.

<a id="reader-compatibility"></a>
## Reader 호환성

`--profile reader`만 지원하며 계속 기본값입니다. 탐색은 계층형으로 유지합니다.
이전 빌더 선택지 `lesson`과 `change`에는 포함된 자산이 없어 문서를 빌드할 수 없었습니다.
이 선택지는 제거한 것이며 대체 경로로 바꾼 것이 아닙니다. `tk-explain`의 워크플로 모드나 선택한 렌더러는 바뀌지 않습니다.
