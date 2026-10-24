const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),{pathToFileURL}=require('node:url');
const ready=!!(process.env.TK_PLAYWRIGHT_MODULE&&process.env.TK_CHROMIUM_EXECUTABLE&&process.env.TK_FIGURE_PAGE);
test('fixed slide frames reject geometry overrides and unreadable density, preserve data and cues',{skip:!ready,timeout:240000},async()=>{
 const {chromium}=require(process.env.TK_PLAYWRIGHT_MODULE),browser=await chromium.launch({env:{...process.env,...(process.env.TK_BROWSER_FONTCONFIG?{FONTCONFIG_FILE:process.env.TK_BROWSER_FONTCONFIG}:{})},headless:true,executablePath:process.env.TK_CHROMIUM_EXECUTABLE,args:['--no-sandbox','--disable-dev-shm-usage','--enable-automation']});
 const audit=fs.readFileSync(path.resolve(__dirname,'../../../skills/tk-course/scripts/slide_geometry.js'),'utf8');
 const inspect=svg=>svg.evaluate((node,code)=>(0,eval)(code)(node),audit);
 const evidence=process.env.TK_FIGURE_SCREENSHOTS,metrics=[],errors=[];
 if(evidence)fs.mkdirSync(evidence,{recursive:true});
 const capture=async(page,name)=>{if(evidence){fs.mkdirSync(evidence,{recursive:true});await page.frameLocator('#course-frame').locator('#media-viewport').screenshot({path:path.join(evidence,name+'.png')});}};
 try{
  for(const width of [1440,1024,390])for(const colorScheme of ['light','dark']){
   const context=await browser.newContext({viewport:{width,height:1000},colorScheme});try{
    const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));await page.goto(pathToFileURL(process.env.TK_FIGURE_PAGE).href);
    const f=page.frameLocator('#course-frame');await f.locator('#home-start').click();await f.locator('#player-page').waitFor({state:'visible'});await f.locator('#slide-wrap').focus();
    if(await f.locator('#play').getAttribute('aria-label')==='일시정지')await page.keyboard.press('k');
    await f.locator('#sound-toast').waitFor({state:'hidden'});
    await f.locator('#settings-toggle').click();
    for(const id of ['slide-pause','sentence-pause']){await f.locator('#'+id).fill('0');await f.locator('#'+id).press('Tab');}
    await f.locator('#silent-hold').fill('15');await f.locator('#silent-hold').press('Tab');await f.locator('#settings-toggle').click();
    await f.locator('#tab-transcript').click();
    const slides=await f.locator('#lesson-data').evaluate(e=>JSON.parse(e.textContent).slides);
    for(let n=0;n<slides.length;n++){
     await f.locator('[data-thumb="'+n+'"]').click();
     // Clicking a transcript sentence is the actual cue-seek control, even when paused.
     await f.locator('#tx-copy .tx-cue').first().click();await f.locator('#slide-wrap').focus();await page.keyboard.press('k');
     const slide=f.locator('.lesson-slide[data-slide="'+n+'"]'),svg=slide.locator('svg:visible');await svg.waitFor({state:'visible'});
     await f.locator('body').evaluate(()=>document.fonts.ready);
     const geometry=await svg.evaluate(svg=>{
      const vb=svg.viewBox.baseVal,items=[...svg.querySelectorAll('text')].filter(e=>e.textContent.trim()).map(e=>{const r=e.getBBox();return {text:e.textContent,x:r.x,y:r.y,w:r.width,h:r.height};});
      const clipped=items.filter(r=>r.x<-.5||r.y<-.5||r.x+r.w>vb.width+.5||r.y+r.h>vb.height+.5);
      const overlaps=[];for(let i=0;i<items.length;i++)for(let j=i+1;j<items.length;j++){const a=items[i],b=items[j];if(Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x)>1&&Math.min(a.y+a.h,b.y+b.h)-Math.max(a.y,b.y)>3)overlaps.push([a.text,b.text]);}
      return {clipped,overlaps,width:vb.width,viewport:svg.getBoundingClientRect().width,groups:[...svg.querySelectorAll('[data-focus-key]')].map(g=>({key:g.dataset.focusKey,opacity:getComputedStyle(g).opacity,visibility:getComputedStyle(g).visibility}))};
     });
     const auditResult=await inspect(svg);
     const detail={viewportWidth:width,colorScheme,slide:slides[n].id,...geometry,audit:auditResult};metrics.push(detail);
     assert(auditResult.ratioOK&&auditResult.frameOK&&auditResult.scrollOK&&auditResult.contained,JSON.stringify(detail));
     assert.deepEqual(auditResult.outside,[],JSON.stringify(detail));
     // Rich numeric/code fixtures exercise exact data bounds, not acceptance at any scale.
     // Their small labels MUST be rejected at narrow width, even with no clipping.
     if(width===390&&slides[n].type==='code'){assert(auditResult.unreadable.length>0);assert.equal(auditResult.ok,false);}
     if(width===390&&slides[n].type==='image'){assert.deepEqual(auditResult.unreadable,[],JSON.stringify(detail));assert(auditResult.ok);}

     assert.deepEqual(geometry.clipped,[],JSON.stringify(detail));assert.deepEqual(geometry.overlaps,[],JSON.stringify(detail));assert(geometry.groups.every(g=>g.visibility!=='hidden'&&Number(g.opacity)>0));
     assert(await f.locator('body').evaluate(e=>e.scrollWidth<=innerWidth));
     if(!slides[n].narration[0].focus.length)assert(geometry.groups.every(g=>Number(g.opacity)===1));
     const caption=await f.locator('#live-caption').boundingBox(),viewport=await f.locator('#media-viewport').boundingBox();assert(caption&&caption.y>=viewport.y+viewport.height-1,'captions must stay below the figure');
     if(width===390||width===1440&&['line','output','cover'].includes(slides[n].type))await capture(page,width+'-'+colorScheme+'-'+slides[n].id);
     // Cover every narrated data reference with a real transcript interaction.
     for(let c=0;c<slides[n].narration.length&&(width===390||width===1440&&colorScheme==='light');c++){
      await f.locator('#tx-copy .tx-cue').nth(c).click();await f.locator('#slide-wrap').focus();await page.keyboard.press('k');
      const wanted=slides[n].narration[c].focus;
      if(wanted.length){const highlighted=await svg.locator('[data-focused="true"]').evaluateAll(gs=>gs.map(g=>g.dataset.focusKey));assert(wanted.every(key=>highlighted.includes(key)),JSON.stringify({n,c,wanted,highlighted}));}
     }
    }
    if(colorScheme==='light'&&[1440,390].includes(width)){
     // Reproduce a consumer's postprocessing override; frame-fit must fail.
     let active=f.locator('.lesson-slide:not([hidden]) svg:visible');
     await f.locator('#media-viewport').evaluate(e=>{e.style.aspectRatio='auto';e.style.height='900px';});
     assert.equal((await inspect(active)).frameOK,false);
     await f.locator('#media-viewport').evaluate(e=>{e.style.removeProperty('aspect-ratio');e.style.removeProperty('height');});
     assert((await inspect(active)).frameOK);
     // Navigation/transcript and fullscreen never change media aspect.
     for(const transcript of [false,true]){
      if((await f.locator('#transcript-toggle').getAttribute('aria-expanded')==='true')!==transcript)await f.locator('#transcript-toggle').click();
      for(const toc of [false,true]){
       if((await f.locator('#menu-toggle').getAttribute('aria-expanded')==='true')!==toc)await f.locator('#menu-toggle').click();
       assert((await inspect(active)).frameOK);
      }
      if(width===390&&await f.locator('#toc').evaluate(e=>e.classList.contains('open')))await f.locator('#toc-close').click();
      await f.locator('#fullscreen').click();
      await page.waitForTimeout(80);
      assert(await f.locator('body').evaluate(()=>!!document.fullscreenElement),'native fullscreen was not exercised');
      let report=await inspect(active);assert(report.frameOK&&report.contained,JSON.stringify(report));
      const toolbar=await f.locator('#controls').boundingBox();assert(toolbar.y>=0&&toolbar.y+toolbar.height<=1001);
      await f.locator('#fullscreen').click();
      // Explicitly reject the request to exercise the supported in-window fallback.
      await f.locator('#stage').evaluate(e=>{e.requestFullscreen=()=>Promise.reject(new Error('test fullscreen rejection'));});
      await f.locator('#fullscreen').click();await page.waitForTimeout(80);
      assert(await f.locator('#stage').evaluate(e=>e.classList.contains('stage-expanded')));
      report=await inspect(active);assert(report.frameOK&&report.contained,JSON.stringify(report));
      await f.locator('#fullscreen').click();
      await f.locator('#stage').evaluate(e=>{delete e.requestFullscreen;});
     }
     // Notes retain real document scrolling; metadata link opens full rights/source.
     await f.locator('[data-thumb="'+slides.findIndex(s=>s.type==='image')+'"]').click();
     const image=active.locator('image');
     await image.evaluate(e=>e.setAttribute('preserveAspectRatio','none'));assert.equal((await inspect(active)).imageOK,false);
     await image.evaluate(e=>e.setAttribute('preserveAspectRatio','xMidYMid meet'));
     await active.evaluate(e=>{const p=document.createElementNS('http://www.w3.org/2000/svg','path');p.id='out-of-bounds-fixture';p.setAttribute('d','M-100 50L100 50');e.append(p);});
     assert((await inspect(active)).outside.some(e=>e.tag==='path'));
     await active.locator('#out-of-bounds-fixture').evaluate(e=>e.remove());
     await f.locator('.lesson-slide:not([hidden]) svg:visible [data-figure-note]').click();
     assert(await f.locator('.figure-values[open]').innerText().then(t=>t.includes('redistribution permitted')));
     assert(await f.locator('.player-column').evaluate(e=>e.scrollHeight>e.clientHeight));
     assert((await inspect(active)).scrollOK);
    }
    // The native setting controls still provide complete all/show and highlight-only states.
    await f.locator('[data-thumb="1"]').click();await f.locator('#settings-toggle').click();await f.locator('#motion-mode').selectOption('off');
    assert.equal(await f.locator('.lesson-slide[data-slide="1"] svg[data-follow-cue]').count(),0);
    await f.locator('#motion-mode').selectOption('highlight');assert.equal(await f.locator('.lesson-slide[data-slide="1"] svg[data-progressive]').count(),0);
    await f.locator('#settings-toggle').click();await f.locator('#tab-notes').click();assert(await f.locator('.figure-values table').count()>=3);
   }finally{await context.close();}
  }
  assert.deepEqual(errors,[]);
 }finally{await browser.close();if(evidence)fs.writeFileSync(path.join(evidence,'geometry.json'),JSON.stringify(metrics,null,2));}
});
