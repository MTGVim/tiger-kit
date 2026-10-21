// Local-only: explicit installed Playwright and browser; no package/browser installation.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {spawnSync} = require('node:child_process');
const root = path.resolve(__dirname, '../../..');
const asset = name => fs.readFileSync(path.join(root, 'skills/tk-explain/assets', name), 'utf8');
const sources = [
  '/* multiline\n * comment */\n@Composable\nval count = 42\nfun greeting(name: String): String = "<safe> & 한글"\n\n    val veryLongDeclaration = "' + 'LongIdentifier'.repeat(45) + '"\n',
  '+ added ' + 'longDiffLine'.repeat(55) + '\n- removed\n unchanged\n',
  '\n  unknown <tag> & text\n\t\n',
];
const code = sources.map((source, i) => {
  const result = spawnSync('python3', ['-c', 'import sys; sys.path.insert(0, "skills/tk-explain/scripts"); from highlight_code import highlight; print(highlight(sys.stdin.read(), sys.argv[1], 20), end="")', ['kt','diff','unknown'][i]], {cwd:root,input:source,encoding:'utf8'});
  assert.equal(result.status, 0, result.stderr); return result.stdout;
}).join('');
const reference = fs.readFileSync(path.join(root,'skills/tk-explain/references/html-output.md'),'utf8');
function html(css=asset('html-theme.css')) {
  if (process.env.TK_FONT_FILE) css += `@font-face {font-family:FixtureKorean;src:url(data:font/otf;base64,${fs.readFileSync(process.env.TK_FONT_FILE).toString('base64')})} :root {--font-family:FixtureKorean,sans-serif}`;
  let markup = reference.match(/```html\n([\s\S]*?)\n```/)[1];
  markup = markup.replace('<!-- Sections. -->', `<h1>공용 문서 셸 검증</h1><p class="ht-lede">본문과 footer를 가운데 정렬합니다.</p><section id="overview"><h2>목표와 결론</h2><h3>코드 원문을 보존합니다.</h3>${code}<div style="height:1000px" aria-hidden="true"></div></section><section id="conditions"><h2>판단 조건</h2><table class="ht-table-scroll"><tbody><tr><td>본문 크기</td></tr></tbody></table><dl><dt>조건</dt><dd>정렬과 원문 보존</dd></dl></section><section id="sources"><h2>참고문헌</h2><ol><li id="ref-1">현재 셸 소스</li></ol></section>`)
    .replace('<footer id="document-bottom">...</footer>', '<footer id="document-bottom"><p>기준: TigerKit 공용 문서 셸</p><p>작성일: 2026-10-21</p><p>AI가 작성했습니다.</p></footer>');
  return `<!doctype html><html lang="ko" data-default-theme="system"><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>공용 셸 검증</title><style>${css}</style></head>${markup}<script>${asset('html-theme.js')}</script></body></html>`;
}
test('centered shell, footer, status, code and native fallbacks', {skip:!process.env.TK_PLAYWRIGHT_MODULE || !process.env.TK_CHROMIUM_EXECUTABLE}, async () => {
  const {chromium} = require(process.env.TK_PLAYWRIGHT_MODULE);
  const browser = await chromium.launch({headless:true, executablePath:process.env.TK_CHROMIUM_EXECUTABLE,args:['--no-sandbox','--disable-dev-shm-usage']});
  const evidence = process.env.TK_SHELL_EVIDENCE_DIR;
  if (evidence) fs.mkdirSync(evidence,{recursive:true});
  const results=[];
  try {
    for (const width of [1600,1280,961,960,900,760,390]) for (const theme of ['light','dark']) {
      const context=await browser.newContext({viewport:{width,height:900},colorScheme:theme,reducedMotion:'reduce'});
      const page=await context.newPage(); const errors=[];
      page.on('pageerror',e=>errors.push(String(e)));
      await page.route('**/*',r=>{throw Error('Offline page requested '+r.request().url());});
      await page.setContent(html());
      await page.evaluate(() => document.fonts.ready);
      const geometry=await page.evaluate(()=>{
        const box=s=>document.querySelector(s).getBoundingClientRect();
        const c=box('.ht-doc-content'), f=box('footer'),n=box('.ht-doc-nav'), h=box('.ht-topbar'),t=box('.ht-theme-control');
        const sizes=Object.fromEntries(['.ht-doc-content','h2','h3','.ht-lede','pre','td','dd','#ref-1','.ht-topbar-title','.ht-doc-nav'].map(s=>[s,parseFloat(getComputedStyle(document.querySelector(s)).fontSize)]));
        return {width:innerWidth,scroll:document.documentElement.scrollWidth,left:c.left,right:innerWidth-c.right,footerLeft:f.left,footerRight:innerWidth-f.right,overlap:f.left<n.right&&f.right>n.left&&f.top<n.bottom&&f.bottom>n.top,headerRight:h.right-parseFloat(getComputedStyle(document.querySelector('.ht-topbar')).paddingRight),themeRight:t.right,sizes};
      });
      assert.equal(geometry.width,width);assert.ok(geometry.scroll<=width,JSON.stringify(geometry));
      if(width>960){assert.ok(Math.abs(geometry.left-geometry.right)<=1,JSON.stringify(geometry));assert.equal(geometry.overlap,false);assert.equal(geometry.sizes['.ht-doc-nav'],13);}
      assert.equal(geometry.sizes['.ht-doc-content'],14);assert.equal(geometry.sizes.h2,19);assert.equal(geometry.sizes.h3,16);assert.equal(geometry.sizes['.ht-lede'],17);assert.equal(geometry.sizes.pre,13.5);assert.ok(geometry.sizes['#ref-1']<=14);assert.equal(geometry.sizes['.ht-topbar-title'],20);
      assert.ok(Math.abs(geometry.themeRight-geometry.headerRight)<=1,JSON.stringify(geometry));
      await page.locator('[data-ht-export-status]').evaluate(e=>{e.hidden=false;e.textContent='다운로드 자료를 준비하지 못했습니다. 원본 파일을 확인해 주세요. '.repeat(5);});
      const statusLayout=await page.evaluate(()=>{
        const b=document.querySelector('.ht-topbar'),r=b.getBoundingClientRect(),t=b.querySelector('.ht-topbar-title').getBoundingClientRect(),a=b.querySelector('.ht-document-actions').getBoundingClientRect(),c=b.querySelector('.ht-theme-control').getBoundingClientRect();
        return {titleWidth:t.width,titleRight:t.right,actionsLeft:a.left,controlRight:c.right,right:r.right-parseFloat(getComputedStyle(b).paddingRight),scroll:document.documentElement.scrollWidth};
      });
      assert.ok(statusLayout.titleWidth>0,JSON.stringify(statusLayout));
      assert.ok(Math.abs(statusLayout.controlRight-statusLayout.right)<=1,JSON.stringify(statusLayout));
      if(width>760) assert.ok(statusLayout.titleRight<=statusLayout.actionsLeft,JSON.stringify(statusLayout));
      assert.ok(statusLayout.scroll<=width,JSON.stringify(statusLayout));
      await page.locator('[data-ht-export-status]').evaluate(e=>{e.textContent='다운로드 자료를 준비하지 못했습니다. 생성한 원본 파일을 확인해 주세요.';});
      assert.deepEqual(await page.locator('pre code').allTextContents(),sources);
      const contrast=await page.evaluate(()=>{
        const rgb=s=>s.match(/[\d.]+/g).slice(0,3).map(Number);
        const lum=c=>rgb(c).map(x=>{x/=255;return x<=.04045?x/12.92:((x+.055)/1.055)**2.4;}).reduce((v,x,i)=>v+x*[.2126,.7152,.0722][i],0);
        return [...document.querySelectorAll('code span[class^="ht-code-"]:not(.ht-code-line)')].map(e=>{const a=lum(getComputedStyle(e).color),b=lum(getComputedStyle(e.closest('pre')).backgroundColor);return (Math.max(a,b)+.05)/(Math.min(a,b)+.05);});
      });
      assert.ok(contrast.length);assert.ok(Math.min(...contrast)>=4.5,Math.min(...contrast));
      const buttons=page.locator('.ht-code-toolbar button');assert.equal(await buttons.count(),3);
      if(evidence && [1280,390].includes(width)){await page.screenshot({path:path.join(evidence,`${width}-${theme}-top.png`)});}
      for(let i=0;i<3;i++){
        await buttons.nth(i).focus();await page.keyboard.press('Space');assert.equal(await buttons.nth(i).getAttribute('aria-pressed'),'true');
        const bounds=await page.locator('pre').nth(i).evaluate(e=>{
          const line=e.querySelector('.ht-code-line');
          const r=document.createRange(); r.selectNodeContents(line);
          const text=r.getClientRects()[0];
          const style=getComputedStyle(line), before=getComputedStyle(line,'::before');
          return {scroll:e.scrollWidth,width:e.clientWidth,textLeft:text?.left,numberRight:line.getBoundingClientRect().left+parseFloat(before.width)};
        });assert.ok(bounds.scroll<=bounds.width,JSON.stringify(bounds));
        if (bounds.textLeft!==undefined) assert.ok(bounds.textLeft>=bounds.numberRight,JSON.stringify(bounds));
      }
      assert.deepEqual(await page.locator('pre code').allTextContents(),sources);
      // Each toggle belongs to one block and can restore its original scrolling mode.
      await buttons.first().press('Enter');assert.equal(await buttons.first().getAttribute('aria-pressed'),'false');assert.equal(await buttons.nth(1).getAttribute('aria-pressed'),'true');
      await page.locator('a[href="#document-bottom"]').click();
      await page.locator('footer').scrollIntoViewIfNeeded();
      if(evidence && [1280,390].includes(width)){await page.screenshot({path:path.join(evidence,`${width}-${theme}-end.png`)});}
      if(width<=960){const toc=page.locator('.ht-doc-toc');await toc.locator('summary').click();assert.ok(await toc.getAttribute('open')!==null);await toc.locator('summary').press('Escape');assert.equal(await toc.getAttribute('open'),null);}
      assert.deepEqual(errors,[]);results.push({...geometry,theme,minContrast:Math.min(...contrast),codeText:'identical',wrap:'Pass'});await context.close();
    }
    for(const width of [1280,390]) for(const theme of ['light','dark']){
      const context=await browser.newContext({javaScriptEnabled:false,viewport:{width,height:900},colorScheme:theme});const page=await context.newPage();await page.setContent(html());
      assert.equal(await page.locator('.ht-code-toolbar').count(),0);assert.deepEqual(await page.locator('pre code').allTextContents(),sources);assert.ok(await page.locator('.ht-doc-toc-panel').isVisible());
      await page.locator('a[href="#document-bottom"]').press('Enter');assert.equal(await page.evaluate(()=>location.hash),'#document-bottom');
      await context.close();
    }
    // Exercise the shipped report, not just the reference example.
    for (const width of [1280,390]) for (const theme of ['light','dark']) {
      const context=await browser.newContext({viewport:{width,height:900},colorScheme:theme,reducedMotion:'reduce'});
      const page=await context.newPage();
      let report=fs.readFileSync(path.join(root,'skills/tk-research/assets/report.html'),'utf8');
      if(process.env.TK_FONT_FILE) report=report.replace('</style>',`@font-face {font-family:FixtureKorean;src:url(data:font/otf;base64,${fs.readFileSync(process.env.TK_FONT_FILE).toString('base64')})} :root {--font-family:FixtureKorean,sans-serif}</style>`);
      await page.setContent(report);await page.evaluate(()=>document.fonts.ready);
      assert.equal(await page.locator('body > footer#document-bottom').count(),1);
      await page.locator('footer').scrollIntoViewIfNeeded();
      assert.equal(await page.locator('footer').evaluate(e=>getComputedStyle(e).textAlign),'center');
      assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
      if(evidence) await page.screenshot({path:path.join(evidence,`report-${width}-${theme}-end.png`)});
      await context.close();
    }
    if(process.env.TK_SHELL_BASELINE) {
      const old=spawnSync('git',['show',`${process.env.TK_SHELL_BASELINE}:skills/tk-explain/assets/html-theme.css`],{cwd:root,encoding:'utf8'});assert.equal(old.status,0,old.stderr);
      const context=await browser.newContext({viewport:{width:1280,height:900}});const page=await context.newPage();await page.setContent(html(old.stdout));
      const margins=await page.locator('.ht-doc-content').evaluate(e=>{const r=e.getBoundingClientRect();return {left:r.left,right:innerWidth-r.right};});
      assert.ok(Math.abs(margins.left-margins.right)>1,JSON.stringify(margins));
      if(evidence) fs.writeFileSync(path.join(evidence,'baseline-rejection.json'),JSON.stringify({ref:process.env.TK_SHELL_BASELINE,margins,centeredShellCheck:'Fail as expected'},null,2));await context.close();
    }
    if(evidence) fs.writeFileSync(path.join(evidence,'measurements.json'),JSON.stringify({browser:browser.version(),headless:true,results},null,2));
  }finally{await browser.close();}
});
