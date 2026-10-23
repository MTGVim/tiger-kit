// Run only with an explicitly configured local browser; test tones are not listening evidence.
const {test}=require('node:test'),assert=require('node:assert/strict');
const {pathToFileURL}=require('node:url');
const ready=!!(process.env.TK_PLAYWRIGHT_MODULE&&process.env.TK_CHROMIUM_EXECUTABLE&&process.env.TK_COURSE_PAGE);
test('shared course preferences, breadcrumb, curriculum and standalone catalog discovery', {skip:!ready},async()=>{
 const {chromium}=require(process.env.TK_PLAYWRIGHT_MODULE),browser=await chromium.launch({headless:true,executablePath:process.env.TK_CHROMIUM_EXECUTABLE,args:['--no-sandbox','--disable-dev-shm-usage']});
 const url=pathToFileURL(process.env.TK_COURSE_PAGE).href;
 async function enter(page){await page.goto(url);const f=page.frameLocator('#course-frame');await f.locator('#home-start').click();await f.locator('#player-page').waitFor({state:'visible'});return f;}
 try{
  for(const width of [390,853,1024,1280])for(const colorScheme of ['light','dark']){
   const context=await browser.newContext({viewport:{width,height:900},colorScheme});
   try{
    const page=await context.newPage(),f=await enter(page);
    assert.equal(await f.locator('#mute-toggle').getAttribute('aria-pressed'),'false');
    assert(await f.locator('#menu-toggle').isVisible());
    const bar=await f.locator('header').boundingBox();assert(bar.height<=72,`${width}: ${bar.height}`);
    assert.equal(await f.locator('#collection-link').getAttribute('target'),'_top');
    await f.locator('#collection-link').waitFor({state:'visible'});
    assert.equal(await f.locator('#back-home,.collection-home').count(),0);
    const widthBefore=(await f.locator('#stage').boundingBox()).width;
    await f.locator('#menu-toggle').click();
    if(width>700){assert((await f.locator('#stage').boundingBox()).width>widthBefore);assert.equal(await f.locator('#menu-toggle').getAttribute('aria-expanded'),'false');}
    await f.locator('#volume').evaluate(el=>{el.value='60';el.dispatchEvent(new Event('input',{bubbles:true}));});
    await f.locator('#caption-opacity').evaluate(el=>{el.value='80';el.dispatchEvent(new Event('input',{bubbles:true}));});
    await f.locator('#next-lesson').click();
    await f.locator('#lesson-heading').filter({hasText:'조건과 결과 2'}).waitFor();
    assert.equal(await f.locator('#volume').inputValue(),'60');assert.equal(await f.locator('#caption-opacity').inputValue(),'80');
    await page.reload();await f.locator('#home-start').click();
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
      const play=HTMLMediaElement.prototype.play;let failed=false;
      HTMLMediaElement.prototype.play=function(){if(!failed&&!this.muted){failed=true;return Promise.reject(new DOMException('blocked','NotAllowedError'));}return play.call(this);};
     }
    },mode);
    const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));const f=await enter(page);
    if(mode==='policy')await f.locator('#sound-toast-message').filter({hasText:'소리를 켜려면'}).waitFor();
    else{assert.equal(await f.locator('#volume').inputValue(),'100');assert.equal(await f.locator('#caption-opacity').inputValue(),'50');}
    assert.deepEqual(errors,[]);
   }finally{await context.close();}
  }
  if(process.env.TK_COURSE_STANDALONE){
   const context=await browser.newContext();try{const page=await context.newPage();await page.goto(pathToFileURL(process.env.TK_COURSE_STANDALONE).href);const f=page.frameLocator('#course-frame');await f.locator('#home-start').waitFor();await page.waitForTimeout(4200);assert(await f.locator('#collection-link').isHidden());}finally{await context.close();}
  }
 }finally{await browser.close();}
});
