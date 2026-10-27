// Optional local browser regression; no provider download.
const test=require('node:test'), assert=require('node:assert/strict'), fs=require('node:fs');
const os=require('node:os'),path=require('node:path'),{spawnSync}=require('node:child_process'),{pathToFileURL}=require('node:url');
const root=path.resolve(__dirname,'../../..'),pkg=path.join(root,'skills/tk-teach');
const skip=!process.env.TK_PLAYWRIGHT_MODULE||!process.env.TK_CHROMIUM_EXECUTABLE;
test('lesson focus, scoped retry and native fallbacks', {skip}, async()=>{
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'lesson-html-'));let browser;
  try{
    const output=path.join(dir,'lesson.html');
    const built=spawnSync('python3',[path.join(pkg,'scripts/build_html.py'),'--profile','lesson','--body',path.join(pkg,'assets/lesson-example.html'),'--title','Lesson','--output',output,'--theme','system'],{encoding:'utf8'});
    assert.equal(built.status,0,built.stderr);
    const {chromium}=require(process.env.TK_PLAYWRIGHT_MODULE);
    browser=await chromium.launch({headless:true,executablePath:process.env.TK_CHROMIUM_EXECUTABLE,args:['--no-sandbox','--disable-dev-shm-usage']});
    for(const width of [1440,390])for(const colorScheme of ['light','dark']){
      const context=await browser.newContext({viewport:{width,height:width===390?844:900},colorScheme,reducedMotion:'reduce'}),page=await context.newPage(),requests=[];
      page.on('request',r=>{if(/^https?:/.test(r.url()))requests.push(r.url())});await page.goto(pathToFileURL(output).href);
      await page.locator('[data-ht-focus]').press('Enter');assert.equal(await page.evaluate(()=>location.hash),'#expiry-code');
      assert.equal(await page.locator('#expiry-code').evaluate(e=>e.classList.contains('ht-lesson-focus')),true);
      const hint=page.locator('[data-ht-hint]'),solution=page.locator('[data-ht-solution]');
      await hint.locator('summary').click();await solution.locator('summary').click();
      assert.ok(await hint.getAttribute('open')!==null);await page.locator('[data-ht-retry]').press('Enter');
      assert.equal(await hint.getAttribute('open'),null);assert.equal(await solution.getAttribute('open'),null);
      const font=page.getByLabel('글자 크기');if(await font.count())await font.selectOption('200');
      assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));assert.deepEqual(requests,[]);await context.close();
    }
    const context=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}}),page=await context.newPage();
    await page.goto(pathToFileURL(output).href);assert.ok(await page.locator('#expiry-code').isVisible());
    await page.locator('[data-ht-hint] summary').click();assert.ok(await page.locator('[data-ht-hint]').getAttribute('open')!==null);
    await page.locator('[data-ht-retry]').click();assert.equal(await page.evaluate(()=>location.hash),'#expiry-practice');await context.close();
  } finally {if(browser)await browser.close();fs.rmSync(dir,{recursive:true,force:true});}
});
