import unittest
from unittest.mock import patch

import scripts.tigerkit_state as tigerkit_state

PLUGIN_VERSION = "16.2.1"


class ValidateEnvironmentSupportTests(unittest.TestCase):
    def test_preview_environment_is_allowed_without_capability_proof(self):
        with patch.object(
            tigerkit_state,
            "support_matrix",
            return_value={
                "pluginVersion": PLUGIN_VERSION,
                "environments": [
                    {
                        "environmentKey": "claude-code/linux/local/default",
                        "status": "preview",
                        "boundaryArchitecture": "hook_gate",
                        "boundaryComponents": ["hooks/hooks.json"],
                    }
                ],
            },
        ), patch.object(
            tigerkit_state,
            "current_environment_key",
            return_value="claude-code/linux/local/default",
        ):
            ok, reason, message = tigerkit_state.validate_environment_support()

        self.assertTrue(ok)
        self.assertIsNone(reason)
        self.assertIsNone(message)

    def test_unsupported_environment_is_rejected(self):
        with patch.object(
            tigerkit_state,
            "support_matrix",
            return_value={
                "pluginVersion": PLUGIN_VERSION,
                "environments": [
                    {
                        "environmentKey": "claude-code/linux/local/default",
                        "status": "unsupported",
                        "reason": "not supported here",
                    }
                ],
            },
        ), patch.object(
            tigerkit_state,
            "current_environment_key",
            return_value="claude-code/linux/local/default",
        ):
            ok, reason, message = tigerkit_state.validate_environment_support()

        self.assertFalse(ok)
        self.assertEqual(reason, "hard_enforcement_unavailable")
        self.assertIsNotNone(message)
        text = message or ""
        self.assertIn("unsupported", text)

    def test_missing_environment_entry_is_rejected(self):
        with patch.object(
            tigerkit_state,
            "support_matrix",
            return_value={"pluginVersion": PLUGIN_VERSION, "environments": []},
        ), patch.object(
            tigerkit_state,
            "current_environment_key",
            return_value="claude-code/linux/local/default",
        ):
            ok, reason, message = tigerkit_state.validate_environment_support()

        self.assertFalse(ok)
        self.assertEqual(reason, "hard_enforcement_unavailable")
        self.assertIsNotNone(message)
        text = message or ""
        self.assertIn("No support matrix entry", text)


if __name__ == "__main__":
    unittest.main()
