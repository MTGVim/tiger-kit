// Exercise the shipped shell through a real local browser; never install a runtime.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {spawnSync} = require('node:child_process');
const root = path.resolve(__dirname, '../../..');
const skip = !process.env.TK_PLAYWRIGHT_MODULE || !process.env.TK_CHROMIUM_EXECUTABLE;
test('offline reader controls, previews, arrival cues and exact copying', {skip}, async () => {
  const {chromium} = require(process.env.TK_PLAYWRIGHT_MODULE);
  const dir = path.join(root, '.tigerkit/evidence/html-artifacts');
  fs.mkdirSync(dir, {recursive:true});
  const source = 'const result: Result = api.read({enabled: true, label: `hi ${user.name}`});\n\n';
  const built = spawnSync('python3', ['-c', `import sys
sys.path.insert(0, 'skills/tk-explain/scripts')
from build_html import assemble
from highlight_code import highlight
from package_html import package
from pathlib import Path
root = Path(sys.argv[1])
code = highlight(sys.stdin.read(), 'ts', 10).replace('<pre ', '<pre data-label="reader.ts" ', 1)
body = '<p><a id="term-link" href="#term">Term</a> <a id="appendix-link" href="#appendix">Appendix</a> <a id="section-link" href="#section" data-ht-preview>Section</a> <a id="external" href="https://example.org/guide" aria-label="Guide">Guide</a></p>' + code + '<section id="intro"><h2>Introduction</h2><p id="sentence">Actual source context <sup id="cite-1"><a href="#ref-1">[1]</a></sup></p></section><div style="height:1800px"></div><section id="section"><h2>Destination</h2><dl><dt id="term">Term title</dt><dd>' + ('Definition text ' * 50) + '</dd></dl><ol><li id="appendix"><h3>Appendix title</h3><p>Appendix explanation</p></li><li id="ref-1"><a href="https://example.org/source">Source title</a><span>Source evidence</span> <a id="backlink" href="#cite-1">↩</a></li></ol></section>'
(root / 'reader.html').write_text(assemble(body, 'Reader test'))
package(root, ['reader.html'], 'reader.html')
` ,dir], {cwd:root, input:source, encoding:'utf8'});
  assert.equal(built.status, 0, built.stderr);
  if(process.env.TK_FONT_FILE) {
    const file=path.join(dir,'reader.html');
    const font=fs.readFileSync(process.env.TK_FONT_FILE).toString('base64');
    fs.writeFileSync(file,fs.readFileSync(file,'utf8').replace('</style>',`@font-face{font-family:FixtureKorean;src:url(data:font/otf;base64,${font})} :root{--font-family:FixtureKorean,sans-serif} </style>`));
  }
  const browser = await chromium.launch({headless:true, executablePath:process.env.TK_CHROMIUM_EXECUTABLE,args:['--no-sandbox','--disable-dev-shm-usage']});
  const records=[];
  try {
    for (const width of [1280,390]) for (const theme of ['light','dark']) {
      const context = await browser.newContext({viewport:{width,height:900},colorScheme:theme});
      await context.addInitScript(() => {
        window.copyResults=[];
        Object.defineProperty(navigator,'clipboard',{value:{writeText:async value=>copyResults.push(value)},configurable:true});
        Object.defineProperty(navigator,'canShare',{value:()=>true,configurable:true});
        Object.defineProperty(navigator,'share',{value:async()=>{throw Error('Must not share local files');},configurable:true});
      });
      const page = await context.newPage(); const errors=[],requests=[];
      page.on('pageerror',e=>errors.push(String(e)));
      page.on('request',r=>{if(!r.url().startsWith('file:'))requests.push(r.url());});
      await page.goto(pathToFileURL(path.join(dir,'reader.html')).href);
      assert.equal(await page.locator('[data-ht-share]').isHidden(),true);
      assert.equal(await page.locator('[data-ht-download]').isVisible(),true);
      assert.equal(await page.locator('[data-ht-download] svg').count(),1);
      assert.equal(await page.locator('.ht-code-toolbar').count(),1);
      assert.equal(await page.locator('.ht-code-label').innerText(),'reader.ts');
      assert.equal(await page.locator('pre code').textContent(),source);
      await page.locator('[data-ht-copy]').click();
      assert.deepEqual(await page.evaluate(()=>copyResults),[source]);
      assert.match(await page.locator('.ht-code-toolbar [aria-live]').textContent(),/복사했습니다/);
      await page.locator('.ht-code-toolbar [aria-pressed]').press('Space');
      assert.equal(await page.locator('.ht-code-toolbar [aria-pressed]').getAttribute('aria-pressed'),'true');
      assert.equal(await page.locator('pre code').textContent(),source);
      // Clipboard denial falls back without dropping source bytes, focus or selection.
      await page.evaluate(()=>{
        navigator.clipboard.writeText=async()=>{throw Error('denied');};
        document.execCommand=()=>{copyResults.push(document.activeElement.value);return true;};
      });
      await page.locator('[data-ht-copy]').press('Enter');
      assert.deepEqual(await page.evaluate(()=>copyResults),[source,source]);
      assert.equal(await page.locator('[data-ht-copy]').evaluate(e=>e===document.activeElement),true);
      assert.equal(await page.locator('textarea').count(),0);
      assert.equal(await page.locator('#external').getAttribute('target'),'_blank');
      assert.match(await page.locator('#external').getAttribute('rel'),/noopener/);
      assert.match(await page.locator('#external').getAttribute('aria-label'),/새 탭/);
      const contrast=await page.locator('pre').evaluate(pre=>{
        const lum=color=>color.match(/[\d.]+/g).slice(0,3).map(Number).map(x=>{x/=255;return x<=.04045?x/12.92:((x+.055)/1.055)**2.4;}).reduce((v,x,i)=>v+x*[.2126,.7152,.0722][i],0);
        const bg=lum(getComputedStyle(pre).backgroundColor);
        return [...pre.querySelectorAll('code span:not(.ht-code-line)')].map(e=>{const fg=lum(getComputedStyle(e).color);return(Math.max(fg,bg)+.05)/(Math.min(fg,bg)+.05);});
      });
      assert.ok(Math.min(...contrast)>=4.5,`${theme}: ${Math.min(...contrast)}`);
      for(const [id,expected] of [['term-link','Term title'],['appendix-link','Appendix explanation'],['section-link','Destination'],['backlink','Actual source context']]) {
        const link=page.locator('#'+id); await link.scrollIntoViewIfNeeded();await link.focus();
        const tip=page.locator('.ht-citation-preview');await tip.waitFor({state:'visible'});
        assert.match(await tip.innerText(),new RegExp(expected));
        const size=await tip.boundingBox();assert.ok(size.x>=0&&size.y>=0&&size.x+size.width<=width&&size.y+size.height<=900);
        if(id==='term-link')assert.ok((await tip.innerText()).length<300);
        await page.keyboard.press('Escape');assert.equal(await tip.isHidden(),true);
      }
      await page.locator('#cite-1 a').scrollIntoViewIfNeeded();await page.locator('#cite-1 a').focus();
      assert.equal(await page.locator('.ht-preview-title').textContent(),'Source title');
      assert.equal(await page.locator('.ht-citation-preview > span').textContent(),'Source evidence');
      await page.locator('#term-link').scrollIntoViewIfNeeded();await page.locator('#term-link').focus();
      if(process.env.TK_READER_SCREENSHOTS)await page.screenshot({path:path.join(dir,`reader-${width}-${theme}.png`)});
      await page.locator('#term-link').click();
      assert.equal(await page.locator('#term').evaluate(e=>e.classList.contains('ht-arrival')),true);
      assert.equal(await page.locator('#term + dd').evaluate(e=>e.classList.contains('ht-arrival')),true);
      // Simulated continuous scroll events keep the cue alive past its first timeout.
      for(let i=0;i<5;i++){await page.waitForTimeout(300);await page.evaluate(()=>document.dispatchEvent(new Event('scroll')));}
      assert.equal(await page.locator('#term').evaluate(e=>e.classList.contains('ht-arrival-fade')),false);
      await page.waitForFunction(()=>!document.querySelector('#term').classList.contains('ht-arrival'));
      await page.locator('#term-link').click();
      assert.equal(await page.locator('#term').evaluate(e=>e.classList.contains('ht-arrival')),true);
      await page.locator('#section-link').click();
      assert.equal(await page.locator('#term').evaluate(e=>e.classList.contains('ht-arrival')),false);
      assert.equal(await page.locator('#section').evaluate(e=>e.classList.contains('ht-arrival')),false);
      assert.equal(await page.locator('#section > h2').evaluate(e=>e.classList.contains('ht-arrival')),true);
      await page.locator('#section > h2').click();
      assert.equal(await page.locator('.ht-arrival').count(),0);
      await page.emulateMedia({reducedMotion:'reduce'});
      await page.locator('#section-link').click();
      await page.waitForFunction(()=>document.querySelector('#section > h2').classList.contains('ht-arrival-fade'));
      assert.equal(await page.locator('#section > h2').evaluate(e=>getComputedStyle(e).transitionDuration),'0s');
      assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
      assert.deepEqual(errors,[]);assert.deepEqual(requests,[]);
      records.push({width,theme,minContrast:Math.min(...contrast),checks:'Pass'});
      await context.close();
    }
    const context=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:900}});
    const page=await context.newPage();await page.goto(pathToFileURL(path.join(dir,'reader.html')).href);
    assert.equal(await page.locator('.ht-code-toolbar').count(),0);
    assert.equal(await page.locator('pre code').textContent(),source);
    await page.locator('#term-link').click();assert.match(page.url(),/#term$/);await context.close();
    fs.writeFileSync(path.join(dir,'reader-results.json'),JSON.stringify({headless:true,browser:browser.version(),records},null,2));
  } finally {await browser.close();}
});
