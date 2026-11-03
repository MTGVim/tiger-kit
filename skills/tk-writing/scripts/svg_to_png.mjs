#!/usr/bin/env node
import {readFile, writeFile} from 'node:fs/promises';
import {pathToFileURL} from 'node:url';
import {realpathSync} from 'node:fs';
import {withPage, evaluate} from './chrome_capture.mjs';

export async function convert(input, output) {
  const data = await readFile(input);
  const source = 'data:image/svg+xml;base64,' + data.toString('base64');
  const png = await withPage(async page => {
    await page.setContent('<!doctype html><meta http-equiv="Content-Security-Policy" content="default-src \'none\'; img-src data:; style-src \'unsafe-inline\'"><style>html,body{margin:0;background:transparent}img{display:block}</style><img alt="">');
    const size = await evaluate(page, `(async()=>{const root=new DOMParser().parseFromString(${JSON.stringify(data.toString('utf8'))},'image/svg+xml').documentElement;if(root.localName!=='svg')throw new Error('Invalid SVG');const vb=(root.getAttribute('viewBox')||'').trim().split(/[ ,]+/).map(Number);const dimension=(name,index)=>{const value=root.getAttribute(name)||'';return /^[0-9]+(?:[.][0-9]+)?(?:px)?$/.test(value)?parseFloat(value):vb.length===4?vb[index]:0};const img=document.querySelector('img');img.width=dimension('width',2);img.height=dimension('height',3);if(!img.width||!img.height)throw new Error('SVG needs dimensions or viewBox');img.src=${JSON.stringify(source)};await img.decode();return {width:img.width,height:img.height}})()`);
    if (!(size.width > 0 && size.width <= 4096 && size.height > 0 && size.height <= 16384)) throw new Error('Unsupported SVG dimensions');
    await page.setViewportSize(size);
    return await page.screenshot({type: 'png', fullPage: true, omitBackground: true, scale: 'device',
      clip: {x: 0, y: 0, ...size}});
  }, {deviceScaleFactor: 2});
  await writeFile(output, png, {flag: 'wx'});
}
if (process.argv[1] && import.meta.url === pathToFileURL(realpathSync(process.argv[1])).href) {
  if (process.argv.length !== 4) { console.error('Usage: svg_to_png.mjs input.svg new-output.png'); process.exitCode = 2; }
  else { try { await convert(...process.argv.slice(2)); } catch (e) { console.error(e.message); process.exitCode ||= 1; } }
}
