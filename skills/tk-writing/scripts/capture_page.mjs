#!/usr/bin/env node
import {writeFile, realpath} from 'node:fs/promises';
import {pathToFileURL} from 'node:url';
import {realpathSync, existsSync} from 'node:fs';
import {withPage, evaluate} from './chrome_capture.mjs';

export async function capture(input, output, width = 1440, viewportHeight) {
  if (!Number.isInteger(width) || width < 320 || width > 3840) throw new Error('Width must be 320-3840');
  if (viewportHeight !== undefined && (!Number.isInteger(viewportHeight) || viewportHeight < 1 || viewportHeight > 100000)) throw new Error('Height must be 1-100000');
  if (existsSync(output)) {
    // Fail before launching Chrome; a stale PNG left in place is easy to review by mistake.
    const m = output.match(/^(.*?)(?:-(\d+))?(\.png)$/i);
    let n = m && m[2] ? Number(m[2]) + 1 : 2, next;
    do { next = m ? `${m[1]}-${n++}${m[3]}` : `${output}-${n++}`; } while (existsSync(next));
    throw new Error(`Output exists and is never overwritten: ${output}\nRe-capture to a new name, e.g. ${next}, and review that file.`);
  }
  const url = pathToFileURL(await realpath(input)).href;
  const png = await withPage(async page => {
    await page.goto(url, {waitUntil: 'load'});
    await evaluate(page, `(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(i=>i.decode()));await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))})()`);
    // Native diagrams can lay out after load/fonts; require bounded stable geometry.
    await evaluate(page, `new Promise((resolve,reject)=>{
      const start=performance.now();let previous='',stable=start;
      const check=()=>{const now=performance.now();
        const signature=JSON.stringify([document.documentElement.scrollWidth,document.documentElement.scrollHeight,
          [...document.querySelectorAll('svg,iframe,img')].map(e=>{const r=e.getBoundingClientRect();return [r.x,r.y,r.width,r.height]})]);
        if(signature!==previous){previous=signature;stable=now}
        if(now-start>=1000&&now-stable>=300){resolve();return}
        if(now-start>10000){reject(new Error('Page layout did not stabilize'));return}
        requestAnimationFrame(check)};check()})`);
    const metrics = () => evaluate(page, `({width:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight})`);
    let size = await metrics();
    if (viewportHeight === undefined) {
      let fitted = false;
      for (let attempt = 0; attempt < 4; attempt++) {
        const height = Math.ceil(size.height);
        if (height < 1 || height > 100000) throw new Error('Page exceeds bounded capture size');
        await page.setViewportSize({width, height});
        await evaluate(page, 'new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))');
        size = await metrics();
        if (Math.ceil(size.height) === height) { fitted = true; break; }
      }
      if (!fitted) throw new Error('Document height depends on the viewport; pass an explicit height');
    }
    const {width: w, height} = size;
    if (w > 16384 || height > 100000) throw new Error('Page exceeds bounded capture size');
    // Explicit height controls layout, not cropping: retain the entire document.
    const clip = {x: 0, y: 0, width: Math.max(width, w), height};
    return await page.screenshot({type: 'png', fullPage: true, scale: 'css', clip});
  }, {viewport: {width, height: viewportHeight ?? 1}});
  await writeFile(output, png, {flag: 'wx'});
}
if (process.argv[1] && import.meta.url === pathToFileURL(realpathSync(process.argv[1])).href) {
  if (process.argv.length < 4 || process.argv.length > 6) { console.error('Usage: capture_page.mjs input.html new-output.png [width] [height]'); process.exitCode = 2; }
  else { try { await capture(process.argv[2], process.argv[3], Number(process.argv[4] ?? 1440), process.argv[5] === undefined ? undefined : Number(process.argv[5])); } catch (e) { console.error(e.message); process.exitCode ||= 1; } }
}
