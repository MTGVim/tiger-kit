(() => {
  'use strict';
  const $=id=>document.getElementById(id), P=PlayerModel, S=CourseShellModel;
  const data=JSON.parse($('lesson-data').textContent), C=CourseCore.create(data.course_meta), count=data.slides.length, published=data.published_lessons || data.lessons.map(l=>l.id);
  const publishedCompleted=()=>state.completed.filter(id=>C.LESSONS.includes(id));
  let view={lesson:published[0],slide:0}, storageBlocked=false, storedRaw='', state=C.empty(), narration=null, videoNarration=null, homeVisible=true, lastPosition=null,seekController=null,seekVideo=null;
  const key='tigerkit-course:'+C.COURSE, positionKey=key+':position:'+data.lesson_id+':'+data.narration_revision;
  const progressId=()=>data.lesson_id;
  function headerContext(title='') {
    const node=document.querySelector('.header-title');
    node.textContent=title===data.course_label?'':title;node.hidden=!node.textContent;
  }
  function courseJump(id){if(!C.LESSONS.includes(id))return;if(window.parent!==window)window.parent.postMessage({type:'course-lesson',id},'*');else location.href='lesson-'+id+'.html#lesson-'+data.course_lessons.find(x=>x.id===id).kind;}
  let captionsEnabled=true,transcriptOpen=false,playbackRate=1,scrubbing=false,lastAudibleVolume=1;
  const U=CourseControls;
  const volumePopover=U.volumePopover({container:document.querySelector('.volume-control'),panel:$('volume-panel'),trigger:$('mute-toggle'),slider:$('volume'),document,window});
  function setControl(id,icon,label){U.icon($(id),icon,label);}
  const pacing=data.production_choices.pacing;
  try{lastPosition=S.position(localStorage.getItem(positionKey),data.slides);if(lastPosition && !published.includes(lastPosition.lesson))lastPosition=null;}catch(_){}
  try {storedRaw=localStorage.getItem(key)||'';if(storedRaw)state=C.parse(storedRaw);}catch(_){storageBlocked=true;$('save-status').textContent='⚠️ 저장된 진도를 읽지 못했습니다. 원본을 내보내고 올바른 JSON을 가져오세요. 기존 저장은 보존합니다.';}
  function save() {
    if(storageBlocked){$('save-status').textContent='⚠️ 기존 진도 보존 중입니다. 원본을 내보내고 올바른 JSON을 가져오세요.';return;}
    try {localStorage.setItem(key,JSON.stringify(state));$('save-status').textContent='이 브라우저에 진도와 메모를 저장했습니다.';}
    catch(_) {$('save-status').textContent='브라우저 저장을 사용할 수 없습니다. 진도 JSON을 복사해 보관하세요.';}
  }
  function progress() {
    $('course-fill').style.width=(publishedCompleted().length/C.LESSONS.length*100)+'%';
    $('completion-count').textContent=`${publishedCompleted().length} / ${C.LESSONS.length}`;
    document.querySelectorAll('[data-lesson]').forEach(el=>{
      const done=state.completed.includes(data.lesson_id);
      el.querySelector('.lesson-check').textContent=done?'✓':'';
      el.querySelector('.lesson-check').dataset.completed=String(done);
      el.querySelector('.lesson-check').setAttribute('aria-label',done?'완료로 표시한 강의':'완료 표시 없음');
    });
    $('mark-complete').checked=state.completed.includes(data.lesson_id);
    $('memo').value=Object.hasOwn(state.memos,data.lesson_id)?state.memos[data.lesson_id]:'';
    document.querySelectorAll('[data-course-check]').forEach(el=>{const done=state.completed.includes(el.dataset.courseCheck);el.dataset.completed=String(done);el.textContent=done?'✓':'';el.setAttribute('aria-label',done?'완료로 표시한 강의':state.archived.some(x=>x.lesson===el.dataset.courseCheck)?'다시 확인 필요':'완료 표시 없음');});
    $('home-progress-label').textContent=`${publishedCompleted().length} / ${C.LESSONS.length}`;
    $('home-fill').style.width=(publishedCompleted().length/C.LESSONS.length*100)+'%';
    $('home-start-label').textContent=lastPosition?'이어서 학습하기':'강의 시작하기';
    let latest=null;try{latest=localStorage.getItem(key+':last-lesson');}catch(_){}
    $('home-start').dataset.courseJump=C.LESSONS.includes(latest)?latest:C.LESSONS[0];$('home-start-label').textContent=C.LESSONS.includes(latest)?'이어서 학습하기':'강의 시작하기';
    document.querySelectorAll('[data-home-status]').forEach(el=>{
      const done=state.completed.includes(el.dataset.homeStatus);
      el.textContent=done?'✓ 완료':state.archived.some(x=>x.lesson===el.dataset.homeStatus)?'다시 확인 필요':'시작 전';
      el.classList.toggle('done',done);
    });
  }
  function render() {
    const visible=P.visible(view,count), isSlide=view.lesson==='slides', lesson=data.lessons.find(l=>l.id===view.lesson);
    $('lesson-heading').textContent=lesson.title;
    headerContext(homeVisible?'':lesson.title);
    $('lesson-kind').textContent=isSlide?`${count}장 / 음성으로 진행`:data.video_lesson.has_audio?'영상 / 내장 음성':'영상 / 무음 영상';
    $('settings-toggle').hidden=false;$('stage').dataset.mediaKind=isSlide?'slides':'video';
    $('slide-num').textContent=isSlide?`${view.slide+1} / ${count}`:'설명 영상';
    $('slide-fill').style.width=isSlide?`${(view.slide+1)/count*100}%`:'0%';
    $('video-wrap').hidden=!visible.video;
    $('slide-wrap').hidden=!isSlide;
    document.querySelectorAll('[data-slide]').forEach(el=>{el.hidden=Number(el.dataset.slide)!==visible.slide;});
    $('controls').hidden=false;$('thumbs').hidden=!isSlide;
    $('prev').disabled=view.slide===0;$('next').disabled=view.slide===count-1;
    $('pos').textContent=`${view.slide+1} / ${count}`;
    document.querySelectorAll('[data-thumb]').forEach(el=>{const active=Number(el.dataset.thumb)===view.slide;el.classList.toggle('current',active);if(active)el.setAttribute('aria-current','step');else el.removeAttribute('aria-current');});
    document.querySelectorAll('[data-lesson]').forEach(el=>{const active=el.dataset.lesson===view.lesson;el.classList.toggle('active',active);if(active)el.setAttribute('aria-current','page');else el.removeAttribute('aria-current');});
    $('tx-title').textContent=isSlide?data.slides[view.slide].title:data.lesson_title;
    $('tx-copy').replaceChildren();$('rail-copy').replaceChildren();$('rail-title').textContent=$('tx-title').textContent;
    const transcript=isSlide?data.slides[view.slide].narration:data.video_scenes;
    transcript.forEach((cue,i)=>{
      for(const target of ['tx-copy','rail-copy']){
        const line=document.createElement('button');line.type='button';line.className='tx-cue';line.dataset.cue=i;line.textContent=cue.caption;line.title='이 문장부터 듣기';
        line.addEventListener('click',()=>isSlide?narration.select(view.slide,i,true):videoNarration.select(i,0,true));$(target).append(line);
      }
    });
    $('reading-note').textContent=lesson.note;
    $('next-lesson').textContent='다음 강의';
    $('end-panel').classList.toggle('active',isSlide && narration && narration.snapshot().status==='ended');
    $('live-caption').hidden=!isSlide || !narration || !['playing','loading','waiting','paused','ended'].includes(narration.snapshot().status);
    $('next-lesson').hidden=C.LESSONS.indexOf(data.lesson_id)===C.LESSONS.length-1;
    $('voice-state').hidden=false;
    if(isSlide && narration)paintPlayback(narration.snapshot());else if(videoNarration)paintVideoPlayback(videoNarration.snapshot());
    progress();
  }
  function remember() {
    if(homeVisible || !narration)return;
    const snap=narration.snapshot();
    const position={lesson:view.lesson,slide:view.slide,cue:view.lesson==='slides'?snap.cue:0,videoTime:view.lesson==='video'?videoNarration.snapshot().time:0};
    if(JSON.stringify(position)===JSON.stringify(lastPosition))return;
    lastPosition=position;
    try{localStorage.setItem(positionKey,JSON.stringify(position));localStorage.setItem(key+':last-lesson',data.lesson_id);}catch(_){}
  }
  function navigate(hash) {
    if(location.hash===hash)return;
    try{history.pushState(null,'',hash);}catch(_){}
  }
  function lesson(id,options={}) {
    if(!published.includes(id)){home();return;}
    if(seekController)seekController.cancel(false);
    const resume=options.resume && lastPosition && lastPosition.lesson===id?{...lastPosition}:null;
    volumePopover.close();setCaptionMenu(false);setSpeedMenu(false);setSettings(false);showTranscript(false);scrubbing=false;remember();narration.stop();videoNarration.stop();$('lesson-video').pause();
    homeVisible=false;$('home').hidden=true;$('player-page').hidden=false;
    $('back-home').hidden=false;$('menu-toggle').hidden=false;$('skip-main').setAttribute('href','#lesson-heading');
    view={lesson:id,slide:resume?resume.slide:0};
    P.visible(view,count);
    if(id==='slides')narration.select(view.slide,resume?resume.cue:0,false);
    else{videoNarration.select(view.slide,0,false);if(resume)videoNarration.seekProgress(resume.videoTime);}
    activeTransport().setRate(playbackRate);
    render();remember();
    $('toc').classList.remove('open');$('menu-toggle').setAttribute('aria-expanded','false');
    if(options.push!==false)navigate('#lesson-'+id);
    if(options.focus!==false)$('lesson-heading').focus();
  }
  function home(push=true,focus=true) {
    if(seekController)seekController.cancel(false);
    volumePopover.close();setCaptionMenu(false);setSpeedMenu(false);setSettings(false);showTranscript(false);scrubbing=false;remember();narration.stop();videoNarration.stop();$('lesson-video').pause();
    homeVisible=true;$('home').hidden=false;$('player-page').hidden=true;
    headerContext();
    $('back-home').hidden=true;$('menu-toggle').hidden=true;$('toc').classList.remove('open');
    $('menu-toggle').setAttribute('aria-expanded','false');$('skip-main').setAttribute('href','#home-title');
    progress();if(push)navigate('#home');if(focus)$('home-title').focus();
  }
  function applyRoute() {
    const target=S.route(location.hash,published);
    if(target==='home')home(false,false);
    else if(homeVisible || view.lesson!==target)lesson(target,{resume:true,push:false,focus:false});
  }
  function activeTransport(){return view.lesson==='slides'?narration:videoNarration;}
  function currentIndex(){return view.lesson==='slides'?view.slide:videoNarration.snapshot().slide;}
  function paintPlayback(s) {
    if(view.lesson!=='slides' || homeVisible)return;
    if(view.slide!==s.slide){view=P.step(view,s.slide-view.slide,count);render();return;}
    paintTransport(s,data.slides[s.slide].narration,s.cue);
  }
  function paintVideoPlayback(s) {
    if(view.lesson!=='video' || homeVisible)return;
    if(view.slide!==s.slide){view={lesson:'video',slide:s.slide};render();return;}
    paintTransport(s,data.video_scenes,s.slide);
  }
  function paintTransport(s,cues,index) {
    const isSlide=view.lesson==='slides',running=['playing','loading','waiting'].includes(s.status);
    setControl('play',running?'pause':s.status==='ended'?'replay':'play',running?'일시정지':s.status==='ended'?'다시 듣기':'재생');
    $('speed-label').textContent=s.rate+'×';$('speed-pending').hidden=!s.ratePending;
    const rateLabel=s.ratePending?'현재 '+s.appliedRate+'배, 다음 문장부터 '+s.rate+'배':'재생 속도 '+s.rate+'배';
    $('speed').setAttribute('aria-label',rateLabel+', 속도 선택 열기');$('speed').title=rateLabel;
    document.querySelectorAll('[name="playback-speed"]').forEach(el=>{el.checked=Number(el.value)===s.rate;});
    const quiet=s.muted||s.volume===0||s.mode==='silent';
    setControl('mute-toggle',quiet?'volume-off':'volume',s.mode==='silent'?'음성 설정 열기':'음소거');
    if(s.mode==='silent')$('mute-toggle').removeAttribute('aria-pressed');else $('mute-toggle').setAttribute('aria-pressed',String(quiet));
    $('mute-toggle').title=s.mode==='silent'?'무음 재생, 음성 설정 열기':quiet?'음소거 해제':'음소거';
    document.querySelector('.volume-control').dataset.silent=String(s.mode==='silent');$('volume').disabled=s.mode==='silent';if(s.mode==='silent')volumePopover.close();
    $('volume').value=Math.round(s.volume*100);$('volume').setAttribute('aria-valuetext',Math.round(s.volume*100)+'%'+(quiet?', 음소거':''));
    $('volume-note').textContent=s.mode==='silent'?'':s.mode==='video'?(s.hasAudio?'영상에 포함된 음성을 재생합니다.':'⚠️ 현재 영상에는 음성이 없습니다.'):s.mode==='device'?'':'생성 음원의 볼륨과 음소거는 재생 위치를 유지하며 바로 적용됩니다.';
    $('play').disabled=!s.available;$('stage-play').disabled=!s.available;
    $('stage-play').hidden=!isSlide || running;$('stage-play').setAttribute('aria-label',s.status==='ended'?'강의 다시 듣기':'강의 재생');
    $('voice-state').textContent=s.mode==='video'?(s.hasAudio?'영상 내장 음성':'무음 영상'):s.mode==='silent'?'무음':s.mode==='assets'?(s.hasAssets?'생성한 강의 음성':'⚠️ 생성 음성 파일 준비 전'):s.available?'브라우저 음성: '+s.voice:s.voiceSelection?'⚠️ 선택한 한국어 음성을 사용할 수 없습니다.':'⚠️ 이 브라우저에 설치된 한국어 음성을 찾지 못했습니다.';
    $('voice-fallback').hidden=!isSlide||s.mode==='silent'||s.available;
    $('voice-preflight-message').textContent=s.mode==='device'?'이 기기에서 한국어 음성을 찾지 못했습니다.':'생성 음성이 준비되지 않았습니다.';
    $('use-browser-voice').disabled=!s.voices.length;$('use-browser-voice').title=s.voices.length?'브라우저 음성':'이 기기에서 사용할 한국어 음성이 없습니다.';
    const messages={idle:'재생을 누르면 도식이 설명 순서대로 나타납니다. 재생 설정에서 모두 볼 수도 있습니다.',playing:isSlide?'강의를 재생하고 있습니다.':'한국어 영상과 음성을 함께 재생하고 있습니다.',waiting:s.waitKind==='slide'?'화면을 살펴볼 수 있도록 잠시 기다립니다.':'다음 문장 전에 잠시 쉽니다.',loading:'음성을 불러오고 있습니다.',paused:'일시정지했습니다.',ended:'강의가 끝났습니다. 이해 확인을 풀거나 코스 홈으로 돌아가세요.',blocked:'⚠️ 강의 음성을 사용할 수 없습니다.',error:'⚠️ 음성을 재생하지 못했습니다. 현재 음성 모드를 확인한 뒤 다시 시도하세요.'};
    $('player-status').textContent=s.available?(['error','blocked','ended'].includes(s.status)?messages[s.status]:''):s.mode==='assets'?'':s.voiceSelection?'⚠️ 선택한 음성을 찾지 못했습니다. 재생 설정에서 다른 로컬 한국어 음성을 선택하세요.':'⚠️ 이 브라우저에서 사용할 수 있는 로컬 한국어 음성이 없습니다.';
    const cc=U.caption({enabled:captionsEnabled,status:s.status,cue:!isSlide&&!s.captionActive?'':cues[index].caption,gap:s.status==='paused'&&s.waitMs!==null,previous:isSlide&&index>0?cues[index-1].caption:''});
    $('live-caption').hidden=cc.hidden;$('caption-text').textContent=cc.text;
    $('captions-toggle').setAttribute('aria-pressed',String(captionsEnabled));
    setControl('captions-toggle','captions',captionsEnabled?'자막 숨기기':'자막 보이기');
    paintVoiceOptions(s);
    document.querySelectorAll('.tx-cue').forEach(line=>{const current=Number(line.dataset.cue)===index&&(isSlide||s.captionActive);line.classList.toggle('active',current);if(current)line.setAttribute('aria-current','true');else line.removeAttribute('aria-current');});
    $('end-panel').classList.toggle('active',isSlide && s.status==='ended');
    $('audio-progress').hidden=false;$('audio-seek').hidden=false;
    if(!scrubbing){
      $('audio-seek').max=s.progress.total;$('audio-seek').step=isSlide?'0.001':'0.1';$('audio-seek').value=s.progress.value;
      $('audio-seek').style.setProperty('--played',(100*s.progress.value/s.progress.total)+'%');
      const label=isSlide?U.progressLabel(data,view.lesson,s.index).label:U.timeLabel(s.time,s.duration);
      $('audio-time').textContent=label+(s.status==='ended'?' · 완료':'');$('audio-seek').setAttribute('aria-valuetext',label);
      const stamp=n=>Math.floor(n/60)+':'+String(Math.floor(n%60)).padStart(2,'0');
      $('progress-kind').textContent=s.mode==='video'?(s.hasAudio?'':'⚠️ 무음 영상'):s.mode==='silent'?`무음 · 설명당 ${s.silentHoldMs/1000}초`:s.mode==='assets'&&s.duration?`현재 문장 ${stamp(s.time||0)} / ${stamp(s.duration)}`:s.progress.kind==='boundary'?'발화 위치 기준':'설명 단위 이동';
    }
    $('pos').textContent=`${isSlide?'슬라이드':'장면'} ${s.slide+1} / ${isSlide?count:data.video_scenes.length}`;
    $('prev').disabled=s.slide===0;$('next').disabled=s.slide===(isSlide?count:data.video_scenes.length)-1;
    paintEmphasis(s);remember();
  }
  function paintEmphasis(s){
    const mode=$('motion-mode').value;
    document.querySelectorAll('.lesson-slide').forEach(el=>{
      const svg=el.querySelector('svg'),current=Number(el.dataset.slide)===s.slide;
      if(current&&mode!=='off')svg.setAttribute('data-follow-cue','true');else svg.removeAttribute('data-follow-cue');
      if(current&&mode==='on')svg.setAttribute('data-progressive','true');else svg.removeAttribute('data-progressive');
      el.querySelectorAll('[data-emphasis]').forEach(group=>{
        const indices=group.dataset.emphasis.trim()?group.dataset.emphasis.split(' ').map(Number):[];
        const v=CoursePresentation.step(indices,s,current?mode:'off');
        group.setAttribute('data-revealed',String(v.visible));group.setAttribute('data-focused',String(v.focused));
      });
    });
  }
  function jump(index) {
    index=Math.max(0,Math.min((view.lesson==='slides'?count:data.video_scenes.length)-1,index));if(index===currentIndex())return;
    activeTransport().select(index);
  }
  document.querySelectorAll('[data-js-only]').forEach(el=>{el.hidden=false;});
  $('play').addEventListener('click',()=>activeTransport().toggle());
  $('stage-play').addEventListener('click',()=>activeTransport().toggle());
  function setVoiceMode(mode){
    narration.setMode(mode);$('voice-mode').value=mode;
    render();
  }
  $('voice-mode').addEventListener('change',()=>setVoiceMode($('voice-mode').value));
  function setMasterMuted(value){narration.setMuted(value);videoNarration.setMuted(value);}
  function setMasterVolume(value){if(value>0)lastAudibleVolume=value;narration.setVolume(value);videoNarration.setVolume(value);}
  $('use-browser-voice').addEventListener('click',()=>{setVoiceMode('device');$('mute-toggle').focus();});
  $('use-silent').addEventListener('click',()=>{setVoiceMode('silent');activeTransport().play();$('play').focus();});
  $('mute-toggle').addEventListener('click',()=>{const s=activeTransport().snapshot();if(s.mode==='silent'){setSettings(true);$('voice-mode').focus();return;}if(s.muted||s.volume===0){if(s.volume===0)setMasterVolume(lastAudibleVolume);setMasterMuted(false);}else setMasterMuted(true);});
  $('volume').addEventListener('input',()=>{const value=Number($('volume').value)/100;setMasterVolume(value);setMasterMuted(value===0);});
  function pacingChanged(){
    const values=[$('slide-pause'),$('sentence-pause')];
    if(values.some(el=>!el.validity.valid || el.value===''))return;
    const next={slidePauseMs:Number(values[0].value)*1000,sentencePauseMs:Number(values[1].value)*1000};
    narration.setPacing(next);
  }
  $('slide-pause').addEventListener('change',pacingChanged);$('sentence-pause').addEventListener('change',pacingChanged);
  $('silent-hold').addEventListener('change',()=>{const el=$('silent-hold');if(!el.validity.valid||el.value==='')return;const ms=Number(el.value)*1000;narration.setSilentHold(ms);});
  $('motion-mode').addEventListener('change',()=>{if(view.lesson==='slides')paintEmphasis(narration.snapshot());});
  function setSpeedMenu(open){$('speed-panel').hidden=!open;$('speed').setAttribute('aria-expanded',String(open));if(open){setCaptionMenu(false);setSettings(false);$('speed-panel').querySelector('input:checked').focus();}}
  $('speed').addEventListener('click',()=>setSpeedMenu($('speed-panel').hidden));
  document.querySelectorAll('[name="playback-speed"]').forEach(el=>el.addEventListener('change',()=>{
    if(!el.checked)return;playbackRate=Number(el.value);$('speed').value=el.value;
    narration.setRate(playbackRate);videoNarration.setRate(playbackRate);setSpeedMenu(false);$('speed').focus();
  }));
  function previewPoint(request){
    if(request.owner!==activeTransport())return;
    const card=$('seek-preview'),isSlide=view.lesson==='slides';
    card.hidden=false;card.dataset.kind=isSlide?'slides':'video';
    const width=$('audio-progress').clientWidth;
    card.style.left=CourseSeekPreview.position(request.fraction,width,card.offsetWidth)+'px';
    const label=isSlide?U.progressLabel(data,'slides',request.value).label:U.timeLabel(request.value,request.total);
    $('seek-preview-position').textContent=label;
    if(isSlide){
      seekVideo.close();card.dataset.loading='false';card.dataset.error='false';
      const point=CourseSeekPreview.slidePoint(data.slides,request.value),mode=$('motion-mode').value;
      const clone=document.querySelector('.lesson-slide[data-slide="'+point.slide+'"] svg').cloneNode(true);
      clone.removeAttribute('id');clone.removeAttribute('aria-labelledby');clone.setAttribute('aria-hidden','true');
      clone.querySelectorAll('[id]').forEach(el=>el.removeAttribute('id'));
      clone.removeAttribute('data-follow-cue');clone.removeAttribute('data-progressive');
      if(mode!=='off')clone.setAttribute('data-follow-cue','true');if(mode==='on')clone.setAttribute('data-progressive','true');
      clone.querySelectorAll('[data-emphasis]').forEach(group=>{
        const indices=group.dataset.emphasis.trim()?group.dataset.emphasis.split(' ').map(Number):[];
        const state=CoursePresentation.step(indices,{cue:point.cue,status:'paused',waitMs:null},mode);
        group.setAttribute('data-revealed',String(state.visible));group.setAttribute('data-focused',String(state.focused));
      });
      $('seek-preview-slide').replaceChildren(clone);
      $('seek-preview-caption').textContent=data.slides[point.slide].narration[point.cue].caption;
    }else{
      const scene=data.video_scenes.find(c=>request.value>=c.start&&request.value<c.end);
      $('seek-preview-caption').textContent=scene?.caption||'';
      seekVideo.request(data.video_lesson.src,request.value);
    }
  }
  seekVideo=CourseSeekPreview.createVideo({video:$('seek-preview-video'),
    onPending:()=>{$('seek-preview').dataset.loading='true';$('seek-preview').dataset.error='false';},
    onFrame:()=>{$('seek-preview').dataset.loading='false';},
    onError:()=>{$('seek-preview').dataset.loading='false';$('seek-preview').dataset.error='true';}
  });
  seekController=CourseSeekPreview.create({transport:activeTransport,onPreview:previewPoint,
    onDragging:value=>{scrubbing=value;},onClose:()=>{$('seek-preview').hidden=true;seekVideo.close();}
  });
  function commitScrub(){seekController.commit(Number($('audio-seek').value));refreshCaption();}
  $('audio-seek').addEventListener('pointerdown',e=>{
    if(e.button!==0)return;
    seekController.begin();$('audio-seek').value=activeTransport().snapshot().progress.value;
    $('audio-seek').setPointerCapture?.(e.pointerId);seekController.preview(Number($('audio-seek').value));
  });
  $('audio-seek').addEventListener('input',()=>{
    if(!seekController.isDragging())seekController.begin();
    const value=Number($('audio-seek').value),total=activeTransport().snapshot().progress.total;
    const label=view.lesson==='video'?U.timeLabel(value,total):U.progressLabel(data,'slides',value).label;
    $('audio-time').textContent=label;$('audio-seek').setAttribute('aria-valuetext',label);
    $('audio-seek').style.setProperty('--played',(100*value/total)+'%');seekController.preview(value);
  });
  $('audio-seek').addEventListener('change',commitScrub);
  $('audio-seek').addEventListener('pointerup',commitScrub);
  $('audio-seek').addEventListener('pointermove',e=>{
    if(seekController.isDragging()||e.pointerType==='touch')return;
    const rect=$('audio-seek').getBoundingClientRect(),fraction=Math.max(0,Math.min(1,(e.clientX-rect.left)/rect.width));
    seekController.preview(fraction*activeTransport().snapshot().progress.total);
  });
  $('audio-seek').addEventListener('pointerleave',()=>seekController.hide());
  for(const type of ['pointercancel','blur'])$('audio-seek').addEventListener(type,()=>{seekController.cancel();refreshCaption();});
  $('audio-seek').addEventListener('keydown',e=>{
    if(e.key==='Escape'){if(seekController.isDragging()){e.preventDefault();seekController.cancel();refreshCaption();}else seekController.hide();return;}
    if(!['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','Home','End'].includes(e.key))return;e.preventDefault();
    const s=activeTransport().snapshot(),videoMode=view.lesson==='video',n=e.key==='Home'?0:e.key==='End'?(videoMode?s.progress.total:s.progress.total-1):(videoMode?s.progress.value:s.index)+(['ArrowRight','ArrowUp'].includes(e.key)?1:-1)*(videoMode?5:1);
    seekController.begin();$('audio-seek').value=Math.max(0,Math.min(videoMode?s.progress.total:s.progress.total-1,n));commitScrub();
  });
  window.addEventListener('pagehide',()=>{seekController.cancel(false);remember();narration.stop();videoNarration.stop();$('lesson-video').pause();});
  window.addEventListener('hashchange',applyRoute);
  for(const type of ['pause','ended'])$('lesson-video').addEventListener(type,remember);
  document.addEventListener('click',e=>{
    const link=e.target.closest?.('a[data-home],a[data-enter],a[data-resume]');
    if(!link || e.defaultPrevented || e.button!==0 || e.altKey || e.ctrlKey || e.metaKey || e.shiftKey)return;
    e.preventDefault();
    if(link.hasAttribute('data-home'))home();
    else if(link.hasAttribute('data-resume'))lesson(lastPosition?lastPosition.lesson:'slides',{resume:true});
    else lesson(link.dataset.enter);
  });
  $('prev').addEventListener('click',()=>jump(currentIndex()-1));
  $('next').addEventListener('click',()=>jump(currentIndex()+1));
  document.querySelectorAll('[data-thumb]').forEach(el=>el.addEventListener('click',()=>jump(Number(el.dataset.thumb))));
  document.querySelectorAll('[data-lesson]').forEach(el=>el.addEventListener('click',()=>lesson(el.dataset.lesson)));
  $('next-lesson').addEventListener('click',()=>courseJump(C.LESSONS[C.LESSONS.indexOf(data.lesson_id)+1]));
  $('end-next').addEventListener('click',()=>{state=C.complete(state,progressId(),true);save();home();});
  $('mark-complete').addEventListener('change',()=>{state=C.complete(state,progressId(),$('mark-complete').checked);progress();save();});
  $('menu-toggle').addEventListener('click',()=>{const open=$('toc').classList.toggle('open');$('menu-toggle').setAttribute('aria-expanded',String(open));});
  document.addEventListener('keydown',e=>{if(e.key==='Escape'){$('toc').classList.remove('open');$('menu-toggle').setAttribute('aria-expanded','false');}});
  $('slide-wrap').addEventListener('keydown',e=>{if(e.target!==$('slide-wrap') || e.altKey || e.ctrlKey || e.metaKey)return;if(e.code==='Space'){e.preventDefault();narration.toggle();}else if(['ArrowLeft','ArrowRight'].includes(e.key)){e.preventDefault();jump(view.slide+(e.key==='ArrowRight'?1:-1));}});
  function refreshCaption(){if(view.lesson==='slides')paintPlayback(narration.snapshot());else paintVideoPlayback(videoNarration.snapshot());}
  $('captions-toggle').addEventListener('click',()=>{captionsEnabled=!captionsEnabled;refreshCaption();});
  function setCaptionMenu(open){$('caption-size-panel').hidden=!open;$('caption-size-toggle').setAttribute('aria-expanded',String(open));if(open){setSpeedMenu(false);setSettings(false);$('caption-size-panel').querySelector('input:checked').focus();}}
  $('caption-size-toggle').addEventListener('click',()=>setCaptionMenu($('caption-size-panel').hidden));
  document.querySelectorAll('[name="caption-size"]').forEach(el=>el.addEventListener('change',()=>{if(!el.checked)return;$('stage').dataset.captionSize=el.value;setCaptionMenu(false);$('caption-size-toggle').focus();}));
  function setSettings(open){if(open){setSpeedMenu(false);setCaptionMenu(false);}$('playback-settings').hidden=!open;$('settings-toggle').setAttribute('aria-expanded',String(open));setControl('settings-toggle','settings',open?'재생 설정 닫기':'재생 설정 열기');}
  $('settings-toggle').addEventListener('click',e=>{e.stopPropagation();setSettings($('playback-settings').hidden);});
  function showTranscript(open){transcriptOpen=open;$('transcript-rail').hidden=!open;$('course-layout').classList.toggle('with-transcript',open);$('transcript-toggle').setAttribute('aria-expanded',String(open));setControl('transcript-toggle','transcript',open?'전체 대본 닫기':'전체 대본 열기');if(open)$('rail-title').focus();}
  $('transcript-toggle').addEventListener('click',()=>showTranscript(!transcriptOpen));
  $('transcript-close').addEventListener('click',()=>{showTranscript(false);$('transcript-toggle').focus();});
  document.addEventListener('click',e=>U.dismissOutside(e,[{panel:$('playback-settings'),trigger:$('settings-toggle'),close:()=>setSettings(false)},{panel:$('speed-panel'),trigger:$('speed'),close:()=>setSpeedMenu(false)},{panel:$('caption-size-panel'),trigger:$('caption-size-toggle'),close:()=>setCaptionMenu(false)}]));
  document.addEventListener('keydown',e=>{if(e.key==='Escape'){if(volumePopover.isOpen()){volumePopover.close();}else if(!$('caption-size-panel').hidden){setCaptionMenu(false);$('caption-size-toggle').focus();}else if(!$('speed-panel').hidden){setSpeedMenu(false);$('speed').focus();}else if(!$('playback-settings').hidden){setSettings(false);$('settings-toggle').focus();}else if(transcriptOpen){showTranscript(false);$('transcript-toggle').focus();}}});
  $('fullscreen').addEventListener('click',async()=>{try{setCaptionMenu(false);setSpeedMenu(false);setSettings(false);volumePopover.close();if(document.fullscreenElement)await document.exitFullscreen();else await $('stage').requestFullscreen();}catch(_){$('player-status').textContent='이 브라우저에서는 전체 화면을 사용할 수 없습니다.';}});
  document.addEventListener('fullscreenchange',()=>setControl('fullscreen',document.fullscreenElement?'restore':'fullscreen',document.fullscreenElement?'전체 화면 나가기':'전체 화면'));
  function paintVoiceOptions(s){
    const select=$('browser-voice'),signature=JSON.stringify([s.voices,s.voiceSelection]);
    if(select.dataset.signature!==signature){
      select.replaceChildren();const auto=document.createElement('option');auto.value='';auto.textContent='자동 선택 (기기 기본 우선)';select.append(auto);
      for(const voice of s.voices){const option=document.createElement('option');option.value=voice.id;option.textContent=voice.name+' / '+voice.lang+(voice.default?' / 기기 기본':'');select.append(option);}
      if(s.voiceSelection&&!s.voices.some(v=>v.id===s.voiceSelection)){const missing=document.createElement('option');missing.value=s.voiceSelection;missing.textContent='선택한 음성을 찾지 못했습니다';missing.disabled=true;select.append(missing);}
      select.value=s.voiceSelection;select.dataset.signature=signature;
    }
    document.querySelector('.browser-voice-setting').hidden=s.mode!=='device';
    const reasons={'selected':'직접 선택한 음성입니다.','browser-default':'브라우저가 기본으로 표시한 로컬 한국어 음성입니다.','first-local':'기본으로 표시된 한국어 음성이 없어 목록의 첫 로컬 한국어 음성을 사용합니다.','unavailable':'사용할 수 있는 선택 음성이 없습니다.'};
    $('voice-selection-reason').textContent=reasons[s.voiceOrigin];
  }
  $('browser-voice').addEventListener('change',()=>{try{narration.setVoice($('browser-voice').value);}catch(_){$('player-status').textContent='선택한 로컬 한국어 음성을 사용할 수 없습니다.';}});
  function tab(name) {
    document.querySelectorAll('[data-panel]').forEach(el=>{el.hidden=el.dataset.panel!==name;});
    document.querySelectorAll('[data-tab]').forEach(el=>{const active=el.dataset.tab===name;el.setAttribute('aria-selected',String(active));el.tabIndex=active?0:-1;});
  }
  document.querySelectorAll('[data-tab]').forEach(el=>el.addEventListener('click',()=>tab(el.dataset.tab)));
  $('tabs').addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight','Home','End'].includes(e.key))return;const all=[...$('tabs').querySelectorAll('[data-tab]')];const i=all.indexOf(document.activeElement);if(i<0)return;e.preventDefault();const next=e.key==='Home'?0:e.key==='End'?all.length-1:(i+(e.key==='ArrowRight'?1:-1)+all.length)%all.length;tab(all[next].dataset.tab);all[next].focus();});
  $('grade').addEventListener('click',()=>{
    const answers={};
    document.querySelectorAll('#quiz-form input:checked').forEach(el=>{answers[el.name]=el.value;});
    const result=C.grade(answers,data.questions);
    result.forEach(r=>{
      const feedback=$('feedback-'+r.id);
      feedback.dataset.result=!r.answered?'unanswered':r.correct?'correct':'incorrect';
      feedback.textContent=(!r.answered?'⚠️ 미응답입니다. ':r.correct?'✅ 정답입니다. ':'❌ 오답입니다. ')+r.explanation;
    });
    const correct=result.filter(x=>x.correct).length, unanswered=result.filter(x=>!x.answered).length;
    $('quiz-result').textContent=`✅ 정답 ${correct} · ❌ 오답 ${result.length-correct-unanswered} · ⚠️ 미응답 ${unanswered}`;
  });
  $('memo').addEventListener('input',()=>{state.memos[data.lesson_id]=$('memo').value.slice(0,10000);save();});
  $('export').addEventListener('click',()=>{$('state-json').value=storageBlocked?storedRaw:JSON.stringify(state,null,2);$('save-status').textContent='아래 JSON을 복사해 보관하세요.';});
  $('import').addEventListener('click',()=>{try{state=C.parse($('state-json').value);storageBlocked=false;progress();save();}catch(_){$('save-status').textContent='가져오지 못했습니다. 이 코스의 진도 JSON인지 확인하세요.';}});
  videoNarration=published.includes('video')?NativeVideoPlayer.create({lesson:data.video_lesson,scenes:data.video_scenes,video:$('lesson-video'),initialMuted:true,onChange:paintVideoPlayback,onError:message=>{$('player-status').textContent=message;}}):{stop(){},setMuted(){},setVolume(){},setRate(){},snapshot(){return {time:0};}};
  narration=CourseNarration.create({slides:data.slides,audio:new Audio(),initialMode:data.production_choices.voice==='none'?'silent':'assets',initialMuted:true,pacing,synth:window.speechSynthesis,Utterance:window.SpeechSynthesisUtterance,onChange:paintPlayback});
  if(window.speechSynthesis)window.speechSynthesis.addEventListener('voiceschanged',()=>{narration.refreshVoices();});
  for(const [id,icon,label] of [['prev','prev','이전 장'],['next','next','다음 장'],['play','play','재생'],['captions-toggle','captions','자막 숨기기'],['caption-size-toggle','caption-size','자막 크기 선택'],['mute-toggle','volume-off','음소거 해제'],['transcript-toggle','transcript','전체 대본 열기'],['transcript-close','close','전체 대본 닫기'],['settings-toggle','settings','재생 설정 열기'],['fullscreen','fullscreen','전체 화면']])setControl(id,icon,label);
  $('speed-icon').innerHTML=U.svg('speed');
  document.querySelectorAll('[data-course-jump]').forEach(el=>el.addEventListener('click',e=>{e.preventDefault();courseJump(el.dataset.courseJump);}));
  $('caption-opacity').addEventListener('input',()=>{const v=Math.max(0,Math.min(100,Number($('caption-opacity').value)||0));$('stage').style.setProperty('--caption-opacity',String(v/100));$('caption-opacity-value').value=v+'%';$('caption-opacity-value').textContent=v+'%';});
  window.addEventListener('message',e=>{if(e.source===window.parent&&e.data?.type==='course-enter')lesson(published[0],{resume:true,push:false});});
  render();tab('notes');applyRoute();
})();
