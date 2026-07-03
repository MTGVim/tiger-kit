# Driver: CDP-direct (raw Chrome DevTools Protocol)

MCP driver가 없을 때(예: 세션에서 MCP가 로드 안 됨)의 폴백. 크롬을 원격 디버깅으로 띄우고 CDP를 직접 두드린다. 어떤 FE web 프로젝트에도 동일하게 적용된다. 코드는 표준 JS라 그대로 이식된다.

## 러너 (환경 치환 가능)

아래 JS를 실행할 수단은 환경마다 다르다 — **가용한 것을 쓴다**:
- `ctx_execute`(context-mode 플러그인이 있으면) — HTTP/WebSocket 허용
- `node`(Node 18+; 전역 `fetch`·`WebSocket` 있음)
- 기타 JS 런타임
스크린샷은 **파일 쓰기가 되는 러너**(예: node) 필요. sandbox 러너는 host 파일 저장이 안 될 수 있다.

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

## 측정 (예시 heuristic — 대상에 맞게 셀렉터 조정)

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
