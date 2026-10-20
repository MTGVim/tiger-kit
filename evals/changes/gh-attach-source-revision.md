# `gh-attach` 검토 소스 고정

`enthus-appdev/gh-attach`의 `v0.7.0`은 `annotated` `tag` 객체
`55660547092ef379f23a9d887fb48f67fd408b30`을 거쳐 `commit`
`663d13d6e42b98eadf6f1d9a517813b8a0f4eaf1`을 가리킵니다. GitHub Git `refs`/`tags` API로 확인했습니다.
기본 설치 경로는 이 `upstream`으로 바꾸며, 바이너리 확장의 태그 기반 설치 방식은 유지합니다.

기존 `MTGVim/gh-attach`의 `v0.7.0-mtgvim.1`은 `commit`
`77e51e2a0b8e099b6e9fc7310ad0c2d5a319c60b`으로 확인했습니다. 기존 설치와 별도 승인된 설치의
호환 경로로 보존하며, 저장소 공개 범위를 변경하거나 `private` `mirror`를 만들지 않습니다.

검토된 분류에는 태그를 `commit`까지 해제한 전체 SHA 일치가 필요합니다. 이동한 `upstream` 태그는
미검토 상태이며, 조회 실패나 포크 불일치는 출처 미확인 상태입니다. 매핑을 모르는 상태에서는
도움말도 실행하지 않고, 이동한 태그 재설치를 복구책으로 제시하지 않습니다. 소스 `commit` 고정은
설치된 실행 파일 바이트의 무결성 증명과 구분합니다.

새 평가 네 개는 태그 이동, `annotated` `tag` 해제, 조회 실패, 승인된 `upstream` 설치 후 재검증을 다룹니다.
기본 설치 경로를 소유한 기존 평가 두 개는 명시적 `migration`으로 바꾸고, 기존 승인·업로드 경계는 유지합니다.
추가 지시는 `gh-attach` 경로에서만 읽는 참조에 두며 다른 스킬과 공통 질문 참조는 바꾸지 않습니다.

`README: no public change`. `skills/tk-pr-media/references/gh-attach.md`의 설치·검토 절차만 바뀌며
`README.md`가 소유하는 스킬명, 호출 방식, 카탈로그 설명은 바뀌지 않습니다.
