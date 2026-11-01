<a id="images-and-ui-captures"></a>
# 이미지와 UI 캡처

로컬 Pillow나 기존 이미지 도구를 사용하여 동일한 canvas에 새 PNG 사본을 준비합니다.
EXIF, 주석이나 원본 파일명 없이 RGB/RGBA pixel을 다시 인코딩합니다. 가로세로 비율을 보존하고 늘리는 대신 letterbox를 사용해 같은 크기로 맞춥니다. UI 변형은 같은 viewport, 배율과 상호작용 상태에서 캡처합니다. 비교 질문을 보존할 수 있는 경우에만 사본에서 브라우저 tab/address bar를 잘라내고 식별 가능한 로고, watermark와 레이블을 중립화합니다.
실제 pixel과 남아 있는 파일명, desktop/browser chrome을 확인합니다. 메타데이터 제거로 눈에 보이는 watermark까지 제거되었다거나 자동 자르기가 모든 신원 단서를 찾았다고 주장하지 않습니다.
watermark 자체가 결정에 중요한 특성이라면 완전한 블라인드 처리가 불가능함을 공개합니다.
