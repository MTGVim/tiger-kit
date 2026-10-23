const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const R=path.resolve(__dirname,'../skills/tk-course/assets'),Core=require(path.join(R,'course-core.js'));
const meta={id:'sample',lessons:[{id:'first',revision:'1'},{id:'second',revision:'1'}]};
test('manual completion survives rename/reorder and preserves notes',()=>{const c=Core.create(meta),s=c.complete(c.empty(),'first',true);s.memos.first='나의 근거';const reordered=Core.create({...meta,lessons:[...meta.lessons].reverse()});const next=reordered.parse(JSON.stringify(s));assert.deepEqual(next.completed,['first']);assert.equal(next.memos.first,'나의 근거');assert.deepEqual(s.archived,[]);});
test('changed and deleted lessons archive completions while preserving notes',()=>{const c=Core.create(meta);let s=c.complete(c.empty(),'first',true);s=c.complete(s,'second',true);s.memos.second='삭제 전 메모';const changed=Core.create({id:'sample',lessons:[{id:'first',revision:'2'}]});const next=changed.parse(JSON.stringify(s));assert.deepEqual(next.completed,[]);assert.deepEqual(next.archived,[{lesson:'first',revision:'1'},{lesson:'second',revision:'1'}]);assert.equal(next.memos.second,'삭제 전 메모');const done=changed.complete(next,'first',true);assert.deepEqual(done.completed,['first']);assert.equal(done.revisions.first,'2');assert.equal(done.archived.length,2);});
test('unknown or corrupt progress is rejected rather than converted to empty state',()=>{const c=Core.create(meta);for(const value of ['broken','{}',JSON.stringify({...c.empty(),version:99}),JSON.stringify({...c.empty(),course:'someone-else'}),JSON.stringify({...c.empty(),completed:['first','first']})])assert.throws(()=>c.parse(value));});
test('grading separates correct incorrect and unanswered, independent of completion',()=>{const c=Core.create(meta),questions=[{id:'a',answer:'yes',explanation:'理由'},{id:'b',answer:'yes',explanation:'理由'},{id:'c',answer:'yes',explanation:'理由'}];const s=c.empty(),r=c.grade({a:'yes',b:'no'},questions);assert.deepEqual(r.map(x=>[x.answered,x.correct]),[[true,true],[true,false],[false,false]]);assert.deepEqual(s.completed,[]);});
test('actual opacity handler updates CSS and output without touching playback',()=>{const script=fs.readFileSync(path.join(R,'player.js'),'utf8');const line=script.split('\n').find(x=>x.includes("$('caption-opacity').addEventListener('input'"));let callback,opacity;const nodes={'caption-opacity':{value:'50',addEventListener:(name,fn)=>callback=fn},stage:{style:{setProperty:(name,value)=>{assert.equal(name,'--caption-opacity');opacity=value;}}},'caption-opacity-value':{}};vm.runInNewContext(line,{$:id=>nodes[id],prefs:{},savePrefs(){}});for(const [value,want] of [['50','0.5'],['0','0'],['100','1']]){nodes['caption-opacity'].value=value;callback();assert.equal(opacity,want);assert.equal(nodes['caption-opacity-value'].textContent,value+'%');}assert(fs.readFileSync(path.join(R,'app-shell.css'),'utf8').includes('var(--caption-opacity,.5)'));});
test('actual regrade handler replaces icons and does not update course progress',()=>{const script=fs.readFileSync(path.join(R,'player.js'),'utf8'),part=script.slice(script.indexOf("  $('grade').addEventListener"),script.indexOf("  $('memo').addEventListener"));const c=Core.create(meta),data={questions:[{id:'a',answer:'yes',explanation:'이유입니다.'}]};let handler,selected=[];const nodes={grade:{addEventListener:(_,fn)=>handler=fn},'feedback-a':{dataset:{}},'quiz-result':{}};vm.runInNewContext(part,{$:id=>nodes[id],C:c,data,document:{querySelectorAll:()=>selected}});handler();assert(nodes['feedback-a'].textContent.startsWith('⚠️'));selected=[{name:'a',value:'no'}];handler();assert(nodes['feedback-a'].textContent.startsWith('❌'));selected=[{name:'a',value:'yes'}];handler();assert(nodes['feedback-a'].textContent.startsWith('✅'));assert.equal(nodes['feedback-a'].dataset.result,'correct');assert(!nodes['feedback-a'].textContent.includes('❌'));});

