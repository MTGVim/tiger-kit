"""Data-figure authoring, rendering and offline distribution regressions."""
from __future__ import annotations

import copy
import json
import math
import os
import subprocess
import tempfile
import unittest
import warnings
from html import escape, unescape
from pathlib import Path
from xml.etree import ElementTree as ET

from test_course import fixture, builder, catalog
from components import svg
from slide_components import contract, render, table
from distribution import embedded_manifest


def _slide(id, kind, title, visual, keys, *, greeting=None, role=None, code=None):
    cues=[]
    if greeting:
        cues.append({'id':id+'-hello','speech':greeting,'caption':greeting,'focus':[]})
    for i,key in enumerate(keys,1):
        caption='이제 '+str(i)+'번째 근거에서 조건과 결과를 확인합니다.'
        cues.append({'id':id+'-cue-'+str(i),'speech':caption,'caption':caption,'focus':[key]})
    result={'id':id,'type':kind,'title':title,'eyebrow':'측정과 예측','objective_ids':['predict'],
            'visual':visual,'narration':cues,'transcript':' '.join(c['caption'] for c in cues)}
    if role:result['role']=role
    if code is not None:result['code']=code
    return result


def figure_course():
    """Rich authored fixture shared with real-browser verification."""
    course=fixture('figure-course')
    first,second=course['lessons']
    first['title']='작업자 수와 실행 시간';second['title']='출력에서 원인 찾기'
    axes={'unit':'s','x_label':'Workers','y_label':'Elapsed time',
          'source':'Three-run measurement; reference = 63.2 / workers, excluding overhead'}
    xs=[1,2,4,12]
    line={**axes,'x_unit':'workers','data':[
        {'label':'Measured','points':[{'x':x,'y':y} for x,y in zip(xs,[63.2,34.0,18.8,13.4])]},
        {'label':'Ideal reference','points':[{'x':x,'y':63.2/x} for x in xs]}]}
    output=[' Test Files  4 passed (4)','      Tests  20 passed (20)',
            '   Duration  1.21s (transform 300ms, setup 90ms, tests 110ms)',
            ' details {"tag": "<script>&</script>"}']
    summary={'items':[{'question':'작업자가 늘면 시간은 어떻게 바뀌나요?','answer':'측정 시간은 줄지만 기준선과 차이가 남습니다.'},
                       {'question':'조건과 결과는 어떻게 확인하나요?','answer':'동일한 단위의 원자료와 출력을 함께 비교합니다.'}]}
    first['slides']=[
        _slide('cover','cover',first['title'],{'number':1,'question':'작업자가 열두 명이면 시간도 열두 배 줄까요?'},['title','question'],
               greeting='안녕하세요, 첫 번째 강의입니다.'),
        _slide('line','line','작업자가 늘어도 기준선과 차이가 남습니다',line,['point-1','point-2','point-3','point-4','series-2']),
        _slide('stacked','stacked','전체 시간은 세 단계로 나뉩니다',{'unit':'s','x_label':'Run','y_label':'Stage time','source':'Illustrative breakdown; same run',
            'data':[{'label':'Transform','value':12},{'label':'Setup','value':8},{'label':'Tests','value':20}]},['segment-1','segment-2','segment-3']),
        _slide('bar-vertical','bar','조건별 시간 차이를 비교합니다',{**axes,'data':[{'label':'Before','value':34},{'label':'After','value':18.8}]},['bar-1','bar-2']),
        _slide('bar-horizontal','bar','증감에는 음수와 양수가 함께 있습니다',{**axes,'orientation':'horizontal','data':[{'label':'Saved','value':-8},{'label':'Added','value':3},{'label':'Unchanged','value':0}]},['bar-1','bar-2','bar-3']),
        _slide('output','output','출력 원문에서 실행 시간을 찾습니다',{'source':'Vitest run, supplied terminal capture','data':output},['line-1','line-2','line-3','line-4']),
        _slide('code','code','반영 전에 조건을 확인합니다',{'footnote':'결과 반영 전에 입력 조건을 확인합니다.'},['line-'+str(i) for i in range(1,11)]+['takeaway'],
               code=['const id = 1;','await work();','if (id) {','  compare();','  render();','}', 'const n = 2;','check(n);','save(n);','done();']),
        _slide('timeline','timeline','요청과 응답의 순서를 구분합니다',{'lanes':['Client','Worker','Store'],
            'events':[{'lane':i%3,'label':label} for i,label in enumerate(['Request A','Start A','Read A','Request B','Result B','Commit B'])],
            'callout':'배열의 순서는 사건 순서이며 실제 소요 시간이 아닙니다.'},['event-'+str(i) for i in range(1,7)]+['callout']),
        _slide('hook','hook','세 근거로 조건을 점검합니다',{'title_lines':['출력과 측정을 함께 봅니다'],
            'cards':[{'label':'첫 측정','value':'63.2 seconds measured'},{'label':'최신 측정','value':'13.4 seconds measured'},{'label':'해석 조건','value':'same input, same machine'}],
            'question':'어떤 조건에서 결과를 비교할 수 있나요?'},['card-1','card-2','card-3']),
        _slide('map','course-map','다음에는 출력에서 원인을 찾습니다',{'lessons':[first['title'],second['title']],'current':1},['lesson-1','lesson-2']),
        _slide('summary','summary','측정과 기준선을 함께 비교합니다',summary,['answer-1','answer-2'],role='summary')]
    second['slides']=[
        _slide('opening-output','output','앞서 본 시간을 출력과 연결합니다',{'source':'Vitest run, supplied terminal capture','data':output[:3]},['line-1','line-2','line-3'],
               greeting='안녕하세요, 두 번째 강의입니다.'),
        _slide('closing-summary','summary','원자료로 예측의 근거를 정리합니다',summary,['answer-1','answer-2'],role='closing')]
    course['preview_slide']={'lesson_id':'lesson-1','slide_id':'line'}
    def cue(id,caption,focus):return {'id':id,'caption':caption,'speech':caption,'focus':focus}
    first['slides'][0]['narration'][1:1]=[
        cue('course-setup','같은 입력과 컴퓨터에서 작업자 수만 바꿀 테스트 프로젝트를 준비해 주세요.',['title']),
        cue('first-goal','이번 강의를 마치면 측정 시간과 이상적 기준선의 차이를 설명할 수 있습니다.',['question'])]
    second['slides'][0]['narration'][1:1]=[
        cue('second-connection','지난 강의에서는 작업자를 늘려도 기준선과 차이가 남는 것을 보았습니다.',['line-1']),
        cue('second-goal','이번에는 실행 출력의 시간을 읽고 어느 단계부터 점검할지 판단해 봅시다.',['line-2'])]
    for lesson in course['lessons']:
        for slide in lesson['slides']:slide['transcript']=' '.join(c['caption'] for c in slide['narration'])
    for lesson,text in [(first,'다음 강의에서는 실행 출력에서 어느 단계에 시간이 들었는지 찾아보겠습니다.'),(second,'우리 함께 측정과 원자료로 판단하는 과정을 마쳤으니 다른 프로젝트에도 적용해 보세요.')]:
        last=lesson['slides'][-1];last['narration'].append(cue(lesson['id']+'-farewell',text,['answer-2']));last['transcript']=' '.join(c['caption'] for c in last['narration'])
    return course


