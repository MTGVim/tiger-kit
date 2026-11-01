<a id="sdd-artifact-transport"></a>
# SDD 산출물 전달

정확한 콘텐츠를 직접 전달할 수 없고 자식에게 파일 기반 자료가 필요할 때만 읽습니다.


Unit 요약, 보고서와 정확한 diff에는 직접 호스트 payload와 자식 반환값을 우선합니다. 현재 호스트가 정보를 충실히 전달할 수 있다면 정보를 넘기기 위해 산출물을 파일로 만들지 않습니다.

자식에게 파일 경로가 필요하거나, 호스트 인터페이스로 정확한 묶음을 안정적으로 전달할 수 없거나, 제한된 맥락 크기로 파일 전달이 필요할 때만 평면적인 `.tigerkit/sdd-tmp/`를 사용합니다. 첫 쓰기 전에 [산출물 경로](../../tk-artifacts/references/artifact-paths.md)를 읽고 `git check-ignore -q -- .tigerkit/`로 Git의 실제 ignore 규칙이 `.tigerkit/`를 포함함을 입증하며 `git ls-files -- .tigerkit/`가 추적 경로를 반환하지 않는지 검증합니다. 디렉터리별 `.gitignore`, `.git/info/exclude`와 설정된 사용자 수준 제외 소스는 모두 유효합니다. 제외 범위가 부족하면 담당 SKILL.md의 Artifact Paths 설정을 적용한 뒤 다시 확인합니다. 필요한 파일 전달이 여전히 제외되지 않거나, 쓰기 불가능하거나, 자식에게 보이지 않으면 운영체제 임시 경로로 대체하지 않습니다. 디스패치 전에 `Blocked | Unverifiable`을 반환합니다.

실행별 또는 계획별 계층을 만들지 않습니다. Seed 식별자, `Unit`과 범위를 포함한 고유 파일명을 사용합니다. 실행 소유 파일만 정리하고 무관한 파일은 삭제하지 않습니다. 산출물에 비밀을 넣지 않습니다.