test('valid constructor ID never uses an inherited revision',()=>{const c=Core.create({id:'constructor-course',lessons:[{id:'constructor',revision:'1'}]});assert.throws(()=>c.parse(JSON.stringify({...c.empty(),completed:['constructor']})));const state=c.complete(c.empty(),'constructor',true);assert.deepEqual(state.completed,['constructor']);assert.equal(state.revisions.constructor,'1');});

test('actual readiness handler distinguishes unknown, misconception and retry without progress writes',()=>{
 const script=fs.readFileSync(path.join(R,'player.js'),'utf8'),start=script.indexOf("  $('readiness-check')?.addEventListener"),end=script.indexOf("  $('memo').addEventListener",start);
 assert(start>=0&&end>start);
 const c=Core.create(meta),original=JSON.stringify(c.empty()),feedback={dataset:{}},nodes={'readiness-check':{addEventListener:(_,fn)=>handler=fn}};
 const q={id:'order',answer:'b',explanation:'완료 순서는 시작 순서와 다릅니다.',choice_explanations:{a:'시작 순서와 혼동했습니다.',b:'실제 완료 순서를 확인했습니다.'},preparation:'완료 시점을 비교하세요.'};
 let handler,selected=[];
 vm.runInNewContext(script.slice(start,end),{$:id=>nodes[id],C:c,data:{readiness:[q]},document:{querySelectorAll:()=>selected,querySelector:selector=>{assert.equal(selector,'[data-readiness-feedback="order"]');return feedback;}},save:()=>assert.fail('readiness must not save progress'),localStorage:{setItem:()=>assert.fail('readiness must not persist answers')},fetch:()=>assert.fail('readiness must stay offline')});
 handler();assert.equal(feedback.dataset.result,'unanswered');assert.match(feedback.textContent,/미응답/);
 selected=[{name:'readiness-order',value:'a'}];handler();assert.equal(feedback.dataset.result,'incorrect');assert.match(feedback.textContent,/시작 순서와 혼동/);assert.match(feedback.textContent,/사전 복습: 완료 시점/);
 selected=[{name:'readiness-order',value:'b'}];handler();assert.equal(feedback.dataset.result,'correct');assert.match(feedback.textContent,/실제 완료 순서/);assert(!feedback.textContent.includes('혼동'));assert.equal(JSON.stringify(c.empty()),original);
});

