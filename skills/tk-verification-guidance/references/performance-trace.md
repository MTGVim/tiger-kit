<a id="chrome-performance-trace"></a>
# Chrome 성능 분석

실제 과제가 JavaScript CPU 표본, 긴 작업, 레이아웃·페인트 비용이나 User Timing 구간을 요구할 때만
읽습니다. 일반 상호작용 재현은 CLI `tracing-start`/`tracing-stop`의 Playwright Trace를 사용합니다.
두 형식은 서로 대체하지 않습니다. Registry에 기능이 있다는 이유만으로 성능 기록을 켜거나
별도 Chrome DevTools MCP를 설치하지 않습니다.

## 같은 CLI 세션의 공개 API

선택한 Chromium 페이지의 공식 `run-code`에서 `page.context().browser().startTracing(page, options)`와
`stopTracing()`을 먼저 확인합니다. 공개 Chromium 전용 Playwright API이며 직접 CDP 연결이나
두 번째 브라우저가 필요하지 않습니다. 출력은 `traceEvents`를 가진 Chrome trace JSON입니다.
`path`는 승인된 새 실행 소유 절대 경로로 고정하고 호스트에서 기존 파일이 없음을 확인합니다.
이 API는 파일을 덮어쓸 수 있으므로 기존 근거나 사용자 파일을 대상으로 삼지 않습니다.
민감 페이지에서는 trace·스크린샷의 비밀 안전성을 확립하기 전 기록하지 않습니다.

```js
async page => {
  const browser = page.context().browser();
  await browser.startTracing(page, {
    path: '<new-run-owned-absolute-path>/chrome-trace.json',
    screenshots: false,
    categories: ['devtools.timeline', 'v8.execute',
      'disabled-by-default-v8.cpu_profiler', 'blink.user_timing']
  });
  try {
    // Perform only the already approved action on this exact page.
    await page.getByRole('button', { name: '<observed exact name>' }).click();
  } finally {
    await browser.stopTracing();
  }
}
```

Node `fs`, `require`와 모듈 import는 필요하지 않습니다. `path` 저장과 바이트 반환은 실제 설치
버전에서 확인합니다. 반환 바이트를 호스트로 전달한다면 출력 크기·잘림·디코딩을 검증합니다.
이미 활성화된 다른 trace를 중지하거나 소유하지 않은 브라우저를 닫지 않습니다. 중단으로
`finally` 실행을 확인할 수 없으면 자신이 만든 CLI 세션을 닫고 프로세스·프로필 정리를 확인합니다.
필요한 이벤트·CPU 표본·대상 스레드·실제 작업 구간이 없는 파일은 해당 분석의 성공 근거가 아닙니다.

API가 없거나 필요한 카테고리가 빠지면 실제 오류와 누락 데이터를 기록합니다. 일반 검증은
계속하되 성능 행만 `Unverifiable`로 남기고, 입증된 기능 공백과 승인된 동일 페이지에 한해서
최소 특수 경로를 검토합니다. Playwright Trace가 있다는 이유로 Chrome trace를 얻었다고 하지 않습니다.

## 실행 근거와 한계

2026-11-03에 공식 CLI `0.1.23`, 그 의존 Playwright `1.65.0-alpha-2026-10-30`, Chrome
`156.0.8078.74`의 격리 headless 세션에서 로컬 CPU fixture를 실행했습니다. CLI 기본 trace와
별도로 위 공개 API의 Chrome trace를 얻었고, `Profile` 1개, `ProfileChunk` 18개, `Layout` 1개,
`Paint` 2개와 `work.onclick` CPU 표본을 확인했습니다. 해당 `FunctionCall`은 100044µs,
User Timing `cpu-task` 구간은 100002µs였습니다. 이는 fixture 측정이며 제품 성능 목표가 아닙니다.
`path` 파일 저장, 제어된 예외에서 `finally` 종료와 같은 세션의 다음 trace 시작도 실제 통과했습니다.
추가 `CDPSession`의 `Profiler` 비교에서는 표본 75개를 얻었지만 이 과제에는 공개 API가 충분하므로
직접 `Profiler` 명령이나 별도 MCP를 요구하지 않습니다. 자동 인사이트 UI·메모리 덤프·다른
브라우저 엔진까지 동등하다는 주장은 하지 않습니다. 현재 TigerKit에는 이 기능들을 소비하는
성능 분석 실행 코드가 없으며, 별도 기능을 실제 요청받을 때 그 데이터 계약을 먼저 확정합니다.
