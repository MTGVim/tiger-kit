/* Playback only. File synthesis belongs to the proposed tk-tts owner. */
(function(root) {
  'use strict';
  function localKoreanVoices(synth) {
    return synth ? synth.getVoices().filter(v=>v.localService===true && /^ko(?:[-_]|$)/i.test(v.lang)) : [];
  }
  function voiceKey(v){return v.voiceURI||v.lang+':'+v.name;}
  function create({slides,audio,synth,Utterance,onChange=()=>{},initialMode='auto',initialMuted=false,initialVolume=1,silentHoldMs=4000,pacing={},clock={now:()=>Date.now(),setTimeout:(fn,ms)=>setTimeout(fn,ms),clearTimeout:id=>clearTimeout(id)}}) {
    const clips=slides.flatMap((s,slide)=>s.narration.map((c,cue)=>({...c,slide,cue})));
    if(!clips.length)throw new Error('missing-narration');
    const hasAssets=clips.every(c=>typeof c.audio==='string' && c.audio.length>0);
    if(clips.some(c=>c.audio) && !hasAssets)throw new Error('partial-narration');
    if(!['auto','assets','device','silent'].includes(initialMode))throw new Error('invalid-mode');
    let mode=initialMode==='auto'?(hasAssets?'assets':'device'):initialMode;
    let index=0,status='idle',rate=1,epoch=0,active=null,voice=null,finishedWhilePaused=false;
    let timer=null,deadline=0,remaining=null,waitKind='slide',freshEntry=true;
    let speechChar=0,boundarySeen=false,pendingSeekFraction=0;
    let silentHold=Number(silentHoldMs);
    if(!Number.isFinite(silentHold)||silentHold<1000||silentHold>15000)throw new Error('invalid-silent-hold');
    if(typeof initialMuted!=='boolean'||!Number.isFinite(initialVolume)||initialVolume<0||initialVolume>1)throw new Error('invalid-volume');
    let muted=initialMuted,volume=initialVolume,deviceQueued=false,mutedBlocked=false,playRequest=0;
    audio.muted=muted;audio.volume=volume;
    let initialLeadInMs=0,postSlideHoldMs=0,slidePauseMs=0,sentencePauseMs=0,preferredVoice='',voiceOrigin='unavailable',voiceOptions=[];
    function available(){return mode==='silent'||(mode==='assets'?hasAssets:!!voice);}
    function silentElapsed(){return active&&active.kind==='silent'?Math.min(silentHold,active.elapsed+(status==='playing'?(clock.now()-active.started)*active.rate:0)):0;}
    function snapshot() {
      const held=(status==='waiting'||status==='paused'&&remaining!==null)&&waitKind==='hold';
      const fraction=status==='ended'||held?1:status==='idle'||status==='blocked'||status==='waiting'||(status==='paused'&&remaining!==null)?0:
        mode==='silent'?(active&&active.kind==='silent'?silentElapsed()/silentHold:pendingSeekFraction):mode==='assets'?(active===audio&&Number.isFinite(audio.duration)&&audio.duration>0?Math.max(0,Math.min(1,(Number(audio.currentTime)||0)/audio.duration)):pendingSeekFraction):
        speechChar/clips[index].speech.length;
      const appliedRate=mode==='device'&&active?active.rate:rate;
      return {index,slide:clips[index].slide,cue:clips[index].cue,status,rate,mode,
        appliedRate,ratePending:rate!==appliedRate,
        muted,volume,mutedBlocked,volumePending:false,
        silentHoldMs:silentHold,progress:{value:status==='ended'?clips.length:index+fraction,total:clips.length,fraction,
          kind:mode==='silent'?'silent':mode==='assets'?'audio':boundarySeen?'boundary':'cue'},
        voice:voice?voice.name:'',voiceSelection:preferredVoice,voiceOrigin,voices:voiceOptions,available:available(),hasAssets,
        waitKind,waitMs:status==='waiting'?Math.max(0,deadline-clock.now()):remaining,
        pacing:{initialLeadInMs,postSlideHoldMs,slidePauseMs,sentencePauseMs},
        time:mode==='assets'&&active===audio?Number(audio.currentTime)||0:null,
        duration:mode==='assets'&&active===audio&&Number.isFinite(audio.duration)?audio.duration:null};
    }
    function emit(){onChange(snapshot());}
    function invalidate() {
      epoch++;active=null;finishedWhilePaused=false;deviceQueued=false;
      if(timer!==null)clock.clearTimeout(timer);timer=null;remaining=null;
      audio.onended=audio.onerror=audio.ontimeupdate=audio.onloadedmetadata=null;
      audio.pause();
      if(synth && mode==='device')synth.cancel();
    }
    function refreshVoices() {
      const voices=localKoreanVoices(synth);
      voiceOptions=voices.map(v=>({id:voiceKey(v),name:v.name,lang:v.lang,default:!!v.default}));
      voice=preferredVoice?voices.find(v=>voiceKey(v)===preferredVoice)||null:voices.find(v=>v.default)||voices[0]||null;
      voiceOrigin=!voice?'unavailable':preferredVoice?'selected':voice.default?'browser-default':'first-local';
      if(status==='blocked' && available())status='idle';
      emit();
    }
    function fail(token) {
      if(token!==epoch)return;
      invalidate();status='error';emit();
    }
    function next(token) {
      if(token!==epoch)return;
      if(status==='paused'){finishedWhilePaused=true;return;}
      if(status!=='playing' && status!=='loading')return;
      const previousSlide=clips[index].slide;
      invalidate();
      speechChar=0;boundarySeen=false;pendingSeekFraction=0;
      if(index===clips.length-1){status='ended';emit();return;}
      status='idle';
      if(clips[index+1].slide!==previousSlide)queue(postSlideHoldMs,'hold');
      else{index++;queue(sentencePauseMs,'sentence');}
    }
    function scheduleSilent(token){
      if(token!==epoch||status!=='playing'||!active||active.kind!=='silent')return;
      const left=Math.max(0,(silentHold-silentElapsed())/rate);
      if(left<=0){next(token);return;}
      timer=clock.setTimeout(()=>{timer=null;if(token!==epoch||status!=='playing')return;if(silentElapsed()>=silentHold)next(token);else{emit();scheduleSilent(token);}},Math.min(100,left));
    }
    function begin(token) {
      if(token!==epoch)return;
      const clip=clips[index];remaining=null;timer=null;
      if(mode==='silent'){
        active={kind:'silent',elapsed:pendingSeekFraction*silentHold,started:clock.now(),rate};pendingSeekFraction=0;
        status='playing';emit();scheduleSilent(token);
      }else if(mode==='assets') {
        audio.src=clip.audio;audio.playbackRate=rate;active=audio;
        audio.currentTime=0;
        status='loading';emit();
        audio.onended=()=>next(token);audio.onerror=()=>fail(token);
        audio.onloadedmetadata=()=>{
          if(token!==epoch)return;
          if(pendingSeekFraction&&Number.isFinite(audio.duration)&&audio.duration>0){audio.currentTime=pendingSeekFraction*audio.duration;pendingSeekFraction=0;}
          emit();
        };
        audio.ontimeupdate=()=>{if(token===epoch)emit();};
        playAudio(token);
      } else {speechChar=0;boundarySeen=false;beginDevice(token);}
    }
    function attemptPlay(){try{return Promise.resolve(audio.play());}catch(error){return Promise.reject(error);}}
    function playAudio(token){
      const request=++playRequest,startedMuted=muted;
      const success=()=>{if(token===epoch&&request===playRequest&&status==='loading'){status='playing';emit();}};
      attemptPlay().then(success).catch(error=>{
        if(token!==epoch||request!==playRequest||!['playing','loading'].includes(status))return;
        if(error?.name==='NotAllowedError'&&!startedMuted){
          mutedBlocked=true;muted=true;audio.muted=true;emit();
          attemptPlay().then(success).catch(()=>{if(request===playRequest&&['playing','loading'].includes(status))fail(token);});
        }else fail(token);
      });
    }
    function beginDevice(token,offset=0,appliedRate=rate,defer=false){
      const clip=clips[index],utterance=new Utterance(clip.speech.slice(offset));
      utterance.lang='ko-KR';utterance.voice=voice;utterance.rate=appliedRate;utterance.volume=muted?0:volume;active=utterance;
      deviceQueued=defer;speechChar=offset;
      utterance.onboundary=event=>{
        if(token!==epoch||status!=='playing'||!Number.isFinite(event.charIndex)||event.charIndex<0)return;
        boundarySeen=true;speechChar=Math.max(speechChar,Math.min(clip.speech.length,offset+event.charIndex));emit();
      };
      utterance.onend=()=>next(token);utterance.onerror=()=>fail(token);
      status=defer?'paused':'playing';emit();
      if(!defer)try{synth.resume();synth.speak(utterance);}catch(_){fail(token);}
    }
    function applyDeviceOutput(previous){
      if(mode!=='device'||!active||finishedWhilePaused||previous===(muted?0:volume))return;
      // Submitted utterance mutations are undefined. Recreate only the remaining text
      // at the last engine boundary; this is not sample-accurate media seeking.
      const offset=speechChar,appliedRate=active.rate,defer=status==='paused';
      const token=++epoch;deviceQueued=false;active=null;synth.cancel();
      beginDevice(token,offset,appliedRate,defer);
    }
    function finishWait(token){
      if(token!==epoch)return;
      timer=null;remaining=null;
      if(waitKind==='hold'){index++;speechChar=0;boundarySeen=false;pendingSeekFraction=0;queue(slidePauseMs,'slide');}
      else begin(token);
    }
    function queue(ms,kind) {
      if(!available()){status='blocked';emit();return;}
      waitKind=kind;
      const token=epoch;
      if(ms===0){finishWait(token);return;}
      status='waiting';deadline=clock.now()+ms;remaining=null;
      timer=clock.setTimeout(()=>finishWait(token),ms);emit();
    }
    function play() {
      if(['playing','loading','waiting'].includes(status))return;
      if(!available()){status='blocked';emit();return;}
      if(status==='paused' && remaining!==null){queue(remaining,waitKind);return;}
      if(status==='paused' && active) {
        if(finishedWhilePaused){status='playing';next(epoch);return;}
        const token=epoch;if(mode==='silent')active.started=clock.now();status='playing';emit();
        if(mode==='silent'){scheduleSilent(token);}
        else if(mode==='assets')playAudio(token);
        else if(deviceQueued){deviceQueued=false;try{synth.resume();synth.speak(active);}catch(_){fail(token);}}
        else synth.resume();
        return;
      }
      if(status==='ended'){index=0;freshEntry=true;}
      const delay=freshEntry?initialLeadInMs:0;freshEntry=false;
      invalidate();queue(delay,'start');
    }
    function pause() {
      if(!['playing','loading','waiting'].includes(status))return;
      if(status==='waiting'){
        remaining=Math.max(0,deadline-clock.now());clock.clearTimeout(timer);timer=null;epoch++;
      }else if(mode==='silent'){active.elapsed=silentElapsed();clock.clearTimeout(timer);timer=null;}
      else if(mode==='assets'){playRequest++;audio.pause();}else synth.pause();
      status='paused';emit();
    }
    function stop() {freshEntry=true;invalidate();speechChar=0;boundarySeen=false;pendingSeekFraction=0;status='idle';emit();}
    function select(slide,cue=0,autoplay=['playing','loading','waiting'].includes(status),fraction=0,initial=false) {
      const found=clips.findIndex(c=>c.slide===slide && c.cue===cue);
      if(found<0)throw new Error('unknown-cue');
      const changed=clips[found].slide!==clips[index].slide;freshEntry=initial;
      invalidate();index=found;speechChar=0;boundarySeen=false;pendingSeekFraction=mode!=='device'?Math.max(0,Math.min(.999,Number(fraction)||0)):0;status='idle';emit();
      if(autoplay)queue(changed?slidePauseMs:sentencePauseMs,changed?'slide':'sentence');
    }
    function setRate(value) {
      value=Number(value);if(![0.75,1,1.25,1.5,2].includes(value))throw new Error('invalid-rate');
      if(mode==='silent'&&active&&active.kind==='silent'){active.elapsed=silentElapsed();active.started=clock.now();active.rate=value;if(timer!==null)clock.clearTimeout(timer);timer=null;}
      rate=value;
      if(mode==='assets')audio.playbackRate=rate;
      // SpeechSynthesis owns the active utterance. Apply at the next natural cue,
      // preserving the current sentence, pause state and visual position.
      emit();if(mode==='silent')scheduleSilent(epoch);
    }
    function setSilentHold(value){
      value=Number(value);if(!Number.isFinite(value)||value<1000||value>15000)throw new Error('invalid-silent-hold');
      if(mode==='silent'&&active){const fraction=silentElapsed()/silentHold;active.elapsed=fraction*value;active.started=clock.now();if(timer!==null)clock.clearTimeout(timer);timer=null;}
      silentHold=value;emit();if(mode==='silent')scheduleSilent(epoch);
    }
    function setMuted(value){
      if(typeof value!=='boolean')throw new Error('invalid-muted');
      const previous=muted?0:volume;muted=value;audio.muted=value;if(!value)mutedBlocked=false;
      applyDeviceOutput(previous);
      emit();
    }
    function setVolume(value){
      value=Number(value);if(!Number.isFinite(value)||value<0||value>1)throw new Error('invalid-volume');
      const previous=muted?0:volume;volume=value;audio.volume=value;
      applyDeviceOutput(previous);
      emit();
    }
    function seekProgress(value) {
      value=Number(value);if(!Number.isFinite(value))throw new Error('invalid-progress');
      const position=Math.max(0,Math.min(clips.length-.000001,value)),target=Math.floor(position),fraction=position-target;
      if(mode==='silent'&&target===index&&active&&active.kind==='silent'){active.elapsed=fraction*silentHold;active.started=clock.now();if(timer!==null)clock.clearTimeout(timer);timer=null;emit();scheduleSilent(epoch);return;}
      if(mode==='assets'&&target===index&&active===audio&&Number.isFinite(audio.duration)&&audio.duration>0){seek(fraction*audio.duration);return;}
      const autoplay=['playing','loading','waiting'].includes(status),clip=clips[target];
      select(clip.slide,clip.cue,autoplay,fraction);
      if(!autoplay){status='paused';emit();}
    }
    function setVoice(id){
      if(typeof id!=='string'||(id && !localKoreanVoices(synth).some(v=>voiceKey(v)===id)))throw new Error('unknown-local-voice');
      invalidate();speechChar=0;boundarySeen=false;pendingSeekFraction=0;preferredVoice=id;status='idle';refreshVoices();
    }
    function setMode(value){
      if(!['assets','device','silent'].includes(value))throw new Error('invalid-mode');
      invalidate();speechChar=0;boundarySeen=false;pendingSeekFraction=0;mode=value;status='idle';emit();
    }
    function setPacing(value){
      if(!value||typeof value!=='object'||Array.isArray(value))throw new Error('invalid-pacing');
      const next={initialLeadInMs,postSlideHoldMs,slidePauseMs,sentencePauseMs,...value};
      if(Object.keys(next).some(k=>!['initialLeadInMs','postSlideHoldMs','slidePauseMs','sentencePauseMs'].includes(k))||!Object.values(next).every(n=>Number.isFinite(n)&&n>=0&&n<=5000))throw new Error('invalid-pacing');
      ({initialLeadInMs,postSlideHoldMs,slidePauseMs,sentencePauseMs}=next);
      emit();
    }
    function seek(seconds) {
      if(mode!=='assets' || !active || !Number.isFinite(audio.duration))return;
      audio.currentTime=Math.max(0,Math.min(audio.duration,Number(seconds)||0));emit();
    }
    setPacing(pacing);refreshVoices();
    return {play,pause,stop,select,setRate,setMuted,setVolume,setSilentHold,setMode,setVoice,setPacing,seek,seekProgress,refreshVoices,snapshot,
      toggle(){if(['playing','loading','waiting'].includes(status))pause();else play();}};
  }
  const api={create,localKoreanVoices};
  if(typeof module==='object' && module.exports)module.exports=api;
  else root.CourseNarration=api;
})(typeof globalThis==='object'?globalThis:this);
