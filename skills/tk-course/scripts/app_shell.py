from html import escape as h
from distribution import date_label
from readiness import readiness_html
import re
from pathlib import Path

THEME_CONTROL=(Path(__file__).resolve().parents[1]/'assets/theme-control.html').read_text().strip()
BOOTSTRAP="""try{const t=localStorage.getItem('tigerkit-html-theme');if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t);}catch(_){}"""

def theme_styles(css,root):
    groups={
        'bg':'#0f1115 #101319',
        'panel':'#12151c #181c26 #121824 #172333 #ffffff #fff',
        'hover':'#222a3a #2a3547 #222a3a #1a1f29 #181f2c #1a2e4a #21344e #eaf0f6',
        'line':'#1f2430 #2a3345 #242d3a #232c3a #27303e #344054 #3c4d65 #455970 #222c39 #556881',
        'text':'#e8eaed #f4f7fb #f3f6fb #eaf0f8 #dae4f2 #c4cad6 #bcc9da #b6c3d4 #1e314a',
        'muted':'#aab8ca #8497ae #8190a4 #8b95a7 #879ab2 #77899f #a6b7cf #9faec1 #9fb0c6 #627890 #b7c9e1',
        'accent':'#5793e6 #609dee #4f8ee9 #7bb1fc #6da4f5 #5b9bf3 #9fc7ff #7cb7ff #2d6cdf #3578e5 #5ea0ff #4b87df',
        'good':'#8de1b6 #3a8a4f',
    }
    colors={color:'var(--'+token+')' for token,values in groups.items() for color in values.split()}
    css=re.sub(r'(?<![-\w])(color\s*:\s*)#(?:ffffff|fff)(?=\s*[;}])',r'\1var(--text)',css)
    css=re.sub(r'#[0-9a-fA-F]{3,8}\b',lambda m:colors.get(m[0].lower(),m[0]),css)
    return (root/'html-theme.css').read_text()+'\n'+css+'\n'+(root/'app-shell.css').read_text()

def theme_svg(svg):
    colors={
        '#ffffff':'var(--slide-paper)', '#182a42':'var(--slide-text)',
        '#f1f5fa':'var(--slide-soft)', '#e9eef5':'var(--slide-soft)', '#e9f4ee':'var(--slide-good-bg)',
        '#446991':'var(--slide-muted)', '#596d83':'var(--slide-muted)', '#46607c':'var(--slide-muted)',
        '#d4dce7':'var(--slide-line)', '#e0e6ee':'var(--slide-line)', '#63768b':'var(--slide-muted)',
        '#5579a2':'var(--slide-accent)', '#25835f':'var(--slide-good)', '#fff2dc':'var(--slide-warn-bg)',
        '#875018':'var(--slide-warn)', '#355d8a':'var(--slide-accent)', '#52677d':'var(--slide-muted)', '#61758c':'var(--slide-muted)',
    }
    return re.sub(r'#[0-9a-fA-F]{6}\b',lambda m:colors.get(m[0].lower(),m[0]),svg)

def home_page(data,preview):
    meta=data['course_meta'];overview=data['overview'];items=data['course_lessons']
    dates=date_label(overview)
    date_html='<p class="home-dates">'+h(dates)+'</p>' if dates else ''
    outcomes=''.join('<li>'+h(x)+'</li>' for x in overview['outcomes'])
    curriculum='';section=None
    for n,item in enumerate(items,1):
        if section!=item['section']:
            if section is not None:curriculum+='</details>'
            section=item['section'];curriculum+='<details open><summary>'+h(section)+'</summary>'
        curriculum+='<a class="home-lesson" href="#" data-course-jump="'+item['id']+'"><span class="home-lesson-num">'+str(n).zfill(2)+'</span><span class="home-lesson-title"><strong>'+h(item['title'])+'</strong><small>'+h(item['kind_label'])+'</small></span><span class="home-lesson-status" data-home-status="'+item['id']+'">시작 전</span><span class="home-chevron" aria-hidden="true">›</span></a>'
    curriculum+='</details>'
    curriculum=readiness_html(data.get('readiness',[]))+curriculum
    return f"""<main id="home" aria-labelledby="home-title"><div class="home-hero"><div class="home-copy"><h1 id="home-title" tabindex="-1">{h(data['title'])}</h1><p class="home-description">{h(overview['description'])}</p><div class="course-chips"><span>{h(overview['level'])}</span><span>{len(items)}개 강의</span></div>{date_html}<section class="home-learn"><h2>이 코스에서 배우는 내용</h2><ul>{outcomes}</ul></section></div><aside class="start-card" aria-label="학습 시작과 진도"><div class="home-preview">{preview}</div><div class="start-card-body"><a href="#" id="home-start" data-course-jump="{items[0]['id']}" class="primary-cta"><span id="home-start-label">강의 시작하기</span><span aria-hidden="true">→</span></a><div class="home-progress"><div class="home-progress-line"><span>완료로 표시한 강의</span><strong id="home-progress-label">0 / {len(items)}</strong></div><div class="home-track"><span id="home-fill"></span></div></div></div></aside></div><section class="curriculum" aria-labelledby="curriculum-title"><div class="curriculum-heading"><h2 id="curriculum-title">커리큘럼</h2></div>{curriculum}</section></main>"""