NS={'s':'http://www.w3.org/2000/svg'}
def parsed(slide,compact=False):return ET.fromstring(render(slide,0,compact))
def focus_group(root,key):return next(e for e in root.iter() if e.get('data-focus-key')==key)
def text_content(root):return ''.join(root.itertext())


class FigureTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.data=figure_course();self.source=self.root/'course.json'
    def tearDown(self):self.tmp.cleanup()
    def slide(self,id):return next(s for l in self.data['lessons'] for s in l['slides'] if s['id']==id)
    def build(self,name='built'):
        self.source.write_text(json.dumps(self.data,ensure_ascii=False))
        return builder.build(self.source,self.root/name)
    def reject(self,change):
        self.data=figure_course();change(self.data)
        with self.assertRaises(ValueError):self.build('invalid')
        self.assertFalse((self.root/'invalid').exists())

    def test_rich_authored_course_builds_without_plot_warnings(self):
        with warnings.catch_warnings(record=True) as captured:
            warnings.simplefilter('always');self.build()
        self.assertEqual(captured,[])
        for lesson in self.data['lessons']:
            for slide in lesson['slides']:
                self.assertEqual(slide['transcript'],' '.join(c['caption'] for c in slide['narration']))
                for compact in (False,True):parsed(slide,compact)
        self.assertEqual(self.slide('cover')['narration'][0]['focus'],[])

    @unittest.skipUnless(os.environ.get('TK_PLAYWRIGHT_MODULE') and os.environ.get('TK_CHROMIUM_EXECUTABLE'),'Configured local browser required')
    def test_figures_in_actual_browser(self):
        from PIL import Image,ImageDraw
        im=Image.new('RGB',(800,450),'#eceff3');draw=ImageDraw.Draw(im)
        draw.rectangle((80,90,320,225),fill='#4c8c62');draw.rectangle((480,90,720,225),fill='#a35b58')
        from PIL import ImageFont
        font=ImageFont.truetype('DejaVuSans.ttf',54)
        draw.text((90,110),'OPEN',font=font,fill='white');draw.text((490,110),'STOP',font=font,fill='white');im.save(self.root/'layout.png')
        self.data['lessons'][0]['slides'].insert(-1,_slide('observed-layout','image','Compare the open and blocked routes',{
            'src':'layout.png','alt':'An open left route and a blocked right route',
            'description':'Open vs blocked',
            'source':'Original synthetic layout for this regression test','rights':'Original test figure; redistribution permitted',
            'regions':[{'id':'open','label':'Open left','x':.1,'y':.2,'width':.3,'height':.3}]},['image','region-open']))
        self.data['lessons'][0]['notes']+='\nLong document notes remain independently scrollable.'*120
        self.build('browser')
        env={**os.environ,'TK_FIGURE_PAGE':str(self.root/'browser/index.html')}
        video_pages=[]
        for label,dimensions in [('wide','640x180'),('standard','320x240'),('portrait','180x320')]:
            movie=self.root/(label+'.mp4')
            subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=c=steelblue:s='+dimensions+':d=4','-an','-c:v','libx264',str(movie)],check=True)
            course=fixture('video-'+label);lesson=course['lessons'][0];lesson.pop('slides');lesson['kind']='video';lesson['video']={'src':movie.name,'narration':'none','captions':[{'id':'video-cue','start':0,'end':4,'caption':'화면을 확인합니다.'}]}
            source=self.root/(label+'.json');source.write_text(json.dumps(course));builder.build(source,self.root/('video-'+label));video_pages.append(str(self.root/('video-'+label)/'index.html'))
        env['TK_VIDEO_PAGES']=json.dumps(video_pages)
        tests=Path(__file__).resolve().parents[1]/'evals/skills/tk-course'
        result=subprocess.run(['node','--test','--test-concurrency=1',str(tests/'figures.test.cjs'),str(tests/'media-layout.test.cjs')],env=env,capture_output=True,text=True,timeout=330)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)

    def test_fixed_canvas_for_all_components_and_regions(self):
        for lesson in self.data['lessons']:
            for slide in lesson['slides']:
                for compact in (False,True):
                    with self.subTest(slide=slide['id'],compact=compact):
                        root=parsed(slide,compact)
                        self.assertEqual(list(map(float,root.get('viewBox').split())),[0,0,1600,900])
                        for e in root.iter():
                            if e.tag.rsplit('}',1)[-1] in {'rect','image'}:
                                x,y,w,h=[float(e.get(k,'0')) for k in ('x','y','width','height')]
                                self.assertGreaterEqual(x,0);self.assertGreaterEqual(y,0)
                                self.assertLessEqual(x+w,1600.01);self.assertLessEqual(y+h,900.01)

    def test_overfull_rows_require_meaningful_splitting_before_output(self):
        slide=self.slide('timeline');slide['visual']['events']*=2
        # Even still within the public maximum, a dense physical layout may fail.
        slide['visual']['events']=slide['visual']['events'][:8]
        slide['narration'][0]['focus']+=['event-7','event-8']
        self.source.write_text(json.dumps(self.data))
        with self.assertRaisesRegex(ValueError,'slide timeline: timeline events/callout.*split'):
            builder.build(self.source,self.root/'overfull')
        self.assertFalse((self.root/'overfull').exists())

    def test_invalid_numbers_and_missing_units_fail_before_writing(self):
        for bad in [float('nan'),float('inf'),float('-inf'),True,'34',10**13]:
            with self.subTest(value=bad):
                self.reject(lambda c:c['lessons'][0]['slides'][1]['visual']['data'][0]['points'][0].update(y=bad))
        self.reject(lambda c:c['lessons'][0]['slides'][1]['visual'].pop('unit'))
        self.reject(lambda c:c['lessons'][0]['slides'][1]['visual'].pop('x_unit'))

    def test_coverage_and_focus_references_are_semantic(self):
        self.reject(lambda c:c['lessons'][0]['slides'][1]['narration'][-1].update(focus=['series-1']))
        self.reject(lambda c:c['lessons'][0]['slides'][1]['narration'][0].update(focus=['point-99']))
        for id in ['output','code']:
            for lines in [['x']*13,['x'*101],['x'*100]*12]:
                with self.subTest(component=id,lines=len(lines)):
                    self.data=figure_course();slide=self.slide(id)
                    if id=='code':slide['code']=lines
                    else:slide['visual']['data']=lines
                    with self.assertRaises(ValueError):self.build('oversized')
                    self.assertFalse((self.root/'oversized').exists())

    def test_numeric_series_must_remain_comparable_and_stacks_have_a_total(self):
        for change in [
            lambda v:v['data'][0]['points'][1].update(x=1),
            lambda v:v['data'][1]['points'][1].update(x=3),
            lambda v:v['data'][0]['points'][0].update(x=True),
        ]:
            with self.subTest(change=change):
                self.reject(lambda c:change(c['lessons'][0]['slides'][1]['visual']))
        for values in [[0,0,0],[-1,2,3],[True,2,3],['1',2,3]]:
            self.data=figure_course();slide=self.slide('stacked')
            for item,value in zip(slide['visual']['data'],values):item['value']=value
            with self.subTest(values=values),self.assertRaises(ValueError):self.build('bad-stack')
            self.assertFalse((self.root/'bad-stack').exists())

    def test_code_and_output_soft_wraps_preserve_every_original_character(self):
        for id in ['code','output']:
            slide=copy.deepcopy(self.slide(id))
            lines=slide['code'] if id=='code' else slide['visual']['data']
            lines[1]=''
            contract(slide)
            for compact in (False,True):
                root=parsed(slide,compact)
                for i,line in enumerate(lines,1):
                    group=focus_group(root,'line-'+str(i))
                    fragments=[e.text or '' for e in group.findall('s:text',NS) if e.get('font-family')=='monospace']
                    self.assertEqual(''.join(fragments),line)
                    self.assertEqual(group.find('s:text',NS).text,str(i))
                self.assertFalse(root.findall('.//s:foreignObject',NS))

    def test_real_x_spacing_and_reference_distinction(self):
        slide=self.slide('line')
        for compact in (False,True):
            root=parsed(slide,compact)
            marks=[focus_group(root,'point-'+str(i)).find('s:circle',NS) for i in range(1,5)]
            xs=[float(e.get('cx')) for e in marks];dx=[b-a for a,b in zip(xs,xs[1:])]
            self.assertAlmostEqual(dx[1]/dx[0],2,places=4)
            self.assertAlmostEqual(dx[2]/dx[0],8,places=4)
            ref=focus_group(root,'series-2').find('s:path',NS)
            self.assertTrue(ref.get('stroke-dasharray'))
            self.assertIsNotNone(focus_group(root,'point-5').find('s:rect',NS))
            for i in range(5,9):self.assertEqual(focus_group(root,'point-'+str(i)).get('data-emphasis'),'4')

    def test_bars_include_zero_and_have_finite_geometry(self):
        for orientation in ['vertical','horizontal']:
            for values in [[0,0],[-8,3],[7,7],[-4,-4]]:
                with self.subTest(orientation=orientation,values=values):
                    slide=copy.deepcopy(self.slide('bar-vertical'))
                    slide['visual'].update(orientation=orientation,data=[{'label':str(i),'value':v} for i,v in enumerate(values)])
                    contract(slide)
                    for compact in (False,True):
                        root=parsed(slide,compact)
                        for e in root.iter():
                            for attr in ['x','y','width','height','cx','cy']:
                                if e.get(attr) is not None:self.assertTrue(math.isfinite(float(e.get(attr))))
                        for i,value in enumerate(values,1):
                            mark=focus_group(root,'bar-'+str(i)).find('s:rect',NS)
                            length=float(mark.get('width' if orientation=='horizontal' else 'height'))
                            self.assertGreaterEqual(length,0)
                            if value==0:self.assertEqual(length,0)

    def test_focus_groups_own_complete_cards_and_escape_svg(self):
        slide=self.slide('hook');slide['visual']['cards'][0]={'label':'<label>&','value':'value <tag> & "quoted"'}
        for compact in (False,True):
            root=parsed(slide,compact);group=focus_group(root,'card-1')
            self.assertIsNotNone(group.find('s:rect',NS))
            self.assertIn('<label>&',text_content(group));self.assertIn('value <tag> & "quoted"',text_content(group))
            self.assertEqual(group.get('data-emphasis'),'0')
            self.assertFalse(any(e.tag.endswith('script') or e.tag.endswith('tag') for e in root.iter()))

    def test_original_tables_and_output_survive_notes_and_no_script(self):
        self.build();page=(self.root/'built/index.html').read_text()
        fallback=page.split('<noscript>',1)[1].split('</noscript>',1)[0]
        lesson=(self.root/'built/lesson-lesson-1.html').read_text()
        for id in ['line','bar-horizontal','stacked','output','code']:
            original=table(self.slide(id));self.assertIn(original,fallback);self.assertIn(original,lesson)
        self.assertIn(str(63.2/12),table(self.slide('line')))
        output='\n'.join(self.slide('output')['visual']['data'])
        self.assertIn(escape(output),fallback)
        self.assertNotIn('<script>&</script>',fallback)
        self.assertEqual(unescape(table(self.slide('output')).split('>',1)[1].rsplit('</pre>',1)[0]),output)

    def test_legacy_aliases_cover_actual_rendered_lines_and_cards(self):
        code=self.slide('code');code['code']=code['code'][:6]
        code['narration']=[{'id':'legacy-code','speech':'조건을 확인합니다.','caption':'조건을 확인합니다.','focus':['request-id','await','compare','render','takeaway']}]
        code['transcript']='조건을 확인합니다.'
        timeline=self.slide('timeline');timeline['visual'].update(lanes=['Client','Server'],events=['Request A','Request B','Result B','Result A'])
        timeline['narration']=[{'id':'legacy-events','speech':'순서를 확인합니다.','caption':'순서를 확인합니다.','focus':['request-a','request-b','response-b','response-a','overwrite']}];timeline['transcript']='순서를 확인합니다.'
        hook=self.slide('hook');hook['visual']['cards']=hook['visual']['cards'][:2]
        hook['narration']=[{'id':'legacy-cards','speech':'두 값을 비교합니다.','caption':'두 값을 비교합니다.','focus':['first-search','latest-search']}];hook['transcript']='두 값을 비교합니다.'
        self.build()
        for slide,keys in [(code,['line-'+str(i) for i in range(1,7)]+['takeaway']), (timeline,['event-'+str(i) for i in range(1,5)]+['callout']),(hook,['card-1','card-2'])]:
            for compact in (False,True):
                root=parsed(slide,compact)
                for key in keys:self.assertEqual(focus_group(root,key).get('data-emphasis'),'0')

    def test_explicit_preview_uses_selected_visual_without_media(self):
        selected=self.slide('line');selected['narration'][0]['audio']='voice.wav'
        self.data['narration_seconds']=0
        tag=embedded_manifest(self.data)
        manifest=json.loads(tag.split('>',1)[1].rsplit('</script>',1)[0])
        preview=manifest['preview_slide']
        self.assertEqual(preview['type'],'line');self.assertEqual(preview['visual'],selected['visual'])
        self.assertNotIn('voice.wav',json.dumps(preview));self.assertFalse(any(c.get('audio') for c in preview.get('narration',[])))
        self.assertIn(selected['title'],text_content(ET.fromstring(catalog.preview(manifest,0))))
        for ref in [{'lesson_id':'missing','slide_id':'line'},{'lesson_id':'lesson-1','slide_id':'missing'},{'slide_id':'line'}]:
            with self.subTest(ref=ref):self.reject(lambda c:c.update(preview_slide=ref))

    def test_optional_lesson_forms_do_not_generate_formula_warnings(self):
        self.data['lessons'][0]['slides'][-1].pop('role')
        opening=copy.deepcopy(self.slide('cover'));opening['id']='second-cover'
        for cue in opening['narration']:cue['id']='second-'+cue['id']
        self.data['lessons'][1]['slides'].insert(0,opening)
        with warnings.catch_warnings(record=True) as captured:
            warnings.simplefilter('always');self.build()
        messages=' '.join(str(w.message) for w in captured)
        self.assertEqual(messages,'')
        self.assertTrue((self.root/'built/index.html').is_file())


