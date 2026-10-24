const {test}=require('node:test'),assert=require('node:assert/strict'),{pathToFileURL}=require('node:url');
const ready=!!(process.env.TK_PLAYWRIGHT_MODULE&&process.env.TK_CHROMIUM_EXECUTABLE&&process.env.TK_FIGURE_PAGE);
test('slides and video reclaim transcript space and maximize centrally without changing the clock',{skip:!ready,timeout:90000},async()=>{
 const {chromium}=require(process.env.TK_PLAYWRIGHT_MODULE),browser=await chromium.launch({headless:true,executablePath:process.env.TK_CHROMIUM_EXECUTABLE,env:{...process.env,...(process.env.TK_BROWSER_FONTCONFIG?{FONTCONFIG_FILE:process.env.TK_BROWSER_FONTCONFIG}:{})},args:['--no-sandbox','--disable-dev-shm-usage','--enable-automation']});
 const errors=[];
 try{
  const cdp=await browser.newBrowserCDPSession(),args=(await cdp.send('Browser.getBrowserCommandLine')).arguments;
  assert(args.some(a=>a.startsWith('--headless')));assert(args.some(a=>a.startsWith('--user-data-dir=')));
  const files=[process.env.TK_FIGURE_PAGE,...JSON.parse(process.env.TK_VIDEO_PAGES||'[]')];
  for(const file of files){
   const context=await browser.newContext({viewport:{width:1440,height:900}});try{
    const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));await page.goto(pathToFileURL(file).href);const f=page.frameLocator('#course-frame');await f.locator('#home-start').click();
    // Wait for layout to settle on actual frames; no generated narration is needed.
    const settle=()=>f.locator('#stage').evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))));
    const measure=()=>f.locator('#stage').evaluate(stage=>{
     const main=document.getElementById('stage-main'),viewport=document.getElementById('media-viewport'),rect=e=>e.getBoundingClientRect().toJSON(),style=getComputedStyle(main);
     const rest=['fullscreen-status','audio-progress','controls'].reduce((n,id)=>n+document.getElementById(id).getBoundingClientRect().height,0);
     const height=main.clientHeight-rest-(parseFloat(style.paddingTop)||0)-(parseFloat(style.paddingBottom)||0),media=rect(viewport),controls=rect(document.getElementById('controls'));
     return {main:rect(main),media,controls,height,ideal:Math.min(main.clientWidth,Math.max(0,height)*16/9),open:stage.classList.contains('with-transcript'),slide:document.querySelector('.lesson-slide:not([hidden])')?.dataset.slide,time:document.getElementById('lesson-video').currentTime,paused:document.getElementById('lesson-video').paused,overflow:document.documentElement.scrollWidth>innerWidth,window:{width:innerWidth,height:innerHeight}};
    });
    const transcript=async open=>{if((await f.locator('#transcript-toggle').getAttribute('aria-expanded')==='true')!==open)await f.locator('#transcript-toggle').click();await settle();};
    for(const mode of ['normal','native','fallback']){
     if(mode==='fallback')await f.locator('#stage').evaluate(e=>{e.requestFullscreen=()=>Promise.reject(Error('test rejection'));});
     if(mode!=='normal'){await f.locator('#fullscreen').click();await settle();assert(await f.locator('#stage').evaluate((e,mode)=>mode==='native'?document.fullscreenElement===e:e.classList.contains('stage-expanded'),mode));}
     for(const size of [{width:1440,height:900},{width:2560,height:1440},{width:1101,height:850},{width:1100,height:850},{width:701,height:600},{width:700,height:600},{width:390,height:844},{width:844,height:390}]){
      // Chromium requires restoring its native window before changing its bounds.
      if(mode==='native')await f.locator('#fullscreen').click();
      await page.setViewportSize(size);
      if(mode==='native')await f.locator('#fullscreen').click();
      await settle();await transcript(true);const open=await measure();
      for(const isOpen of [false,true,false]){
       await transcript(isOpen);const r=await measure(),detail=JSON.stringify({file,mode,size,r});
       assert(!r.overflow,detail);assert(Math.abs(r.media.width-r.media.height*16/9)<=1,detail);assert(r.paused,detail);assert.equal(r.time,open.time,detail);assert.equal(r.slide,open.slide,detail);
       assert(r.controls.y>=r.media.bottom-1,detail);
       if(!isOpen){assert(r.media.width>=open.media.width-1,detail);if(mode==='normal'&&size.width>1100)assert(r.media.width>open.media.width+10,detail);}
       if(mode!=='normal'){
        assert(Math.abs(r.media.width-r.ideal)<1,detail);
        assert(Math.abs((r.media.x+r.media.width/2)-(r.main.x+r.main.width/2))<1,detail);
        assert(Math.abs(r.media.y-(r.main.y+(r.height-r.media.height)/2))<1,detail);
        assert(r.controls.bottom<=r.window.height+1&&r.media.y>=0,detail);
        if(!isOpen){const bounds=await f.locator('#stage').evaluate(e=>{const s=getComputedStyle(e);return {w:e.clientWidth-parseFloat(s.paddingLeft)-parseFloat(s.paddingRight),h:e.clientHeight-parseFloat(s.paddingTop)-parseFloat(s.paddingBottom)};});assert(Math.abs(r.main.width-bounds.w)<1&&Math.abs(r.main.height-bounds.h)<1,detail);}
       }
      }
     }
     if(mode!=='normal')await f.locator('#fullscreen').click();
    }
   }finally{await context.close();}
  }
  assert.deepEqual(errors,[]);
 }finally{await browser.close();}
});
