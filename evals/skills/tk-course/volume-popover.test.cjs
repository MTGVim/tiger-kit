// Requires explicitly configured installed Playwright/Chromium; never installs a browser.
const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {pathToFileURL}=require('node:url');
const configured=!!(process.env.TK_PLAYWRIGHT_MODULE&&process.env.TK_CHROMIUM_EXECUTABLE&&process.env.TK_COURSE_PAGE);
test('volume popup preserves toolbar height and native keyboard/touch access', {skip:!configured},async()=>{
 const {chromium}=require(process.env.TK_PLAYWRIGHT_MODULE);
 const browser=await chromium.launch({env:{...process.env,...(process.env.TK_BROWSER_FONTCONFIG?{FONTCONFIG_FILE:process.env.TK_BROWSER_FONTCONFIG}:{})},headless:true,executablePath:process.env.TK_CHROMIUM_EXECUTABLE,args:['--no-sandbox','--disable-dev-shm-usage']});
 const url=pathToFileURL(process.env.TK_COURSE_PAGE).href,evidence=process.env.TK_VOLUME_EVIDENCE_DIR;
 if(evidence)fs.mkdirSync(evidence,{recursive:true});
 async function lesson(page){
  await page.goto(url);const frame=page.frameLocator('#course-frame');
  await frame.locator('#home-start').click();await frame.locator('#player-page').waitFor({state:'visible'});
  return frame;
 }
 async function bounded(frame,width){
  const box=await frame.locator('#volume-panel').boundingBox();assert(box);assert(box.x>=0&&box.x+box.width<=width);assert(box.y>=0&&box.y+box.height<=900);
 }
 try{
  for(const colorScheme of ['light','dark'])for(const width of [390,600,800,1024,1440]){
   const context=await browser.newContext({viewport:{width,height:900},deviceScaleFactor:1,colorScheme});
   try{
    const page=await context.newPage(),frame=await lesson(page),toolbar=frame.locator('#controls'),mute=frame.locator('#mute-toggle'),panel=frame.locator('#volume-panel');
    await frame.locator('body').evaluate(el=>el.ownerDocument.fonts.ready.then(()=>true));
    const before=(await toolbar.boundingBox()).height;
    await mute.hover();await panel.waitFor({state:'visible'});await bounded(frame,width);
    assert.equal((await toolbar.boundingBox()).height,before,`${width} ${colorScheme} hover`);
    if(evidence)await page.screenshot({path:path.join(evidence,`${width}-${colorScheme}-hover.png`)});
    await mute.click();await page.keyboard.press('Tab');
    assert(await frame.locator('#volume').evaluate(el=>el===el.ownerDocument.activeElement));
    const value=Number(await frame.locator('#volume').inputValue());await page.keyboard.press('ArrowLeft');
    assert.equal(Number(await frame.locator('#volume').inputValue()),Math.max(0,value-1));
    await page.keyboard.press('Escape');assert(await panel.isHidden());
    assert(await mute.evaluate(el=>el===el.ownerDocument.activeElement));
    assert.equal((await toolbar.boundingBox()).height,before,`${width} ${colorScheme} escape`);
    // Reopen at the same focused button, then verify the open panel after viewport resize.
    await mute.click();await bounded(frame,width);await page.setViewportSize({width:390,height:900});await bounded(frame,390);
   }finally{await context.close();}
  }
  const context=await browser.newContext({viewport:{width:390,height:900},deviceScaleFactor:1,hasTouch:true,isMobile:true});
  try{
   const page=await context.newPage(),frame=await lesson(page),toolbar=frame.locator('#controls');
   const before=(await toolbar.boundingBox()).height;
   await frame.locator('#mute-toggle').tap();await frame.locator('#volume-panel').waitFor({state:'visible'});await bounded(frame,390);
   assert.equal((await toolbar.boundingBox()).height,before);
   await frame.locator('#captions-toggle').tap();assert(await frame.locator('#volume-panel').isHidden());
   assert.equal((await toolbar.boundingBox()).height,before);
  }finally{await context.close();}
 }finally{await browser.close();}
});
