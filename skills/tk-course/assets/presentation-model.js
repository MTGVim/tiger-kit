/* Derive visible teaching steps from the same cue timeline, with no extra timers. */
(function(root){
 'use strict';
 function step(indices,s,mode,completeOpening=false){
   const gap=s.status==='waiting'||(s.status==='paused'&&s.waitMs!==null);
   const speaking=['playing','loading','paused'].includes(s.status)&&!gap;
   const through=s.status==='ended'?Infinity:s.status==='idle'||s.status==='blocked'?-1:gap?s.cue-1:s.cue;
   return {visible:completeOpening||mode!=='on'||s.status==='ended'||indices.some(n=>n<=through),focused:mode!=='off'&&speaking&&indices.includes(s.cue)};
 }
 const api={step};if(typeof module==='object'&&module.exports)module.exports=api;else root.CoursePresentation=api;
})(globalThis);