test('actual slide volume mute and speed handlers honor the optional-video boundary',()=>{
 const script=fs.readFileSync(path.join(R,'player.js'),'utf8'),nodes={},handlers={};
 const node=id=>nodes[id]??=( {value:'50',hidden:true,setAttribute(){},focus(){},addEventListener:(event,fn)=>{handlers[id+':'+event]=fn;}} );
 const rate={value:'0.75',checked:true,addEventListener:(_,fn)=>handlers.rate=fn};
 const state={muted:true,volume:1,rate:1},narration={setMuted:v=>state.muted=v,setVolume:v=>state.volume=v,setRate:v=>state.rate=v,snapshot:()=>state};
 const context={prefs:{muted:false,volume:1},savePrefs(){},$:node,narration,videoNarration:null,lastAudibleVolume:1,playbackRate:1,published:['slides'],NativeVideoPlayer:{},document:{querySelector:()=>({classList:{add(){}}}),querySelectorAll:()=>[rate]},activeTransport:()=>narration,setSettings(){},setSpeedMenu:()=>nodes['speed-panel'].hidden=true,paintVideoPlayback(){}};
 vm.createContext(context);
 const init=script.split('\n').find(x=>x.trim().startsWith('videoNarration=published.includes'));
 const setters=script.split('\n').filter(x=>x.includes('function setMasterMuted')||x.includes('function setMasterVolume')||x.includes("$('volume').addEventListener('input'")||x.includes("$('mute-toggle').addEventListener('click'")).join('\n');
 const speed=script.slice(script.indexOf('  document.querySelectorAll(\'[name="playback-speed"]\').forEach(el=>el.addEventListener'),script.indexOf('  function previewPoint'));
 node('speed-panel');vm.runInContext(init+'\n'+setters+'\n'+speed,context);
 handlers['volume:input']();assert.equal(state.volume,.5);assert.equal(state.muted,false);
 handlers['mute-toggle:click']();assert.equal(state.muted,true);
 handlers.rate();assert.equal(state.rate,.75);assert.equal(nodes['speed-panel'].hidden,true);
});
function nativeVideo(){const listeners={};return {readyState:1,duration:10,currentTime:0,playbackRate:1,ended:false,addEventListener:(n,fn)=>listeners[n]=fn,fire(n){listeners[n]?.();},load(){},play(){return Promise.resolve();},pause(){}};}
test('native video captions honor initial intermediate and trailing gaps',()=>{
 const v=nativeVideo(),p=require(path.join(R,'native-video-player.js')).create({lesson:{duration:10},scenes:[{start:2,end:3},{start:5,end:6}],video:v});
 for(const [time,active,index] of [[0,false,0],[2,true,0],[3,false,0],[4,false,0],[5,true,1],[6,false,1],[9,false,1]]){v.currentTime=time;const s=p.snapshot();assert.equal(s.captionActive,active,'time '+time);assert.equal(s.index,index);}
});
test('native video explicit seek after ended wins while plain replay starts at zero',async()=>{
 const v=nativeVideo(),p=require(path.join(R,'native-video-player.js')).create({lesson:{duration:10},scenes:[{start:2,end:3},{start:5,end:6}],video:v});
 v.currentTime=10;v.fire('ended');p.select(1,0,true);await Promise.resolve();assert.equal(v.currentTime,5);assert.equal(p.snapshot().status,'playing');
 v.currentTime=10;v.fire('ended');p.seekProgress(2.5);p.play();await Promise.resolve();assert.equal(v.currentTime,2.5);
 v.currentTime=10;v.fire('ended');p.play();await Promise.resolve();assert.equal(v.currentTime,0);
});
test('actual course-jump listener reads the updated resume target on click',()=>{
 const script=fs.readFileSync(path.join(R,'player.js'),'utf8'),line=script.split('\n').find(x=>x.includes("document.querySelectorAll('[data-course-jump]').forEach(el=>el.addEventListener"));
 let handler,jumped,prevented=false;const node={dataset:{courseJump:'first'},addEventListener:(_,fn)=>handler=fn};
 vm.runInNewContext(line,{document:{querySelectorAll:()=>[node]},courseJump:id=>jumped=id});
 node.dataset.courseJump='second';handler({preventDefault:()=>prevented=true});assert.equal(jumped,'second');assert.equal(prevented,true);
});

test('catalog search filters title description objectives and lesson names without storage or network',()=>{
 const cards=['React 요청 경합 응답 순서 경쟁 조건','테스트 최적화 번들 빌드 Vitest 실행'].map(text=>({dataset:{search:text},hidden:false}));
 let handler,clear,focused=false;const nodes={'catalog-search':{value:'',focus:()=>focused=true,addEventListener:(event,fn)=>{assert.equal(event,'input');handler=fn;}},'catalog-sort':{value:'recommended',addEventListener(){}},'catalog-direction':{addEventListener(){},setAttribute(){}},'catalog-count':{},'catalog-empty':{},'catalog-empty-title':{},'catalog-clear':{addEventListener:(_,fn)=>clear=fn},'catalog-search-controls':{hidden:true}},grid={hidden:false,append(){}};
 vm.runInNewContext(fs.readFileSync(path.join(R,'catalog.js'),'utf8'),{document:{getElementById:id=>nodes[id],querySelectorAll:()=>cards,querySelector:()=>grid,createDocumentFragment:()=>({append(){}})}});
 assert.equal(nodes['catalog-search-controls'].hidden,false);assert.deepEqual(cards.map(x=>x.hidden),[false,false]);
 for(const [query,want] of [['ｒｅａｃｔ',[false,true]],['응답 순서',[false,true]],['Vitest 실행',[true,false]],['없는 강의',[true,true]],['  ',[false,false]]]){nodes['catalog-search'].value=query;handler();assert.deepEqual(cards.map(x=>x.hidden),want);assert.equal(nodes['catalog-empty'].hidden,!want.every(Boolean));}
 assert.equal(nodes['catalog-count'].textContent,'전체 2개 중 2개 코스');
 nodes['catalog-search'].value='<없는 검색어>';handler();assert.equal(grid.hidden,true);assert.equal(nodes['catalog-empty-title'].textContent,"'<없는 검색어>'와 일치하는 코스가 없습니다.");
 clear();assert.equal(nodes['catalog-search'].value,'');assert.equal(focused,true);assert.equal(grid.hidden,false);assert.equal(nodes['catalog-empty'].hidden,true);assert.deepEqual(cards.map(x=>x.hidden),[false,false]);
});

