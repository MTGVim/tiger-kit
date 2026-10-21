"""Shared explicit narration choice at media-producing owners; no runtime dispatcher."""
from pathlib import Path
OWNERS=('tk-prep','tk-explain','tk-explain-diff','tk-teach','tk-video','tk-course')
START='<!-- tigerkit:narration-choice -->'
END='<!-- /tigerkit:narration-choice -->'
BLOCK=START+'''
## Narration Choice

Ask the creator to choose TTS, supplied audio or no narration before any video or spoken-slide
production. Reuse an answered parent/user choice; video or a voice preference is not TTS consent.
Show current tk-tts model/voice/device/setup options before synthesis/assembly. Preserve no
narration; offer MP4 for GIF sound. Static HTML/text needs no unrelated voice interview.
Installation/download/publication require their own authority; playback mute/fallback are separate.
'''+END+'\n'

def errors(root:Path):
    result=[]
    for name in OWNERS:
        p=root/'skills'/name/'SKILL.md'
        if not p.is_file():continue
        if p.read_text().count(BLOCK)!=1:result.append(f'{name}: explicit narration choice must match its canonical block exactly once')
    return result

def sync(root:Path):
    for name in OWNERS:
        p=root/'skills'/name/'SKILL.md'
        if not p.is_file():continue
        s=p.read_text()
        if START in s:
            a,rest=s.split(START,1);_,b=rest.split(END,1);s=a+BLOCK.rstrip()+b
        else:
            marker='<!-- tigerkit:artifact-paths -->'
            s=s.replace(marker,BLOCK+'\n'+marker,1) if marker in s else s.rstrip()+'\n\n'+BLOCK
        p.write_text(s)
