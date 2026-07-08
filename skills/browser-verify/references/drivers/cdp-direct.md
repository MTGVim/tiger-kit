# Driver: CDP-direct (raw Chrome DevTools Protocol)

MCP driver가 없을 때(예: 세션에서 MCP가 로드 안 됨)의 폴백. 크롬을 원격 디버깅으로 띄우고 CDP를 직접 두드린다. 어떤 FE web 프로젝트에도 동일하게 적용된다. 코드는 표준 JS라 그대로 이식된다.

## 러너 (환경 치환 가능)

아래 JS를 실행할 수단은 환경마다 다르다 — **가용한 것을 쓴다**:
- `ctx_execute`(context-mode 플러그인이 있으면) — HTTP/WebSocket 허용
- `node`(Node 18+; 전역 `fetch`·`WebSocket` 있음)
- 기타 JS 런타임
스크린샷은 **파일 쓰기가 되는 러너**(예: node) 필요. sandbox 러너는 host 파일 저장이 안 될 수 있다.

## Safety boundary

- `skills/browser-verify/SKILL.md`가 canonical policy이고, 이 문서는 fallback 실행 레시피입니다. fallback이라는 이유로 상호작용 safety rule을 완화하지 않습니다.
- 클릭 / 활성화 / submit 계열 상호작용은 driver가 제공하는 trusted 입력 surface로 실행합니다. CDP-direct에선 `Input.dispatchMouseEvent`, 필요할 때 `Input.dispatchKeyEvent`를 사용합니다. 이 규칙은 아래 native setter 입력 주입 예시와 별개로, 텍스트 입력 자체보다 클릭 / 활성화 / submit 계열 상호작용에 적용합니다.
- `element.click()`, `dispatchEvent(new MouseEvent(...))`, `form.submit()` 같은 합성 상호작용은 실행용 수단으로 사용하지 않습니다.
- `Runtime.evaluate`는 selector 조회, 상태 read, `scrollIntoView`, rect / 좌표 계산 같은 비파괴적 관측·계산·준비 단계에만 사용합니다. 클릭 / 활성화 / submit 실행용 surface로 사용하지 않습니다.
- trusted 클릭 / 활성화 / submit 전에 native dialog 대응을 먼저 준비합니다. 대상은 `alert`, `confirm`, `beforeunload`입니다.
- native dialog와 DOM overlay / custom modal은 별도 경우로 다룹니다. overlay를 확인했다고 native dialog 대응이 끝난 것으로 간주하지 않습니다.
- dialog가 열리면 가능한 한 즉시 `accept` 또는 `dismiss`로 해제하고, `dialog opened` 상태로 오래 방치하지 않습니다.
- 저장 / 삭제 / 제출처럼 write 가능성이 있는 흐름은 DOM alert, modal close, toggle state change만으로 성공 판정하지 않습니다. 실제 PUT / POST / PATCH / DELETE 요청 발생 여부와 결과를 ground-truth로 확인합니다.
- destructive side-effect 가능성이 있으므로 이런 검증은 비프로덕션 환경이나 테스트 데이터 기준으로 수행합니다.

## 크롬 기동 (OS별 실행 경로)

