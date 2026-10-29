#!/usr/bin/env node
import {writeFile, realpath} from 'node:fs/promises';
import {pathToFileURL} from 'node:url';
import {realpathSync} from 'node:fs';
import {withPage, evaluate} from './chrome_capture.mjs';

export async function capture(input, output, width = 1440) {
  if (!Number.isInteger(width) || width < 320 || width > 3840) throw new Error('Width must be 320-3840');
  const url = pathToFileURL(await realpath(input)).href;
  await withPage(async call => {
    await call('Emulation.setDeviceMetricsOverride', {width, height: 900, deviceScaleFactor: 1, mobile: false});
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
    const metrics = await call('Page.getLayoutMetrics');
    const {width: w, height} = metrics.cssContentSize;
    if (w > 16384 || height > 100000) throw new Error('Page exceeds bounded capture size');
    const {data} = await call('Page.captureScreenshot', {format: 'png', captureBeyondViewport: true,
      clip: {x: 0, y: 0, width: Math.max(width, w), height, scale: 1}});
    await writeFile(output, Buffer.from(data, 'base64'), {flag: 'wx'});
  });
}
if (process.argv[1] && import.meta.url === pathToFileURL(realpathSync(process.argv[1])).href) {
  if (process.argv.length < 4 || process.argv.length > 5) { console.error('Usage: capture_page.mjs input.html new-output.png [width]'); process.exitCode = 2; }
  else { try { await capture(process.argv[2], process.argv[3], Number(process.argv[4] || 1440)); } catch (e) { console.error(e.message); process.exitCode = 1; } }
}
