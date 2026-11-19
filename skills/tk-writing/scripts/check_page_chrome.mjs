#!/usr/bin/env node
/** Offline report browser checks using the installed Chrome capture backend. */
import {readFile, writeFile, mkdir} from 'node:fs/promises';
import {join} from 'node:path';
import {pathToFileURL} from 'node:url';
import {withPage, evaluate} from './chrome-capture.mjs';

async function main() {
  const [input, evidenceDir, widthsJson, runtimeFile] = process.argv.slice(2);
  if (!input || !evidenceDir || !widthsJson || !runtimeFile) throw Error('required arguments: html evidence widths runtime');
  const widths = JSON.parse(widthsJson);
  const runtime = await readFile(runtimeFile, 'utf8');
  const results = [];
  await mkdir(evidenceDir, {recursive: true});
  for (const width of widths) {
    await withPage(async page => {
      await page.setViewportSize({width, height: 900});
      await page.goto(pathToFileURL(input).href);
      for (const theme of ['light', 'dark']) {
        const changed = await evaluate(page, '(() => { const theme=' + JSON.stringify(theme) +
          '; const control=document.querySelector("[data-ht-theme-control] input[value=\\""+theme+"\\"]");' +
          'if(control){control.click();return document.documentElement.getAttribute("data-theme")===theme;}' +
          'document.documentElement.setAttribute("data-theme",theme);return true;})()');
        if (!changed) throw Error('theme control did not change data-theme');
        for (const ratio of [0, 0.25, 0.5, 0.75, 1]) {
          const row = await evaluate(page, '(() => {scrollTo(0,(document.documentElement.scrollHeight-innerHeight)*' + ratio +
            '); return (' + runtime + ')();})()');
          row.theme = theme;
          row.ratio = ratio;
          row.page_errors = [];
          if ([0, 0.5, 1].includes(ratio) && [375, 1440].includes(width)) {
            const name = 'chrome-pipe-' + width + '-' + theme + '-' + ratio + '.png';
            const png = await page.screenshot({clip: {x: 0, y: 0, width, height: 900}});
            await writeFile(join(evidenceDir, name), png, {flag: 'wx'});
            row.screenshot = name;
          }
          results.push(row);
        }
      }
    }, {viewport: {width, height: 900}});
  }
  process.stdout.write(JSON.stringify({views: results, blocked_network: [],
    visual_inspection: 'not performed by this script',
    delivery_transport: 'Chrome pipe local file navigation; network blocked by proxy and Chrome settings; file:// behavior tested'}));
}
main().catch(error => { console.error(error.stack || error.message); process.exitCode = 2; });
