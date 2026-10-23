const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),{pathToFileURL}=require('node:url');
const ready=!!(process.env.TK_PLAYWRIGHT_MODULE&&process.env.TK_CHROMIUM_EXECUTABLE&&process.env.TK_CATALOG_FIXTURE);
test('catalog order/date sorting, readable responsive cards, player preferences, fullscreen and shortcuts',{skip:!ready,timeout:120000},async()=>{
 const {chromium}=require(process.env.TK_PLAYWRIGHT_MODULE),browser=await chromium.launch({env:{...process.env,...(process.env.TK_BROWSER_FONTCONFIG?{FONTCONFIG_FILE:process.env.TK_BROWSER_FONTCONFIG}:{})},headless:true,executablePath:process.env.TK_CHROMIUM_EXECUTABLE,args:['--no-sandbox','--disable-dev-shm-usage','--enable-automation']});
 const capture=async(page,name)=>{if(process.env.TK_CATALOG_SCREENSHOTS){fs.mkdirSync(process.env.TK_CATALOG_SCREENSHOTS,{recursive:true});await page.screenshot({path:path.join(process.env.TK_CATALOG_SCREENSHOTS,name+'.png'),fullPage:true});}};
 const root=process.env.TK_CATALOG_FIXTURE,url=file=>pathToFileURL(path.join(root,file)).href,errors=[];
 try{
  const session=await browser.newBrowserCDPSession(),args=(await session.send('Browser.getBrowserCommandLine')).arguments;
  assert(args.some(x=>x.startsWith('--headless')));assert(args.some(x=>x.startsWith('--user-data-dir=')));
  for(const width of [1440,1024,390,619,620,643,644,923,924]){
   const context=await browser.newContext({viewport:{width,height:900}});try{
    const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));await page.goto(url('dist/index.html'));await page.evaluate(()=>document.fonts.ready);
    const geometry=await page.evaluate(()=>{let cards=[...document.querySelectorAll('[data-catalog-card]')].map(e=>e.getBoundingClientRect()),control=document.querySelector('#catalog-search-controls').getBoundingClientRect();return {center:(Math.min(...cards.map(r=>r.left))+Math.max(...cards.map(r=>r.right)))/2,controls:control.x+control.width/2,width:innerWidth,overflow:document.documentElement.scrollWidth>innerWidth,clipped:[...document.querySelectorAll('.catalog-copy h2,.catalog-description,.catalog-meta span,.catalog-dates')].some(e=>e.scrollHeight>e.clientHeight+1||e.scrollWidth>e.clientWidth+1)};});
    assert(Math.abs(geometry.center-width/2)<=1,JSON.stringify(geometry));assert(Math.abs(geometry.controls-width/2)<=1);assert(!geometry.overflow);assert(!geometry.clipped);if(width===390||width===1440)await capture(page,'cards-'+width);
    const before=await page.locator('[data-catalog-card]').first().boundingBox();await page.locator('#catalog-search').pressSequentially('course-1');
    // A filter with zero results does not alter horizontal geometry through scrollbar changes.
    const empty=await page.locator('#catalog-empty').boundingBox();assert(Math.abs(empty.x+empty.width/2-width/2)<=1);await page.locator('#catalog-clear').click();
    const after=await page.locator('[data-catalog-card]').first().boundingBox();assert(Math.abs(before.x-after.x)<1);assert(Math.abs(before.width-after.width)<1);
   }finally{await context.close();}
  }
  const context=await browser.newContext();try{
   const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));await page.goto(url('dist/index.html'));
   const ids=()=>page.locator('[data-catalog-card]').evaluateAll(es=>es.map(e=>e.dataset.courseId));
   assert.deepEqual(await ids(),['course-1','course-2','course-3','course-4']);assert(await page.locator('#catalog-direction').isDisabled());
   await page.locator('#catalog-sort').focus();await page.keyboard.press('ArrowDown');
   assert.equal(await page.locator('#catalog-sort').inputValue(),'updated_at');assert.deepEqual(await ids(),['course-1','course-2','course-3','course-4']);
   await page.locator('#catalog-direction').click();assert.deepEqual(await ids(),['course-3','course-1','course-2','course-4']);assert.equal(await page.locator('#catalog-direction').getAttribute('aria-pressed'),'true');
   await page.locator('#catalog-sort').focus();await page.keyboard.press('ArrowDown');assert.deepEqual(await ids(),['course-2','course-1','course-3','course-4']);
   await page.reload();assert.equal(await page.locator('#catalog-sort').inputValue(),'created_at');assert.equal(await page.locator('#catalog-direction').getAttribute('aria-pressed'),'true');
   await page.locator('#catalog-search').pressSequentially('needle');const visible=await page.locator('[data-catalog-card]:visible').count();await page.locator('#catalog-direction').click();assert.equal(await page.locator('[data-catalog-card]:visible').count(),visible);
   await page.locator('#catalog-sort').focus();await page.keyboard.press('Home');assert(await page.locator('#catalog-direction').isDisabled());
  }finally{await context.close();}
  for(const mode of ['denied','corrupt']){const context=await browser.newContext();try{await context.addInitScript(mode=>{if(mode==='denied')Object.defineProperty(window,'localStorage',{get(){throw Error('blocked');}});else localStorage.setItem('tigerkit-course-catalog:sort','{bad');},mode);const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));await page.goto(url('dist/index.html'));assert.equal(await page.locator('#catalog-sort').inputValue(),'recommended');await page.locator('#catalog-sort').focus();await page.keyboard.press('ArrowDown');assert(await page.locator('#catalog-direction').isEnabled());}finally{await context.close();}}
  for(const blocked of [false,true]){
   const context=await browser.newContext({viewport:{width:1024,height:900}});try{
    const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));await page.goto(url(blocked?'blocked.html':'player-dist/player/index.html'));
    const f=blocked?page.frameLocator('#host').frameLocator('#course-frame'):page.frameLocator('#course-frame');
    await f.locator('#home-start').click();assert.equal(await f.locator('#mute-toggle').getAttribute('aria-pressed'),'true');assert.equal(await f.locator('#captions-toggle').getAttribute('aria-pressed'),'true');assert.equal(await f.locator('#sound-toast-message').textContent(),'소리 꺼짐 · 자막 켜짐');
    await f.locator('#slide-wrap').focus();await page.keyboard.press('k');await page.keyboard.press('ArrowRight');assert.equal(await f.locator('#tx-copy .tx-cue.active').getAttribute('data-cue'),'1');await page.keyboard.press('ArrowLeft');assert.equal(await f.locator('#tx-copy .tx-cue.active').getAttribute('data-cue'),'0');
    await page.keyboard.press('m');assert.equal(await f.locator('#mute-toggle').getAttribute('aria-pressed'),'false');await page.keyboard.press('c');assert.equal(await f.locator('#captions-toggle').getAttribute('aria-pressed'),'false');
    await capture(page,blocked?'entry-blocked':'entry');await page.keyboard.press('?');assert(await f.locator('#shortcut-help').isVisible());await capture(page,blocked?'help-blocked':'help');await page.keyboard.press('Escape');assert(await f.locator('#shortcut-help').isHidden());
    await f.locator('#fullscreen').click();
    if(blocked){assert(await f.locator('#stage').evaluate(e=>e.classList.contains('stage-expanded')));assert(await f.locator('#fullscreen-status').isVisible());const r=await f.locator('#stage').boundingBox();assert(r.width>=1000);await capture(page,'expanded');await page.keyboard.press('Escape');assert(!(await f.locator('#stage').evaluate(e=>e.classList.contains('stage-expanded'))));}
    else{assert(await f.locator('#stage').evaluate(e=>e.ownerDocument.fullscreenElement===e));await f.locator('#fullscreen').click();}
    await f.locator('#tab-my-note').click();await f.locator('#memo').pressSequentially('mcf?k');assert.equal(await f.locator('#memo').inputValue(),'mcf?k');assert(await f.locator('#shortcut-help').isHidden());
    await page.reload();await f.locator('#home-start').click();assert.equal(await f.locator('#mute-toggle').getAttribute('aria-pressed'),'false');assert.equal(await f.locator('#captions-toggle').getAttribute('aria-pressed'),'false');
   }finally{await context.close();}
  }
  if(fs.existsSync(path.join(root,'video-dist/video/index.html'))){const context=await browser.newContext();try{const page=await context.newPage();await page.goto(url('video-dist/video/index.html'));const f=page.frameLocator('#course-frame');await f.locator('#home-start').click();await f.locator('#slide-wrap').focus();await page.keyboard.press('k');await page.keyboard.press('ArrowRight');assert(await f.locator('#lesson-video').evaluate(v=>v.currentTime>=5&&v.currentTime<5.5));await page.keyboard.press('ArrowLeft');assert(await f.locator('#lesson-video').evaluate(v=>v.currentTime<.5));}finally{await context.close();}}
  assert.deepEqual(errors,[]);
 }finally{await browser.close();}
});
