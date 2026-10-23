const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),{pathToFileURL}=require('node:url');
const ready=!!(process.env.TK_PLAYWRIGHT_MODULE&&process.env.TK_CHROMIUM_EXECUTABLE&&process.env.TK_FIGURE_PAGE);
test('SVG figures stay readable in portrait, preserve original data, and follow semantic cues',{skip:!ready,timeout:240000},async()=>{
 const {chromium}=require(process.env.TK_PLAYWRIGHT_MODULE),browser=await chromium.launch({env:{...process.env,...(process.env.TK_BROWSER_FONTCONFIG?{FONTCONFIG_FILE:process.env.TK_BROWSER_FONTCONFIG}:{})},headless:true,executablePath:process.env.TK_CHROMIUM_EXECUTABLE,args:['--no-sandbox','--disable-dev-shm-usage','--enable-automation']});
 const evidence=process.env.TK_FIGURE_SCREENSHOTS,metrics=[],errors=[];
 if(evidence)fs.mkdirSync(evidence,{recursive:true});
 const capture=async(page,name)=>{if(evidence){fs.mkdirSync(evidence,{recursive:true});await page.screenshot({path:path.join(evidence,name+'.png'),fullPage:true});}};
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
     const detail={viewportWidth:width,colorScheme,slide:slides[n].id,...geometry};metrics.push(detail);
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
