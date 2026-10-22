const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const R=path.resolve(__dirname,'../skills/tk-course/assets'),Core=require(path.join(R,'course-core.js'));
const meta={id:'sample',lessons:[{id:'first',revision:'1'},{id:'second',revision:'1'}]};
test('manual completion survives rename/reorder and preserves notes',()=>{const c=Core.create(meta),s=c.complete(c.empty(),'first',true);s.memos.first='나의 근거';const reordered=Core.create({...meta,lessons:[...meta.lessons].reverse()});const next=reordered.parse(JSON.stringify(s));assert.deepEqual(next.completed,['first']);assert.equal(next.memos.first,'나의 근거');assert.deepEqual(s.archived,[]);});
test('changed and deleted lessons archive completions while preserving notes',()=>{const c=Core.create(meta);let s=c.complete(c.empty(),'first',true);s=c.complete(s,'second',true);s.memos.second='삭제 전 메모';const changed=Core.create({id:'sample',lessons:[{id:'first',revision:'2'}]});const next=changed.parse(JSON.stringify(s));assert.deepEqual(next.completed,[]);assert.deepEqual(next.archived,[{lesson:'first',revision:'1'},{lesson:'second',revision:'1'}]);assert.equal(next.memos.second,'삭제 전 메모');const done=changed.complete(next,'first',true);assert.deepEqual(done.completed,['first']);assert.equal(done.revisions.first,'2');assert.equal(done.archived.length,2);});
test('unknown or corrupt progress is rejected rather than converted to empty state',()=>{const c=Core.create(meta);for(const value of ['broken','{}',JSON.stringify({...c.empty(),version:99}),JSON.stringify({...c.empty(),course:'someone-else'}),JSON.stringify({...c.empty(),completed:['first','first']})])assert.throws(()=>c.parse(value));});
test('grading separates correct incorrect and unanswered, independent of completion',()=>{const c=Core.create(meta),questions=[{id:'a',answer:'yes',explanation:'理由'},{id:'b',answer:'yes',explanation:'理由'},{id:'c',answer:'yes',explanation:'理由'}];const s=c.empty(),r=c.grade({a:'yes',b:'no'},questions);assert.deepEqual(r.map(x=>[x.answered,x.correct]),[[true,true],[true,false],[false,false]]);assert.deepEqual(s.completed,[]);});
test('actual opacity handler updates CSS and output without touching playback',()=>{const script=fs.readFileSync(path.join(R,'player.js'),'utf8');const line=script.split('\n').find(x=>x.includes("$('caption-opacity').addEventListener('input'"));let callback,opacity;const nodes={'caption-opacity':{value:'50',addEventListener:(name,fn)=>callback=fn},stage:{style:{setProperty:(name,value)=>{assert.equal(name,'--caption-opacity');opacity=value;}}},'caption-opacity-value':{}};vm.runInNewContext(line,{$:id=>nodes[id]});for(const [value,want] of [['50','0.5'],['0','0'],['100','1']]){nodes['caption-opacity'].value=value;callback();assert.equal(opacity,want);assert.equal(nodes['caption-opacity-value'].textContent,value+'%');}assert(fs.readFileSync(path.join(R,'app-shell.css'),'utf8').includes('var(--caption-opacity,.5)'));});
test('actual regrade handler replaces icons and does not update course progress',()=>{const script=fs.readFileSync(path.join(R,'player.js'),'utf8'),part=script.slice(script.indexOf("  $('grade').addEventListener"),script.indexOf("  $('memo').addEventListener"));const c=Core.create(meta),data={questions:[{id:'a',answer:'yes',explanation:'이유입니다.'}]};let handler,selected=[];const nodes={grade:{addEventListener:(_,fn)=>handler=fn},'feedback-a':{dataset:{}},'quiz-result':{}};vm.runInNewContext(part,{$:id=>nodes[id],C:c,data,document:{querySelectorAll:()=>selected}});handler();assert(nodes['feedback-a'].textContent.startsWith('⚠️'));selected=[{name:'a',value:'no'}];handler();assert(nodes['feedback-a'].textContent.startsWith('❌'));selected=[{name:'a',value:'yes'}];handler();assert(nodes['feedback-a'].textContent.startsWith('✅'));assert.equal(nodes['feedback-a'].dataset.result,'correct');assert(!nodes['feedback-a'].textContent.includes('❌'));});

