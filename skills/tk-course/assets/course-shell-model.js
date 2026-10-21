(function(root){
  'use strict';
  function route(hash,published=['slides','video']){const id=hash==='#lesson-slides'?'slides':hash==='#lesson-video'?'video':'home';return published.includes(id)?id:'home';}
  function position(text,slides){
    try{
      const p=JSON.parse(text);
      if(!p || Object.keys(p).sort().join(',')!=='cue,lesson,slide,videoTime' || !['slides','video'].includes(p.lesson) ||
        !Number.isInteger(p.slide) || p.slide<0 || p.slide>=slides.length ||
        !Number.isInteger(p.cue) || p.cue<0 || p.cue>=slides[p.slide].narration.length ||
        !Number.isFinite(p.videoTime) || p.videoTime<0 || p.videoTime>86400)return null;
      return {lesson:p.lesson,slide:p.slide,cue:p.cue,videoTime:p.videoTime};
    }catch(_){return null;}
  }
  const api={route,position};
  if(typeof module==='object' && module.exports)module.exports=api;else root.CourseShellModel=api;
})(globalThis);
