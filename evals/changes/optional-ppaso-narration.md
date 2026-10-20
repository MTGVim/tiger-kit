# 제거 가능한 `ppaso` 내레이션

내레이션은 `tk-browser-verify/references/narration.md`와
`scripts/narration/ppaso.py`, `ppaso-files.json`에 격리합니다. 실제 분기의 연결은
`motion-evidence.md` 한 곳이며, MP4 조립기는 일반 오디오 입력만 받습니다. 내레이션 파일·참조·연결과
전용 `scripts/test_optional_narration.py`를 제거해도 스크린샷·GIF·자막 MP4가 유지되도록 합니다.
내레이션 없는 격리 조립기에서 오디오 누락과 자막 MP4 생성을 실제 테스트합니다.

`akamotaco/ppaso-tts-v1`의 전체 `revision` `53d09664c4f636a5fb6f2ebe3ec22cd83ee249b9`에서
모델·추론 코드·설정·사전·라이선스·출처 파일 18개를 다운로드하여 실제 전체 SHA256을 계산하고 검증했습니다.
바이너리는 무시된 실행 소유 경로에만 두며 저장소나 `Release`에는 넣지 않습니다. 원본 모델의
`LICENSE`, 한국어 README와 제삼자 고지를 유지합니다. 저장소에 개인 `mirror`를 필수 의존성으로 추가하지 않습니다.

다운로드는 명시된 `--download`에서만 허용하고, 오프라인 검증은 네트워크와 추론 의존성을 불러오지 않습니다.
설치와 캐시는 실행 소유 가상환경에 격리하며 런타임 스킬은 사용자 승인 없는 자동 설치를 수행하지 않습니다.
원본 접근 실패나 엔진 누락은 자막 MP4를 유지합니다. 숫자·영어 발음은 작성한 대본과 사용자 사전에서 처리하고
음성 디코딩·유한 샘플·길이·무음을 검사합니다. 실제 청취와 장면 동기화는 별도 검수이며, 결정적 추론을
발음 정확성의 증거로 쓰지 않습니다. ASR 재전사나 `Whisper`는 도입하지 않았습니다.

README 공개 카탈로그는 내레이션만으로 추가 변경하지 않습니다. 출처는 고정 `revision`의
[모델 문서](https://huggingface.co/akamotaco/ppaso-tts-v1/blob/53d09664c4f636a5fb6f2ebe3ec22cd83ee249b9/README_ko.md)입니다.

스냅샷은 필수 파일뿐 아니라 전체 파일 집합을 검증하여 추가된 모델이나 초기화 코드의 우선 로딩을
차단합니다. 새 프로세스에서 검증된 `runtime` 경로와 `PPASO_LEXICON`을 고정하여 외부 패키지·사전의
영향도 차단합니다. 해당 환경변수가 잘못된 외부 경로를 가리키는 실제 합성에서도 고정 사전을 사용합니다.