test('valid constructor ID never uses an inherited revision',()=>{const c=Core.create({id:'constructor-course',lessons:[{id:'constructor',revision:'1'}]});assert.throws(()=>c.parse(JSON.stringify({...c.empty(),completed:['constructor']})));const state=c.complete(c.empty(),'constructor',true);assert.deepEqual(state.completed,['constructor']);assert.equal(state.revisions.constructor,'1');});

test('actual slide volume mute and speed handlers honor the optional-video boundary',()=>{
 const script=fs.readFileSync(path.join(R,'player.js'),'utf8'),nodes={},handlers={};
 const node=id=>nodes[id]??=( {value:'50',hidden:true,setAttribute(){},focus(){},addEventListener:(event,fn)=>{handlers[id+':'+event]=fn;}} );
 const rate={value:'0.75',checked:true,addEventListener:(_,fn)=>handlers.rate=fn};
 const state={muted:true,volume:1,rate:1},narration={setMuted:v=>state.muted=v,setVolume:v=>state.volume=v,setRate:v=>state.rate=v,snapshot:()=>state};
 const context={$:node,narration,videoNarration:null,lastAudibleVolume:1,playbackRate:1,published:['slides'],NativeVideoPlayer:{},document:{querySelector:()=>({classList:{add(){}}}),querySelectorAll:()=>[rate]},activeTransport:()=>narration,setSettings(){},setSpeedMenu:()=>nodes['speed-panel'].hidden=true,paintVideoPlayback(){}};
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
 let handler,clear,focused=false;const nodes={'catalog-search':{value:'',focus:()=>focused=true,addEventListener:(event,fn)=>{assert.equal(event,'input');handler=fn;}},'catalog-count':{},'catalog-empty':{},'catalog-empty-title':{},'catalog-clear':{addEventListener:(_,fn)=>clear=fn},'catalog-search-controls':{hidden:true}},grid={hidden:false};
 vm.runInNewContext(fs.readFileSync(path.join(R,'catalog.js'),'utf8'),{document:{getElementById:id=>nodes[id],querySelectorAll:()=>cards,querySelector:()=>grid}});
 assert.equal(nodes['catalog-search-controls'].hidden,false);assert.deepEqual(cards.map(x=>x.hidden),[false,false]);
 for(const [query,want] of [['ｒｅａｃｔ',[false,true]],['응답 순서',[false,true]],['Vitest 실행',[true,false]],['없는 강의',[true,true]],['  ',[false,false]]]){nodes['catalog-search'].value=query;handler();assert.deepEqual(cards.map(x=>x.hidden),want);assert.equal(nodes['catalog-empty'].hidden,!want.every(Boolean));}
 assert.equal(nodes['catalog-count'].textContent,'전체 2개 중 2개 코스');
 nodes['catalog-search'].value='<없는 검색어>';handler();assert.equal(grid.hidden,true);assert.equal(nodes['catalog-empty-title'].textContent,"'<없는 검색어>'와 일치하는 코스가 없습니다.");
 clear();assert.equal(nodes['catalog-search'].value,'');assert.equal(focused,true);assert.equal(grid.hidden,false);assert.equal(nodes['catalog-empty'].hidden,true);assert.deepEqual(cards.map(x=>x.hidden),[false,false]);
});

test('actual header context exposes lesson titles and clears them on return home',()=>{
 const script=fs.readFileSync(path.join(R,'player.js'),'utf8'),start=script.indexOf('  function headerContext('),end=script.indexOf('\n  let captionsEnabled',start);
 const node={textContent:'',hidden:true},context={document:{querySelector:()=>node},data:{course_label:'코스 제목'}};
 vm.createContext(context);vm.runInContext(script.slice(start,end),context);
 context.headerContext('첫 번째 강의');assert.equal(node.textContent,'첫 번째 강의');assert.equal(node.hidden,false);
 context.headerContext();assert.equal(node.textContent,'');assert.equal(node.hidden,true);
 context.headerContext('코스 제목');assert.equal(node.textContent,'');assert.equal(node.hidden,true);
 context.headerContext('<새 강의>');assert.equal(node.textContent,'<새 강의>');assert.equal(node.hidden,false);
});
