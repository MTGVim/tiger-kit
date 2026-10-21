# 나레이션 첫 실행의 의존성과 출처 표시

사용자 회고의 F1-F4를 `6328c30ca3f31c4da4bc97139ff5656274af1037`의 구현과
대조했습니다. F5는 기존 경로·소유권 검사와 실행 지침이 이미 담당하므로 규칙을 추가하지 않습니다.

- F1: 양쪽 엔진 매니페스트에 `soundfile==0.13.1`과 `libsndfile`을 포함한 플랫폼별
  `wheel` URL·SHA256을 고정합니다. `--verify`와 CLI 합성은 모델 접근 전에
  `numpy`, `soundfile`, `cffi`, 선택 엔진 모듈을 `find_spec`으로 확인하고 고정 패키지
  버전을 검사합니다. 실제 합성은 모델 로딩 전에 `soundfile`을 불러옵니다.
  `ModuleNotFoundError`는 정상적인 모듈 식별자만 반환하며 원시 예외 본문은 노출하지 않습니다.
  자동 설치와 최초 설치 승인 경계는 그대로 유지합니다.
- F2: 한국어 전용 합성의 함수·CLI·문서 기본값을 `sohee`로 변경합니다.
  명시적인 `serena` 선택과 요청 > 저장소 > 사용자 > 팀 > 기본값의 우선순위는 보존합니다.
  기존 MLX 기본 화자 평가를 이유가 명시된 개별 마이그레이션으로 갱신합니다.
- F3: 렌더링 카드에 사용자 언어의 모서리 출처 태그를 작성하고 검사합니다.
  프레임의 `source_in_picture: true` 선언은 자막 접두어를 생략하지만
  `source_kind: rendered`를 유지합니다. 미선언 시 `source_label`을 사용하며 기본값은
  `렌더링 장면`입니다. 출처 태그를 나레이션 자막의 대체물로 취급하지 않습니다.
- F4: 명시적으로 승인된 `--download`는 네트워크 전에 같은 저장소·리비전의 HF 캐시를
  확인합니다. 캐시 내부의 일반 파일과 `blob` 심볼릭 링크를 임시 일반 파일로 복사하고 해시가
  일치할 때만 소유 스냅샷에 수락합니다. 캐시 누락·불일치는 고정 다운로드로 복구하며,
  저장소 캐시 밖을 가리키는 심볼릭 링크는 재사용하지 않습니다. 원본 캐시와 기존 불일치
  스냅샷은 수정하거나 삭제하지 않습니다.

## 공식 근거와 증류

- [`mlx-audio 0.6.1`](https://pypi.org/project/mlx-audio/0.6.1/)의 고정 `wheel`
  `METADATA`에 `soundfile` 의존성이 없고,
  [`qwen-tts 0.1.1`](https://pypi.org/project/qwen-tts/0.1.1/)에는 있습니다.
  원래 가상환경의 설치 이력은 없으므로 당시 누락 경위를 단정하지 않습니다.
- [`soundfile 0.13.1`](https://pypi.org/project/soundfile/0.13.1/)의 배포 파일과
  소스 배포본의 `soundfile.py`, `tests/test_soundfile.py`를 확인했습니다. 플랫폼 `wheel` 여섯 개의
  SHA256을 실제 바이트로 검증하고 동봉된 `libsndfile` 파일을 확인했습니다.
  최신 `0.14.0`의 변경 기록도 확인했습니다. 동시 파일 열기 수정과 타입 주석,
  `Python <= 3.9` 지원 제거 및 추가 의존성이 있으며, 이번 순차 생성 경로는
  실제 왕복 검증을 마친 `0.13.1`을 고정합니다.
  소스의 동봉 라이브러리 로딩와 `test_write_float_data_to_pcm_file`,
  `test_libsndfile_version`을 참고하여 리눅스 `wheel`의 PCM16 쓰기·읽기 왕복도 확인했습니다.
  Python 모듈은 BSD-3-Clause이고 동봉 라이브러리는 LGPL이므로 전체 의존성을 MIT나
  `Apache`로만 설명하지 않습니다. 기존 엔진·모델 버전은 변경하지 않습니다.
- 화자 선택은 고정 모델 리비전과 사용자 근거, 공식
  [Qwen3-TTS 화자 표](https://github.com/QwenLM/Qwen3-TTS#custom-voice-generation)를
  대조했습니다. 음질 우열이나 억양 개선을 실측했다고 주장하지 않습니다.
- HF 캐시는 공식 [환경변수](https://huggingface.co/docs/huggingface_hub/en/package_reference/environment_variables)와
  [캐시 구조](https://huggingface.co/docs/huggingface_hub/en/guides/manage-cache)를 참고했습니다.
  유지: 고정 리비전·해시와 심볼릭 링크가 아닌 목적지. 적용: 로컬 캐시 바이트의 복사·재검증.
  제외: 캐시 삭제, HF 런타임 의존성, 자동 설치, 엔진 전환, 범용 설치 관리자.

## 검증 범위

빈 가상환경에 `NumPy` 탐색용 대역만 두고 CLI `--verify`를 실행하면 모델 경로에
접근하기 전에 `missing runtime module: soundfile`로 실패합니다. 엔진별 모듈과 고정
버전 검사, 기본 `sohee`와 명시 `serena`, 심볼릭 링크 캐시의 무네트워크 복사·해시 검증,
다른 리비전·불일치·캐시 밖 심볼릭 링크의 고정 다운로드 복구를 회귀 검사합니다.
그림 속 출처 선언 시 자막에 접두어가 붙지 않고, 실제 MP4 조립에서도 짧거나 빈
나레이션 자막은 `narration-subtitles-short`로 실패하는 동작을 보존합니다.

실제 `Apple Silicon` 추론과 사람이 듣는 음성 품질은 이번 환경에서 확인하지 않았습니다.
`human_action: listen`과 문장별 사전 검사, 설치 승인, 엔진 분리 및 무음 영상 경로를 유지합니다.

`README: no public change`. `tk-video`, `tk-prep`, `tk-browser-verify`의 내부 기본값과
참조·도구 동작만 바꾸며 공개 스킬 목록·호출명·카탈로그 설명에는 변화가 없습니다.