test('actual header context exposes lesson titles and clears them on return home',()=>{
 const script=fs.readFileSync(path.join(R,'player.js'),'utf8'),start=script.indexOf('  function headerContext('),end=script.indexOf('\n  let captionsEnabled',start);
 const item={hidden:true},node={textContent:'',closest:()=>item},context={document:{querySelector:selector=>selector==='.header-title'?node:{classList:{toggle(){}}}},data:{course_label:'코스 제목'}};
 vm.createContext(context);vm.runInContext(script.slice(start,end),context);
 context.headerContext('첫 번째 강의');assert.equal(node.textContent,'첫 번째 강의');assert.equal(item.hidden,false);
 context.headerContext();assert.equal(node.textContent,'');assert.equal(item.hidden,true);
 context.headerContext('코스 제목');assert.equal(node.textContent,'');assert.equal(item.hidden,true);
 context.headerContext('<새 강의>');assert.equal(node.textContent,'<새 강의>');assert.equal(item.hidden,false);
});

test('volume popover offsets keep corner panels inside every requested viewport',()=>{
 const {popoverOffset}=require(path.join(R,'controls-ui.js'));
 for(const width of [390,600,800,1024,1440])for(const side of ['left','right','top']){
  const viewport={left:0,top:0,width,height:900},trigger={bottom:side==='top'?50:810};
  const rect={left:side==='left'?-20:side==='right'?width-60:100,top:side==='top'?-40:700,width:120,height:50};
  const offset=popoverOffset(rect,trigger,viewport),x=rect.left+offset.x,y=rect.top+offset.y;
  assert(x>=8 && x+rect.width<=width-8);assert(y>=8 && y+rect.height<=892);
  if(side==='top')assert.equal(y,58);
 }
 const rect={left:10,top:0,width:120,height:50},viewport={left:40,top:20,width:300,height:200};
 const {x,y}=popoverOffset(rect,{bottom:50},viewport);assert.equal(rect.left+x,48);assert.equal(rect.top+y,58);
});

