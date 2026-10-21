/* Local SVG controls; visible glyphs never replace accessible action names. */
(function(root){
 'use strict';
 const paths={
  play:'<path d="m9 5 11 7-11 7z" fill="currentColor" stroke="none"/>',
  pause:'<path d="M7 5h4v14H7zM15 5h4v14h-4z" fill="currentColor" stroke="none"/>',
  replay:'<path d="M4 9a8 8 0 1 1 0 6M4 4v5h5"/>',
  prev:'<path d="M6 5v14M19 5 9 12l10 7z"/>',
  next:'<path d="M18 5v14M5 5l10 7L5 19z"/>',
  captions:'<rect x="2" y="4" width="20" height="16" rx="3"/><path d="M10 9a3 3 0 1 0 0 6m10-6a3 3 0 1 0 0 6" transform="translate(-2 0)"/>',
  speed:'<path d="M4 18a9 9 0 1 1 16 0M12 14l5-7M7 8l1 1m-4 5h2m12 0h2"/><circle cx="12" cy="14" r="1.5" fill="currentColor"/>',
  settings:'<path d="M21.00 12.00 20.83 13.76 18.93 14.87 18.24 16.17 18.36 18.36 17.00 19.48 14.87 18.93 13.46 19.36 12.00 21.00 10.24 20.83 9.13 18.93 7.83 18.24 5.64 18.36 4.52 17.00 5.07 14.87 4.64 13.46 3.00 12.00 3.17 10.24 5.07 9.13 5.76 7.83 5.64 5.64 7.00 4.52 9.13 5.07 10.54 4.64 12.00 3.00 13.76 3.17 14.87 5.07 16.17 5.76 18.36 5.64 19.48 7.00 18.93 9.13 19.36 10.54Z"/><circle cx="12" cy="12" r="3"/>',
  transcript:'<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M14 3v18M6 8h5m-5 4h5m-5 4h4"/>',
  fullscreen:'<path d="M9 3H3v6m12-6h6v6M3 15v6h6m12-6v6h-6"/>',
  restore:'<path d="M3 9h6V3m6 0v6h6M9 21v-6H3m12 6v-6h6"/>',
  close:'<path d="m6 6 12 12M18 6 6 18"/>'
  ,volume:'<path d="M3 9h4l5-4v14l-5-4H3zM16 8a6 6 0 0 1 0 8m3-11a10 10 0 0 1 0 14"/>'
  ,'volume-off':'<path d="M3 9h4l5-4v14l-5-4H3zM16 9l6 6m0-6-6 6"/>'
  ,'caption-size':'<path d="M3 19 9 5l6 14M5 14h8m3 5 3-8 3 8m-5-3h4"/>'
 };
 const renderedIcons=new WeakMap();
 function svg(name){return '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" pointer-events="none" aria-hidden="true" focusable="false">'+paths[name]+'</svg>';}
 function icon(button,name,label){if(renderedIcons.get(button)!==name||!button.firstElementChild){button.innerHTML=svg(name);renderedIcons.set(button,name);}if(label){button.setAttribute('aria-label',label);button.title=label;}}
 function eventInside(event,node){const path=typeof event.composedPath==='function'?event.composedPath():[];return path.includes(node)||node===event.target||node.contains(event.target);}
 function dismissOutside(event,popovers){for(const {panel,trigger,close} of popovers)if(!panel.hidden&&!eventInside(event,panel)&&!eventInside(event,trigger))close();}
 function caption({enabled,status,cue,gap=false,previous=''}){
  // A breathing gap keeps the sentence just heard, never the upcoming one.
  const text=(status==='waiting'||gap)?previous:cue;
  return {hidden:!enabled||!text||!['playing','loading','waiting','paused','ended'].includes(status),text:text||''};
 }
 function timeLabel(time,total){const stamp=n=>Math.floor(Math.max(0,n)/60)+':'+String(Math.floor(Math.max(0,n)%60)).padStart(2,'0');return stamp(time)+' / '+stamp(total);}
 function progressLabel(data,lesson,index){
  if(lesson==='video'){const n=data.video_scenes.length,i=Math.max(0,Math.min(n-1,Math.floor(index)));return {label:`영상 · 장면 ${i+1} / ${n}`,slide:i,cue:0};}
  const total=data.slides.reduce((n,s)=>n+s.narration.length,0);let rest=Math.max(0,Math.min(total-1,Math.floor(index)));
  for(let slide=0;slide<data.slides.length;slide++){
   const cues=data.slides[slide].narration.length;
   if(rest<cues)return {label:`슬라이드 ${slide+1} / ${data.slides.length} · 설명 ${rest+1} / ${cues}`,slide,cue:rest};rest-=cues;
  }
 }
 const api={svg,icon,eventInside,dismissOutside,caption,timeLabel,progressLabel};if(typeof module==='object'&&module.exports)module.exports=api;else root.CourseControls=api;
})(globalThis);