```
<chrome-binary> --remote-debugging-port=9222 --user-data-dir="<debug-profile-dir>" \
  --window-size=<viewport> "<baseline_url>" "<target_url>"
```
- 포트 9222는 관례(설정 가능). `<chrome-binary>`는 OS별 경로(macOS: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`).

## 헬퍼 (JS, 매 실행 재정의)

```javascript
// 단일 CDP 명령
function cdp(w,method,params={}){return new Promise((res,rej)=>{const ws=new WebSocket(w);ws.onopen=()=>ws.send(JSON.stringify({id:1,method,params}));ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id===1){ws.close();m.error?rej(m.error):res(m.result);}};ws.onerror=e=>rej(String(e));setTimeout(()=>{try{ws.close()}catch{};rej("t")},9000);});}
// 페이지 JS 평가 (returnByValue)
function ev(w,expr){return new Promise((res,rej)=>{const ws=new WebSocket(w);ws.onopen=()=>ws.send(JSON.stringify({id:1,method:"Runtime.evaluate",params:{expression:expr,returnByValue:true,awaitPromise:true}}));ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id===1){ws.close();m.result?.exceptionDetails?rej(JSON.stringify(m.result.exceptionDetails).slice(0,300)):res(m.result.result.value);}};ws.onerror=e=>rej(String(e));setTimeout(()=>{try{ws.close()}catch{};rej("t")},9000);});}
// 여러 명령 배치 (실제 마우스 클릭용)
function rpc(w,msgs){return new Promise((res)=>{const ws=new WebSocket(w);let i=0;const r={};ws.onopen=()=>msgs.forEach(m=>ws.send(JSON.stringify(m)));ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id){r[m.id]=m.result||m.error;i++;if(i>=msgs.length){ws.close();res(r);}}};ws.onerror=()=>res(r);setTimeout(()=>{try{ws.close()}catch{};res(r);},9000);});}
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const clickXY=(w,x,y)=>rpc(w,[{id:1,method:"Input.dispatchMouseEvent",params:{type:"mousePressed",x,y,button:"left",clickCount:1}},{id:2,method:"Input.dispatchMouseEvent",params:{type:"mouseReleased",x,y,button:"left",clickCount:1}}]);
// 열린 탭 목록 (webSocketDebuggerUrl 획득). PAGE_ID = 그 URL의 마지막 segment
const tabs=async()=>(await (await fetch("http://127.0.0.1:9222/json")).json()).filter(t=>t.type==="page");
```

## 입력 주입 (native setter)

```javascript
const set=(el,v)=>{const s=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set;s.call(el,v);el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));};
```

## 클릭 (실제 마우스 이벤트 + 뷰포트 보정)

```javascript
const el=await ev(w,`(()=>{const e=document.querySelector('<sel>');if(!e)return null;e.scrollIntoView({block:'center'});const r=e.getBoundingClientRect();return JSON.stringify({x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2)});})()`);
const {x,y}=JSON.parse(el); await sleep(500); await clickXY(w,x,y);
```

위 패턴에서 `ev(...)`는 스크롤과 좌표 계산을 위한 비파괴적 준비 단계이고, 실제 상호작용 실행은 마지막 `clickXY(...)` trusted 입력으로 끝냅니다.

## 쓰기 가능 흐름 검증

- 저장 / 삭제 / 제출처럼 write가 날 수 있는 흐름은 DOM만 보고 성공 판정하지 않습니다.
- alert 표시, modal 닫힘, toggle 변화는 보조 신호일 뿐입니다.
- 최소한 아래 중 하나로 ground-truth를 확인합니다.
  - CDP `Network` domain으로 PUT / POST / PATCH / DELETE 요청 발생 여부와 결과 확인
  - 서버 로그 / API 로그 / 테스트 백엔드에서 실제 write 여부 확인
- 합성 상호작용이 phantom success를 만들 수 있으므로, write-capable flow에서는 “UI가 바뀌었다”보다 “실제 write가 있었는지”를 먼저 확인합니다.

## 측정 (예시 heuristic — 대상에 맞게 셀렉터 조정)

- baseline 측정은 실제 baseline runtime에서 렌더된 요소를 직접 재는 것을 우선합니다.
- class 주입 probe로 baseline을 흉내 내야 할 때는 `variant` class만 따로 넣지 말고 소비처의 전체 `className`을 그대로 사용합니다.
- 이런 probe는 inline style, cascade, parent context, consumer override를 완전히 담지 못하므로 low-trust 측정으로 취급합니다.
- baseline 타입이나 원래 스타일 출처는 commit message나 라벨보다 pre-change source, 예: `git show <base>:<file>`와 그 렌더 근거를 우선합니다.

```javascript
const measure=`(()=>{const vw=innerWidth,vh=innerHeight;
  const dark=[...document.querySelectorAll('div')].filter(d=>{const r=d.getBoundingClientRect();const s=getComputedStyle(d);return r.width>vw*0.9&&r.height>vh*0.9&&s.backgroundColor.includes('0, 0, 0')&&s.backgroundColor!=='rgba(0, 0, 0, 0)';}).map(d=>{const s=getComputedStyle(d);return {bg:s.backgroundColor,op:s.opacity,cls:(d.className||'').toString().slice(0,32)};});
  const img=[...document.querySelectorAll('img')].sort((a,b)=>b.getBoundingClientRect().width-a.getBoundingClientRect().width)[0];
  let card=null;if(img){let el=img;for(let i=0;i<8&&el;i++){const s=getComputedStyle(el),r=el.getBoundingClientRect();if(s.backgroundColor.includes('255, 255, 255')&&r.width>200){card={w:Math.round(r.width),x:Math.round(r.x)};break;}el=el.parentElement;}}
  return JSON.stringify({vw,vh,dark,imgW:img?Math.round(img.getBoundingClientRect().width):null,card});
})()`;
```
prop 후보: width/height, padding/margin, background-color, opacity, border, border-radius, font-size, color, z-index, getBoundingClientRect.

## 스크린샷 (파일 쓰기 되는 러너, 예: node)

```
node -e '
const WS="ws://127.0.0.1:9222/devtools/page/<PAGE_ID>";const fs=require("fs");const ws=new WebSocket(WS);let id=0;const p={};
const send=(m,pa={})=>new Promise((r)=>{const i=++id;p[i]=r;ws.send(JSON.stringify({id:i,method:m,params:pa}));});
ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id&&p[m.id]){p[m.id](m.result);delete p[m.id];}};
ws.onopen=async()=>{await send("Page.enable");const r=await send("Page.captureScreenshot",{format:"png"});fs.writeFileSync("shot.png",Buffer.from(r.data,"base64"));ws.close();process.exit(0);};
'
```
- OS 임시폴더 권한으로 외부에서 만든 스크린샷 파일을 못 읽을 수 있으니, 위처럼 CDP로 직접 캡처해 접근 가능한 경로에 저장.
