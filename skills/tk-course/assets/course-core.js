/* Course-local manual progress. Reading, playback and scores do not imply mastery. */
(function(root){
 'use strict';
 function create(meta){
  const ids=meta.lessons.map(x=>x.id),revs=Object.fromEntries(meta.lessons.map(x=>[x.id,x.revision]));
  function empty(){return {version:2,course:meta.id,completed:[],revisions:{},memos:{},archived:[]};}
  function validate(v){
   if(!v||Object.getPrototypeOf(v)!==Object.prototype||Object.keys(v).sort().join(',')!=='archived,completed,course,memos,revisions,version'||v.version!==2||v.course!==meta.id||!Array.isArray(v.completed)||v.completed.length>10000||new Set(v.completed).size!==v.completed.length||!Array.isArray(v.archived)||v.archived.length>10000)throw new Error('진도 파일의 코스와 형식을 확인하세요.');
   const id=x=>typeof x==='string'&&/^[a-z0-9][a-z0-9-]{0,79}$/.test(x);
   for(const map of [v.memos,v.revisions])if(!map||Object.getPrototypeOf(map)!==Object.prototype||Object.keys(map).length>10000||Object.entries(map).some(([k,x])=>!id(k)||typeof x!=='string'||x.length>10000))throw new Error('진도 항목 형식이 올바르지 않습니다.');
   if(v.completed.some(x=>!id(x)||!Object.hasOwn(v.revisions,x))||v.archived.some(x=>!x||Object.keys(x).sort().join(',')!=='lesson,revision'||!id(x.lesson)||typeof x.revision!=='string'||x.revision.length>10000))throw new Error('완료 기록 형식이 올바르지 않습니다.');
   const next=JSON.parse(JSON.stringify(v));
   next.completed=v.completed.filter(lesson=>{
    if(Object.hasOwn(revs,lesson)&&revs[lesson]===v.revisions[lesson])return true;
    if(!next.archived.some(x=>x.lesson===lesson&&x.revision===v.revisions[lesson]))next.archived.push({lesson,revision:v.revisions[lesson]});
    return false;
   });
   return next;
  }
  function parse(text){if(typeof text!=='string'||text.length>2000000)throw new Error('진도 파일이 너무 큽니다.');return validate(JSON.parse(text));}
  function complete(state,id,checked){
   if(!ids.includes(id)||typeof checked!=='boolean')throw new Error('알 수 없는 강의입니다.');
   const next=validate(state);next.completed=ids.filter(x=>x===id?checked:next.completed.includes(x));next.revisions[id]=revs[id];return next;
  }
  function grade(answers,questions){return questions.map(q=>({id:q.id,answered:Object.hasOwn(answers,q.id),correct:answers[q.id]===q.answer,explanation:q.explanation}));}
  return {COURSE:meta.id,LESSONS:ids,empty,parse,validate,complete,grade};
 }
 const api={create};if(typeof module==='object'&&module.exports)module.exports=api;else root.CourseCore=api;
})(globalThis);
