/* Learner preferences are independent of course progress and its import/export schema. */
(function(root){
 'use strict';
 const KEY='tigerkit-course-player:prefs';
 const defaults=()=>({version:1,muted:true,volume:1,speed:1,captions:true,captionSize:'default',captionOpacity:.5,tocCollapsed:false});
 function parse(raw){
  try{
   const v=JSON.parse(raw),d=defaults();
   if(!v||v.version!==1||typeof v.muted!=='boolean'||typeof v.captions!=='boolean'||
      typeof v.volume!=='number'||!Number.isFinite(v.volume)||v.volume<0||v.volume>1||
      ![.75,1,1.25,1.5,2].includes(v.speed)||!['small','default','large'].includes(v.captionSize)||
      typeof v.captionOpacity!=='number'||!Number.isFinite(v.captionOpacity)||v.captionOpacity<0||v.captionOpacity>1||
      (v.tocCollapsed!==undefined&&typeof v.tocCollapsed!=='boolean'))return d;
   for(const key of Object.keys(d))if(Object.hasOwn(v,key))d[key]=v[key];return d;
  }catch(_){return defaults();}
 }
 function load(storage){try{return parse(storage().getItem(KEY));}catch(_){return defaults();}}
 function save(storage,value){try{storage().setItem(KEY,JSON.stringify(value));return true;}catch(_){return false;}}
 const api={KEY,defaults,parse,load,save};if(typeof module==='object'&&module.exports)module.exports=api;else root.CoursePreferences=api;
})(globalThis);
