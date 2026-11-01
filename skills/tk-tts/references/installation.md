<a id="installation-and-pinned-models"></a>
# 설치와 고정 모델

먼저 현재 Python/장치/의존성을 검사합니다. `scripts/list_options.py`는 설치나 네트워크 접근을 하지 않습니다. 최초 설정 전에 선택한 전용 venv, 정확한 manifest, 플랫폼 wheel 해시, 모델/캐시 크기, 위치와 텍스트 외부 전송 정책을 제안합니다. 일치하는 승인을 재사용합니다. 영상/TTS 선택은 전역 pip 설치, 추가 모델 또는 유료 호출의 승인이 아닙니다.

Qwen MLX는 native Apple Silicon에서 기본적으로 `qwen3.py --engine mlx --quantization 5`를 사용합니다. `--quantization 8`은 이전 모델/캐시를 유지합니다. 다른 장치는 명시적인 auto/cpu/mps/cuda 선택과 함께 공식 `--engine
pytorch`를 유지합니다. `mlx-files.json`, `mlx-8bit-files.json`과 `qwen3-files.json`은 정확한 모델 revision, 패키지/wheel 해시와 호환 버전을 소유합니다. `ppaso.py`는 고정된 ONNX CPU만 사용하며 `ppaso-files.json`이 모델/런타임 파일과 wheel 메타데이터를 소유합니다. 8bit weight 해시를 5bit에 적용하거나 CustomVoice와 Base를 혼동하지 않습니다. `supertonic3.py`는 명시적으로 선택하는 한국어 CPU/F1 경로입니다. `supertonic3-files.json`은 보관 처리된 모델, 공식 도우미/코드 라이선스와 핵심 런타임 패키지 3개를 고정합니다. 기존 기본값을 유지합니다.

전용 venv, 설치 캐시와 `snapshots/<revision>`을 두고 `${XDG_CACHE_HOME:-~/.cache}/tigerkit/tts/mlx/`, `tts/qwen3/` 또는 `tts/ppaso/`를 사용합니다. Supertonic 3는 `tts/supertonic3/`를 사용합니다. Manifest에서 호환 wheel을 선택하고 승인된 venv에 설치하기 전에 SHA256을 검증하며 의존성/lexicon 고지를 보존합니다. Qwen5bit의 weight 2개는 합계 약 1.76GB이고 ppaso의 ONNX/external-data 파일 8개는 약 38.50MB입니다. 이는 모델 파일 크기이며 전체 설치 크기나 메모리 수치가 아닙니다. 모델 카드의 변환 시점 mlx-audio 버전은 현재 고정 런타임과의 호환성을 입증하지 않습니다. Supertonic 3에서 선택한 모델/설정/F1/라이선스 파일의 합계는 약 398.68MB이며 도우미, 환경과 설치 캐시는 별도입니다. 핵심 고정 버전은 NumPy 2.2.6, soundfile 0.13.1과 onnxruntime 1.23.1입니다. 전용 Python 환경을 선택하기 전에 호환 wheel을 검사합니다.

<a id="installation-footprint-and-dependency-scope"></a>
## 설치 용량과 의존성 범위

설정 전에 모델 바이트, 압축 wheel/다운로드 바이트, 압축 해제된 venv/런타임, 보존할 설치 캐시와 최대 임시 공간/여유 공간 필요량을 구별합니다. 모델 크기만으로 설치 용량을 추정하지 않습니다. 실제 OS, 아키텍처와 Python 버전에 맞는 wheel을 선택합니다. 메타데이터 크기를 합산하고 하위 의존성과 압축 해제 파일도 추정에 포함합니다. 정확한 총량을 만들어 내지 말고 근거와 불확실성을 밝힙니다. 메타데이터/크기를 확보할 수 없다면 해당 부분을 알 수 없음으로 표시하고 모델만의 수치 대신 유사 환경의 관찰값을 사용합니다. 해당 권한 없이 추정만을 위해 다운로드/설치하지 않습니다.

제공된 설치 관찰값(2026-10-29, macOS arm64, Python 3.12, ppaso ONNX 전용 venv와 모델)은 약 406MB였으며 모델 파일만의 크기는 약 38.50MB였습니다. 이는 사용자 보고 측정값이며 이 스킬이 직접 수행한 native 측정이나 플랫폼 전반의 보장이 아닙니다. 유사 설정에는 약 0.4GB를 관찰된 설치 용량 참고값으로 사용하고 wheel 캐시/임시 여유 공간을 별도로 더합니다. 총 설치 용량을 38.50MB로 안내하지 않습니다. 다른 엔진에는 선택한 플랫폼 자체의 wheel/의존성 추정이 필요합니다. ppaso의 총량을 재사용하지 않습니다. 승인된 설치 후 해당 호스트에서 venv/모델/캐시를 각각 측정하고 실제 바이트와 환경을 보고합니다. 계획의 의미를 몰래 바꾸지 말고 계획과 비교합니다.

