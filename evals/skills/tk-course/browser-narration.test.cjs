const {test}=require('node:test'),assert=require('node:assert/strict'),{pathToFileURL}=require('node:url');
const ready=process.env.TK_PLAYWRIGHT_MODULE&&process.env.TK_CHROMIUM_EXECUTABLE&&process.env.TK_COURSE_BROWSER_PAGE;
test('browser narration keeps settings and explicit silent recovery reachable',{skip:!ready,timeout:45000},async()=>{
 const {chromium}=require(process.env.TK_PLAYWRIGHT_MODULE),browser=await chromium.launch({headless:true,executablePath:process.env.TK_CHROMIUM_EXECUTABLE,args:['--no-sandbox']});
 try{
  const context=await browser.newContext({viewport:{width:1440,height:1000}}),page=await context.newPage(),errors=[];
  page.on('pageerror',e=>errors.push(e.message));await page.goto(pathToFileURL(process.env.TK_COURSE_BROWSER_PAGE).href);
  const f=page.frameLocator('#course-frame');await f.locator('#home-start').click();
  assert.equal(await f.locator('#voice-mode').inputValue(),'device');
  await f.locator('#settings-toggle').click();assert(await f.locator('#playback-settings').isVisible());
  await f.locator('#settings-toggle').click();
  if(await f.locator('#voice-fallback').isVisible()){
   assert(await f.locator('#play').isDisabled());assert.equal(await f.locator('#player-status').innerText(),'');
   await f.locator('#use-silent').click();assert.equal(await f.locator('#voice-mode').inputValue(),'silent');
   assert(await f.locator('#play').isEnabled());assert.equal(await f.locator('#play').getAttribute('aria-label'),'일시정지');
   await f.locator('#play').click();assert.equal(await f.locator('#play').getAttribute('aria-label'),'재생');
   const fs=require('node:fs'),path=require('node:path'),audit=fs.readFileSync(path.resolve(__dirname,'../../../skills/tk-course/scripts/slide_geometry.js'),'utf8');
   for(const width of [1440,390])for(const slide of [0,1]){
    await page.setViewportSize({width,height:1000});await f.locator('[data-thumb="'+slide+'"]').click();
    await f.locator('#play').click();await f.locator('#play').click();
    await f.locator('#fullscreen').click();await page.waitForTimeout(100);
    const report=await f.locator('.lesson-slide:not([hidden]) svg:visible').evaluate((svg,source)=>eval(source)(svg),audit);
    if(process.env.TK_COURSE_BROWSER_EVIDENCE)await page.screenshot({path:path.join(process.env.TK_COURSE_BROWSER_EVIDENCE,'grid-'+slide+'-'+width+'.png')});
    assert(report.ok,JSON.stringify({slide,width,...report}));await f.locator('#fullscreen').click();
   }
  }
  assert.deepEqual(errors,[]);await context.close();
 }finally{await browser.close();}
});
