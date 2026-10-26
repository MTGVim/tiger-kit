import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/tk-retro/scripts/scan_verbatim.py'
spec = importlib.util.spec_from_file_location('retro_scan', SCRIPT)
scanner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scanner)


class RetroPrivacyTest(unittest.TestCase):
    def test_korean_wording_with_linebreaks_and_repetition_is_found(self):
        phrase = '새 설정을 저장하면 이전 기록이 사라집니다'
        text = f'증상: {phrase}. 예시: {phrase}.'
        result = scanner.scan([text], [phrase.replace(' ', '\n')], [])
        self.assertEqual(result['verbatim_matches'], 2)
        self.assertNotIn(phrase, json.dumps(result, ensure_ascii=False))

    def test_public_exceptions_never_hide_private_identifiers(self):
        value = 'PUBLIC_EXAMPLE_WITH_PRIVATE_SENTINEL'
        result = scanner.scan([value], [value], ['PRIVATE_SENTINEL'], [value])
        self.assertEqual(result['verbatim_matches'], 0)
        self.assertEqual(result['identifier_matches'], 1)

    def test_separate_messages_do_not_create_fictional_shared_runs(self):
        self.assertEqual(scanner.scan(['abcde fghij'], ['abcde', 'fghij'], [])['verbatim_matches'], 0)

    def test_unicode_normalization_and_neutral_control(self):
        import unicodedata
        phrase = '가상의 계정 설정을 다시 불러옵니다'
        self.assertEqual(scanner.scan([phrase], [unicodedata.normalize('NFD', phrase)], [])['verbatim_matches'], 1)
        self.assertEqual(scanner.scan(['일반적인 문서 구성 예시'], [phrase], [])['verbatim_matches'], 0)

    def test_cli_exit_codes_and_redacted_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            evidence, draft = path / 'input.json', path / 'draft.md'
            draft.write_text('PRIVATE_SENTINEL_X', encoding='utf-8')
            evidence.write_text(json.dumps({'messages': ['그림 아래쪽의 이름이 생략되었습니다'],
                                            'terms': ['PRIVATE_SENTINEL_X']}), encoding='utf-8')
            def run():
                return subprocess.run([sys.executable, str(SCRIPT), '--input', str(evidence), str(draft)],
                                      capture_output=True, text=True)
            result = run()
            self.assertEqual(result.returncode, 1)
            self.assertNotIn('PRIVATE_SENTINEL_X', result.stdout + result.stderr)
            draft.write_text('식별자를 제외한 일반 설명입니다', encoding='utf-8')
            self.assertEqual(run().returncode, 0)
            for invalid in ({'messages': [], 'terms': []}, {'messages': ['PRIVATE_SENTINEL_X']},
                            {'messages': 'PRIVATE_SENTINEL_X', 'terms': []}, ['PRIVATE_SENTINEL_X']):
                evidence.write_text(json.dumps(invalid), encoding='utf-8')
                result = run()
                self.assertEqual(result.returncode, 2)
                self.assertNotIn('PRIVATE_SENTINEL_X', result.stdout + result.stderr)
            # The scanner never deletes original evidence or arbitrary caller files.
            self.assertTrue(evidence.exists())


if __name__ == '__main__':
    unittest.main()