if __name__=='__main__':unittest.main()

class TeachingImageTests(unittest.TestCase):
    def setUp(self):
        from PIL import Image,ImageDraw
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        im=Image.new('RGB',(800,450),'#eeeeee');d=ImageDraw.Draw(im);d.rectangle((80,90,320,270),fill='#5da969');d.rectangle((480,90,720,270),fill='#a25c5c');im.save(self.root/'layout.png')
        self.data=fixture('image-course');s=self.data['lessons'][0]['slides'][0]
        s.update(type='image',visual={'src':'layout.png','alt':'Two routes with a visible boundary','description':'Open vs blocked','source':'Synthetic layout, authored for this test','rights':'Original test illustration; redistribution permitted','regions':[{'id':'open','label':'Open route','x':.1,'y':.2,'width':.3,'height':.4}]})
        s['narration'][0]['focus']=['image','region-open'];self.slide=s
    def tearDown(self):self.tmp.cleanup()
    def test_safe_offline_image_and_actual_aspect_ratio_with_no_source_mutation(self):
        from PIL import Image
        Image.new('RGB',(600,600),'white').save(self.root/'layout.png')
        builder.validate(copy.deepcopy(self.data),self.root)
        runtime=builder.payload(self.data,self.data['lessons'][0],self.root)
        image=runtime['slides'][0]
        self.assertTrue(image['visual']['src'].startswith('data:image/png;base64,'));self.assertEqual(image['visual']['aspect_ratio'],1)
        markup=svg(0,image,responsive=True);self.assertIn('data-focus-key="region-open"',markup);self.assertIn('Open route',markup);self.assertIn('redistribution permitted',table(image))
        self.assertEqual(self.slide['visual']['src'],'layout.png')
        source=self.root/'course.json';source.write_text(json.dumps(self.data));builder.build(source,self.root/'built')
        page=(self.root/'built/index.html').read_text();self.assertIn('data:image/png;base64,',page)
        fallback=page.split('<noscript>')[1].split('</noscript>')[0];self.assertIn('<image ',fallback)
        from distribution import read_manifest
        manifest=read_manifest(self.root/'built/index.html');self.assertNotIn('layout.png',json.dumps(manifest))
    def test_png_jpeg_webp_build_without_pillow_and_reject_truncated_or_mismatched_bytes(self):
        import sys
        from PIL import Image
        for suffix,codec in [('png','PNG'),('jpg','JPEG'),('webp','WEBP')]:
            path=self.root/('screen.'+suffix)
            Image.new('RGB',(800,450),'#5b8aaa').save(path,format=codec)
            self.slide['visual']['src']=path.name
            source=self.root/'course.json';source.write_text(json.dumps(self.data))
            # -S excludes site packages (including Pillow) from the actual builder process.
            result=subprocess.run([sys.executable,'-S',str(builder.__file__),'--input',str(source),'--output',str(self.root/('built-'+suffix)),'--audio-format','wav','--dist',str(self.root/('dist-'+suffix))],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            entry=Path(json.loads(result.stdout)['path']);self.assertNotIn('data:image/',entry.read_text())
            self.assertIn('../assets/image/',(entry.parent/'lessons/lesson-lesson-1.html').read_text())
            self.assertEqual(len(list((entry.parent/'assets/image').iterdir())),1)
            (self.root/'wrong.png').write_bytes(path.read_bytes() if suffix!='png' else b'not an image')
            with self.assertRaises(ValueError):builder.image_info(self.root,'wrong.png')
            (self.root/('cut.'+suffix)).write_bytes(path.read_bytes()[:len(path.read_bytes())//2])
            with self.assertRaises(ValueError):builder.image_info(self.root,'cut.'+suffix)
        for cut in (1,2,4):
            (self.root/'no-eoi.jpg').write_bytes((self.root/'screen.jpg').read_bytes()[:-cut])
            with self.assertRaisesRegex(ValueError,'JPEG ending'):builder.image_info(self.root,'no-eoi.jpg')
        (self.root/'padded.jpg').write_bytes((self.root/'screen.jpg').read_bytes()+b'padding')
        self.assertAlmostEqual(builder.image_info(self.root,'padded.jpg'),800/450)
        (self.root/'no-iend.png').write_bytes((self.root/'screen.png').read_bytes()[:-12])
        with self.assertRaisesRegex(ValueError,'PNG ending'):builder.image_info(self.root,'no-iend.png')
        Image.new('RGB',(17000,1)).save(self.root/'large.png')
        with self.assertRaisesRegex(ValueError,'oversized'):builder.image_info(self.root,'large.png')
        from unittest.mock import patch
        with patch.object(builder.shutil,'which',return_value=None):
            with self.assertRaisesRegex(ValueError,'ffprobe and ffmpeg'):builder.image_info(self.root,'screen.png')
            builder.validate(fixture(),self.root)
        with patch.object(builder.subprocess,'run',side_effect=subprocess.TimeoutExpired('ffprobe',15)):
            with self.assertRaisesRegex(ValueError,'timed-out'):builder.image_info(self.root,'screen.png')

    def test_hook_repeated_title_is_rendered_once_and_distinct_emphasis_remains(self):
        slide=figure_course()['lessons'][0]['slides'][8]
        slide['visual']['title_lines']=[slide['title'],'Distinct teaching point']
        root=parsed(slide);texts=[e.text for e in root.findall('.//s:text',NS)]
        self.assertEqual(texts.count(slide['title']),1);self.assertIn('Distinct teaching point',texts)
        slide['title']='Where should we look?';slide['visual']['title_lines']=['Where should','we look?']
        self.assertEqual(sum((e.text or '').count('Where should') for e in parsed(slide).findall('.//s:text',NS)),1)

    def test_tall_two_panel_composite_rejected_and_separate_scene_assets_pass(self):
        from PIL import Image,ImageDraw
        im=Image.new('RGB',(1600,2704),'white');draw=ImageDraw.Draw(im)
        draw.rectangle((50,50,1550,1250),outline='black',width=10)
        draw.rectangle((50,1350,1550,2550),outline='black',width=10)
        draw.text((80,2600),'Long provenance / detailed legend',fill='black')
        im.save(self.root/'layout.png')
        self.data['lessons'][0]['notes']='Full source and rights.\n'*150
        source=self.root/'course.json';source.write_text(json.dumps(self.data))
        with self.assertRaisesRegex(ValueError,'slide slide-1: image region.*split'):
            builder.build(source,self.root/'rejected')
        self.assertFalse((self.root/'rejected').exists())
        # Explicit source reauthoring keeps both states and remaps semantic cues.
        for name,color in [('before.png','#5da969'),('after.png','#a25c5c')]:
            panel=Image.new('RGB',(800,450),'white');ImageDraw.Draw(panel).rectangle((80,90,320,270),fill=color);panel.save(self.root/name)
        before=copy.deepcopy(self.slide);after=copy.deepcopy(self.slide)
        before['visual']['src']='before.png';after['id']='after-state';after['visual']['src']='after.png'
        before['visual']['description']='Route open';after['visual']['description']='Route blocked'
        after['narration'][0]['id']='after-cue'
        self.data['lessons'][0]['slides']=[before,after];source.write_text(json.dumps(self.data))
        builder.build(source,self.root/'split')
        for slide in [before,after]:
            runtime=copy.deepcopy(slide);runtime['visual']['aspect_ratio']=16/9
            root=parsed(runtime);self.assertEqual(root.get('viewBox'),'0 0 1600 900')
            image=root.find('.//s:image',NS)
            self.assertAlmostEqual(float(image.get('width'))/float(image.get('height')),16/9,places=5)
        self.assertEqual(before['visual']['regions'],after['visual']['regions'])
        self.assertIn(self.slide['visual']['rights'],(self.root/'split/index.html').read_text())

    def test_missing_unsafe_symlink_corrupt_and_unsupported_images_fail_before_build(self):
        (self.root/'bad.svg').write_text('<svg/>');(self.root/'corrupt.png').write_text('not an image');(self.root/'link.png').symlink_to(self.root/'layout.png')
        for name in ['missing.png','../layout.png','/etc/passwd','link.png','bad.svg','corrupt.png']:
            with self.subTest(name=name):
                data=copy.deepcopy(self.data);data['lessons'][0]['slides'][0]['visual']['src']=name
                with self.assertRaises((ValueError,OSError)):builder.validate(data,self.root)
    def test_description_source_rights_and_cue_region_coverage_are_required(self):
        for field in ['alt','description','source','rights']:
            data=copy.deepcopy(self.data);del data['lessons'][0]['slides'][0]['visual'][field]
            with self.subTest(field=field),self.assertRaises(ValueError):builder.validate(data,self.root)
        for mutation in ['missing-focus','outside','duplicate']:
            data=copy.deepcopy(self.data);s=data['lessons'][0]['slides'][0]
            if mutation=='missing-focus':s['narration'][0]['focus']=['image']
            if mutation=='outside':s['visual']['regions'][0]['width']=1
            if mutation=='duplicate':s['visual']['regions']*=2
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):builder.validate(data,self.root)
    def test_same_path_image_bytes_require_revision_and_pacing_only_rebuild_retains_content(self):
        from PIL import Image
        source=self.root/'course.json';source.write_text(json.dumps(self.data));builder.build(source,self.root/'first')
        self.data['pacing']={'initialLeadInMs':5000,'postSlideHoldMs':1800,'slidePauseMs':1200,'sentencePauseMs':600};source.write_text(json.dumps(self.data))
        builder.build(source,self.root/'paced',self.root/'first/course.json')
        changes=json.loads((self.root/'paced/changes.json').read_text());self.assertTrue(all(c['status']=='retained' for c in changes))
        Image.new('RGB',(800,450),'yellow').save(self.root/'layout.png')
        with self.assertRaisesRegex(ValueError,'revision'):builder.build(source,self.root/'rejected',self.root/'first/course.json')
        self.data['lessons'][0]['revision']='2';source.write_text(json.dumps(self.data));builder.build(source,self.root/'updated',self.root/'first/course.json')
        changes=json.loads((self.root/'updated/changes.json').read_text());self.assertEqual([c['status'] for c in changes],['changed','retained'])
    def test_pacing_defaults_legacy_zero_and_bad_types(self):
        self.assertEqual(builder.course_pacing(self.data),{'initialLeadInMs':5000,'postSlideHoldMs':1800,'slidePauseMs':1200,'sentencePauseMs':600})
        legacy=builder.course_pacing({'pacing':{'slidePauseMs':0,'sentencePauseMs':0}});self.assertEqual(legacy,dict.fromkeys(legacy,0))
        for bad in [{'initialLeadInMs':True},{'postSlideHoldMs':-1},{'slidePauseMs':'0'},{'sentencePauseMs':float('nan')},{'typo':1},[]]:
            with self.subTest(bad=bad),self.assertRaises(ValueError):builder.course_pacing({'pacing':bad})
