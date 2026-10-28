#!/usr/bin/env node
import {readFile, writeFile} from 'node:fs/promises';
import {pathToFileURL} from 'node:url';
import {withPage, evaluate} from './chrome_capture.mjs';

export async function convert(input, output) {
  const data = await readFile(input);
  const source = 'data:image/svg+xml;base64,' + data.toString('base64');
  await withPage(async call => {
    await call('Page.setDocumentContent', {frameId: (await call('Page.getFrameTree')).frameTree.frame.id,
      html: '<!doctype html><meta http-equiv="Content-Security-Policy" content="default-src \'none\'; img-src data:; style-src \'unsafe-inline\'"><style>html,body{margin:0;background:transparent}img{display:block}</style><img alt="">'});
    const size = await evaluate(call, `(async()=>{const root=new DOMParser().parseFromString(${JSON.stringify(data.toString('utf8'))},'image/svg+xml').documentElement;if(root.localName!=='svg')throw new Error('Invalid SVG');const vb=(root.getAttribute('viewBox')||'').trim().split(/[ ,]+/).map(Number);const dimension=(name,index)=>{const value=root.getAttribute(name)||'';return /^[0-9]+(?:[.][0-9]+)?(?:px)?$/.test(value)?parseFloat(value):vb.length===4?vb[index]:0};const img=document.querySelector('img');img.width=dimension('width',2);img.height=dimension('height',3);if(!img.width||!img.height)throw new Error('SVG needs dimensions or viewBox');img.src=${JSON.stringify(source)};await img.decode();return {width:img.width,height:img.height}})()`);
    if (!(size.width > 0 && size.width <= 4096 && size.height > 0 && size.height <= 16384)) throw new Error('Unsupported SVG dimensions');
    await call('Emulation.setDeviceMetricsOverride', {...size, deviceScaleFactor: 2, mobile: false});
    await call('Emulation.setDefaultBackgroundColorOverride', {color: {r: 0, g: 0, b: 0, a: 0}});
    const {data: png} = await call('Page.captureScreenshot', {format: 'png', captureBeyondViewport: true,
      clip: {x: 0, y: 0, ...size, scale: 1}});
    await writeFile(output, Buffer.from(png, 'base64'), {flag: 'wx'});
  });
}
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  if (process.argv.length !== 4) { console.error('Usage: svg_to_png.mjs input.svg new-output.png'); process.exitCode = 2; }
  else { try { await convert(...process.argv.slice(2)); } catch (e) { console.error(e.message); process.exitCode = 1; } }
}
