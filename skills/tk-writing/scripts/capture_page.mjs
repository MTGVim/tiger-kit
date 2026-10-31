#!/usr/bin/env node
import {writeFile, realpath} from 'node:fs/promises';
import {pathToFileURL} from 'node:url';
import {realpathSync} from 'node:fs';
import {withPage, evaluate} from './chrome_capture.mjs';

export async function capture(input, output, width = 1440, viewportHeight) {
  if (!Number.isInteger(width) || width < 320 || width > 3840) throw new Error('Width must be 320-3840');
  if (viewportHeight !== undefined && (!Number.isInteger(viewportHeight) || viewportHeight < 1 || viewportHeight > 100000)) throw new Error('Height must be 1-100000');
  const url = pathToFileURL(await realpath(input)).href;
  await withPage(async call => {
    // A one-pixel bootstrap measures short documents without a 900px viewport floor.
    await call('Emulation.setDeviceMetricsOverride', {width, height: viewportHeight ?? 1, deviceScaleFactor: 1, mobile: false});
    const result = await call('Page.navigate', {url});
    if (result.errorText) throw new Error(result.errorText);
    await evaluate(call, `new Promise((resolve,reject)=>{const start=Date.now();const check=()=>{if(location.href===${JSON.stringify(url)}&&document.readyState==='complete')resolve();else if(Date.now()-start>15000)reject(new Error('Page load timeout'));else setTimeout(check,50)};check()})`);
    await evaluate(call, `(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(i=>i.decode()));await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))})()`);
    // Native diagrams can lay out after load/fonts; require bounded stable geometry.
    await evaluate(call, `new Promise((resolve,reject)=>{
      const start=performance.now();let previous='',stable=start;
      const check=()=>{const now=performance.now();
        const signature=JSON.stringify([document.documentElement.scrollWidth,document.documentElement.scrollHeight,
          [...document.querySelectorAll('svg,iframe,img')].map(e=>{const r=e.getBoundingClientRect();return [r.x,r.y,r.width,r.height]})]);
        if(signature!==previous){previous=signature;stable=now}
        if(now-start>=1000&&now-stable>=300){resolve();return}
        if(now-start>10000){reject(new Error('Page layout did not stabilize'));return}
        requestAnimationFrame(check)};check()})`);
    let metrics = await call('Page.getLayoutMetrics');
    if (viewportHeight === undefined) {
      let fitted = false;
      for (let attempt = 0; attempt < 4; attempt++) {
        const height = Math.ceil(metrics.cssContentSize.height);
        if (height < 1 || height > 100000) throw new Error('Page exceeds bounded capture size');
        await call('Emulation.setDeviceMetricsOverride', {width, height, deviceScaleFactor: 1, mobile: false});
        await evaluate(call, 'new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))');
        metrics = await call('Page.getLayoutMetrics');
        if (Math.ceil(metrics.cssContentSize.height) === height) { fitted = true; break; }
      }
      if (!fitted) throw new Error('Document height depends on the viewport; pass an explicit height');
    }
    const {width: w, height} = metrics.cssContentSize;
    if (w > 16384 || height > 100000) throw new Error('Page exceeds bounded capture size');
    const {data} = await call('Page.captureScreenshot', {format: 'png', captureBeyondViewport: true,
      clip: {x: 0, y: 0, width: Math.max(width, w), height, scale: 1}});
    await writeFile(output, Buffer.from(data, 'base64'), {flag: 'wx'});
  });
}
if (process.argv[1] && import.meta.url === pathToFileURL(realpathSync(process.argv[1])).href) {
  if (process.argv.length < 4 || process.argv.length > 6) { console.error('Usage: capture_page.mjs input.html new-output.png [width] [height]'); process.exitCode = 2; }
  else { try { await capture(process.argv[2], process.argv[3], Number(process.argv[4] ?? 1440), process.argv[5] === undefined ? undefined : Number(process.argv[5])); } catch (e) { console.error(e.message); process.exitCode = 1; } }
}