test('actual volume popover handles hover keyboard escape touch outside dismissal and disabled audio',()=>{
 const {volumePopover}=require(path.join(R,'controls-ui.js'));
 function node(){
  const events=new Map(),classes=new Set();return {events,dataset:{},hidden:true,disabled:false,attrs:{},style:{setProperty(name,value){this[name]=value;}},
   classList:{add:value=>classes.add(value),remove:value=>classes.delete(value),contains:value=>classes.has(value)},
   addEventListener(type,fn){if(!events.has(type))events.set(type,[]);events.get(type).push(fn);},
   removeEventListener(type,fn){events.set(type,events.get(type).filter(x=>x!==fn));},
   setAttribute(name,value){this.attrs[name]=value;},contains(other){return [this,trigger,panel,slider].includes(other);},
   getBoundingClientRect:()=>({left:-20,top:700,width:120,height:50,bottom:750}),
   fire(type,event={}){for(const fn of [...events.get(type)||[]])fn({target:this,...event});}};
 }
 const container=node(),panel=node(),trigger=node(),slider=node(),doc=node(),win=node();win.innerWidth=390;win.innerHeight=900;doc.activeElement=null;
 trigger.focus=()=>{const previous=doc.activeElement;doc.activeElement=trigger;container.fire('focusin',{target:trigger,relatedTarget:previous});};
 const popup=volumePopover({container,panel,trigger,slider,document:doc,window:win});
 assert.equal(panel.hidden,true);assert.equal(trigger.attrs['aria-expanded'],'false');
 // Browsers can blur a focused range when its panel becomes hidden before focus is returned.
 let hidden=panel.hidden;Object.defineProperty(panel,'hidden',{get:()=>hidden,set(value){const previous=hidden;hidden=value;if(value&&!previous&&doc.activeElement===slider){doc.activeElement=null;container.fire('focusout',{relatedTarget:null});}}});
 container.fire('pointerenter',{pointerType:'mouse'});assert.equal(panel.hidden,false);assert.equal(container.classList.contains('open'),true);
 assert.equal(panel.style['--volume-shift-x'],'28px');container.fire('pointerleave');assert.equal(panel.hidden,true);
 // Tab entering from outside exposes the native range; its arrows are not intercepted.
 trigger.focus();assert.equal(popup.isOpen(),true);doc.activeElement=slider;
 let prevented=false,stopped=false;container.fire('keydown',{key:'ArrowRight',preventDefault:()=>prevented=true});assert.equal(prevented,false);
 container.fire('keydown',{key:'Escape',preventDefault:()=>prevented=true,stopPropagation:()=>stopped=true});
 assert.equal(prevented,true);assert.equal(stopped,true);assert.equal(panel.hidden,true);assert.equal(doc.activeElement,trigger);
 assert.equal(trigger.attrs['aria-expanded'],'false');assert.equal(popup.isOpen(),false);
 // Repeated touch activation opens without changing the range value or muting transport.
 slider.value='60';trigger.fire('click');assert.equal(panel.hidden,false);assert.equal(slider.value,'60');
 doc.fire('pointerdown',{target:{},composedPath:()=>[{}]});assert.equal(panel.hidden,true);
 trigger.fire('click');doc.fire('pointerdown',{target:slider,composedPath:()=>[slider,panel,container]});assert.equal(panel.hidden,false);
 container.fire('focusout',{relatedTarget:{}});assert.equal(panel.hidden,true);
 slider.disabled=true;trigger.fire('click');assert.equal(panel.hidden,true);assert.equal(trigger.attrs['aria-expanded'],'false');
 slider.disabled=false;trigger.fire('click');win.fire('resize');win.fire('scroll');doc.fire('fullscreenchange');assert.equal(panel.hidden,false);
 popup.destroy();assert.equal(panel.hidden,true);for(const item of [container,trigger,doc,win])for(const handlers of item.events.values())assert.equal(handlers.length,0);
});

test('versioned preferences survive fresh instances independently of progress, and reject invalid storage',()=>{
 const Prefs=require(path.join(R,'player-preferences.js')),values=new Map(),storage=()=>({getItem:k=>values.get(k),setItem:(k,v)=>values.set(k,v)});
 const initial=Prefs.load(storage);assert.equal(initial.muted,true);assert.equal(initial.captions,true);assert.equal(initial.captionOpacity,.5);assert.equal(initial.tocCollapsed,false);
 const chosen={...initial,muted:false,volume:.6,speed:1.5,captions:false,captionSize:'large',captionOpacity:.8,tocCollapsed:true};
 assert.equal(Prefs.save(storage,chosen),true);assert.deepEqual(Prefs.load(storage),chosen);assert.deepEqual([...values.keys()],[Prefs.KEY]);
 for(const bad of ['oops',JSON.stringify({...chosen,version:2}),JSON.stringify({...chosen,volume:101}),JSON.stringify({...chosen,muted:'false'}),JSON.stringify({...chosen,captionOpacity:-1}),JSON.stringify({...chosen,speed:NaN}),JSON.stringify({...chosen,tocCollapsed:1})])assert.deepEqual(Prefs.parse(bad),Prefs.defaults());
 const denied=()=>{throw Error('denied');};assert.deepEqual(Prefs.load(denied),Prefs.defaults());assert.equal(Prefs.save(denied,chosen),false);
 const old={...chosen};delete old.tocCollapsed;assert.equal(Prefs.parse(JSON.stringify(old)).tocCollapsed,false);
});

