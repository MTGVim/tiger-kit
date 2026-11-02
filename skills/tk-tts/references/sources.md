<a id="tts-sources-and-distillation"></a>
# TTS 출처와 증류

- TigerKit `68b14419cdef1ac9c2c93766c3926f0a192e2098`: 엔진을 중복하지 않고 기존 Qwen CLI, 고정, MLX/PyTorch, 캐시/오프라인, 디코딩과 무음이 아님을 확인하는 계약을 추출합니다.
- [Qwen CustomVoice MLX 5bit](https://huggingface.co/mlx-community/Qwen3-TTS-12Hz-0.6B-CustomVoice-5bit/tree/ea57eb1094e142071162f79568581c9315dfd2e7):
  Apple Silicon 권장 경로로 적용합니다. 작은 파일의 SHA256은 고정된 바이트에서 계산했고 큰 weight 해시는 공식 LFS 메타데이터에서 가져왔습니다. `049ef77fe8816b536193c0c25f9a214d17921282`의 명시적 8bit 호환성과 공식 PyTorch 고정을 유지합니다.
- [ppaso](https://huggingface.co/akamotaco/ppaso-tts-v1/tree/53d09664c4f636a5fb6f2ebe3ec22cd83ee249b9):
  ONNX CPU/핵심 한국어 합성만 적용합니다. 정확한 모델/런타임/lexicon 바이트와 Apache/MIT/BSD 고지를 유지합니다. 샘플 avatar, 선택적 그래픽, RKNN, lipsync와 서버는 제외합니다.
- [Supertonic 3 보관 모델](https://huggingface.co/supertone-oss-archive/supertonic-3/tree/aafc6e32416a594460b32413efc49d7fe4ce6d46)
  및 [공식 Python 도우미/예시](https://github.com/supertone-oss-archive/supertonic/tree/1e9799e964ea4c0dad7cde993b65c3c813a7b373/py):
  CPUExecutionProvider, 한국어/F1, native chunk 분할, 8단계와 speed 1.05를 유지합니다. 고정된 오프라인 로딩을 적용하고 디코딩한 각 chunk를 자른 후 연결합니다. 이 revision의 도우미, 예시, requirements, 모델 카드와 두 라이선스를 검사합니다. 모델/런타임 SHA256 값과 플랫폼 wheel 메타데이터는 `supertonic3-files.json`에 있습니다. OpenRAIL-M Attachment A(e) 고지는 선택 전 사용자 안내와 receipt 필드로 유지합니다. 후속 영상은 tk-video의 고지 게이트가 소비하며 실제 프레임 확인은 별도로 남깁니다. 코드 upstream은 보관 처리되었으며 개발/지원이 종료되었습니다. SDK/서버, 자동 다운로드, 복제, 다른 언어/preset은 제외합니다. TTS 패키지에 영상 validator를 중복 구현하지 않습니다. 소스 검사와 adapter 테스트는 음향 품질을 입증하지 않습니다. Native smoke와 사람의 청취를 별도로 보고합니다.
- 제공된 2026-10-21/22 사용자 실험은 청취자 1명과 문장당 샘플 1개를 바탕으로 Qwen5bit와 ppaso를 선택했습니다. 이는 지원 정책의 참고이며 보편적인 품질 순위가 아닙니다. 실제 모델 revision은 없었습니다. 이 최신 소스 고정값을 벤치마크로 테스트한 고정값이라고 표시하지 않습니다.
- [NeMo 한국어 기수와 단위 명사 정규화](https://github.com/NVIDIA/NeMo-text-processing/blob/ddadfb2a38d2bc6b8cc6232c4f915eb60f500688/nemo_text_processing/text_normalization/ko/taggers/cardinal.py#L277-L374)
  및 [기수 fixture](https://github.com/NVIDIA/NeMo-text-processing/blob/ddadfb2a38d2bc6b8cc6232c4f915eb60f500688/tests/nemo_text_processing/ko/data_text_normalization/test_cases_cardinal.txt):
  맥락에 따른 수량/개별 숫자/단위 명사 구별을 직접 작성하는 낭독 원고 준비에 적용합니다. 소스 literal과 원시 벤치마크 입력을 유지합니다. 고정된 0/구분자 규칙을 복사하지 않습니다.
- 동일 revision의 NeMo [측정값 구현](https://github.com/NVIDIA/NeMo-text-processing/blob/ddadfb2a38d2bc6b8cc6232c4f915eb60f500688/nemo_text_processing/text_normalization/ko/taggers/measure.py)
  및 [측정값 fixture](https://github.com/NVIDIA/NeMo-text-processing/blob/ddadfb2a38d2bc6b8cc6232c4f915eb60f500688/tests/nemo_text_processing/ko/data_text_normalization/test_cases_measure.txt):
  숫자/단위의 분리 해석을 적용합니다. [단위 lexicon](https://github.com/NVIDIA/NeMo-text-processing/blob/ddadfb2a38d2bc6b8cc6232c4f915eb60f500688/nemo_text_processing/text_normalization/ko/data/measure/unit.tsv)에는 `ms`와 `GB`가 없습니다. 해당 예시의 지원을 추론하지 않습니다. 외부 normalizer, WFST 런타임, Cloud 호출, SSML과 전역 치환 규칙은 제외합니다. 소스/주석/fixture는 검증된 2026-10-23 main revision에서 읽었습니다. Upstream 테스트와 음향 A/B는 실행하지 않았습니다.

최장 입력/동일 캐시 smoke와 실제/기대 런타임 진단을 유지합니다. 자동 ASR, 모델/엔진 fallback, 테스트하지 않은 짧은 발화 재시도 규칙과 새 블라인드 갤러리 스킬은 제외합니다. 대상 하드웨어에서의 실제 모델 합성/청취는 mocked adapter 테스트, 소스/고정 검사와 런타임 부재 진단과 별도로 보고해야 합니다.


<a id="setup-transparency-2026-10-29"></a>
## 설정 투명성(2026-10-29)

TigerKit `e672abcc0fedc8b91766266c8117a21496f02cbe`에서 현재 패키지 로컬 `ppaso-files.json`의 핵심 의존성/wheel 해시와 `list_options.py` 탐색 동작을 검사했습니다. 핵심 고정값 5개를 유지합니다. 해시를 만들어 내거나 완전한 재현성을 주장하는 대신 완전한 하위 의존성 lock이 없음을 고지합니다. 제공된 macOS arm64/Python 3.12 관찰값(venv와 모델 약 406MB)을 출처가 명확한 용량 참고값으로 적용합니다. 이는 새로 수행한 native 설치 측정이 아닙니다. 모델/런타임 업그레이드, 숨겨진 엔진 제외와 크기 확인만을 위한 자동 설정은 제외합니다. 선택지 탐색은 오프라인으로 유지하며 엔진을 import하지 않습니다.

## 문장 속도와 고지 소비 (2026-11-03)

사용자 제공 결함 묶음의 문장 속도 수치(중앙값 1.03배, 짧은 문장 3.6초/0.92배, atempo 하한 0.88)는 제작 경험에서 온 조정 출발값입니다. `keep`: 고정 adapter speed, 원본 WAV와 청취 대기를 유지합니다. `adapt`: 실제 낭독형 입력, 문장별 측정·상한 감속·재측정과 부모 alias 허용을 적용합니다. `omit`: 숫자 읽기 추측, 엔진 속도 변경과 12% 상한을 넘기는 자동 반복입니다. 첨부본을 그대로 배포하지 않고 실제 CLI의 안전한 새 출력과 남은 빠른 문장 보고를 구현합니다.
고정 모델 revision `aafc6e32416a594460b32413efc49d7fe4ce6d46`의 LICENSE와 README를 다시 읽어 Attachment A(e)의 명시적 기계 생성 고지 요구를 확인했습니다. 위치·전 구간은 해당 조항의 직접 요구라고 주장하지 않으며 tk-video가 정한 누락 방지 계약입니다. TTS는 선택 전 안내와 receipt를 유지하고 영상 픽셀 검사는 소비자가 담당합니다.
