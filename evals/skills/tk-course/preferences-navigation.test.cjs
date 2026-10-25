// Run only with an explicitly configured local browser; test tones are not listening evidence.
const {test}=require('node:test'),assert=require('node:assert/strict');
const {pathToFileURL}=require('node:url');
const ready=!!(process.env.TK_PLAYWRIGHT_MODULE&&process.env.TK_CHROMIUM_EXECUTABLE&&process.env.TK_COURSE_PAGE);
test('shared course preferences, breadcrumb, curriculum and standalone catalog discovery', {skip:!ready},async()=>{
 const {chromium}=require(process.env.TK_PLAYWRIGHT_MODULE),browser=await chromium.launch({env:{...process.env,...(process.env.TK_BROWSER_FONTCONFIG?{FONTCONFIG_FILE:process.env.TK_BROWSER_FONTCONFIG}:{})},headless:true,executablePath:process.env.TK_CHROMIUM_EXECUTABLE,args:['--no-sandbox','--disable-dev-shm-usage']});
 const url=pathToFileURL(process.env.TK_COURSE_PAGE).href;
 async function enter(page){await page.goto(url);const f=page.frameLocator('#course-frame');await f.locator('#home-start').click();await f.locator('#player-page').waitFor({state:'visible'});return f;}
 try{
  for(const width of [390,853,1024,1280])for(const colorScheme of ['light','dark']){
   const context=await browser.newContext({viewport:{width,height:900},colorScheme});
   try{
    const page=await context.newPage(),f=await enter(page);
    assert.equal(await f.locator('#mute-toggle').getAttribute('aria-pressed'),'true');
    assert(await f.locator('#menu-toggle').isVisible());
    const bar=await f.locator('header').boundingBox();assert(bar.height<=72,`${width}: ${bar.height}`);
    assert.equal(await f.locator('#collection-link').getAttribute('target'),'_top');
    await f.locator('#collection-link').waitFor({state:'visible'});
    assert.equal(await f.locator('#back-home,.collection-home').count(),0);
    const widthBefore=(await f.locator('#stage').boundingBox()).width;
    await f.locator('#menu-toggle').click();
    if(width>700){assert((await f.locator('#stage').boundingBox()).width>widthBefore);assert.equal(await f.locator('#menu-toggle').getAttribute('aria-expanded'),'false');}
    else{assert.equal(await f.locator('#menu-toggle').getAttribute('aria-expanded'),'true');await f.locator('#toc-close').click();}
    await f.locator('#volume').evaluate(el=>{el.value='60';el.dispatchEvent(new Event('input',{bubbles:true}));});
    await f.locator('#caption-opacity').evaluate(el=>{el.value='80';el.dispatchEvent(new Event('input',{bubbles:true}));});
    await f.locator('#next-lesson').click();
    await f.locator('#lesson-heading').filter({hasText:'조건과 결과 2'}).waitFor();
    assert.equal(await f.locator('#volume').inputValue(),'60');assert.equal(await f.locator('#caption-opacity').inputValue(),'80');
    await page.reload();await f.locator('#home-start').click();
    // Wait through file-frame navigation without assuming a shared file origin.
    await f.locator('#lesson-heading').filter({hasText:'조건과 결과 2'}).waitFor();
    assert.equal(await f.locator('#volume').inputValue(),'60');assert.equal(await f.locator('#caption-opacity').inputValue(),'80');
    if(width>700)assert.equal(await f.locator('#menu-toggle').getAttribute('aria-expanded'),'false');
    assert(await f.locator('body').evaluate(el=>el.scrollWidth<=el.ownerDocument.defaultView.innerWidth));
   }finally{await context.close();}
  }
  for(const mode of ['corrupt','denied','policy']){
   const context=await browser.newContext();
   try{
    await context.addInitScript(mode=>{
     if(mode==='corrupt'){try{localStorage.setItem('tigerkit-course-player:prefs','{broken');}catch(_){}}
     if(mode==='denied')Object.defineProperty(window,'localStorage',{get(){throw new Error('blocked');}});
     if(mode==='policy'){
      localStorage.setItem('tigerkit-course-player:prefs',JSON.stringify({version:1,muted:false,volume:1,speed:1,captions:false,captionSize:'default',captionOpacity:.5,tocCollapsed:false}));
      const play=HTMLMediaElement.prototype.play;let failed=false;
      HTMLMediaElement.prototype.play=function(){if(!failed&&!this.muted){failed=true;return Promise.reject(new DOMException('blocked','NotAllowedError'));}return play.call(this);};
     }
    },mode);
    const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));const f=await enter(page);
    if(mode==='policy'){await f.locator('#play').click();await f.locator('#sound-toast-message').filter({hasText:'브라우저가 소리'}).waitFor();}
    else{assert.equal(await f.locator('#volume').inputValue(),'100');assert.equal(await f.locator('#caption-opacity').inputValue(),'50');}
    assert.deepEqual(errors,[]);
   }finally{await context.close();}
  }
  if(process.env.TK_COURSE_STANDALONE){
   const context=await browser.newContext();try{const page=await context.newPage();await page.goto(pathToFileURL(process.env.TK_COURSE_STANDALONE).href);const f=page.frameLocator('#course-frame');await f.locator('#home-start').waitFor();await page.waitForTimeout(4200);assert(await f.locator('#collection-link').isHidden());}finally{await context.close();}
  }
 }finally{await browser.close();}
});