현재 `ppaso-files.json`은 핵심 런타임 패키지 5개의 버전/해시를 고정하며 완전한 하위 의존성 lock은 아닙니다. 설치 계획에는 `하위 의존성은 해시 고정이 없습니다`를 명시적으로 고지해야 합니다. 승인된 계획에서 하위 의존성 버전과 wheel 출처를 해석하여 나열합니다. `--require-hashes`가 완전하다거나 전체 환경을 결정적으로 재현한다고 주장하지 않습니다. 기존 핵심/모델 고정을 모두 보존합니다. 이 고지를 없애려고 검증되지 않은 하위 의존성 해시를 만들어 내지 않습니다. Supertonic 3 manifest도 핵심 패키지 3개만 고정하며 완전한 하위 의존성 lock이 아닙니다. 해당 설치 계획에도 `하위 의존성은 해시 고정이 없습니다`를 고지합니다.

승인된 설치/다운로드 후 선택한 venv Python을 사용합니다.

```bash
python -B scripts/qwen3.py --engine mlx --quantization 5 --download --verify
python -B scripts/qwen3.py --engine mlx --quantization 8 --verify
python -B scripts/qwen3.py --engine pytorch --verify
python -B scripts/ppaso.py --download --verify
python -B scripts/supertonic3.py --download --verify
```

경로는 호출자의 작업 디렉터리가 아니라 이 패키지를 기준으로 해석합니다. `--model-dir`은 명시적인 일반 snapshot을 받습니다. `--download`는 먼저 일치하는 로컬 HF snapshot 바이트를 소유권이 확인된 일반 파일로 복사하고 해시를 계산합니다. 캐시 symlink/원본, 부분/불일치 파일과 다른 실행 자료는 보존합니다. 해당 flag가 없으면 검증/합성은 다운로드하지 않습니다. 다운로드 후 자동 추론을 수행하지 않습니다. 모델 코드를 import/load하기 전에 정확한 파일 집합과 모든 해시를 검증합니다. 추가 파일, symlink나 안전하지 않은 경로는 거부합니다. 제3자 import 전에 실행 소유 런타임 캐시와 오프라인 모델 로딩을 설정합니다. ppaso는 자신의 snapshot 아래에서 해시가 검증된 코드만 import하며 상위 런타임을 검색하거나 외부 lexicon override를 따르지 않습니다.

두 모델 모두 Apache-2.0을 선언합니다. 모델/라이선스/readme와 관련 G2P/lexicon 출처 표기를 보존합니다. Manifest는 ppaso 샘플 avatar/VRM, RKNN, Vocos와 lipsync 자산을 제외합니다. 핵심 ppaso에는 NumPy, soundfile, 고정 dictionary가 있는 python-mecab-ko와 onnxruntime이 필요합니다. Upstream의 버전 범위가 제한되지 않은 requirements가 아니라 고정 manifest를 사용합니다. TigerKit Git 이력에 weight를 포함하지 않습니다.

Supertonic 3는 다릅니다. 모델은 OpenRAIL-M이고 공식 도우미는 MIT입니다. 검증된 snapshot에 두 라이선스를 모두 보존합니다. Attachment A(e)는 생성된 콘텐츠가 기계 생성임을 명확히 이해할 수 있는 고지를 요구합니다. 이 엔진을 선택하거나 전달할 때 사용자에게 요구 사항을 알립니다. `이 음성은 AI로 합성되었습니다.`를 제안하고 receipt의 고지를 반환합니다. 이는 사용자 안내이며 자동 표시나 후속 영상에 고지가 들어갔다는 증거가 아닙니다. 보관 처리된 upstream은 유지보수/보안 수정을 제공하지 않습니다. SDK 자동 다운로드, 서버, 목소리 복제나 추가 preset은 포함하지 않습니다. 고정 모델 파일과 도우미만 다운로드합니다.

`--verify`는 모듈 가용성, 실제 고정 버전과 snapshot 해시를 확인하며 native 합성 품질을 확인하지 않습니다. 고정을 완화하지 않고 실제/기대 불일치와 venv 복원 명령을 보고합니다. 새 런타임/모델을 수용하기 전에는 대표 입력과 계획한 최장 입력의 합성/디코딩 smoke가 필요합니다. 실행하지 않은 합성이나 청취는 명시적으로 남깁니다.
