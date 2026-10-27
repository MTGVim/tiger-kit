// Optional local browser regression; no installation or network access.
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {spawnSync} = require('node:child_process');
const root = path.resolve(__dirname, '../../..');
const pkg = path.join(root,'skills/tk-explain-diff');
const skip = !process.env.TK_PLAYWRIGHT_MODULE || !process.env.TK_CHROMIUM_EXECUTABLE;

test('change groups, evidence, controls and no-JS reading', {skip}, async () => {
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'change-html-'));
  let browser;
  try {
    const output=path.join(dir,'change.html');
    const built=spawnSync('python3',[path.join(pkg,'scripts/build_change.py'),'--model',path.join(pkg,'assets/change-flow-example.json'),'--sources',path.join(pkg,'assets/change-example.sources.json'),'--output',output,'--theme','system'],{encoding:'utf8'});
    assert.equal(built.status,0,built.stderr);
    const {chromium}=require(process.env.TK_PLAYWRIGHT_MODULE);
    browser=await chromium.launch({headless:true,executablePath:process.env.TK_CHROMIUM_EXECUTABLE,args:['--no-sandbox','--disable-dev-shm-usage']});
    for(const width of [1440,390]) for(const colorScheme of ['light','dark']) {
      const context=await browser.newContext({viewport:{width,height:width===390?844:900},colorScheme,reducedMotion:'reduce'});
      const page=await context.newPage(), requests=[], errors=[];
      page.on('request',req=>{if(/^https?:/.test(req.url())) requests.push(req.url());});
      page.on('pageerror',e=>errors.push(String(e)));
      await page.goto(pathToFileURL(output).href);
      assert.equal(await page.locator('section[data-ht-nav-unit]').count(),2);
      assert.ok(await page.locator('#evidence-e-policy-base').isVisible());
      const flow=page.locator('[data-change-flow]').first();
      assert.equal(await flow.locator('[data-change-step][data-active="true"]').count(),1);
      await flow.getByRole('button',{name:'다음 단계'}).click();
      assert.equal(await flow.locator('[data-change-step]').nth(1).getAttribute('data-active'),'true');
      await flow.getByRole('button',{name:'처음으로'}).click();
      assert.equal(await flow.locator('[data-change-step]').first().getAttribute('data-active'),'true');
      const link=page.locator('#cite-change-1-1 a'); await link.click();
      assert.equal(await page.evaluate(()=>location.hash),'#evidence-e-policy-base');
      await page.locator('[data-ht-backlinks="evidence-e-policy-base"] a').first().click();
      assert.equal(await page.evaluate(()=>location.hash),'#cite-change-1-1');
      const font=page.getByLabel('글자 크기'); if(await font.count()) await font.selectOption('200');
      assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth <= innerWidth));
      assert.deepEqual(requests,[]);assert.deepEqual(errors,[]);await context.close();
    }
    const context=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});
    const page=await context.newPage();await page.goto(pathToFileURL(output).href);
    assert.ok(await page.locator('#evidence-e-policy-base').isVisible());
    assert.equal(await page.locator('[data-change-flow-controls]').first().isHidden(),true);
    assert.ok(await page.locator('[data-change-step]').count()>0);await context.close();
  } finally {if(browser)await browser.close();fs.rmSync(dir,{recursive:true,force:true});}
});