test('bounded lesson panels retain curriculum position, transcript and real default pacing',{skip:!ready||!process.env.TK_COURSE_LONG_PAGE,timeout:120000},async()=>{
 const {chromium}=require(process.env.TK_PLAYWRIGHT_MODULE),browser=await chromium.launch({env:{...process.env,...(process.env.TK_BROWSER_FONTCONFIG?{FONTCONFIG_FILE:process.env.TK_BROWSER_FONTCONFIG}:{})},headless:true,executablePath:process.env.TK_CHROMIUM_EXECUTABLE,args:['--no-sandbox','--disable-dev-shm-usage']});
 try{
  for(const width of [390,1024,1440]){
   const context=await browser.newContext({viewport:{width,height:600}});try{
    const page=await context.newPage();await page.goto(pathToFileURL(process.env.TK_COURSE_LONG_PAGE).href);const f=page.frameLocator('#course-frame');await f.locator('#home-start').click();
    assert(await f.locator('#transcript-rail').isVisible());assert.equal(await f.locator('#rail-title').evaluate(e=>e===document.activeElement),false);
    if(width<=700)await f.locator('#menu-toggle').click();
    await f.locator('#toc-list').hover();await page.mouse.wheel(0,10000);await page.waitForTimeout(120);
    const tail=await f.locator('#toc-list').evaluate(e=>({top:e.scrollTop,last:e.lastElementChild.getBoundingClientRect().bottom,bottom:e.getBoundingClientRect().bottom,root:scrollY}));assert(tail.top>0);assert(tail.last<=tail.bottom+1);assert.equal(tail.root,0);assert(await f.locator('#toc-close').isVisible());
    // Navigation through a visible tail item exercises the real frame replacement.
    await f.locator('#toc-list [data-course-jump="lesson-20"]').click();await f.locator('#lesson-heading').filter({hasText:'조건과 결과 20'}).waitFor();
    if(width<=700)await f.locator('#menu-toggle').click();
    assert.equal(await f.locator('#toc-list').evaluate(e=>e.scrollTop),tail.top);
    await f.locator('#toc-close').click();assert.equal(await f.locator('#menu-toggle').getAttribute('aria-expanded'),'false');
    const geometry=await f.locator('#transcript-rail').evaluate(e=>({rail:e.getBoundingClientRect().toJSON(),media:document.getElementById('media-viewport').getBoundingClientRect().toJSON(),root:scrollY}));
    if(width<=1100)assert(geometry.rail.y>=geometry.media.bottom,'transcript must sit below media without overlap');
    // Both native and explicitly denied fullscreen use the same single transcript subtree.
    await f.locator('#fullscreen').click();await f.locator('#stage').evaluate(e=>{if(!document.fullscreenElement&&!e.classList.contains('stage-expanded'))throw Error('missing expansion');});
    assert.equal(await f.locator('#stage #transcript-rail').count(),1);assert(await f.locator('#transcript-toggle').isVisible());assert(await f.locator('#transcript-rail').isVisible());
    await f.locator('#transcript-close').click();assert(await f.locator('#transcript-rail').isHidden());assert(await f.locator('#transcript-toggle').evaluate(e=>e===document.activeElement));await f.locator('#transcript-toggle').click();assert(await f.locator('#transcript-rail').isVisible());
    await page.keyboard.press('Escape');
    if(await f.locator('#stage').evaluate(e=>!!document.fullscreenElement))await f.locator('#fullscreen').click();
    await f.locator('#stage').evaluate(e=>{e.requestFullscreen=()=>Promise.reject(new DOMException('test policy','NotAllowedError'));});
    await f.locator('#fullscreen').click();assert(await f.locator('#stage.stage-expanded').isVisible());
    await f.locator('#transcript-close').click();await page.keyboard.press('Tab');assert(await f.locator('#stage').evaluate(e=>e.contains(document.activeElement)));
    await page.keyboard.press('Escape');assert.equal(await f.locator('#stage.stage-expanded').count(),0);assert.equal(await f.locator('body').evaluate(e=>e.style.overflow),'');
   }finally{await context.close();}
  }
  const context=await browser.newContext({viewport:{width:1440,height:900}});try{
   // Observe actual embedded media events; the defaults are deliberately not zeroed.
   await context.addInitScript(()=>{window.__pacing=[];window.__layout=[];const sample=()=>{const d=document,media=d.getElementById('media-viewport'),controls=d.getElementById('controls'),thumbs=d.getElementById('thumbs'),status=d.getElementById('playback-announcement');if(media&&controls&&thumbs)window.__layout.push({status:status?.textContent,media:media.getBoundingClientRect().toJSON(),controls:controls.getBoundingClientRect().toJSON(),thumbs:thumbs.getBoundingClientRect().toJSON()});};new MutationObserver(sample).observe(document,{subtree:true,childList:true,characterData:true});const play=HTMLMediaElement.prototype.play,seen=new WeakSet();HTMLMediaElement.prototype.play=function(){if(this instanceof HTMLAudioElement&&!seen.has(this)){seen.add(this);for(const type of ['playing','ended'])this.addEventListener(type,()=>window.__pacing.push({type:type==='playing'?'play':type,at:performance.now(),slide:document.querySelector('.lesson-slide:not([hidden])')?.dataset.slide}));}return play.apply(this,arguments);};new MutationObserver(records=>{for(const r of records)if(r.target.matches?.('.lesson-slide')&&!r.target.hidden)window.__pacing.push({type:'slide',at:performance.now(),slide:r.target.dataset.slide});}).observe(document,{subtree:true,attributes:true,attributeFilter:['hidden']});});
   const page=await context.newPage();await page.goto(pathToFileURL(process.env.TK_COURSE_LONG_PAGE).href);const f=page.frameLocator('#course-frame');await f.locator('#home-start').click();await f.locator('#play').click();await f.locator('#playback-announcement').filter({hasText:'첫 화면'}).waitFor();
   await page.waitForFunction(()=>{const w=document.getElementById('course-frame')?.contentWindow;return w?.__pacing?.filter(e=>e.type==='play').length>=2;},{timeout:15000});
   const layout=await f.locator('body').evaluate(()=>window.__layout).then(rows=>rows.filter(r=>r.media.height>0&&r.controls.height>0));assert(layout.some(r=>r.status.includes('첫 화면')));assert(layout.some(r=>r.status.includes('이전 장')));assert(layout.some(r=>r.status.includes('새 화면')));const initial=layout.find(r=>r.status.includes('첫 화면'));for(const row of layout.slice(layout.indexOf(initial)))for(const key of ['media','controls','thumbs'])for(const axis of ['y','height'])assert(Math.abs(row[key][axis]-initial[key][axis])<1,JSON.stringify({key,axis,initial,row}));
   const events=await f.locator('body').evaluate(()=>window.__pacing),end=events.find(e=>e.type==='ended'),next=events.find(e=>e.type==='slide'&&e.slide==='1'),play=events.find(e=>e.type==='play'&&e.slide==='1');assert(end&&next&&play,JSON.stringify(events));assert(next.at-end.at>=1750);assert(play.at-next.at>=1150);assert(play.at-end.at>=2950);assert(play.at-end.at<5000);
  }finally{await context.close();}
 }finally{await browser.close();}
});


