"""Validate local narration and encode build-only copies; keep authored bytes untouched."""
from array import array
import base64,json,math,shutil,subprocess,wave
from pathlib import Path

MIME={'.wav':'audio/wav','.webm':'audio/webm;codecs=opus','.ogg':'audio/ogg;codecs=opus','.mp3':'audio/mpeg','.m4a':'audio/mp4'}

def tool(name):
    path=shutil.which(name)
    if not path:raise ValueError(name+' is required for compressed narration; use --audio-format wav for PCM WAV inputs')
    return path

def inspect_audio(path):
    if path.stat().st_size>500_000_000:raise ValueError('narration exceeds single-file budget; split the course')
    if path.suffix.lower() not in MIME:raise ValueError('unsupported narration format')
    if path.suffix.lower()=='.wav':
        try:
            with wave.open(str(path),'rb') as wav:
                if wav.getnchannels()!=1 or wav.getnframes()<1 or wav.getsampwidth()!=2 or wav.getcomptype()!='NONE':raise ValueError('expected nonempty mono PCM16 narration WAV')
                frames=wav.getnframes();rate=wav.getframerate();pcm=wav.readframes(frames)
                if len(pcm)!=frames*2:raise ValueError('truncated narration WAV')
        except (wave.Error,EOFError) as e:raise ValueError('invalid narration WAV') from e
        duration=frames/rate
    else:
        probe=json.loads(subprocess.run([tool('ffprobe'),'-v','error','-show_format','-show_streams','-of','json',str(path)],check=True,capture_output=True,text=True).stdout)
        streams=probe.get('streams',[])
        if len(streams)!=1 or streams[0].get('codec_type')!='audio':raise ValueError('narration requires one audio stream')
        expected={'.webm':'opus','.ogg':'opus','.mp3':'mp3','.m4a':'aac'}[path.suffix.lower()]
        if streams[0].get('codec_name')!=expected:raise ValueError('narration codec does not match MIME type')
        # Decode the complete stream with error escalation; metadata alone cannot prove valid audio.
        pcm=subprocess.run([tool('ffmpeg'),'-v','error','-xerror','-i',str(path),'-map','0:a:0','-ac','1','-ar','24000','-f','s16le','pipe:1'],check=True,capture_output=True).stdout
        duration=len(pcm)/48000
        reported=float(probe['format'].get('duration',streams[0].get('duration',duration)))
        if not math.isfinite(reported) or abs(reported-duration)>.1:raise ValueError('narration duration differs from decoded audio by more than 0.1 seconds')
    if not math.isfinite(duration) or duration<=0 or not pcm or not any(array('h',pcm)):raise ValueError('silent or empty narration audio')
    return duration

class AudioBuild:
    def __init__(self,base,names,format,directory):
        if format not in {'opus','mp3','wav'}:raise ValueError('unsupported --audio-format')
        self.uris={};self.records=[];self.format=format
        for n,name in enumerate(sorted(set(names))):
            source=base/name;before=inspect_audio(source)
            if format=='wav' and source.suffix.lower()=='.wav':target=source
            else:
                target=Path(directory)/(str(n)+{'opus':'.webm','mp3':'.mp3','wav':'.wav'}[format])
                encoding={'opus':['-c:a','libopus','-b:a','32k','-application','voip'], 'mp3':['-c:a','libmp3lame','-b:a','48k'], 'wav':['-c:a','pcm_s16le']}[format]
                subprocess.run([tool('ffmpeg'),'-v','error','-xerror','-nostdin','-i',str(source),'-map','0:a:0','-ac','1','-ar','24000',*encoding,'-y',str(target)],check=True,capture_output=True)
            after=inspect_audio(target)
            if abs(before-after)>.1:raise ValueError('encoded narration duration drift exceeds 0.1 seconds')
            raw=target.read_bytes();self.uris[name]='data:'+MIME[target.suffix.lower()]+';base64,'+base64.b64encode(raw).decode()
            self.records.append({'source':name,'source_bytes':source.stat().st_size,'encoded_bytes':len(raw),'seconds':round(after,6),'source_seconds':round(before,6)})
    def manifest(self):
        return {'format':self.format,'bitrate':{'opus':32000,'mp3':48000,'wav':None}[self.format], 'source_bytes':sum(x['source_bytes'] for x in self.records),'encoded_bytes':sum(x['encoded_bytes'] for x in self.records),'files':self.records}
