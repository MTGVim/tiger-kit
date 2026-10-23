/* A finished video owns picture, sound, captions, pauses and playback time. */
(function(root){
 'use strict';
 function create({lesson,scenes,video,onChange=()=>{},onError=()=>{},initialMuted=false,initialVolume=1}){
  let status='idle',pendingTime=null,epoch=0,mutedBlocked=false;
  video.controls=false;video.muted=initialMuted;video.volume=initialVolume;
  function duration(){return Number.isFinite(video.duration)&&video.duration>0?video.duration:lesson.duration;}
  function position(){return pendingTime===null?Math.max(0,Number(video.currentTime)||0):pendingTime;}
  function snapshot(){
   const time=position(),total=duration();let index=scenes.findLastIndex(s=>time>=s.start);
   if(index<0)index=0;
   const captionActive=time>=scenes[index].start&&time<scenes[index].end;
   return {mode:'video',index,slide:index,cue:0,captionActive,status,rate:video.playbackRate||1,appliedRate:video.playbackRate||1,ratePending:false,
    muted:video.muted,volume:video.volume,mutedBlocked,volumePending:false,available:true,hasAssets:true,
    hasAudio:lesson.has_audio,voice:'',voiceSelection:'',voiceOrigin:'unavailable',voices:[],waitMs:null,
    time,duration:total,progress:{value:time,total,fraction:total?time/total:0,kind:'video'}};
  }
  function emit(){onChange(snapshot());}
  function seek(value){
   const t=Math.max(0,Math.min(duration(),Number(value)||0));
   if(status==='ended'&&t<duration())status='paused';
   if(video.readyState>=1){video.currentTime=t;pendingTime=null;}else pendingTime=t;
   emit();
  }
  function metadata(){if(pendingTime!==null){video.currentTime=Math.min(pendingTime,duration());pendingTime=null;}emit();}
  function attemptPlay(){try{return Promise.resolve(video.play());}catch(error){return Promise.reject(error);}}
  function play(){
   if(['playing','loading'].includes(status))return;
   if(status==='ended')seek(0);
   const token=++epoch;status='loading';emit();
   const success=()=>{if(token===epoch&&status==='loading'){status='playing';emit();}};
   attemptPlay().then(success).catch(error=>{
    if(token!==epoch)return;
    if(error?.name==='NotAllowedError'&&!video.muted){
     mutedBlocked=true;video.muted=true;emit();
     attemptPlay().then(success).catch(()=>failed(token));
    }else failed(token);
   });
  }
  function failed(token){if(token!==epoch)return;status='error';emit();onError('영상을 재생하지 못했습니다.');}

  function pause(){epoch++;video.pause();if(status!=='idle'&&status!=='ended')status='paused';emit();}
  function stop(){epoch++;video.pause();status='idle';emit();}
  function select(index,cue=0,autoplay=['playing','loading'].includes(status)){
   if(!Number.isInteger(index)||index<0||index>=scenes.length)throw new Error('unknown-video-scene');
   const wasPlaying=['playing','loading'].includes(status);seek(scenes[index].start);
   if(autoplay&&!wasPlaying)play();else if(!autoplay)pause();
  }
  video.addEventListener('loadedmetadata',metadata);
  video.addEventListener('durationchange',emit);
  video.addEventListener('timeupdate',emit);
  video.addEventListener('playing',()=>{if(['playing','loading'].includes(status)){status='playing';emit();}});
  video.addEventListener('waiting',()=>{if(status==='playing'){status='loading';emit();}});
  video.addEventListener('pause',()=>{if(!video.ended&&['playing','loading'].includes(status)){epoch++;status='paused';emit();}});
  video.addEventListener('ended',()=>{epoch++;status='ended';emit();});
  video.addEventListener('error',()=>{epoch++;status='error';emit();onError('영상 파일을 읽지 못했습니다.');});
  video.poster=lesson.poster||'';video.src=lesson.src;video.load();
  return {snapshot,play,pause,stop,select,seekProgress:seek,
   toggle(){if(['playing','loading'].includes(status))pause();else play();},
   setRate(value){value=Number(value);if(![.75,1,1.25,1.5,2].includes(value))throw new Error('invalid-rate');video.playbackRate=value;emit();},
   setMuted(value){if(typeof value!=='boolean')throw new Error('invalid-muted');video.muted=value;if(!value)mutedBlocked=false;emit();},
   setVolume(value){value=Number(value);if(!Number.isFinite(value)||value<0||value>1)throw new Error('invalid-volume');video.volume=value;emit();}
  };
 }
 const api={create};if(typeof module==='object'&&module.exports)module.exports=api;else root.NativeVideoPlayer=api;
})(globalThis);