test('home, same-lesson, playing/paused transitions and stored resume prepare paused until Play',{skip:!ready,timeout:90000},async()=>{
 const {chromium}=require(process.env.TK_PLAYWRIGHT_MODULE),browser=await chromium.launch({env:{...process.env,...(process.env.TK_BROWSER_FONTCONFIG?{FONTCONFIG_FILE:process.env.TK_BROWSER_FONTCONFIG}:{})},headless:true,executablePath:process.env.TK_CHROMIUM_EXECUTABLE,args:['--no-sandbox','--disable-dev-shm-usage']});
 const context=await browser.newContext({viewport:{width:1440,height:1000}});
 try{
  await context.addInitScript(()=>{window.__mediaPlayCalls=0;const play=HTMLMediaElement.prototype.play;HTMLMediaElement.prototype.play=function(){window.__mediaPlayCalls++;return play.apply(this,arguments);};});
  const page=await context.newPage();await page.goto(pathToFileURL(process.env.TK_COURSE_PAGE).href);const f=page.frameLocator('#course-frame');
  const paused=async()=>{await page.waitForTimeout(5300);assert.equal(await f.locator('body').evaluate(()=>window.__mediaPlayCalls),0);assert.equal(await f.locator('#play').getAttribute('aria-label'),'재생');assert(await f.locator('#live-caption').isHidden());};
  await f.locator('#home-start').click();await paused();
  // Current-lesson links must not be a hidden Play action.
  await f.locator('#toc [data-course-jump]').first().click();await paused();
  await f.locator('#play').click();await page.waitForFunction(()=>document.getElementById('course-frame')?.contentWindow?.__mediaPlayCalls>0);await f.locator('#next-lesson').click();await f.locator('#lesson-heading').filter({hasText:'조건과 결과 2'}).waitFor();await paused();
  await f.locator('#play').click();await f.locator('#play').click();await f.locator('#toc [data-course-jump]').first().click();await f.locator('#lesson-heading').filter({hasText:'조건과 결과 1'}).waitFor();await paused();
  await page.reload();await f.locator('#home-start').click();await f.locator('#player-page').waitFor({state:'visible'});await paused();
 }finally{await context.close();await browser.close();}
});
