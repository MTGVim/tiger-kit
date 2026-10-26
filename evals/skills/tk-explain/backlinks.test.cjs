const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {spawnSync} = require('node:child_process');
const root = path.resolve(__dirname, '../../..');
const skip = !process.env.TK_PLAYWRIGHT_MODULE || !process.env.TK_CHROMIUM_EXECUTABLE;
test('numbered return links keep native navigation and only identify an observed origin', {skip}, async () => {
  const dir = path.join(root, '.tigerkit/evidence/backlinks');
  fs.mkdirSync(dir, {recursive:true});
  const body = `<section id="first"><h2>First context</h2><p>First use of <a id="foo-1" href="#foo">FOO<sup>[1]</sup></a>.</p></section>
<section id="second"><h2>Second context</h2><p>${'Earlier unrelated prose. '.repeat(25)} Second use of <a id="foo-2" href="#foo">FOO<sup>[2]</sup></a>.</p>
<p>Evidence A<sup id="cite-1-1"><a href="#ref-1">[1.1]</a></sup>. Evidence B<sup id="cite-1-2"><a href="#ref-1">[1.2]</a></sup>.</p>
<p><a id="single" href="#bar">BAR</a></p></section>
<section id="terms"><h2>Definitions</h2><dl><dt id="foo">FOO definition</dt><dd>Definition sentence.
<span class="ht-backlinks" data-ht-backlinks="foo">본문으로 ↩ <a href="#foo-1">[1]</a> <a href="#foo-2" aria-label="두 번째 위치로 복귀">[2]</a></span></dd>
<dt id="bar">BAR definition</dt><dd>Single occurrence. <span class="ht-backlinks" data-ht-backlinks="bar"><a href="#single">본문으로 돌아가기</a></span></dd></dl></section>
<section id="refs"><h2>References</h2><ol><li id="ref-1">Evidence source.
<span class="ht-backlinks" data-ht-backlinks="ref-1">본문으로 ↩ <a href="#cite-1-1">[1.1]</a> <a href="#cite-1-2">[1.2]</a></span></li></ol></section>`;
  const result=spawnSync('python3',['-c',`import sys
sys.path.insert(0,'skills/tk-explain/scripts')
from build_html import assemble
print(assemble(sys.stdin.read(),'Backlink test'))`],{cwd:root,input:body,encoding:'utf8'});
  assert.equal(result.status,0,result.stderr);
  let html=result.stdout;
  if(process.env.TK_FONT_FILE)html=html.replace('</style>',`@font-face{font-family:FixtureKorean;src:url(data:font/otf;base64,${fs.readFileSync(process.env.TK_FONT_FILE).toString('base64')})}:root{--font-family:FixtureKorean,sans-serif}</style>`);
  const file=path.join(dir,'backlinks.html');fs.writeFileSync(file,html);
  const {chromium}=require(process.env.TK_PLAYWRIGHT_MODULE);
  const browser=await chromium.launch({headless:true,executablePath:process.env.TK_CHROMIUM_EXECUTABLE,args:['--no-sandbox','--disable-dev-shm-usage']});
  try {
    for(const width of [390,1280])for(const theme of ['light','dark']) {
      const context=await browser.newContext({viewport:{width,height:900},colorScheme:theme,reducedMotion:'reduce'});
      const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(String(e)));
      await page.goto(pathToFileURL(file).href+'#foo');
      const mark=page.locator('.ht-backlink-current');
      const back=page.locator('[data-ht-backlinks="foo"] a[href="#foo-2"]');
      assert.equal(await mark.count(),0);
      await page.locator('#foo-2').press('Enter');
      assert.equal(await mark.count(),1);
      assert.equal(await mark.locator('..').getAttribute('href'),'#foo-2');
      assert.match(await back.getAttribute('aria-label'),/읽던 곳/);
      await back.focus();
      assert.match(await page.locator('.ht-citation-preview').innerText(),/Second context/);
      assert.match(await page.locator('.ht-citation-preview').innerText(),/Second use of FOO/);
      await page.screenshot({path:path.join(dir,`backlinks-${width}-${theme}.png`)});
      await back.press('Enter');assert.match(page.url(),/#foo-2$/);
      assert.equal(await mark.count(),0);
      assert.equal(await back.getAttribute('aria-label'),'두 번째 위치로 복귀');
      await page.goBack();assert.match(page.url(),/#foo$/);assert.equal(await mark.count(),0);
      await page.goForward();assert.match(page.url(),/#foo-2$/);
      await page.locator('#foo-1').click();assert.equal(await mark.locator('..').getAttribute('href'),'#foo-1');
      await page.locator('#foo-2').click();assert.equal(await mark.locator('..').getAttribute('href'),'#foo-2');
      // Modified and canceled activation cannot overwrite the known same-tab origin.
      await page.locator('#foo-1').dispatchEvent('click',{ctrlKey:true,button:0});
      assert.equal(await mark.locator('..').getAttribute('href'),'#foo-2');
      await page.evaluate(()=>{const link=document.querySelector('#foo-1');link.addEventListener('click',e=>e.preventDefault(),{once:true});link.click();});
      assert.equal(await mark.locator('..').getAttribute('href'),'#foo-2');
      await page.locator('#foo-2').focus();
      assert.doesNotMatch(await page.locator('.ht-citation-preview').innerText(),/읽던 곳|본문으로/);
      await page.reload();assert.equal(await mark.count(),0);
      await page.locator('#cite-1-2 a').click();assert.equal(await mark.locator('..').getAttribute('href'),'#cite-1-2');
      await page.locator('a[href="#cite-1-2"]').click();assert.match(page.url(),/#cite-1-2$/);
      assert.equal(await mark.count(),0);
      await page.locator('#single').click();assert.equal(await mark.count(),0);
      await page.locator('a[href="#single"]').click();assert.match(page.url(),/#single$/);
      assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
      assert.deepEqual(errors,[]);await context.close();
    }
    const context=await browser.newContext({javaScriptEnabled:false,reducedMotion:'reduce',viewport:{width:390,height:900}});
    const page=await context.newPage();await page.goto(pathToFileURL(file).href);
    // The native no-JS mobile contents panel starts open; close it as a reader would.
    await page.locator('.ht-doc-toc > summary').press('Enter');
    assert.equal(await page.locator('#foo-2 sup').textContent(),'[2]');
    await page.locator('#foo-2').click();assert.match(page.url(),/#foo$/);
    await page.locator('a[href="#foo-2"]').click();assert.match(page.url(),/#foo-2$/);
    await page.locator('#cite-1-2 a').click();assert.match(page.url(),/#ref-1$/);
    await page.locator('a[href="#cite-1-2"]').click();assert.match(page.url(),/#cite-1-2$/);
    assert.equal(await page.locator('.ht-backlink-current').count(),0);
    await context.close();
  } finally {await browser.close();}
});
