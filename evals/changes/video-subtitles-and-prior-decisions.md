# 자막 전제조건과 선행 결정

`ffmpeg` 실행 파일이 있어도 자막 필터가 없으면 기존 조립기는 원인 없이 실패했습니다. 관련 회귀 시험의 `RED`를 확인한 뒤, 필터 조회와 명시적인 자막 옵션, MP4 소프트 자막·SRT 및 GIF·SRT 보존을 추가했습니다. 구운 자막의 완료 상태는 `blocked`, 전제조건은 `ffmpeg-subtitles-filter`이고 자동 설치하지 않습니다. 영상 생성·실제 앱 판정·게시 권한은 독립적으로 유지합니다.

`tk-retro`는 대상 저장소의 관련 `.tigerkit/retro/`에서 선행 결정을 읽고 충돌을 재검토로 표시합니다. 기존 `10fps`와 `ASR` 미도입 결정을 다시 제안하지 않습니다.

출처는 `obra/superpowers`의 병합 커밋 `dd53fe0b57223bbbbb8ceae0bda2ba8a26d1c29a`에 있는 `assembling.md`이며, 필터 전제조건과 명시 옵션만 적응합니다. 해당 구현은 #2335에서 릴리스 품질 사유로 제거되었으므로 코드를 가져오지 않습니다. 내레이션 재전사·`30fps`·자동 설치·터미널 릴은 도입하지 않습니다.

`README: no public change`. 대상은 `skills/tk-browser-verify/scripts/build_movie.py`, 조건부 참조와 `skills/tk-retro/SKILL.md`이며 공개 카탈로그 호출 방식은 바뀌지 않습니다. `tk-prep/references/runtime-verification.md`에는 영상 제안 계약이 이미 존재합니다.
