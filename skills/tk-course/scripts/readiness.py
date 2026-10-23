"""Optional, transient prerequisite preparation using the native question component."""
from html import escape as h


def validate_readiness(course, identifier, text):
    probes = course.get('readiness', [])
    if not isinstance(probes, list) or len(probes) > 100:
        raise ValueError('readiness must be a bounded list')
    known = {o['id'] for o in course['objectives']}
    seen = set()
    for q in probes:
        if not isinstance(q, dict):
            raise ValueError('invalid readiness question')
        identifier(q['id'])
        if q['id'] in seen:
            raise ValueError('duplicate readiness ID')
        seen.add(q['id'])
        for key in ('title', 'basis', 'prompt', 'explanation', 'preparation'):
            text(q[key])
        if q['confidence'] not in ('confirmed', 'inferred'):
            raise ValueError('readiness confidence must be confirmed or inferred')
        goals = q['objective_ids']
        if not isinstance(goals, list) or not goals or any(not isinstance(x, str) or x not in known for x in goals):
            raise ValueError('readiness requires affected course objectives')
        choices = q['choices']
        if not isinstance(choices, list) or not 2 <= len(choices) <= 6:
            raise ValueError('invalid readiness choices')
        keys = set()
        for choice in choices:
            if not isinstance(choice, list) or len(choice) != 2:
                raise ValueError('invalid readiness choice')
            key, label = choice
            identifier(key); text(label)
            if key in keys:
                raise ValueError('duplicate readiness choice')
            keys.add(key)
        if not isinstance(q['answer'], str) or q['answer'] not in keys:
            raise ValueError('readiness requires one correct choice')
        explanations = q['choice_explanations']
        if not isinstance(explanations, dict) or set(explanations) != keys:
            raise ValueError('readiness requires reasoning for every choice')
        for value in explanations.values():
            text(value)


def question_html(q, prefix=''):
    """Same accessible fieldset, radio choices and answer reveal for both uses."""
    name = prefix + q['id']
    choices = ''.join(f'<label class="choice"><input type="radio" name="{name}" value="{v}"> {h(t)}</label>' for v, t in q['choices'])
    explanation = '<p>' + h(q['explanation']) + '</p>'
    if 'choice_explanations' in q:
        explanation += '<ul>' + ''.join('<li>' + h(label) + ': ' + h(q['choice_explanations'][key]) + '</li>' for key, label in q['choices']) + '</ul>'
    feedback = f'data-readiness-feedback="{q["id"]}"' if prefix else f'id="feedback-{name}"'
    return f'<fieldset><legend>{h(q["prompt"])}</legend>{choices}<p {feedback} role="status"></p><details><summary>해설 보기</summary>{explanation}</details></fieldset>'


def readiness_html(probes):
    if not probes:
        return ''
    cards = ''
    for q in probes:
        status = '확인된 선수지식' if q['confidence'] == 'confirmed' else '추정한 선수지식 · 확인이 필요합니다'
        cards += '<article><h3>' + h(q['title']) + '</h3><p>' + status + '</p><p>' + h(q['basis']) + '</p>'
        cards += question_html(q, 'readiness-')
        cards += '<details><summary>사전 복습</summary><p class="readiness-preparation">' + h(q['preparation']) + '</p></details></article>'
    return '<section id="readiness" class="material-panel" aria-labelledby="readiness-title"><details><summary id="readiness-title">시작 전 선수지식 확인 (선택)</summary><p>필요한 부분을 먼저 복습할 수 있습니다. 응답은 저장·전송되지 않으며 숙련도나 강의 진도로 반영되지 않습니다. 모든 강의를 바로 시작할 수 있습니다.</p>' + cards + '<button type="button" id="readiness-check" data-js-only hidden>응답 확인하기</button><p>복습 항목은 학습 목표에 필요한 순서로 안내합니다. 미응답 항목은 아직 확인하지 않은 상태입니다.</p></details></section>'
