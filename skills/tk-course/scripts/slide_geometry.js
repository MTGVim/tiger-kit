/* Evaluate in a real browser with the active SVG. This is a validation helper,
   not a runtime dependency. Pixel inspection remains necessary for raster labels. */
(svg) => {
  const frame=svg.closest('#media-viewport'),vb=svg.viewBox.baseVal;
  const bounds=svg.getBoundingClientRect(),box=frame.getBoundingClientRect();
  const logicalBounds=e=>{const r=e.getBBox(),m=svg.getScreenCTM().inverse().multiply(e.getScreenCTM()),points=[[r.x,r.y],[r.x+r.width,r.y],[r.x,r.y+r.height],[r.x+r.width,r.y+r.height]].map(([x,y])=>new DOMPoint(x,y).matrixTransform(m)),xs=points.map(p=>p.x),ys=points.map(p=>p.y);return {x:Math.min(...xs),y:Math.min(...ys),width:Math.max(...xs)-Math.min(...xs),height:Math.max(...ys)-Math.min(...ys)};};
  const inside=r=>r.x>=-.5&&r.y>=-.5&&r.x+r.width<=vb.width+.5&&r.y+r.height<=vb.height+.5;
  const items=[...svg.querySelectorAll('text,image,rect,path,circle,line,polyline,polygon')].filter(e=>!e.closest('defs,clipPath'));
  const outside=items.filter(e=>!inside(logicalBounds(e))).map(e=>({tag:e.tagName,text:e.textContent}));
  const unreadable=[...svg.querySelectorAll('text')].filter(e=>e.textContent.trim()&&!e.closest('[data-slide-metadata]')).map(e=>({text:e.textContent,pixels:parseFloat(getComputedStyle(e).fontSize)*Math.min(Math.hypot(e.getScreenCTM().a,e.getScreenCTM().b),Math.hypot(e.getScreenCTM().c,e.getScreenCTM().d))})).filter(e=>e.pixels<11);
  const texts=[...svg.querySelectorAll('text')].filter(e=>e.textContent.trim()),overlaps=[];
  for(let i=0;i<texts.length;i++)for(let j=i+1;j<texts.length;j++){const a=logicalBounds(texts[i]),b=logicalBounds(texts[j]);if(Math.min(a.x+a.width,b.x+b.width)-Math.max(a.x,b.x)>1&&Math.min(a.y+a.height,b.y+b.height)-Math.max(a.y,b.y)>3)overlaps.push([texts[i].textContent,texts[j].textContent]);}
  const concealed=texts.filter(e=>!e.closest('[data-slide-metadata]')).filter(e=>{for(let p=e;p&&p!==svg.parentElement;p=p.parentElement){const s=getComputedStyle(p);if(s.display==='none'||s.visibility==='hidden'||Number(s.opacity)===0)return true;}return false;}).map(e=>e.textContent);
  const imageOK=[...svg.querySelectorAll('image')].every(e=>{const m=e.getScreenCTM();return e.preserveAspectRatio.baseVal.align!==1&&Math.abs(Math.hypot(m.a,m.b)-Math.hypot(m.c,m.d))<.001;});
  const ratioOK=Math.abs(vb.width/vb.height-16/9)<1e-6;
  const frameOK=Math.abs(box.height-box.width*9/16)<=1;
  const scrollOK=frame.scrollHeight<=frame.clientHeight+1&&frame.scrollWidth<=frame.clientWidth+1;
  const contained=bounds.left>=box.left-1&&bounds.top>=box.top-1&&bounds.right<=box.right+1&&bounds.bottom<=box.bottom+1;
  return {ok:imageOK&&ratioOK&&frameOK&&scrollOK&&contained&&!outside.length&&!unreadable.length&&!overlaps.length&&!concealed.length,imageOK,ratioOK,frameOK,scrollOK,contained,outside,unreadable,overlaps,concealed,frame:{width:box.width,height:box.height},logical:{width:vb.width,height:vb.height}};
}
