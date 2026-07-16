# 브라우저 안전

안전한 테스트 환경이나 명시적 권한이 없으면 실제 결제, 외부 커뮤니케이션, 되돌릴 수 없는 삭제, 프로덕션 데이터 변경, 계정 변경, 권한 변경 또는 이에 준하는 부작용을 유발하지 마세요. Guard mode는 위험한 mutation을 실행하지 않고 제한을 보고하세요. Verdict mode는 차단된 최종 상태를 screenshot으로 저장하고 이미지 자체를 분석한 뒤 `Unverifiable`로 보고하세요.

특정 API 상태에서만 보이는 UI는 가능한 경우 실제 mutation 대신 정확한 response envelope mock으로 도달하세요. Mock shape은 소스의 response mapping을 확인하고, 성공 상태를 만들기 위해 실제 발송·저장·결제를 실행하지 마세요.

OTP, passkey, CAPTCHA, 기기 승인 등 interactive auth에서만 headed 재실행과 사용자 로그인 요청을 허용하세요. 저장소 밖 user-local persistent profile만 재사용하고 secret·cookie·token·profile 내용이나 경로를 출력·복사·commit하지 마세요. 자격 증명을 저장하지 마세요.

Verdict mode의 모든 성공·실패·runtime 차단 최종 상태에는 screenshot과 실제 이미지 분석이 있어야 합니다. 필수 screenshot 또는 분석이 누락되면 `Pass`로 판정하지 마세요.
