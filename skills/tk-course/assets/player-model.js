(function(root) {
  'use strict';
  function initial() { return { lesson: 'slides', slide: 0 }; }
  function select(state, lesson, count) {
    if (!['slides','video'].includes(lesson) || !Number.isInteger(count) || count < 1) throw new Error('Invalid lesson');
    return { lesson, slide: lesson === state.lesson ? Math.max(0,Math.min(count-1,state.slide)) : 0 };
  }
  function step(state, offset, count) {
    if (state.lesson !== 'slides') return {...state};
    if (!Number.isInteger(offset) || !Number.isInteger(count) || count < 1) throw new Error('Invalid step');
    return { lesson: 'slides', slide: Math.max(0,Math.min(count-1,state.slide+offset)) };
  }
  function visible(state, count) {
    if (!['slides','video'].includes(state.lesson) || !Number.isInteger(state.slide) || state.slide < 0 || state.slide >= count) throw new Error('Invalid view');
    return { slide: state.lesson === 'slides' ? state.slide : null, video: state.lesson === 'video' };
  }
  const api={initial,select,step,visible};
  if(typeof module !== 'undefined' && module.exports) module.exports=api; else root.PlayerModel=api;
})(globalThis);
