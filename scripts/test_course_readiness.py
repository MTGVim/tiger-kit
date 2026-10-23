"""Readiness remains optional, source-validated and separate from manual progress."""
import copy
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from test_course import fixture, builder, ROOT


def probe():
    return {
        'id': 'completion-order', 'title': 'Promise 완료 순서',
        'basis': '고급 캐싱의 화면 예측은 완료 순서를 전제하며 이 코스는 이를 가르치지 않습니다.',
        'confidence': 'confirmed', 'objective_ids': ['predict'],
        'prompt': 'A 다음 B 요청을 시작했지만 B가 먼저 완료됐습니다. 먼저 완료된 요청은 무엇인가요?',
        'choices': [['a', 'A입니다.'], ['b', 'B입니다.']], 'answer': 'b',
        'explanation': '요청 시작 순서와 완료 순서는 다를 수 있습니다.',
        'choice_explanations': {'a': '먼저 시작한 요청이 먼저 끝난다고 가정했습니다.', 'b': '문제에 주어진 실제 완료 순서를 따릅니다.'},
        'preparation': 'Promise는 시작 순서가 아니라 실제 작업이 끝나는 시점에 완료됩니다. A 시작 → B 시작 → B 완료 → A 완료를 구분해 보세요.'
    }


class ReadinessTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.root = Path(self.tmp.name)
        self.source = self.root/'course.json'; self.data = fixture(); self.write()

    def tearDown(self):
        self.tmp.cleanup()

    def write(self):
        self.source.write_text(json.dumps(self.data, ensure_ascii=False))

    def test_optional_and_reused_component_in_bundle_and_direct_page(self):
        builder.build(self.source, self.root/'plain')
        self.assertNotIn('id="readiness"', (self.root/'plain/lesson-lesson-1.html').read_text())
        self.data['readiness'] = [probe()]
        self.data['readiness'][0]['title'] = '<script>alert(1)</script>'
        self.write(); builder.build(self.source, self.root/'prepared')
        page = (self.root/'prepared/lesson-lesson-1.html').read_text()
        self.assertIn('id="readiness"', page)
        self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt;', page)
        self.assertNotIn('<h3><script>', page)
        self.assertIn('name="readiness-completion-order"', page)
        self.assertIn(probe()['preparation'], page)
        self.assertIn(probe()['choice_explanations']['a'], page)
        self.assertIn('role="status"', page)
        self.assertIn('시작 전 선수지식 확인', (self.root/'prepared/index.html').read_text())
        payload = builder.payload(builder.validate(copy.deepcopy(self.data), self.root), self.data['lessons'][0], self.root)
        self.assertEqual(payload['readiness'], self.data['readiness'])
        self.assertNotIn('readiness', payload['course_meta'])

    def test_invalid_probes_rejected_before_any_output(self):
        invalid = []
        for key, value in [('confidence', 'certain'), ('objective_ids', ['missing']), ('answer', 'other'), ('choice_explanations', {'a': 'one'}), ('preparation', ''), ('choices', [['a', 'one'], ['a', 'two']])]:
            q = probe(); q[key] = value; invalid.append([q])
        invalid.extend([[probe(), probe()], {'unexpected': probe()}])
        for n, probes in enumerate(invalid):
            self.data = fixture(); self.data['readiness'] = probes; self.write()
            with self.subTest(n=n), self.assertRaises((ValueError, KeyError)):
                builder.build(self.source, self.root/f'invalid-{n}')
            self.assertFalse((self.root/f'invalid-{n}').exists())

    def test_inferred_evidence_visible_and_readiness_revision_preserves_lessons(self):
        self.data['readiness'] = [probe()];self.data['readiness'][0]['confidence'] = 'inferred'
        self.write()
        with patch.object(builder, 'build_day', return_value='2026-10-20'):
            builder.build(self.source, self.root/'first')
        original = (self.root/'first/course.json').read_text()
        self.assertIn('추정한 선수지식', (self.root/'first/lesson-lesson-1.html').read_text())
        self.data['readiness'][0]['preparation'] += ' 완료 시점을 시간축에 그려 보세요.';self.write()
        with self.assertRaisesRegex(ValueError, 'course revision'):
            builder.build(self.source, self.root/'bad', self.root/'first/course.json')
        self.data['revision'] = '2';self.write()
        with patch.object(builder, 'build_day', return_value='2026-10-23'):
            builder.build(self.source, self.root/'second', self.root/'first/course.json')
        updated = json.loads((self.root/'second/course.json').read_text())
        self.assertEqual(updated['created_at'], '2026-10-20')
        self.assertEqual(updated['updated_at'], '2026-10-23')
        self.assertEqual([x['status'] for x in json.loads((self.root/'second/changes.json').read_text())], ['retained', 'retained'])
        self.assertEqual((self.root/'first/course.json').read_text(), original)

    @unittest.skipUnless(os.environ.get('TK_PLAYWRIGHT_MODULE') and os.environ.get('TK_CHROMIUM_EXECUTABLE'), 'Readiness file browser checks require a configured installed browser')
    def test_offline_browser_feedback_keyboard_themes_privacy(self):
        self.data['readiness'] = [probe()];self.write();builder.build(self.source, self.root/'browser')
        env = {**os.environ, 'TK_COURSE_PAGE': str(self.root/'browser/index.html'), 'TK_COURSE_DIRECT': str(self.root/'browser/lesson-lesson-1.html')}
        result = subprocess.run(['node', '--test', str(ROOT/'evals/skills/tk-course/readiness.test.cjs')], env=env, capture_output=True, text=True, timeout=120)
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)


if __name__ == '__main__':
    unittest.main()