function narrationAudio(){return {duration:1,currentTime:0,plays:0,pause(){},play(){this.plays++;return this.plays===1?Promise.reject(Object.assign(new Error('gesture required'),{name:'NotAllowedError'})):Promise.resolve();}};}
const flush=async()=>{for(let i=0;i<8;i++)await Promise.resolve();};
test('audible narration retries muted only on policy rejection without blocking progress',async()=>{
 const create=require(path.join(R,'narration-player.js')).create,audio=narrationAudio(),slides=[{narration:[{speech:'설명',caption:'설명',audio:'data:audio/wav;base64,fixture'}]}];
 const player=create({slides,audio,initialMode:'assets',initialMuted:false});player.play();assert.equal(audio.muted,false);await flush();
 assert.equal(audio.plays,2);assert.equal(audio.muted,true);assert.equal(player.snapshot().mutedBlocked,true);assert.equal(player.snapshot().status,'playing');
 audio.onended();assert.equal(player.snapshot().status,'ended');player.setMuted(false);assert.equal(player.snapshot().mutedBlocked,false);
 const broken=narrationAudio();broken.play=()=>Promise.reject(new Error('decode'));const failed=create({slides,audio:broken,initialMode:'assets'});failed.play();await flush();assert.equal(failed.snapshot().status,'error');assert.equal(failed.snapshot().muted,false);
 const slow=narrationAudio(),stopped=create({slides,audio:slow,initialMode:'assets'});stopped.play();stopped.stop();await flush();assert.equal(slow.plays,1);assert.equal(stopped.snapshot().status,'idle');
});
test('finished-video audible rejection falls back muted and retains its native clock',async()=>{
 const video={...nativeVideo(),...narrationAudio(),duration:10,readyState:1};
 const player=require(path.join(R,'native-video-player.js')).create({lesson:{duration:10,has_audio:true},scenes:[{start:0,end:10}],video,initialMuted:false});
 player.play();await flush();assert.equal(video.plays,2);assert.equal(player.snapshot().status,'playing');assert.equal(player.snapshot().mutedBlocked,true);assert.equal(video.muted,true);
 video.currentTime=6;assert.equal(player.snapshot().time,6);player.setMuted(false);assert.equal(player.snapshot().mutedBlocked,false);
});
test('pausing a pending audible attempt cancels its muted retry even if playback resumes',async()=>{
 const create=require(path.join(R,'narration-player.js')).create,slides=[{narration:[{speech:'설명',caption:'설명',audio:'fixture'}]}];
 let reject,plays=0;const audio={duration:1,currentTime:0,pause(){},play(){plays++;return plays===1?new Promise((_,no)=>reject=no):Promise.resolve();}};
 const player=create({slides,audio,initialMode:'assets'});player.play();player.pause();player.play();
 reject(Object.assign(Error('blocked'),{name:'NotAllowedError'}));await flush();assert.equal(plays,2);assert.equal(player.snapshot().muted,false);assert.equal(player.snapshot().status,'playing');
 let no;const pausedAudio={...audio,play:()=>new Promise((_,reject)=>no=reject)};const paused=create({slides,audio:pausedAudio,initialMode:'assets'});paused.play();paused.pause();no(Object.assign(Error('blocked'),{name:'NotAllowedError'}));await flush();assert.equal(paused.snapshot().status,'paused');assert.equal(paused.snapshot().muted,false);
});

