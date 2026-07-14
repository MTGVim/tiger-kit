# 환경 비교

기본 실행은 headless입니다. 네이티브 브라우저, Playwright 호환 드라이버, MCP 또는 CDP 드라이버 중 현재 환경에서 실제 관찰과 screenshot 저장을 지원하는 가장 단순한 수단을 선택하고, 브라우저·버전·OS·DPR·font·assets·zoom을 기록하세요.

OTP, passkey, CAPTCHA, 기기 승인처럼 headless에서 완료할 수 없는 interactive auth에서만 같은 실행을 headed로 재시도하세요. 그때 사용자에게 직접 로그인하도록 요청하고, 인증이 끝나면 검증을 계속하세요. 저장소 밖 user-local persistent profile을 우선 재사용하되 profile 경로, 쿠키, 토큰, secret은 출력·복사·커밋하지 마세요.

지정된 환경, 뷰포트 또는 기능 플래그만 비교하세요. 정확한 대상을 기록하고 제품 차이와 접근 권한, 데이터 또는 인프라 차이를 구분하세요. 인증을 완료할 수 없거나 권한이 없으면 차단된 최종 상태를 캡처·분석하고 `Unverifiable`로 보고하세요.
