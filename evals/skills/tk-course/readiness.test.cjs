const {test}=require('node:test'),assert=require('node:assert/strict');
const {pathToFileURL}=require('node:url');
const ready=!!(process.env.TK_PLAYWRIGHT_MODULE&&process.env.TK_CHROMIUM_EXECUTABLE&&process.env.TK_COURSE_PAGE);
test('optional preparation works offline without storing answers or gating entry',{skip:!ready},async()=>{
 const {chromium}=require(process.env.TK_PLAYWRIGHT_MODULE);
 const browser=await chromium.launch({headless:true,executablePath:process.env.TK_CHROMIUM_EXECUTABLE,args:['--no-sandbox','--disable-dev-shm-usage']});
 try{
  for(const direct of [false,true])for(const width of [390,1280])for(const colorScheme of ['light','dark','no-preference']){
   const context=await browser.newContext({viewport:{width,height:900},colorScheme});
   try{
    await context.route(/^https?:/,route=>route.abort());
    const page=await context.newPage(),errors=[],requests=[];page.on('pageerror',e=>errors.push(e.message));page.on('request',r=>{if(/^https?:/.test(r.url()))requests.push(r.url());});
    await page.goto(pathToFileURL(direct?process.env.TK_COURSE_DIRECT:process.env.TK_COURSE_PAGE).href);
    const f=direct?page:page.frameLocator('#course-frame');
    const storage=()=>f.locator('body').evaluate(()=>Object.fromEntries(Object.entries(localStorage)));
    const before=await storage();
    await f.locator('#readiness-title').focus();await page.keyboard.press('Enter');
    await f.locator('#readiness-check').click();assert.match(await f.locator('[data-readiness-feedback="completion-order"]').innerText(),/미응답/);
    await f.locator('[name="readiness-completion-order"][value="a"]').check();await f.locator('#readiness-check').click();
    assert.match(await f.locator('[data-readiness-feedback="completion-order"]').innerText(),/먼저 시작한 요청/);
    assert.match(await f.locator('[data-readiness-feedback="completion-order"]').innerText(),/사전 복습/);
    await f.locator('[name="readiness-completion-order"][value="a"]').focus();await page.keyboard.press('ArrowDown');
    assert(await f.locator('[name="readiness-completion-order"][value="b"]').isChecked());await f.locator('#readiness-check').click();
    assert.match(await f.locator('[data-readiness-feedback="completion-order"]').innerText(),/정답입니다/);
    assert.deepEqual(await storage(),before);assert.equal(await f.locator('#home-progress-label').innerText(),'0 / 2');
    assert(await f.locator('body').evaluate(el=>el.scrollWidth<=el.ownerDocument.defaultView.innerWidth));
    if(process.env.TK_READINESS_SCREENSHOTS&&!direct&&colorScheme==='light'){
     await f.locator('#readiness fieldset').scrollIntoViewIfNeeded();
     await page.screenshot({path:process.env.TK_READINESS_SCREENSHOTS+`/readiness-${width}.png`});
    }
    await f.locator('#home-start').click();await f.locator('#player-page').waitFor({state:'visible'});
    await f.locator('[data-tab="my-note"]').click();await f.locator('#panel-my-note summary').click();await f.locator('#export').click();
    const progress=JSON.parse(await f.locator('#state-json').inputValue());assert.deepEqual(progress.completed,[]);assert(!JSON.stringify(progress).includes('completion-order'));
    assert.deepEqual(errors,[]);assert.deepEqual(requests,[]);
   }finally{await context.close();}
  }
  const context=await browser.newContext({javaScriptEnabled:false});
  try{const page=await context.newPage();await page.goto(pathToFileURL(process.env.TK_COURSE_PAGE).href);await page.locator('#readiness-title').click();await page.getByText('사전 복습',{exact:true}).click();assert.match(await page.locator('noscript').innerText(),/Promise는 시작 순서/);}finally{await context.close();}
 }finally{await browser.close();}
});
