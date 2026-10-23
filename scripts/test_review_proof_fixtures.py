"""Keep review examples executable and distinguish contracts from paired GREEN tests."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReviewProofFixtures(unittest.TestCase):
    def test_fixed_contract_oracles_discriminate_candidate_behaviors(self):
        cases = json.loads((ROOT/'evals/skills/tk-review/review-proof-fixtures.json').read_text())['cases']
        for case in cases:
            for phase in ('baseline', 'candidate'):
                with self.subTest(case=case['id'], phase=phase), tempfile.TemporaryDirectory() as temporary:
                    directory = Path(temporary)
                    for name, content in case[phase+'_files'].items():
                        file = directory/name; file.parent.mkdir(parents=True, exist_ok=True); file.write_text(content)
                    test = subprocess.run(['node', '--test', 'producer.test.mjs'], cwd=directory, text=True, capture_output=True, timeout=15)
                    self.assertEqual(test.returncode, case['expected_'+phase+'_test_exit'], test.stdout+test.stderr)
                    oracle = subprocess.run(['node', '--input-type=module', '-e', case[phase+'_oracle']], cwd=directory, text=True, capture_output=True, timeout=15)
                    self.assertEqual(oracle.returncode, case['expected_'+phase+'_oracle_exit'], oracle.stdout+oracle.stderr)
                    if oracle.returncode:
                        # A valid runtime contract failure, not a syntax/dependency accident.
                        error = 'ERR_MODULE_NOT_FOUND' if case['id'] == 'absence-dynamic-entrypoint' else 'ERR_ASSERTION'
                        self.assertIn(error, oracle.stderr)


if __name__ == '__main__':
    unittest.main()
