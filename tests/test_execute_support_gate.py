import unittest
from pathlib import Path

import scripts.tigerkit_state as tigerkit_state

ROOT = Path(__file__).resolve().parents[1]
NO_ENV_GATE_TEXT = "current environment entry 검사는 하지 않습니다. 어떤 environment route에서도 execute를 막지 않습니다."


class ExecuteRuntimeWithoutEnvironmentGateTests(unittest.TestCase):
    def test_runtime_module_has_no_environment_gate_helpers(self):
        self.assertFalse(hasattr(tigerkit_state, "validate_environment_support"))
        self.assertFalse(hasattr(tigerkit_state, "current_environment_key"))
        self.assertFalse(hasattr(tigerkit_state, "runtime_binding"))

        source = (ROOT / "scripts/tigerkit_state.py").read_text()
        self.assertNotIn("validate_environment_support(", source)
        self.assertNotIn("current_environment_key(", source)

    def test_execute_docs_explicitly_state_no_environment_gate(self):
        for rel in ["README.md", "commands/execute.md", ".tigerkit/docs/usage.md"]:
            text = (ROOT / rel).read_text()
            self.assertIn(NO_ENV_GATE_TEXT, text)

    def test_execute_contract_still_keeps_loop_spec_checks(self):
        text = (ROOT / "commands/execute.md").read_text()
        self.assertIn("legacy LoopSpec, stale spec, blocked spec, invalid spec은 위임 전에 reject합니다.", text)


if __name__ == "__main__":
    unittest.main()
