/* Preview without mutating the active lesson; commit a drag exactly once. */
(function(root){
 'use strict';
 const running=s=>['playing','loading','waiting'].includes(s.status);
 function position(fraction,width,cardWidth){const margin=8,half=Math.min(cardWidth,width-2*margin)/2;return Math.max(half+margin,Math.min(width-half-margin,fraction*width));}
 function slidePoint(slides,value){
  const total=slides.reduce((n,s)=>n+s.narration.length,0);let rest=Math.max(0,Math.min(total-.000001,Number(value)||0));
  for(let slide=0;slide<slides.length;slide++){if(rest<slides[slide].narration.length)return {slide,cue:Math.floor(rest)};rest-=slides[slide].narration.length;}
 }
 function create({transport,onPreview=()=>{},onClose=()=>{},onDragging=()=>{},intervalMs=120,clock={setTimeout:(f,t)=>setTimeout(f,t),clearTimeout:id=>clearTimeout(id)}}){
  let session=null,timer=null,pending=null,epoch=0;
  function reset(){epoch++;if(timer!==null)clock.clearTimeout(timer);timer=null;pending=null;onClose();}
  function begin(){if(session)return;const owner=transport(),s=owner.snapshot();session={owner,start:s.progress.value,resume:running(s)};onDragging(true);owner.pause();}
  function preview(value){
   const owner=session?session.owner:transport(),s=owner.snapshot(),total=s.progress.total;
   if(!Number.isFinite(Number(value))||!Number.isFinite(total)||total<=0)return;
   const v=Math.max(0,Math.min(total,Number(value)));pending={owner,value:v,total,fraction:v/total};
   if(timer===null){const token=epoch;timer=clock.setTimeout(()=>{timer=null;if(token!==epoch||!pending)return;const latest=pending;pending=null;onPreview(latest);},intervalMs);}
  }
  function commit(value){
   if(!session)return false;const saved=session;session=null;reset();onDragging(false);
   const total=saved.owner.snapshot().progress.total,n=Number(value),target=Number.isFinite(n)?Math.max(0,Math.min(total,n)):saved.start;
   if(Math.abs(target-saved.start)>.00001)saved.owner.seekProgress(target);
   if(saved.resume&&target<total)saved.owner.play();return true;
  }
  function cancel(resume=true){const saved=session;session=null;reset();onDragging(false);if(saved&&saved.resume&&resume)saved.owner.play();}
  function hide(){if(!session)reset();}
  return {begin,preview,commit,cancel,hide,isDragging:()=>!!session};
 }
 function createVideo({video,onPending=()=>{},onFrame=()=>{},onError=()=>{}}){
  let source='',latest=null,busy=null,active=false,epoch=0;
  video.muted=true;video.volume=0;video.controls=false;
  function target(time){return Math.max(0,Number.isFinite(video.duration)?Math.min(time,Math.max(0,video.duration-.001)):time);}
  function pump(){
   if(!active||!latest||busy||video.readyState<1)return;
   const wanted={...latest,time:target(latest.time)};busy=wanted;
   if(video.readyState>=2&&!video.seeking&&Math.abs((Number(video.currentTime)||0)-wanted.time)<.01){settled();return;}
   try{video.currentTime=wanted.time;}catch(_){busy=null;onError();}
  }
  function settled(){
   if(!active||!busy||video.seeking||video.readyState<2||Math.abs(video.currentTime-busy.time)>.25)return;
   const done=busy;busy=null;
   if(latest&&done.token===latest.token){onFrame({time:video.currentTime,requested:latest.time});return;}
   pump();
  }
  video.addEventListener('loadedmetadata',pump);video.addEventListener('loadeddata',()=>{if(busy)settled();else pump();});
  video.addEventListener('seeked',settled);
  video.addEventListener('error',()=>{if(active){busy=null;onError();}});
  function request(src,time){
   active=true;latest={time:Math.max(0,Number(time)||0),token:++epoch};onPending();
   if(source!==src){source=src;busy=null;video.pause();video.src=src;video.load();return;}
   pump();
  }
  function close(){active=false;latest=null;busy=null;epoch++;video.pause();}
  return {request,close};
 }
 const api={create,createVideo,position,slidePoint};if(typeof module==='object'&&module.exports)module.exports=api;else root.CourseSeekPreview=api;
})(globalThis);