function testClock(){let now=0,id=0;const timers=new Map();return {now:()=>now,setTimeout:(fn,ms)=>{timers.set(++id,{at:now+ms,fn});return id;},clearTimeout:id=>timers.delete(id),advance(ms){const end=now+ms;while(true){const next=[...timers].sort((a,b)=>a[1].at-b[1].at)[0];if(!next||next[1].at>end)break;now=next[1].at;timers.delete(next[0]);next[1].fn();}now=end;}};}
function pacedPlayer(pacing={initialLeadInMs:5000,postSlideHoldMs:1800,slidePauseMs:1200,sentencePauseMs:600}){
 const clock=testClock(),audio={duration:1,currentTime:0,plays:0,pause(){},play(){this.plays++;return Promise.resolve();}},slides=[{narration:[{speech:'첫 설명',audio:'one'},{speech:'다음 문장',audio:'two'}]},{narration:[{speech:'다음 장',audio:'three'}]}];
 return {clock,audio,p:require(path.join(R,'narration-player.js')).create({slides,audio,pacing,clock})};
}
test('fresh lead-in, sentence control, post-slide hold, and next lead-in have distinct clock boundaries',async()=>{
 const {clock,audio,p}=pacedPlayer();p.play();assert.equal(p.snapshot().waitKind,'start');clock.advance(4999);assert.equal(audio.plays,0);clock.advance(1);await flush();assert.equal(audio.plays,1);
 audio.onended();assert.equal(p.snapshot().cue,1);assert.equal(p.snapshot().waitKind,'sentence');clock.advance(599);assert.equal(audio.plays,1);clock.advance(1);await flush();assert.equal(audio.plays,2);
 audio.onended();assert.equal(p.snapshot().slide,0);assert.equal(p.snapshot().cue,1);assert.equal(p.snapshot().waitKind,'hold');clock.advance(1799);assert.equal(p.snapshot().slide,0);clock.advance(1);assert.equal(p.snapshot().slide,1);assert.equal(p.snapshot().waitKind,'slide');clock.advance(1199);assert.equal(audio.plays,2);clock.advance(1);await flush();assert.equal(audio.plays,3);audio.onended();assert.equal(p.snapshot().status,'ended');clock.advance(10000);assert.equal(audio.plays,3);
});
test('pause/resume consumes only remaining waits, rate and pacing edits do not restart an active wait',async()=>{
 const {clock,audio,p}=pacedPlayer();p.play();clock.advance(2000);p.pause();clock.advance(9999);assert.equal(audio.plays,0);p.setRate(2);p.play();clock.advance(2999);assert.equal(audio.plays,0);clock.advance(1);await flush();audio.onended();clock.advance(600);await flush();audio.onended();clock.advance(800);p.pause();p.setPacing({postSlideHoldMs:5000});clock.advance(9999);p.play();clock.advance(999);assert.equal(p.snapshot().slide,0);clock.advance(1);assert.equal(p.snapshot().slide,1);clock.advance(1200);await flush();assert.equal(audio.plays,3);
});
test('manual selection and seek cancel hold advancement and never replay fresh-entry lead-in',async()=>{
 const {clock,audio,p}=pacedPlayer();p.play();clock.advance(5000);await flush();audio.onended();clock.advance(600);await flush();audio.onended();const stale=audio.onended;p.select(1,0,true);assert.equal(p.snapshot().waitKind,'slide');clock.advance(1200);await flush();assert.equal(audio.plays,3);clock.advance(5000);assert.equal(p.snapshot().slide,1);p.pause();p.seekProgress(0);const beforeSeek=audio.plays;p.play();assert.equal(audio.plays,beforeSeek+1);assert.notEqual(p.snapshot().status,'waiting');clock.advance(5000);await flush();assert.equal(p.snapshot().slide,0);if(stale)stale();assert.equal(p.snapshot().slide,0);
});
test('explicit zero and legacy pacing keep immediate-first behavior, silent progression still advances safely',()=>{
 const {p,audio}=pacedPlayer({slidePauseMs:0,sentencePauseMs:0});p.play();assert.equal(audio.plays,1);
 const {p:s,clock}=pacedPlayer();s.setMode('silent');s.play();clock.advance(5000);assert.equal(s.snapshot().status,'playing');clock.advance(4000);assert.equal(s.snapshot().waitKind,'sentence');s.stop();clock.advance(100000);assert.equal(s.snapshot().status,'idle');
 for(const bad of [{initialLeadInMs:-1},{postSlideHoldMs:5001},{slidePauseMs:'0'},{sentencePauseMs:NaN},{extra:1},null])assert.throws(()=>p.setPacing(bad));
});
